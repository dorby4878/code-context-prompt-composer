"""Prompt generation functions for different AI assistants."""

from pathlib import Path
from typing import Set


def generate_copilot_prompt_text(user_query: str, selected_files: Set[str]) -> str:
    """Generate structured prompt for GitHub Copilot following strict rules.
    
    Args:
        user_query: The user's task description
        selected_files: Set of file paths to be modified
        
    Returns:
        Formatted prompt string for GitHub Copilot
    """
    prompt_parts = []
    
    # Role (always include)
    prompt_parts.append("# Role")
    prompt_parts.append("You are a Senior Software Engineer & Reviewer. Work within a minimal diff budget and avoid new dependencies or unrelated changes.\n")
    
    # Task (always include)
    prompt_parts.append("# Task")
    prompt_parts.append(f"{user_query}\n")
    
    # Context (always include - files to modify)
    prompt_parts.append("# Context")
    prompt_parts.append("Primary files to modify:\n")
    for file_path in sorted(selected_files):
        prompt_parts.append(f"- `{file_path}`")
    prompt_parts.append("")
    
    # Plan (always include)
    prompt_parts.append("# Plan")
    prompt_parts.append("1. Review the current implementation in the listed files")
    prompt_parts.append("2. Identify minimal changes needed to fulfill the task")
    prompt_parts.append("3. Apply surgical edits maintaining existing patterns")
    prompt_parts.append("4. Verify changes align with the task goal\n")
    
    # Edits (always include)
    prompt_parts.append("# Edits")
    prompt_parts.append("Provide minimal, surgical changes to the files listed above.")
    prompt_parts.append("Reference exact file paths and line numbers where applicable.")
    prompt_parts.append("Avoid reformatting unrelated code or adding new files.\n")
    
    # Rationale (conditional - include by default)
    prompt_parts.append("# Rationale")
    prompt_parts.append("Explain why each key edit is necessary to achieve the task goal.")
    prompt_parts.append("Keep explanations concise and tied to the specific requirements.\n")
    
    # Verification (conditional - omitted unless criteria exist)
    # Omitted for now as we don't have acceptance criteria
    
    # Default constraints reminder
    prompt_parts.append("# Constraints")
    prompt_parts.append("- Change budget: minimal diff (surgical edits only)")
    prompt_parts.append("- Do not add new dependencies or files")
    prompt_parts.append("- Mirror existing project conventions")
    prompt_parts.append("- Do not add documentation or changelog files unless requested")
    prompt_parts.append("- Do not add docstrings or comments unless necessary for clarity")
    
    return '\n'.join(prompt_parts)


def generate_chatgpt_prompt_text(user_query: str, selected_files: Set[str], repo_root: Path) -> str:
    """Generate a simpler prompt for ChatGPT focused on code questions/suggestions.
    
    Args:
        user_query: The user's task description
        selected_files: Set of file paths to include
        repo_root: Root path of the repository
        
    Returns:
        Formatted prompt string for ChatGPT with file contents
    """
    import re
    
    # Denylist for binary/noisy assets (case-insensitive)
    NOISE_SUFFIXES = {
        '.lock', '.min.js', '.min.css', '.map',
        '.png', '.jpg', '.jpeg', '.gif', '.webp',
        '.pdf', '.zip', '.tar', '.gz', '.tgz', '.xz',
        '.mp4', '.mov', '.avi'
    }
    
    # Size/line limits for truncation
    MAX_FILE_KB = 50
    MAX_FILE_LINES = 800
    HEAD_LINES = 400
    TAIL_LINES = 100
    
    def _is_noisy_asset(file_path: str) -> bool:
        """Check if file should be skipped due to binary/noisy suffix."""
        return any(file_path.lower().endswith(suffix) for suffix in NOISE_SUFFIXES)
    
    def _redact_secrets(content: str) -> str:
        """Redact likely secrets from content (conservative approach).
        
        Assumptions:
        - Uses conservative regexes to avoid false positives
        - Better to slightly over-redact than to leak secrets
        """
        lines = content.split('\n')
        redacted_lines = []
        in_pem_block = False
        
        for line in lines:
            # PEM block detection
            if '-----BEGIN' in line:
                in_pem_block = True
                redacted_lines.append('[REDACTED]')
                continue
            if '-----END' in line:
                in_pem_block = False
                redacted_lines.append('[REDACTED]')
                continue
            if in_pem_block:
                redacted_lines.append('[REDACTED]')
                continue
            
            # Key=value secrets (API_KEY, SECRET, TOKEN)
            if re.search(r'(API_KEY|SECRET|TOKEN)\s*=', line, re.IGNORECASE):
                redacted_lines.append('[REDACTED]')
                continue
            
            # JWT-like tokens (three base64url segments separated by dots)
            if re.match(r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$', line.strip()):
                redacted_lines.append('[REDACTED]')
                continue
            
            redacted_lines.append(line)
        
        return '\n'.join(redacted_lines)
    
    def _truncate_large_content(content: str, line_count: int) -> tuple[str, bool]:
        """Truncate content if it exceeds size limits.
        
        Assumptions:
        - If both size and line limits are exceeded, truncation applies once (head+tail)
        
        Returns:
            (content, was_truncated)
        """
        if line_count <= MAX_FILE_LINES:
            return content, False
        
        lines = content.split('\n')
        head = lines[:HEAD_LINES]
        tail = lines[-TAIL_LINES:]
        truncated = '\n'.join(head) + '\n--- TRUNCATED MIDDLE ---\n' + '\n'.join(tail)
        return truncated, True
    
    prompt_parts = []
    
    # Role with clarified scope
    prompt_parts.append("You are a Senior Software Architecture Consultant. Focus on design guidance, options, and trade-offs. Do not write full implementations unless explicitly requested.\n")
    
    # User query
    prompt_parts.append("## User Query")
    prompt_parts.append(f"{user_query}\n")
    
    # Deterministic response contract (after role and query)
    prompt_parts.append("## What I need from you\n")
    prompt_parts.append("1. **Understanding & Assumptions** (brief)")
    prompt_parts.append("2. **Options & Trade-offs** (2–3)")
    prompt_parts.append("3. **Recommendation** (pick one and justify)")
    prompt_parts.append("4. **High-Level Plan** (3–7 steps)")
    prompt_parts.append("5. **Risks/Edge Cases** (include only if relevant)")
    prompt_parts.append("6. **Quick Checks** (how to validate the design)\n")
    
    # Context files with primary subsection
    prompt_parts.append("## Context Files\n")
    prompt_parts.append(f"The following {len(selected_files)} file(s) provide context for this request:\n")
    prompt_parts.append("### Primary files to consider\n")
    
    # Add file contents with metadata, truncation, and redaction
    for file_path in sorted(selected_files):
        full_path = repo_root / file_path
        
        # Check if noisy asset
        if _is_noisy_asset(file_path):
            prompt_parts.append(f"- `{file_path}` — _Skipped embedding (binary/noisy asset)_\n")
            continue
        
        if not full_path.exists():
            prompt_parts.append(f"\n### File: `{file_path}`")
            prompt_parts.append("_File not found_\n")
            continue
        
        try:
            # Read file and get metadata
            content = full_path.read_text(errors='ignore')
            size_bytes = len(content.encode('utf-8'))
            size_kb = size_bytes / 1024.0
            lines = content.split('\n')
            line_count = len(lines)
            
            # Apply secret redaction
            content = _redact_secrets(content)
            
            # Apply size-based truncation
            was_truncated = False
            if size_kb > MAX_FILE_KB or line_count > MAX_FILE_LINES:
                content, was_truncated = _truncate_large_content(content, line_count)
            
            # File header with metadata
            header = f"### File: `{file_path}` ({line_count} lines, {size_kb:.1f} KB)"
            if was_truncated:
                header += f" — TRUNCATED to first {HEAD_LINES} and last {TAIL_LINES} lines"
            
            prompt_parts.append(f"\n{header}\n")
            prompt_parts.append(f"```{full_path.suffix[1:] if full_path.suffix else ''}")
            prompt_parts.append(content)
            prompt_parts.append("```\n")
            
        except Exception as e:
            prompt_parts.append(f"\n### File: `{file_path}`")
            prompt_parts.append(f"_Error reading file: {e}_\n")
    
    return '\n'.join(prompt_parts)
