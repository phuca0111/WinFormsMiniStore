import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.product_variant import get_all_product_variants, add_product_variant, update_product_variant, delete_product_variant
from Core.product import get_all_products
from Core.barcode_scanner import scan_barcode

class ProductVariantView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#F5F7FA")
        self.setup_ui()
        self.product_dict = self.load_products_combobox()
        self.load_variants()

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
        columns = ('ID', 'Sản phẩm', 'Tên biến thể', 'Giá', 'Barcode')
        self.tree = ttk.Treeview(table_inner, columns=columns, show='headings', height=8, style="Custom.Treeview")
        self.tree.heading('ID', text='ID', anchor="center")
        self.tree.heading('Sản phẩm', text='Sản phẩm', anchor="w")
        self.tree.heading('Tên biến thể', text='Tên biến thể', anchor="w")
        self.tree.heading('Giá', text='Giá', anchor="center")
        self.tree.heading('Barcode', text='Barcode', anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Sản phẩm', width=180, anchor="w")
        self.tree.column('Tên biến thể', width=200, anchor="w")
        self.tree.column('Giá', width=100, anchor="center")
        self.tree.column('Barcode', width=160, anchor="center")
        self.tree.pack(fill=tk.X, padx=8, pady=8)

        # Input có label, padding lớn
        input_frame = tk.Frame(self, bg="#F5F7FA")
        input_frame.pack(fill=tk.X, padx=32, pady=8)
        tk.Label(input_frame, text="Sản phẩm:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=0, sticky="e", padx=8, pady=12)
        self.combo_product = ttk.Combobox(input_frame, font=("Segoe UI", 12))
        self.combo_product.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        tk.Label(input_frame, text="Tên biến thể:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=2, sticky="e", padx=8, pady=12)
        self.entry_variant = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_variant.grid(row=0, column=3, sticky="ew", padx=8, pady=12)
        tk.Label(input_frame, text="Giá:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=4, sticky="e", padx=8, pady=12)
        self.entry_price = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_price.grid(row=0, column=5, sticky="ew", padx=8, pady=12)
        tk.Label(input_frame, text="Barcode:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=6, sticky="e", padx=8, pady=12)
        self.entry_barcode = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_barcode.grid(row=0, column=7, sticky="ew", padx=8, pady=12)
        # Responsive: cho entry, combobox co giãn
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        input_frame.grid_columnconfigure(5, weight=1)
        input_frame.grid_columnconfigure(7, weight=1)

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
        btn_scan = tk.Button(btn_frame, text='Quét mã vạch', command=self.on_scan)
        style_btn(btn_scan, "#eafaf1", "#d1f2eb")
        btn_scan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.load_variants)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)

    def load_products_combobox(self):
        products = get_all_products()
        self.combo_product['values'] = [f"{p.id} - {p.ten}" for p in products]
        return {p.id: p.ten for p in products}

    def load_variants(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        variants = get_all_product_variants()
        for v in variants:
            product_name = self.product_dict.get(v.sanpham_id, '')
            self.tree.insert('', 'end', values=(v.id, product_name, v.ten_bienthe, v.gia, v.barcode))

    def on_add(self):
        prod_str = self.combo_product.get()
        ten_bienthe = self.entry_variant.get().strip()
        gia = self.entry_price.get().strip()
        barcode = self.entry_barcode.get().strip()
        if not prod_str or not ten_bienthe or not gia or not barcode:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin!')
            return
        try:
            gia = float(gia)
        except:
            messagebox.showwarning('Cảnh báo', 'Giá phải là số!')
            return
        sanpham_id = int(prod_str.split(' - ')[0])
        add_product_variant(sanpham_id, ten_bienthe, gia, barcode)
        self.entry_variant.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_barcode.delete(0, tk.END)
        self.combo_product.set('')
        self.load_variants()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn biến thể để xóa!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        delete_product_variant(id)
        self.entry_variant.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_barcode.delete(0, tk.END)
        self.combo_product.set('')
        self.load_variants()

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn biến thể để sửa!')
            return
        prod_str = self.combo_product.get()
        ten_bienthe = self.entry_variant.get().strip()
        gia = self.entry_price.get().strip()
        barcode = self.entry_barcode.get().strip()
        if not prod_str or not ten_bienthe or not gia or not barcode:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin!')
            return
        try:
            gia = float(gia)
        except:
            messagebox.showwarning('Cảnh báo', 'Giá phải là số!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        sanpham_id = int(prod_str.split(' - ')[0])
        update_product_variant(id, sanpham_id, ten_bienthe, gia, barcode)
        self.entry_variant.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_barcode.delete(0, tk.END)
        self.combo_product.set('')
        self.load_variants()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.entry_variant.delete(0, tk.END)
            self.entry_variant.insert(0, item['values'][2])
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, item['values'][3])
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, item['values'][4])
            sanpham_id = int(item['values'][1].split(' - ')[0])
            for v in self.combo_product['values']:
                if v.startswith(str(sanpham_id) + ' -'):
                    self.combo_product.set(v)
                    break

    def on_scan(self):
        barcode = scan_barcode()
        if barcode:
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, barcode) 