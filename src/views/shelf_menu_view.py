import tkinter as tk
from tkinter import ttk
from src.views.shelf_view import ShelfView
from src.views.product_on_shelf_view import ProductOnShelfView

class ShelfMenuView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.window = tk.Toplevel(parent)
        self.window.title("Menu Kệ hàng")
        self.window.geometry("300x200")

        ttk.Label(self.window, text="Chức năng kệ hàng", font=("Arial", 14, "bold")).pack(pady=10, fill=tk.X, expand=True)
        ttk.Button(self.window, text="Quản lý kệ", width=25, command=self.open_shelf).pack(pady=5, fill=tk.X, expand=True)
        ttk.Button(self.window, text="Quản lý sản phẩm trên kệ", width=25, command=self.open_product_on_shelf).pack(pady=5, fill=tk.X, expand=True)

    def open_shelf(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        shelf_view = ShelfView(self.window, self.db_path)
        shelf_view.pack(fill=tk.BOTH, expand=True)

    def open_product_on_shelf(self):
        ProductOnShelfView(self.window, self.db_path) 