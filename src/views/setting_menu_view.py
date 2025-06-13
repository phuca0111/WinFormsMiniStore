import tkinter as tk
from tkinter import ttk
from src.views.account_view import AccountView
from src.views.store_view import StoreView
# import các view khác nếu cần

class SettingMenuView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.window = tk.Toplevel(parent)  # Luôn tạo Toplevel mới
        self.window.title("Cài đặt hệ thống")
        self.window.geometry("300x300")

        for widget in self.window.winfo_children():
            widget.destroy()

        ttk.Label(self.window, text="Chức năng cài đặt", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(self.window, text="Quản lý tài khoản", width=25, command=self.open_account).pack(pady=5)
        ttk.Button(self.window, text="Quản lý cửa hàng", width=25, command=self.open_store).pack(pady=5)
        # Thêm các nút khác nếu cần

    def open_account(self):
        AccountView(self.window)  # Mở form con với parent là cửa sổ menu cài đặt

    def open_store(self):
        StoreView(self.window, self.db_path)  # Mở form con với parent là cửa sổ menu cài đặt 