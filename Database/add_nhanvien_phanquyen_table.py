import sqlite3
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nhanvien_phanquyen (
            nhanvien_id INTEGER,
            phanquyen_id INTEGER,
            PRIMARY KEY (nhanvien_id, phanquyen_id),
            FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id),
            FOREIGN KEY (phanquyen_id) REFERENCES phanquyen(id)
        )
    ''')
    conn.commit()
    conn.close()
    print('Đã tạo bảng nhanvien_phanquyen!')

if __name__ == '__main__':
    main() 