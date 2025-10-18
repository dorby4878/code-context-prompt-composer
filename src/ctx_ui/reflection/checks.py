"""Reflection checks - scope guards, secrets scanning, and validation."""

from pathlib import Path
from typing import List, Dict, Any
import re


class ScopeGuard:
    """Check if changes are within expected scope."""
    
    def __init__(self, allowed_paths: List[str], excluded_paths: List[str]):
        self.allowed_paths = allowed_paths
        self.excluded_paths = excluded_paths
    
    def check_file(self, file_path: str) -> tuple[bool, str]:
        """Check if file is within allowed scope."""
        path = Path(file_path)
        
        # Check excluded patterns
        for pattern in self.excluded_paths:
            if path.match(pattern):
                return False, f"File matches excluded pattern: {pattern}"
        
        # Check allowed patterns
        if not self.allowed_paths:
            return True, "No scope restrictions"
        
        for pattern in self.allowed_paths:
            if path.match(pattern):
                return True, "File is within allowed scope"
        
        return False, "File is outside allowed scope"


class SecretsScanner:
    """Simple secrets scanner to detect potential sensitive data."""
    
    # Common patterns for secrets
    PATTERNS = {
        'api_key': re.compile(r'(?i)api[_-]?key["\s:=]+["\']?([a-zA-Z0-9_\-]{20,})["\']?'),
        'password': re.compile(r'(?i)password["\s:=]+["\']?([^\s"\']{8,})["\']?'),
        'token': re.compile(r'(?i)token["\s:=]+["\']?([a-zA-Z0-9_\-]{20,})["\']?'),
        'secret': re.compile(r'(?i)secret["\s:=]+["\']?([a-zA-Z0-9_\-]{20,})["\']?'),
        'private_key': re.compile(r'-----BEGIN (RSA |EC )?PRIVATE KEY-----'),
        'aws_key': re.compile(r'AKIA[0-9A-Z]{16}'),
    }
    
    def scan_text(self, text: str) -> List[Dict[str, Any]]:
        """Scan text for potential secrets."""
        findings = []
        
        for secret_type, pattern in self.PATTERNS.items():
            matches = pattern.finditer(text)
            for match in matches:
                findings.append({
                    'type': secret_type,
                    'line': text[:match.start()].count('\n') + 1,
                    'snippet': match.group(0)[:50] + '...' if len(match.group(0)) > 50 else match.group(0)
                })
        
        return findings
    
    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan file for potential secrets."""
        try:
            text = file_path.read_text(errors='ignore')
            findings = self.scan_text(text)
            for finding in findings:
                finding['file'] = str(file_path)
            return findings
        except Exception:
            return []


class JsonSchemaDiffer:
    """Compare JSON schemas to detect breaking changes."""
    
    @staticmethod
    def diff_schemas(old_schema: Dict[str, Any], new_schema: Dict[str, Any]) -> List[str]:
        """Compare two JSON schemas and return list of changes."""
        changes = []
        
        # Check for removed required fields
        old_required = set(old_schema.get('required', []))
        new_required = set(new_schema.get('required', []))
        removed_required = old_required - new_required
        added_required = new_required - old_required
        
        if removed_required:
            changes.append(f"Removed required fields: {', '.join(removed_required)}")
        if added_required:
            changes.append(f"Added required fields: {', '.join(added_required)}")
        
        # Check for removed properties
        old_props = set(old_schema.get('properties', {}).keys())
        new_props = set(new_schema.get('properties', {}).keys())
        removed_props = old_props - new_props
        added_props = new_props - old_props
        
        if removed_props:
            changes.append(f"Removed properties: {', '.join(removed_props)}")
        if added_props:
            changes.append(f"Added properties: {', '.join(added_props)}")
        
        # Check for type changes in common properties
        common_props = old_props & new_props
        for prop in common_props:
            old_type = old_schema['properties'][prop].get('type')
            new_type = new_schema['properties'][prop].get('type')
            if old_type != new_type:
                changes.append(f"Type changed for '{prop}': {old_type} -> {new_type}")
        
        return changes


def run_reflection_checks(files: List[Path], context_dir: Path) -> Dict[str, Any]:
    """Run all reflection checks on given files."""
    results = {
        'scope_violations': [],
        'secrets_found': [],
        'schema_changes': []
    }
    
    # Initialize checkers
    scope_guard = ScopeGuard(
        allowed_paths=['src/**', 'tests/**', 'docs/**'],
        excluded_paths=['**/.git/**', '**/node_modules/**', '**/__pycache__/**']
    )
    
    secrets_scanner = SecretsScanner()
    
    # Run checks
    for file_path in files:
        # Scope check
        is_valid, message = scope_guard.check_file(str(file_path))
        if not is_valid:
            results['scope_violations'].append({'file': str(file_path), 'reason': message})
        
        # Secrets scan
        findings = secrets_scanner.scan_file(file_path)
        results['secrets_found'].extend(findings)
    
    return results
