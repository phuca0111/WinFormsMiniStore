import tkinter as tk
from tkinter import ttk
from src.views.account_view import AccountView
from src.views.store_view import StoreView
# import các view khác nếu cần

class SettingMenuView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.parent = parent
        self.db_path = db_path
        self.current_view = None  # Lưu trữ view hiện tại

        # Cấu hình grid cho self.frame
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        row_idx = 0

        # Tiêu đề "Chức năng cài đặt"
        label = ttk.Label(self.frame, text="Cài đặt", font=("Arial", 18))
        label.grid(row=row_idx, column=0, padx=20, pady=5, sticky=tk.N)
        row_idx += 1

        # Frame chứa các nút
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=row_idx, column=0, pady=5, sticky=tk.N)
        row_idx += 1

        # Tạo giao diện trong frame
        ttk.Button(button_frame, text="Quản lý tài khoản", width=25, command=self.open_account).grid(row=0, column=0, pady=5, padx=5)
        ttk.Button(button_frame, text="Quản lý cửa hàng", width=25, command=self.open_store).grid(row=0, column=1, pady=5, padx=5)

        # Frame chứa nội dung
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.grid(row=row_idx, column=0, sticky=tk.NSEW, padx=10, pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def clear_current_view(self):
        if self.current_view:
            self.current_view.frame.grid_forget()
            self.current_view = None

    def open_account(self):
        self.clear_current_view()
        self.current_view = AccountView(self.content_frame, self.db_path)
        self.current_view.frame.grid(row=0, column=0, sticky=tk.NSEW)

    def open_store(self):
        self.clear_current_view()
        self.current_view = StoreView(self.content_frame, self.db_path)
        self.current_view.frame.grid(row=0, column=0, sticky=tk.NSEW) 