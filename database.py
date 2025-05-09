import sqlite3

class CertDBHandler:
    def __init__(self, node_id):
        self.db_path = f"certificate_database_{node_id}.db"
        self._ensure_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_table(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cert (
                id INTEGER PRIMARY KEY UNIQUE,
                recipient_id TEXT NOT NULL,
                issuer_id TEXT NOT NULL,
                cert_hash TEXT NOT NULL,
                db_id TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def insert_cert(self, recipient_id, issuer_id, cert_hash, db_id, timestamp):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cert (recipient_id, issuer_id, cert_hash, db_id, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (recipient_id, issuer_id, cert_hash, db_id, timestamp))
        conn.commit()
        conn.close()

    def fetch_certs(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cert")
        rows = cursor.fetchall()
        conn.close()
        return rows
