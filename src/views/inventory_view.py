import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.inventory import get_all_inventory, add_inventory, update_inventory, delete_inventory
from Core.product_variant import get_all_product_variants

def load_inventory(tree, variant_dict):
    for item in tree.get_children():
        tree.delete(item)
    inventory_list = get_all_inventory()
    for inv in inventory_list:
        variant_name = variant_dict.get(inv.bienthe_id, '')
        tree.insert('', 'end', values=(inv.id, variant_name, inv.soluong, inv.bienthe_id))

def load_variant_combobox(combobox):
    variants = get_all_product_variants()
    combobox['values'] = [f"{v.id} - {v.ten_bienthe}" for v in variants]
    return {v.id: v.ten_bienthe for v in variants}

def on_add(combobox_variant, entry_soluong, tree, variant_dict):
    variant_str = combobox_variant.get()
    soluong = entry_soluong.get().strip()
    if not variant_str or not soluong:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin!')
        return
    try:
        soluong = int(soluong)
    except:
        messagebox.showwarning('Cảnh báo', 'Số lượng phải là số nguyên!')
        return
    bienthe_id = int(variant_str.split(' - ')[0])
    add_inventory(bienthe_id, soluong)
    entry_soluong.delete(0, tk.END)
    combobox_variant.set('')
    load_inventory(tree, variant_dict)

def on_delete(tree, combobox_variant, entry_soluong, variant_dict):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn tồn kho để xóa!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    delete_inventory(id)
    entry_soluong.delete(0, tk.END)
    combobox_variant.set('')
    load_inventory(tree, variant_dict)

def on_update(tree, combobox_variant, entry_soluong, variant_dict):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn tồn kho để sửa!')
        return
    variant_str = combobox_variant.get()
    soluong = entry_soluong.get().strip()
    if not variant_str or not soluong:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin!')
        return
    try:
        soluong = int(soluong)
    except:
        messagebox.showwarning('Cảnh báo', 'Số lượng phải là số nguyên!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    bienthe_id = int(variant_str.split(' - ')[0])
    update_inventory(id, bienthe_id, soluong)
    entry_soluong.delete(0, tk.END)
    combobox_variant.set('')
    load_inventory(tree, variant_dict)

def on_select(event, tree, combobox_variant, entry_soluong):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        entry_soluong.delete(0, tk.END)
        entry_soluong.insert(0, item['values'][2])
        bienthe_id = item['values'][3]
        for v in combobox_variant['values']:
            if v.startswith(str(bienthe_id) + ' -'):
                combobox_variant.set(v)
                break

def main():
    root = tk.Tk()
    root.title('Quản lý tồn kho')
    root.geometry('600x400')

    columns = ('ID', 'Tên biến thể', 'Số lượng', 'bienthe_id')
    tree = ttk.Treeview(root, columns=columns, show='headings', height=12)
    tree.heading('ID', text='ID')
    tree.heading('Tên biến thể', text='Tên biến thể')
    tree.heading('Số lượng', text='Số lượng')
    tree.heading('bienthe_id', text='bienthe_id')
    tree.column('bienthe_id', width=0, stretch=False)
    tree.pack(fill=tk.X, padx=10, pady=10)

    combobox_variant = ttk.Combobox(root, font=('Arial', 12), state='readonly')
    combobox_variant.pack(fill=tk.X, padx=10, pady=5)
    entry_soluong = tk.Entry(root, font=('Arial', 12))
    entry_soluong.pack(fill=tk.X, padx=10, pady=5)

    variant_dict = load_variant_combobox(combobox_variant)
    tree.bind('<<TreeviewSelect>>', lambda e: on_select(e, tree, combobox_variant, entry_soluong))

    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=5)
    btn_add = tk.Button(frame_btn, text='Thêm', width=10, command=lambda: on_add(combobox_variant, entry_soluong, tree, variant_dict))
    btn_update = tk.Button(frame_btn, text='Sửa', width=10, command=lambda: on_update(tree, combobox_variant, entry_soluong, variant_dict))
    btn_delete = tk.Button(frame_btn, text='Xóa', width=10, command=lambda: on_delete(tree, combobox_variant, entry_soluong, variant_dict))
    btn_refresh = tk.Button(frame_btn, text='Làm mới', width=10, command=lambda: [variant_dict.update(load_variant_combobox(combobox_variant)), load_inventory(tree, variant_dict)])
    btn_add.grid(row=0, column=0, padx=5)
    btn_update.grid(row=0, column=1, padx=5)
    btn_delete.grid(row=0, column=2, padx=5)
    btn_refresh.grid(row=0, column=3, padx=5)

    load_inventory(tree, variant_dict)
    root.mainloop()

if __name__ == '__main__':
    main() 