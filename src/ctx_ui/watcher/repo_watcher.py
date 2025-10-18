"""Background repository watcher - monitors file changes and git events."""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from pathlib import Path
from typing import Callable, List
import subprocess
import time
import hashlib


class RepoWatcher(FileSystemEventHandler):
    """Watch repository for file system changes."""
    
    def __init__(
        self,
        repo_path: Path,
        on_change: Callable[[Path, str], None],
        exclude_patterns: List[str] = None
    ):
        self.repo_path = repo_path
        self.on_change = on_change
        self.exclude_patterns = exclude_patterns or []
        self.observer = None
    
    def should_ignore(self, path: str) -> bool:
        """Check if path should be ignored."""
        import fnmatch
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        return False
    
    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if self.should_ignore(str(path.relative_to(self.repo_path))):
            return
        
        self.on_change(path, 'modified')
    
    def on_created(self, event: FileSystemEvent):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if self.should_ignore(str(path.relative_to(self.repo_path))):
            return
        
        self.on_change(path, 'created')
    
    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion events."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if self.should_ignore(str(path.relative_to(self.repo_path))):
            return
        
        self.on_change(path, 'deleted')
    
    def start(self):
        """Start watching the repository."""
        self.observer = Observer()
        self.observer.schedule(self, str(self.repo_path), recursive=True)
        self.observer.start()
    
    def stop(self):
        """Stop watching the repository."""
        if self.observer:
            self.observer.stop()
            self.observer.join()


class GitIntegration:
    """Git integration for tracking repository state."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
    
    def is_git_repo(self) -> bool:
        """Check if directory is a git repository."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_current_branch(self) -> str:
        """Get current git branch name."""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception:
            return 'unknown'
    
    def get_latest_commit(self) -> str:
        """Get latest commit hash."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception:
            return 'unknown'
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files (unstaged + staged)."""
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return [f for f in result.stdout.strip().split('\n') if f]
        except Exception:
            return []
    
    def get_file_history(self, file_path: str, limit: int = 10) -> List[dict]:
        """Get commit history for a specific file."""
        try:
            result = subprocess.run(
                ['git', 'log', '--pretty=format:%H|%an|%at|%s', f'-{limit}', '--', file_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            history = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split('|', 3)
                if len(parts) == 4:
                    history.append({
                        'commit': parts[0],
                        'author': parts[1],
                        'timestamp': int(parts[2]),
                        'message': parts[3]
                    })
            return history
        except Exception:
            return []


def compute_file_hash(file_path: Path) -> str:
    """Compute SHA-256 hash of file contents."""
    try:
        content = file_path.read_bytes()
        return f"sha256:{hashlib.sha256(content).hexdigest()}"
    except Exception:
        return "error"
