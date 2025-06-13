import sqlite3

db_path = "database/ministore_db.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Kiểm tra cột store_id đã tồn tại chưa
cursor.execute("PRAGMA table_info(hoadon)")
columns = [col[1] for col in cursor.fetchall()]
if "store_id" not in columns:
    cursor.execute("ALTER TABLE hoadon ADD COLUMN store_id INTEGER")
    print("Đã thêm cột store_id vào bảng hoadon.")
else:
    print("Bảng hoadon đã có cột store_id.")

conn.commit()
conn.close() 