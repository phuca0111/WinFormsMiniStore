import sqlite3

db_path = "database/ministore_db.sqlite"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS thongtincuahang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten_cua_hang TEXT NOT NULL,
    dia_chi TEXT,
    so_dien_thoai TEXT,
    ma_so_thue TEXT,
    website TEXT,
    ghi_chu TEXT
)
""")

conn.commit()
conn.close()

print("Đã tạo bảng thongtincuahang thành công!") 