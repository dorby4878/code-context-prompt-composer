"""Tests for context pack functionality."""

import pytest
from pathlib import Path
from src.ctx_ui.models.context_pack import ContextPack, Snippet


def test_snippet_creation():
    """Test creating a snippet."""
    snippet = Snippet(
        path='src/test.py',
        hash='sha256:abc123',
        why='Main implementation file'
    )
    assert snippet.path == 'src/test.py'
    assert snippet.start == 1
    assert snippet.end == 9999
    assert snippet.hash == 'sha256:abc123'


def test_context_pack_creation():
    """Test creating a context pack."""
    pack = ContextPack(
        version='1',
        task_id='test-task',
        snippets=[
            Snippet(path='file1.py', hash='sha256:123'),
            Snippet(path='file2.py', hash='sha256:456')
        ]
    )
    assert len(pack.snippets) == 2
    assert pack.task_id == 'test-task'


def test_context_pack_save_load(tmp_path):
    """Test saving and loading a context pack."""
    pack = ContextPack(
        task_id='test-task',
        snippets=[Snippet(path='test.py', hash='sha256:123')]
    )
    
    file_path = tmp_path / 'context.json'
    pack.save(file_path)
    
    loaded_pack = ContextPack.load(file_path)
    assert loaded_pack.task_id == 'test-task'
    assert len(loaded_pack.snippets) == 1
    assert loaded_pack.snippets[0].path == 'test.py'
