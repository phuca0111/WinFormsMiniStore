import sqlite3
from Core.edit_delete_log_core import log_edit_delete

class Category:
    def __init__(self, id=None, ten=None):
        self.id = id
        self.ten = ten

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten FROM theloai")
        rows = cursor.fetchall()
        conn.close()
        return [Category(id=row[0], ten=row[1]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten FROM theloai WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Category(id=row[0], ten=row[1])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO theloai (ten) VALUES (?)", (self.ten,))
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            # Ghi log thêm mới (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            log_edit_delete(nguoi_thao_tac, 'thêm', 'theloai', self.id, self.ten, None, None, f'tên: {self.ten}')
        else:
            cursor.execute("SELECT ten FROM theloai WHERE id = ?", (self.id,))
            old = cursor.fetchone()
            cursor.execute("UPDATE theloai SET ten = ? WHERE id = ?", (self.ten, self.id))
            # Lưu lại thông tin log nếu cần
            log_info = None
            if old and old[0] != self.ten:
                nguoi_thao_tac = get_last_login_user()
                log_info = (nguoi_thao_tac, self.id, self.ten, old[0], self.ten)
            conn.commit()
            conn.close()
            # Ghi log sửa (sau khi đã đóng kết nối)
            if log_info:
                log_edit_delete(log_info[0], 'sửa', 'theloai', log_info[1], log_info[2], 'ten', log_info[3], log_info[4])

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT ten FROM theloai WHERE id = ?", (self.id,))
            old = cursor.fetchone()
            cursor.execute("DELETE FROM theloai WHERE id = ?", (self.id,))
            nguoi_thao_tac = get_last_login_user()
            if old:
                log_edit_delete(nguoi_thao_tac, 'xóa', 'theloai', self.id, old[0], None, old[0], None)
            conn.commit()
            conn.close()

def get_last_login_user():
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT nhanvien_id FROM nhanvien_login_log ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        cursor.execute('SELECT ten FROM nhanvien WHERE id = ?', (row[0],))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else 'Chưa xác định'
    conn.close()
    return 'Chưa xác định' 