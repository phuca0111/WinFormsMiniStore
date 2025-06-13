import sqlite3

conn = sqlite3.connect('database/ministore_db.sqlite')
cursor = conn.cursor()
cursor.execute("INSERT INTO phanquyen (tenquyen) VALUES ('Quản lý cửa hàng')")
conn.commit()
conn.close()

print('Đã thêm quyền Quản lý cửa hàng!') 