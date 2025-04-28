"""
Document storage system for commit analysis results.
"""

import json
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import sqlite3


class DocumentStore:
    """
    Hybrid storage system that can save both raw documents and vector embeddings.
    """
    
    def __init__(self, storage_path: str = "./data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize SQLite database for metadata
        self.db_path = self.storage_path / "analysis_db.sqlite"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for metadata storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timeframe TEXT,
                created_at TIMESTAMP,
                commit_count INTEGER,
                report_path TEXT,
                metadata JSON
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS commit_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commit_hash TEXT UNIQUE,
                author TEXT,
                date TIMESTAMP,
                category TEXT,
                impact_score REAL,
                risk_assessment TEXT,
                summary TEXT,
                raw_data JSON
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_analysis_report(self, report: Dict[str, Any]) -> str:
        """Store complete analysis report."""
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report_path = self.storage_path / f"{report_id}.json"
        
        # Save full report to file with custom serialization
        with open(report_path, 'w') as f:
            # Convert any non-serializable objects to dicts
            serializable_report = self._make_serializable(report)
            json.dump(serializable_report, f, indent=2, default=str)
        
        # Store metadata in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analysis_reports 
            (timeframe, created_at, commit_count, report_path, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            report['timeframe'],
            datetime.now().isoformat(),
            report['commits_analyzed'],
            str(report_path),
            json.dumps({'report_id': report_id})
        ))
        
        conn.commit()
        conn.close()
        
        return report_id
    
    def _make_serializable(self, obj):
        """Convert non-serializable objects to dictionaries."""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self._make_serializable(obj.__dict__)
        elif hasattr(obj, '_asdict'):
            return self._make_serializable(obj._asdict())
        else:
            return obj
    
    def store_commit_analysis(self, analysis):
        """Store individual commit analysis."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO commit_analyses
            (commit_hash, author, date, category, impact_score, risk_assessment, summary, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis.commit_hash,
            analysis.author,
            analysis.date.isoformat(),
            analysis.category,
            analysis.impact_score,
            analysis.risk_assessment,
            analysis.summary,
            json.dumps({
                'files_changed': analysis.files_changed,
                'insertions': analysis.insertions,
                'deletions': analysis.deletions,
                'message': analysis.message
            })
        ))
        
        conn.commit()
        conn.close()
    
    def retrieve_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a stored report by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT report_path FROM analysis_reports
            WHERE metadata LIKE ?
        """, (f'%"{report_id}"%',))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            report_path = Path(result[0])
            if report_path.exists():
                with open(report_path, 'r') as f:
                    return json.load(f)
        
        return None
    
    def get_recent_reports(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analysis reports."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timeframe, created_at, commit_count, metadata
            FROM analysis_reports
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in results:
            reports.append({
                'timeframe': row[0],
                'created_at': row[1],
                'commit_count': row[2],
                'metadata': json.loads(row[3])
            })
        
        return reports
    
    def store_vector_embeddings(self, document_id: str, embeddings: List[float]):
        """Store vector embeddings for RAG."""
        embeddings_path = self.storage_path / "embeddings" / f"{document_id}.pkl"
        embeddings_path.parent.mkdir(exist_ok=True)
        
        with open(embeddings_path, 'wb') as f:
            pickle.dump(embeddings, f)
    
    def retrieve_vector_embeddings(self, document_id: str) -> Optional[List[float]]:
        """Retrieve vector embeddings."""
        embeddings_path = self.storage_path / "embeddings" / f"{document_id}.pkl"
        
        if embeddings_path.exists():
            with open(embeddings_path, 'rb') as f:
                return pickle.load(f)
        
        return None
