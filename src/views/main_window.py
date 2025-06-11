import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys


class MainWindow:
    def __init__(self, root, user_info=None):
        self.root = root
<<<<<<< HEAD
        self.user_info = user_info
=======
>>>>>>> phuc
        self.root.title("Quản lý MiniStore")
        self.root.geometry("1000x700")
        self.create_menu()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

<<<<<<< HEAD
        # Hiển thị tên nhân viên
        if self.user_info:
            label = ttk.Label(self.root, text=f"Xin chào, {self.user_info[1]}!", font=("Arial", 13, "bold"), foreground="blue")
            label.pack(side=tk.TOP, pady=5)

        # Khởi tạo các biến trạng thái và khung submenu
        self.product_submenu_frame = None
        self.product_expanded = False
        self.product_button = None

        self.order_submenu_frame = None
        self.order_expanded = False
        self.order_button = None

        self.shipping_submenu_frame = None
        self.shipping_expanded = False
        self.shipping_button = None

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        roles = self.user_info[2] if self.user_info else []
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Quản lý', menu=manage_menu)
        if 'Quản lý khách hàng' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Khách hàng', command=self.open_customer)
        if 'Quản lý thanh toán' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Thanh toán', command=self.open_payment)
        if 'Quản lý sản phẩm' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Sản phẩm', command=self.open_product)
        if 'Quản lý loại sản phẩm' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Loại sản phẩm', command=self.open_category)
        if 'Quản lý biến thể sản phẩm' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Biến thể sản phẩm', command=self.open_product_variant)
        if 'Quản lý nhà sản xuất' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Nhà sản xuất', command=self.open_producer)
        if 'Quản lý đơn hàng' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Đơn hàng', command=self.open_order)
        if 'Quản lý tồn kho' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Tồn kho', command=self.open_inventory)
        if 'Quản lý tài khoản' in roles or 'Quản lý toàn bộ' in roles or 'Quản trị hệ thống' in roles:
            manage_menu.add_command(label='Tài khoản', command=self.open_account)
        manage_menu.add_separator()
        manage_menu.add_command(label='Thoát', command=self.root.quit)

=======
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Menu', menu=manage_menu)
        manage_menu.add_command(label='Tài khoản', command=self.open_account)
        manage_menu.add_command(label='Loại sản phẩm', command=self.open_category)
        manage_menu.add_command(label='Khách hàng', command=self.open_customer)
        manage_menu.add_command(label='Tồn kho', command=self.open_inventory)
        manage_menu.add_command(label='Đơn hàng', command=self.open_order)
        manage_menu.add_command(label='Thanh toán', command=self.open_payment)
        manage_menu.add_command(label='Nhà sản xuất', command=self.open_producer)
        manage_menu.add_command(label='Biến thể sản phẩm', command=self.open_product_variant)
        manage_menu.add_command(label='Sản phẩm', command=self.open_product)
        manage_menu.add_separator()
        manage_menu.add_command(label='Thoát', command=self.root.quit)

    def open_account(self):
        account_view_path = os.path.join(os.path.dirname(__file__), 'account_view.py')
        subprocess.Popen([sys.executable, account_view_path])

    def open_category(self):
        category_view_path = os.path.join(os.path.dirname(__file__), 'category_view.py')
        subprocess.Popen([sys.executable, category_view_path])

>>>>>>> phuc
    def open_customer(self):
        customer_view_path = os.path.join(os.path.dirname(__file__), 'customer_view.py')
        subprocess.Popen([sys.executable, customer_view_path])

<<<<<<< HEAD
    def open_payment(self):
        payment_view_path = os.path.join(os.path.dirname(__file__), 'payment_view.py')
        subprocess.Popen([sys.executable, payment_view_path])

    def open_product(self):
        product_view_path = os.path.join(os.path.dirname(__file__), 'product_view.py')
        subprocess.Popen([sys.executable, product_view_path])

    def open_category(self):
        category_view_path = os.path.join(os.path.dirname(__file__), 'category_view.py')
        subprocess.Popen([sys.executable, category_view_path])

    def open_product_variant(self):
        product_variant_view_path = os.path.join(os.path.dirname(__file__), 'product_variant_view.py')
        subprocess.Popen([sys.executable, product_variant_view_path])

    def open_producer(self):
        producer_view_path = os.path.join(os.path.dirname(__file__), 'producer_view.py')
        subprocess.Popen([sys.executable, producer_view_path])

    def open_order(self):
        order_view_path = os.path.join(os.path.dirname(__file__), 'order_view.py')
        subprocess.Popen([sys.executable, order_view_path])

=======
>>>>>>> phuc
    def open_inventory(self):
        inventory_view_path = os.path.join(os.path.dirname(__file__), 'inventory_view.py')
        subprocess.Popen([sys.executable, inventory_view_path])

<<<<<<< HEAD
    def open_account(self):
        account_view_path = os.path.join(os.path.dirname(__file__), 'account_view.py')
        subprocess.Popen([sys.executable, account_view_path])

    def create_menu_items(self):
        # Tạo các mục menu chính
        self.add_menu_item("Tổng quan", self.on_tong_quan_click)
        self.add_menu_item("Bán hàng", self.on_ban_hang_click)

        # Mục "Đơn hàng" với submenu
        self.order_button = self.create_button("Đơn hàng", self.toggle_order_menu, has_arrow=True)
        self.order_button.pack(fill="x", padx=10, pady=5)

        # Mục "Vận chuyển" với submenu
        self.shipping_button = self.create_button("Vận chuyển", self.toggle_shipping_menu, has_arrow=True)
        self.shipping_button.pack(fill="x", padx=10, pady=5)

        self.add_menu_item("Khách hàng", self.on_khach_hang_click)

        # Mục "Sản phẩm" với submenu
        self.product_button = self.create_button("Sản phẩm", self.toggle_product_menu, has_arrow=True)
        self.product_button.pack(fill="x", padx=10, pady=5)

    def add_menu_item(self, text, command, has_arrow=False):
        button = self.create_button(text, command, has_arrow)
        button.pack(fill="x", padx=10, pady=5)

    def add_submenu_item(self, parent_frame, text, command, new_tag=False, has_arrow=False):
        # Tạo mục con và thêm vào parent_frame
        button_frame = tk.Frame(parent_frame, bg="#34495e")
        button_frame.bind("<Button-1>", lambda e: command())

        text_label = tk.Label(button_frame, text=text, fg="white", bg="#34495e",
                              font=("Arial", 10), anchor="w")
        text_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        text_label.bind("<Button-1>", lambda e: command())

        if has_arrow:
            arrow_label = tk.Label(button_frame, text=">", fg="white",
                                   bg="#34495e", font=("Arial", 10, "bold"))
            arrow_label.pack(side="right", padx=(0, 5))
            arrow_label.bind("<Button-1>", lambda e: command())

        # Hover effects
        button_frame.bind("<Enter>", lambda e: button_frame.config(bg="#4a637d"))
        button_frame.bind("<Leave>", lambda e: button_frame.config(bg="#34495e"))
        text_label.bind("<Enter>", lambda e: text_label.config(bg="#4a637d"))
        text_label.bind("<Leave>", lambda e: text_label.config(bg="#34495e"))
        if has_arrow:
            arrow_label.bind("<Enter>", lambda e: arrow_label.config(bg="#4a637d"))
            arrow_label.bind("<Leave>", lambda e: arrow_label.config(bg="#34495e"))

        button_frame.pack(fill="x", padx=15, pady=3)

        if new_tag:
            new_label = tk.Label(button_frame, text="NEW", bg="#f39c12", fg="white", font=("Arial", 8, "bold"),
                                 relief="flat",
                                 padx=3, pady=1)
            new_label.pack(side="right", padx=(0, 5))

        return button_frame

    def create_button(self, text, command, has_arrow=False, is_submenu=False):
        button_frame = tk.Frame(self.main_frame, bg="#2c3e50" if not is_submenu else "#34495e")
        button_frame.bind("<Button-1>", lambda e: command())

        text_label = tk.Label(button_frame, text=text, fg="white", bg="#2c3e50" if not is_submenu else "#34495e",
                              font=("Arial", 10), anchor="w")
        text_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        text_label.bind("<Button-1>", lambda e: command())

        if has_arrow:
            arrow_label = tk.Label(button_frame, text=">", fg="white",
                                   bg="#2c3e50" if not is_submenu else "#34495e", font=("Arial", 10, "bold"))
            arrow_label.pack(side="right", padx=(0, 5))
            arrow_label.bind("<Button-1>", lambda e: command())

        button_frame.bind("<Enter>", lambda e: button_frame.config(bg="#34495e" if not is_submenu else "#4a637d"))
        button_frame.bind("<Leave>", lambda e: button_frame.config(bg="#2c3e50" if not is_submenu else "#34495e"))
        text_label.bind("<Enter>", lambda e: text_label.config(bg="#34495e" if not is_submenu else "#4a637d"))
        text_label.bind("<Leave>", lambda e: text_label.config(bg="#2c3e50" if not is_submenu else "#34495e"))
        if has_arrow:
            arrow_label.bind("<Enter>", lambda e: arrow_label.config(bg="#34495e" if not is_submenu else "#4a637d"))
            arrow_label.bind("<Leave>", lambda e: arrow_label.config(bg="#2c3e50" if not is_submenu else "#34495e"))

        return button_frame

    def update_arrow(self, button, expanded):
        """Cập nhật mũi tên của button"""
        for child in button.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") in [">", "V"]:
                child.config(text="V" if expanded else ">")
                break

    def toggle_product_menu(self):
        if not self.product_expanded:
            # Tạo khung con nếu chưa tồn tại
            if self.product_submenu_frame is None:
                self.product_submenu_frame = tk.Frame(self.main_frame, bg="#34495e")
                self.add_submenu_item(self.product_submenu_frame, "Danh sách sản phẩm",
                                      self.on_danh_sach_san_pham_click)
                self.add_submenu_item(self.product_submenu_frame, "Quản lý kho", self.on_quan_ly_kho_click,
                                      has_arrow=True)
                self.add_submenu_item(self.product_submenu_frame, "Nhập hàng", self.on_nhap_hang_click)
                self.add_submenu_item(self.product_submenu_frame, "Kiểm hàng Beta", self.on_kiem_hang_click,
                                      new_tag=True)
                self.add_submenu_item(self.product_submenu_frame, "Chuyển hàng", self.on_chuyen_hang_click)
                self.add_submenu_item(self.product_submenu_frame, "Nhà cung cấp", self.on_nha_cung_cap_click)
                self.add_submenu_item(self.product_submenu_frame, "Điều chỉnh giá vốn",
                                      self.on_dieu_chinh_gia_von_click)

            self.product_submenu_frame.pack(fill="x", after=self.product_button)
            self.product_expanded = True
        else:
            # Ẩn khung con
            if self.product_submenu_frame:
                self.product_submenu_frame.pack_forget()
            self.product_expanded = False

        self.update_arrow(self.product_button, self.product_expanded)

    def toggle_order_menu(self):
        if not self.order_expanded:
            # Tạo khung con nếu chưa tồn tại
            if self.order_submenu_frame is None:
                self.order_submenu_frame = tk.Frame(self.main_frame, bg="#34495e")
                self.add_submenu_item(self.order_submenu_frame, "Danh sách đơn hàng", self.on_danh_sach_don_hang_click)
                self.add_submenu_item(self.order_submenu_frame, "Đơn hàng chờ xử lý", self.on_don_hang_cho_xu_ly_click)
                self.add_submenu_item(self.order_submenu_frame, "Đơn hàng đã hủy", self.on_don_hang_da_huy_click)
                self.add_submenu_item(self.order_submenu_frame, "Báo cáo đơn hàng", self.on_bao_cao_don_hang_click)

            self.order_submenu_frame.pack(fill="x", after=self.order_button)
            self.order_expanded = True
        else:
            # Ẩn khung con
            if self.order_submenu_frame:
                self.order_submenu_frame.pack_forget()
            self.order_expanded = False

        self.update_arrow(self.order_button, self.order_expanded)

    def toggle_shipping_menu(self):
        if not self.shipping_expanded:
            # Tạo khung con nếu chưa tồn tại
            if self.shipping_submenu_frame is None:
                self.shipping_submenu_frame = tk.Frame(self.main_frame, bg="#34495e")
                self.add_submenu_item(self.shipping_submenu_frame, "Quản lý vận chuyển",
                                      self.on_quan_ly_van_chuyen_click)
                self.add_submenu_item(self.shipping_submenu_frame, "Đơn vị vận chuyển", self.on_don_vi_van_chuyen_click)
                self.add_submenu_item(self.shipping_submenu_frame, "Theo dõi đơn hàng", self.on_theo_doi_don_hang_click)
                self.add_submenu_item(self.shipping_submenu_frame, "Cài đặt phí ship", self.on_cai_dat_phi_ship_click)

            self.shipping_submenu_frame.pack(fill="x", after=self.shipping_button)
            self.shipping_expanded = True
        else:
            # Ẩn khung con
            if self.shipping_submenu_frame:
                self.shipping_submenu_frame.pack_forget()
            self.shipping_expanded = False

        self.update_arrow(self.shipping_button, self.shipping_expanded)

    # --- Các hàm xử lý khi click vào từng mục menu chính ---
    def on_tong_quan_click(self):
        print("Click: Tổng quan")

    def on_ban_hang_click(self):
        print("Click: Bán hàng")

    def on_khach_hang_click(self):
        print("Click: Khách hàng")

    # --- Các hàm xử lý cho menu Sản phẩm ---
    def on_danh_sach_san_pham_click(self):
        print("Click: Danh sách sản phẩm")

    def on_quan_ly_kho_click(self):
        print("Click: Quản lý kho")

    def on_nhap_hang_click(self):
        print("Click: Nhập hàng")

    def on_kiem_hang_click(self):
        print("Click: Kiểm hàng Beta")

    def on_chuyen_hang_click(self):
        print("Click: Chuyển hàng")

    def on_nha_cung_cap_click(self):
        print("Click: Nhà cung cấp")

    def on_dieu_chinh_gia_von_click(self):
        print("Click: Điều chỉnh giá vốn")

    # --- Các hàm xử lý cho menu Đơn hàng ---
    def on_danh_sach_don_hang_click(self):
        print("Click: Danh sách đơn hàng")

    def on_don_hang_cho_xu_ly_click(self):
        print("Click: Đơn hàng chờ xử lý")

    def on_don_hang_da_huy_click(self):
        print("Click: Đơn hàng đã hủy")

    def on_bao_cao_don_hang_click(self):
        print("Click: Báo cáo đơn hàng")

    # --- Các hàm xử lý cho menu Vận chuyển ---
    def on_quan_ly_van_chuyen_click(self):
        print("Click: Quản lý vận chuyển")

    def on_don_vi_van_chuyen_click(self):
        print("Click: Đơn vị vận chuyển")

    def on_theo_doi_don_hang_click(self):
        print("Click: Theo dõi đơn hàng")

    def on_cai_dat_phi_ship_click(self):
        print("Click: Cài đặt phí ship")

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from views.login_view import show_login

    def start_main():
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
    show_login(start_main)
=======
    def open_order(self):
        order_view_path = os.path.join(os.path.dirname(__file__), 'order_view.py')
        subprocess.Popen([sys.executable, order_view_path])

    def open_payment(self):
        payment_view_path = os.path.join(os.path.dirname(__file__), 'payment_view.py')
        subprocess.Popen([sys.executable, payment_view_path])

    def open_producer(self):
        producer_view_path = os.path.join(os.path.dirname(__file__), 'producer_view.py')
        subprocess.Popen([sys.executable, producer_view_path])

    def open_product_variant(self):
        product_variant_view_path = os.path.join(os.path.dirname(__file__), 'product_variant_view.py')
        subprocess.Popen([sys.executable, product_variant_view_path])

    def open_product(self):
        product_view_path = os.path.join(os.path.dirname(__file__), 'product_view.py')
        subprocess.Popen([sys.executable, product_view_path])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
>>>>>>> phuc
