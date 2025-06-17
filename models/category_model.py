import sqlite3

class Category:
    def __init__(self, id=None, ten=None):
        self.id = id
        self.ten = ten

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten FROM theloai")
        rows = cursor.fetchall()
        conn.close()
        return [Category(id=row[0], ten=row[1]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten FROM theloai WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Category(id=row[0], ten=row[1])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO theloai (ten) VALUES (?)", (self.ten,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE theloai SET ten = ? WHERE id = ?", (self.ten, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM theloai WHERE id = ?", (self.id,))
            conn.commit()
            conn.close() 