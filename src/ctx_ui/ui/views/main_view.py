"""Main View - Simplified Context File Picker + Prompt Query."""

from nicegui import ui
from pathlib import Path
from typing import List, Dict, Set
from ...context.indexer import list_repo_files
from ...models.context_pack import ContextPack
from ...config import AppState


def build_file_tree(files: List[Path]) -> Dict:
    """Build a hierarchical tree structure from flat file list."""
    tree = {}
    
    for file_path in files:
        parts = file_path.parts
        current = tree
        
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # It's a file
                if '_files' not in current:
                    current['_files'] = []
                current['_files'].append(file_path)
            else:
                # It's a directory
                if part not in current:
                    current[part] = {}
                current = current[part]
    
    return tree


def main_page(state: AppState):
    """Create the main simplified page."""
    
    # Simple header without navigation
    with ui.header().classes('items-center justify-between'):
        ui.label('🧠 Code Context & Prompt Composer').classes('text-xl font-bold')
    
    with ui.column().classes('w-full p-4'):
        ui.label('Context File Picker + Prompt Composer').classes('text-2xl font-bold mb-4')
        
        repo = state.config.repo_root
        files = list_repo_files(repo, state.config.index_include, state.config.index_exclude)
        file_tree = build_file_tree(files)
        
        selected_files: Set[str] = set()
        file_checkboxes: Dict[str, ui.checkbox] = {}
        output_expanded = {'value': False}  # Track expansion state
        
        # Main layout: Left (file browser) + Right (prompt area + output)
        with ui.splitter(value=25).classes('w-full').style('height: calc(100vh - 180px)') as splitter:
            with splitter.before:
                with ui.card().classes('w-full h-full overflow-y-auto p-4'):
                    ui.label('📂 Project Files').classes('text-lg font-bold mb-2')
                    ui.label(f'{len(files)} files found').classes('text-sm text-gray-600 mb-4')
                    
                    # File tree with checkboxes
                    tree_container = ui.column().classes('w-full')
                    
                    def render_tree(tree_node: Dict, parent_path: str = '', level: int = 0):
                        """Recursively render the file tree."""
                        indent = '  ' * level
                        
                        # Render directories first
                        for key in sorted(tree_node.keys()):
                            if key == '_files':
                                continue
                            
                            dir_path = f"{parent_path}/{key}" if parent_path else key
                            
                            with ui.expansion(key, icon='folder').classes('w-full').props('dense'):
                                render_tree(tree_node[key], dir_path, level + 1)
                        
                        # Render files
                        if '_files' in tree_node:
                            for file_path in sorted(tree_node['_files']):
                                file_str = str(file_path)
                                
                                with ui.row().classes('w-full items-center gap-2'):
                                    checkbox = ui.checkbox('', value=False, on_change=lambda e, f=file_str: toggle_file(f, e.value))
                                    file_checkboxes[file_str] = checkbox
                                    ui.label(file_path.name).classes('text-sm')
                    
                    with tree_container:
                        render_tree(file_tree)
            
            with splitter.after:
                with ui.card().classes('w-full h-full p-4').style('display: flex; flex-direction: column; overflow: hidden;'):
                    ui.label('✍️ Your Query').classes('text-lg font-bold mb-2')
                    
                    # Selected files summary
                    with ui.row().classes('w-full items-center justify-between gap-2 mb-2'):
                        selected_count = ui.label('0 files selected').classes('text-sm font-semibold text-gray-700')
                        ui.button('Clear All', on_click=lambda: clear_all_selections(), icon='clear').props('flat dense size=sm')
                    
                    # Selected files list (collapsible)
                    selected_files_container = ui.column().classes('w-full mb-2').style('max-height: 100px; overflow-y: auto; flex-shrink: 0;')
                    
                    # User query input
                    user_query = ui.textarea(
                        label='Describe the change or refactor you want to make',
                        placeholder='E.g., "Refactor the authentication module to use JWT tokens instead of sessions"'
                    ).classes('w-full mb-2').props('outlined').style('min-height: 120px; max-height: 150px; flex-shrink: 0;')
                    
                    # Action buttons
                    with ui.row().classes('w-full gap-2 mb-2').style('flex-shrink: 0;'):
                        ui.button(
                            '🤖 Generate Copilot Prompt',
                            on_click=lambda: generate_copilot_prompt(),
                            icon='smart_toy'
                        ).props('color=primary')
                        ui.button(
                            '💬 Generate ChatGPT Prompt',
                            on_click=lambda: generate_chatgpt_prompt(),
                            icon='chat'
                        ).props('color=secondary')
                        ui.button(
                            '🔄 Start Fresh',
                            on_click=lambda: start_fresh(),
                            icon='refresh'
                        ).props('color=warning outline')
                    
                    # Output area - with expand/collapse
                    with ui.row().classes('w-full items-center justify-between mb-2').style('flex-shrink: 0;'):
                        ui.label('📝 Output').classes('text-lg font-bold')
                        expand_button = ui.button(
                            icon='unfold_more',
                            on_click=lambda: toggle_output_expansion()
                        ).props('flat dense').tooltip('Expand output area')
                    
                    # Output area container with flexible height
                    with ui.column().classes('w-full').style('flex: 1 1 auto; min-height: 0; overflow: hidden;'):
                        output_area = ui.textarea(value='').classes('w-full font-mono text-sm').props('readonly outlined').style('height: 100%; min-height: 200px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word;')
                    
                    # Copy button container (shown after prompt generation)
                    copy_container = ui.row().classes('w-full gap-2 mt-2').style('flex-shrink: 0;')
        
        def toggle_output_expansion():
            """Toggle output area between normal and expanded view."""
            if output_expanded['value']:
                # Collapse - restore flexible sizing
                output_area.style('height: 100%; min-height: 200px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word;')
                user_query.style('min-height: 120px; max-height: 150px; flex-shrink: 0;')
                expand_button.props('icon=unfold_more')
                expand_button.tooltip('Expand output area')
                output_expanded['value'] = False
                ui.notify('Output collapsed to normal size', type='info')
            else:
                # Expand - minimize query area, maximize output
                output_area.style('height: 100%; min-height: 400px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word;')
                user_query.style('min-height: 80px; max-height: 80px; flex-shrink: 0;')
                expand_button.props('icon=unfold_less')
                expand_button.tooltip('Collapse output area')
                output_expanded['value'] = True
                ui.notify('Output expanded - more space for output', type='info')
        
        def toggle_file(file_path: str, checked: bool):
            """Toggle file selection."""
            if checked:
                selected_files.add(file_path)
            else:
                selected_files.discard(file_path)
            update_selected_count()
        
        def clear_all_selections():
            """Clear all selected files."""
            selected_files.clear()
            for checkbox in file_checkboxes.values():
                checkbox.value = False
            update_selected_count()
            ui.notify('Cleared all selections', type='info')
        
        def update_selected_count():
            """Update the selected files count and list."""
            count = len(selected_files)
            selected_count.text = f'{count} file(s) selected'
            
            # Update the selected files list
            selected_files_container.clear()
            if count > 0:
                with selected_files_container:
                    for file_path in sorted(selected_files):
                        with ui.row().classes('w-full items-center gap-1'):
                            ui.icon('description', size='xs').classes('text-blue-600')
                            ui.label(file_path).classes('text-xs text-gray-700')
        
        def start_fresh():
            """Clear everything and start fresh."""
            # Clear selected files
            selected_files.clear()
            for checkbox in file_checkboxes.values():
                checkbox.value = False
            update_selected_count()
            
            # Clear user query
            user_query.value = ''
            
            # Clear output
            output_area.value = ''
            
            # Clear copy button
            copy_container.clear()
            
            ui.notify('✓ Cleared all - starting fresh!', type='info')
        
        def _validate_inputs():
            """Validate user inputs for prompt generation."""
            if not user_query.value.strip():
                ui.notify('Please enter a query', type='warning')
                return False
            
            if not selected_files:
                ui.notify('Please select at least one file', type='warning')
                return False
                
            return True
        
        def _get_file_contents():
            """Get the contents of all selected files."""
            file_contents_list = []
            
            for file_path in sorted(selected_files):
                full_path = repo / file_path
                if full_path.exists():
                    try:
                        content = full_path.read_text(errors='ignore')
                        file_contents_list.append(f"\n### File: `{file_path}`\n")
                        file_contents_list.append(f"```{full_path.suffix[1:] if full_path.suffix else ''}")
                        file_contents_list.append(content)
                        file_contents_list.append("```\n")
                    except Exception as e:
                        file_contents_list.append(f"\n### File: `{file_path}`")
                        file_contents_list.append(f"_Error reading file: {e}_\n")
                else:
                    file_contents_list.append(f"\n### File: `{file_path}`")
                    file_contents_list.append("_File not found_\n")
            
            return file_contents_list
        
        def generate_copilot_prompt():
            """Generate the full detailed prompt for GitHub Copilot (same as the original functionality)."""
            if not _validate_inputs():
                return
            
            prompt_parts = []
            
            prompt_parts.append("# AI Coding Assistant Prompt\n")
            prompt_parts.append("## Task Description")
            prompt_parts.append(f"{user_query.value}\n")
            
            prompt_parts.append("## Context Files\n")
            prompt_parts.append(f"The following {len(selected_files)} file(s) are relevant to this task:\n")
            
            # Add file contents
            prompt_parts.extend(_get_file_contents())
            
            prompt_parts.append("\n## Instructions\n")
            prompt_parts.append("Please analyze the provided code and implement the requested changes following these guidelines:\n")
            prompt_parts.append("1. **Understand** the current implementation in the provided files")
            prompt_parts.append("2. **Plan** the changes needed to fulfill the request")
            prompt_parts.append("3. **Implement** the changes with clear, maintainable code")
            prompt_parts.append("4. **Explain** your changes and reasoning")
            prompt_parts.append("5. **Consider** edge cases, error handling, and best practices")
            prompt_parts.append("6. **Do not** add .md files of logchange file unsless you asked specifically for it")
            prompt_parts.append("\n---\n")
            prompt_parts.append("**Ready to assist!** Please provide the implementation with step-by-step explanations.")
            
            # Set output value
            prompt_text = '\n'.join(prompt_parts)
            output_area.value = prompt_text
            
            # Show copy button
            copy_container.clear()
            with copy_container:
                ui.button(
                    '📋 Copy Copilot Prompt',
                    on_click=lambda: copy_prompt('Copilot'),
                    icon='content_copy'
                ).props('color=primary')
            
            ui.notify('✓ Copilot prompt generated! Copy and use with GitHub Copilot', type='positive', timeout=5000)
        
        def generate_chatgpt_prompt():
            """Generate a simpler prompt for ChatGPT focused on code questions/suggestions."""
            if not _validate_inputs():
                return
            
            prompt_parts = []
            
            # Main chat role
            prompt_parts.append("You are a senior code assistant with expertise in software development and code architecture.\n")
            
            # User query
            prompt_parts.append("## User Query")
            prompt_parts.append(f"{user_query.value}\n")
            
            # Context files
            prompt_parts.append("## Context Files\n")
            prompt_parts.append(f"The following {len(selected_files)} file(s) provide context for this request:\n")
            
            # Add file contents
            prompt_parts.extend(_get_file_contents())
            
            # Set output value
            prompt_text = '\n'.join(prompt_parts)
            output_area.value = prompt_text
            
            # Show copy button
            copy_container.clear()
            with copy_container:
                ui.button(
                    '📋 Copy ChatGPT Prompt',
                    on_click=lambda: copy_prompt('ChatGPT'),
                    icon='content_copy'
                ).props('color=secondary')
            
            ui.notify('✓ ChatGPT prompt generated! Copy and use with ChatGPT', type='positive', timeout=5000)
        
        def copy_prompt(prompt_type: str):
            """Copy the prompt to clipboard."""
            if not output_area.value:
                ui.notify('No prompt to copy', type='warning')
                return
            
            ui.run_javascript(f'''
                navigator.clipboard.writeText({repr(output_area.value)});
            ''')
            ui.notify(f'✓ {prompt_type} prompt copied to clipboard', type='positive')
