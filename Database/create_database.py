import sqlite3
import os

def create_database():
    # Đường dẫn đến file database
    db_path = os.path.join(os.path.dirname(__file__), "ministore_db.sqlite")
    
    # Kết nối đến database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Đọc file SQL
    sql_file = os.path.join(os.path.dirname(__file__), "ministore_db.sql")
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
                print(f"Error executing command: {command}")
                print(f"Error: {e}")
    
    # Tạo bảng nhanvien_phanquyen nếu chưa có
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nhanvien_phanquyen (
            nhanvien_id INTEGER,
            phanquyen_id INTEGER,
            PRIMARY KEY (nhanvien_id, phanquyen_id),
            FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id),
            FOREIGN KEY (phanquyen_id) REFERENCES phanquyen(id)
        )
    ''')
    
    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()
    
    print("Database created successfully!")

if __name__ == "__main__":
    create_database() 