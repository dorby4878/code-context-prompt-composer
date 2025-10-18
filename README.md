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

3. **Use the `observe` Script (Recommended for Multiple Projects)**

   The `observe` script allows you to quickly launch the tool for **any project** on your system, without needing to be in this repository.

   a. **Make the script globally accessible**
      
      Add the scripts directory to your PATH by adding this to your `~/.zshrc` or `~/.bashrc`:
      ```bash
      export PATH="$PATH:/Users/yourusername/path/to/code-context-prompt-composer/scripts"
      ```
      
      Or create a symlink in a directory already in your PATH:
      ```bash
      sudo ln -s /Users/yourusername/path/to/code-context-prompt-composer/scripts/observe /usr/local/bin/observe
      ```

   b. **Reload your shell**
      ```bash
      source ~/.zshrc  # or source ~/.bashrc
      ```

### Usage

Navigate to any project and run:
```bash
cd ~/my_project
observe .
```

Or specify a path directly:
```bash
observe ~/my_project
```

Or run from anywhere:
```bash
observe /path/to/any/project
```

The tool will open in your browser showing the file tree for that specific project! 🎯

**How it works**:
- The `observe` script activates the tool's virtual environment
- Launches the app pointing to your target project directory
- Opens the browser automatically at `http://localhost:8080`
- You can now browse and select files from your target project

---

## � Quick Reference

### Launch Commands

```bash
# From the tool's directory (analyzes this project)
./start.sh

# From any project directory (analyzes that project)
cd ~/projects/my-awesome-app
observe .

# Or specify a path from anywhere
observe ~/projects/my-awesome-app
```

---

## �📖 Usage Guide

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
