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
    prompt_parts = []
    
    # Main chat role
    prompt_parts.append("You are a senior code assistant with expertise in software development and code architecture.\n")
    
    # User query
    prompt_parts.append("## User Query")
    prompt_parts.append(f"{user_query}\n")
    
    # Context files
    prompt_parts.append("## Context Files\n")
    prompt_parts.append(f"The following {len(selected_files)} file(s) provide context for this request:\n")
    
    # Add file contents
    for file_path in sorted(selected_files):
        full_path = repo_root / file_path
        if full_path.exists():
            try:
                content = full_path.read_text(errors='ignore')
                prompt_parts.append(f"\n### File: `{file_path}`\n")
                prompt_parts.append(f"```{full_path.suffix[1:] if full_path.suffix else ''}")
                prompt_parts.append(content)
                prompt_parts.append("```\n")
            except Exception as e:
                prompt_parts.append(f"\n### File: `{file_path}`")
                prompt_parts.append(f"_Error reading file: {e}_\n")
        else:
            prompt_parts.append(f"\n### File: `{file_path}`")
            prompt_parts.append("_File not found_\n")
    
    return '\n'.join(prompt_parts)
