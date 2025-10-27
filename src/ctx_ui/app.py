"""Code Context & Prompt Composer - Main Application Entry Point."""

from nicegui import ui, app
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ctx_ui.config import AppState, AppConfig
from ctx_ui.ui.views.main_view import main_page
from ctx_ui.watcher.repo_watcher import RepoWatcher


# Global watcher instance
watcher = None


def main():
    """Main application entry point."""
    global watcher
    
    # Initialize configuration
    config = AppConfig()
    config.repo_root = Path.cwd()
    
    state = AppState(config=config)
    
    # Initialize file watcher
    def on_file_change(file_path: Path, event_type: str):
        """Handle file system changes - this will be connected to UI refresh."""
        # Store the last change event in app storage
        if not hasattr(app.storage.general, 'file_changes'):
            app.storage.general['file_changes'] = []
        
        rel_path = file_path.relative_to(config.repo_root)
        app.storage.general['file_changes'].append({
            'path': str(rel_path),
            'type': event_type,
            'timestamp': __import__('time').time()
        })
        
        # Keep only last 100 changes
        if len(app.storage.general['file_changes']) > 100:
            app.storage.general['file_changes'] = app.storage.general['file_changes'][-100:]
    
    # Start watching the repository
    watcher = RepoWatcher(
        repo_path=config.repo_root,
        on_change=on_file_change,
        exclude_patterns=config.index_exclude
    )
    watcher.start()
    
    # Setup shutdown hook
    def shutdown():
        """Cleanup on shutdown."""
        if watcher:
            watcher.stop()
    
    app.on_shutdown(shutdown)
    
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


if __name__ == '__main__':
    main()
