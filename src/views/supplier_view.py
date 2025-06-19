import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Thêm đường dẫn gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Core.supplier_core import SupplierCore

class SupplierView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#F5F7FA")
        self.setup_ui()
        self.load_suppliers()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#F5F7FA", relief="flat")
        style.configure("Custom.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#F5F7FA")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")

        # Input có label, padding lớn, bố cục cùng hàng
        input_frame = tk.LabelFrame(self, text="Thông tin nhà cung cấp", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222", bd=0)
        input_frame.pack(fill=tk.X, padx=32, pady=(24, 8))
        tk.Label(input_frame, text="Tên:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=0, sticky="e", padx=8, pady=8)
        self.entry_name = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Địa chỉ:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=1, column=0, sticky="e", padx=8, pady=8)
        self.entry_address = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_address.grid(row=1, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="SĐT:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=2, column=0, sticky="e", padx=8, pady=8)
        self.entry_phone = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_phone.grid(row=2, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Email:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=3, column=0, sticky="e", padx=8, pady=8)
        self.entry_email = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_email.grid(row=3, column=1, sticky="ew", padx=8, pady=8)
        # Responsive: cho entry co giãn
        input_frame.grid_columnconfigure(1, weight=1)

        # Nút chức năng pastel bo tròn
        btn_frame = tk.Frame(self, bg="#F5F7FA")
        btn_frame.pack(fill=tk.X, padx=32, pady=(0, 16))
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Thêm', command=self.on_add)
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_update = tk.Button(btn_frame, text='Sửa', command=self.on_update)
        style_btn(btn_update, "#f9e7cf", "#f6cba3")
        btn_update.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=self.on_delete)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.load_suppliers)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)

        # Bảng bo tròn giả lập
        table_frame = tk.Frame(self, bg="#F5F7FA")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(0, 32))
        table_border = tk.Frame(table_frame, bg="#DDE2E6", bd=0)
        table_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        columns = ('ID', 'Tên', 'Địa chỉ', 'SĐT', 'Email')
        self.tree = ttk.Treeview(table_inner, columns=columns, show='headings', height=8, style="Custom.Treeview")
        self.tree.heading('ID', text='ID', anchor="center")
        self.tree.heading('Tên', text='Tên', anchor="w")
        self.tree.heading('Địa chỉ', text='Địa chỉ', anchor="w")
        self.tree.heading('SĐT', text='SĐT', anchor="center")
        self.tree.heading('Email', text='Email', anchor="w")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Tên', width=180, anchor="w")
        self.tree.column('Địa chỉ', width=250, anchor="w")
        self.tree.column('SĐT', width=120, anchor="center")
        self.tree.column('Email', width=180, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Biến lưu ID nhà cung cấp đang được chọn
        self.selected_id = None

    def load_suppliers(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy và hiển thị dữ liệu mới
        suppliers = SupplierCore.get_all_suppliers()
        for supplier in suppliers:
            self.tree.insert("", "end", values=(
                supplier.id,
                supplier.ten,
                supplier.diachi,
                supplier.sdt,
                supplier.gmail
            ))

    def clear_inputs(self):
        self.entry_name.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.selected_id = None

    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            self.selected_id = item["values"][0]
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, item["values"][1])
            self.entry_address.delete(0, tk.END)
            self.entry_address.insert(0, item["values"][2])
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, item["values"][3])
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, item["values"][4])

    def on_add(self):
        success, result = SupplierCore.add_supplier(
            self.entry_name.get(),
            self.entry_address.get(),
            self.entry_phone.get(),
            self.entry_email.get()
        )
        
        if success:
            self.clear_inputs()
            self.load_suppliers()
            messagebox.showinfo("Thành công", result)
        else:
            messagebox.showerror("Lỗi", "\n".join(result))

    def on_update(self):
        if not self.selected_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhà cung cấp cần sửa!")
            return

        success, result = SupplierCore.update_supplier(
            self.selected_id,
            self.entry_name.get(),
            self.entry_address.get(),
            self.entry_phone.get(),
            self.entry_email.get()
        )
        
        if success:
            self.clear_inputs()
            self.load_suppliers()
            messagebox.showinfo("Thành công", result)
        else:
            messagebox.showerror("Lỗi", "\n".join(result) if isinstance(result, list) else result)

    def on_delete(self):
        if not self.selected_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhà cung cấp cần xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa nhà cung cấp này?"):
            success, result = SupplierCore.delete_supplier(self.selected_id)
            if success:
                self.clear_inputs()
                self.load_suppliers()
                messagebox.showinfo("Thành công", result)
            else:
                messagebox.showerror("Lỗi", result) 