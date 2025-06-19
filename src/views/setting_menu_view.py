import tkinter as tk
from tkinter import ttk
from src.views.account_view import AccountView
from src.views.store_view import StoreView
import os
from PIL import Image, ImageTk
# import các view khác nếu cần

class SettingMenuView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.window = tk.Toplevel(parent)
        self.window.title("Cài đặt hệ thống")
        self.window.geometry("320x340")
        self.window.configure(bg="#F5F7FA")
        # Load icon
        def load_icon(name, size=(22, 22)):
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Assets/icon', name))
            try:
                img = Image.open(icon_path).resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except:
                return None
        self.icon_gear = load_icon("gear.png")
        self.icon_user = load_icon("user.png")
        self.icon_store = load_icon("store.png")
        # --- Nhóm Quản lý cài đặt ---
        self.setting_group_expanded = True
        self.frame_setting_group = tk.Frame(self.window, bg="#F5F7FA")
        self.frame_setting_group.pack(fill=tk.X, padx=0, pady=(18, 0))
        def toggle_setting_group(event=None):
            if self.setting_group_expanded:
                self.frame_setting_subs.pack_forget()
                self.setting_group_expanded = False
                btn_setting_group.configure(text="  Quản lý cài đặt ▼", compound=tk.LEFT, image=self.icon_gear)
            else:
                self.frame_setting_subs.pack(after=btn_setting_group, fill=tk.X, padx=0, pady=0)
                self.setting_group_expanded = True
                btn_setting_group.configure(text="  Quản lý cài đặt ▲", compound=tk.LEFT, image=self.icon_gear)
        btn_setting_group = tk.Button(
            self.frame_setting_group, text="  Quản lý cài đặt ▲", compound=tk.LEFT, image=self.icon_gear,
            anchor="w", padx=12, font=("Segoe UI", 11, "bold"), fg="#232a36",
            relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0, cursor="hand2"
        )
        btn_setting_group.bind("<Button-1>", toggle_setting_group)
        btn_setting_group.pack(fill=tk.X, pady=2, padx=8, anchor="w")
        # --- Các nút con ---
        self.frame_setting_subs = tk.Frame(self.frame_setting_group, bg="#F5F7FA")
        # Quản lý tài khoản
        sub_frame1 = tk.Frame(self.frame_setting_subs, bg="#F5F7FA")
        btn_account = tk.Button(sub_frame1, text="  Quản lý tài khoản", compound=tk.LEFT, image=self.icon_user,
            anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
            relief="flat", bg="#F5F7FA", activebackground="#eafaf1", borderwidth=0, cursor="hand2",
            command=self.open_account)
        btn_account.pack(fill=tk.X)
        sub_frame1.pack(fill=tk.X, pady=2, padx=32)
        # Quản lý cửa hàng
        sub_frame2 = tk.Frame(self.frame_setting_subs, bg="#F5F7FA")
        btn_store = tk.Button(sub_frame2, text="  Quản lý cửa hàng", compound=tk.LEFT, image=self.icon_store,
            anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
            relief="flat", bg="#F5F7FA", activebackground="#eafaf1", borderwidth=0, cursor="hand2",
            command=self.open_store)
        btn_store.pack(fill=tk.X)
        sub_frame2.pack(fill=tk.X, pady=2, padx=32)
        self.frame_setting_subs.pack(fill=tk.X, padx=0, pady=0)

    def open_account(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        AccountView(self.window)  # Mở form con với parent là cửa sổ menu cài đặt

    def open_store(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        store_view = StoreView(self.window, self.db_path)
        store_view.pack(fill=tk.BOTH, expand=True) 