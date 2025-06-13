import sqlite3
conn = sqlite3.connect('Database/ministore_db.sqlite')
cursor = conn.cursor()
cursor.execute('ALTER TABLE hoadon ADD COLUMN khachhang_id INTEGER;')
conn.commit()
conn.close()
print("Đã thêm cột khachhang_id vào bảng hoadon!") 