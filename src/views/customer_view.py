import tkinter as tk
from tkinter import ttk


class CustomerView:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        # Nhãn
        ttk.Label(self.frame, text="Quản lý khách hàng").pack(pady=20)

        # Trường nhập liệu
        self.id_entry = ttk.Entry(self.frame)
        self.name_entry = ttk.Entry(self.frame)
        self.phone_entry = ttk.Entry(self.frame)

        ttk.Label(self.frame, text="Mã khách hàng:").pack()
        self.id_entry.pack(pady=5)
        ttk.Label(self.frame, text="Tên khách hàng:").pack()
        self.name_entry.pack(pady=5)
        ttk.Label(self.frame, text="Số điện thoại:").pack()
        self.phone_entry.pack(pady=5)

        # Nút
        ttk.Button(self.frame, text="Thêm khách hàng", command=self.add_customer).pack(pady=10)

    def add_customer(self):
        print("Đang thêm khách hàng:", self.id_entry.get(), self.name_entry.get())

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)