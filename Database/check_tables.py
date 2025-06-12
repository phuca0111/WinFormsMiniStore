import sqlite3
import os

def check_tables():
    # Đường dẫn đến file database
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    
    # Kết nối đến database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Kiểm tra cấu trúc bảng hoadon
        print("\nCấu trúc bảng hoadon:")
        cursor.execute("PRAGMA table_info(hoadon)")
        columns = cursor.fetchall()
        for column in columns:
            print(f"Cột {column[0]}: {column[1]} ({column[2]})")
        
        # Kiểm tra cấu trúc bảng hoadon_chitiet
        print("\nCấu trúc bảng hoadon_chitiet:")
        cursor.execute("PRAGMA table_info(hoadon_chitiet)")
        columns = cursor.fetchall()
        for column in columns:
            print(f"Cột {column[0]}: {column[1]} ({column[2]})")
        
    except Exception as e:
        print(f"Lỗi khi kiểm tra: {str(e)}")
    
    finally:
        # Đóng kết nối
        conn.close()

if __name__ == "__main__":
    check_tables() 