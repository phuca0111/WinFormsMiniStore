import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý MiniStore")
        self.root.geometry("1000x700")
        self.create_menu()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Menu', menu=manage_menu)
        manage_menu.add_command(label='Tài khoản', command=self.open_account)
        manage_menu.add_command(label='Loại sản phẩm', command=self.open_category)
        manage_menu.add_command(label='Khách hàng', command=self.open_customer)
        manage_menu.add_command(label='Tồn kho', command=self.open_inventory)
        manage_menu.add_command(label='Đơn hàng', command=self.open_order)
        manage_menu.add_command(label='Thanh toán', command=self.open_payment)
        manage_menu.add_command(label='Nhà sản xuất', command=self.open_producer)
        manage_menu.add_command(label='Biến thể sản phẩm', command=self.open_product_variant)
        manage_menu.add_command(label='Sản phẩm', command=self.open_product)
        manage_menu.add_separator()
        manage_menu.add_command(label='Thoát', command=self.root.quit)

    def open_account(self):
        account_view_path = os.path.join(os.path.dirname(__file__), 'account_view.py')
        subprocess.Popen([sys.executable, account_view_path])

    def open_category(self):
        category_view_path = os.path.join(os.path.dirname(__file__), 'category_view.py')
        subprocess.Popen([sys.executable, category_view_path])

    def open_customer(self):
        customer_view_path = os.path.join(os.path.dirname(__file__), 'customer_view.py')
        subprocess.Popen([sys.executable, customer_view_path])

    def open_inventory(self):
        inventory_view_path = os.path.join(os.path.dirname(__file__), 'inventory_view.py')
        subprocess.Popen([sys.executable, inventory_view_path])

    def open_order(self):
        order_view_path = os.path.join(os.path.dirname(__file__), 'order_view.py')
        subprocess.Popen([sys.executable, order_view_path])

    def open_payment(self):
        payment_view_path = os.path.join(os.path.dirname(__file__), 'payment_view.py')
        subprocess.Popen([sys.executable, payment_view_path])

    def open_producer(self):
        producer_view_path = os.path.join(os.path.dirname(__file__), 'producer_view.py')
        subprocess.Popen([sys.executable, producer_view_path])

    def open_product_variant(self):
        product_variant_view_path = os.path.join(os.path.dirname(__file__), 'product_variant_view.py')
        subprocess.Popen([sys.executable, product_variant_view_path])

    def open_product(self):
        product_view_path = os.path.join(os.path.dirname(__file__), 'product_view.py')
        subprocess.Popen([sys.executable, product_view_path])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()