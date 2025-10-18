from pydantic import BaseModel, Field
from pathlib import Path
from typing import List
import os


class AppConfig(BaseModel):
    """Application configuration."""
    repo_root: Path = Field(default_factory=lambda: Path(os.getenv('CTX_REPO_ROOT', Path.cwd())))
    db_path: Path = Field(default=Path('.ctx/metadata.db'))
    index_include: List[str] = Field(default_factory=lambda: ['*.py', '*.js', '*.ts', '*.md', '*.yaml', '*.yml', '*.json', '*.txt'])
    index_exclude: List[str] = Field(default_factory=lambda: [
        '.git/**', 
        '.venv/**', 
        'venv/**',
        'node_modules/**', 
        '__pycache__/**',
        '*.pyc',
        '.ctx/**',
        'dist/**',
        'build/**'
    ])
    tasks_dir: Path = Field(default=Path('.ctx/tasks'))
    context_packs_dir: Path = Field(default=Path('.ctx'))
    prompt_templates_dir: Path = Field(default=Path('.ctx/templates'))
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for dir_path in [self.tasks_dir, self.context_packs_dir, self.prompt_templates_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


class AppState(BaseModel):
    """Application runtime state."""
    config: AppConfig = Field(default_factory=AppConfig)
    current_task: str = ''
    selected_files: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
