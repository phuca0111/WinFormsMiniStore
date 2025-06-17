import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.product import get_all_products, add_product, update_product, delete_product
from Core.category import get_all_categories
from Core.producer import get_all_producers

class ProductView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.parent = parent
        self.db_path = db_path

        # Cấu hình grid cho self.frame
        self.frame.grid_rowconfigure(4, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        row_idx = 0

        # Tiêu đề "Quản lý sản phẩm"
        label = ttk.Label(self.frame, text='Quản lý sản phẩm', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=2, padx=20, pady=5, sticky=tk.N)
        row_idx += 1
        # Add new label for product list
        label_list = ttk.Label(self.frame, text="Danh sách sản phẩm", font=("Arial", 12))
        label_list.grid(row=row_idx, column=0, padx=10, pady=4, sticky=tk.W)
        row_idx += 1

        # Treeview
        self.columns = ('ID', 'Tên sản phẩm', 'Thể loại', 'Hãng sản xuất', 'theloai_id', 'hangsanxuat_id')
        self.tree = ttk.Treeview(self.frame, columns=self.columns, show='headings', height=10)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tên sản phẩm', text='Tên sản phẩm')
        self.tree.heading('Thể loại', text='Thể loại')
        self.tree.heading('Hãng sản xuất', text='Hãng sản xuất')
        self.tree.heading('theloai_id', text='theloai_id')
        self.tree.heading('hangsanxuat_id', text='hangsanxuat_id')
        self.tree.column('theloai_id', width=0, stretch=False)
        self.tree.column('hangsanxuat_id', width=0, stretch=False)
        self.tree.column('ID', anchor=tk.CENTER)
        self.tree.column('Tên sản phẩm', anchor=tk.CENTER)
        self.tree.column('Thể loại', anchor=tk.CENTER)
        self.tree.column('Hãng sản xuất', anchor=tk.CENTER)
        self.tree.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1

        # Input fields
        input_frame = ttk.Frame(self.frame)
        input_frame.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1
        input_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Tên sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_ten = tk.Entry(input_frame, font=('Arial', 12))
        self.entry_ten.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Thể loại:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.combobox_cat = ttk.Combobox(input_frame, font=('Arial', 12), state='readonly')
        self.combobox_cat.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Hãng sản xuất:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_prod = ttk.Combobox(input_frame, font=('Arial', 12), state='readonly')
        self.combobox_prod.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        self.category_dict = self.load_categories_combobox(self.combobox_cat)
        self.producer_dict = self.load_producers_combobox(self.combobox_prod)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Button frame
        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(1, weight=1)
        frame_btn.grid_columnconfigure(2, weight=1)
        frame_btn.grid_columnconfigure(3, weight=1)

        ttk.Button(frame_btn, text='Thêm', command=self.on_add).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame_btn, text='Sửa', command=self.on_update).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame_btn, text='Xóa', command=self.on_delete).grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame_btn, text='Làm mới', command=self.on_refresh).grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        products = get_all_products()
        for p in products:
            theloai = self.category_dict.get(p.theloai_id, '')
            hang = self.producer_dict.get(getattr(p, 'hangsanxuat_id', None), '')
            self.tree.insert('', 'end', values=(p.id, p.ten, theloai, hang, p.theloai_id, getattr(p, 'hangsanxuat_id', None)))

    def load_categories_combobox(self, combobox):
        categories = get_all_categories()
        combobox['values'] = [f"{c.id} - {c.ten}" for c in categories]
        return {c.id: c.ten for c in categories}

    def load_producers_combobox(self, combobox):
        producers = get_all_producers()
        combobox['values'] = [f"{p.id} - {p.ten}" for p in producers]
        return {p.id: p.ten for p in producers}

    def on_add(self):
        ten = self.entry_ten.get().strip()
        theloai_str = self.combobox_cat.get()
        hang_str = self.combobox_prod.get()
        if not ten or not theloai_str or not hang_str:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên, chọn thể loại và hãng sản xuất!')
            return
        theloai_id = int(theloai_str.split(' - ')[0])
        hang_id = int(hang_str.split(' - ')[0])
        add_product(ten, theloai_id, hang_id)
        self.entry_ten.delete(0, tk.END)
        self.combobox_cat.set('')
        self.combobox_prod.set('')
        self.load_products()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để xóa!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        delete_product(id)
        self.entry_ten.delete(0, tk.END)
        self.combobox_cat.set('')
        self.combobox_prod.set('')
        self.load_products()

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để sửa!')
            return
        ten_moi = self.entry_ten.get().strip()
        theloai_str = self.combobox_cat.get()
        hang_str = self.combobox_prod.get()
        if not ten_moi or not theloai_str or not hang_str:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên, chọn thể loại và hãng sản xuất!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        theloai_id = int(theloai_str.split(' - ')[0])
        hang_id = int(hang_str.split(' - ')[0])
        update_product(id, ten_moi, theloai_id, hang_id)
        self.entry_ten.delete(0, tk.END)
        self.combobox_cat.set('')
        self.combobox_prod.set('')
        self.load_products()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.entry_ten.delete(0, tk.END)
            self.entry_ten.insert(0, item['values'][1])
            theloai_id = item['values'][4]
            for v in self.combobox_cat['values']:
                if v.startswith(str(theloai_id) + ' -'):
                    self.combobox_cat.set(v)
                    break
            hang_id = item['values'][5]
            for v in self.combobox_prod['values']:
                if v.startswith(str(hang_id) + ' -'):
                    self.combobox_prod.set(v)
                    break
    
    def on_refresh(self):
        self.category_dict.update(self.load_categories_combobox(self.combobox_cat))
        self.producer_dict.update(self.load_producers_combobox(self.combobox_prod))
        self.load_products()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Quản lý sản phẩm')
    root.geometry('700x450')

    product_view = ProductView(root)
    root.mainloop() 