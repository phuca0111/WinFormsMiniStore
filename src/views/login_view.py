import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core import login
from Core.customer import CustomerCore

def show_login(on_success):
    login_win = tk.Tk()
    login_win.title('Đăng nhập hệ thống')
    login_win.geometry('350x200')
    login_win.resizable(False, False)

    ttk.Label(login_win, text='Tên đăng nhập:').pack(pady=(20,5))
    username_var = tk.StringVar()
    entry_user = ttk.Entry(login_win, textvariable=username_var)
    entry_user.pack(pady=5)

    ttk.Label(login_win, text='Mật khẩu:').pack(pady=5)
    password_var = tk.StringVar()
    entry_pass = ttk.Entry(login_win, textvariable=password_var, show='*')
    entry_pass.pack(pady=5)

    def do_login():
        username = username_var.get().strip()
        password = password_var.get().strip()
        if not username or not password:
            messagebox.showwarning('Thiếu thông tin', 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!')
            return
        user_info = login.check_login(username, password)
        if user_info:
            login_win.destroy()
            on_success(user_info)
        else:
            messagebox.showerror('Đăng nhập thất bại', 'Sai tên đăng nhập hoặc mật khẩu!')

    btn_login = ttk.Button(login_win, text='Đăng nhập', command=do_login)
    btn_login.pack(pady=15)
    entry_user.focus_set()
    login_win.mainloop() 