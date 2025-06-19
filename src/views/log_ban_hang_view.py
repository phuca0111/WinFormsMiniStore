import tkinter as tk
from tkinter import ttk
import sqlite3

class LogBanHangView(tk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("LogBanHang.Treeview.Heading", font=("Segoe UI", 12, "bold"), foreground="#222", background="#EEF2F6", relief="flat")
        style.configure("LogBanHang.Treeview", font=("Segoe UI", 11), rowheight=30, background="#EEF2F6", fieldbackground="#EEF2F6", borderwidth=0)
        columns = ("ID", "Ngày giờ", "Người thao tác", "Mã sản phẩm", "Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền", "Loại xuất")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="LogBanHang.Treeview")
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, ngay_gio, nguoi_thao_tac, ma_san_pham, ten_san_pham, so_luong, don_gia, thanh_tien, loai_xuat FROM log_ban_hang ORDER BY ngay_gio DESC")
        rows = cursor.fetchall()
        conn.close()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lịch sử bán hàng")
    root.geometry("1300x500")
    LogBanHangView(root)
    root.mainloop() 