import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk
from Core.inventory import (
    load_inventory, load_variant_combobox, on_add, on_update, on_delete, on_select, on_scan_barcode, on_barcode_entered
)

class InventoryView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#F5F7FA")
        self.setup_ui()
        load_variant_combobox(self.combobox_variant)
        load_inventory(self.tree)
        self.entry_barcode.focus()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#F5F7FA", relief="flat")
        style.configure("Custom.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#F5F7FA")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")
        style.configure("TCombobox", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff", fieldbackground="#fff")
        style.map("TCombobox",
            fieldbackground=[('readonly', '#fff'), ('!disabled', '#fff')],
            background=[('readonly', '#fff'), ('!disabled', '#fff')]
        )

        # Bảng bo tròn giả lập
        table_frame = tk.Frame(self, bg="#F5F7FA")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(32, 16))
        table_border = tk.Frame(table_frame, bg="#DDE2E6", bd=0)
        table_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        columns = ('ID', 'Tên sản phẩm', 'Tên biến thể', 'Barcode', 'Số lượng')
        self.tree = ttk.Treeview(table_inner, columns=columns, show='headings', height=6, style="Custom.Treeview")
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Tên sản phẩm', width=180, anchor="w")
        self.tree.column('Tên biến thể', width=180, anchor="w")
        self.tree.column('Barcode', width=160, anchor="center")
        self.tree.column('Số lượng', width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        scrollbar = tk.Scrollbar(table_inner, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Khung nhập thông tin bo tròn, input cùng hàng
        input_frame = tk.LabelFrame(self, text="Nhập thông tin", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222", bd=0)
        input_frame.pack(fill=tk.X, padx=120, pady=8)
        # Barcode
        tk.Label(input_frame, text="Barcode:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222").grid(row=0, column=0, sticky="e", padx=8, pady=8)
        self.entry_barcode = ttk.Entry(input_frame, font=("Segoe UI", 12), width=18)
        self.entry_barcode.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        self.entry_barcode.bind('<Return>', lambda e: on_barcode_entered(self.entry_barcode, self.combobox_variant))
        # Sản phẩm
        tk.Label(input_frame, text="Sản phẩm:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222").grid(row=0, column=2, sticky="e", padx=8, pady=8)
        self.combobox_variant = ttk.Combobox(input_frame, font=("Segoe UI", 12), state='readonly', style="TCombobox", width=18)
        self.combobox_variant.grid(row=0, column=3, sticky="ew", padx=8, pady=8)
        # Số lượng
        tk.Label(input_frame, text="Số lượng:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222").grid(row=0, column=4, sticky="e", padx=8, pady=8)
        self.entry_soluong = ttk.Entry(input_frame, font=("Segoe UI", 12), width=10)
        self.entry_soluong.grid(row=0, column=5, sticky="ew", padx=8, pady=8)
        # Nút quét mã vạch
        btn_scan = tk.Button(input_frame, text="Quét mã vạch (Camera)", font=("Segoe UI", 12, "bold"), command=lambda: on_scan_barcode(self.entry_barcode, self.combobox_variant, None))
        btn_scan.configure(bg="#eafaf1", fg="#222", activebackground="#d1f2eb", activeforeground="#222", relief="flat", bd=0, cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
        btn_scan.bind("<Enter>", lambda e: btn_scan.configure(bg="#d1f2eb"))
        btn_scan.bind("<Leave>", lambda e: btn_scan.configure(bg="#eafaf1"))
        btn_scan.grid(row=0, column=6, sticky="ew", padx=8, pady=8)
        # Responsive: chia đều các cột
        input_frame.grid_columnconfigure(1, weight=2, minsize=120)
        input_frame.grid_columnconfigure(3, weight=2, minsize=120)
        input_frame.grid_columnconfigure(5, weight=1, minsize=80)
        input_frame.grid_columnconfigure(6, weight=2, minsize=140)

        # Nút chức năng pastel bo tròn
        btn_frame = tk.Frame(self, bg="#F5F7FA")
        btn_frame.pack(fill=tk.X, padx=32, pady=(0, 32))
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Thêm', command=lambda: on_add(self.combobox_variant, self.entry_soluong, self.entry_barcode, self.tree))
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_update = tk.Button(btn_frame, text='Sửa', command=lambda: on_update(self.tree, self.combobox_variant, self.entry_soluong, self.entry_barcode))
        style_btn(btn_update, "#f9e7cf", "#f6cba3")
        btn_update.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=lambda: on_delete(self.tree, self.combobox_variant, self.entry_soluong, self.entry_barcode))
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=lambda: load_inventory(self.tree))
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.entry_soluong.delete(0, tk.END)
            self.entry_soluong.insert(0, item['values'][4])  # Số lượng
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, item['values'][3])  # Barcode
            bienthe_id = item['values'][5]
            for v in self.combobox_variant['values']:
                if v.startswith(str(bienthe_id) + ' -'):
                    self.combobox_variant.set(v)
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryView(root)
    root.mainloop() 