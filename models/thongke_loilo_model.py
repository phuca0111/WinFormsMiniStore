import sqlite3
import os

class ThongKeLoiLoModel:
    def __init__(self, db_path=None):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Database', 'ministore_db.sqlite')

    def get_doanhthu_data(self, kieu):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if kieu == 'ngày':
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
        elif kieu == 'tháng':
            group = "strftime('%Y-%m', hd.ngay)"
            select = "strftime('%Y-%m', hd.ngay)"
        elif kieu == 'năm':
            group = "strftime('%Y', hd.ngay)"
            select = "strftime('%Y', hd.ngay)"
        else:
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
        query = f'''
            SELECT {select} as thoigian,
                IFNULL(SUM(hdct.soluong * hdct.dongia), 0) AS doanh_thu
            FROM hoadon hd
            LEFT JOIN hoadon_chitiet hdct ON hd.id = hdct.hoadon_id
            GROUP BY {group}
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_loinhuan_data(self, kieu):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if kieu == 'ngày':
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
        elif kieu == 'tháng':
            group = "strftime('%Y-%m', hd.ngay)"
            select = "strftime('%Y-%m', hd.ngay)"
        elif kieu == 'năm':
            group = "strftime('%Y', hd.ngay)"
            select = "strftime('%Y', hd.ngay)"
        else:
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
        query = f'''
            SELECT {select} as thoigian,
                IFNULL(SUM(hdct.soluong * (hdct.dongia - hdct.gia_nhap)), 0) AS loinhuan
            FROM hoadon hd
            LEFT JOIN hoadon_chitiet hdct ON hd.id = hdct.hoadon_id
            GROUP BY {group}
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_banchay_data(self, top_n):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sp.ten, SUM(hdct.soluong) as tong_ban
            FROM hoadon_chitiet hdct
            JOIN sanpham_bienthe spbt ON hdct.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            GROUP BY sp.id
            ORDER BY tong_ban DESC
            LIMIT ?
        ''', (top_n,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_hethan_data(self, days):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
            SELECT sp.ten, SUM(nsp.so_luong_con_lai)
            FROM nhacungcap_sanpham nsp
            JOIN sanpham_bienthe spbt ON nsp.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            WHERE nsp.so_luong_con_lai > 0
                AND nsp.han_su_dung IS NOT NULL
                AND nsp.han_su_dung != ''
                AND DATE(nsp.han_su_dung) <= DATE('now', '+' || ? || ' days')
                AND DATE(nsp.han_su_dung) >= DATE('now')
            GROUP BY sp.id
        '''
        cursor.execute(query, (days,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_loilo_data(self, kieu):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if kieu == 'ngày':
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
            group_phieu = "DATE(ngay_huy)"
            select_phieu = "DATE(ngay_huy)"
        elif kieu == 'tháng':
            group = "strftime('%Y-%m', hd.ngay)"
            select = "strftime('%Y-%m', hd.ngay)"
            group_phieu = "strftime('%Y-%m', ngay_huy)"
            select_phieu = "strftime('%Y-%m', ngay_huy)"
        elif kieu == 'năm':
            group = "strftime('%Y', hd.ngay)"
            select = "strftime('%Y', hd.ngay)"
            group_phieu = "strftime('%Y', ngay_huy)"
            select_phieu = "strftime('%Y', ngay_huy)"
        elif kieu == 'tuần':
            group = "strftime('%Y-%W', hd.ngay)"
            select = "strftime('%Y-%W', hd.ngay)"
            group_phieu = "strftime('%Y-%W', ngay_huy)"
            select_phieu = "strftime('%Y-%W', ngay_huy)"
        else:
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
            group_phieu = "DATE(ngay_huy)"
            select_phieu = "DATE(ngay_huy)"
        # Lấy dữ liệu bán hàng
        query = f'''
            SELECT {select} as thoigian,
                IFNULL(SUM(hdct.soluong * hdct.dongia), 0) AS doanh_thu,
                IFNULL(SUM(hdct.soluong * hdct.gia_nhap), 0) AS chi_phi_nhap
            FROM hoadon hd
            LEFT JOIN hoadon_chitiet hdct ON hd.id = hdct.hoadon_id
            GROUP BY {group}
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        # Lấy dữ liệu tiêu hủy
        query_phieu = f'''
            SELECT {select_phieu} as thoigian, IFNULL(SUM(so_luong_huy * gia_nhap), 0) as tong_tieu_huy
            FROM phieu_tieu_huy
            GROUP BY {group_phieu}
        '''
        cursor.execute(query_phieu)
        phieu_data = {r[0]: r[1] for r in cursor.fetchall()}
        # Ghép dữ liệu
        result = []
        for row in rows:
            thoigian, doanh_thu, chi_phi_nhap = row
            chi_phi_tieu_huy = phieu_data.get(thoigian, 0)
            chi_phi_nhap_tong = chi_phi_nhap + chi_phi_tieu_huy
            loi = max(doanh_thu - chi_phi_nhap_tong, 0)
            lo = min(doanh_thu - chi_phi_nhap_tong, 0)
            result.append((thoigian, doanh_thu, chi_phi_nhap_tong, loi, lo))
        # Thêm các mốc chỉ có tiêu hủy mà không có bán hàng
        for thoigian in phieu_data:
            if not any(r[0] == thoigian for r in result):
                doanh_thu = 0
                chi_phi_nhap = 0
                chi_phi_tieu_huy = phieu_data[thoigian]
                chi_phi_nhap_tong = chi_phi_nhap + chi_phi_tieu_huy
                loi = max(doanh_thu - chi_phi_nhap_tong, 0)
                lo = min(doanh_thu - chi_phi_nhap_tong, 0)
                result.append((thoigian, doanh_thu, chi_phi_nhap_tong, loi, lo))
        conn.close()
        return result

    # ... (các hàm khác sẽ bổ sung sau) ... 