import sqlite3

class ShelfModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_all_shelves(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten FROM kehang")
        shelves = cursor.fetchall()
        conn.close()
        return shelves

    def add_shelf(self, ten):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kehang (ten) VALUES (?)", (ten,))
        conn.commit()
        conn.close()

    def update_shelf(self, shelf_id, ten):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE kehang SET ten=? WHERE id=?", (ten, shelf_id))
        conn.commit()
        conn.close()

    def delete_shelf(self, shelf_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kehang WHERE id=?", (shelf_id,))
        conn.commit()
        conn.close() 