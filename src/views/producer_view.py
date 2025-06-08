import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.producer import get_all_producers, add_producer, update_producer, delete_producer


def load_producers(tree):
    for item in tree.get_children():
        tree.delete(item)
    producers = get_all_producers()
    for p in producers:
        tree.insert('', 'end', values=(p.id, p.ten))

def on_add(entry, tree):
    ten = entry.get().strip()
    if not ten:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên hãng sản xuất!')
        return
    add_producer(ten)
    entry.delete(0, tk.END)
    load_producers(tree)

def on_delete(tree, entry):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn hãng để xóa!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    delete_producer(id)
    entry.delete(0, tk.END)
    load_producers(tree)

def on_update(tree, entry):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn hãng để sửa!')
        return
    ten_moi = entry.get().strip()
    if not ten_moi:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên mới!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    update_producer(id, ten_moi)
    entry.delete(0, tk.END)
    load_producers(tree)

def on_select(event, tree, entry):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        entry.delete(0, tk.END)
        entry.insert(0, item['values'][1])

def main():
    root = tk.Tk()
    root.title('Quản lý hãng sản xuất')
    root.geometry('420x400')

    columns = ('ID', 'Tên hãng sản xuất')
    tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
    tree.heading('ID', text='ID')
    tree.heading('Tên hãng sản xuất', text='Tên hãng sản xuất')
    tree.pack(fill=tk.X, padx=10, pady=10)

    entry = tk.Entry(root, font=('Arial', 12))
    entry.pack(fill=tk.X, padx=10, pady=5)
    tree.bind('<<TreeviewSelect>>', lambda e: on_select(e, tree, entry))

    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=5)
    btn_add = tk.Button(frame_btn, text='Thêm', width=10, command=lambda: on_add(entry, tree))
    btn_update = tk.Button(frame_btn, text='Sửa', width=10, command=lambda: on_update(tree, entry))
    btn_delete = tk.Button(frame_btn, text='Xóa', width=10, command=lambda: on_delete(tree, entry))
    btn_refresh = tk.Button(frame_btn, text='Làm mới', width=10, command=lambda: load_producers(tree))
    btn_add.grid(row=0, column=0, padx=5)
    btn_update.grid(row=0, column=1, padx=5)
    btn_delete.grid(row=0, column=2, padx=5)
    btn_refresh.grid(row=0, column=3, padx=5)

    load_producers(tree)
    root.mainloop()

if __name__ == '__main__':
    main() 