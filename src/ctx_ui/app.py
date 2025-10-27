"""Code Context & Prompt Composer - Main Application Entry Point."""

from nicegui import ui
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ctx_ui.config import AppState, AppConfig
from ctx_ui.ui.views.main_view import main_page


def main():
    """Main application entry point."""
    # Initialize configuration
    config = AppConfig()
    config.repo_root = Path.cwd()
    
    state = AppState(config=config)
    
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
