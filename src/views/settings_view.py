import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

class SettingsView:
    def __init__(self, root, nhanvien_id):
        self.root = root
        self.nhanvien_id = nhanvien_id
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'ministore_db.sqlite')
        
        self.root.title("Cài đặt")
        self.root.geometry("800x600")
        
        # Tạo notebook để chứa các tab
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Tab Tài khoản
        self.account_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.account_frame, text='Tài khoản')
        self.setup_account_tab()
        
        # Tab Cửa hàng
        self.store_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.store_frame, text='Cửa hàng')
        self.setup_store_tab()
        
        # Tab Hệ thống
        self.system_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.system_frame, text='Hệ thống')
        self.setup_system_tab()

    def setup_account_tab(self):
        # Frame chứa thông tin tài khoản
        info_frame = ttk.LabelFrame(self.account_frame, text="Thông tin tài khoản")
        info_frame.pack(fill='x', padx=5, pady=5)
        
        # Lấy thông tin tài khoản
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nv.ten, nv.sdt, nv.gmail, nv.gioitinh, nv.ngaysinh
            FROM nhanvien nv
            WHERE nv.id = ?
        ''', (self.nhanvien_id,))
        info = cursor.fetchone()
        conn.close()
        
        # Hiển thị thông tin
        ttk.Label(info_frame, text=f"Họ tên: {info[0]}").pack(anchor='w', padx=5, pady=2)
        ttk.Label(info_frame, text=f"Số điện thoại: {info[1]}").pack(anchor='w', padx=5, pady=2)
        ttk.Label(info_frame, text=f"Email: {info[2]}").pack(anchor='w', padx=5, pady=2)
        ttk.Label(info_frame, text=f"Giới tính: {info[3]}").pack(anchor='w', padx=5, pady=2)
        ttk.Label(info_frame, text=f"Ngày sinh: {info[4]}").pack(anchor='w', padx=5, pady=2)

    def setup_store_tab(self):
        # Frame chứa thông tin cửa hàng
        store_frame = ttk.LabelFrame(self.store_frame, text="Thông tin cửa hàng")
        store_frame.pack(fill='x', padx=5, pady=5)
        
        # Lấy thông tin cửa hàng
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM thongtincuahang LIMIT 1')
        store = cursor.fetchone()
        conn.close()
        
        if store:
            ttk.Label(store_frame, text=f"Tên cửa hàng: {store[1]}").pack(anchor='w', padx=5, pady=2)
            ttk.Label(store_frame, text=f"Địa chỉ: {store[2]}").pack(anchor='w', padx=5, pady=2)
            ttk.Label(store_frame, text=f"Số điện thoại: {store[3]}").pack(anchor='w', padx=5, pady=2)
            ttk.Label(store_frame, text=f"Mã số thuế: {store[4]}").pack(anchor='w', padx=5, pady=2)
            ttk.Label(store_frame, text=f"Website: {store[5]}").pack(anchor='w', padx=5, pady=2)
            ttk.Label(store_frame, text=f"Ghi chú: {store[6]}").pack(anchor='w', padx=5, pady=2)
        else:
            ttk.Label(store_frame, text="Chưa có thông tin cửa hàng").pack(anchor='w', padx=5, pady=2)

    def setup_system_tab(self):
        # Frame chứa thông tin hệ thống
        system_frame = ttk.LabelFrame(self.system_frame, text="Thông tin hệ thống")
        system_frame.pack(fill='x', padx=5, pady=5)
        
        # Hiển thị thông tin hệ thống
        ttk.Label(system_frame, text="Phiên bản: 1.0.0").pack(anchor='w', padx=5, pady=2)
        ttk.Label(system_frame, text="Nhà phát triển: MiniStore Team").pack(anchor='w', padx=5, pady=2)
        ttk.Label(system_frame, text="© 2024 MiniStore. All rights reserved.").pack(anchor='w', padx=5, pady=2) 