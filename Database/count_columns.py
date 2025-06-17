import sqlite3
import os

def count_columns():
    # Đường dẫn đến file database
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    
    # Kết nối đến database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Lấy thông tin cột từ bảng hoadon_chitiet
        cursor.execute("PRAGMA table_info(hoadon_chitiet)")
        columns = cursor.fetchall()
        
        # Hiển thị số lượng cột
        print(f"Số lượng cột trong bảng hoadon_chitiet: {len(columns)}")
        
    except Exception as e:
        print(f"Lỗi khi kiểm tra số lượng cột: {str(e)}")
    
    finally:
        # Đóng kết nối
        conn.close()

if __name__ == "__main__":
    count_columns() 