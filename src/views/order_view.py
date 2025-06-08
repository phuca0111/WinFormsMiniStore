import tkinter as tk
from tkinter import ttk


class OrderView:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        # Nhãn
        ttk.Label(self.frame, text="Quản lý đơn hàng").pack(pady=20)

        # Trường nhập liệu
        self.order_id_entry = ttk.Entry(self.frame)
        self.customer_id_entry = ttk.Entry(self.frame)

        ttk.Label(self.frame, text="Mã đơn hàng:").pack()
        self.order_id_entry.pack(pady=5)
        ttk.Label(self.frame, text="Mã khách hàng:").pack()
        self.customer_id_entry.pack(pady=5)

        # Nút
        ttk.Button(self.frame, text="Tạo đơn hàng", command=self.create_order).pack(pady=10)

    def create_order(self):
        print("Đang tạo đơn hàng:", self.order_id_entry.get())

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)