import sqlite3

class Supplier:
    def __init__(self, id=None, ten=None, diachi=None, sdt=None, gmail=None):
        self.id = id
        self.ten = ten
        self.diachi = diachi
        self.sdt = sdt
        self.gmail = gmail

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, diachi, sdt, gmail FROM nhacungcap')
        rows = cursor.fetchall()
        conn.close()
        return [Supplier(id=row[0], ten=row[1], diachi=row[2], sdt=row[3], gmail=row[4]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, ten, diachi, sdt, gmail FROM nhacungcap WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Supplier(id=row[0], ten=row[1], diachi=row[2], sdt=row[3], gmail=row[4])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('''
                INSERT INTO nhacungcap (ten, diachi, sdt, gmail) 
                VALUES (?, ?, ?, ?)
            ''', (self.ten, self.diachi, self.sdt, self.gmail))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE nhacungcap 
                SET ten = ?, diachi = ?, sdt = ?, gmail = ? 
                WHERE id = ?
            ''', (self.ten, self.diachi, self.sdt, self.gmail, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM nhacungcap WHERE id = ?', (self.id,))
            conn.commit()
            conn.close() 