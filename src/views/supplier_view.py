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
        self.parent = parent
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Frame chứa form nhập liệu
        input_frame = ttk.LabelFrame(self, text="Thông tin nhà cung cấp")
        input_frame.pack(fill="x", padx=5, pady=5)

        # Tên nhà cung cấp
        ttk.Label(input_frame, text="Tên:").grid(row=0, column=0, padx=5, pady=5)
        self.ten_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.ten_var).grid(row=0, column=1, padx=5, pady=5)

        # Địa chỉ
        ttk.Label(input_frame, text="Địa chỉ:").grid(row=1, column=0, padx=5, pady=5)
        self.diachi_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.diachi_var).grid(row=1, column=1, padx=5, pady=5)

        # Số điện thoại
        ttk.Label(input_frame, text="SĐT:").grid(row=2, column=0, padx=5, pady=5)
        self.sdt_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.sdt_var).grid(row=2, column=1, padx=5, pady=5)

        # Email
        ttk.Label(input_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.gmail_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.gmail_var).grid(row=3, column=1, padx=5, pady=5)

        # Frame chứa các nút
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Thêm", command=self.add_supplier).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.edit_supplier).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_supplier).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Làm mới", command=self.refresh_data).pack(side="left", padx=5)

        # Treeview để hiển thị danh sách
        self.tree = ttk.Treeview(self, columns=("ID", "Tên", "Địa chỉ", "SĐT", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Địa chỉ", text="Địa chỉ")
        self.tree.heading("SĐT", text="SĐT")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind sự kiện chọn item
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Biến lưu ID nhà cung cấp đang được chọn
        self.selected_id = None

    def load_data(self):
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
        self.ten_var.set("")
        self.diachi_var.set("")
        self.sdt_var.set("")
        self.gmail_var.set("")
        self.selected_id = None

    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            self.selected_id = item["values"][0]
            self.ten_var.set(item["values"][1])
            self.diachi_var.set(item["values"][2])
            self.sdt_var.set(item["values"][3])
            self.gmail_var.set(item["values"][4])

    def add_supplier(self):
        success, result = SupplierCore.add_supplier(
            self.ten_var.get(),
            self.diachi_var.get(),
            self.sdt_var.get(),
            self.gmail_var.get()
        )
        
        if success:
            self.clear_inputs()
            self.load_data()
            messagebox.showinfo("Thành công", result)
        else:
            messagebox.showerror("Lỗi", "\n".join(result))

    def edit_supplier(self):
        if not self.selected_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhà cung cấp cần sửa!")
            return

        success, result = SupplierCore.update_supplier(
            self.selected_id,
            self.ten_var.get(),
            self.diachi_var.get(),
            self.sdt_var.get(),
            self.gmail_var.get()
        )
        
        if success:
            self.clear_inputs()
            self.load_data()
            messagebox.showinfo("Thành công", result)
        else:
            messagebox.showerror("Lỗi", "\n".join(result) if isinstance(result, list) else result)

    def delete_supplier(self):
        if not self.selected_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhà cung cấp cần xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa nhà cung cấp này?"):
            success, result = SupplierCore.delete_supplier(self.selected_id)
            if success:
                self.clear_inputs()
                self.load_data()
                messagebox.showinfo("Thành công", result)
            else:
                messagebox.showerror("Lỗi", result)

    def refresh_data(self):
        self.clear_inputs()
        self.load_data() 