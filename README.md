# 🧠 Code Context & Prompt Composer

A streamlined web-based tool designed to help developers efficiently gather and organize code context for AI coding assistants like ChatGPT, GitHub Copilot, or Claude.

## 🎯 What Does It Do?

When working with AI coding assistants on complex refactoring or implementation tasks, you often need to provide relevant code files as context. **Code Context & Prompt Composer** simplifies this workflow by:

1. **📂 Browsing your project files** in an intuitive tree view
2. **✅ Selecting relevant files** with simple checkboxes
3. **✍️ Describing your task** in natural language
4. **📋 Generating a well-formatted prompt** with all selected file contents
5. **📤 Copying to clipboard** ready to paste into your AI assistant

No more manually copying and pasting multiple files, no more losing track of which files you've included - just select, describe, and generate.

---

## ✨ Features

- **Interactive File Browser**: Navigate your project structure with a collapsible tree view
- **Smart File Selection**: Checkbox interface to select/deselect files easily
- **Context Preview**: See exactly which files you've selected at a glance
- **Prompt Generation**: Automatically formats your files into a structured prompt
- **Copy to Clipboard**: One-click copy of the entire context
- **Start Fresh**: Quick reset button to begin a new task
- **Expandable Output**: Toggle between normal and expanded view for long prompts
- **File Filtering**: Respects `.gitignore` patterns (configurable)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **Git** (to clone the repository)
- A code project you want to work with

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai_context_orchestrator.git
   cd ai_context_orchestrator
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   
   This script will:
   - Create a Python virtual environment
   - Install all required dependencies
   - Set up the project structure

3. **Configure your project path** (optional)
   
   Edit `src/ctx_ui/config.py` to point to your target repository:
   ```python
   repo_root = Path("/path/to/your/project")
   ```
   
   Or it will default to the current repository.

### Running the Application

1. **Start the web interface**
   ```bash
   ./start.sh
   ```
   
   Or manually:
   ```bash
   source venv/bin/activate
   python -m src.ctx_ui.app
   ```

2. **Open your browser**
   
   Navigate to: `http://localhost:8080`

3. **Start using the tool!**
   - Browse your project files in the left panel
   - Select files by checking the boxes
   - Describe your task in the query field
   - Click "Generate Full Prompt"
   - Copy the generated prompt and paste into your AI assistant

---

## 📖 Usage Guide

### Basic Workflow

1. **Select Files**
   - Use the left panel to browse your project structure
   - Click the folders to expand/collapse directories
   - Check the boxes next to files you want to include as context
   - See the selected file count update in real-time

2. **Describe Your Task**
   - In the "Your Query" text area, describe what you want to accomplish
   - Be specific: "Refactor the authentication module to use JWT tokens"
   - Or ask questions: "How can I improve the error handling in these files?"

3. **Generate Prompt**
   - Click "✅ Generate Full Prompt"
   - The tool validates you have files selected and a query entered
   - A formatted prompt appears in the output area with:
     - Your task description
     - All selected file contents with syntax highlighting markers
     - Clear instructions for the AI assistant

4. **Copy & Use**
   - Click "📋 Copy Full Prompt" to copy everything to your clipboard
   - Paste into ChatGPT, Claude, or your AI assistant of choice
   - Get intelligent, context-aware responses!

5. **Start Fresh**
   - Click "🔄 Start Fresh" to clear everything and begin a new task
   - This clears: selected files, query text, and output

### Tips & Best Practices

- **Select only relevant files**: More context isn't always better. Focus on files directly related to your task.
- **Be specific in your query**: Clear descriptions lead to better AI responses.
- **Use the expand button**: Click the expand icon (⬍) next to "Output" for more space when viewing long prompts.
- **Clear selections carefully**: Use "Clear All" next to the file count to deselect all files at once.

---

## ⚙️ Configuration

### File Filtering

Edit `src/ctx_ui/config.py` to customize which files are indexed:

```python
index_include = [
    "**/*.py",      # Python files
    "**/*.js",      # JavaScript files
    "**/*.ts",      # TypeScript files
    "**/*.jsx",     # React files
    "**/*.tsx",     # React TypeScript files
    "**/*.vue",     # Vue files
    "**/*.html",    # HTML files
    "**/*.css",     # CSS files
    "**/*.md",      # Markdown files
]

index_exclude = [
    "**/node_modules/**",
    "**/__pycache__/**",
    "**/venv/**",
    "**/.venv/**",
    "**/dist/**",
    "**/build/**",
    "**/.git/**",
]
```

### Port Configuration

By default, the app runs on port `8080`. To change this, edit `src/ctx_ui/app.py`:

```python
ui.run(port=8080)  # Change to your preferred port
```

---

## 🏗️ Project Structure

```
ai_context_orchestrator/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── setup.sh                   # Setup script
├── start.sh                   # Launch script
├── src/
│   └── ctx_ui/
│       ├── app.py            # Main application entry point
│       ├── config.py         # Configuration settings
│       ├── context/
│       │   └── indexer.py    # File indexing logic
│       ├── models/
│       │   ├── context_pack.py
│       │   └── task_card.py
│       ├── storage/
│       │   └── store.py
│       └── ui/
│           └── views/
│               └── main_view.py  # Main UI implementation
└── tests/
    ├── test_context_pack.py
    └── test_indexer.py
```

---

## 🛠️ Development

### Running Tests

```bash
source venv/bin/activate
python -m pytest tests/
```

### Adding New Features

The main UI logic is in `src/ctx_ui/ui/views/main_view.py`. Key components:

- `build_file_tree()`: Builds the hierarchical file structure
- `render_tree()`: Renders the interactive file tree
- `generate_full_prompt()`: Creates the AI-ready prompt
- `start_fresh()`: Resets the interface

### Dependencies

- **NiceGUI**: Modern Python UI framework (web-based)
- **pathlib**: File path handling
- Standard library modules for file operations

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🐛 Troubleshooting

### Port Already in Use

If port 8080 is already in use:
```bash
# Find and kill the process using port 8080
lsof -ti:8080 | xargs kill -9
```

Or change the port in `src/ctx_ui/app.py`.

### Virtual Environment Issues

If you encounter issues with the virtual environment:
```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Files Not Showing Up

Check your `index_include` and `index_exclude` patterns in `src/ctx_ui/config.py`. Make sure your file types are included and not accidentally excluded.

---

## 💡 Use Cases

- **Refactoring**: Select related files and describe the refactoring you want
- **Bug Fixes**: Include the buggy files and describe the issue
- **Feature Implementation**: Select relevant modules and describe the new feature
- **Code Review**: Get AI analysis of specific files
- **Documentation**: Generate documentation for selected code files
- **Learning**: Ask questions about how specific parts of your codebase work

---

## 📧 Support

If you encounter issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above

---

## 🙏 Acknowledgments

Built with [NiceGUI](https://nicegui.io/) - a wonderful Python UI framework that makes building web interfaces a breeze!

---

**Happy Coding! 🚀**
