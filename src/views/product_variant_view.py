import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.product_variant import get_all_product_variants, add_product_variant, update_product_variant, delete_product_variant
from Core.product import get_all_products
from Core.barcode_scanner import scan_barcode

def load_variants(tree, product_dict):
    for item in tree.get_children():
        tree.delete(item)
    variants = get_all_product_variants()
    for v in variants:
        product_name = product_dict.get(v.sanpham_id, '')
        tree.insert('', 'end', values=(v.id, product_name, v.ten_bienthe, v.gia, v.barcode, v.sanpham_id))

def load_products_combobox(combobox):
    products = get_all_products()
    combobox['values'] = [f"{p.id} - {p.ten}" for p in products]
    return {p.id: p.ten for p in products}

def on_add(combobox_prod, entry_ten, entry_gia, entry_barcode, tree, product_dict):
    prod_str = combobox_prod.get()
    ten_bienthe = entry_ten.get().strip()
    gia = entry_gia.get().strip()
    barcode = entry_barcode.get().strip()
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
    entry_ten.delete(0, tk.END)
    entry_gia.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)
    combobox_prod.set('')
    load_variants(tree, product_dict)

def on_delete(tree, combobox_prod, entry_ten, entry_gia, entry_barcode, product_dict):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn biến thể để xóa!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    delete_product_variant(id)
    entry_ten.delete(0, tk.END)
    entry_gia.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)
    combobox_prod.set('')
    load_variants(tree, product_dict)

def on_update(tree, combobox_prod, entry_ten, entry_gia, entry_barcode, product_dict):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn biến thể để sửa!')
        return
    prod_str = combobox_prod.get()
    ten_bienthe = entry_ten.get().strip()
    gia = entry_gia.get().strip()
    barcode = entry_barcode.get().strip()
    if not prod_str or not ten_bienthe or not gia or not barcode:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin!')
        return
    try:
        gia = float(gia)
    except:
        messagebox.showwarning('Cảnh báo', 'Giá phải là số!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    sanpham_id = int(prod_str.split(' - ')[0])
    update_product_variant(id, sanpham_id, ten_bienthe, gia, barcode)
    entry_ten.delete(0, tk.END)
    entry_gia.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)
    combobox_prod.set('')
    load_variants(tree, product_dict)

def on_select(event, tree, combobox_prod, entry_ten, entry_gia, entry_barcode):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, item['values'][2])
        entry_gia.delete(0, tk.END)
        entry_gia.insert(0, item['values'][3])
        entry_barcode.delete(0, tk.END)
        entry_barcode.insert(0, item['values'][4])
        sanpham_id = item['values'][5]
        for v in combobox_prod['values']:
            if v.startswith(str(sanpham_id) + ' -'):
                combobox_prod.set(v)
                break

def on_scan_barcode(entry_barcode):
    barcode = scan_barcode()
    if barcode:
        entry_barcode.delete(0, tk.END)
        entry_barcode.insert(0, barcode)

def main():
    root = tk.Tk()
    root.title('Quản lý biến thể sản phẩm')
    root.geometry('800x500')

    columns = ('ID', 'Sản phẩm', 'Tên biến thể', 'Giá', 'Barcode', 'sanpham_id')
    tree = ttk.Treeview(root, columns=columns, show='headings', height=12)
    tree.heading('ID', text='ID')
    tree.heading('Sản phẩm', text='Sản phẩm')
    tree.heading('Tên biến thể', text='Tên biến thể')
    tree.heading('Giá', text='Giá')
    tree.heading('Barcode', text='Barcode')
    tree.heading('sanpham_id', text='sanpham_id')
    tree.column('sanpham_id', width=0, stretch=False)
    tree.pack(fill=tk.X, padx=10, pady=10)

    combobox_prod = ttk.Combobox(root, font=('Arial', 12), state='readonly')
    combobox_prod.pack(fill=tk.X, padx=10, pady=5)
    entry_ten = tk.Entry(root, font=('Arial', 12))
    entry_ten.pack(fill=tk.X, padx=10, pady=5)
    entry_gia = tk.Entry(root, font=('Arial', 12))
    entry_gia.pack(fill=tk.X, padx=10, pady=5)
    entry_barcode = tk.Entry(root, font=('Arial', 12))
    entry_barcode.pack(fill=tk.X, padx=10, pady=5)

    product_dict = load_products_combobox(combobox_prod)
    tree.bind('<<TreeviewSelect>>', lambda e: on_select(e, tree, combobox_prod, entry_ten, entry_gia, entry_barcode))

    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=5)
    btn_add = tk.Button(frame_btn, text='Thêm', width=10, command=lambda: on_add(combobox_prod, entry_ten, entry_gia, entry_barcode, tree, product_dict))
    btn_update = tk.Button(frame_btn, text='Sửa', width=10, command=lambda: on_update(tree, combobox_prod, entry_ten, entry_gia, entry_barcode, product_dict))
    btn_delete = tk.Button(frame_btn, text='Xóa', width=10, command=lambda: on_delete(tree, combobox_prod, entry_ten, entry_gia, entry_barcode, product_dict))
    btn_scan = tk.Button(frame_btn, text='Quét mã vạch', width=12, command=lambda: on_scan_barcode(entry_barcode))
    btn_refresh = tk.Button(frame_btn, text='Làm mới', width=10, command=lambda: [product_dict.update(load_products_combobox(combobox_prod)), load_variants(tree, product_dict)])
    btn_add.grid(row=0, column=0, padx=5)
    btn_update.grid(row=0, column=1, padx=5)
    btn_delete.grid(row=0, column=2, padx=5)
    btn_scan.grid(row=0, column=3, padx=5)
    btn_refresh.grid(row=0, column=4, padx=5)

    load_variants(tree, product_dict)
    root.mainloop()

if __name__ == '__main__':
    main() 