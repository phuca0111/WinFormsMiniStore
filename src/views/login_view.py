import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core import login
from Core.customer import CustomerCore
from views.main_window import MainWindow
from models.account_model import AccountModel

def show_login(root, on_success):
    root.deiconify()  # Hiện cửa sổ khi vẽ form đăng nhập
    root.title("Đăng nhập hệ thống")
    root.geometry("380x340")
    root.configure(bg="#8eb6f9")

    # Khung trắng bo tròn (giả lập)
    frame = tk.Frame(root, bg="white", bd=0, highlightthickness=0)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=320)

    # Tiêu đề
    tk.Label(frame, text="Đăng nhập", font=("Segoe UI", 18, "bold"), bg="white", fg="#232a36").pack(pady=(22, 10))

    # Entry với placeholder
    def make_entry(parent, placeholder, show=None):
        var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=var, font=("Segoe UI", 12), bg="#f5f7fa", fg="#232a36", relief="flat", bd=0, highlightthickness=1, highlightbackground="#dde2e6", highlightcolor="#8eb6f9", show=show)
        entry.pack(fill="x", padx=28, pady=7, ipady=8)
        entry.insert(0, placeholder)
        entry.config(fg="#888")
        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="#232a36", show=show)
        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg="#888", show=None)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry, var
    entry_user, user_var = make_entry(frame, "Enter email / phone")
    entry_pass, pass_var = make_entry(frame, "Password", show="*")

    # Nút đăng nhập
    btn_login = tk.Button(frame, text="Đăng nhập", font=("Segoe UI", 13, "bold"), bg="#ff5e5e", fg="white", activebackground="#ff7b7b", activeforeground="white", bd=0, relief="flat", cursor="hand2")
    btn_login.pack(pady=(18, 8), ipadx=10, ipady=7, fill="x", padx=28)

    # Dòng đăng ký
    bottom_frame = tk.Frame(frame, bg="white")
    bottom_frame.pack(pady=(10, 0), fill="x")
    tk.Label(bottom_frame, text="TK:admin - MK:123456", font=("Segoe UI", 10), bg="white", fg="#888").pack(side="left", padx=(28, 0))
    lbl_register = tk.Label(bottom_frame, text="Đăng ký ngay", font=("Segoe UI", 10, "underline"), bg="white", fg="#1976d2", cursor="hand2")
    lbl_register.pack(side="left", padx=(4, 0))
    # Bind click đăng ký
    lbl_register.bind("<Button-1>", lambda e: messagebox.showinfo("Đăng ký", "Chức năng đăng ký sẽ được bổ sung!"))

    # Xử lý đăng nhập
    def on_login():
        username = user_var.get().strip()
        password = pass_var.get().strip()
        if username == "Enter email / phone": username = ""
        if password == "Password": password = ""
        if not username or not password:
            tk.messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Gọi hàm check_login từ Core.login
        user_info = login.check_login(username, password)
        if user_info:
            on_success(user_info)  # Truyền user_info (tuple) thay vì username, password
        else:
            tk.messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
    btn_login.config(command=on_login)
    entry_user.focus_set()

def start_app(user_info):
    nhanvien_id = user_info[3]
    ten_nhanvien = user_info[1]
    root = tk.Tk()
    app = MainWindow(root, nhanvien_id, ten_nhanvien)
    show_login(root, lambda info: None)  # Chỉ show login nếu cần đăng nhập lại
    root.mainloop()

def main():
    root = tk.Tk()
    def on_success(user_info):
        nhanvien_id = user_info[3]
        ten_nhanvien = user_info[1]
        app = MainWindow(root, nhanvien_id, ten_nhanvien)
    show_login(root, on_success)
    root.mainloop()

if __name__ == "__main__":
    main() 