import tkinter as tk
from tkinter import ttk, messagebox
from Core.shelf_core import ShelfCore
from models.shelf_model import ShelfModel

class ShelfView(tk.Frame):
    def __init__(self, parent, db_path):
        super().__init__(parent, bg="#eef2f6")
        self.db_path = db_path
        self.core = ShelfCore(db_path)
        self.model = ShelfModel(db_path)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Shelf.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#eef2f6", relief="flat")
        style.configure("Shelf.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        # Khung danh sách
        frame = tk.LabelFrame(self, text='Danh sách kệ', font=("Segoe UI", 12, "bold"), bg="#eef2f6", fg="#232a36", bd=0)
        frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=(24, 8))
        columns = ("ID", "Tên kệ")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=12, style="Shelf.Treeview")
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Tên kệ', width=220, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        # Border bo tròn giả lập
        frame.config(highlightbackground="#dde2e6", highlightthickness=2)
        # Thanh cuộn
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        # Entry
        entry_frame = tk.Frame(frame, bg="#eef2f6")
        entry_frame.pack(fill=tk.X, pady=10)
        lbl = tk.Label(entry_frame, text="Tên kệ:", font=("Segoe UI", 11, "bold"), bg="#eef2f6", fg="#232a36")
        lbl.pack(side=tk.LEFT, padx=(0,8))
        self.entry_ten = tk.Entry(entry_frame, font=("Segoe UI", 12), relief="groove", bd=2, highlightthickness=1, highlightbackground="#dde2e6")
        self.entry_ten.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        # Nút chức năng pastel
        btn_frame = tk.Frame(frame, bg="#eef2f6")
        btn_frame.pack(fill=tk.X, pady=10)
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Thêm', command=self.add_shelf)
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_edit = tk.Button(btn_frame, text='Sửa', command=self.update_shelf)
        style_btn(btn_edit, "#f9e7cf", "#f6cba3")
        btn_edit.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=self.delete_shelf)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.load_data)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for shelf in self.model.get_all_shelves():
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