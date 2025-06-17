import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import sqlite3

from .base_view import BaseView
from .category_view import CategoryView
from .customer_view import CustomerView
from .inventory_view import InventoryView
from .order_view import OrderView
from .payment_view import PaymentView
from .producer_view import ProducerView
from .product_variant_view import ProductVariantView
from .setting_menu_view import SettingMenuView
from .shelf_menu_view import ShelfMenuView
from .product_view import ProductView
from .shelf_view import ShelfView
from .product_on_shelf_view import ProductOnShelfView

class MainWindow:
    def __init__(self, root, nhanvien_id, ten_nhanvien, db_path=None):
        self.root = root
        self.nhanvien_id = nhanvien_id
        self.ten_nhanvien = ten_nhanvien
        self.db_path = db_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Database/ministore_db.sqlite'))
        store_name = self.get_selected_store_name()
        if store_name:
            hello_text = f"Xin chào, {self.ten_nhanvien}!"
        else:
            hello_text = f"Xin chào, {self.ten_nhanvien}!"
        self.root.title("Hệ thống Quản lý MiniStore")
        self.root.geometry("1200x700")
        
        # Khởi tạo Style
        style = ttk.Style()
        style.configure("LeftMenu.TFrame", background="#3366ff")
        
        # Tạo container chính
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Tạo khung menu bên trái
        self.menu_frame = ttk.Frame(self.main_container, width=250,style="LeftMenu.TFrame")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Tạo khung nội dung
        self.content_frame = ttk.Frame(self.main_container,style="LeftMenu.TFrame")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Thêm nhãn chào mừng
        self.label_hello = ttk.Label(self.menu_frame, text=hello_text, font=("Arial", 12, "bold"), foreground="blue", wraplength=180)
        self.label_hello.pack(pady=10,padx=10)
        
        # Thêm đường phân cách
        ttk.Separator(self.menu_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Khởi tạo BaseView để quản lý nội dung
        self.base_view = BaseView(self.content_frame)
        
        # Lấy quyền và tạo các nút menu
        self.permissions = self.get_permissions()
        self.create_menu_buttons()
        
        # Thêm nút đăng xuất ở cuối menu
        ttk.Separator(self.menu_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Button(self.menu_frame, text="Đăng xuất", command=self.switch_account).pack(pady=5)

    def create_menu_buttons(self):
        menu_items = [
            ("Khách hàng", "Quản lý khách hàng", self.open_customer),
            ("Thanh toán", "Quản lý thanh toán", self.open_payment),
            ("Sản phẩm", "Quản lý sản phẩm", self.open_product),
            ("Loại sản phẩm", "Quản lý loại sản phẩm", self.open_category),
            ("Biến thể sản phẩm", "Quản lý biến thể sản phẩm", self.open_product_variant),
            ("Nhà sản xuất", "Quản lý nhà sản xuất", self.open_producer),
            ("Danh sách đơn hàng", "Quản lý đơn hàng", self.open_order),
            ("Tồn kho", "Quản lý tồn kho", self.open_inventory),
            ("Cài đặt", "Quản lý cài đặt", self.open_setting_menu),
            ("Kệ hàng", "Quản lý kệ hàng", self.open_shelf),
            ("Sản phẩm trên kệ", "Quản lý sản phẩm trên kệ", self.open_product_on_shelf)
        ]
        
        for display_text, permission_name, command in menu_items:
            if permission_name in self.permissions:
                btn = ttk.Button(self.menu_frame, text=display_text, command=command, width=20)
                btn.pack(pady=2)

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

    # def create_menu(self):
    #     menubar = tk.Menu(self.root)
    #     self.root.config(menu=menubar)
    #     manage_menu = tk.Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label='Menu', menu=manage_menu)
    #     # Xóa mục 'Tài khoản' khỏi menu chính
    #     # if 'Quản lý tài khoản' in self.permissions:
    #     #     manage_menu.add_command(label='Tài khoản', command=self.open_account)
    #     if 'Quản lý loại sản phẩm' in self.permissions:
    #         manage_menu.add_command(label='Loại sản phẩm', command=self.open_category)
    #     if 'Quản lý khách hàng' in self.permissions:
    #         manage_menu.add_command(label='Khách hàng', command=self.open_customer)
    #     if 'Quản lý tồn kho' in self.permissions:
    #         manage_menu.add_command(label='Tồn kho', command=self.open_inventory)
    #     if 'Quản lý đơn hàng' in self.permissions:
    #         manage_menu.add_command(label='Đơn hàng', command=self.open_order)
    #     if 'Quản lý thanh toán' in self.permissions:
    #         manage_menu.add_command(label='Thanh toán', command=self.open_payment)
    #     if 'Quản lý nhà sản xuất' in self.permissions:
    #         manage_menu.add_command(label='Nhà sản xuất', command=self.open_producer)
    #     if 'Quản lý biến thể sản phẩm' in self.permissions:
    #         manage_menu.add_command(label='Biến thể sản phẩm', command=self.open_product_variant)
    #     if 'Quản lý sản phẩm' in self.permissions:
    #         manage_menu.add_command(label='Sản phẩm', command=self.open_product)
    #     if 'Quản lý cài đặt' in self.permissions:
    #         manage_menu.add_command(label='Cài đặt', command=self.open_setting_menu)
    #     if 'Quản lý kệ hàng' in self.permissions:
    #         manage_menu.add_command(label='Kệ hàng', command=self.open_shelf)
    #     manage_menu.add_separator()
    #     manage_menu.add_command(label='Thoát', command=self.root.quit)
    #     manage_menu.add_command(label='Đổi tài khoản', command=self.switch_account)

    def open_account(self):
        from .account_view import AccountView
        view = AccountView(self.content_frame, self.db_path)
        self.base_view.add_view("account", view)
        self.base_view.show_view("account")

    def open_category(self):
        if "category" not in self.base_view.views:
            view = CategoryView(self.content_frame, self.db_path)
            self.base_view.add_view("category", view)
        self.base_view.show_view("category")

    def open_customer(self):
        if "customer" not in self.base_view.views:
            view = CustomerView(self.content_frame, self.db_path)
            self.base_view.add_view("customer", view)
        self.base_view.show_view("customer")

    def open_inventory(self):
        if "inventory" not in self.base_view.views:
            view = InventoryView(self.content_frame, self.db_path)
            self.base_view.add_view("inventory", view)
        self.base_view.show_view("inventory")

    def open_order(self):
        if "order" not in self.base_view.views:
            view = OrderView(self.content_frame)
            self.base_view.add_view("order", view)
        self.base_view.show_view("order")

    def open_payment(self):
        if "payment" not in self.base_view.views:
            view = PaymentView(self.content_frame, self.db_path)
            self.base_view.add_view("payment", view)
        self.base_view.show_view("payment")

    def open_producer(self):
        if "producer" not in self.base_view.views:
            view = ProducerView(self.content_frame, self.db_path)
            self.base_view.add_view("producer", view)
        self.base_view.show_view("producer")

    def open_product_variant(self):
        if "product_variant" not in self.base_view.views:
            view = ProductVariantView(self.content_frame, self.db_path)
            self.base_view.add_view("product_variant", view)
        self.base_view.show_view("product_variant")

    def open_product(self):
        if "product" not in self.base_view.views:
            view = ProductView(self.content_frame, self.db_path)
            self.base_view.add_view("product", view)
        self.base_view.show_view("product")

    def open_store(self):
        if "store" not in self.base_view.views:
            from .store_view import StoreView
            view = StoreView(self.content_frame, self.db_path)
            self.base_view.add_view("store", view)
        self.base_view.show_view("store")

    def open_setting_menu(self):
        if "setting" not in self.base_view.views:
            view = SettingMenuView(self.content_frame, self.db_path)
            self.base_view.add_view("setting", view)
        self.base_view.show_view("setting")

    def open_shelf(self):
        view = ShelfView(self.content_frame, self.db_path)
        self.base_view.add_view("shelf", view)
        self.base_view.show_view("shelf")

    def open_product_on_shelf(self):
        view = ProductOnShelfView(self.content_frame, self.db_path)
        self.base_view.add_view("product_on_shelf", view)
        self.base_view.show_view("product_on_shelf")

    def switch_account(self):
        # Đóng cửa sổ hiện tại
        self.root.destroy()
        # Mở lại form đăng nhập
        from views.login_view import show_login
        from main import start_app
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