import sqlite3
import os

def update_database():
    # Đường dẫn đến file database
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    
    # Kết nối đến database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Đọc file SQL
        with open(os.path.join(os.path.dirname(__file__), 'update_tables.sql'), 'r') as file:
            sql_commands = file.read()
        
        # Thực thi các câu lệnh SQL
        cursor.executescript(sql_commands)
        
        # Lưu thay đổi
        conn.commit()
        print("Cập nhật database thành công!")
        
    except Exception as e:
        print(f"Lỗi khi cập nhật database: {str(e)}")
        conn.rollback()
    
    finally:
        # Đóng kết nối
        conn.close()

if __name__ == "__main__":
    update_database() 