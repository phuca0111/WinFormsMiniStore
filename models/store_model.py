import sqlite3
from typing import List, Optional, Tuple

class StoreModel:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_all_stores(self) -> List[Tuple]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM thongtincuahang")
            return cursor.fetchall()

    def get_store_by_id(self, store_id: int) -> Optional[Tuple]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM thongtincuahang WHERE id = ?", (store_id,))
            return cursor.fetchone()

    def add_store(self, ten_cua_hang: str, dia_chi: str = None, so_dien_thoai: str = None,
                 ma_so_thue: str = None, website: str = None, ghi_chu: str = None) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO thongtincuahang (ten_cua_hang, dia_chi, so_dien_thoai, ma_so_thue, website, ghi_chu)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ten_cua_hang, dia_chi, so_dien_thoai, ma_so_thue, website, ghi_chu))
            conn.commit()
            return cursor.lastrowid

    def update_store(self, store_id: int, ten_cua_hang: str = None, dia_chi: str = None,
                    so_dien_thoai: str = None, ma_so_thue: str = None, website: str = None,
                    ghi_chu: str = None) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            values = []
            if ten_cua_hang is not None:
                updates.append("ten_cua_hang = ?")
                values.append(ten_cua_hang)
            if dia_chi is not None:
                updates.append("dia_chi = ?")
                values.append(dia_chi)
            if so_dien_thoai is not None:
                updates.append("so_dien_thoai = ?")
                values.append(so_dien_thoai)
            if ma_so_thue is not None:
                updates.append("ma_so_thue = ?")
                values.append(ma_so_thue)
            if website is not None:
                updates.append("website = ?")
                values.append(website)
            if ghi_chu is not None:
                updates.append("ghi_chu = ?")
                values.append(ghi_chu)
            if not updates:
                return False
            values.append(store_id)
            query = f"UPDATE thongtincuahang SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
            return True

    def delete_store(self, store_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM thongtincuahang WHERE id = ?", (store_id,))
            conn.commit()
            return cursor.rowcount > 0 