import sqlite3
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Thêm quyền Cài đặt
    cursor.execute("INSERT OR IGNORE INTO phanquyen (tenquyen) VALUES ('Quản lý cài đặt')")
    
    # Gán quyền cho admin
    cursor.execute("SELECT id FROM nhanvien WHERE ten = ?", ('Admin',))
    admin_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM phanquyen WHERE tenquyen = ?", ('Quản lý cài đặt',))
    role_id = cursor.fetchone()[0]
    
    cursor.execute("INSERT OR IGNORE INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id) VALUES (?, ?)", 
                  (admin_id, role_id))
    
    conn.commit()
    conn.close()
    print('Đã thêm quyền Quản lý cài đặt!')

if __name__ == "__main__":
    main() 