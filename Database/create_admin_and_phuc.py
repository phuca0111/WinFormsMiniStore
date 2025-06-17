import sqlite3
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Thêm/quyền admin
    cursor.execute("SELECT id FROM nhanvien WHERE ten = ?", ('Admin',))
    row = cursor.fetchone()
    if row:
        admin_id = row[0]
    else:
        cursor.execute("INSERT INTO nhanvien (ten, sdt, gmail, gioitinh, ngaysinh) VALUES (?, ?, ?, ?, ?)",
                       ('Admin', '0123456789', 'admin@example.com', 'Nam', '2000-01-01'))
        admin_id = cursor.lastrowid
    # Tạo tài khoản admin nếu chưa có
    username = 'admin'
    password = '123456'
    hashed = hash_password(password)
    cursor.execute("SELECT id FROM taikhoan WHERE username = ?", (username,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO taikhoan (nhanvien_id, username, password) VALUES (?, ?, ?)", (admin_id, username, hashed))
    # Gán quyền cao nhất cho admin
    cursor.execute("SELECT id FROM phanquyen WHERE tenquyen IN (?, ?)", ("Quản lý toàn bộ", "Quản trị hệ thống"))
    role_ids = [r[0] for r in cursor.fetchall()]
    for role_id in role_ids:
        cursor.execute("INSERT OR IGNORE INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id) VALUES (?, ?)", (admin_id, role_id))

    # Thêm nhân viên tên Phúc
    cursor.execute("SELECT id FROM nhanvien WHERE ten = ?", ('Phúc',))
    row = cursor.fetchone()
    if row:
        phuc_id = row[0]
    else:
        cursor.execute("INSERT INTO nhanvien (ten, sdt, gmail, gioitinh, ngaysinh) VALUES (?, ?, ?, ?, ?)",
                       ('Phúc', '0987654321', 'phuc@example.com', 'Nam', '2001-01-01'))
        phuc_id = cursor.lastrowid
    # Tạo tài khoản cho Phúc nếu chưa có
    username2 = 'phuc'
    password2 = '123456'
    hashed2 = hash_password(password2)
    cursor.execute("SELECT id FROM taikhoan WHERE username = ?", (username2,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO taikhoan (nhanvien_id, username, password) VALUES (?, ?, ?)", (phuc_id, username2, hashed2))
    # Gán quyền nhân viên bán hàng cho Phúc
    cursor.execute("SELECT id FROM phanquyen WHERE tenquyen = ?", ("Quản lý khách hàng",))
    row = cursor.fetchone()
    if row:
        role_id = row[0]
        cursor.execute("INSERT OR IGNORE INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id) VALUES (?, ?)", (phuc_id, role_id))
    cursor.execute("SELECT id FROM phanquyen WHERE tenquyen = ?", ("Quản lý thanh toán",))
    row = cursor.fetchone()
    if row:
        role_id = row[0]
        cursor.execute("INSERT OR IGNORE INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id) VALUES (?, ?)", (phuc_id, role_id))
    cursor.execute("SELECT id FROM phanquyen WHERE tenquyen = ?", ("Quản lý đơn hàng",))
    row = cursor.fetchone()
    if row:
        role_id = row[0]
        cursor.execute("INSERT OR IGNORE INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id) VALUES (?, ?)", (phuc_id, role_id))
    conn.commit()
    conn.close()
    print('Đã tạo tài khoản admin (quyền cao nhất) và nhân viên Phúc (quyền bán hàng)!')

if __name__ == "__main__":
    main() 