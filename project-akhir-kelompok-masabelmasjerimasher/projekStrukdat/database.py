import sqlite3
import json
from datetime import datetime

# ============================
# Class untuk mengelola history pencarian resep
# ============================

class RecipeSearchHistory:
    """
    Class untuk menyimpan dan mengelola riwayat pencarian resep
    menggunakan database SQLite
    """
    
    def __init__(self, db_path='recipe_history.db'):
        """
        Inisialisasi koneksi database
        Args:
            db_path: Path file database SQLite
        """
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()
    
    # ============================
    # Fungsi: Membuat tabel database
    # ============================
    def create_table(self):
        """
        Membuat tabel search_history jika belum ada
        Struktur tabel:
        - id: Primary key
        - username: Nama user yang melakukan pencarian
        - search_query: Query pencarian
        - search_type: Jenis pencarian (search/filter/recommendation)
        - result_data: Data hasil pencarian dalam format JSON
        - timestamp: Waktu pencarian
        """
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                search_query TEXT NOT NULL,
                search_type TEXT,
                result_data JSON,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Index untuk mempercepat query berdasarkan username
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_username ON search_history(username)')
        # Index untuk mempercepat query berdasarkan timestamp
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON search_history(timestamp DESC)')
        self.conn.commit()
    
    # ============================
    # Fungsi: Menyimpan pencarian ke database
    # ============================
    def save_search(self, username, query, search_type, result_data):
        """
        Menyimpan history pencarian ke database
        
        Args:
            username: Username yang melakukan pencarian
            query: Kata kunci pencarian
            search_type: Tipe pencarian (search/filter/recommendation)
            result_data: Dictionary berisi data hasil pencarian
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO search_history 
            (username, search_query, search_type, result_data)
            VALUES (?, ?, ?, ?)
        ''', (
            username,
            query,
            search_type,
            json.dumps(result_data)  # Convert dict ke JSON string
        ))
        self.conn.commit()
    
    # ============================
    # Fungsi: Mengambil riwayat pencarian user
    # ============================
    def get_history(self, username, limit=20):
        """
        Mengambil riwayat pencarian user dari database
        
        Args:
            username: Username yang ingin dilihat historynya
            limit: Jumlah maksimal history yang diambil
            
        Returns:
            List of dict berisi history pencarian
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, search_query, search_type, result_data, timestamp
            FROM search_history
            WHERE username = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (username, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'query': row[1],
                'type': row[2],
                'data': json.loads(row[3]) if row[3] else {},  # Convert JSON string ke dict
                'timestamp': row[4]
            })
        return results
    
    # ============================
    # Fungsi: Mengambil detail pencarian tertentu
    # ============================
    def get_search_detail(self, search_id):
        """
        Mengambil detail lengkap dari satu pencarian berdasarkan ID
        
        Args:
            search_id: ID history yang ingin dilihat
            
        Returns:
            Dictionary berisi detail pencarian atau None jika tidak ditemukan
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT search_query, search_type, result_data, timestamp
            FROM search_history
            WHERE id = ?
        ''', (search_id,))
        
        row = cursor.fetchone()
        if row:
            return {
                'query': row[0],
                'type': row[1],
                'data': json.loads(row[2]) if row[2] else {},
                'timestamp': row[3]
            }
        return None
    
    # ============================
    # Fungsi: Menghapus semua history user
    # ============================
    def clear_history(self, username):
        """
        Menghapus semua riwayat pencarian user
        
        Args:
            username: Username yang historynya akan dihapus
        """
        self.conn.execute(
            'DELETE FROM search_history WHERE username = ?',
            (username,)
        )
        self.conn.commit()
    
    # ============================
    # Fungsi: Mencari dalam history
    # ============================
    def search_in_history(self, username, keyword):
        """
        Mencari history berdasarkan keyword
        
        Args:
            username: Username yang historynya akan dicari
            keyword: Kata kunci untuk mencari dalam query
            
        Returns:
            List of dict berisi history yang cocok dengan keyword
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, search_query, search_type, timestamp
            FROM search_history
            WHERE username = ? AND search_query LIKE ?
            ORDER BY timestamp DESC
        ''', (username, f'%{keyword}%'))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'query': row[1],
                'type': row[2],
                'timestamp': row[3]
            })
        return results