import sqlite3

#hãng sản xuất
class Producer:
    def __init__(self, id=None, ten=None):
        self.id = id
        self.ten = ten

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten FROM hangsanxuat')
        rows = cursor.fetchall()
        conn.close()
        return [Producer(id=row[0], ten=row[1]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten FROM hangsanxuat WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Producer(id=row[0], ten=row[1])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO hangsanxuat (ten) VALUES (?)', (self.ten,))
            self.id = cursor.lastrowid
        else:
            cursor.execute('UPDATE hangsanxuat SET ten = ? WHERE id = ?', (self.ten, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM hangsanxuat WHERE id = ?', (self.id,))
            conn.commit()
            conn.close() 