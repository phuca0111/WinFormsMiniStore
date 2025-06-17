import sqlite3
from Core.edit_delete_log_core import log_edit_delete

class Product:
    def __init__(self, id=None, ten=None, theloai_id=None, hangsanxuat_id=None):
        self.id = id
        self.ten = ten
        self.theloai_id = theloai_id
        self.hangsanxuat_id = hangsanxuat_id

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, theloai_id, hangsanxuat_id FROM sanpham')
        rows = cursor.fetchall()
        conn.close()
        return [Product(id=row[0], ten=row[1], theloai_id=row[2], hangsanxuat_id=row[3]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, theloai_id, hangsanxuat_id FROM sanpham WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Product(id=row[0], ten=row[1], theloai_id=row[2], hangsanxuat_id=row[3])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO sanpham (ten, theloai_id, hangsanxuat_id) VALUES (?, ?, ?)', (self.ten, self.theloai_id, self.hangsanxuat_id))
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            # Ghi log thêm mới (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            log_edit_delete(nguoi_thao_tac, 'thêm', 'sanpham', self.id, self.ten, None, None, f'tên: {self.ten}, thể loại: {self.theloai_id}, hãng: {self.hangsanxuat_id}')
        else:
            cursor.execute('SELECT ten, theloai_id, hangsanxuat_id FROM sanpham WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('UPDATE sanpham SET ten = ?, theloai_id = ?, hangsanxuat_id = ? WHERE id = ?', (self.ten, self.theloai_id, self.hangsanxuat_id, self.id))
            conn.commit()
            conn.close()
            # Ghi log sửa (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            if old:
                if old[0] != self.ten:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'sanpham', self.id, self.ten, 'ten', old[0], self.ten)
                if old[1] != self.theloai_id:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'sanpham', self.id, self.ten, 'theloai_id', old[1], self.theloai_id)
                if old[2] != self.hangsanxuat_id:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'sanpham', self.id, self.ten, 'hangsanxuat_id', old[2], self.hangsanxuat_id)

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('SELECT ten FROM sanpham WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('DELETE FROM sanpham WHERE id = ?', (self.id,))
            nguoi_thao_tac = get_last_login_user()
            if old:
                log_edit_delete(nguoi_thao_tac, 'xóa', 'sanpham', self.id, old[0], None, old[0], None)
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