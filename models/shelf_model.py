from Core.edit_delete_log_core import log_edit_delete
import sqlite3

class ShelfModel:
    def __init__(self, db_path):
        self.db_path = db_path
    # Nếu cần, chỉ giữ lại các hàm thao tác dữ liệu đơn giản (select, get, v.v.)
    # Ví dụ:
    def get_all_shelves(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten FROM kehang")
        shelves = cursor.fetchall()
        conn.close()
        return shelves 