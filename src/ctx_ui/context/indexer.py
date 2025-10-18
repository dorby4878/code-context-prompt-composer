from pathlib import Path
import fnmatch
from typing import List


def list_repo_files(root: Path, include: List[str], exclude: List[str]) -> List[Path]:
    """
    List all files in repository matching include patterns and not matching exclude patterns.
    
    Args:
        root: Repository root path
        include: List of glob patterns to include (e.g., ['*.py', '*.js'])
        exclude: List of glob patterns to exclude (e.g., ['node_modules/**', '.git/**'])
    
    Returns:
        Sorted list of relative file paths
    """
    all_files = []
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        
        rel = p.relative_to(root)
        rel_str = str(rel)
        
        # Check exclude patterns first
        if any(fnmatch.fnmatch(rel_str, ex) for ex in exclude):
            continue
        
        # Check include patterns
        if include and any(fnmatch.fnmatch(rel_str, inc) for inc in include):
            all_files.append(rel)
        elif not include:  # If no include patterns, include all non-excluded
            all_files.append(rel)
    
    return sorted(all_files)
