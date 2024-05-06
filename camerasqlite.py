import sqlite3
import logging
from perfdecorator import time_execution
#import threading
import re



def singleton(cls):
   instance = None

   def wrapper(*args, **kwargs):
       nonlocal instance
       if instance is None:
           instance = cls(*args, **kwargs)
       return instance
   return wrapper

#@singleton
class camerasqlite():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            address TEXT,
            image BLOB
        ) """
    def __init__(self, file='main.db'):
        self.logger = logging.getLogger(__name__)
        self.file = file
        self.conn = sqlite3.connect(self.file)
        #self.lock = threading.Lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def checkiftableexist(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='your_table_name'
        """)
        result = cursor.fetchone()

        if result:
            self.logger.info(f"Table exists.")
            return True
        else:
            self.logger.error(f"Table does not exist.")
            return False

    def createtable(self):
        cursor = self.conn.cursor()
        cursor.execute(camerasqlite.create_table_query)
        self.conn.commit()


    @time_execution
    def store(self, image, address='unknown') -> int:
        image_bytes = image
        cursor = self.conn.cursor()
        # Store in the database
        cursor.execute("INSERT INTO images (image,address) VALUES (?,?)", (image_bytes,address))
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

    @time_execution
    def getalldata(self,id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT image,address,timestamp FROM images WHERE id = ?", (id,))
        blob_data = cursor.fetchone()[0]
        im_address = cursor.fetchone()[1]
        im_timestamp = cursor.fetchone()[2]
        return blob_data,im_address,im_timestamp

    def getmax(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(id) FROM images")
        result = cursor.fetchone()
        max_id = result[0]
        self.logger.info(f"last inserted id:{max_id}")
        return max_id

    def sanitize_address(self, address:str) -> str:
        # Allow letters, numbers, underscores
        return re.sub(r"[^\w\.]", "", address)

    def getcameras(self) -> list:
        cursor = self.conn.cursor()
        cursor.execute("SELECT distinct(address) FROM images")
        result = cursor.fetchall()
        cam_list = [row[0] for row in result]
        self.logger.info(f"cameras:{cam_list}")
        return cam_list

    @time_execution
    def getlastforaddress(self, address:str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT image FROM images WHERE id = ( SELECT MAX(id) FROM images where address = ?)", (address,))
        blob_data = cursor.fetchone()[0]
        return blob_data

    def getidbetweentimestamp(self, address:str, tfrom:str, tto:str) -> list:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM images WHERE address = ? AND timestamp BETWEEN ? AND ?", (address,tfrom, tto))
        result = cursor.fetchall()
        ids = [row[0] for row in result]
        self.logger.info(f"ids:{ids}")
        print(f"ids:{ids}")
        return ids

    def deleteold(self,hours:int):
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM images WHERE timestamp < DATETIME('now', '-{str(hours)} hour'); ")
        self.conn.commit()
