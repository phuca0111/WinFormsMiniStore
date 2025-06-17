import sqlite3
import os

def create_tables():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Tạo bảng phanquyen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phanquyen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ten_quyen TEXT NOT NULL UNIQUE
            )
        ''')

        # Tạo bảng nhanvien_phanquyen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nhanvien_phanquyen (
                nhanvien_id INTEGER,
                phanquyen_id INTEGER,
                PRIMARY KEY (nhanvien_id, phanquyen_id),
                FOREIGN KEY (nhanvien_id) REFERENCES nhanvien (id),
                FOREIGN KEY (phanquyen_id) REFERENCES phanquyen (id)
            )
        ''')

        # Thêm các quyền cơ bản
        cursor.execute('''
            INSERT OR IGNORE INTO phanquyen (ten_quyen)
            VALUES 
                ('Quản lý sản phẩm'),
                ('Quản lý nhà cung cấp'),
                ('Quản lý nhập hàng')
        ''')

        conn.commit()
        print("Đã tạo bảng phanquyen và nhanvien_phanquyen thành công!")
    except Exception as e:
        print(f"Lỗi: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables() 