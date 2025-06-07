import sqlite3
from sqlite3 import Error
import os
from .config import DB_PATH, DB_TIMEOUT, DB_CHECK_SAME_THREAD

class Database:
    def __init__(self, db_file=DB_PATH):
        """Khởi tạo kết nối database"""
        self.db_file = db_file
        self.conn = None
        try:
            self.conn = sqlite3.connect(
                db_file,
                timeout=DB_TIMEOUT,
                check_same_thread=DB_CHECK_SAME_THREAD
            )
            print(f"Kết nối thành công đến SQLite database: {db_file}")
        except Error as e:
            print(f"Lỗi khi kết nối đến database: {e}")

    def create_connection(self):
        """Tạo kết nối mới đến database"""
        try:
            self.conn = sqlite3.connect(
                self.db_file,
                timeout=DB_TIMEOUT,
                check_same_thread=DB_CHECK_SAME_THREAD
            )
            return self.conn
        except Error as e:
            print(f"Lỗi khi tạo kết nối: {e}")
            return None

    def close_connection(self):
        """Đóng kết nối database"""
        if self.conn:
            self.conn.close()
            print("Đã đóng kết nối database")

    def execute_query(self, query, params=None):
        """Thực thi câu query và trả về kết quả"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except Error as e:
            print(f"Lỗi khi thực thi query: {e}")
            return None

    def fetch_all(self, query, params=None):
        """Lấy tất cả kết quả từ query"""
        try:
            cursor = self.execute_query(query, params)
            if cursor:
                return cursor.fetchall()
            return None
        except Error as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")
            return None

    def fetch_one(self, query, params=None):
        """Lấy một kết quả từ query"""
        try:
            cursor = self.execute_query(query, params)
            if cursor:
                return cursor.fetchone()
            return None
        except Error as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")
            return None

    def insert_data(self, table, data):
        """Thêm dữ liệu vào bảng"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor = self.conn.cursor()
            cursor.execute(query, list(data.values()))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Lỗi khi thêm dữ liệu: {e}")
            return None

    def update_data(self, table, data, condition):
        """Cập nhật dữ liệu trong bảng"""
        try:
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            where_clause = ' AND '.join([f"{k} = ?" for k in condition.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            
            cursor = self.conn.cursor()
            cursor.execute(query, list(data.values()) + list(condition.values()))
            self.conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Lỗi khi cập nhật dữ liệu: {e}")
            return None

    def delete_data(self, table, condition):
        """Xóa dữ liệu từ bảng"""
        try:
            where_clause = ' AND '.join([f"{k} = ?" for k in condition.keys()])
            query = f"DELETE FROM {table} WHERE {where_clause}"
            
            cursor = self.conn.cursor()
            cursor.execute(query, list(condition.values()))
            self.conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Lỗi khi xóa dữ liệu: {e}")
            return None

# Ví dụ sử dụng:
if __name__ == "__main__":
    # Khởi tạo kết nối
    db = Database()
    
    # Ví dụ thêm cửa hàng mới
    cuahang_data = {
        'ten': 'Cửa hàng chính'
    }
    cuahang_id = db.insert_data('cuahang', cuahang_data)
    print(f"Đã thêm cửa hàng mới với ID: {cuahang_id}")
    
    # Ví dụ truy vấn dữ liệu
    result = db.fetch_all("SELECT * FROM cuahang")
    print("Danh sách cửa hàng:")
    for row in result:
        print(row)
    
    # Đóng kết nối
    db.close_connection() 