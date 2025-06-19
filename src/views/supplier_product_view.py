import tkinter as tk
from tkinter import ttk, messagebox, END
import sys
import os

# Thêm thư mục hiện tại vào PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from Core.supplier_product_core import SupplierProductCore
from datetime import datetime
from models.supplier_model import Supplier
from models.product_variant_model import ProductVariant
from models.supplier_product_model import SupplierProduct

class SupplierProductView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#F5F7FA")
        self.core = SupplierProductCore()
        self.setup_ui()
        self.load_suppliers()
        self.load_variants()
        self.load_data()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#F5F7FA", relief="flat")
        style.configure("Custom.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#F5F7FA")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")
        style.configure("TCombobox", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")

        # Input có label, padding lớn, bố cục cùng hàng
        input_frame = tk.LabelFrame(self, text="Thông tin nhập hàng", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222", bd=0)
        input_frame.pack(fill=tk.X, padx=32, pady=(24, 8))
        tk.Label(input_frame, text="Nhà cung cấp:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=0, column=0, sticky="e", padx=8, pady=8)
        self.combo_supplier = ttk.Combobox(input_frame, font=("Segoe UI", 12))
        self.combo_supplier.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Biến thể sản phẩm:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=1, column=0, sticky="e", padx=8, pady=8)
        self.combo_variant = ttk.Combobox(input_frame, font=("Segoe UI", 12))
        self.combo_variant.grid(row=1, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Số lượng nhập:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=2, column=0, sticky="e", padx=8, pady=8)
        self.entry_qty = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_qty.grid(row=2, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Giá nhập:", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=3, column=0, sticky="e", padx=8, pady=8)
        self.entry_price = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_price.grid(row=3, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Hạn sử dụng (YYYY-MM-DD):", font=("Segoe UI", 12), bg="#F5F7FA", fg="#222").grid(row=4, column=0, sticky="e", padx=8, pady=8)
        self.entry_expiry = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_expiry.grid(row=4, column=1, sticky="ew", padx=8, pady=8)
        # Responsive: cho entry, combobox co giãn
        input_frame.grid_columnconfigure(1, weight=1)

        # Nút chức năng pastel bo tròn
        btn_frame = tk.Frame(self, bg="#F5F7FA")
        btn_frame.pack(fill=tk.X, padx=32, pady=(0, 16))
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Thêm', command=self.add_supplier_product)
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_update = tk.Button(btn_frame, text='Sửa', command=self.edit_supplier_product)
        style_btn(btn_update, "#f9e7cf", "#f6cba3")
        btn_update.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=self.delete_supplier_product)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.load_data)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)

        # Bảng bo tròn giả lập
        table_frame = tk.Frame(self, bg="#F5F7FA")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(0, 32))
        table_border = tk.Frame(table_frame, bg="#DDE2E6", bd=0)
        table_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        columns = ('ID', 'Mã lô', 'Nhà cung cấp', 'Sản phẩm', 'Biến thể', 'Ngày nhập', 'Số lượng', 'Giá nhập', 'Hạn sử dụng')
        self.tree = ttk.Treeview(table_inner, columns=columns, show='headings', height=10, style="Custom.Treeview")
        self.tree.heading('ID', text='ID', anchor="center")
        self.tree.heading('Mã lô', text='Mã lô', anchor="w")
        self.tree.heading('Nhà cung cấp', text='Nhà cung cấp', anchor="w")
        self.tree.heading('Sản phẩm', text='Sản phẩm', anchor="w")
        self.tree.heading('Biến thể', text='Biến thể', anchor="w")
        self.tree.heading('Ngày nhập', text='Ngày nhập', anchor="center")
        self.tree.heading('Số lượng', text='Số lượng', anchor="center")
        self.tree.heading('Giá nhập', text='Giá nhập', anchor="center")
        self.tree.heading('Hạn sử dụng', text='Hạn sử dụng', anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Mã lô', width=120, anchor="w")
        self.tree.column('Nhà cung cấp', width=150, anchor="w")
        self.tree.column('Sản phẩm', width=120, anchor="w")
        self.tree.column('Biến thể', width=150, anchor="w")
        self.tree.column('Ngày nhập', width=120, anchor="center")
        self.tree.column('Số lượng', width=80, anchor="center")
        self.tree.column('Giá nhập', width=100, anchor="center")
        self.tree.column('Hạn sử dụng', width=120, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        scrollbar = tk.Scrollbar(table_inner, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_suppliers(self):
        try:
            suppliers = Supplier.get_all()
            self.combo_supplier['values'] = [f"{s.id} - {s.ten}" for s in suppliers]
            if suppliers:
                self.combo_supplier.set(f"{suppliers[0].id} - {suppliers[0].ten}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách nhà cung cấp: {str(e)}")

    def load_variants(self):
        try:
            variants = ProductVariant.get_all()
            self.combo_variant['values'] = [f"{v.id} - {v.ten_bienthe}" for v in variants]
            if variants:
                self.combo_variant.set(f"{variants[0].id} - {variants[0].ten_bienthe}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách biến thể: {str(e)}")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        supplier_products = self.core.get_all_supplier_products()
        for sp in supplier_products:
            self.tree.insert("", "end", values=sp)

    def get_selected_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            for v in self.combo_supplier['values']:
                if v.endswith(f"- {values[2]}"):
                    self.combo_supplier.set(v)
                    break
            for v in self.combo_variant['values']:
                if v.endswith(f"- {values[4]}"):
                    self.combo_variant.set(v)
                    break
            self.entry_qty.delete(0, END)
            self.entry_qty.insert(0, values[6])
            self.entry_price.delete(0, END)
            self.entry_price.insert(0, values[7])
            if len(values) > 8:
                self.entry_expiry.delete(0, END)
                self.entry_expiry.insert(0, values[8])
            else:
                self.entry_expiry.delete(0, END)

    def clear_form(self):
        self.combo_supplier.delete(0, END)
        self.combo_variant.delete(0, END)
        self.entry_qty.delete(0, END)
        self.entry_price.delete(0, END)
        self.entry_expiry.delete(0, END)

    def add_supplier_product(self):
        try:
            supplier_id = int(self.combo_supplier.get().split(' - ')[0])
            variant_id = int(self.combo_variant.get().split(' - ')[0])
            qty = int(self.entry_qty.get())
            price = float(self.entry_price.get())
            expiry = self.entry_expiry.get()

            if not all([supplier_id, variant_id, qty, price, expiry]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return

            # Tạo mã lô tự động
            batch_code = f"B{datetime.now().strftime('%Y%m%d%H%M%S')}"

            self.core.create_supplier_product(supplier_id, variant_id, qty, price, expiry)
            messagebox.showinfo("Thành công", "Thêm nhập hàng thành công!")
            self.load_data()
            self.clear_form()
        except ValueError as e:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm nhập hàng: {str(e)}")

    def edit_supplier_product(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showerror("Lỗi", "Vui lòng chọn nhập hàng cần sửa!")
                return

            supplier_id = int(self.combo_supplier.get().split(' - ')[0])
            variant_id = int(self.combo_variant.get().split(' - ')[0])
            qty = int(self.entry_qty.get())
            price = float(self.entry_price.get())
            expiry = self.entry_expiry.get()

            if not all([supplier_id, variant_id, qty, price, expiry]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return

            item_id = self.tree.item(selected[0])['values'][0]
            self.core.update_supplier_product(item_id, supplier_id, variant_id, qty, price, expiry)
            messagebox.showinfo("Thành công", "Cập nhật nhập hàng thành công!")
            self.load_data()
            self.clear_form()
        except ValueError as e:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")
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