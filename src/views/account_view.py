import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core import account

class AccountView:
    def __init__(self, root):
        self.root = root
        self.root.title('Quản lý tài khoản & phân quyền')
        self.root.geometry('800x500')
        self.create_widgets()
        self.load_accounts()

    def create_widgets(self):
        # Frame danh sách tài khoản
        frame_list = ttk.LabelFrame(self.root, text='Danh sách tài khoản')
        frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        columns = ('ID', 'Username', 'Tên nhân viên', 'Quyền', 'Trạng thái')
        self.tree = ttk.Treeview(frame_list, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Nút thêm, sửa, xóa tài khoản
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        btn_add = ttk.Button(btn_frame, text='Tạo tài khoản mới', command=self.show_add_form)
        btn_add.pack(side=tk.LEFT, padx=5)
        btn_edit = ttk.Button(btn_frame, text='Sửa', command=self.show_edit_form)
        btn_edit.pack(side=tk.LEFT, padx=5)
        btn_delete = ttk.Button(btn_frame, text='Xóa', command=self.delete_selected)
        btn_delete.pack(side=tk.LEFT, padx=5)

    def load_accounts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        accounts = account.get_accounts()
        for acc in accounts:
            self.tree.insert('', tk.END, values=acc)

    def show_add_form(self):
        popup = tk.Toplevel(self.root)
        popup.title('Tạo tài khoản mới')
        popup.geometry('400x600')

        # Thông tin nhân viên
        ttk.Label(popup, text='Tên nhân viên:').pack(pady=2)
        name_var = tk.StringVar()
        ttk.Entry(popup, textvariable=name_var).pack(pady=2)

        ttk.Label(popup, text='Số điện thoại:').pack(pady=2)
        phone_var = tk.StringVar()
        ttk.Entry(popup, textvariable=phone_var).pack(pady=2)

        ttk.Label(popup, text='Email:').pack(pady=2)
        email_var = tk.StringVar()
        ttk.Entry(popup, textvariable=email_var).pack(pady=2)

        ttk.Label(popup, text='Giới tính:').pack(pady=2)
        gender_var = tk.StringVar()
        ttk.Combobox(popup, textvariable=gender_var, values=['Nam', 'Nữ']).pack(pady=2)

        ttk.Label(popup, text='Ngày sinh (YYYY-MM-DD):').pack(pady=2)
        birth_var = tk.StringVar()
        ttk.Entry(popup, textvariable=birth_var).pack(pady=2)

        # Chọn nhiều quyền
        ttk.Label(popup, text='Chọn quyền (giữ Ctrl để chọn nhiều):').pack(pady=2)
        roles = account.get_roles()
        role_names = [r[1] for r in roles]
        role_ids = [r[0] for r in roles]
        listbox_roles = tk.Listbox(popup, selectmode=tk.MULTIPLE, height=8)
        for name in role_names:
            listbox_roles.insert(tk.END, name)
        listbox_roles.pack(pady=2, fill=tk.X, padx=10)

        # Thông tin tài khoản
        ttk.Label(popup, text='Username:').pack(pady=2)
        user_var = tk.StringVar()
        ttk.Entry(popup, textvariable=user_var).pack(pady=2)

        ttk.Label(popup, text='Password:').pack(pady=2)
        pass_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pass_var, show='*').pack(pady=2)

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
        ttk.Button(popup, text='Lưu', command=on_save).pack(pady=10)

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
        # Lấy lại thông tin chi tiết từ database
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
        # Lấy quyền hiện tại
        cursor.execute('SELECT phanquyen_id FROM nhanvien_phanquyen WHERE nhanvien_id=?', (nhanvien_id,))
        current_roles = [r[0] for r in cursor.fetchall()]
        conn.close()

        popup = tk.Toplevel(self.root)
        popup.title('Sửa tài khoản')
        popup.geometry('400x600')

        ttk.Label(popup, text='Tên nhân viên:').pack(pady=2)
        name_var = tk.StringVar(value=name)
        ttk.Entry(popup, textvariable=name_var).pack(pady=2)

        ttk.Label(popup, text='Số điện thoại:').pack(pady=2)
        phone_var = tk.StringVar(value=phone)
        ttk.Entry(popup, textvariable=phone_var).pack(pady=2)

        ttk.Label(popup, text='Email:').pack(pady=2)
        email_var = tk.StringVar(value=email)
        ttk.Entry(popup, textvariable=email_var).pack(pady=2)

        ttk.Label(popup, text='Giới tính:').pack(pady=2)
        gender_var = tk.StringVar(value=gender)
        ttk.Combobox(popup, textvariable=gender_var, values=['Nam', 'Nữ']).pack(pady=2)

        ttk.Label(popup, text='Ngày sinh (YYYY-MM-DD):').pack(pady=2)
        birth_var = tk.StringVar(value=birth)
        ttk.Entry(popup, textvariable=birth_var).pack(pady=2)

        # Chọn nhiều quyền
        ttk.Label(popup, text='Chọn quyền (giữ Ctrl để chọn nhiều):').pack(pady=2)
        roles = account.get_roles()
        role_names = [r[1] for r in roles]
        role_ids = [r[0] for r in roles]
        listbox_roles = tk.Listbox(popup, selectmode=tk.MULTIPLE, height=8)
        for i, name in enumerate(role_names):
            listbox_roles.insert(tk.END, name)
            if role_ids[i] in current_roles:
                listbox_roles.selection_set(i)
        listbox_roles.pack(pady=2, fill=tk.X, padx=10)

        # Thông tin tài khoản
        ttk.Label(popup, text='Username:').pack(pady=2)
        user_var = tk.StringVar(value=username)
        ttk.Entry(popup, textvariable=user_var).pack(pady=2)

        ttk.Label(popup, text='Password (để trống nếu không đổi):').pack(pady=2)
        pass_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pass_var, show='*').pack(pady=2)

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
                messagebox.showerror('Lỗi', msg)
        ttk.Button(popup, text='Lưu', command=on_save).pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = AccountView(root)
    root.mainloop() 