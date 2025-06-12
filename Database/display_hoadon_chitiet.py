import sqlite3
import os

def display_hoadon_chitiet():
    # Đường dẫn đến file database
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    
    # Kết nối đến database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Lấy dữ liệu từ bảng hoadon_chitiet
        cursor.execute("SELECT * FROM hoadon_chitiet")
        rows = cursor.fetchall()
        
        # Hiển thị dữ liệu
        print("Dữ liệu trong bảng hoadon_chitiet:")
        for row in rows:
            print(row)
        
    except Exception as e:
        print(f"Lỗi khi hiển thị dữ liệu: {str(e)}")
    
    finally:
        # Đóng kết nối
        conn.close()

if __name__ == "__main__":
    display_hoadon_chitiet() 