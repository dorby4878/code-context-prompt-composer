"""Code Context & Prompt Composer - Main Application Entry Point."""

from nicegui import ui
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ctx_ui.config import AppState, AppConfig
from ctx_ui.ui.views.main_view import main_page
from ctx_ui.storage.store import MetadataStore
from ctx_ui.watcher.repo_watcher import RepoWatcher, GitIntegration, compute_file_hash


def main():
    """Main application entry point."""
    # Initialize configuration
    config = AppConfig()
    config.repo_root = Path.cwd()
    config.ensure_directories()
    
    state = AppState(config=config)
    
    # Initialize storage
    metadata_store = MetadataStore(config.db_path)
    
    # Initialize git integration
    git = GitIntegration(config.repo_root)
    if git.is_git_repo():
        print(f"✓ Git repository detected: {git.get_current_branch()}")
    
    # Initialize file watcher
    def on_file_change(path: Path, event_type: str):
        """Handle file change events."""
        if event_type == 'deleted':
            return
        
        try:
            rel_path = path.relative_to(config.repo_root)
            file_hash = compute_file_hash(path)
            size = path.stat().st_size
            metadata_store.index_file(str(rel_path), file_hash, size)
            print(f"Indexed: {rel_path} ({event_type})")
        except Exception as e:
            print(f"Error indexing {path}: {e}")
    
    watcher = RepoWatcher(
        config.repo_root,
        on_file_change,
        exclude_patterns=config.index_exclude
    )
    watcher.start()
    print("✓ File watcher started")
    
    # Setup routes
    @ui.page('/')
    def index():
        main_page(state)
    
    # Configure UI
    ui.run(
        title='Code Context & Prompt Composer',
        port=8080,
        show=True,
        reload=False,
        dark=None
    )
    
    # Cleanup
    watcher.stop()


if __name__ == '__main__':
    main()
