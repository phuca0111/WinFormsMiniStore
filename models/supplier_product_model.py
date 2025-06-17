import sqlite3
from datetime import datetime

class SupplierProduct:
    def __init__(self, id=None, nhacungcap_id=None, bienthe_id=None, ngaynhap=None, soluong_nhap=None, gia_nhap=None):
        self.id = id
        self.nhacungcap_id = nhacungcap_id
        self.bienthe_id = bienthe_id
        self.ngaynhap = ngaynhap or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.soluong_nhap = soluong_nhap
        self.gia_nhap = gia_nhap

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nsp.id, nc.ten, sp.ten, spbt.ten_bienthe, nsp.ngaynhap, nsp.soluong_nhap, nsp.gia_nhap
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
            SELECT id, nhacungcap_id, bienthe_id, ngaynhap, soluong_nhap, gia_nhap
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
                gia_nhap=row[5]
            )
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute('''
                    INSERT INTO nhacungcap_sanpham (
                        nhacungcap_id, bienthe_id, ngaynhap, soluong_nhap, gia_nhap
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (self.nhacungcap_id, self.bienthe_id, self.ngaynhap, 
                      self.soluong_nhap, self.gia_nhap))
                self.id = cursor.lastrowid

                # Cập nhật tồn kho
                cursor.execute('''
                    INSERT INTO tonkho (bienthe_id, soluong)
                    VALUES (?, ?)
                    ON CONFLICT(bienthe_id) DO UPDATE SET
                    soluong = soluong + ?
                ''', (self.bienthe_id, self.soluong_nhap, self.soluong_nhap))
            else:
                # Lấy số lượng cũ
                cursor.execute('SELECT soluong_nhap FROM nhacungcap_sanpham WHERE id = ?', (self.id,))
                old_quantity = cursor.fetchone()[0]

                # Cập nhật bảng nhacungcap_sanpham
                cursor.execute('''
                    UPDATE nhacungcap_sanpham 
                    SET nhacungcap_id = ?, bienthe_id = ?, ngaynhap = ?, 
                        soluong_nhap = ?, gia_nhap = ?
                    WHERE id = ?
                ''', (self.nhacungcap_id, self.bienthe_id, self.ngaynhap,
                      self.soluong_nhap, self.gia_nhap, self.id))

                # Cập nhật tồn kho
                quantity_diff = self.soluong_nhap - old_quantity
                cursor.execute('''
                    UPDATE tonkho 
                    SET soluong = soluong + ?
                    WHERE bienthe_id = ?
                ''', (quantity_diff, self.bienthe_id))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            try:
                # Lấy số lượng trước khi xóa
                cursor.execute('SELECT soluong_nhap FROM nhacungcap_sanpham WHERE id = ?', (self.id,))
                quantity = cursor.fetchone()[0]

                # Xóa bản ghi
                cursor.execute('DELETE FROM nhacungcap_sanpham WHERE id = ?', (self.id,))

                # Cập nhật tồn kho
                cursor.execute('''
                    UPDATE tonkho 
                    SET soluong = soluong - ?
                    WHERE bienthe_id = ?
                ''', (quantity, self.bienthe_id))

                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close() 