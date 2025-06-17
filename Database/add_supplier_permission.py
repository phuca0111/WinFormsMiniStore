import sqlite3
import os

def add_supplier_permission():
    try:
        # Đường dẫn đến file database
        db_path = os.path.join(os.path.dirname(__file__), "ministore_db.sqlite")
        
        # Kết nối đến database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Thêm quyền quản lý nhà cung cấp
        cursor.execute('''
            INSERT OR IGNORE INTO phanquyen (tenquyen)
            VALUES ('Quản lý nhà cung cấp')
        ''')
        
        # Lấy ID của quyền vừa thêm
        cursor.execute('SELECT id FROM phanquyen WHERE tenquyen = ?', ('Quản lý nhà cung cấp',))
        permission_id = cursor.fetchone()[0]
        
        # Gán quyền cho tất cả nhân viên có quyền quản lý sản phẩm
        cursor.execute('''
            INSERT OR IGNORE INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id)
            SELECT DISTINCT nv.id, ?
            FROM nhanvien nv
            JOIN nhanvien_phanquyen npq ON nv.id = npq.nhanvien_id
            JOIN phanquyen pq ON npq.phanquyen_id = pq.id
            WHERE pq.tenquyen = 'Quản lý sản phẩm'
        ''', (permission_id,))
        
        # Lưu thay đổi và đóng kết nối
        conn.commit()
        conn.close()
        
        print("Đã thêm quyền quản lý nhà cung cấp thành công!")
        
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    add_supplier_permission() 