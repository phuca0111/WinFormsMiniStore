import tkinter as tk
from tkinter import ttk
import sqlite3

class ImportLogView(tk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        columns = ("ID", "Ngày giờ nhập", "Người thao tác", "Mã sản phẩm", "Tên sản phẩm", "Số lượng", "Giá nhập", "Số lô", "Hạn dùng")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, ngay_gio_nhap, nguoi_nhap, ma_san_pham, ten_san_pham, so_luong, gia_nhap, so_lo, han_dung FROM log_nhap_hang ORDER BY ngay_gio_nhap DESC")
        rows = cursor.fetchall()
        conn.close()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

# Để sử dụng độc lập:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lịch sử nhập hàng")
    root.geometry("1100x500")
    ImportLogView(root)
    root.mainloop() 