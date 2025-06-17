import sqlite3

class Inventory:
    def __init__(self, id=None, bienthe_id=None, soluong=0):
        self.id = id
        self.bienthe_id = bienthe_id
        self.soluong = soluong

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, bienthe_id, soluong FROM tonkho')
        rows = cursor.fetchall()
        conn.close()
        return [Inventory(id=row[0], bienthe_id=row[1], soluong=row[2]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, bienthe_id, soluong FROM tonkho WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Inventory(id=row[0], bienthe_id=row[1], soluong=row[2])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO tonkho (bienthe_id, soluong) VALUES (?, ?)', (self.bienthe_id, self.soluong))
            self.id = cursor.lastrowid
        else:
            cursor.execute('UPDATE tonkho SET bienthe_id = ?, soluong = ? WHERE id = ?', (self.bienthe_id, self.soluong, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tonkho WHERE id = ?', (self.id,))
            conn.commit()
            conn.close() 