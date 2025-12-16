import sqlite3
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, db_name="recipe_history.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table untuk history pencarian
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                search_query TEXT NOT NULL,
                meal_id TEXT,
                meal_name TEXT,
                meal_thumb TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table untuk history detail view
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detail_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                meal_id TEXT NOT NULL,
                meal_name TEXT NOT NULL,
                meal_thumb TEXT,
                meal_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table untuk history analisis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                meal_id TEXT NOT NULL,
                meal_name TEXT NOT NULL,
                meal_thumb TEXT,
                analysis_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table untuk history download PDF
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS download_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                meal_id TEXT NOT NULL,
                meal_name TEXT NOT NULL,
                download_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table untuk history video watched
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                meal_id TEXT NOT NULL,
                meal_name TEXT NOT NULL,
                video_url TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # SEARCH HISTORY
    def add_search_history(self, username, search_query, meal_id=None, meal_name=None, meal_thumb=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO search_history (username, search_query, meal_id, meal_name, meal_thumb)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, search_query, meal_id, meal_name, meal_thumb))
        conn.commit()
        conn.close()
    
    def get_search_history(self, username, limit=50):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM search_history 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (username, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def delete_search_history(self, history_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM search_history WHERE id = ?', (history_id,))
        conn.commit()
        conn.close()
    
    def clear_search_history(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM search_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
    
    # DETAIL HISTORY
    def add_detail_history(self, username, meal_id, meal_name, meal_thumb, meal_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO detail_history (username, meal_id, meal_name, meal_thumb, meal_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, meal_id, meal_name, meal_thumb, json.dumps(meal_data)))
        conn.commit()
        conn.close()
    
    def get_detail_history(self, username, limit=50):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM detail_history 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (username, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def delete_detail_history(self, history_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM detail_history WHERE id = ?', (history_id,))
        conn.commit()
        conn.close()
    
    def clear_detail_history(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM detail_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
    
    # ANALYSIS HISTORY
    def add_analysis_history(self, username, meal_id, meal_name, meal_thumb, analysis_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO analysis_history (username, meal_id, meal_name, meal_thumb, analysis_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, meal_id, meal_name, meal_thumb, json.dumps(analysis_data)))
        conn.commit()
        conn.close()
    
    def get_analysis_history(self, username, limit=50):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM analysis_history 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (username, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def delete_analysis_history(self, history_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM analysis_history WHERE id = ?', (history_id,))
        conn.commit()
        conn.close()
    
    def clear_analysis_history(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM analysis_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
    
    # DOWNLOAD HISTORY
    def add_download_history(self, username, meal_id, meal_name, download_type):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO download_history (username, meal_id, meal_name, download_type)
            VALUES (?, ?, ?, ?)
        ''', (username, meal_id, meal_name, download_type))
        conn.commit()
        conn.close()
    
    def get_download_history(self, username, limit=50):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM download_history 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (username, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def delete_download_history(self, history_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM download_history WHERE id = ?', (history_id,))
        conn.commit()
        conn.close()
    
    def clear_download_history(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM download_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
    
    # VIDEO HISTORY
    def add_video_history(self, username, meal_id, meal_name, video_url):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO video_history (username, meal_id, meal_name, video_url)
            VALUES (?, ?, ?, ?)
        ''', (username, meal_id, meal_name, video_url))
        conn.commit()
        conn.close()
    
    def get_video_history(self, username, limit=50):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM video_history 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (username, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def delete_video_history(self, history_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM video_history WHERE id = ?', (history_id,))
        conn.commit()
        conn.close()
    
    def clear_video_history(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM video_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
    
    # UTILITY FUNCTIONS
    def get_all_history_count(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        counts = {}
        tables = ['search_history', 'detail_history', 'analysis_history', 'download_history', 'video_history']
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) as count FROM {table} WHERE username = ?', (username,))
            counts[table] = cursor.fetchone()['count']
        
        conn.close()
        return counts
    
    def clear_all_history(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tables = ['search_history', 'detail_history', 'analysis_history', 'download_history', 'video_history']
        for table in tables:
            cursor.execute(f'DELETE FROM {table} WHERE username = ?', (username,))
        
        conn.commit()
        conn.close()