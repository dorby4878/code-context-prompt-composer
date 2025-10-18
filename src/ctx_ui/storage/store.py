"""Storage layer - SQLite for metadata and FAISS for embeddings."""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class MetadataStore:
    """SQLite-based metadata storage."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    hash TEXT NOT NULL,
                    size INTEGER,
                    last_modified TIMESTAMP,
                    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    context_pack TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS context_packs (
                    id TEXT PRIMARY KEY,
                    task_id TEXT,
                    file_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            conn.commit()
    
    def index_file(self, path: str, hash: str, size: int, metadata: Optional[Dict[str, Any]] = None):
        """Index a file in the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO files (path, hash, size, last_modified, indexed_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (path, hash, size, datetime.now(), datetime.now(), json.dumps(metadata or {})))
            conn.commit()
    
    def get_file(self, path: str) -> Optional[Dict[str, Any]]:
        """Get file metadata by path."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM files WHERE path = ?', (path,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_files(self) -> List[Dict[str, Any]]:
        """List all indexed files."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM files ORDER BY path')
            return [dict(row) for row in cursor.fetchall()]
    
    def save_task(self, task_id: str, title: str, description: str, context_pack: Optional[str], metadata: Optional[Dict[str, Any]] = None):
        """Save task metadata."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO tasks (id, title, description, context_pack, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, COALESCE((SELECT created_at FROM tasks WHERE id = ?), ?), ?, ?)
            ''', (task_id, title, description, context_pack, task_id, datetime.now(), datetime.now(), json.dumps(metadata or {})))
            conn.commit()
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task metadata by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM tasks ORDER BY updated_at DESC')
            return [dict(row) for row in cursor.fetchall()]


class EmbeddingStore:
    """FAISS-based embedding storage with TF-IDF fallback."""
    
    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.use_faiss = False
        self.embeddings = {}
        
        try:
            import faiss
            self.use_faiss = True
            self.dimension = 384  # sentence-transformers default
            self.index = faiss.IndexFlatL2(self.dimension)
            self.id_map = []
        except ImportError:
            # Fallback to simple dictionary storage
            pass
    
    def add_embedding(self, file_id: str, embedding: List[float]):
        """Add an embedding to the store."""
        if self.use_faiss:
            import numpy as np
            self.index.add(np.array([embedding], dtype='float32'))
            self.id_map.append(file_id)
        else:
            self.embeddings[file_id] = embedding
    
    def search(self, query_embedding: List[float], k: int = 5) -> List[str]:
        """Search for similar embeddings."""
        if self.use_faiss and self.index.ntotal > 0:
            import numpy as np
            distances, indices = self.index.search(np.array([query_embedding], dtype='float32'), k)
            return [self.id_map[i] for i in indices[0] if i < len(self.id_map)]
        else:
            # Simple cosine similarity fallback
            import math
            scores = []
            for file_id, emb in self.embeddings.items():
                dot_product = sum(a * b for a, b in zip(query_embedding, emb))
                norm_a = math.sqrt(sum(a * a for a in query_embedding))
                norm_b = math.sqrt(sum(b * b for b in emb))
                similarity = dot_product / (norm_a * norm_b) if norm_a and norm_b else 0
                scores.append((file_id, similarity))
            scores.sort(key=lambda x: x[1], reverse=True)
            return [file_id for file_id, _ in scores[:k]]
