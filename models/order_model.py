import sqlite3
from datetime import datetime

class Order:
    def __init__(self, id=None, ma_hoa_don=None, nhanvien_id=None, khachhang_id=None, ngay=None, tongtien=None, tien_lam_tron=None, tien_khach_dua=None, tien_thoi_lai=None, store_id=None):
        self.id = id
        self.ma_hoa_don = ma_hoa_don
        self.nhanvien_id = nhanvien_id
        self.khachhang_id = khachhang_id
        self.ngay = ngay
        self.tongtien = tongtien
        self.tien_lam_tron = tien_lam_tron
        self.tien_khach_dua = tien_khach_dua
        self.tien_thoi_lai = tien_thoi_lai
        self.store_id = store_id

class OrderDetail:
    def __init__(self, id=None, hoadon_id=None, bienthe_id=None, ten_hang=None, soluong=None, dongia=None, thanh_tien=None):
        self.id = id
        self.hoadon_id = hoadon_id
        self.bienthe_id = bienthe_id
        self.ten_hang = ten_hang
        self.soluong = soluong
        self.dongia = dongia
        self.thanh_tien = thanh_tien

class OrderModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def _execute_query(self, query, params=()):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor

    def get_all_orders(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT hd.id, hd.ma_hoa_don, nv.ten, kh.ten, hd.ngay, hd.tongtien
            FROM hoadon hd
            JOIN nhanvien nv ON hd.nhanvien_id = nv.id
            LEFT JOIN khachhang kh ON hd.khachhang_id = kh.id
            ORDER BY hd.ngay DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_order_details(self, order_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, hoadon_id, bienthe_id, ten_hang, soluong, dongia, thanh_tien
            FROM hoadon_chitiet
            WHERE hoadon_id = ?
        ''', (order_id,))
        rows = cursor.fetchall()
        conn.close()
        return [OrderDetail(*row) for row in rows]

    def delete_order(self, order_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hoadon_chitiet WHERE hoadon_id = ?", (order_id,))
            cursor.execute("DELETE FROM hoadon WHERE id = ?", (order_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa đơn hàng: {e}")
            return False 