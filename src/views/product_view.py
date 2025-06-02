import tkinter as tk
from tkinter import ttk

class ProductView:
    def __init__(self, parent):
        self.parent = parent

        # Nhãn
        ttk.Label(self.parent, text="Quản lý sản phẩm").pack(pady=20)

        # Trường nhập liệu
        self.id_entry = ttk.Entry(self.parent)
        self.name_entry = ttk.Entry(self.parent)
        self.price_entry = ttk.Entry(self.parent)
        self.quantity_entry = ttk.Entry(self.parent)

        ttk.Label(self.parent, text="Mã sản phẩm:").pack()
        self.id_entry.pack(pady=5)
        ttk.Label(self.parent, text="Tên sản phẩm:").pack()
        self.name_entry.pack(pady=5)
        ttk.Label(self.parent, text="Giá:").pack()
        self.price_entry.pack(pady=5)
        ttk.Label(self.parent, text="Số lượng:").pack()
        self.quantity_entry.pack(pady=5)

        # Nút
        ttk.Button(self.parent, text="Thêm sản phẩm", command=self.add_product).pack(pady=10)
        ttk.Button(self.parent, text="Tìm kiếm sản phẩm", command=self.search_product).pack(pady=5)

        # Bảng
        self.tree = ttk.Treeview(self.parent, columns=("ID", "Name", "Price", "Quantity"), show="headings")
        self.tree.heading("ID", text="Mã sản phẩm")
        self.tree.heading("Name", text="Tên sản phẩm")
        self.tree.heading("Price", text="Giá")
        self.tree.heading("Quantity", text="Số lượng")
        self.tree.pack(pady=10)

    def add_product(self):
        print("Đang thêm sản phẩm:", self.id_entry.get(), self.name_entry.get())

    def search_product(self):
        print("Đang tìm kiếm sản phẩm:", self.id_entry.get())