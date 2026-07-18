"""
Database Manager for CyberSuite
Handles SQLite database operations for scan history and results
"""
import sqlite3
import json
import os
from typing import Any, Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            # Create database directory if it doesn't exist
            db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, 'scans.db')
        
        self.db_path: str = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Targets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_name TEXT NOT NULL,
                ip_address TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                scan_id TEXT PRIMARY KEY,
                target_id INTEGER,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                tool_used TEXT NOT NULL,
                options TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'running',
                result_summary TEXT,
                full_output TEXT,
                FOREIGN KEY (target_id) REFERENCES targets(id)
            )
        ''')
        
        # Vulnerabilities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                vuln_id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                recommendation TEXT,
                date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_scan(self, tool_name: str, target: str, options: Dict[str, Any]) -> str:
        """Create a new scan entry"""
        import uuid
        scan_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insert or get target
        cursor.execute('SELECT id FROM targets WHERE target_name = ?', (target,))
        result = cursor.fetchone()
        
        if result:
            target_id = result[0]
        else:
            cursor.execute('INSERT INTO targets (target_name) VALUES (?)', (target,))
            target_id = cursor.lastrowid
        
        # Insert scan
        cursor.execute('''
            INSERT INTO scans (scan_id, target_id, target, scan_type, tool_used, options, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (scan_id, target_id, target, tool_name, tool_name, json.dumps(options), 'running'))
        
        conn.commit()
        conn.close()
        
        return scan_id
    
    def update_scan_result(self, scan_id: str, result: Dict[str, Any], status: str = 'completed') -> None:
        """Update scan with results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        result_summary = json.dumps(result)[:500]  # Store first 500 chars as summary
        full_output = json.dumps(result)
        
        cursor.execute('''
            UPDATE scans 
            SET status = ?, result_summary = ?, full_output = ?
            WHERE scan_id = ?
        ''', (status, result_summary, full_output, scan_id))
        
        conn.commit()
        conn.close()
    
    def add_vulnerability(
        self,
        scan_id: str,
        severity: str,
        title: str,
        description: str,
        recommendation: str
    ) -> None:
        """Add a vulnerability finding"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO vulnerabilities (scan_id, severity, title, description, recommendation)
            VALUES (?, ?, ?, ?, ?)
        ''', (scan_id, severity, title, description, recommendation))
        
        conn.commit()
        conn.close()
    
    def get_scan_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get scan history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT scan_id, target, tool_used, date, status, result_summary
            FROM scans
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        
        results: List[Dict[str, Any]] = []
        for row in cursor.fetchall():
            results.append({
                'scan_id': row[0],
                'target': row[1],
                'tool': row[2],
                'date': row[3],
                'status': row[4],
                'summary': row[5]
            })
        
        conn.close()
        return results
    
    def get_scan_details(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed scan information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT scan_id, target, tool_used, date, status, full_output, options
            FROM scans
            WHERE scan_id = ?
        ''', (scan_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'scan_id': row[0],
                'target': row[1],
                'tool': row[2],
                'date': row[3],
                'status': row[4],
                'output': json.loads(row[5]) if row[5] else {},
                'options': json.loads(row[6]) if row[6] else {}
            }
        return None
    
    def get_vulnerabilities(self, scan_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get vulnerabilities, optionally filtered by scan_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if scan_id:
            cursor.execute('''
                SELECT vuln_id, scan_id, severity, title, description, recommendation, date_found
                FROM vulnerabilities
                WHERE scan_id = ?
                ORDER BY date_found DESC
            ''', (scan_id,))
        else:
            cursor.execute('''
                SELECT vuln_id, scan_id, severity, title, description, recommendation, date_found
                FROM vulnerabilities
                ORDER BY date_found DESC
                LIMIT 100
            ''')
        
        results: List[Dict[str, Any]] = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'scan_id': row[1],
                'severity': row[2],
                'title': row[3],
                'description': row[4],
                'recommendation': row[5],
                'date': row[6]
            })
        
        conn.close()
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total scans
        cursor.execute('SELECT COUNT(*) FROM scans')
        total_scans = cursor.fetchone()[0]
        
        # Total targets
        cursor.execute('SELECT COUNT(*) FROM targets')
        total_targets = cursor.fetchone()[0]
        
        # Total vulnerabilities
        cursor.execute('SELECT COUNT(*) FROM vulnerabilities')
        total_vulns = cursor.fetchone()[0]
        
        # Vulnerabilities by severity
        cursor.execute('''
            SELECT severity, COUNT(*) 
            FROM vulnerabilities 
            GROUP BY severity
        ''')
        vulns_by_severity = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_scans': total_scans,
            'total_targets': total_targets,
            'total_vulnerabilities': total_vulns,
            'vulnerabilities_by_severity': vulns_by_severity
        }
    
    def clear_all(self) -> None:
        """Clear all data from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM vulnerabilities')
        cursor.execute('DELETE FROM scans')
        cursor.execute('DELETE FROM targets')
        
        conn.commit()
        conn.close()
