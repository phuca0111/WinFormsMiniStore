import sys
import os
import subprocess
import webbrowser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.barcode_scanner import scan_barcode
from Core import cart, payment
from Core.setting import SettingCore
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import pytz
from datetime import datetime, timedelta
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register DejaVu font
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))
except Exception as e:
    print(f"Error registering font: {e}")

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
        self.entry_cash = tk.Entry(self.popup, font=('Arial', 12))
        self.entry_cash.pack(pady=5)
        self.label_change = ttk.Label(self.popup, text='', font=('Arial', 11, 'bold'), foreground='blue')
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

class CustomerPopup:
    def __init__(self, parent, db_path):
        self.popup = tk.Toplevel(parent)
        self.popup.title('Thêm khách hàng mới')
        self.popup.geometry('400x500')
        self.db_path = db_path
        self.result = {'ok': False}
        
        # Tạo các trường nhập liệu
        ttk.Label(self.popup, text='Tên khách hàng:').pack(pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(self.popup, textvariable=self.name_var, width=40).pack(pady=2)
        
        ttk.Label(self.popup, text='Số điện thoại:').pack(pady=2)
        self.phone_var = tk.StringVar()
        ttk.Entry(self.popup, textvariable=self.phone_var, width=40).pack(pady=2)
        
        ttk.Label(self.popup, text='Email:').pack(pady=2)
        self.email_var = tk.StringVar()
        ttk.Entry(self.popup, textvariable=self.email_var, width=40).pack(pady=2)
        
        ttk.Label(self.popup, text='Địa chỉ:').pack(pady=2)
        self.address_var = tk.StringVar()
        ttk.Entry(self.popup, textvariable=self.address_var, width=40).pack(pady=2)
        
        ttk.Label(self.popup, text='Ngày sinh (YYYY-MM-DD):').pack(pady=2)
        self.birthdate_var = tk.StringVar()
        ttk.Entry(self.popup, textvariable=self.birthdate_var, width=40).pack(pady=2)
        
        ttk.Label(self.popup, text='Giới tính:').pack(pady=2)
        self.gender_var = tk.StringVar()
        ttk.Combobox(self.popup, textvariable=self.gender_var, values=['Nam', 'Nữ'], width=37).pack(pady=2)
        
        # Nút lưu
        ttk.Button(self.popup, text='Lưu', command=self.on_save).pack(pady=10)
        
    def on_save(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        birthdate = self.birthdate_var.get().strip()
        gender = self.gender_var.get().strip()
        
        if not (name and phone):
            messagebox.showerror('Lỗi', 'Vui lòng nhập tên và số điện thoại!')
            return
            
        success, msg = payment.create_customer_by_phone(name, phone)
        if success:
            messagebox.showinfo('Thành công', 'Thêm khách hàng thành công!')
            self.result['ok'] = True
            self.result['phone'] = phone
            self.popup.destroy()
        else:
            messagebox.showerror('Lỗi', msg)

class PaymentView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.parent = parent
        self.db_path = db_path
        self.setting_core = SettingCore(self.db_path)
        
        # Khai báo biến ở scope của instance
        self.tien_khach_dua = 0
        self.tien_thoi_lai = 0

        # Cấu hình grid cho self.frame
        self.frame.grid_rowconfigure(3, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        row_idx = 0

        # Tiêu đề "Tạo đơn hàng"
        label = ttk.Label(self.frame, text='Tạo đơn hàng', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=5, padx=20, pady=5, sticky=tk.N)
        row_idx += 1

        # Frame nhập barcode và hiển thị barcode
        frame_barcode = ttk.Frame(self.frame)
        frame_barcode.grid(row=row_idx, column=0, columnspan=5, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1
        frame_barcode.grid_columnconfigure(1, weight=1)

        ttk.Label(frame_barcode, text='Barcode:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_barcode = ttk.Entry(frame_barcode, font=('Arial', 12))
        self.entry_barcode.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        self.label_barcode = ttk.Label(frame_barcode, text='', font=('Arial', 12), foreground='blue')
        self.label_barcode.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        btn_scan = ttk.Button(frame_barcode, text='Quét mã vạch (Camera)', command=self.on_scan_barcode_button)
        btn_scan.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)

        # Treeview giỏ hàng
        frame_cart = ttk.LabelFrame(self.frame, text='Danh sách sản phẩm trong giỏ hàng', padding=10)
        frame_cart.grid(row=row_idx, column=0, columnspan=5, padx=10, pady=10, sticky=tk.NSEW)
        row_idx += 1
        frame_cart.grid_rowconfigure(0, weight=1)
        frame_cart.grid_columnconfigure(0, weight=1)

        # Frame chứa treeview và các nút điều khiển
        cart_control_frame = ttk.Frame(frame_cart)
        cart_control_frame.grid(row=0, column=0, sticky=tk.NSEW)
        cart_control_frame.grid_columnconfigure(0, weight=1)

        self.columns = ('STT', 'Tên sản phẩm', 'Tên biến thể', 'Số lượng', 'Đơn giá', 'Thành tiền', 'Barcode')
        self.tree_cart = ttk.Treeview(cart_control_frame, columns=self.columns, show='headings', height=10)
        for col in self.columns:
            self.tree_cart.heading(col, text=col)
            self.tree_cart.column(col, anchor='center')
        self.tree_cart.grid(row=0, column=0, sticky=tk.NSEW)

        # Frame chứa các nút điều khiển
        cart_buttons_frame = ttk.Frame(cart_control_frame)
        cart_buttons_frame.grid(row=1, column=0, sticky=tk.EW, pady=5)
        cart_buttons_frame.grid_columnconfigure(0, weight=1)

        # Nút xóa sản phẩm
        ttk.Button(cart_buttons_frame, text='Xóa sản phẩm', command=self.remove_selected_item).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)

        label_hint_frame = ttk.Frame(frame_cart) # Create a frame for hints
        label_hint_frame.grid(row=1, column=0, sticky=tk.W, padx=5)

        tk.Label(label_hint_frame, text="Mẹo: Nhấp đúp vào ô Số lượng để sửa nhanh số lượng sản phẩm. Nhập 0 để xóa sản phẩm.", 
                  font=('Arial', 9), fg='gray').pack(anchor='w')
        tk.Label(label_hint_frame, text="Mẹo: Khi không quét được mã vạch, hãy nhập thủ công và ấn enter bạn nhé.", 
                  font=('Arial', 9), fg='gray').pack(anchor='w')
        tk.Label(label_hint_frame, text="Mẹo: Khi nhập số điện thoại, sẽ hiển thị tên khách hàng.", 
                  font=('Arial', 9), fg='gray').pack(anchor='w')

        # Frame thông tin khách hàng và thanh toán
        frame_info = ttk.LabelFrame(self.frame, text='Thông tin thanh toán', padding=10)
        frame_info.grid(row=row_idx, column=0, columnspan=5, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1

        frame_info.grid_columnconfigure(1, weight=1)
        frame_info.grid_columnconfigure(3, weight=1)

        ttk.Label(frame_info, text='Tên khách hàng:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_customer = ttk.Entry(frame_info, font=('Arial', 12), state='readonly')
        self.entry_customer.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(frame_info, text='Số điện thoại:').grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.entry_phone = ttk.Entry(frame_info, font=('Arial', 12))
        self.entry_phone.grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)

        # Nút tạo khách hàng mới (luôn hiển thị)
        btn_create_customer = ttk.Button(frame_info, text='Tạo thông tin khách hàng', command=self.show_add_customer)
        btn_create_customer.grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)

        ttk.Label(frame_info, text='Tổng tiền:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_total = ttk.Entry(frame_info, font=('Arial', 12), state='readonly')
        self.entry_total.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(frame_info, text='Phương thức thanh toán:').grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.combobox_method = ttk.Combobox(frame_info, font=('Arial', 12), state='readonly')
        self.combobox_method['values'] = ['Tiền mặt', 'Chuyển khoản', 'Thẻ']
        self.combobox_method.grid(row=1, column=3, padx=5, pady=5, sticky=tk.EW)

        # Nút xác nhận thanh toán
        btn_pay = ttk.Button(self.frame, text='Xác nhận thanh toán', width=20, command=self.on_pay)
        btn_pay.grid(row=row_idx, column=0, columnspan=5, pady=15)
        row_idx += 1

        # Hiển thị giỏ hàng khi mở form
        self.reload_cart()

        # Bindings
        self.entry_phone.bind('<FocusOut>', self.on_phone_focus_out)
        self.entry_phone.bind('<Return>', lambda e: self.on_phone_focus_out())
        self.tree_cart.bind('<Key>', self.on_key_press)
        self.tree_cart.focus_set()
        self.tree_cart.bind('<Double-1>', self.on_double_click)
        self.entry_barcode.bind('<Return>', self.on_barcode_enter)
        self.combobox_method.bind('<<ComboboxSelected>>', self.on_method_selected)

    def on_scan_barcode_button(self):
        barcode = scan_barcode() # Use original scan_barcode
        if barcode:
            payment.scan_and_add_barcode(lambda: barcode, barcode) # Ensure this function call is correct
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, barcode)
            self.label_barcode.config(text=f"Barcode: {barcode}")
            self.reload_cart()

    def reload_cart(self):
        cart_items, total = payment.reload_cart()
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)
        for item in cart_items:
            self.tree_cart.insert('', 'end', values=item)
        self.entry_total.config(state='normal')
        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(0, f"{total:,}")
        self.entry_total.config(state='readonly')

    def on_phone_focus_out(self, event=None):
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
            self.entry_customer.insert(0, customer[1])  # customer[1] là tên
        else:
            self.entry_customer.delete(0, tk.END)
        self.entry_customer.config(state='readonly')

    def show_add_customer(self):
        popup = CustomerPopup(self.frame, self.db_path)
        self.frame.wait_window(popup.popup)
        if popup.result['ok']:
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, popup.result['phone'])
            self.entry_phone.event_generate('<FocusOut>')  # Trigger focus out event to load customer info

    def on_key_press(self, event):
        selected_item = self.tree_cart.selection()
        if not selected_item:
            return
        item = self.tree_cart.item(selected_item[0])
        values = item['values']
        barcode = values[6]
        quantity = int(values[3])
        if event.keysym in ('plus', 'KP_Add', 'Up'):
            payment.update_cart_item(barcode, quantity + 1)
            self.reload_cart()
        elif event.keysym in ('minus', 'KP_Subtract', 'Down'):
            if quantity > 1:
                payment.update_cart_item(barcode, quantity - 1)
            else:
                payment.remove_from_cart(barcode)
            self.reload_cart()
        elif event.keysym == 'Delete':
            payment.remove_from_cart(barcode)
            self.reload_cart()

    def on_double_click(self, event):
        region = self.tree_cart.identify('region', event.x, event.y)
        if region != 'cell':
            return
        col = self.tree_cart.identify_column(event.x)
        col_index = int(col.replace('#', '')) - 1
        # Use self.columns directly, as it's a class attribute now
        if self.columns[col_index] != 'Số lượng': 
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
            print(f"DEBUG: New value entered: {new_value}")
            try:
                new_quantity = int(new_value)
                print(f"DEBUG: Converted new quantity: {new_quantity}")
                item = self.tree_cart.item(row_id)
                barcode = item['values'][6]
                print(f"DEBUG: Barcode of item: {barcode}")
                if new_quantity <= 0:
                    payment.remove_from_cart(barcode)
                    print(f"DEBUG: Removed item with barcode: {barcode}")
                else:
                    payment.update_cart_item(barcode, new_quantity)
                    print(f"DEBUG: Updated item {barcode} to quantity {new_quantity}")
                self.reload_cart()
            except ValueError:
                print(f"DEBUG: Invalid quantity entered: {new_value}. Please enter a valid number.")
                messagebox.showerror("Lỗi", "Số lượng không hợp lệ. Vui lòng nhập một số.")
            except Exception as e:
                print(f'DEBUG: Lỗi cập nhật số lượng: {e}')
                import traceback
                traceback.print_exc()
            finally:
                entry.destroy()

        entry.bind('<Return>', on_entry_confirm)
        entry.bind('<FocusOut>', on_entry_confirm)

    def on_barcode_enter(self, event=None):
        barcode = self.entry_barcode.get().strip()
        print(f"DEBUG: Nhận barcode từ input: {barcode}")
        if not barcode:
            print("DEBUG: Barcode trống")
            return
        payment.add_to_cart(barcode, 1)  # Thêm số lượng 1
        self.entry_barcode.delete(0, tk.END)
        self.label_barcode.config(text=f"Barcode: {barcode}")
        self.reload_cart()

    def remove_selected_item(self):
        selected_item = self.tree_cart.selection()
        if not selected_item:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm cần xóa!')
            return
        if messagebox.askyesno('Xác nhận', 'Bạn có chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?'):
            item = self.tree_cart.item(selected_item[0])
            values = item['values']
            barcode = values[6]
            payment.remove_from_cart(barcode)
            self.reload_cart()

    def on_method_selected(self, event=None):
        method = self.combobox_method.get()
        if method == 'Tiền mặt':
            total = float(self.entry_total.get().replace(',', ''))
            popup = CashPopup(self.frame, total)
            self.frame.wait_window(popup.popup)
            if popup.result['ok']:
                self.tien_khach_dua = popup.tien_khach_dua
                self.tien_thoi_lai = popup.tien_thoi_lai
                # Call on_pay after cash amount is confirmed
                self.on_pay()

    def on_pay(self):
        # Kiểm tra giỏ hàng
        cart_items = payment.get_cart_items()
        if not cart_items:
            messagebox.showerror('Lỗi', 'Vui lòng thêm sản phẩm vào giỏ hàng trước khi thanh toán!')
            return

        method = self.combobox_method.get()
        if not method:
            messagebox.showerror('Lỗi', 'Vui lòng chọn phương thức thanh toán!')
            return
        phone = self.entry_phone.get().strip()
        if not phone:
            messagebox.showerror('Lỗi', 'Vui lòng nhập số điện thoại khách hàng!')
            return
        customer = payment.get_customer_by_phone(phone)
        if not customer:
            messagebox.showerror('Lỗi', 'Không tìm thấy thông tin khách hàng!')
            return
        total = float(self.entry_total.get().replace(',', ''))
        
        # If cash payment, on_method_selected already calls on_pay after popup.
        # So we only proceed if method is not 'Tiền mặt' or if it's already set from popup.
        if method == 'Tiền mặt' and self.tien_khach_dua == 0: # Ensure popup has been processed
            return
            
        success, msg = payment.process_payment(
            customer_name=self.entry_customer.get(),
            phone=phone,
            payment_method=method,
            cart_items=payment.get_cart_items(),
            total=total,
            tien_khach_dua=self.tien_khach_dua,
            tien_thoi_lai=self.tien_thoi_lai
        )
        if success:
            payment.clear_cart()
            self.reload_cart()
            self.entry_phone.delete(0, tk.END)
            self.entry_customer.config(state='normal')
            self.entry_customer.delete(0, tk.END)
            self.entry_customer.config(state='readonly')
            self.combobox_method.set('')
            pdf_path = payment.export_invoice_pdf(msg, self.tien_khach_dua, self.tien_thoi_lai) # msg is hoadon_id
            if pdf_path:
                messagebox.showinfo('Thành công', f'Thanh toán thành công! Hóa đơn đã được lưu: {pdf_path}')
                webbrowser.open(pdf_path)
            else:
                messagebox.showinfo('Thành công', f'Thanh toán thành công! (Không tạo được file hóa đơn)')
        else:
            messagebox.showerror('Lỗi', f'Thanh toán thất bại: {msg}')

def main(nhanvien_id):
    root = tk.Tk()
    root.title('Thanh toán hóa đơn')
    root.geometry('900x600')
    app = PaymentView(root)
    app.frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == '__main__':
    main(1) 