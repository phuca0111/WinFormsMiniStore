import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import sqlite3


class MainWindow:
    def __init__(self, root, nhanvien_id, ten_nhanvien, db_path=None):
        self.root = root
        self.nhanvien_id = nhanvien_id
        self.ten_nhanvien = ten_nhanvien
        self.db_path = db_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Database/ministore_db.sqlite'))
        store_name = self.get_selected_store_name()
        if store_name:
            hello_text = f"Xin chào, {self.ten_nhanvien}!\nChào mừng bạn đến với cửa hàng: {store_name}"
        else:
            hello_text = f"Xin chào, {self.ten_nhanvien}!"
        self.root.title("Quản lý MiniStore")
        self.root.geometry("1000x700")
        self.label_hello = ttk.Label(self.root, text=hello_text, font=("Arial", 14, "bold"), foreground="blue")
        self.label_hello.pack(pady=10)
        self.permissions = self.get_permissions()
        self.create_menu()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def get_selected_store_name(self):
        try:
            from Core.setting import SettingCore
            from models.store_model import StoreModel
            setting = SettingCore(self.db_path)
            store_id = setting.get_setting("selected_store_id")
            if store_id:
                store_model = StoreModel(self.db_path)
                store = store_model.get_store_by_id(int(store_id))
                if store:
                    return store[1]
        except Exception as e:
            print("Lỗi lấy tên cửa hàng:", e)
        return None

    def get_permissions(self):
        # Lấy danh sách quyền của nhân viên từ database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pq.tenquyen FROM nhanvien_phanquyen npq
            JOIN phanquyen pq ON npq.phanquyen_id = pq.id
            WHERE npq.nhanvien_id = ?
        ''', (self.nhanvien_id,))
        rows = cursor.fetchall()
        conn.close()
        return set(r[0] for r in rows)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Menu', menu=manage_menu)
        # Xóa mục 'Tài khoản' khỏi menu chính
        # if 'Quản lý tài khoản' in self.permissions:
        #     manage_menu.add_command(label='Tài khoản', command=self.open_account)
        if 'Quản lý loại sản phẩm' in self.permissions:
            manage_menu.add_command(label='Loại sản phẩm', command=self.open_category)
        if 'Quản lý khách hàng' in self.permissions:
            manage_menu.add_command(label='Khách hàng', command=self.open_customer)
        if 'Quản lý tồn kho' in self.permissions:
            manage_menu.add_command(label='Tồn kho', command=self.open_inventory)
        if 'Quản lý đơn hàng' in self.permissions:
            manage_menu.add_command(label='Đơn hàng', command=self.open_order)
        if 'Quản lý thanh toán' in self.permissions:
            manage_menu.add_command(label='Thanh toán', command=self.open_payment)
        if 'Quản lý nhà sản xuất' in self.permissions:
            manage_menu.add_command(label='Nhà sản xuất', command=self.open_producer)
        if 'Quản lý biến thể sản phẩm' in self.permissions:
            manage_menu.add_command(label='Biến thể sản phẩm', command=self.open_product_variant)
        if 'Quản lý sản phẩm' in self.permissions:
            manage_menu.add_command(label='Sản phẩm', command=self.open_product)
        manage_menu.add_separator()
        manage_menu.add_command(label='Cài đặt', command=self.open_setting_menu)
        manage_menu.add_command(label='Thoát', command=self.root.quit)
        manage_menu.add_command(label='Đổi tài khoản', command=self.switch_account)

    def open_account(self):
        account_view_path = os.path.join(os.path.dirname(__file__), 'account_view.py')
        subprocess.Popen([sys.executable, account_view_path])

    def open_category(self):
        category_view_path = os.path.join(os.path.dirname(__file__), 'category_view.py')
        subprocess.Popen([sys.executable, category_view_path])

    def open_customer(self):
        customer_view_path = os.path.join(os.path.dirname(__file__), 'customer_view.py')
        subprocess.Popen([sys.executable, customer_view_path])

    def open_inventory(self):
        inventory_view_path = os.path.join(os.path.dirname(__file__), 'inventory_view.py')
        subprocess.Popen([sys.executable, inventory_view_path])

    def open_order(self):
        order_view_path = os.path.join(os.path.dirname(__file__), 'order_view.py')
        subprocess.Popen([sys.executable, order_view_path])

    def open_payment(self):
        import src.views.payment_view as payment_view
        payment_view.main(self.nhanvien_id)

    def open_producer(self):
        producer_view_path = os.path.join(os.path.dirname(__file__), 'producer_view.py')
        subprocess.Popen([sys.executable, producer_view_path])

    def open_product_variant(self):
        product_variant_view_path = os.path.join(os.path.dirname(__file__), 'product_variant_view.py')
        subprocess.Popen([sys.executable, product_variant_view_path])

    def open_product(self):
        product_view_path = os.path.join(os.path.dirname(__file__), 'product_view.py')
        subprocess.Popen([sys.executable, product_view_path])

    def open_store(self):
        """Mở cửa sổ quản lý cửa hàng"""
        from src.views.store_view import StoreView
        StoreView(self.root, self.db_path)

    def open_setting_menu(self):
        from src.views.setting_menu_view import SettingMenuView
        SettingMenuView(self.root, self.db_path)

    def switch_account(self):
        from views.login_view import show_login
        from main import start_app
        self.root.destroy()
        show_login(start_app)

    def calc_change(self, *args):
        cash_str = self.entry_cash.get().replace(',', '').strip()
        print('DEBUG entry_cash.get():', cash_str)
        if not cash_str:
            self.label_change.config(text='Tiền thừa: 0 VND', foreground='blue')
            return
        try:
            cash = float(cash_str)
            change = cash - self.total
            if change < 0:
                self.label_change.config(text=f'Thiếu {abs(change):,.0f} VND', foreground='red')
            else:
                self.label_change.config(text=f'Tiền thừa: {change:,.0f} VND', foreground='blue')
        except Exception:
            self.label_change.config(text='Nhập số hợp lệ!', foreground='red')

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()