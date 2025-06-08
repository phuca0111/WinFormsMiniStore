import tkinter as tk
from tkinter import ttk

class ProductView:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        # Nhãn
        ttk.Label(self.frame, text="Quản lý sản phẩm").pack(pady=20)

        # Trường nhập liệu
        self.id_entry = ttk.Entry(self.frame)
        self.name_entry = ttk.Entry(self.frame)
        self.price_entry = ttk.Entry(self.frame)
        self.quantity_entry = ttk.Entry(self.frame)

        ttk.Label(self.frame, text="Mã sản phẩm:").pack()
        self.id_entry.pack(pady=5)
        ttk.Label(self.frame, text="Tên sản phẩm:").pack()
        self.name_entry.pack(pady=5)
        ttk.Label(self.frame, text="Giá:").pack()
        self.price_entry.pack(pady=5)
        ttk.Label(self.frame, text="Số lượng:").pack()
        self.quantity_entry.pack(pady=5)

        # Nút
        ttk.Button(self.frame, text="Thêm sản phẩm", command=self.add_product).pack(pady=10)
        ttk.Button(self.frame, text="Tìm kiếm sản phẩm", command=self.search_product).pack(pady=5)

        # Bảng
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Price", "Quantity"), show="headings")
        self.tree.heading("ID", text="Mã sản phẩm")
        self.tree.heading("Name", text="Tên sản phẩm")
        self.tree.heading("Price", text="Giá")
        self.tree.heading("Quantity", text="Số lượng")
        self.tree.pack(pady=10)

    def add_product(self):
        print("Đang thêm sản phẩm:", self.id_entry.get(), self.name_entry.get())

    def search_product(self):
        print("Đang tìm kiếm sản phẩm:", self.id_entry.get())