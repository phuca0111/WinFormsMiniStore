import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk
from Core.inventory import (
    load_inventory, load_variant_combobox, on_add, on_update, on_delete, on_select, on_scan_barcode, on_barcode_entered
)
from Core.barcode_scanner import scan_barcode
import time

class BarcodeEntry(ttk.Entry):
    def __init__(self, master=None, on_barcode_entered=None, **kwargs):
        super().__init__(master, **kwargs)
        self.barcode_buffer = ""
        self.last_key_time = 0
        self.is_scanning = False
        self.on_barcode_entered = on_barcode_entered
        self.bind('<KeyPress>', self.on_key_press)
        self.bind('<Return>', self.on_enter)
    def on_key_press(self, event):
        current_time = time.time()
        if event.keysym == 'Return' and self.is_scanning:
            self.is_scanning = False
            self.delete(0, tk.END)
            self.insert(0, self.barcode_buffer)
            if self.on_barcode_entered:
                self.on_barcode_entered(self.barcode_buffer)
            self.barcode_buffer = ""
            return "break"
        if current_time - self.last_key_time > 0.1:
            self.is_scanning = False
            self.barcode_buffer = ""
        self.last_key_time = current_time
        if not self.is_scanning:
            self.is_scanning = True
            self.barcode_buffer = ""
        if event.char:
            self.barcode_buffer += event.char
    def on_enter(self, event):
        if not self.is_scanning:
            if self.on_barcode_entered:
                self.on_barcode_entered(self.get())
            return
        self.is_scanning = False
        self.delete(0, tk.END)
        self.insert(0, self.barcode_buffer)
        if self.on_barcode_entered:
            self.on_barcode_entered(self.barcode_buffer)
        self.barcode_buffer = ""
        return "break"

def main():
    root = tk.Tk()
    root.title('Quản lý tồn kho')
    root.geometry('800x600')

    input_frame = ttk.LabelFrame(root, text='Nhập thông tin', padding=10)
    input_frame.pack(fill=tk.X, padx=10, pady=5)

    ttk.Label(input_frame, text='Sản phẩm:').grid(row=1, column=0, padx=5, pady=5)
    combobox_variant = ttk.Combobox(input_frame, font=('Arial', 12), state='readonly')
    combobox_variant.grid(row=1, column=1, padx=5, pady=5)

    label_sanpham = ttk.Label(input_frame, text='', font=('Arial', 12), foreground='blue')
    label_sanpham.grid(row=1, column=2, padx=5, pady=5)

    ttk.Label(input_frame, text='Barcode:').grid(row=0, column=0, padx=5, pady=5)
    entry_barcode = BarcodeEntry(
        input_frame,
        font=('Arial', 12),
        on_barcode_entered=lambda barcode: on_barcode_entered(barcode, combobox_variant, label_sanpham)
    )
    entry_barcode.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(input_frame, text='(Quét mã vạch hoặc nhập tay)', 
             font=('Arial', 8), foreground='gray').grid(row=0, column=2, padx=5, pady=5)
    btn_scan = ttk.Button(input_frame, text="Quét mã vạch (Camera)",
        command=lambda: on_scan_barcode(entry_barcode, combobox_variant, label_sanpham))
    btn_scan.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(input_frame, text='Số lượng:').grid(row=2, column=0, padx=5, pady=5)
    entry_soluong = ttk.Entry(input_frame, font=('Arial', 12))
    entry_soluong.grid(row=2, column=1, padx=5, pady=5)

    columns = ('ID', 'Tên sản phẩm', 'Tên biến thể', 'Barcode', 'Số lượng', 'bienthe_id')
    tree = ttk.Treeview(root, columns=columns, show='headings', height=15)
    for col in columns:
        tree.heading(col, text=col)
    tree.column('bienthe_id', width=0, stretch=False)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    frame_btn = ttk.Frame(root)
    frame_btn.pack(pady=5)
    btn_add = ttk.Button(frame_btn, text='Thêm', width=15, 
                        command=lambda: on_add(combobox_variant, entry_soluong, entry_barcode, tree))
    btn_update = ttk.Button(frame_btn, text='Sửa', width=15,
                           command=lambda: on_update(tree, combobox_variant, entry_soluong, entry_barcode))
    btn_delete = ttk.Button(frame_btn, text='Xóa', width=15,
                           command=lambda: on_delete(tree, combobox_variant, entry_soluong, entry_barcode))
    btn_refresh = ttk.Button(frame_btn, text='Làm mới', width=15,
                            command=lambda: [load_variant_combobox(combobox_variant), load_inventory(tree)])
    btn_add.grid(row=0, column=0, padx=5)
    btn_update.grid(row=0, column=1, padx=5)
    btn_delete.grid(row=0, column=2, padx=5)
    btn_refresh.grid(row=0, column=3, padx=5)

    tree.bind('<<TreeviewSelect>>', 
              lambda e: on_select(e, tree, combobox_variant, entry_soluong, entry_barcode))

    load_variant_combobox(combobox_variant)
    load_inventory(tree)
    entry_barcode.focus()
    root.mainloop()

if __name__ == '__main__':
    main() 