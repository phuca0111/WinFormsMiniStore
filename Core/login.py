import sqlite3
import hashlib
import os

def get_db_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Database', 'ministore_db.sqlite')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_login(username, password):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute('''
        SELECT tk.username, nv.ten, tk.nhanvien_id
        FROM taikhoan tk
        JOIN nhanvien nv ON tk.nhanvien_id = nv.id
        WHERE tk.username = ? AND tk.password = ?
    ''', (username, hashed))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return None
    # Lấy danh sách quyền
    nhanvien_id = user[2]
    cursor.execute('''
        SELECT pq.tenquyen FROM nhanvien_phanquyen npq
        JOIN phanquyen pq ON npq.phanquyen_id = pq.id
        WHERE npq.nhanvien_id = ?
    ''', (nhanvien_id,))
    roles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return (user[0], user[1], roles)  # username, tên, [danh sách quyền] 