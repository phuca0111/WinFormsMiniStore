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

class InventoryView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1) # Row for the treeview
        self.setup_ui()

    def setup_ui(self):
        title_label = ttk.Label(self.frame, text="Tổng kho", font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=10, sticky=tk.N)

        input_frame = ttk.LabelFrame(self.frame, text='Nhập thông tin', padding=10)
        input_frame.grid(row=1, column=0, padx=10, pady=5, sticky=tk.EW)
        input_frame.columnconfigure(1, weight=1) # Make the second column (for inputs) expand
        input_frame.columnconfigure(0, weight=0)
        input_frame.columnconfigure(2, weight=0)
        input_frame.columnconfigure(3, weight=0)

        ttk.Label(input_frame, text='Sản phẩm:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_variant = ttk.Combobox(input_frame, font=('Arial', 12), state='readonly')
        self.combobox_variant.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        self.label_sanpham = ttk.Label(input_frame, text='', font=('Arial', 12), foreground='blue')
        self.label_sanpham.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text='Barcode:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_barcode = BarcodeEntry(
            input_frame,
            font=('Arial', 12),
            on_barcode_entered=lambda barcode: on_barcode_entered(barcode, self.combobox_variant, self.label_sanpham)
        )
        self.entry_barcode.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(input_frame, text='(Quét mã vạch hoặc nhập tay)', 
                 font=('Arial', 8), foreground='gray').grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        btn_scan = ttk.Button(input_frame, text="Quét mã vạch (Camera)",
            command=lambda: on_scan_barcode(self.entry_barcode, self.combobox_variant, self.label_sanpham))
        btn_scan.grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text='Số lượng:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_soluong = ttk.Entry(input_frame, font=('Arial', 12))
        self.entry_soluong.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        columns = ('ID', 'Tên sản phẩm', 'Tên biến thể', 'Barcode', 'Số lượng', 'bienthe_id')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column('bienthe_id', width=0, stretch=False)
        self.tree.grid(row=2, column=0, padx=10, pady=5, sticky=tk.NSEW)

        frame_btn = ttk.Frame(self.frame)
        frame_btn.grid(row=3, column=0, pady=5, sticky=tk.EW)
        frame_btn.columnconfigure(0, weight=1)
        frame_btn.columnconfigure(1, weight=1)
        frame_btn.columnconfigure(2, weight=1)
        frame_btn.columnconfigure(3, weight=1)

        btn_add = ttk.Button(frame_btn, text='Thêm', width=15, 
                            command=lambda: on_add(self.combobox_variant, self.entry_soluong, self.entry_barcode, self.tree))
        btn_update = ttk.Button(frame_btn, text='Sửa', width=15,
                               command=lambda: on_update(self.tree, self.combobox_variant, self.entry_soluong, self.entry_barcode))
        btn_delete = ttk.Button(frame_btn, text='Xóa', width=15,
                               command=lambda: on_delete(self.tree, self.combobox_variant, self.entry_soluong, self.entry_barcode))
        btn_refresh = ttk.Button(frame_btn, text='Làm mới', width=15,
                                command=lambda: [load_variant_combobox(self.combobox_variant), load_inventory(self.tree)])
        btn_add.grid(row=0, column=0, padx=5, sticky=tk.EW)
        btn_update.grid(row=0, column=1, padx=5, sticky=tk.EW)
        btn_delete.grid(row=0, column=2, padx=5, sticky=tk.EW)
        btn_refresh.grid(row=0, column=3, padx=5, sticky=tk.EW)

        self.tree.bind('<<TreeviewSelect>>', 
                      lambda e: on_select(e, self.tree, self.combobox_variant, self.entry_soluong, self.entry_barcode))

        load_variant_combobox(self.combobox_variant)
        load_inventory(self.tree)
        self.entry_barcode.focus()

def main():
    root = tk.Tk()
    root.title('Quản lý tồn kho')
    root.geometry('800x600')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = InventoryView(root)
    app.frame.grid(row=0, column=0, sticky=tk.NSEW)
    root.mainloop()

if __name__ == '__main__':
    main() 