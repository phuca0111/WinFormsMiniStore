import tkinter as tk
from tkinter import ttk, messagebox
from src.core.shelf_core import ShelfCore

class ShelfView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.core = ShelfCore(db_path)
        self.window = tk.Toplevel(parent)
        self.window.title("Quản lý kệ hàng")
        self.window.geometry("400x400")
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=("ID", "Tên kệ"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên kệ", text="Tên kệ")
        self.tree.column("ID", width=50)
        self.tree.column("Tên kệ", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        entry_frame = ttk.Frame(frame)
        entry_frame.pack(fill=tk.X, pady=5)
        ttk.Label(entry_frame, text="Tên kệ:").pack(side=tk.LEFT)
        self.entry_ten = ttk.Entry(entry_frame)
        self.entry_ten.pack(side=tk.LEFT, padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Thêm", command=self.add_shelf).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Sửa", command=self.update_shelf).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Xóa", command=self.delete_shelf).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Làm mới", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for shelf in self.core.get_all_shelves():
            self.tree.insert('', tk.END, values=shelf)
        self.entry_ten.delete(0, tk.END)
        self.selected_id = None

    def add_shelf(self):
        ten = self.entry_ten.get().strip()
        if not ten:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên kệ!")
            return
        self.core.add_shelf(ten)
        self.load_data()

    def update_shelf(self):
        if not hasattr(self, 'selected_id') or not self.selected_id:
            messagebox.showwarning("Chọn kệ", "Vui lòng chọn kệ để sửa!")
            return
        ten = self.entry_ten.get().strip()
        if not ten:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên kệ!")
            return
        self.core.update_shelf(self.selected_id, ten)
        self.load_data()

    def delete_shelf(self):
        if not hasattr(self, 'selected_id') or not self.selected_id:
            messagebox.showwarning("Chọn kệ", "Vui lòng chọn kệ để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa kệ này?"):
            self.core.delete_shelf(self.selected_id)
            self.load_data()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.selected_id = values[0]
            self.entry_ten.delete(0, tk.END)
            self.entry_ten.insert(0, values[1]) 