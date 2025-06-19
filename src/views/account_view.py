import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core import account

class AccountView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#eef2f6")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_accounts()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Account.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#eef2f6", relief="flat")
        style.configure("Account.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        # Khung danh sách
        frame_list = tk.LabelFrame(self, text='Danh sách tài khoản', font=("Segoe UI", 12, "bold"), bg="#eef2f6", fg="#232a36", bd=0)
        frame_list.pack(fill=tk.BOTH, expand=True, padx=24, pady=(24, 8))
        columns = ('ID', 'Username', 'Tên nhân viên', 'Quyền', 'Trạng thái')
        self.tree = ttk.Treeview(frame_list, columns=columns, show='headings', height=12, style="Account.Treeview")
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Username', width=120, anchor="center")
        self.tree.column('Tên nhân viên', width=180, anchor="w")
        self.tree.column('Quyền', width=320, anchor="w")
        self.tree.column('Trạng thái', width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        # Border bo tròn giả lập
        frame_list.config(highlightbackground="#dde2e6", highlightthickness=2)
        # Thanh cuộn
        scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        # Nút chức năng pastel
        btn_frame = tk.Frame(self, bg="#eef2f6")
        btn_frame.pack(pady=16)
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Tạo tài khoản mới', command=self.show_add_form)
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_edit = tk.Button(btn_frame, text='Sửa', command=self.show_edit_form)
        style_btn(btn_edit, "#f9e7cf", "#f6cba3")
        btn_edit.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=self.delete_selected)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)

    def load_accounts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        accounts = account.get_accounts()
        for acc in accounts:
            self.tree.insert('', tk.END, values=acc)

    def show_add_form(self):
        popup = tk.Toplevel(self)
        popup.title('Tạo tài khoản mới')
        popup.geometry('520x520')
        popup.configure(bg="#eef2f6")
        frm = tk.Frame(popup, bg="#eef2f6")
        frm.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        def style_label(widget):
            widget.configure(bg="#eef2f6", fg="#232a36", font=("Segoe UI", 11, "bold"), anchor="w")
        def style_entry(widget):
            widget.configure(font=("Segoe UI", 12), relief="groove", bd=2, highlightthickness=1, highlightbackground="#dde2e6")
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        # Grid 2 cột cho các trường
        row = 0
        def add_row(label, entry):
            lbl = tk.Label(frm, text=label)
            lbl.grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
            style_label(lbl)
            entry.grid(row=row, column=1, sticky="ew", padx=(0,8), pady=6)
            style_entry(entry)
        frm.grid_columnconfigure(1, weight=1)
        # Tên nhân viên
        name_var = tk.StringVar()
        entry = tk.Entry(frm, textvariable=name_var)
        add_row('Tên nhân viên:', entry)
        row += 1
        # Số điện thoại
        phone_var = tk.StringVar()
        entry = tk.Entry(frm, textvariable=phone_var)
        add_row('Số điện thoại:', entry)
        row += 1
        # Email
        email_var = tk.StringVar()
        entry = tk.Entry(frm, textvariable=email_var)
        add_row('Email:', entry)
        row += 1
        # Giới tính
        gender_var = tk.StringVar()
        combo = ttk.Combobox(frm, textvariable=gender_var, values=['Nam', 'Nữ'], font=("Segoe UI", 12))
        lbl = tk.Label(frm, text='Giới tính:')
        lbl.grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        style_label(lbl)
        combo.grid(row=row, column=1, sticky="ew", padx=(0,8), pady=6)
        row += 1
        # Ngày sinh
        birth_var = tk.StringVar()
        entry = tk.Entry(frm, textvariable=birth_var)
        add_row('Ngày sinh (YYYY-MM-DD):', entry)
        row += 1
        # Quyền
        lbl = tk.Label(frm, text='Chọn quyền (giữ Ctrl để chọn nhiều):')
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", pady=(12,2))
        style_label(lbl)
        row += 1
        roles = account.get_roles()
        role_names = [r[1] for r in roles]
        role_ids = [r[0] for r in roles]
        listbox_roles = tk.Listbox(frm, selectmode=tk.MULTIPLE, height=6, font=("Segoe UI", 12), relief="groove", bd=2, highlightthickness=1, highlightbackground="#dde2e6")
        for name in role_names:
            listbox_roles.insert(tk.END, name)
        listbox_roles.grid(row=row, column=0, columnspan=2, sticky="ew", padx=(0,8), pady=2)
        row += 1
        # Username
        user_var = tk.StringVar()
        entry = tk.Entry(frm, textvariable=user_var)
        add_row('Username:', entry)
        row += 1
        # Password
        pass_var = tk.StringVar()
        entry = tk.Entry(frm, textvariable=pass_var, show='*')
        add_row('Password:', entry)
        row += 1
        # Nút lưu
        btn_save = tk.Button(frm, text='Lưu', command=lambda: on_save())
        style_btn(btn_save, "#eafaf1", "#d1f2eb")
        btn_save.grid(row=row, column=0, columnspan=2, sticky="ew", pady=16, padx=(0,8))
        def on_save():
            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()
            gender = gender_var.get().strip()
            birth = birth_var.get().strip()
            username = user_var.get().strip()
            password = pass_var.get().strip()
            selected = listbox_roles.curselection()
            if not (name and phone and username and password and selected):
                messagebox.showwarning('Thiếu thông tin', 'Vui lòng nhập đầy đủ các trường bắt buộc và chọn ít nhất 1 quyền!')
                return
            role_id_list = [role_ids[i] for i in selected]
            success, msg = account.add_account(name, phone, email, gender, birth, role_id_list, username, password)
            if success:
                messagebox.showinfo('Thành công', msg)
                popup.destroy()
                self.load_accounts()
            else:
                messagebox.showerror('Lỗi', msg)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Chọn tài khoản', 'Vui lòng chọn tài khoản để xóa!')
            return
        item = self.tree.item(selected[0])
        account_id = item['values'][0]
        if messagebox.askyesno('Xác nhận', 'Bạn có chắc chắn muốn xóa tài khoản này?'):
            success, msg = account.delete_account(account_id)
            if success:
                messagebox.showinfo('Thành công', msg)
                self.load_accounts()
            else:
                messagebox.showerror('Lỗi', msg)

    def show_edit_form(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Chọn tài khoản', 'Vui lòng chọn tài khoản để sửa!')
            return
        item = self.tree.item(selected[0])
        account_id = item['values'][0]
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Database/ministore_db.sqlite'))
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT tk.username, nv.ten, nv.sdt, nv.gmail, nv.gioitinh, nv.ngaysinh, tk.trangthai, nv.id
            FROM taikhoan tk JOIN nhanvien nv ON tk.nhanvien_id = nv.id WHERE tk.id = ?
        ''', (account_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            messagebox.showerror('Lỗi', 'Không tìm thấy tài khoản!')
            return
        username, name, phone, email, gender, birth, status, nhanvien_id = row
        cursor.execute('SELECT phanquyen_id FROM nhanvien_phanquyen WHERE nhanvien_id=?', (nhanvien_id,))
        current_roles = [r[0] for r in cursor.fetchall()]
        conn.close()
        popup = tk.Toplevel(self)
        popup.title('Sửa tài khoản')
        popup.geometry('520x520')
        popup.configure(bg="#eef2f6")
        frm = tk.Frame(popup, bg="#eef2f6")
        frm.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        def style_label(widget):
            widget.configure(bg="#eef2f6", fg="#232a36", font=("Segoe UI", 11, "bold"), anchor="w")
        def style_entry(widget):
            widget.configure(font=("Segoe UI", 12), relief="groove", bd=2, highlightthickness=1, highlightbackground="#dde2e6")
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        row = 0
        def add_row(label, entry):
            lbl = tk.Label(frm, text=label)
            lbl.grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
            style_label(lbl)
            entry.grid(row=row, column=1, sticky="ew", padx=(0,8), pady=6)
            style_entry(entry)
        frm.grid_columnconfigure(1, weight=1)
        # Tên nhân viên
        name_var = tk.StringVar(value=name)
        entry = tk.Entry(frm, textvariable=name_var)
        add_row('Tên nhân viên:', entry)
        row += 1
        # Số điện thoại
        phone_var = tk.StringVar(value=phone)
        entry = tk.Entry(frm, textvariable=phone_var)
        add_row('Số điện thoại:', entry)
        row += 1
        # Email
        email_var = tk.StringVar(value=email)
        entry = tk.Entry(frm, textvariable=email_var)
        add_row('Email:', entry)
        row += 1
        # Giới tính
        gender_var = tk.StringVar(value=gender)
        combo = ttk.Combobox(frm, textvariable=gender_var, values=['Nam', 'Nữ'], font=("Segoe UI", 12))
        lbl = tk.Label(frm, text='Giới tính:')
        lbl.grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        style_label(lbl)
        combo.grid(row=row, column=1, sticky="ew", padx=(0,8), pady=6)
        row += 1
        # Ngày sinh
        birth_var = tk.StringVar(value=birth)
        entry = tk.Entry(frm, textvariable=birth_var)
        add_row('Ngày sinh (YYYY-MM-DD):', entry)
        row += 1
        # Quyền
        lbl = tk.Label(frm, text='Chọn quyền (giữ Ctrl để chọn nhiều):')
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", pady=(12,2))
        style_label(lbl)
        row += 1
        roles = account.get_roles()
        role_names = [r[1] for r in roles]
        role_ids = [r[0] for r in roles]
        listbox_roles = tk.Listbox(frm, selectmode=tk.MULTIPLE, height=6, font=("Segoe UI", 12), relief="groove", bd=2, highlightthickness=1, highlightbackground="#dde2e6")
        for i, name_role in enumerate(role_names):
            listbox_roles.insert(tk.END, name_role)
            if role_ids[i] in current_roles:
                listbox_roles.selection_set(i)
        listbox_roles.grid(row=row, column=0, columnspan=2, sticky="ew", padx=(0,8), pady=2)
        row += 1
        # Username
        user_var = tk.StringVar(value=username)
        entry = tk.Entry(frm, textvariable=user_var)
        add_row('Username:', entry)
        row += 1
        # Password
        pass_var = tk.StringVar()
        entry = tk.Entry(frm, textvariable=pass_var, show='*')
        add_row('Password (để trống nếu không đổi):', entry)
        row += 1
        # Nút lưu
        btn_save = tk.Button(frm, text='Lưu', command=lambda: on_save())
        style_btn(btn_save, "#eafaf1", "#d1f2eb")
        btn_save.grid(row=row, column=0, columnspan=2, sticky="ew", pady=16, padx=(0,8))
        def on_save():
            name_ = name_var.get().strip()
            phone_ = phone_var.get().strip()
            email_ = email_var.get().strip()
            gender_ = gender_var.get().strip()
            birth_ = birth_var.get().strip()
            username_ = user_var.get().strip()
            password_ = pass_var.get().strip()
            selected = listbox_roles.curselection()
            if not (name_ and phone_ and username_ and selected):
                messagebox.showwarning('Thiếu thông tin', 'Vui lòng nhập đầy đủ các trường bắt buộc và chọn ít nhất 1 quyền!')
                return
            role_id_list = [role_ids[i] for i in selected]
            success, msg = account.update_account(account_id, name_, phone_, email_, gender_, birth_, role_id_list, username_, password_)
            if success:
                messagebox.showinfo('Thành công', msg)
                popup.destroy()
                self.load_accounts()
            else:
                if 'UNIQUE constraint failed: taikhoan.username' in msg:
                    messagebox.showerror('Lỗi', 'Username đã tồn tại, vui lòng chọn tên khác!')
                else:
                    messagebox.showerror('Lỗi', msg) 