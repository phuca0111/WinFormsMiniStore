import sqlite3
import os

def update_table():
    try:
        # Đường dẫn đúng tới file database
        db_path = 'Database/ministore_db.sqlite'
        if not os.path.exists(db_path):
            print(f"Lỗi: Không tìm thấy file {db_path}")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Kiểm tra bảng cũ có tồn tại không
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kehang_sanpham'")
        if not cursor.fetchone():
            print("Lỗi: Không tìm thấy bảng kehang_sanpham")
            return

        print("Bắt đầu cập nhật cấu trúc bảng kehang_sanpham...")
        
        # Tạo bảng tạm với cấu trúc mới
        cursor.execute('''
            CREATE TABLE kehang_sanpham_temp (
                kehang_id INTEGER,
                bienthe_id INTEGER,
                soluong INTEGER,
                FOREIGN KEY (kehang_id) REFERENCES kehang(id),
                FOREIGN KEY (bienthe_id) REFERENCES sanpham_bienthe(id)
            )
        ''')
        print("Đã tạo bảng tạm thành công")
        
        # Copy dữ liệu từ bảng cũ sang bảng tạm
        cursor.execute('''
            INSERT INTO kehang_sanpham_temp (kehang_id, bienthe_id, soluong)
            SELECT ks.kehang_id, spbt.id, ks.soluong
            FROM kehang_sanpham ks
            JOIN sanpham sp ON ks.sanpham_id = sp.id
            JOIN sanpham_bienthe spbt ON sp.id = spbt.sanpham_id
        ''')
        print("Đã copy dữ liệu sang bảng tạm")
        
        # Xóa bảng cũ
        cursor.execute('DROP TABLE kehang_sanpham')
        print("Đã xóa bảng cũ")
        
        # Đổi tên bảng tạm thành tên cũ
        cursor.execute('ALTER TABLE kehang_sanpham_temp RENAME TO kehang_sanpham')
        print("Đã đổi tên bảng tạm thành công")
        
        conn.commit()
        print("Đã cập nhật cấu trúc bảng kehang_sanpham thành công!")

    except sqlite3.Error as e:
        print(f"Lỗi SQLite: {e}")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_table() 