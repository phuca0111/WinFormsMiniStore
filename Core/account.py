import sqlite3
import hashlib
import os

def get_db_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Database', 'ministore_db.sqlite')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_roles():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, tenquyen FROM phanquyen')
    roles = cursor.fetchall()
    conn.close()
    return roles

def get_accounts():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tk.id, tk.username, nv.ten, 
            COALESCE(GROUP_CONCAT(pq.tenquyen, ', '), 'None') as quyen, 
            tk.trangthai
        FROM taikhoan tk
        JOIN nhanvien nv ON tk.nhanvien_id = nv.id
        LEFT JOIN nhanvien_phanquyen npq ON nv.id = npq.nhanvien_id
        LEFT JOIN phanquyen pq ON npq.phanquyen_id = pq.id
        GROUP BY tk.id
    ''')
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def add_account(name, phone, email, gender, birthdate, role_ids, username, password):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Tạo nhân viên
        cursor.execute('''
            INSERT INTO nhanvien (ten, sdt, gmail, gioitinh, ngaysinh)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, email, gender, birthdate))
        nhanvien_id = cursor.lastrowid
        # Gán nhiều quyền
        for role_id in role_ids:
            cursor.execute('INSERT INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id) VALUES (?, ?)', (nhanvien_id, role_id))
        # Tạo tài khoản
        hashed = hash_password(password)
        cursor.execute('''
            INSERT INTO taikhoan (nhanvien_id, username, password)
            VALUES (?, ?, ?)
        ''', (nhanvien_id, username, hashed))
        conn.commit()
        return True, 'Tạo tài khoản thành công!'
    except Exception as e:
        conn.rollback()
        return False, f'Lỗi: {e}'
    finally:
        conn.close()

def delete_account(account_id):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Lấy nhanvien_id
        cursor.execute('SELECT nhanvien_id FROM taikhoan WHERE id = ?', (account_id,))
        row = cursor.fetchone()
        if not row:
            return False, 'Không tìm thấy tài khoản!'
        nhanvien_id = row[0]
        # Xóa quyền
        cursor.execute('DELETE FROM nhanvien_phanquyen WHERE nhanvien_id = ?', (nhanvien_id,))
        # Xóa tài khoản
        cursor.execute('DELETE FROM taikhoan WHERE id = ?', (account_id,))
        # Xóa nhân viên (nếu muốn giữ lại nhân viên thì bỏ dòng này)
        cursor.execute('DELETE FROM nhanvien WHERE id = ?', (nhanvien_id,))
        conn.commit()
        return True, 'Đã xóa tài khoản thành công!'
    except Exception as e:
        conn.rollback()
        return False, f'Lỗi: {e}'
    finally:
        conn.close()

def update_account(account_id, name, phone, email, gender, birthdate, role_ids, username, password):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Lấy nhanvien_id
        cursor.execute('SELECT nhanvien_id FROM taikhoan WHERE id = ?', (account_id,))
        row = cursor.fetchone()
        if not row:
            return False, 'Không tìm thấy tài khoản!'
        nhanvien_id = row[0]
        # Cập nhật nhân viên
        cursor.execute('''
            UPDATE nhanvien SET ten=?, sdt=?, gmail=?, gioitinh=?, ngaysinh=? WHERE id=?
        ''', (name, phone, email, gender, birthdate, nhanvien_id))
        # Cập nhật username, password
        if password:
            hashed = hash_password(password)
            cursor.execute('UPDATE taikhoan SET username=?, password=? WHERE id=?', (username, hashed, account_id))
        else:
            cursor.execute('UPDATE taikhoan SET username=? WHERE id=?', (username, account_id))
        # Cập nhật quyền
        cursor.execute('DELETE FROM nhanvien_phanquyen WHERE nhanvien_id=?', (nhanvien_id,))
        for role_id in role_ids:
            cursor.execute('INSERT INTO nhanvien_phanquyen (nhanvien_id, phanquyen_id) VALUES (?, ?)', (nhanvien_id, role_id))
        conn.commit()
        return True, 'Cập nhật tài khoản thành công!'
    except Exception as e:
        conn.rollback()
        return False, f'Lỗi: {e}'
    finally:
        conn.close() 