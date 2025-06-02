import tkinter as tk
from tkinter import ttk
from .product_view import ProductView
from .customer_view import CustomerView
from .order_view import OrderView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Shop Manager")
        self.root.geometry("800x600")

        # Tạo notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Tạo các tab
        self.product_frame = ttk.Frame(self.notebook)
        self.customer_frame = ttk.Frame(self.notebook)
        self.order_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.product_frame, text="Quản lý sản phẩm")
        self.notebook.add(self.customer_frame, text="Quản lý khách hàng")
        self.notebook.add(self.order_frame, text="Quản lý đơn hàng")

        # Khởi tạo các view
        ProductView(self.product_frame)
        CustomerView(self.customer_frame)
        OrderView(self.order_frame)