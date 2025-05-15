from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import sqlite3

@dataclass
class Certificate:
    cert_id: str
    user_public_key: str  # Foreign key to User
    cert_hash: str
    issued_at: str = datetime.utcnow().isoformat()

class CertificateRepository:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS certificates (
            cert_id TEXT PRIMARY KEY,
            user_public_key TEXT NOT NULL,
            cert_hash TEXT NOT NULL,
            issued_at TEXT,
            FOREIGN KEY(user_public_key) REFERENCES users(public_key)
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_certificate(self, cert: Certificate):
        query = """
        INSERT OR REPLACE INTO certificates (cert_id, user_public_key, cert_hash, issued_at)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(query, (cert.cert_id, cert.user_public_key, cert.cert_hash, cert.issued_at))
        self.conn.commit()

    def get_certificates_by_user(self, user_public_key: str) -> List[Certificate]:
        cursor = self.conn.execute("SELECT * FROM certificates WHERE user_public_key = ?", (user_public_key,))
        rows = cursor.fetchall()
        return [Certificate(*row) for row in rows]

    def get_all_certificates(self) -> List[Certificate]:
        cursor = self.conn.execute("SELECT * FROM certificates")
        rows = cursor.fetchall()
        return [Certificate(*row) for row in rows]

    def close(self):
        self.conn.close()
