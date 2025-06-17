import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import sqlite3

# Thêm đường dẫn gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.views.supplier_view import SupplierView
from src.views.supplier_product_view import SupplierProductView
from src.views.huongdan_view import HuongDanView
from src.views.thongke_loilo_view import ThongKeTongHopView
from src.views.canhbao_hansudung_view import CanhBaoHanSuDungView
from src.views.inventory_batch_view import InventoryBatchView
from src.views.phieu_tieu_huy_report_view import PhieuTieuHuyReportView


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
        # Thêm nút Hướng dẫn ngoài giao diện
        self.button_huongdan = ttk.Button(self.root, text="Hướng dẫn", command=self.open_huongdan)
        self.button_huongdan.pack(anchor="ne", padx=10, pady=5)
        # Thêm nút Thống kê lời lỗ dưới chữ Menu
        # self.button_loilo = ttk.Button(self.root, text="Thống kê lời lỗ", command=self.open_loilo)
        # self.button_loilo.pack(anchor="nw", padx=10, pady=(35, 5))
        # Thêm nút Cảnh báo hết hạn
        # self.button_canhbao = ttk.Button(self.root, text="Cảnh báo hết hạn", command=self.open_canhbao)
        # self.button_canhbao.pack(anchor="nw", padx=10, pady=(5, 5))
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
        # Thêm mục Thống kê nếu có quyền
        if 'Xem thống kê' in self.permissions or 'Quản lý thống kê' in self.permissions:
            menubar.add_command(label='Thống kê', command=self.open_thongke_tonghop)
        if 'Quản lý loại sản phẩm' in self.permissions:
            manage_menu.add_command(label='Loại sản phẩm', command=self.open_category)
        if 'Quản lý khách hàng' in self.permissions:
            manage_menu.add_command(label='Khách hàng', command=self.open_customer)
        if 'Quản lý tồn kho' in self.permissions:
            manage_menu.add_command(label='Tồn kho', command=self.open_inventory)
            if 'Xem tồn kho chi tiết theo lô' in self.permissions or 'Quản lý tồn kho' in self.permissions:
                manage_menu.add_command(label='Tồn kho chi tiết theo lô', command=self.open_inventory_batch)
            if 'Xem báo cáo tiêu hủy' in self.permissions or 'Quản lý tồn kho' in self.permissions:
                manage_menu.add_command(label='Báo cáo tiêu hủy', command=self.open_phieu_tieu_huy_report)
            if 'Xem lịch sử nhập hàng' in self.permissions:
                manage_menu.add_command(label='Lịch sử nhập hàng', command=self.open_import_log)
            if 'Xem lịch sử chỉnh sửa/xóa' in self.permissions:
                manage_menu.add_command(label='Lịch sử chỉnh sửa/xóa', command=self.open_edit_delete_log)
        if 'Quản lý đơn hàng' in self.permissions:
            manage_menu.add_command(label='Đơn hàng', command=self.open_order)
            if 'Xem lịch sử bán hàng' in self.permissions:
                manage_menu.add_command(label='Lịch sử bán hàng', command=self.open_log_ban_hang)
        if 'Quản lý thanh toán' in self.permissions:
            manage_menu.add_command(label='Thanh toán', command=self.open_payment)
        if 'Quản lý nhà sản xuất' in self.permissions:
            manage_menu.add_command(label='Nhà sản xuất', command=self.open_producer)
        if 'Quản lý biến thể sản phẩm' in self.permissions:
            manage_menu.add_command(label='Biến thể sản phẩm', command=self.open_product_variant)
        if 'Quản lý sản phẩm' in self.permissions:
            manage_menu.add_command(label='Sản phẩm', command=self.open_product)
        if 'Quản lý nhà cung cấp' in self.permissions:
            manage_menu.add_command(label='Nhà cung cấp', command=self.open_supplier)
        if 'Quản lý nhập hàng' in self.permissions:
            manage_menu.add_command(label='Nhập hàng', command=self.open_supplier_product)
        if 'Quản lý cài đặt' in self.permissions:
            manage_menu.add_command(label='Cài đặt', command=self.open_setting_menu)
        if 'Quản lý kệ hàng' in self.permissions:
            manage_menu.add_command(label='Kệ hàng', command=self.open_shelf)
        manage_menu.add_separator()
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

    def open_supplier(self):
        """Mở cửa sổ quản lý nhà cung cấp"""
        # Xóa các widget cũ trong main_frame
        self.clear_main_frame()
        # Tạo và hiển thị giao diện nhà cung cấp
        SupplierView(self.main_frame).pack(fill=tk.BOTH, expand=True)

    def open_store(self):
        """Mở cửa sổ quản lý cửa hàng"""
        from src.views.store_view import StoreView
        StoreView(self.root, self.db_path)

    def open_setting_menu(self):
        from views.setting_menu_view import SettingMenuView
        SettingMenuView(self.root, self.db_path)

    def open_shelf(self):
        from views.shelf_menu_view import ShelfMenuView
        ShelfMenuView(self.root, self.db_path)

    def open_supplier_product(self):
        self.clear_main_frame()
        SupplierProductView(self.main_frame)

    def open_huongdan(self):
        self.clear_main_frame()
        HuongDanView(self.main_frame)

    def open_loilo(self):
        self.clear_main_frame()
        ThongKeTongHopView(self.main_frame, self.db_path)

    def open_canhbao(self):
        self.clear_main_frame()
        CanhBaoHanSuDungView(self.main_frame)

    def open_inventory_batch(self):
        self.clear_main_frame()
        InventoryBatchView(self.main_frame)

    def open_phieu_tieu_huy_report(self):
        self.clear_main_frame()
        PhieuTieuHuyReportView(self.main_frame)

    def open_thongke_tonghop(self):
        self.clear_main_frame()
        ThongKeTongHopView(self.main_frame, self.db_path)

    def open_import_log(self):
        from src.views.import_log_view import ImportLogView
        self.clear_main_frame()
        ImportLogView(self.main_frame)

    def open_edit_delete_log(self):
        from src.views.edit_delete_log_view import EditDeleteLogView
        self.clear_main_frame()
        EditDeleteLogView(self.main_frame)

    def open_log_ban_hang(self):
        from views.log_ban_hang_view import LogBanHangView
        self.clear_main_frame()
        LogBanHangView(self.main_frame)

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

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()