from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from pathlib import Path
import yaml
from datetime import datetime


class TaskCard(BaseModel):
    """Task card defining an AI-assisted development task."""
    id: str
    title: str
    description: str = ''
    context_pack: Optional[str] = None
    prompt_template: str = 'default'
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def save(self, path: Path) -> Path:
        """Save task card to YAML file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        self.updated_at = datetime.utcnow().isoformat()
        path.write_text(yaml.dump(self.model_dump(), default_flow_style=False, sort_keys=False))
        return path

    @staticmethod
    def load(path: Path) -> 'TaskCard':
        """Load task card from YAML file."""
        data = yaml.safe_load(path.read_text())
        return TaskCard(**data)
