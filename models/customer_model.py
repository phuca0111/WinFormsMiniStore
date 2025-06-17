import sqlite3
from datetime import datetime

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
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding customer: {e}")
            return None
        finally:
            conn.close()

    def delete_customer(self, id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM khachhang WHERE id = ?', (id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting customer: {e}")
            return False
        finally:
            conn.close()

    def update_customer(self, id, name=None, phone=None, email=None, address=None, birthdate=None, gender=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
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
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating customer: {e}")
            return False
        finally:
            conn.close()

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