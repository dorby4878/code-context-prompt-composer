from pydantic import BaseModel, Field
from pathlib import Path
from typing import List
import os


class AppConfig(BaseModel):
    """Application configuration."""
    repo_root: Path = Field(default_factory=lambda: Path(os.getenv('CTX_REPO_ROOT', Path.cwd())))
    index_include: List[str] = Field(default_factory=lambda: ['*.py', '*.js', '*.ts', '*.md', '*.yaml', '*.yml', '*.json', '*.txt'])
    index_exclude: List[str] = Field(default_factory=lambda: [
        '.git/**', 
        '.venv/**', 
        'venv/**',
        'node_modules/**', 
        '__pycache__/**',
        '*.pyc',
        'dist/**',
        'build/**'
    ])


class AppState(BaseModel):
    """Application runtime state."""
    config: AppConfig = Field(default_factory=AppConfig)
    current_task: str = ''
    selected_files: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
