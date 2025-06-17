from Core.edit_delete_log_core import log_edit_delete
import sqlite3

class ShelfModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def update_shelf(self, shelf_id, ten):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT ten FROM kehang WHERE id=?", (shelf_id,))
        old = cursor.fetchone()
        cursor.execute("UPDATE kehang SET ten=? WHERE id=?", (ten, shelf_id))
        # Lưu lại thông tin log nếu cần
        log_info = None
        if old and old[0] != ten:
            nguoi_thao_tac = get_last_login_user()
            log_info = (nguoi_thao_tac, shelf_id, ten, old[0], ten)
        conn.commit()
        conn.close()
        # Ghi log sửa (sau khi đã đóng kết nối)
        if log_info:
            log_edit_delete(log_info[0], 'sửa', 'kehang', log_info[1], log_info[2], 'ten', log_info[3], log_info[4])

    def delete_shelf(self, shelf_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Lấy giá trị cũ trước khi xóa
        cursor.execute("SELECT ten FROM kehang WHERE id=?", (shelf_id,))
        old = cursor.fetchone()
        cursor.execute("DELETE FROM kehang WHERE id=?", (shelf_id,))
        # Ghi log
        nguoi_thao_tac = get_last_login_user()
        if old:
            log_edit_delete(nguoi_thao_tac, 'xóa', 'kehang', shelf_id, old[0], None, old[0], None)
        conn.commit()
        conn.close()

    def add_shelf(self, ten):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kehang (ten) VALUES (?)", (ten,))
        shelf_id = cursor.lastrowid
        conn.commit()
        conn.close()
        # Ghi log thêm mới (sau khi đã đóng kết nối)
        nguoi_thao_tac = get_last_login_user()
        log_edit_delete(nguoi_thao_tac, 'thêm', 'kehang', shelf_id, ten, None, None, f'tên: {ten}')

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