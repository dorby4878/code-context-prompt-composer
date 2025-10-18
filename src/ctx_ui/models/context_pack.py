from pydantic import BaseModel, Field
from typing import List
from pathlib import Path
import hashlib
import json


class Snippet(BaseModel):
    """Represents a code snippet with file path and location."""
    path: str
    start: int = 1
    end: int = 9999
    hash: str
    why: str = ''


class ContextPack(BaseModel):
    """A collection of code snippets for a specific task context."""
    version: str = '1'
    task_id: str = ''
    snippets: List[Snippet] = Field(default_factory=list)

    @staticmethod
    def build_from_paths(root: Path, paths: List[str]) -> 'ContextPack':
        """Build a context pack from file paths."""
        snips = []
        for p in paths:
            abs_p = root / p
            try:
                content = abs_p.read_text(errors='ignore')
                h = hashlib.sha256(content.encode()).hexdigest()
                snips.append(Snippet(path=str(p), hash=f'sha256:{h}'))
            except Exception as e:
                print(f"Warning: Could not read {p}: {e}")
        return ContextPack(snippets=snips)

    def save(self, path: Path) -> Path:
        """Save context pack to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.model_dump(), indent=2))
        return path

    @staticmethod
    def load(path: Path) -> 'ContextPack':
        """Load context pack from JSON file."""
        data = json.loads(path.read_text())
        return ContextPack(**data)
