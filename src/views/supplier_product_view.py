import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tkinter import *
from tkinter import ttk, messagebox
from Core.supplier_product_core import SupplierProductCore
from datetime import datetime

class SupplierProductView:
    def __init__(self, parent):
        self.parent = parent
        self.core = SupplierProductCore()
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Frame chính
        self.main_frame = Frame(self.parent)
        self.main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame cho form nhập liệu
        self.form_frame = LabelFrame(self.main_frame, text="Thông tin nhập hàng")
        self.form_frame.pack(fill=X, padx=5, pady=5)

        # Nhà cung cấp
        Label(self.form_frame, text="Nhà cung cấp:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(self.form_frame, textvariable=self.supplier_var, state="readonly")
        self.supplier_combo.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.load_suppliers()

        # Biến thể sản phẩm
        Label(self.form_frame, text="Biến thể sản phẩm:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.variant_var = StringVar()
        self.variant_combo = ttk.Combobox(self.form_frame, textvariable=self.variant_var, state="readonly")
        self.variant_combo.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        self.load_variants()

        # Số lượng nhập
        Label(self.form_frame, text="Số lượng nhập:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.quantity_var = StringVar()
        Entry(self.form_frame, textvariable=self.quantity_var).grid(row=2, column=1, padx=5, pady=5, sticky=W)

        # Giá nhập
        Label(self.form_frame, text="Giá nhập:").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.price_var = StringVar()
        Entry(self.form_frame, textvariable=self.price_var).grid(row=3, column=1, padx=5, pady=5, sticky=W)

        # Frame cho các nút
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack(fill=X, padx=5, pady=5)

        # Các nút chức năng
        Button(self.button_frame, text="Thêm", command=self.add_supplier_product).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Sửa", command=self.edit_supplier_product).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Xóa", command=self.delete_supplier_product).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Làm mới", command=self.load_data).pack(side=LEFT, padx=5)

        # Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Nhà cung cấp", "Sản phẩm", "Biến thể", 
                                                          "Ngày nhập", "Số lượng", "Giá nhập"),
                                 show="headings")
        
        # Định dạng các cột
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nhà cung cấp", text="Nhà cung cấp")
        self.tree.heading("Sản phẩm", text="Sản phẩm")
        self.tree.heading("Biến thể", text="Biến thể")
        self.tree.heading("Ngày nhập", text="Ngày nhập")
        self.tree.heading("Số lượng", text="Số lượng")
        self.tree.heading("Giá nhập", text="Giá nhập")

        self.tree.column("ID", width=50)
        self.tree.column("Nhà cung cấp", width=150)
        self.tree.column("Sản phẩm", width=150)
        self.tree.column("Biến thể", width=150)
        self.tree.column("Ngày nhập", width=150)
        self.tree.column("Số lượng", width=100)
        self.tree.column("Giá nhập", width=100)

        self.tree.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind sự kiện chọn item
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_suppliers(self):
        suppliers = self.core.get_all_suppliers()
        self.supplier_combo['values'] = [f"{s.id} - {s.ten}" for s in suppliers]
        if suppliers:
            self.supplier_combo.current(0)

    def load_variants(self):
        variants = self.core.get_all_product_variants()
        self.variant_combo['values'] = [f"{v.id} - {v.ten_bienthe}" for v in variants]
        if variants:
            self.variant_combo.current(0)

    def load_data(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy và hiển thị dữ liệu mới
        supplier_products = self.core.get_all_supplier_products()
        for sp in supplier_products:
            self.tree.insert("", END, values=sp)

    def get_selected_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            # Cập nhật các trường nhập liệu
            self.supplier_var.set(f"{values[1]}")
            self.variant_var.set(f"{values[2]} ({values[3]})")
            self.quantity_var.set(values[5])
            self.price_var.set(values[6])

    def clear_form(self):
        self.supplier_var.set("")
        self.variant_var.set("")
        self.quantity_var.set("")
        self.price_var.set("")

    def add_supplier_product(self):
        try:
            # Lấy ID từ combobox
            supplier_id = int(self.supplier_var.get().split(" - ")[0])
            variant_id = int(self.variant_var.get().split(" - ")[0])
            quantity = int(self.quantity_var.get())
            price = float(self.price_var.get())

            # Thêm mới
            self.core.create_supplier_product(supplier_id, variant_id, quantity, price)
            messagebox.showinfo("Thành công", "Thêm nhập hàng thành công!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm nhập hàng: {str(e)}")

    def edit_supplier_product(self):
        try:
            id = self.get_selected_id()
            if id is None:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi để sửa!")
                return

            # Lấy ID từ combobox
            supplier_id = int(self.supplier_var.get().split(" - ")[0])
            variant_id = int(self.variant_var.get().split(" - ")[0])
            quantity = int(self.quantity_var.get())
            price = float(self.price_var.get())

            # Cập nhật
            if self.core.update_supplier_product(id, supplier_id, variant_id, quantity, price):
                messagebox.showinfo("Thành công", "Cập nhật nhập hàng thành công!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy bản ghi để cập nhật!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật nhập hàng: {str(e)}")

    def delete_supplier_product(self):
        try:
            id = self.get_selected_id()
            if id is None:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi để xóa!")
                return

            if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bản ghi này?"):
                if self.core.delete_supplier_product(id):
                    messagebox.showinfo("Thành công", "Xóa nhập hàng thành công!")
                    self.clear_form()
                    self.load_data()
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy bản ghi để xóa!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa nhập hàng: {str(e)}") 