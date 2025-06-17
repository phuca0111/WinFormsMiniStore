import sqlite3
from datetime import datetime
import random
from Core.edit_delete_log_core import log_edit_delete

class SupplierProduct:
    def __init__(self, id=None, nhacungcap_id=None, bienthe_id=None, ngaynhap=None, soluong_nhap=None, gia_nhap=None, han_su_dung=None):
        self.id = id
        self.nhacungcap_id = nhacungcap_id
        self.bienthe_id = bienthe_id
        self.ngaynhap = ngaynhap or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.soluong_nhap = soluong_nhap
        self.gia_nhap = gia_nhap
        self.han_su_dung = han_su_dung

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nsp.id, nsp.ma_lo, nc.ten, sp.ten, spbt.ten_bienthe, nsp.ngaynhap, nsp.soluong_nhap, nsp.gia_nhap, nsp.han_su_dung
            FROM nhacungcap_sanpham nsp
            JOIN nhacungcap nc ON nsp.nhacungcap_id = nc.id
            JOIN sanpham_bienthe spbt ON nsp.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            ORDER BY nsp.ngaynhap DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nhacungcap_id, bienthe_id, ngaynhap, soluong_nhap, gia_nhap, han_su_dung
            FROM nhacungcap_sanpham 
            WHERE id = ?
        ''', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return SupplierProduct(
                id=row[0],
                nhacungcap_id=row[1],
                bienthe_id=row[2],
                ngaynhap=row[3],
                soluong_nhap=row[4],
                gia_nhap=row[5],
                han_su_dung=row[6]
            )
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        try:
            if self.id is None:
                # Sinh mã lô tạm thời trước khi insert
                now_str = datetime.now().strftime('%Y%m%d%H%M%S')
                temp_ma_lo = f'LO{now_str}{random.randint(100,999)}'
                cursor.execute('''
                    INSERT INTO nhacungcap_sanpham (
                        nhacungcap_id, bienthe_id, ngaynhap, soluong_nhap, gia_nhap, han_su_dung, so_luong_con_lai, ma_lo
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.nhacungcap_id, self.bienthe_id, self.ngaynhap, 
                      self.soluong_nhap, self.gia_nhap, self.han_su_dung, self.soluong_nhap, temp_ma_lo))
                self.id = cursor.lastrowid
                # Sau khi có id, cập nhật lại mã lô chuẩn
                ma_lo = f'LO{now_str}{self.id}'
                cursor.execute('UPDATE nhacungcap_sanpham SET ma_lo = ? WHERE id = ?', (ma_lo, self.id))
                self.ma_lo = ma_lo
                conn.commit()
                conn.close()
                # Ghi log thêm mới (sau khi đã đóng kết nối)
                nguoi_thao_tac = get_last_login_user()
                log_edit_delete(nguoi_thao_tac, 'thêm', 'nhacungcap_sanpham', self.id, None, None, None, f'Nhà cung cấp: {self.nhacungcap_id}, Biến thể: {self.bienthe_id}, SL: {self.soluong_nhap}')

                # Cập nhật tồn kho
                cursor.execute('''
                    INSERT INTO tonkho (bienthe_id, soluong)
                    VALUES (?, ?)
                    ON CONFLICT(bienthe_id) DO UPDATE SET
                    soluong = soluong + ?
                ''', (self.bienthe_id, self.soluong_nhap, self.soluong_nhap))
            else:
                # Lấy giá trị cũ trước khi update
                cursor.execute('SELECT nhacungcap_id, bienthe_id, soluong_nhap, gia_nhap, han_su_dung FROM nhacungcap_sanpham WHERE id = ?', (self.id,))
                old = cursor.fetchone()
                cursor.execute('''
                    UPDATE nhacungcap_sanpham 
                    SET nhacungcap_id = ?, bienthe_id = ?, ngaynhap = ?, 
                        soluong_nhap = ?, gia_nhap = ?, han_su_dung = ?, so_luong_con_lai = so_luong_con_lai + (? - ?)
                    WHERE id = ?
                ''', (self.nhacungcap_id, self.bienthe_id, self.ngaynhap,
                      self.soluong_nhap, self.gia_nhap, self.han_su_dung, self.soluong_nhap, old[2], self.id))
                conn.commit()
                conn.close()
                # Ghi log sửa (sau khi đã đóng kết nối)
                nguoi_thao_tac = get_last_login_user()
                if old:
                    if old[0] != self.nhacungcap_id:
                        log_edit_delete(nguoi_thao_tac, 'sửa', 'nhacungcap_sanpham', self.id, None, 'nhacungcap_id', old[0], self.nhacungcap_id)
                    if old[1] != self.bienthe_id:
                        log_edit_delete(nguoi_thao_tac, 'sửa', 'nhacungcap_sanpham', self.id, None, 'bienthe_id', old[1], self.bienthe_id)
                    if old[2] != self.soluong_nhap:
                        log_edit_delete(nguoi_thao_tac, 'sửa', 'nhacungcap_sanpham', self.id, None, 'soluong_nhap', old[2], self.soluong_nhap)
                    if old[3] != self.gia_nhap:
                        log_edit_delete(nguoi_thao_tac, 'sửa', 'nhacungcap_sanpham', self.id, None, 'gia_nhap', old[3], self.gia_nhap)
                    if old[4] != self.han_su_dung:
                        log_edit_delete(nguoi_thao_tac, 'sửa', 'nhacungcap_sanpham', self.id, None, 'han_su_dung', old[4], self.han_su_dung)
        except Exception as e:
            conn.rollback()
            raise e

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            try:
                # Lấy giá trị cũ trước khi xóa
                cursor.execute('SELECT nhacungcap_id, bienthe_id, soluong_nhap, gia_nhap, han_su_dung FROM nhacungcap_sanpham WHERE id = ?', (self.id,))
                old = cursor.fetchone()
                cursor.execute('DELETE FROM nhacungcap_sanpham WHERE id = ?', (self.id,))
                # Ghi log
                nguoi_thao_tac = get_last_login_user()
                if old:
                    log_edit_delete(nguoi_thao_tac, 'xóa', 'nhacungcap_sanpham', self.id, None, None, str(old), None)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
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