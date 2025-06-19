import sys
import os
import subprocess
import webbrowser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.barcode_scanner import scan_barcode
from Core import payment
from Core.setting import SettingCore
from models.product_variant_model import ProductVariant
from PIL import Image, ImageTk
from Core.payment import CartManager

class CashPopup:
    def __init__(self, parent, total):
        self.total = float(str(total).replace(',', ''))
        self.result = {'ok': False}
        self.tien_khach_dua = 0
        self.tien_thoi_lai = 0
        self.popup = tk.Toplevel(parent)
        self.popup.title('Tiền khách đưa')
        self.popup.geometry('300x150')
        ttk.Label(self.popup, text=f'Tổng tiền: {self.total:,.0f} VND').pack(pady=5)
        self.entry_cash = tk.Entry(self.popup, font=("Arial", 12))
        self.entry_cash.pack(pady=5)
        self.label_change = ttk.Label(self.popup, text='', font=("Arial", 11, "bold"), foreground='blue')
        self.label_change.pack(pady=5)
        self.entry_cash.focus_set()
        self.entry_cash.bind('<KeyRelease>', lambda e: self.calc_change())
        self.calc_change()
        ttk.Button(self.popup, text='OK', command=self.on_ok).pack(pady=10)
        self.popup.bind('<Return>', lambda e: self.on_ok())
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
    def on_ok(self):
        self.entry_cash.update()
        self.popup.focus_set()
        cash_str = self.entry_cash.get().replace(',', '').strip()
        if not cash_str:
            self.label_change.config(text='Vui lòng nhập số tiền khách đưa!', foreground='red')
            messagebox.showerror('Lỗi', 'Vui lòng nhập số tiền khách đưa!')
            return
        try:
            cash = float(cash_str)
            if cash < self.total:
                self.label_change.config(text='Tiền khách đưa không đủ!', foreground='red')
                messagebox.showerror('Lỗi', 'Tiền khách đưa không được thấp hơn tổng tiền hóa đơn!')
                return
            self.tien_khach_dua = cash
            self.tien_thoi_lai = cash - self.total
            self.result['ok'] = True
            self.popup.destroy()
        except Exception:
            self.label_change.config(text='Nhập số hợp lệ!', foreground='red')
            messagebox.showerror('Lỗi', 'Nhập số hợp lệ!')

class PaymentView(tk.Frame):
    def __init__(self, parent, nhanvien_id, main_window=None, cart_manager=None):
        super().__init__(parent)
        self.nhanvien_id = nhanvien_id
        self.main_window = main_window
        self.cart_manager = cart_manager if cart_manager else CartManager()
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#f5f7fa")
        self.create_layout()
        self.load_products()
        self.reload_cart()
        self.set_status("")
        self.hold_cart_count = 0
        self.hold_carts = []

    def create_layout(self):
        # Đặt font mặc định cho toàn bộ giao diện
        self.option_add("*Font", "Arial 12")
        self.option_add("*Foreground", "#222")
        bg_color = "#f5f7fa"
        border_color = "#DADADA"
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading",
            background="#EEF2F6",  # Màu header mới
            foreground="#232a36",
            font=("Segoe UI", 13, "bold"),
            borderwidth=0,
            relief="flat"
        )
        style.configure("Custom.Treeview",
            font=("Arial", 12),
            rowheight=32,
            background="#fff",
            fieldbackground="#fff",
            borderwidth=0
        )
        style.configure("Custom.TLabelframe", background="#FFFFFF", bordercolor=border_color, borderwidth=0, relief="flat")
        style.configure("Custom.TLabelframe.Label", background="#FFFFFF", foreground="#333", font=("Arial", 11, "bold"))
        style.configure("Custom.TFrame", background=bg_color)
        style.configure("TLabel", foreground="#222")
        style.configure("TEntry", foreground="#222")

        # Chia 2 cột
        left = ttk.Frame(self, style="Custom.TFrame")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right = ttk.Frame(self, style="Custom.TFrame")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- LEFT: Barcode + Sản phẩm ---
        barcode_frame = tk.Frame(left, bg="#FFFFFF")
        barcode_frame.pack(fill=tk.X, pady=5)
        barcode_title = tk.Label(barcode_frame, text="Quét mã vạch / Tìm kiếm", font=("Arial", 11, "bold"), fg="#333", bg="#FFFFFF", anchor="w")
        barcode_title.pack(fill=tk.X, padx=2, pady=(0, 6))
        entry_barcode = tk.Entry(barcode_frame, font=("Arial", 18), fg="#222", bg="#FFFFFF")
        entry_barcode.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_barcode = entry_barcode
        btn_scan = tk.Button(barcode_frame, text="Quét mã", width=10, font=("Arial", 13), command=self.on_scan, fg="#222", bg="#f8f8f8", bd=1, relief="solid")
        btn_scan.pack(side=tk.LEFT, padx=5)

        # Danh sách sản phẩm
        product_frame = tk.Frame(left, bg="#FFFFFF")
        product_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        product_title = tk.Label(product_frame, text="Danh sách sản phẩm", font=("Arial", 11, "bold"), fg="#333", bg="#FFFFFF", anchor="w")
        product_title.pack(fill=tk.X, padx=2, pady=(0, 6))
        self.tree_products = ttk.Treeview(product_frame, columns=("Tên", "Giá"), show="headings", height=12, style="Custom.Treeview")
        self.tree_products.heading("Tên", text="Tên sản phẩm")
        self.tree_products.heading("Giá", text="Giá bán")
        self.tree_products.column("Tên", width=200)
        self.tree_products.column("Giá", width=100, anchor="e")
        self.tree_products.pack(fill=tk.BOTH, expand=True)
        # Thêm sự kiện double click để thêm sản phẩm vào giỏ hàng
        self.tree_products.bind('<Double-1>', self.on_product_double_click)

        # --- RIGHT: Giỏ hàng + Thanh toán ---
        cart_frame = tk.Frame(right, bg="#FFFFFF")
        cart_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        cart_title = tk.Label(cart_frame, text="Giỏ hàng", font=("Arial", 11, "bold"), fg="#333", bg="#FFFFFF", anchor="w")
        cart_title.pack(fill=tk.X, padx=2, pady=(0, 6))
        self.tree_cart = ttk.Treeview(cart_frame, columns=("STT", "Tên SP", "Biến thể", "SL", "Đơn giá", "Thành tiền"), show="headings", height=8, style="Custom.Treeview")
        for col in ("STT", "Tên SP", "Biến thể", "SL", "Đơn giá", "Thành tiền"):
            self.tree_cart.heading(col, text=col)
        self.tree_cart.column("STT", width=50, anchor="center")
        self.tree_cart.column("Tên SP", width=180)
        self.tree_cart.column("Biến thể", width=120)
        self.tree_cart.column("SL", width=60, anchor="center")
        self.tree_cart.column("Đơn giá", width=90, anchor="e")
        self.tree_cart.column("Thành tiền", width=110, anchor="e")
        self.tree_cart.pack(fill=tk.BOTH, expand=True)
        # Label mờ khi giỏ hàng trống
        self.empty_cart_label = tk.Label(cart_frame, text="Chưa có sản phẩm trong giỏ hàng", font=("Arial", 13, "italic"), fg="#888", bg="#FFFFFF")
        self.empty_cart_label.place(relx=0.5, rely=0.5, anchor="center")
        self.empty_cart_label.lower(self.tree_cart)
        # Tổng số mặt hàng
        self.label_total_items = tk.Label(cart_frame, text="Tổng sản phẩm: 0", font=("Arial", 11, "italic"), fg="#555", bg="#FFFFFF", anchor="w")
        self.label_total_items.pack(fill=tk.X, pady=(4, 0), padx=2, anchor="w")

        # Thông tin khách hàng
        customer_frame = tk.Frame(right, bg="#FFFFFF")
        customer_frame.pack(fill=tk.X, pady=5)
        customer_title = tk.Label(customer_frame, text="Khách hàng", font=("Arial", 11, "bold"), fg="#333", bg="#FFFFFF", anchor="w")
        customer_title.grid(row=0, column=0, columnspan=6, sticky="w", padx=2, pady=(0, 6))
        tk.Label(customer_frame, text="Tên KH:", font=("Arial", 13), bg="#FFFFFF", fg="#222").grid(row=1, column=0, sticky="e")
        self.entry_customer = tk.Entry(customer_frame, font=("Arial", 13), fg="#222", bg="#FFFFFF")
        self.entry_customer.grid(row=1, column=1, padx=5, sticky="ew")
        tk.Label(customer_frame, text="SĐT:", font=("Arial", 13), bg="#FFFFFF", fg="#222").grid(row=1, column=2, sticky="e")
        self.entry_phone = tk.Entry(customer_frame, font=("Arial", 13), fg="#222", bg="#FFFFFF")
        self.entry_phone.grid(row=1, column=3, padx=5, sticky="ew")
        ttk.Separator(customer_frame, orient=tk.VERTICAL).grid(row=1, column=4, sticky="ns", padx=8)
        btn_create_cus = tk.Button(customer_frame, text="Tạo mới KH", font=("Arial", 13, "bold"), command=self.on_create_customer,
                                  bg="#3498DB", fg="white", activebackground="#217dbb", activeforeground="white", bd=0, relief="flat", cursor="hand2")
        btn_create_cus.grid(row=1, column=5, padx=(10,0), sticky="ew", ipady=4, ipadx=4)
        # Responsive: cho các cột entry, nút co giãn
        customer_frame.grid_columnconfigure(1, weight=1)
        customer_frame.grid_columnconfigure(3, weight=1)
        customer_frame.grid_columnconfigure(5, weight=1)

        # Tổng tiền & 2 nút thanh toán/hàng chờ
        total_frame = ttk.Frame(right, style="Custom.TFrame")
        total_frame.pack(fill=tk.X, pady=(10, 0))
        tk.Label(total_frame, text="TỔNG TIỀN:", font=("Arial", 16, "bold"), bg=bg_color, fg="#222").pack(side=tk.LEFT)
        self.label_total = tk.Label(total_frame, text="0", font=("Arial", 28, "bold"), fg="red", bg=bg_color)
        self.label_total.pack(side=tk.LEFT, padx=10)

        # Frame chứa 2 nút ngang hàng
        button_row = tk.Frame(right, bg="#f5f7fa")
        button_row.pack(fill=tk.X, pady=(5, 5))
        btn_pay = tk.Button(
            button_row, text="XÁC NHẬN THANH TOÁN", bg="#f5f7fa", fg="#27AE60",
            font=("Arial", 16, "bold"), width=20, height=2, relief="flat", bd=0,
            command=self.on_pay, activebackground="#e0e0e0", activeforeground="#219150"
        )
        btn_pay.pack(side=tk.LEFT, padx=(0, 10), pady=2, fill=tk.X, expand=True)
        btn_hold = tk.Button(
            button_row, text="Đưa vào hàng chờ", font=("Arial", 12, "bold"), bg="#eafaf1", fg="#222", relief="flat", bd=0, padx=12, pady=8, command=self.hold_cart
        )
        btn_hold.pack(side=tk.LEFT, padx=(10, 0), pady=2, fill=tk.X, expand=True)

        # Mẹo nhỏ
        def show_tips():
            tips_popup = tk.Toplevel(self)
            tips_popup.title("Mẹo sử dụng")
            tips_popup.geometry("400x260")
            tips_popup.resizable(False, False)
            tk.Label(tips_popup, text="MẸO SỬ DỤNG", font=("Arial", 14, "bold"), fg="#2980b9").pack(pady=(12, 8))
            tips_text = (
                "- Quét mã vạch hoặc tìm kiếm sản phẩm, nhấn Enter để thêm vào giỏ.\n"
                "- Double click vào số lượng để sửa nhanh.\n"
                "- Có thể tạo khách hàng mới nhanh ở khung bên phải.\n"
                "- Sau khi thanh toán, hóa đơn sẽ tự động lưu file PDF.\n"
            )
            tk.Label(tips_popup, text=tips_text, font=("Arial", 12), justify="left", anchor="w").pack(padx=18, pady=4, fill="both", expand=True)
            tk.Button(tips_popup, text="Đóng", font=("Arial", 11), command=tips_popup.destroy).pack(pady=10)
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Assets/icon/lightbulb.png'))
        print("DEBUG icon_path:", icon_path)
        try:
            img = Image.open(icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            self.lightbulb_icon = ImageTk.PhotoImage(img)
        except Exception as e:
            print("Lỗi load icon:", e)
            self.lightbulb_icon = None
        btn_tip = tk.Button(right, text=" Mẹo", image=self.lightbulb_icon, compound="left", fg="#2980b9", bg=bg_color, font=("Arial", 11, "bold"), bd=0, cursor="hand2", command=show_tips)
        btn_tip.pack(anchor="w", pady=2)
        # Thêm dòng hướng dẫn nhỏ dưới nút Mẹo
        lbl_tip_note = tk.Label(right, text="Nếu gặp khó khăn hãy ấn vào đây", font=("Arial", 10, "italic"), fg="#888", bg=bg_color, anchor="w")
        lbl_tip_note.pack(anchor="w", padx=2, pady=(0, 8))

        # Label trạng thái
        self.status_label = tk.Label(self, text="", font=("Arial", 11, "italic"), fg="#2980b9", bg=bg_color)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=2)

        self.tree_cart.bind('<Key>', self.on_key_press)
        self.tree_cart.bind('<Double-1>', self.on_double_click)
        self.entry_barcode.bind('<Return>', self.on_barcode_enter)
        self.entry_phone.bind('<FocusOut>', self.on_phone_focus_out)
        self.entry_phone.bind('<Return>', self.on_phone_focus_out)

    def set_status(self, msg):
        self.status_label.config(text=msg)

    def load_products(self):
        self.tree_products.delete(*self.tree_products.get_children())
        products = ProductVariant.get_all()
        for p in products:
            self.tree_products.insert('', 'end', values=(p.ten_bienthe, p.gia))

    def reload_cart(self):
        cart_items = self.cart_manager.get_cart_items()
        total = self.cart_manager.calculate_total()
        self.tree_cart.delete(*self.tree_cart.get_children())
        if not cart_items:
            self.empty_cart_label.lift(self.tree_cart)
        else:
            self.empty_cart_label.lower(self.tree_cart)
        for item in cart_items:
            self.tree_cart.insert('', 'end', values=item[:6] + (item[6],))
        self.label_total.config(text=f"{total:,}")
        self.label_total_items.config(text=f"Tổng sản phẩm: {len(cart_items)}")

    def on_scan(self):
        barcode = scan_barcode()
        if barcode:
            self.cart_manager.add_to_cart(barcode, 1)
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, barcode)
            self.reload_cart()
        phone = self.entry_phone.get().strip()
        if not phone:
            self.entry_customer.config(state='normal')
            self.entry_customer.delete(0, tk.END)
            self.entry_customer.config(state='readonly')
            return
        customer = payment.get_customer_by_phone(phone)
        self.entry_customer.config(state='normal')
        if customer:
            self.entry_customer.delete(0, tk.END)
            self.entry_customer.insert(0, customer[1])
        else:
            self.entry_customer.delete(0, tk.END)
        self.entry_customer.config(state='readonly')

    def on_key_press(self, event):
        selected_item = self.tree_cart.selection()
        if not selected_item:
            return
        item = self.tree_cart.item(selected_item[0])
        values = item['values']
        barcode = values[1]
        quantity = int(values[3])
        if event.keysym in ('plus', 'KP_Add', 'Up'):
            self.cart_manager.update_cart_item(barcode, quantity + 1)
            self.reload_cart()
        elif event.keysym in ('minus', 'KP_Subtract', 'Down'):
            if quantity > 1:
                self.cart_manager.update_cart_item(barcode, quantity - 1)
            else:
                self.cart_manager.remove_from_cart(barcode)
            self.reload_cart()
        elif event.keysym == 'Delete':
            self.cart_manager.remove_from_cart(barcode)
            self.reload_cart()

    def on_double_click(self, event):
        region = self.tree_cart.identify('region', event.x, event.y)
        if region != 'cell':
            return
        col = self.tree_cart.identify_column(event.x)
        col_index = int(col.replace('#', '')) - 1
        columns = ('STT', 'Tên SP', 'Biến thể', 'SL', 'Đơn giá', 'Thành tiền')
        if columns[col_index] != 'SL':
            return
        row_id = self.tree_cart.identify_row(event.y)
        if not row_id:
            return
        x, y, width, height = self.tree_cart.bbox(row_id, col)
        value = self.tree_cart.set(row_id, column=col)
        entry = tk.Entry(self.tree_cart, width=5)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus_set()
        def on_entry_confirm(event=None):
            new_value = entry.get()
            try:
                if not new_value.strip():
                    entry.destroy()
                    return
                new_quantity = int(new_value)
                item = self.tree_cart.item(row_id)
                barcode = item['values'][6]
                if new_quantity <= 0:
                    self.cart_manager.remove_from_cart(barcode)
                else:
                    self.cart_manager.update_cart_item(barcode, new_quantity)
                self.reload_cart()
            except Exception as e:
                print('Lỗi cập nhật số lượng:', e)
            finally:
                entry.destroy()
        entry.bind('<Return>', on_entry_confirm)
        entry.bind('<FocusOut>', on_entry_confirm)

    def on_barcode_enter(self, event=None):
        barcode = self.entry_barcode.get().strip()
        if barcode:
            self.cart_manager.add_to_cart(barcode, 1)
            self.reload_cart()

    def on_pay(self):
        tien_khach_dua = 0
        tien_thoi_lai = 0
        name = self.entry_customer.get().strip()
        phone = self.entry_phone.get().strip()
        method = 'Tiền mặt'
        cart_items = self.cart_manager.get_cart_items()
        total = self.cart_manager.calculate_total()
        if not cart_items:
            messagebox.showwarning('Thiếu thông tin', 'Vui lòng có sản phẩm trong giỏ!')
            return
        if not method:
            messagebox.showwarning('Thiếu thông tin', 'Vui lòng chọn phương thức thanh toán!')
            return
        if method == 'Tiền mặt':
            cash_popup = CashPopup(self, float(str(total).replace(',', '')))
            self.wait_window(cash_popup.popup)
            if not cash_popup.result['ok']:
                return
            tien_khach_dua = cash_popup.tien_khach_dua
            tien_thoi_lai = cash_popup.tien_thoi_lai
        db_path = "database/ministore_db.sqlite"
        setting = SettingCore(db_path)
        store_id = setting.get_setting("selected_store_id")
        if store_id is not None:
            store_id = int(store_id)
        else:
            store_id = 1
        success, result = payment.process_payment(name, phone, method, cart_items, total, tien_khach_dua, tien_thoi_lai, self.nhanvien_id, store_id)
        if success:
            self.cart_manager.clear_cart()
            self.reload_cart()
            self.entry_customer.config(state='normal')
            self.entry_customer.delete(0, tk.END)
            self.entry_customer.config(state='readonly')
            self.entry_phone.delete(0, tk.END)
            pdf_path = payment.export_invoice_pdf(result, tien_khach_dua, tien_thoi_lai)
            if pdf_path:
                messagebox.showinfo('Thành công', f'Thanh toán thành công! Hóa đơn đã được lưu: {pdf_path}')
                webbrowser.open(pdf_path)
            else:
                messagebox.showinfo('Thành công', f'Thanh toán thành công! (Không tạo được file hóa đơn)')
            if self.main_window and self.main_window.notebook.tabs():
                current_tab = self.main_window.notebook.select()
                current_tab_text = self.main_window.notebook.tab(current_tab, "text")
                if current_tab_text.startswith("Giỏ hàng"):
                    self.main_window.notebook.forget(current_tab)
                    if current_tab_text in self.main_window.tabs:
                        del self.main_window.tabs[current_tab_text]
        else:
            messagebox.showerror('Lỗi', f'Thanh toán thất bại: {result}')

    def on_create_customer(self):
        popup = tk.Toplevel(self)
        popup.title("Tạo khách hàng mới")
        popup.geometry("350x200")
        tk.Label(popup, text="Tên khách hàng:", font=("Arial", 12)).pack(pady=5)
        entry_name = tk.Entry(popup, font=("Arial", 12))
        entry_name.pack(pady=5)
        tk.Label(popup, text="Số điện thoại:", font=("Arial", 12)).pack(pady=5)
        entry_phone = tk.Entry(popup, font=("Arial", 12))
        entry_phone.pack(pady=5)
        def save():
            name = entry_name.get().strip()
            phone = entry_phone.get().strip()
            if not name or not phone:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên và số điện thoại!")
                return
            try:
                result = payment.create_customer_by_phone(name, phone)
                if result:
                    messagebox.showinfo("Thành công", "Thêm khách hàng thành công!")
                    popup.destroy()
                    self.entry_phone.delete(0, tk.END)
                    self.entry_phone.insert(0, phone)
                    self.entry_customer.config(state='normal')
                    self.entry_customer.delete(0, tk.END)
                    self.entry_customer.insert(0, name)
                    self.entry_customer.config(state='readonly')
                else:
                    messagebox.showerror("Lỗi", "Không thể thêm khách hàng!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        tk.Button(popup, text="Lưu", font=("Arial", 12), command=save).pack(pady=10)

    def hold_cart(self):
        cart_items = self.cart_manager.get_cart_items()
        if not cart_items:
            messagebox.showinfo("Thông báo", "Chưa có sản phẩm trong giỏ hàng để đưa vào hàng chờ!")
            return
        customer = self.entry_customer.get().strip()
        phone = self.entry_phone.get().strip()
        self.hold_cart_count += 1
        customer_name = customer if customer else "Khách lẻ"
        tab_name = f"Giỏ hàng {self.hold_cart_count} - {customer_name}"
        hold_data = {
            'cart': cart_items,
            'customer': customer,
            'phone': phone
        }
        if self.main_window:
            from src.views.payment_view import PaymentView
            frame = tk.Frame(self.main_window.notebook, bg="#F5F7FA")
            new_cart_manager = CartManager()
            for item in cart_items:
                barcode = item[6]
                quantity = item[3]
                new_cart_manager.add_to_cart(barcode, quantity)
            new_payment_view = PaymentView(frame, self.nhanvien_id, self.main_window, new_cart_manager)
            new_payment_view.load_hold_cart_data(hold_data)
            self.main_window.notebook.add(frame, text=tab_name)
            self.main_window.tabs[tab_name] = {"frame": frame}
            self.main_window.notebook.select(frame)
            self.clear_cart()
            messagebox.showinfo("Thành công", f"Đã tạo tab mới: {tab_name}")
        else:
            self.hold_carts.append(hold_data)
            self.clear_cart()
            messagebox.showinfo("Thành công", "Đã đưa giỏ hàng vào hàng chờ!")

    def load_hold_cart_data(self, hold_data):
        self.cart_manager.clear_cart()
        self.clear_cart()
        for item in hold_data['cart']:
            barcode = item[6]
            quantity = item[3]
            self.cart_manager.add_to_cart(barcode, quantity)
        self.entry_customer.delete(0, tk.END)
        self.entry_customer.insert(0, hold_data['customer'])
        self.entry_phone.delete(0, tk.END)
        self.entry_phone.insert(0, hold_data['phone'])
        self.reload_cart()

    def show_hold_carts(self):
        if not self.hold_carts:
            if self.main_window:
                messagebox.showinfo("Thông báo", "Không có giỏ hàng nào đang chờ! Các giỏ hàng chờ sẽ được hiển thị dưới dạng tab riêng biệt.")
            else:
                messagebox.showinfo("Thông báo", "Không có giỏ hàng nào đang chờ!")
            return
        popup = tk.Toplevel(self)
        popup.title("Danh sách hàng chờ")
        popup.geometry("500x300")
        tk.Label(popup, text="Chọn đơn hàng chờ để tiếp tục thanh toán:", font=("Arial", 12, "bold")).pack(pady=8)
        listbox = tk.Listbox(popup, font=("Arial", 12), height=8)
        for idx, h in enumerate(self.hold_carts):
            kh = h['customer'] or "(Không tên)"
            phone = h['phone'] or ""
            listbox.insert(tk.END, f"{idx+1}. {kh} - {phone} ({len(h['cart'])} SP)")
        listbox.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)
        def on_select():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Chọn đơn", "Vui lòng chọn đơn hàng chờ!")
                return
            idx = sel[0]
            hold = self.hold_carts.pop(idx)
            self.load_hold_cart_data(hold)
            popup.destroy()
        btn = tk.Button(popup, text="Chọn đơn này", font=("Arial", 12, "bold"), bg="#eafaf1", fg="#222", relief="flat", bd=0, padx=12, pady=8, command=on_select)
        btn.pack(pady=8)

    def clear_cart(self):
        self.cart_manager.clear_cart()
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)
        self.entry_customer.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.reload_cart()

    def on_product_double_click(self, event):
        selected = self.tree_products.selection()
        if selected:
            values = self.tree_products.item(selected[0])['values']
            ten_bienthe = values[0]
            ok = self.cart_manager.add_product_by_variant_name(ten_bienthe, 1)
            if ok:
                self.reload_cart()
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy barcode cho sản phẩm này!")

    def on_phone_focus_out(self, event):
        phone = self.entry_phone.get().strip()
        if not phone:
            return
        from Core.payment import get_customer_by_phone
        customer = get_customer_by_phone(phone)
        if customer:
            self.entry_customer.delete(0, tk.END)
            self.entry_customer.insert(0, customer[1])  # customer[1] là tên khách hàng
        # Nếu không có khách hàng thì không làm gì hoặc có thể xóa tên KH 