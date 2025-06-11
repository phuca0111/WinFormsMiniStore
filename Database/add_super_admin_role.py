import sqlite3
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO phanquyen (tenquyen) VALUES (?)", ("Quản lý toàn bộ",))
    conn.commit()
    conn.close()
    print("Đã thêm quyền 'Quản lý toàn bộ'!")

if __name__ == "__main__":
    main() 