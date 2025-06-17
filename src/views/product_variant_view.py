import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.product_variant import get_all_product_variants, add_product_variant, update_product_variant, delete_product_variant
from Core.product import get_all_products
from Core.barcode_scanner import scan_barcode

class ProductVariantView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.parent = parent
        self.db_path = db_path

        # Cấu hình grid cho self.frame
        self.frame.grid_rowconfigure(4, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        self.load_variants()

    def setup_ui(self):
        row_idx = 0

        # Tiêu đề "Quản lý biến thể sản phẩm"
        label = ttk.Label(self.frame, text='Quản lý biến thể sản phẩm', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=2, padx=20, pady=5, sticky=tk.N)
        row_idx += 1

        label_list = ttk.Label(self.frame, text="Danh sách các biến thể", font=("Arial", 12))
        label_list.grid(row=row_idx, column=0, padx=10, pady=4, sticky=tk.W)
        row_idx += 1
        # Treeview
        self.columns = ('ID', 'Sản phẩm', 'Tên biến thể', 'Giá', 'Barcode', 'sanpham_id')
        self.tree = ttk.Treeview(self.frame, columns=self.columns, show='headings', height=12)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Sản phẩm', text='Sản phẩm')
        self.tree.heading('Tên biến thể', text='Tên biến thể')
        self.tree.heading('Giá', text='Giá')
        self.tree.heading('Barcode', text='Barcode')
        self.tree.heading('sanpham_id', text='sanpham_id')
        self.tree.column('sanpham_id', width=0, stretch=False)
        self.tree.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1

        # Input fields
        input_frame = ttk.Frame(self.frame)
        input_frame.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1
        input_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_prod = ttk.Combobox(input_frame, font=('Arial', 12), state='readonly')
        self.combobox_prod.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Tên biến thể:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_ten = tk.Entry(input_frame, font=('Arial', 12))
        self.entry_ten.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Giá:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_gia = tk.Entry(input_frame, font=('Arial', 12))
        self.entry_gia.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Barcode:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_barcode = tk.Entry(input_frame, font=('Arial', 12))
        self.entry_barcode.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.product_dict = self.load_products_combobox(self.combobox_prod)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Button frame
        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(1, weight=1)
        frame_btn.grid_columnconfigure(2, weight=1)
        frame_btn.grid_columnconfigure(3, weight=1)
        frame_btn.grid_columnconfigure(4, weight=1)

        ttk.Button(frame_btn, text='Thêm', command=self.on_add).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame_btn, text='Sửa', command=self.on_update).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame_btn, text='Xóa', command=self.on_delete).grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame_btn, text='Quét mã vạch', command=self.on_scan_barcode).grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame_btn, text='Làm mới', command=self.on_refresh).grid(row=0, column=4, padx=5, pady=5, sticky=tk.EW)

    def load_variants(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        variants = get_all_product_variants()
        for v in variants:
            product_name = self.product_dict.get(v.sanpham_id, '')
            self.tree.insert('', 'end', values=(v.id, product_name, v.ten_bienthe, v.gia, v.barcode, v.sanpham_id))

    def load_products_combobox(self, combobox):
        products = get_all_products()
        combobox['values'] = [f"{p.id} - {p.ten}" for p in products]
        return {p.id: p.ten for p in products}

    def on_add(self):
        prod_str = self.combobox_prod.get()
        ten_bienthe = self.entry_ten.get().strip()
        gia = self.entry_gia.get().strip()
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
        self.entry_ten.delete(0, tk.END)
        self.entry_gia.delete(0, tk.END)
        self.entry_barcode.delete(0, tk.END)
        self.combobox_prod.set('')
        self.load_variants()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn biến thể để xóa!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        delete_product_variant(id)
        self.entry_ten.delete(0, tk.END)
        self.entry_gia.delete(0, tk.END)
        self.entry_barcode.delete(0, tk.END)
        self.combobox_prod.set('')
        self.load_variants()

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn biến thể để sửa!')
            return
        prod_str = self.combobox_prod.get()
        ten_bienthe = self.entry_ten.get().strip()
        gia = self.entry_gia.get().strip()
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
        self.entry_ten.delete(0, tk.END)
        self.entry_gia.delete(0, tk.END)
        self.entry_barcode.delete(0, tk.END)
        self.combobox_prod.set('')
        self.load_variants()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.entry_ten.delete(0, tk.END)
            self.entry_ten.insert(0, item['values'][2])
            self.entry_gia.delete(0, tk.END)
            self.entry_gia.insert(0, item['values'][3])
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, item['values'][4])
            sanpham_id = item['values'][5]
            for v in self.combobox_prod['values']:
                if v.startswith(str(sanpham_id) + ' -'):
                    self.combobox_prod.set(v)
                    break

    def on_scan_barcode(self):
        barcode = scan_barcode()
        if barcode:
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, barcode)
    
    def on_refresh(self):
        self.product_dict.update(self.load_products_combobox(self.combobox_prod))
        self.load_variants()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Quản lý biến thể sản phẩm')
    root.geometry('800x500')

    product_view = ProductVariantView(root)
    root.mainloop() 