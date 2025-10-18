"""UI layout components and utilities."""

from nicegui import ui


def page_header(title: str, subtitle: str = ''):
    """Create a standard page header."""
    with ui.row().classes('w-full items-center mb-4 pb-4 border-b'):
        ui.label(title).classes('text-2xl font-bold')
        if subtitle:
            ui.label(subtitle).classes('text-gray-600 ml-4')


def simple_header():
    """Create a simple header without navigation (single page app)."""
    with ui.header().classes('items-center justify-between'):
        ui.label('🧠 Code Context & Prompt Composer').classes('text-xl font-bold')
