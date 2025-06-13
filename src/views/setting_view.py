import tkinter as tk
from tkinter import ttk, messagebox
from Core.setting import SettingCore

class SettingView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.core = SettingCore(db_path)
        self.window = tk.Toplevel(parent)
        self.window.title("Cài đặt hệ thống")
        self.window.geometry("400x250")
        
        ttk.Label(self.window, text="Tên thiết lập:").pack(pady=5)
        self.key_var = tk.StringVar()
        ttk.Entry(self.window, textvariable=self.key_var).pack(pady=5)
        
        ttk.Label(self.window, text="Giá trị:").pack(pady=5)
        self.value_var = tk.StringVar()
        ttk.Entry(self.window, textvariable=self.value_var).pack(pady=5)
        
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Lưu", command=self.save_setting).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Xem", command=self.load_setting).pack(side=tk.LEFT, padx=5)

    def save_setting(self):
        key = self.key_var.get().strip()
        value = self.value_var.get().strip()
        if not key:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên thiết lập!")
            return
        self.core.set_setting(key, value)
        messagebox.showinfo("Thành công", "Đã lưu thiết lập!")

    def load_setting(self):
        key = self.key_var.get().strip()
        if not key:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên thiết lập!")
            return
        value = self.core.get_setting(key)
        if value is not None:
            self.value_var.set(value)
        else:
            messagebox.showinfo("Không tìm thấy", "Chưa có thiết lập này!") 