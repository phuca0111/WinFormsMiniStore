import sqlite3

class ProductVariant:
    def __init__(self, id=None, sanpham_id=None, ten_bienthe=None, gia=None, barcode=None):
        self.id = id
        self.sanpham_id = sanpham_id
        self.ten_bienthe = ten_bienthe
        self.gia = gia
        self.barcode = barcode

    @staticmethod
    def get_all():
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, sanpham_id, ten_bienthe, gia, barcode FROM sanpham_bienthe')
        rows = cursor.fetchall()
        conn.close()
        return [ProductVariant(id=row[0], sanpham_id=row[1], ten_bienthe=row[2], gia=row[3], barcode=row[4]) for row in rows]

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, sanpham_id, ten_bienthe, gia, barcode FROM sanpham_bienthe WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return ProductVariant(id=row[0], sanpham_id=row[1], ten_bienthe=row[2], gia=row[3], barcode=row[4])
        return None

    def save(self):
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO sanpham_bienthe (sanpham_id, ten_bienthe, gia, barcode) VALUES (?, ?, ?, ?)', (self.sanpham_id, self.ten_bienthe, self.gia, self.barcode))
            self.id = cursor.lastrowid
        else:
            cursor.execute('UPDATE sanpham_bienthe SET sanpham_id = ?, ten_bienthe = ?, gia = ?, barcode = ? WHERE id = ?', (self.sanpham_id, self.ten_bienthe, self.gia, self.barcode, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = sqlite3.connect('Database/ministore_db.sqlite')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sanpham_bienthe WHERE id = ?', (self.id,))
            conn.commit()
            conn.close() 