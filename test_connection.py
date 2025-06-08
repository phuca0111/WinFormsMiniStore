import sqlite3
import os

def test_database_connection():
    try:
        # Kiểm tra xem file database có tồn tại không
        db_path = "Database/ministore_db.sqlite"
        if not os.path.exists(db_path):
            print("Tạo mới database...")
            # Tạo kết nối và database mới
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Đọc và thực thi file SQL
            with open("Database/ministore_db.sql", "r", encoding="utf-8") as sql_file:
                sql_script = sql_file.read()
                cursor.executescript(sql_script)
            
            conn.commit()
            print("Đã tạo database thành công!")
        else:
            # Kết nối với database đã tồn tại
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            print("Kết nối với database thành công!")

        # Test truy vấn đơn giản
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nDanh sách các bảng trong database:")
        for table in tables:
            print(f"- {table[0]}")
            
        conn.close()
        print("\nĐóng kết nối thành công!")
        return True
        
    except sqlite3.Error as e:
        print(f"Có lỗi xảy ra: {e}")
        return False
    except Exception as e:
        print(f"Có lỗi không xác định: {e}")
        return False

if __name__ == "__main__":
    test_database_connection() 