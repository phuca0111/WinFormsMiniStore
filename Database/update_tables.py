import sqlite3
import os

def update_database():
    try:
        # Đường dẫn đến file database
        db_path = os.path.join(os.path.dirname(__file__), "ministore_db.sqlite")
        
        # Kết nối đến database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Đọc file SQL
        sql_file = os.path.join(os.path.dirname(__file__), "update_tables.sql")
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        
        # Tách các câu lệnh SQL
        commands = sql_commands.split(';')
        
        # Thực thi từng câu lệnh
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except sqlite3.Error as e:
                    print(f"Lỗi khi thực thi lệnh: {command}")
                    print(f"Chi tiết lỗi: {e}")
        
        # Lưu thay đổi và đóng kết nối
        conn.commit()
        conn.close()
        
        print("Đã cập nhật cơ sở dữ liệu thành công!")
        
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    update_database() 