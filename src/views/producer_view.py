import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.producer import get_all_producers, add_producer, update_producer, delete_producer

class ProducerView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#F5F7FA")
        self.setup_ui()
        self.load_producers()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#F5F7FA", relief="flat")
        style.configure("Custom.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#F5F7FA")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")

        # Bảng bo tròn giả lập
        table_frame = tk.Frame(self, bg="#F5F7FA")
        table_frame.pack(fill=tk.X, padx=32, pady=(32, 16))
        table_border = tk.Frame(table_frame, bg="#DDE2E6", bd=0)
        table_border.pack(fill=tk.X, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.X, padx=2, pady=2)
        columns = ('ID', 'Tên hãng sản xuất')
        self.tree = ttk.Treeview(table_inner, columns=columns, show='headings', height=8, style="Custom.Treeview")
        self.tree.heading('ID', text='ID', anchor="center")
        self.tree.heading('Tên hãng sản xuất', text='Tên hãng sản xuất', anchor="w")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Tên hãng sản xuất', width=300, anchor="w")
        self.tree.pack(fill=tk.X, padx=8, pady=8)

        # Input có label, padding lớn
        input_frame = tk.Frame(self, bg="#F5F7FA")
        input_frame.pack(fill=tk.X, padx=32, pady=8)
        tk.Label(input_frame, text="Tên hãng sản xuất:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=0, sticky="e", padx=8, pady=12)
        self.entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        # Responsive: cho entry co giãn
        input_frame.grid_columnconfigure(1, weight=1)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Nút chức năng pastel bo tròn
        btn_frame = tk.Frame(self, bg="#F5F7FA")
        btn_frame.pack(fill=tk.X, padx=32, pady=(0, 32))
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Thêm', command=self.on_add)
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_update = tk.Button(btn_frame, text='Sửa', command=self.on_update)
        style_btn(btn_update, "#f9e7cf", "#f6cba3")
        btn_update.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=self.on_delete)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.load_producers)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)

    def load_producers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        producers = get_all_producers()
        for p in producers:
            self.tree.insert('', 'end', values=(p.id, p.ten))

    def on_add(self):
        ten = self.entry.get().strip()
        if not ten:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên hãng sản xuất!')
            return
        add_producer(ten)
        self.entry.delete(0, tk.END)
        self.load_producers()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn hãng để xóa!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        delete_producer(id)
        self.entry.delete(0, tk.END)
        self.load_producers()

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn hãng để sửa!')
            return
        ten_moi = self.entry.get().strip()
        if not ten_moi:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên mới!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        update_producer(id, ten_moi)
        self.entry.delete(0, tk.END)
        self.load_producers()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, item['values'][1]) 