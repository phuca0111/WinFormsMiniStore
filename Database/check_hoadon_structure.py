import sqlite3
import os

def check_hoadon_structure():
    # Đường dẫn đến file database
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    
    # Kết nối đến database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Lấy thông tin chi tiết về cấu trúc bảng
        cursor.execute("PRAGMA table_info(hoadon)")
        columns = cursor.fetchall()
        
        print("Chi tiết cấu trúc bảng hoadon:")
        for column in columns:
            print(f"Cột {column[0]}: {column[1]} ({column[2]})")
        
    except Exception as e:
        print(f"Lỗi khi kiểm tra cấu trúc: {str(e)}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_hoadon_structure() 