import sqlite3
from Core.edit_delete_log_core import log_edit_delete

class Inventory:
    def __init__(self, id=None, bienthe_id=None, soluong=0):
        self.id = id
        self.bienthe_id = bienthe_id
        self.soluong = soluong

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, bienthe_id, soluong FROM tonkho')
        rows = cursor.fetchall()
        conn.close()
        return [Inventory(id=row[0], bienthe_id=row[1], soluong=row[2]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, bienthe_id, soluong FROM tonkho WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Inventory(id=row[0], bienthe_id=row[1], soluong=row[2])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO tonkho (bienthe_id, soluong) VALUES (?, ?)', (self.bienthe_id, self.soluong))
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            # Ghi log thêm mới (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            log_edit_delete(nguoi_thao_tac, 'thêm', 'tonkho', self.id, None, None, None, f'biến thể: {self.bienthe_id}, số lượng: {self.soluong}')
        else:
            cursor.execute('SELECT bienthe_id, soluong FROM tonkho WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('UPDATE tonkho SET bienthe_id = ?, soluong = ? WHERE id = ?', (self.bienthe_id, self.soluong, self.id))
            conn.commit()
            conn.close()
            # Ghi log sửa (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            if old:
                if old[0] != self.bienthe_id:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'tonkho', self.id, None, 'bienthe_id', old[0], self.bienthe_id)
                if old[1] != self.soluong:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'tonkho', self.id, None, 'soluong', old[1], self.soluong)

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('SELECT bienthe_id, soluong FROM tonkho WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('DELETE FROM tonkho WHERE id = ?', (self.id,))
            nguoi_thao_tac = get_last_login_user()
            if old:
                log_edit_delete(nguoi_thao_tac, 'xóa', 'tonkho', self.id, None, None, str(old), None)
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