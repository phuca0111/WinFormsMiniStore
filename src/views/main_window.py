import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import sqlite3
from PIL import Image, ImageTk  # Thêm PIL để xử lý icon
from datetime import datetime

# Thêm đường dẫn gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core import login
from Core.customer import CustomerCore
from models.account_model import AccountModel
from src.views.supplier_view import SupplierView
from src.views.supplier_product_view import SupplierProductView
from src.views.huongdan_view import HuongDanView
from src.views.thongke_loilo_view import ThongKeTongHopView
from src.views.canhbao_hansudung_view import CanhBaoHanSuDungView
from src.views.inventory_batch_view import InventoryBatchView
from src.views.phieu_tieu_huy_report_view import PhieuTieuHuyReportView


class MainWindow(tk.Frame):
    def __init__(self, root, nhanvien_id, ten_nhanvien, db_path=None):
        super().__init__(root)
        self.root = root
        self.nhanvien_id = nhanvien_id
        self.ten_nhanvien = ten_nhanvien
        self.db_path = db_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Database/ministore_db.sqlite'))
        self.icon_images = {}  # Dictionary để lưu trữ các icon đã load
        self.permissions = self.get_permissions()
        self.pack(fill=tk.BOTH, expand=True)
        self.create_layout()

    def create_layout(self):
        # Topbar
        self.topbar = tk.Frame(self, bg="#232a36", height=70)
        self.topbar.pack(side=tk.TOP, fill=tk.X)
        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), '../../Assets/logo/logo.png')
        try:
            logo_img = Image.open(logo_path).resize((48, 48), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.topbar, image=self.logo_tk, bg="#232a36")
            logo_label.pack(side=tk.LEFT, padx=18, pady=(0, 10))
        except Exception as e:
            logo_label = tk.Label(self.topbar, text="🏪", bg="#232a36", fg="white", font=("Arial", 24, "bold"))
            logo_label.pack(side=tk.LEFT, padx=18, pady=(0, 10))
        # Tên cửa hàng
        store_name = self.get_selected_store_name() or "(Chưa chọn cửa hàng)"
        store_label = tk.Label(self.topbar, text=f"Cửa hàng: {store_name}", bg="#232a36", fg="white", font=("Segoe UI", 12, "bold"), anchor="w")
        store_label.pack(side=tk.LEFT, padx=(0, 18), pady=(0, 10))
        # Thông tin nhân viên/ngày
        now = datetime.now().strftime("%d/%m/%Y")
        info_text = f"Nhân viên: {self.ten_nhanvien}   |   Ngày: {now}"
        info_label = tk.Label(self.topbar, text=info_text, bg="#232a36", fg="white", font=("Segoe UI", 12, "bold"))
        info_label.pack(side=tk.RIGHT, padx=18, pady=(0, 10))

        # Main layout: sidebar + main content
        self.body = tk.Frame(self, bg="#F5F7FA")
        self.body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Sidebar
        self.sidebar = tk.Frame(self.body, bg="#F5F7FA", width=258)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(0)
        # Tăng kích thước tab Notebook và đặt theme clam trước khi tạo Notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#F5F7FA", borderwidth=0)
        style.configure("TNotebook.Tab", 
                       padding=[16, 8],
                       font=("Segoe UI", 12, "bold"),
                       background="#F5F7FA",
                       foreground="#fff",
                       borderwidth=0)
        style.map("TNotebook.Tab",
                 background=[("selected", "#fff"), ("!selected", "#F5F7FA")],
                 foreground=[("selected", "#222"), ("!selected", "#555")])

        # Main content: dùng Notebook để quản lý tab
        self.notebook = ttk.Notebook(self.body)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.tabs = {}
        self.create_sidebar_buttons()

        # --- Thêm nút đóng tab bên phải vùng tab ---
        close_img = Image.open(os.path.join(os.path.dirname(__file__), '../../Assets/icon/close.png')).resize((16, 16))
        self.close_icon = ImageTk.PhotoImage(close_img)

        def close_current_tab():
            if self.notebook.tabs():
                current = self.notebook.index(self.notebook.select())
                self.notebook.forget(current)

        self.btn_close_tab = tk.Button(self.body, image=self.close_icon, command=close_current_tab, bd=0, relief="flat", cursor="hand2", bg="#f5f5f5", activebackground="#e0e0e0")
        self.btn_close_tab.place(x=270, y=8)  # Điều chỉnh x, y cho phù hợp với vị trí tab

        # Tooltip cho nút X và vùng tab
        def create_tooltip(widget, text):
            tooltip = tk.Toplevel(widget)
            tooltip.withdraw()
            tooltip.overrideredirect(True)
            label = tk.Label(tooltip, text=text, bg="#232a36", fg="#fff", font=("Segoe UI", 10), padx=8, pady=4, borderwidth=1, relief="solid")
            label.pack()
            def enter(event):
                x = widget.winfo_rootx() + 20
                y = widget.winfo_rooty() + 20
                tooltip.geometry(f"+{x}+{y}")
                tooltip.deiconify()
            def leave(event):
                tooltip.withdraw()
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
        create_tooltip(self.btn_close_tab, "Ấn vào X bên góc phải để Đóng tab hiện tại")
        create_tooltip(self.notebook, "Ấn vào X bên góc phải để Đóng tab hiện tại")

        # Tự động cập nhật vị trí nút khi resize
        def update_close_btn_pos(event=None):
            # Lấy vị trí notebook
            sidebar_width = self.sidebar.winfo_width()
            tab_area_width = self.notebook.winfo_width()
            # Đặt nút sát vùng tab, cách phải 10px
            self.btn_close_tab.place(x=sidebar_width + tab_area_width - 40, y=8)
        self.notebook.bind("<Configure>", update_close_btn_pos)
        self.root.bind("<Configure>", update_close_btn_pos)
        update_close_btn_pos()

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

    def load_icon(self, icon_name, size=(20, 20)):
        if not icon_name:  # Nếu không có tên icon, trả về None
            return None
            
        # Nếu icon đã được load trước đó, trả về icon đó
        if icon_name in self.icon_images:
            return self.icon_images[icon_name]
            
        # Lấy đường dẫn tuyệt đối đến thư mục gốc của dự án
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        icon_path = os.path.join(project_root, 'Assets', 'icon', icon_name)
        
        try:
            if not os.path.exists(icon_path):  # Kiểm tra file có tồn tại không
                print(f"Icon không tồn tại: {icon_path}")
                return None
                
            img = Image.open(icon_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.icon_images[icon_name] = tk_img  # Lưu reference để tránh bị garbage collect
            return tk_img
        except Exception as e:
            print(f"Lỗi load icon {icon_name}: {e}")
            return None

    def create_button(self, parent, text, icon_name=None, command=None, **kwargs):
        """Tạo nút với icon (nếu có) và giữ reference cho icon"""
        icon_img = self.load_icon(icon_name) if icon_name else None
        btn = tk.Button(parent, text=text, compound=tk.LEFT if icon_img else None, **kwargs)
        if icon_img:
            btn.configure(image=icon_img)
            btn.image = icon_img  # Giữ reference cho icon
        if command:
            btn.configure(command=command)
        return btn

    def create_sidebar_buttons(self):
        # Danh sách view (trừ đơn hàng)
        sidebar_items = [
            ("Bán hàng", "cart.png", self.open_payment, "Quản lý thanh toán"),
        ]
        # --- Nhóm Quản lý sản phẩm ---
        product_subs = []
        if "Quản lý sản phẩm" in self.permissions:
            product_subs.append(("Sản phẩm", "product.png", self.open_product))
        if "Quản lý loại sản phẩm" in self.permissions:
            product_subs.append(("Loại sản phẩm", "categories.png", self.open_category))
        if "Quản lý biến thể sản phẩm" in self.permissions:
            product_subs.append(("Biến thể sản phẩm", "dairy-products.png", self.open_product_variant))
        if "Quản lý nhà sản xuất" in self.permissions:
            product_subs.append(("Nhà sản xuất", "manufacture.png", self.open_producer))
        if product_subs:
            self.product_group_expanded = False
            frame_product_group = tk.Frame(self.sidebar, bg="#F5F7FA")
            for text, icon, command in product_subs:
                sub_frame = tk.Frame(frame_product_group, bg="#F5F7FA")
                icon_img = self.load_icon(icon)
                btn = tk.Button(sub_frame, text=text, compound=tk.LEFT if icon_img else None,
                    anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
                    relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0,
                    command=command)
                if icon_img:
                    btn.configure(image=icon_img)
                    btn.image = icon_img  # Giữ reference cho icon
                btn.pack(fill=tk.X)
                sub_frame.pack(fill=tk.X, pady=2, padx=32)
            def toggle_product_group(event=None):
                if self.product_group_expanded:
                    frame_product_group.pack_forget()
                    self.product_group_expanded = False
                    icon_img = self.load_icon("product-development.png")
                    btn_product_group.configure(text="Quản lý sản phẩm ▼", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_product_group.configure(image=icon_img)
                        btn_product_group.image = icon_img  # Giữ reference cho icon
                else:
                    frame_product_group.pack(after=btn_product_group, fill=tk.X, padx=0, pady=0)
                    self.product_group_expanded = True
                    icon_img = self.load_icon("product-development.png")
                    btn_product_group.configure(text="Quản lý sản phẩm ▲", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_product_group.configure(image=icon_img)
                        btn_product_group.image = icon_img  # Giữ reference cho icon
                self.sidebar.update_idletasks()
            icon_img = self.load_icon("product-development.png")
            btn_product_group = tk.Button(
                self.sidebar, text="Quản lý sản phẩm ▼", compound=tk.LEFT if icon_img else None,
                anchor="w", padx=18, font=("Segoe UI", 11, "bold"), fg="#232a36",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
            )
            if icon_img:
                btn_product_group.configure(image=icon_img)
                btn_product_group.image = icon_img  # Giữ reference cho icon
            btn_product_group.bind("<Button-1>", toggle_product_group)
            btn_product_group.pack(fill=tk.X, pady=4, padx=8, anchor="w")
        # --- Nhóm Quản lý cung ứng ---
        supply_subs = []
        if "Quản lý nhà cung cấp" in self.permissions:
            supply_subs.append(("Nhà cung cấp", "supplier.png", self.open_supplier))
        if "Quản lý nhập hàng" in self.permissions:
            supply_subs.append(("Nhập hàng", "importation.png", self.open_supplier_product))
        if supply_subs:
            self.supply_group_expanded = False
            frame_supply_group = tk.Frame(self.sidebar, bg="#F5F7FA")
            for text, icon, command in supply_subs:
                sub_frame = tk.Frame(frame_supply_group, bg="#F5F7FA")
                btn = self.create_button(sub_frame, text=text, icon_name=icon, command=command,
                    anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
                    relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0)
                btn.pack(fill=tk.X)
                sub_frame.pack(fill=tk.X, pady=2, padx=32)
            def toggle_supply_group(event=None):
                if self.supply_group_expanded:
                    frame_supply_group.pack_forget()
                    self.supply_group_expanded = False
                    icon_img = self.load_icon("wholesaler.png")
                    btn_supply_group.configure(text="Quản lý cung ứng ▼", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_supply_group.configure(image=icon_img)
                        btn_supply_group.image = icon_img  # Giữ reference cho icon
                else:
                    frame_supply_group.pack(after=btn_supply_group, fill=tk.X, padx=0, pady=0)
                    self.supply_group_expanded = True
                    icon_img = self.load_icon("wholesaler.png")
                    btn_supply_group.configure(text="Quản lý cung ứng ▲", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_supply_group.configure(image=icon_img)
                        btn_supply_group.image = icon_img  # Giữ reference cho icon
                self.sidebar.update_idletasks()
            icon_img = self.load_icon("wholesaler.png")
            btn_supply_group = tk.Button(
                self.sidebar, text="Quản lý cung ứng ▼", compound=tk.LEFT if icon_img else None,
                anchor="w", padx=18, font=("Segoe UI", 11, "bold"), fg="#232a36",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
            )
            if icon_img:
                btn_supply_group.configure(image=icon_img)
                btn_supply_group.image = icon_img  # Giữ reference cho icon
            btn_supply_group.bind("<Button-1>", toggle_supply_group)
            btn_supply_group.pack(fill=tk.X, pady=4, padx=8, anchor="w")
        # --- Nhóm Quản lý kho ---
        inventory_subs = []
        if "Quản lý tồn kho" in self.permissions:
            inventory_subs.append(("Tồn kho", "warehouse_2.png", self.open_inventory))
        if "Xem tồn kho chi tiết theo lô" in self.permissions:
            inventory_subs.append(("Tồn kho chi tiết theo lô", "warehouse_1.png", self.open_inventory_batch))
        if inventory_subs:
            self.inventory_group_expanded = False
            frame_inventory_group = tk.Frame(self.sidebar, bg="#F5F7FA")
            for text, icon, command in inventory_subs:
                sub_frame = tk.Frame(frame_inventory_group, bg="#F5F7FA")
                btn = self.create_button(sub_frame, text=text, icon_name=icon, command=command,
                    anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
                    relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0)
                btn.pack(fill=tk.X)
                sub_frame.pack(fill=tk.X, pady=2, padx=32)
            def toggle_inventory_group(event=None):
                if self.inventory_group_expanded:
                    frame_inventory_group.pack_forget()
                    self.inventory_group_expanded = False
                    icon_img = self.load_icon("warehouse.png")
                    btn_inventory_group.configure(text="Quản lý kho ▼", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_inventory_group.configure(image=icon_img)
                        btn_inventory_group.image = icon_img  # Giữ reference cho icon
                else:
                    frame_inventory_group.pack(after=btn_inventory_group, fill=tk.X, padx=0, pady=0)
                    self.inventory_group_expanded = True
                    icon_img = self.load_icon("warehouse.png")
                    btn_inventory_group.configure(text="Quản lý kho ▲", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_inventory_group.configure(image=icon_img)
                        btn_inventory_group.image = icon_img  # Giữ reference cho icon
                self.sidebar.update_idletasks()
            icon_img = self.load_icon("warehouse.png")
            btn_inventory_group = tk.Button(
                self.sidebar, text="Quản lý kho ▼", compound=tk.LEFT if icon_img else None,
                anchor="w", padx=18, font=("Segoe UI", 11, "bold"), fg="#232a36",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
            )
            if icon_img:
                btn_inventory_group.configure(image=icon_img)
                btn_inventory_group.image = icon_img  # Giữ reference cho icon
            btn_inventory_group.bind("<Button-1>", toggle_inventory_group)
            btn_inventory_group.pack(fill=tk.X, pady=4, padx=8, anchor="w")
        # --- Nhóm Quản lý nhật ký ---
        log_subs = []
        if "Xem lịch sử nhập hàng" in self.permissions:
            log_subs.append(("Lịch sử nhập hàng", "clock.png", self.open_import_log))
        if "Xem lịch sử chỉnh sửa/xóa" in self.permissions:
            log_subs.append(("Lịch sử chỉnh sửa/xóa", "clock.png", self.open_edit_delete_log))
        if "Xem lịch sử bán hàng" in self.permissions:
            log_subs.append(("Lịch sử giao dịch", "clock.png", self.open_log_ban_hang))
        if log_subs:
            self.log_group_expanded = False
            frame_log_group = tk.Frame(self.sidebar, bg="#F5F7FA")
            for text, icon, command in log_subs:
                sub_frame = tk.Frame(frame_log_group, bg="#F5F7FA")
                btn = self.create_button(sub_frame, text=text, icon_name=icon, command=command,
                    anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
                    relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0)
                btn.pack(fill=tk.X)
                sub_frame.pack(fill=tk.X, pady=2, padx=32)
            def toggle_log_group(event=None):
                if self.log_group_expanded:
                    frame_log_group.pack_forget()
                    self.log_group_expanded = False
                    icon_img = self.load_icon("history.png")
                    btn_log_group.configure(text="Quản lý nhật ký ▼", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_log_group.configure(image=icon_img)
                        btn_log_group.image = icon_img  # Giữ reference cho icon
                else:
                    frame_log_group.pack(after=btn_log_group, fill=tk.X, padx=0, pady=0)
                    self.log_group_expanded = True
                    icon_img = self.load_icon("history.png")
                    btn_log_group.configure(text="Quản lý nhật ký ▲", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_log_group.configure(image=icon_img)
                        btn_log_group.image = icon_img  # Giữ reference cho icon
                self.sidebar.update_idletasks()
            icon_img = self.load_icon("history.png")
            btn_log_group = tk.Button(
                self.sidebar, text="Quản lý nhật ký ▼", compound=tk.LEFT if icon_img else None,
                anchor="w", padx=18, font=("Segoe UI", 11, "bold"), fg="#232a36",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
            )
            if icon_img:
                btn_log_group.configure(image=icon_img)
                btn_log_group.image = icon_img  # Giữ reference cho icon
            btn_log_group.bind("<Button-1>", toggle_log_group)
            btn_log_group.pack(fill=tk.X, pady=4, padx=8, anchor="w")
        # --- Nhóm Quản lý cài đặt ---
        if "Quản lý cài đặt" in self.permissions:
            setting_subs = [
                ("Quản lý tài khoản", "user.png", self.open_account),
                ("Quản lý cửa hàng", "store.png", self.open_store),
            ]
            self.setting_group_expanded = False
            frame_setting_group = tk.Frame(self.sidebar, bg="#F5F7FA")
            for text, icon, command in setting_subs:
                sub_frame = tk.Frame(frame_setting_group, bg="#F5F7FA")
                btn = self.create_button(sub_frame, text=text, icon_name=icon, command=command,
                    anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
                    relief="flat", bg="#F5F7FA", activebackground="#eafaf1", borderwidth=0)
                btn.pack(fill=tk.X)
                sub_frame.pack(fill=tk.X, pady=2, padx=32)
            def toggle_setting_group(event=None):
                if self.setting_group_expanded:
                    frame_setting_group.pack_forget()
                    self.setting_group_expanded = False
                    icon_img = self.load_icon("gear.png")
                    btn_setting_group.configure(text="Quản lý cài đặt ▼", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_setting_group.configure(image=icon_img)
                        btn_setting_group.image = icon_img
                else:
                    frame_setting_group.pack(after=btn_setting_group, fill=tk.X, padx=0, pady=0)
                    self.setting_group_expanded = True
                    icon_img = self.load_icon("gear.png")
                    btn_setting_group.configure(text="Quản lý cài đặt ▲", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_setting_group.configure(image=icon_img)
                        btn_setting_group.image = icon_img
                self.sidebar.update_idletasks()
            icon_img = self.load_icon("gear.png")
            btn_setting_group = tk.Button(
                self.sidebar, text="Quản lý cài đặt ▼", compound=tk.LEFT if icon_img else None,
                anchor="w", padx=18, font=("Segoe UI", 11, "bold"), fg="#232a36",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
            )
            if icon_img:
                btn_setting_group.configure(image=icon_img)
                btn_setting_group.image = icon_img
            btn_setting_group.bind("<Button-1>", toggle_setting_group)
            btn_setting_group.pack(fill=tk.X, pady=4, padx=8, anchor="w")
        # --- Nhóm Kệ hàng ---
        if "Quản lý kệ hàng" in self.permissions:
            shelf_subs = [
                ("Quản lý kệ", "shelves.png", self.open_shelf),
                ("Sản phẩm trên kệ", "product-development.png", self.open_product_on_shelf),
            ]
            self.shelf_group_expanded = False
            frame_shelf_group = tk.Frame(self.sidebar, bg="#F5F7FA")
            for text, icon, command in shelf_subs:
                sub_frame = tk.Frame(frame_shelf_group, bg="#F5F7FA")
                btn = self.create_button(sub_frame, text=text, icon_name=icon, command=command,
                    anchor="w", padx=10, font=("Segoe UI", 11), fg="#232a36",
                    relief="flat", bg="#F5F7FA", activebackground="#eafaf1", borderwidth=0)
                btn.pack(fill=tk.X)
                sub_frame.pack(fill=tk.X, pady=2, padx=32)
            def toggle_shelf_group(event=None):
                if self.shelf_group_expanded:
                    frame_shelf_group.pack_forget()
                    self.shelf_group_expanded = False
                    icon_img = self.load_icon("shelves.png")
                    btn_shelf_group.configure(text="Kệ hàng ▼", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_shelf_group.configure(image=icon_img)
                        btn_shelf_group.image = icon_img
                else:
                    frame_shelf_group.pack(after=btn_shelf_group, fill=tk.X, padx=0, pady=0)
                    self.shelf_group_expanded = True
                    icon_img = self.load_icon("shelves.png")
                    btn_shelf_group.configure(text="Kệ hàng ▲", compound=tk.LEFT if icon_img else None)
                    if icon_img:
                        btn_shelf_group.configure(image=icon_img)
                        btn_shelf_group.image = icon_img
                self.sidebar.update_idletasks()
            icon_img = self.load_icon("shelves.png")
            btn_shelf_group = tk.Button(
                self.sidebar, text="Kệ hàng ▼", compound=tk.LEFT if icon_img else None,
                anchor="w", padx=18, font=("Segoe UI", 11, "bold"), fg="#232a36",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
            )
            if icon_img:
                btn_shelf_group.configure(image=icon_img)
                btn_shelf_group.image = icon_img
            btn_shelf_group.bind("<Button-1>", toggle_shelf_group)
            btn_shelf_group.pack(fill=tk.X, pady=4, padx=8, anchor="w")
        # --- Các chức năng còn lại ---
        sidebar_items = [item for item in sidebar_items if item[0] != "Kệ hàng"]
        sidebar_items += [
            ("Báo cáo tiêu hủy", "tomato.png", self.open_phieu_tieu_huy_report, "Xem báo cáo tiêu hủy"),
            ("Khách hàng", "people.png", self.open_customer, "Quản lý khách hàng"),
            ("Thống kê", "trend.png", self.open_thongke_tonghop, "Xem thống kê"),
        ]
        for text, icon, command, required_permission in sidebar_items:
            if required_permission and required_permission not in self.permissions:
                continue
            btn = self.create_button(
                self.sidebar, text=text, icon_name=icon, command=command, anchor="w", padx=18, font=("Segoe UI", 11), fg="#232a36",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
            )
            btn.pack(fill=tk.X, pady=4, padx=8, anchor="w")
        # Thêm nút Đổi tài khoản
        btn_switch = tk.Button(
            self.sidebar, text="Đổi tài khoản", compound=tk.LEFT, command=self.switch_account, anchor="w",
            padx=18, font=("Segoe UI", 11), fg="#c0392b",
            relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
        )
        btn_switch.pack(fill=tk.X, pady=(20, 4), padx=8, anchor="w")
        # Thêm nút Thoát
        btn_exit = tk.Button(
            self.sidebar, text="Thoát", compound=tk.LEFT, command=self.root.quit, anchor="w",
            padx=18, font=("Segoe UI", 11), fg="#c0392b",
            relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0
        )
        btn_exit.pack(fill=tk.X, pady=(0, 8), padx=8, anchor="w")

    def open_account(self):
        from src.views.account_view import AccountView
        self.open_tab("Quản lý tài khoản", AccountView)

    def open_tab(self, tab_name, view_class, *args, **kwargs):
        # Nếu tab đã mở, chuyển sang tab đó
        if tab_name in self.tabs:
            frame = self.tabs[tab_name]["frame"]
            # Kiểm tra frame còn thuộc notebook không
            if str(frame) in self.notebook.tabs():
                self.notebook.select(frame)
                return
            else:
                # Nếu frame không còn thuộc notebook (đã bị đóng), xóa khỏi self.tabs
                del self.tabs[tab_name]
        # Tạo frame mới cho tab
        frame = tk.Frame(self.notebook, bg="#F5F7FA")
        view = view_class(frame, *args, **kwargs)
        if isinstance(view, tk.Widget):
            view.pack(fill=tk.BOTH, expand=True)
            self.notebook.add(frame, text=tab_name)
            self.tabs[tab_name] = {"frame": frame}
            self.notebook.select(frame)
        else:
            return

    def open_customer(self):
        from src.views.customer_view import CustomerView
        self.open_tab("Khách hàng", CustomerView, self.db_path)

    def open_product(self):
        from src.views.product_view import ProductView
        self.open_tab("Sản phẩm", ProductView)

    def open_category(self):
        from src.views.category_view import CategoryView
        self.open_tab("Loại sản phẩm", CategoryView)

    def open_producer(self):
        from src.views.producer_view import ProducerView
        self.open_tab("Nhà sản xuất", ProducerView)

    def open_inventory(self):
        from src.views.inventory_view import InventoryView
        self.open_tab("Tồn kho", InventoryView)

    def open_inventory_batch(self):
        from src.views.inventory_batch_view import InventoryBatchView
        self.open_tab("Tồn kho chi tiết theo lô", InventoryBatchView)

    def open_supplier(self):
        from src.views.supplier_view import SupplierView
        self.open_tab("Nhà cung cấp", SupplierView)

    def open_supplier_product(self):
        from src.views.supplier_product_view import SupplierProductView
        self.open_tab("Nhập hàng", SupplierProductView)
        # Sau khi mở tab, gọi load_variants nếu có
        tab = self.tabs.get("Nhập hàng")
        if tab:
            frame = tab["frame"]
            for child in frame.winfo_children():
                if isinstance(child, SupplierProductView):
                    child.load_variants()
                    break

    def open_payment(self):
        from src.views.payment_view import PaymentView
        self.open_tab("Bán hàng", PaymentView, self.nhanvien_id, self)

    def open_edit_delete_log(self):
        from src.views.edit_delete_log_view import EditDeleteLogView
        self.open_tab("Lịch sử chỉnh sửa/xóa", EditDeleteLogView)

    def open_import_log(self):
        from src.views.import_log_view import ImportLogView
        self.open_tab("Lịch sử nhập hàng", ImportLogView)

    def open_log_ban_hang(self):
        from src.views.log_ban_hang_view import LogBanHangView
        self.open_tab("Lịch sử giao dịch", LogBanHangView)

    def open_setting_menu(self):
        from src.views.setting_menu_view import SettingMenuView
        SettingMenuView(self.root, self.db_path)  # Không mở trong tab, chỉ mở cửa sổ mới

    def open_phieu_tieu_huy_report(self):
        from src.views.phieu_tieu_huy_report_view import PhieuTieuHuyReportView
        self.open_tab("Báo cáo tiêu hủy", PhieuTieuHuyReportView, self.db_path)

    def open_thongke_tonghop(self):
        from src.views.thongke_loilo_view import ThongKeTongHopView
        self.open_tab("Thống kê", ThongKeTongHopView, self.db_path)

    def open_huongdan(self):
        from src.views.huongdan_view import HuongDanView
        self.open_tab("Hướng dẫn", HuongDanView, self.db_path)

    def open_loilo(self):
        from src.views.thongke_loilo_view import ThongKeTongHopView
        self.open_tab("Thống kê", ThongKeTongHopView, self.db_path)

    def open_canhbao(self):
        from src.views.canhbao_hansudung_view import CanhBaoHanSuDungView
        self.open_tab("Cảnh báo hạn sử dụng", CanhBaoHanSuDungView, self.db_path)

    def open_tong_ton_kho(self):
        from src.views.tong_ton_kho_view import TongTonKhoView
        self.open_tab("Tổng tồn kho", TongTonKhoView, self.open_inventory, self.open_inventory_batch)

    def switch_account(self):
        # Đóng cửa sổ hiện tại
        self.root.destroy()
        # Mở lại form đăng nhập với root mới
        import tkinter as tk
        from views.login_view import show_login
        from main import start_app
        new_root = tk.Tk()
        show_login(new_root, on_success=start_app)

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

    def toggle_tong_ton_kho(self):
        if self.tong_ton_kho_expanded:
            for btn in self.tong_ton_kho_sub_buttons:
                btn.destroy()
            self.tong_ton_kho_sub_buttons = []
            self.tong_ton_kho_expanded = False
        else:
            btn1 = tk.Button(
                self.sidebar, text='   Tồn kho', anchor="w",
                padx=20, width=28, height=2, font=("Segoe UI", 10), fg="#5a6a7a",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0,
                command=self.open_inventory
            )
            btn1.pack(after=self.sidebar.winfo_children()[self.get_tong_ton_kho_btn_index()], fill=tk.X, pady=2, padx=20, anchor="w")
            btn2 = tk.Button(
                self.sidebar, text='   Tồn kho chi tiết theo lô', anchor="w",
                padx=20, width=28, height=2, font=("Segoe UI", 10), fg="#5a6a7a",
                relief="flat", bg="#F5F7FA", activebackground="#e0e0e0", borderwidth=0,
                command=self.open_inventory_batch
            )
            btn2.pack(after=btn1, fill=tk.X, pady=2, padx=20, anchor="w")
            self.tong_ton_kho_sub_buttons = [btn1, btn2]
            self.tong_ton_kho_expanded = True

    def get_tong_ton_kho_btn_index(self):
        # Tìm vị trí nút Tổng tồn kho trong sidebar để chèn các nút con ngay sau nó
        for i, widget in enumerate(self.sidebar.winfo_children()):
            if isinstance(widget, tk.Button) and widget.cget('text') == 'Tổng tồn kho':
                return i
        return 0

    def open_dashboard(self):
        self.clear_main_frame()
        from src.views.product_view import ProductView
        ProductView(self.main_frame)

    def open_product_variant(self):
        from src.views.product_variant_view import ProductVariantView
        self.open_tab("Biến thể sản phẩm", ProductVariantView)

    def open_store(self):
        from src.views.store_view import StoreView
        self.open_tab("Quản lý cửa hàng", StoreView, self.db_path)

    def open_product_on_shelf(self):
        from src.views.product_on_shelf_view import ProductOnShelfView
        self.open_tab("Sản phẩm trên kệ", ProductOnShelfView, self.db_path)

    def open_shelf(self):
        from src.views.shelf_view import ShelfView
        self.open_tab("Quản lý kệ", ShelfView, self.db_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root, 1, "Admin")
    root.mainloop()