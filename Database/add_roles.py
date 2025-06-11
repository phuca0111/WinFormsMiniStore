import sqlite3
import os

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'ministore_db.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    roles = [
        'Quản lý khách hàng',
        'Quản lý thanh toán',
        'Quản lý sản phẩm',
        'Quản lý loại sản phẩm',
        'Quản lý biến thể sản phẩm',
        'Quản lý nhà sản xuất',
        'Quản lý đơn hàng',
        'Quản lý tồn kho',
        'Quản lý tài khoản',
        'Quản trị hệ thống'
    ]
    for role in roles:
        cursor.execute("INSERT OR IGNORE INTO phanquyen (tenquyen) VALUES (?)", (role,))
    conn.commit()
    conn.close()
    print("Đã thêm các quyền chi tiết vào hệ thống!")

if __name__ == "__main__":
    main() 