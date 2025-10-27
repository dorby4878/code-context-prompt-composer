# 🧠 Code Context & Prompt Composer

A streamlined web-based tool designed to help developers efficiently gather and organize code context for AI coding assistants like ChatGPT, GitHub Copilot, or Claude. **Now with live file monitoring** to automatically track changes as you work!

## 🎯 What Does It Do?

When working with AI coding assistants on complex refactoring or implementation tasks, you often need to provide relevant code files as context. **Code Context & Prompt Composer** simplifies this workflow by:

1. **📂 Browsing your project files** in an intuitive tree view
2. **✅ Selecting relevant files** with simple checkboxes
3. **✍️ Describing your task** in natural language
4. **📋 Generating a well-formatted prompt** with all selected file contents
5. **📤 Copying to clipboard** ready to paste into your AI assistant
6. **🔴 Live monitoring** - automatically detects file changes in your project and refreshes the file tree

No more manually copying and pasting multiple files, no more losing track of which files you've included - just select, describe, and generate. The tool stays in sync with your project as you code!

---

## ✨ Features

- **Interactive File Browser**: Navigate your project structure with a collapsible tree view
- **Smart File Selection**: Checkbox interface to select/deselect files easily
- **Context Preview**: See exactly which files you've selected at a glance
- **Dual Prompt Generation**: 
  - **🤖 Copilot Prompt**: Structured format with strict rules for minimal, surgical changes (Role/Task/Context/Plan/Edits/Rationale/Constraints)
  - **💬 ChatGPT Prompt**: Architecture-focused guidance with full file contents, design options, and trade-offs analysis
- **Live File Monitoring** 🔴: Automatically detects when files are created, modified, or deleted in your project
- **Auto-Refresh**: File tree updates in real-time as you make changes (checks every 2 seconds)
- **Change Notifications**: Get notified when files change while you work
- **Manual Refresh**: Force immediate refresh with the refresh button in the header
- **Copy to Clipboard**: One-click copy of the entire context
- **Start Fresh**: Quick reset button to begin a new task
- **Expandable Output**: Toggle between normal and expanded view for long prompts
- **File Filtering**: Respects `.gitignore` patterns (configurable)
- **Noise Filtering**: Automatically skips binary/noisy files (.lock, .min.js, .png, etc.)
- **Secret Redaction**: Automatically redacts API keys, tokens, and PEM blocks from file contents
- **Smart Truncation**: Large files are truncated (first 400 + last 100 lines) to keep prompts manageable

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **Git** (to clone the repository)
- A code project you want to work with

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/code-context-prompt-composer.git
   cd code-context-prompt-composer
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
- **Live file monitoring is automatically enabled** - the tool tracks changes as you code
- **No files are created in your project** - the tool is read-only (only watches)

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
   - **New**: The file tree automatically refreshes when files change!

2. **Describe Your Task**
   - In the "Your Query" text area, describe what you want to accomplish
   - Be specific: "Refactor the authentication module to use JWT tokens"
   - Or ask for design guidance: "What are the options for implementing caching here?"

3. **Generate Prompt**
   - Choose between two prompt formats:
     - **🤖 Generate Copilot Prompt**: Structured prompt with strict rules for minimal, surgical changes
       - Lists file names only (no full contents)
       - Includes Role, Task, Context, Plan, Edits, Rationale, and Constraints sections
       - Optimized for GitHub Copilot's surgical editing workflow
     
     - **💬 Generate ChatGPT Prompt**: Architecture consultant prompt with full context
       - Includes complete file contents (with smart truncation for large files)
       - Requests: Understanding, Options & Trade-offs, Recommendation, High-Level Plan, Risks, and Validation steps
       - Automatically redacts secrets (API keys, tokens, PEM blocks)
       - Skips binary/noisy files (.lock, .min.js, .png, etc.)
       - Shows file metadata (line count, size in KB)
   
   - The tool validates you have files selected and a query entered
   - A formatted prompt appears in the output area optimized for the chosen AI assistant

4. **Copy & Use**
   - Click the appropriate copy button for your chosen format:
     - **📋 Copy Copilot Prompt** for GitHub Copilot
     - **📋 Copy ChatGPT Prompt** for ChatGPT or Claude
   - Paste into your AI assistant of choice
   - Get intelligent, context-aware responses!

5. **Start Fresh**
   - Click "🔄 Start Fresh" to clear everything and begin a new task
   - This clears: selected files, query text, and output

### Live Monitoring Features

The tool now includes **real-time file monitoring** to keep your context up-to-date as you work:

- **Automatic Detection**: The tool watches your project directory for any file changes
- **Auto-Refresh**: File tree updates automatically every 2 seconds when changes are detected
- **Change Notifications**: You'll see notifications in the top-right when files are created, modified, or deleted
- **Live Status Indicator**: Look for the green sensor icon (🟢) in the header - it means monitoring is active
- **Manual Refresh**: Click the refresh button (🔄) in the header to force an immediate update
- **Smart Preservation**: Your file selections are preserved when the tree refreshes (except for deleted files)

**Example Workflow with Live Monitoring:**
1. Launch the tool with `observe ~/my-project`
2. Select relevant files for your refactoring task
3. Start editing files in your IDE
4. The tool automatically detects changes and updates the file tree
5. You see which files were modified without leaving the tool
6. Generate updated prompts that reflect your latest changes

### Tips & Best Practices

- **Select only relevant files**: More context isn't always better. Focus on files directly related to your task.
- **Be specific in your query**: Clear descriptions lead to better AI responses.
- **Use the expand button**: Click the expand icon (⬍) next to "Output" for more space when viewing long prompts.
- **Clear selections carefully**: Use "Clear All" next to the file count to deselect all files at once.
- **Leverage live monitoring**: Keep the tool open while coding to track which files you're actively changing.
- **Use Copilot prompts for implementation**: When you know exactly what to change, use the Copilot prompt format.
- **Use ChatGPT prompts for design**: When you need architecture advice or want to explore options, use the ChatGPT format.
- **Watch file notifications**: They help you catch unintended changes or verify your edits were detected.
- **Manual refresh when needed**: If you make rapid changes, click refresh to ensure the tree is current before generating a prompt.
