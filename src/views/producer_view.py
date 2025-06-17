import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.producer import get_all_producers, add_producer, update_producer, delete_producer

class ProducerView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.parent = parent
        self.db_path = db_path

        # Cấu hình grid cho self.frame (áp dụng cho các widget con bên trong frame này)
        self.frame.grid_rowconfigure(3, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        self.load_producers()

    def setup_ui(self):
        row_idx = 0

        # Tiêu đề "Quản lý hãng sản xuất"
        label = ttk.Label(self.frame, text='Quản lý nhà sản xuất', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=2, padx=20, pady=5, sticky=tk.N)
        row_idx += 1

        label_list = ttk.Label(self.frame, text="Danh sách các nhà cung cấp", font=("Arial", 12))
        label_list.grid(row=row_idx, column=0, padx=10, pady=4, sticky=tk.W)
        row_idx += 1

        # Entry and buttons for add/update/delete
        entry_frame = ttk.Frame(self.frame) 
        entry_frame.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry = tk.Entry(entry_frame, font=('Arial', 12))
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        
        # Button frame inside entry_frame (for consistency, move buttons to grid inside entry_frame)
        btn_frame_internal = ttk.Frame(entry_frame)
        btn_frame_internal.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        btn_frame_internal.grid_columnconfigure(0, weight=1)
        btn_frame_internal.grid_columnconfigure(1, weight=1)
        btn_frame_internal.grid_columnconfigure(2, weight=1)
        btn_frame_internal.grid_columnconfigure(3, weight=1)

        ttk.Button(btn_frame_internal, text='Thêm', command=self.on_add).grid(row=0, column=0, padx=2, pady=2, sticky=tk.EW)
        ttk.Button(btn_frame_internal, text='Sửa', command=self.on_update).grid(row=0, column=1, padx=2, pady=2, sticky=tk.EW)
        ttk.Button(btn_frame_internal, text='Xóa', command=self.on_delete).grid(row=0, column=2, padx=2, pady=2, sticky=tk.EW)
        ttk.Button(btn_frame_internal, text='Làm mới', command=self.load_producers).grid(row=0, column=3, padx=2, pady=2, sticky=tk.EW)

        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Tên hãng sản xuất'), show='headings', height=10)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tên hãng sản xuất', text='Tên hãng sản xuất')
        self.tree.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=5, sticky=tk.NSEW)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

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

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Quản lý hãng sản xuất')
    root.geometry('420x400')

    producer_view = ProducerView(root)
    root.mainloop() 