import sqlite3
from datetime import datetime
from Core.edit_delete_log_core import log_edit_delete

class CustomerModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_customer(self, name, phone, email=None, address=None, birthdate=None, gender=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO khachhang (ten, sdt, gmail, diachi, ngaysinh, gioitinh)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, phone, email, address, birthdate, gender))
            customer_id = cursor.lastrowid
            conn.commit()
            conn.close()
            # Ghi log thêm mới (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            log_edit_delete(nguoi_thao_tac, 'thêm', 'khachhang', customer_id, name, None, None, f'tên: {name}, sdt: {phone}')
            return customer_id
        except sqlite3.Error as e:
            print(f"Error adding customer: {e}")
            return None

    def delete_customer(self, id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT ten FROM khachhang WHERE id = ?', (id,))
            old = cursor.fetchone()
            cursor.execute('DELETE FROM khachhang WHERE id = ?', (id,))
            result = cursor.rowcount > 0
            nguoi_thao_tac = get_last_login_user()
            if old:
                log_edit_delete(nguoi_thao_tac, 'xóa', 'khachhang', id, old[0], None, old[0], None)
            return result
        except sqlite3.Error as e:
            print(f"Error deleting customer: {e}")
            return False
        finally:
            conn.close()

    def update_customer(self, id, name=None, phone=None, email=None, address=None, birthdate=None, gender=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT ten, sdt, gmail, diachi, ngaysinh, gioitinh FROM khachhang WHERE id = ?', (id,))
            old = cursor.fetchone()
            
            # Create dynamic UPDATE query based on provided fields
            update_fields = []
            params = []
            
            if name is not None:
                update_fields.append("ten = ?")
                params.append(name)
            if phone is not None:
                update_fields.append("sdt = ?")
                params.append(phone)
            if email is not None:
                update_fields.append("gmail = ?")
                params.append(email)
            if address is not None:
                update_fields.append("diachi = ?")
                params.append(address)
            if birthdate is not None:
                update_fields.append("ngaysinh = ?")
                params.append(birthdate)
            if gender is not None:
                update_fields.append("gioitinh = ?")
                params.append(gender)

            if not update_fields:
                return False

            query = f"UPDATE khachhang SET {', '.join(update_fields)} WHERE id = ?"
            params.append(id)
            
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            # Ghi log sửa (sau khi đã đóng kết nối)
            nguoi_thao_tac = get_last_login_user()
            if old:
                if name is not None and old[0] != name:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'khachhang', id, name, 'ten', old[0], name)
                if phone is not None and old[1] != phone:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'khachhang', id, name, 'sdt', old[1], phone)
                if email is not None and old[2] != email:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'khachhang', id, name, 'gmail', old[2], email)
                if address is not None and old[3] != address:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'khachhang', id, name, 'diachi', old[3], address)
                if birthdate is not None and old[4] != birthdate:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'khachhang', id, name, 'ngaysinh', old[4], birthdate)
                if gender is not None and old[5] != gender:
                    log_edit_delete(nguoi_thao_tac, 'sửa', 'khachhang', id, name, 'gioitinh', old[5], gender)
            return True
        except sqlite3.Error as e:
            print(f"Error updating customer: {e}")
            return False

    def get_all_customers(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM khachhang')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all customers: {e}")
            return []
        finally:
            conn.close()

    def search_customers(self, keyword):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM khachhang 
                WHERE ten LIKE ? OR sdt LIKE ? OR gmail LIKE ?
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching customers: {e}")
            return []
        finally:
            conn.close()

    def get_customer_by_id(self, id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM khachhang WHERE id = ?', (id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting customer by ID: {e}")
            return None
        finally:
            conn.close()

    def get_customer_by_phone(self, phone):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM khachhang WHERE sdt = ?", (phone,))
            customer = cursor.fetchone()
            conn.close()
            return customer
        except Exception as e:
            print("Error getting customer by phone:", e)
            return None

def get_last_login_user():
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT nhanvien_id FROM nhanvien_login_log ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        cursor.execute('SELECT ten FROM nhanvien WHERE id = ?', (row[0],))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else 'Chưa xác định'
    conn.close()
    return 'Chưa xác định'