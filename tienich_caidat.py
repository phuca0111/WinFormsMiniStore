import sqlite3

db_path = "database/ministore_db.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tienich_caidat (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")
conn.commit()
conn.close()
print("Đã tạo bảng cai dặt thành công!") 