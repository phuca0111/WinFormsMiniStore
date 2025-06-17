import tkinter as tk
from tkinter import ttk
import sqlite3

class EditDeleteLogView(tk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        columns = ("ID", "Ngày giờ", "Người thao tác", "Hành động", "Bảng", "ID bản ghi", "Tên sản phẩm", "Trường bị sửa", "Giá trị trước", "Giá trị sau")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, ngay_gio, nguoi_thao_tac, hanh_dong, bang, id_ban_ghi, ten_san_pham, truong_bi_sua, gia_tri_truoc, gia_tri_sau FROM log_edit_delete ORDER BY ngay_gio DESC")
        rows = cursor.fetchall()
        conn.close()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lịch sử chỉnh sửa/xóa dữ liệu")
    root.geometry("1300x500")
    EditDeleteLogView(root)
    root.mainloop() 