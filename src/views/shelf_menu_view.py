import tkinter as tk
from tkinter import ttk
from src.views.shelf_view import ShelfView
from src.views.product_on_shelf_view import ProductOnShelfView

class ShelfMenuView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        label = ttk.Label(self.frame, text='Quản lý kệ hàng (Chưa triển khai)', font=("Arial", 14))
        label.pack(padx=20, pady=20)

    def open_shelf(self):
        ShelfView(self.window, self.db_path)

    def open_product_on_shelf(self):
        ProductOnShelfView(self.window, self.db_path) 