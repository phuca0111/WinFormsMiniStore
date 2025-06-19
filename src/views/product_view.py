import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.product import get_all_products, add_product, update_product, delete_product
from Core.category import get_all_categories
from Core.producer import get_all_producers

class ProductView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#F5F7FA")
        self.category_dict = {}
        self.producer_dict = {}
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#F5F7FA", relief="flat")
        style.configure("Custom.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#F5F7FA")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")
        style.configure("TCombobox", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")

        # Bảng bo tròn giả lập
        table_frame = tk.Frame(self, bg="#F5F7FA")
        table_frame.pack(fill=tk.X, padx=32, pady=(32, 16))
        table_border = tk.Frame(table_frame, bg="#DDE2E6", bd=0)
        table_border.pack(fill=tk.X, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.X, padx=2, pady=2)
        columns = ('ID', 'Tên sản phẩm', 'Thể loại', 'Hãng sản xuất')
        self.tree = ttk.Treeview(table_inner, columns=columns, show='headings', height=8, style="Custom.Treeview")
        self.tree.heading('ID', text='ID', anchor="center")
        self.tree.heading('Tên sản phẩm', text='Tên sản phẩm', anchor="center")
        self.tree.heading('Thể loại', text='Thể loại', anchor="center")
        self.tree.heading('Hãng sản xuất', text='Hãng sản xuất', anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Tên sản phẩm', width=300, anchor="w")
        self.tree.column('Thể loại', width=150, anchor="w")
        self.tree.column('Hãng sản xuất', width=150, anchor="w")
        self.tree.pack(fill=tk.X, padx=8, pady=8)

        # Input + combobox cùng hàng, có label
        input_frame = tk.Frame(self, bg="#F5F7FA")
        input_frame.pack(fill=tk.X, padx=32, pady=8)
        tk.Label(input_frame, text="Tên sản phẩm:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=0, sticky="e", padx=8, pady=12)
        self.entry_name = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        tk.Label(input_frame, text="Thể loại:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=2, sticky="e", padx=8, pady=12)
        self.combo_category = ttk.Combobox(input_frame, font=("Segoe UI", 12))
        self.combo_category.grid(row=0, column=3, sticky="ew", padx=8, pady=12)
        tk.Label(input_frame, text="Hãng SX:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=4, sticky="e", padx=8, pady=12)
        self.combo_producer = ttk.Combobox(input_frame, font=("Segoe UI", 12))
        self.combo_producer.grid(row=0, column=5, sticky="ew", padx=8, pady=12)
        # Responsive: cho các cột entry, combobox co giãn
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        input_frame.grid_columnconfigure(5, weight=1)

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
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.load_products)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)

        self.category_dict = self.load_categories_combobox()
        self.producer_dict = self.load_producers_combobox()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        products = get_all_products()
        for p in products:
            theloai = self.category_dict.get(p.theloai_id, '')
            hang = self.producer_dict.get(getattr(p, 'hangsanxuat_id', None), '')
            self.tree.insert('', 'end', values=(p.id, p.ten, theloai, hang))

    def load_categories_combobox(self):
        categories = get_all_categories()
        self.combo_category['values'] = [f"{c.id} - {c.ten}" for c in categories]
        return {c.id: c.ten for c in categories}

    def load_producers_combobox(self):
        producers = get_all_producers()
        self.combo_producer['values'] = [f"{p.id} - {p.ten}" for p in producers]
        return {p.id: p.ten for p in producers}

    def on_add(self):
        ten = self.entry_name.get().strip()
        theloai_str = self.combo_category.get()
        producer_str = self.combo_producer.get()
        if not ten or not theloai_str or not producer_str:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên, chọn thể loại và hãng sản xuất!')
            return
        theloai_id = int(theloai_str.split(' - ')[0])
        producer_id = int(producer_str.split(' - ')[0])
        add_product(ten, theloai_id, producer_id)
        self.entry_name.delete(0, tk.END)
        self.combo_category.set('')
        self.combo_producer.set('')
        self.load_products()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để xóa!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        delete_product(id)
        self.entry_name.delete(0, tk.END)
        self.combo_category.set('')
        self.combo_producer.set('')
        self.load_products()

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để sửa!')
            return
        ten_moi = self.entry_name.get().strip()
        theloai_str = self.combo_category.get()
        producer_str = self.combo_producer.get()
        if not ten_moi or not theloai_str or not producer_str:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên, chọn thể loại và hãng sản xuất!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        theloai_id = int(theloai_str.split(' - ')[0])
        producer_id = int(producer_str.split(' - ')[0])
        update_product(id, ten_moi, theloai_id, producer_id)
        self.entry_name.delete(0, tk.END)
        self.combo_category.set('')
        self.combo_producer.set('')
        self.load_products()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, item['values'][1])
            # Lấy id thể loại và hãng sản xuất từ treeview
            theloai = item['values'][2]
            hang = item['values'][3]
            # Set combobox thể loại
            for v in self.combo_category['values']:
                if theloai in v:
                    self.combo_category.set(v)
                    break
            # Set combobox hãng sản xuất
            for v in self.combo_producer['values']:
                if v.endswith(f"- {hang}"):
                    self.combo_producer.set(v)
                    break

    def on_refresh(self):
        self.category_dict = self.load_categories_combobox()
        self.producer_dict = self.load_producers_combobox()
        self.load_products() 