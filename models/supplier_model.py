import sqlite3
from Core.edit_delete_log_core import log_edit_delete

class Supplier:
    def __init__(self, id=None, ten=None, diachi=None, sdt=None, gmail=None):
        self.id = id
        self.ten = ten
        self.diachi = diachi
        self.sdt = sdt
        self.gmail = gmail

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, diachi, sdt, gmail FROM nhacungcap')
        rows = cursor.fetchall()
        conn.close()
        return [Supplier(id=row[0], ten=row[1], diachi=row[2], sdt=row[3], gmail=row[4]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, diachi, sdt, gmail FROM nhacungcap WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Supplier(id=row[0], ten=row[1], diachi=row[2], sdt=row[3], gmail=row[4])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('''
                INSERT INTO nhacungcap (ten, diachi, sdt, gmail) 
                VALUES (?, ?, ?, ?)
            ''', (self.ten, self.diachi, self.sdt, self.gmail))
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            # Ghi log thêm mới (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            log_edit_delete(nguoi_thao_tac, 'thêm', 'nhacungcap', self.id, self.ten, None, None, f'tên: {self.ten}, sdt: {self.sdt}')
        else:
            cursor.execute('SELECT ten, diachi, sdt, gmail FROM nhacungcap WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('''
                UPDATE nhacungcap 
                SET ten = ?, diachi = ?, sdt = ?, gmail = ? 
                WHERE id = ?
            ''', (self.ten, self.diachi, self.sdt, self.gmail, self.id))
            # Lưu lại thông tin log nếu cần
            log_info = None
            if old:
                nguoi_thao_tac = get_last_login_user()
                if old[0] != self.ten:
                    log_info = ('ten', old[0], self.ten)
                elif old[1] != self.diachi:
                    log_info = ('diachi', old[1], self.diachi)
                elif old[2] != self.sdt:
                    log_info = ('sdt', old[2], self.sdt)
                elif old[3] != self.gmail:
                    log_info = ('gmail', old[3], self.gmail)
            conn.commit()
            conn.close()
            # Ghi log sửa (sau khi đã đóng kết nối)
            if log_info:
                log_edit_delete(nguoi_thao_tac, 'sửa', 'nhacungcap', self.id, self.ten, log_info[0], log_info[1], log_info[2])

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('SELECT ten FROM nhacungcap WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('DELETE FROM nhacungcap WHERE id = ?', (self.id,))
            nguoi_thao_tac = get_last_login_user()
            conn.commit()
            conn.close()
            # Sau khi đã đóng kết nối, mới ghi log
            if old:
                log_edit_delete(nguoi_thao_tac, 'xóa', 'nhacungcap', self.id, old[0], None, old[0], None)

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