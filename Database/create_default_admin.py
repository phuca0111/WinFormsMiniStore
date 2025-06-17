import sqlite3
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tạo nhân viên mẫu nếu chưa có
    cursor.execute("SELECT id FROM nhanvien WHERE ten = ?", ('Admin',))
    row = cursor.fetchone()
    if row:
        nhanvien_id = row[0]
    else:
        cursor.execute("INSERT INTO nhanvien (ten, sdt, gmail, gioitinh, ngaysinh, phanquyen_id) VALUES (?, ?, ?, ?, ?, ?)",
                       ('Admin', '0123456789', 'admin@example.com', 'Nam', '2000-01-01', 1))
        nhanvien_id = cursor.lastrowid

    # Thêm tài khoản admin
    username = 'admin'
    password = '123456'
    hashed = hash_password(password)
    # Kiểm tra đã có tài khoản admin chưa
    cursor.execute("SELECT id FROM taikhoan WHERE username = ?", (username,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO taikhoan (nhanvien_id, username, password) VALUES (?, ?, ?)", (nhanvien_id, username, hashed))
        print('Tạo tài khoản admin thành công!')
    else:
        print('Tài khoản admin đã tồn tại!')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main() 