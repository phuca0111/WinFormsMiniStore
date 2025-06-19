import sqlite3
from datetime import datetime

def log_edit_delete(nguoi_thao_tac, hanh_dong, bang, id_ban_ghi, ten_san_pham=None, truong_bi_sua=None, gia_tri_truoc=None, gia_tri_sau=None, db_path='Database/ministore_db.sqlite'):
    ngay_gio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO log_edit_delete (
                ngay_gio, nguoi_thao_tac, hanh_dong, bang, id_ban_ghi, ten_san_pham, truong_bi_sua, gia_tri_truoc, gia_tri_sau
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ngay_gio, nguoi_thao_tac, hanh_dong, bang, id_ban_ghi, ten_san_pham, truong_bi_sua, gia_tri_truoc, gia_tri_sau))
        conn.commit()

def log_ban_hang(nguoi_thao_tac, ma_san_pham, ten_san_pham, so_luong, don_gia, thanh_tien, loai_xuat, db_path='Database/ministore_db.sqlite'):
    ngay_gio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO log_ban_hang (
                ngay_gio, nguoi_thao_tac, ma_san_pham, ten_san_pham, so_luong, don_gia, thanh_tien, loai_xuat
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ngay_gio, nguoi_thao_tac, ma_san_pham, ten_san_pham, so_luong, don_gia, thanh_tien, loai_xuat))
        conn.commit()
    finally:
        conn.close() 