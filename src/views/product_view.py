import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.product import get_all_products, add_product, update_product, delete_product
from Core.category import get_all_categories
from Core.producer import get_all_producers

def load_products(tree, category_dict, producer_dict):
    for item in tree.get_children():
        tree.delete(item)
    products = get_all_products()
    for p in products:
        theloai = category_dict.get(p.theloai_id, '')
        hang = producer_dict.get(getattr(p, 'hangsanxuat_id', None), '')
        tree.insert('', 'end', values=(p.id, p.ten, theloai, hang, p.theloai_id, getattr(p, 'hangsanxuat_id', None)))

def load_categories_combobox(combobox):
    categories = get_all_categories()
    combobox['values'] = [f"{c.id} - {c.ten}" for c in categories]
    return {c.id: c.ten for c in categories}

def load_producers_combobox(combobox):
    producers = get_all_producers()
    combobox['values'] = [f"{p.id} - {p.ten}" for p in producers]
    return {p.id: p.ten for p in producers}

def on_add(entry_ten, combobox_cat, combobox_prod, tree, category_dict, producer_dict):
    ten = entry_ten.get().strip()
    theloai_str = combobox_cat.get()
    hang_str = combobox_prod.get()
    if not ten or not theloai_str or not hang_str:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên, chọn thể loại và hãng sản xuất!')
        return
    theloai_id = int(theloai_str.split(' - ')[0])
    hang_id = int(hang_str.split(' - ')[0])
    add_product(ten, theloai_id, hang_id)
    entry_ten.delete(0, tk.END)
    combobox_cat.set('')
    combobox_prod.set('')
    load_products(tree, category_dict, producer_dict)

def on_delete(tree, entry_ten, combobox_cat, combobox_prod, category_dict, producer_dict):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để xóa!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    delete_product(id)
    entry_ten.delete(0, tk.END)
    combobox_cat.set('')
    combobox_prod.set('')
    load_products(tree, category_dict, producer_dict)

def on_update(tree, entry_ten, combobox_cat, combobox_prod, category_dict, producer_dict):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để sửa!')
        return
    ten_moi = entry_ten.get().strip()
    theloai_str = combobox_cat.get()
    hang_str = combobox_prod.get()
    if not ten_moi or not theloai_str or not hang_str:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên, chọn thể loại và hãng sản xuất!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    theloai_id = int(theloai_str.split(' - ')[0])
    hang_id = int(hang_str.split(' - ')[0])
    update_product(id, ten_moi, theloai_id, hang_id)
    entry_ten.delete(0, tk.END)
    combobox_cat.set('')
    combobox_prod.set('')
    load_products(tree, category_dict, producer_dict)

def on_select(event, tree, entry_ten, combobox_cat, combobox_prod):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, item['values'][1])
        theloai_id = item['values'][4]
        for v in combobox_cat['values']:
            if v.startswith(str(theloai_id) + ' -'):
                combobox_cat.set(v)
                break
        hang_id = item['values'][5]
        for v in combobox_prod['values']:
            if v.startswith(str(hang_id) + ' -'):
                combobox_prod.set(v)
                break

def main():
    root = tk.Tk()
    root.title('Quản lý sản phẩm')
    root.geometry('700x450')

    columns = ('ID', 'Tên sản phẩm', 'Thể loại', 'Hãng sản xuất', 'theloai_id', 'hangsanxuat_id')
    tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
    tree.heading('ID', text='ID')
    tree.heading('Tên sản phẩm', text='Tên sản phẩm')
    tree.heading('Thể loại', text='Thể loại')
    tree.heading('Hãng sản xuất', text='Hãng sản xuất')
    tree.heading('theloai_id', text='theloai_id')
    tree.heading('hangsanxuat_id', text='hangsanxuat_id')
    tree.column('theloai_id', width=0, stretch=False)
    tree.column('hangsanxuat_id', width=0, stretch=False)
    tree.pack(fill=tk.X, padx=10, pady=10)

    entry_ten = tk.Entry(root, font=('Arial', 12))
    entry_ten.pack(fill=tk.X, padx=10, pady=5)
    combobox_cat = ttk.Combobox(root, font=('Arial', 12), state='readonly')
    combobox_cat.pack(fill=tk.X, padx=10, pady=5)
    combobox_prod = ttk.Combobox(root, font=('Arial', 12), state='readonly')
    combobox_prod.pack(fill=tk.X, padx=10, pady=5)

    category_dict = load_categories_combobox(combobox_cat)
    producer_dict = load_producers_combobox(combobox_prod)

    tree.bind('<<TreeviewSelect>>', lambda e: on_select(e, tree, entry_ten, combobox_cat, combobox_prod))

    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=5)
    btn_add = tk.Button(frame_btn, text='Thêm', width=10, command=lambda: on_add(entry_ten, combobox_cat, combobox_prod, tree, category_dict, producer_dict))
    btn_update = tk.Button(frame_btn, text='Sửa', width=10, command=lambda: on_update(tree, entry_ten, combobox_cat, combobox_prod, category_dict, producer_dict))
    btn_delete = tk.Button(frame_btn, text='Xóa', width=10, command=lambda: on_delete(tree, entry_ten, combobox_cat, combobox_prod, category_dict, producer_dict))
    btn_refresh = tk.Button(frame_btn, text='Làm mới', width=10, command=lambda: [category_dict.update(load_categories_combobox(combobox_cat)), producer_dict.update(load_producers_combobox(combobox_prod)), load_products(tree, category_dict, producer_dict)])
    btn_add.grid(row=0, column=0, padx=5)
    btn_update.grid(row=0, column=1, padx=5)
    btn_delete.grid(row=0, column=2, padx=5)
    btn_refresh.grid(row=0, column=3, padx=5)

    load_products(tree, category_dict, producer_dict)
    root.mainloop()

if __name__ == '__main__':
    main() 