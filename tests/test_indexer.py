"""Tests for indexer functionality."""

import pytest
from pathlib import Path
from src.ctx_ui.context.indexer import list_repo_files


def test_list_repo_files(tmp_path):
    """Test listing repository files with include/exclude patterns."""
    # Create test files
    (tmp_path / 'src').mkdir()
    (tmp_path / 'src' / 'main.py').write_text('# main')
    (tmp_path / 'src' / 'utils.py').write_text('# utils')
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'tests' / 'test_main.py').write_text('# test')
    (tmp_path / 'node_modules').mkdir()
    (tmp_path / 'node_modules' / 'lib.js').write_text('// lib')
    
    # Test with include pattern
    files = list_repo_files(
        tmp_path,
        include=['*.py'],
        exclude=['node_modules/**']
    )
    
    assert len(files) == 3
    assert any('main.py' in str(f) for f in files)
    assert any('utils.py' in str(f) for f in files)
    assert any('test_main.py' in str(f) for f in files)
    assert not any('lib.js' in str(f) for f in files)


def test_exclude_patterns(tmp_path):
    """Test that exclude patterns work correctly."""
    (tmp_path / '.git').mkdir()
    (tmp_path / '.git' / 'config').write_text('config')
    (tmp_path / 'src').mkdir()
    (tmp_path / 'src' / 'main.py').write_text('# main')
    
    files = list_repo_files(
        tmp_path,
        include=['*'],
        exclude=['.git/**']
    )
    
    assert not any('.git' in str(f) for f in files)
    assert any('main.py' in str(f) for f in files)
