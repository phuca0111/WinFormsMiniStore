import sqlite3

class Product:
    def __init__(self, id=None, ten=None, theloai_id=None, hangsanxuat_id=None):
        self.id = id
        self.ten = ten
        self.theloai_id = theloai_id
        self.hangsanxuat_id = hangsanxuat_id

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, theloai_id, hangsanxuat_id FROM sanpham')
        rows = cursor.fetchall()
        conn.close()
        return [Product(id=row[0], ten=row[1], theloai_id=row[2], hangsanxuat_id=row[3]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, theloai_id, hangsanxuat_id FROM sanpham WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Product(id=row[0], ten=row[1], theloai_id=row[2], hangsanxuat_id=row[3])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO sanpham (ten, theloai_id, hangsanxuat_id) VALUES (?, ?, ?)', (self.ten, self.theloai_id, self.hangsanxuat_id))
            self.id = cursor.lastrowid
        else:
            cursor.execute('UPDATE sanpham SET ten = ?, theloai_id = ?, hangsanxuat_id = ? WHERE id = ?', (self.ten, self.theloai_id, self.hangsanxuat_id, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sanpham WHERE id = ?', (self.id,))
            conn.commit()
            conn.close() 