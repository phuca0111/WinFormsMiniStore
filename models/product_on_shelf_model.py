import sqlite3

class ProductOnShelfModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ks.kehang_id, k.ten, ks.bienthe_id, sp.ten, spbt.ten_bienthe, ks.soluong
            FROM kehang_sanpham ks
            JOIN kehang k ON ks.kehang_id = k.id
            JOIN sanpham_bienthe spbt ON ks.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
        ''')
        data = cursor.fetchall()
        conn.close()
        return data

    def add(self, kehang_id, bienthe_id, soluong):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kehang_sanpham (kehang_id, bienthe_id, soluong) VALUES (?, ?, ?)", (kehang_id, bienthe_id, soluong))
        conn.commit()
        conn.close()

    def update(self, kehang_id, bienthe_id, soluong):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE kehang_sanpham SET soluong=? WHERE kehang_id=? AND bienthe_id=?", (soluong, kehang_id, bienthe_id))
        conn.commit()
        conn.close()

    def delete(self, kehang_id, bienthe_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kehang_sanpham WHERE kehang_id=? AND bienthe_id=?", (kehang_id, bienthe_id))
        conn.commit()
        conn.close()

    def get_all_shelves(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten FROM kehang")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_all_variants(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT spbt.id, sp.ten, spbt.ten_bienthe
            FROM sanpham_bienthe spbt
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
        ''')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_total_on_shelves_by_variant(self, bienthe_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(soluong) FROM kehang_sanpham WHERE bienthe_id=?", (bienthe_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result and result[0] is not None else 0 