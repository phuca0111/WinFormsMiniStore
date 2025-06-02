import tkinter as tk
from tkinter import ttk

class CustomerView:
    def __init__(self, parent):
        self.parent = parent

        # Nhãn
        ttk.Label(self.parent, text="Quản lý khách hàng").pack(pady=20)

        # Trường nhập liệu
        self.id_entry = ttk.Entry(self.parent)
        self.name_entry = ttk.Entry(self.parent)
        self.phone_entry = ttk.Entry(self.parent)

        ttk.Label(self.parent, text="Mã khách hàng:").pack()
        self.id_entry.pack(pady=5)
        ttk.Label(self.parent, text="Tên khách hàng:").pack()
        self.name_entry.pack(pady=5)
        ttk.Label(self.parent, text="Số điện thoại:").pack()
        self.phone_entry.pack(pady=5)

        # Nút
        ttk.Button(self.parent, text="Thêm khách hàng", command=self.add_customer).pack(pady=10)

    def add_customer(self):
        print("Đang thêm khách hàng:", self.id_entry.get(), self.name_entry.get())