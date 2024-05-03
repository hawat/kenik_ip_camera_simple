import sqlite3
import logging
from perfdecorator import time_execution

class camerasqlite():
    def __init__(self, file='main.db'):
        self.logger = logging.getLogger(__name__)
        self.file = file
        self.conn = sqlite3.connect(self.file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


    @time_execution
    def store(self, image) -> int:
        image_bytes = image
        cursor = self.conn.cursor()
        # Store in the database
        cursor.execute("INSERT INTO images (image) VALUES (?)", (image_bytes,))
        self.conn.commit()
        last_id = cursor.lastrowid
        self.logger.info(f"last inserted id:{last_id}")
        return last_id

    @time_execution
    def get(self,id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT image FROM images WHERE id = ?", (id,))
        blob_data = cursor.fetchone()[0]
        return blob_data
