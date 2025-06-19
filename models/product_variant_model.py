import sqlite3
from Core.edit_delete_log_core import log_edit_delete

class ProductVariant:
    def __init__(self, id=None, sanpham_id=None, ten_bienthe=None, gia=None, barcode=None):
        self.id = id
        self.sanpham_id = sanpham_id
        self.ten_bienthe = ten_bienthe
        self.gia = gia
        self.barcode = barcode

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, sanpham_id, ten_bienthe, gia, barcode FROM sanpham_bienthe')
        rows = cursor.fetchall()
        conn.close()
        return [ProductVariant(id=row[0], sanpham_id=row[1], ten_bienthe=row[2], gia=row[3], barcode=row[4]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, sanpham_id, ten_bienthe, gia, barcode FROM sanpham_bienthe WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return ProductVariant(id=row[0], sanpham_id=row[1], ten_bienthe=row[2], gia=row[3], barcode=row[4])
        return None

    @staticmethod
    def get_by_barcode(barcode):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, sanpham_id, ten_bienthe, gia, barcode FROM sanpham_bienthe WHERE barcode = ?', (barcode,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return ProductVariant(id=row[0], sanpham_id=row[1], ten_bienthe=row[2], gia=row[3], barcode=row[4])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO sanpham_bienthe (sanpham_id, ten_bienthe, gia, barcode) VALUES (?, ?, ?, ?)', (self.sanpham_id, self.ten_bienthe, self.gia, self.barcode))
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            # Ghi log thêm mới (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            log_edit_delete(nguoi_thao_tac, 'thêm', 'sanpham_bienthe', self.id, self.ten_bienthe, None, None, f'sản phẩm: {self.sanpham_id}, giá: {self.gia}, barcode: {self.barcode}')
        else:
            cursor.execute('SELECT sanpham_id, ten_bienthe, gia, barcode FROM sanpham_bienthe WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('UPDATE sanpham_bienthe SET sanpham_id = ?, ten_bienthe = ?, gia = ?, barcode = ? WHERE id = ?', (self.sanpham_id, self.ten_bienthe, self.gia, self.barcode, self.id))
            conn.commit()
            conn.close()
            # Ghi log sửa (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            if old:
                if old[0] != self.sanpham_id:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'sanpham_bienthe', self.id, self.ten_bienthe, 'sanpham_id', old[0], self.sanpham_id)
                if old[1] != self.ten_bienthe:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'sanpham_bienthe', self.id, self.ten_bienthe, 'ten_bienthe', old[1], self.ten_bienthe)
                if old[2] != self.gia:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'sanpham_bienthe', self.id, self.ten_bienthe, 'gia', old[2], self.gia)
                if old[3] != self.barcode:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'sanpham_bienthe', self.id, self.ten_bienthe, 'barcode', old[3], self.barcode)

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('SELECT ten_bienthe FROM sanpham_bienthe WHERE id = ?', (self.id,))
            old = cursor.fetchone()
            cursor.execute('DELETE FROM sanpham_bienthe WHERE id = ?', (self.id,))
            nguoi_thao_tac = get_last_login_user()
            conn.commit()
            conn.close()
            # Sau khi đã đóng kết nối, mới ghi log
            if old:
                log_edit_delete(nguoi_thao_tac, 'xóa', 'sanpham_bienthe', self.id, old[0], None, old[0], None)

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