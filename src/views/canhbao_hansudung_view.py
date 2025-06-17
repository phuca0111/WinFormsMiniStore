import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class CanhBaoHanSuDungView(ttk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data(7)

    def create_widgets(self):
        frame_top = ttk.Frame(self)
        frame_top.pack(fill=tk.X, pady=5)
        ttk.Label(frame_top, text="Cảnh báo sản phẩm sắp hết hạn trước:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.combo_days = ttk.Combobox(frame_top, values=[7, 15, 30], state="readonly", width=5)
        self.combo_days.current(0)
        self.combo_days.pack(side=tk.LEFT, padx=5)
        btn_xem = ttk.Button(frame_top, text="Xem", command=self.on_xem)
        btn_xem.pack(side=tk.LEFT, padx=5)

        columns = ("Sản phẩm", "Biến thể", "Hạn sử dụng", "Số lượng còn lại", "Kệ")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def on_xem(self):
        days = int(self.combo_days.get())
        self.load_data(days)

    def load_data(self, days):
        self.tree.delete(*self.tree.get_children())
        data, today, future = self.get_expiry_data(days)
        print(f"[DEBUG] Hôm nay: {today}, Cảnh báo đến: {future}")
        for row in data:
            self.tree.insert('', tk.END, values=row)

    def get_expiry_data(self, days):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        today = datetime.now().date()
        future = today + timedelta(days=days)
        query = '''
            SELECT sp.ten, spbt.ten_bienthe, nsp.han_su_dung, nsp.so_luong_con_lai, k.ten, nsp.id
            FROM nhacungcap_sanpham nsp
            JOIN sanpham_bienthe spbt ON nsp.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            LEFT JOIN kehang_sanpham ks ON ks.bienthe_id = spbt.id
            LEFT JOIN kehang k ON ks.kehang_id = k.id
            WHERE nsp.so_luong_con_lai > 0
                AND nsp.han_su_dung IS NOT NULL
                AND nsp.han_su_dung != ''
            ORDER BY nsp.han_su_dung ASC, nsp.id ASC
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        filtered = []
        ids_seen = set()
        for r in rows:
            try:
                han = datetime.strptime(r[2], '%Y-%m-%d').date()
                if today <= han <= future:
                    # Đảm bảo không bị trùng lô (nếu có nhiều kệ, chỉ lấy lô đầu tiên)
                    if r[5] not in ids_seen:
                        filtered.append((r[0], r[1], r[2], r[3], r[4] if r[4] else ''))
                        ids_seen.add(r[5])
            except Exception as e:
                print(f"[DEBUG] Lỗi chuyển đổi ngày: {r[2]} - {e}")
        return filtered, today, future 