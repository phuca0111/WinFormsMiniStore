import sqlite3
import os

def add_supplier_product_permission():
    try:
        # Kết nối đến database
        db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Thêm quyền mới
        cursor.execute('''
            INSERT OR IGNORE INTO phanquyen (tenquyen)
            VALUES ('Quản lý nhập hàng')
        ''')

        # Lấy ID của quyền vừa thêm
        cursor.execute('SELECT id FROM phanquyen WHERE tenquyen = ?', ('Quản lý nhập hàng',))
        permission_id = cursor.fetchone()[0]

        # Gán quyền cho nhân viên có quyền quản lý sản phẩm
        cursor.execute('''
            INSERT OR IGNORE INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id)
            SELECT nv.id, ?
            FROM nhanvien nv
            JOIN nhanvien_phanquyen nvp ON nv.id = nvp.nhanvien_id
            JOIN phanquyen pq ON nvp.phanquyen_id = pq.id
            WHERE pq.tenquyen = 'Quản lý sản phẩm'
        ''', (permission_id,))

        conn.commit()
        print("Đã thêm quyền quản lý nhập hàng thành công!")
    except Exception as e:
        print(f"Lỗi: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_supplier_product_permission() 