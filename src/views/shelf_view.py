import tkinter as tk
from tkinter import ttk, messagebox
from src.core.shelf_core import ShelfCore

class ShelfView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.core = ShelfCore(db_path)
        self.frame = ttk.Frame(parent)

        # Cấu hình grid cho self.frame
        self.frame.grid_rowconfigure(3, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        row_idx = 0

        # Tiêu đề "Quản lý kệ hàng"
        label = ttk.Label(self.frame, text='Quản lý kệ hàng', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=2, padx=20, pady=5, sticky=tk.N)
        row_idx += 1

        main_frame = ttk.Frame(self.frame)
        main_frame.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Tên kệ"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên kệ", text="Tên kệ")
        self.tree.column("ID", width=50,anchor=tk.CENTER)
        self.tree.column("Tên kệ", width=200,anchor=tk.CENTER)
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        entry_frame = ttk.Frame(self.frame)
        entry_frame.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1
        entry_frame.grid_columnconfigure(0, weight=1)
        entry_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(entry_frame, text="Tên kệ:").grid(row=0, padx=5, pady=5, sticky=tk.W)
        self.entry_ten = ttk.Entry(entry_frame)
        self.entry_ten.grid(row=1, padx=5, pady=5, sticky=tk.EW)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)

        ttk.Button(btn_frame, text="Thêm", command=self.add_shelf).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text="Sửa", command=self.update_shelf).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text="Xóa", command=self.delete_shelf).grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text="Làm mới", command=self.load_data).grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)

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