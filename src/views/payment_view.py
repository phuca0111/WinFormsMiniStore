import sys
import os
import subprocess
import webbrowser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.barcode_scanner import scan_barcode
from Core import cart, payment

def main():
    root = tk.Tk()
    root.title('Thanh toán hóa đơn')
    root.geometry('900x600')

    # Khai báo biến ở scope cao nhất.
    tien_khach_dua = None
    tien_thoi_lai = None

    # Frame nhập barcode và hiển thị barcode
    frame_barcode = ttk.Frame(root)
    frame_barcode.pack(fill=tk.X, padx=10, pady=5)

    ttk.Label(frame_barcode, text='Barcode:').grid(row=0, column=0, padx=5, pady=5)
    entry_barcode = ttk.Entry(frame_barcode, font=('Arial', 12))
    entry_barcode.grid(row=0, column=1, padx=5, pady=5)

    label_barcode = ttk.Label(frame_barcode, text='', font=('Arial', 12), foreground='blue')
    label_barcode.grid(row=0, column=2, padx=5, pady=5)

    # Treeview giỏ hàng
    frame_cart = ttk.LabelFrame(root, text='Danh sách sản phẩm trong giỏ hàng', padding=10)
    frame_cart.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
    columns = ('STT', 'Tên sản phẩm', 'Tên biến thể', 'Số lượng', 'Đơn giá', 'Thành tiền', 'Barcode')
    tree_cart = ttk.Treeview(frame_cart, columns=columns, show='headings', height=10)
    for col in columns:
        tree_cart.heading(col, text=col)
        tree_cart.column(col, anchor='center')
    tree_cart.pack(fill=tk.BOTH, expand=True)

    label_hint = tk.Label(frame_cart, text="Mẹo: Nhấp đúp vào ô Số lượng để sửa nhanh số lượng sản phẩm. Nhập 0 để xóa sản phẩm.", 
                          font=('Arial', 9), fg='gray')
    label_hint.pack(anchor='w', padx=5, pady=(2, 0))
    label_hint = tk.Label(frame_cart, text="Mẹo:khi không quét được mã vạch hãy nhập thủ công và ấn enter bạn nhé.", 
                          font=('Arial', 9), fg='gray')
    label_hint.pack(anchor='w', padx=5, pady=(2, 0))
    label_hint = tk.Label(frame_cart, text="Mẹo:khi nhập số điện thoại sẽ hiển thị tên khách hàng.", 
                          font=('Arial', 9), fg='gray')
    label_hint.pack(anchor='w', padx=5, pady=(2, 0))
    
    def reload_cart():
        cart_items, total = payment.reload_cart()
        for item in tree_cart.get_children():
            tree_cart.delete(item)
        for item in cart_items:
            tree_cart.insert('', 'end', values=item)
        entry_total.config(state='normal')
        entry_total.delete(0, tk.END)
        entry_total.insert(0, f"{total:,}")
        entry_total.config(state='readonly')

    def on_scan():
        barcode = payment.scan_and_add_barcode(scan_barcode)
        if barcode:
            entry_barcode.delete(0, tk.END)
            entry_barcode.insert(0, barcode)
            label_barcode.config(text=f"Barcode: {barcode}")
            reload_cart()

    btn_scan = ttk.Button(frame_barcode, text='Quét mã vạch (Camera)', command=on_scan)
    btn_scan.grid(row=0, column=3, padx=5, pady=5)

    # Frame thông tin khách hàng và thanh toán
    frame_info = ttk.LabelFrame(root, text='Thông tin thanh toán', padding=10)
    frame_info.pack(fill=tk.X, padx=10, pady=5)

    ttk.Label(frame_info, text='Tên khách hàng:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entry_customer = ttk.Entry(frame_info, font=('Arial', 12), state='readonly')
    entry_customer.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_info, text='Số điện thoại:').grid(row=0, column=2, padx=5, pady=5, sticky='e')
    entry_phone = ttk.Entry(frame_info, font=('Arial', 12))
    entry_phone.grid(row=0, column=3, padx=5, pady=5)

    # Nút tạo khách hàng mới (luôn hiển thị)
    btn_create_customer = ttk.Button(frame_info, text='Tạo thông tin khách hàng')
    btn_create_customer.grid(row=0, column=4, padx=5, pady=5)

    ttk.Label(frame_info, text='Tổng tiền:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_total = ttk.Entry(frame_info, font=('Arial', 12), state='readonly')
    entry_total.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_info, text='Phương thức thanh toán:').grid(row=1, column=2, padx=5, pady=5, sticky='e')
    combobox_method = ttk.Combobox(frame_info, font=('Arial', 12), state='readonly')
    combobox_method['values'] = ['Tiền mặt', 'Chuyển khoản', 'Thẻ']
    combobox_method.grid(row=1, column=3, padx=5, pady=5)

    # Nút xác nhận thanh toán
    btn_pay = ttk.Button(root, text='Xác nhận thanh toán', width=20)
    btn_pay.pack(pady=15)

    # Hiển thị giỏ hàng khi mở form
    reload_cart()

    def on_phone_focus_out(event=None):
        phone = entry_phone.get().strip()
        if not phone:
            entry_customer.config(state='normal')
            entry_customer.delete(0, tk.END)
            entry_customer.config(state='readonly')
            return
        customer = payment.get_customer_by_phone(phone)
        entry_customer.config(state='normal')
        if customer:
            entry_customer.delete(0, tk.END)
            entry_customer.insert(0, customer[1])  # customer[1] là tên
        else:
            entry_customer.delete(0, tk.END)
        entry_customer.config(state='readonly')

    entry_phone.bind('<FocusOut>', on_phone_focus_out)
    entry_phone.bind('<Return>', lambda e: on_phone_focus_out())

    def open_customer_view():
        customer_view_path = os.path.join(os.path.dirname(__file__), 'customer_view.py')
        subprocess.Popen([sys.executable, customer_view_path])

    btn_create_customer.config(command=open_customer_view)

    def on_key_press(event):
        selected_item = tree_cart.selection()
        if not selected_item:
            return
        item = tree_cart.item(selected_item[0])
        values = item['values']
        barcode = values[6]
        quantity = int(values[3])
        if event.keysym in ('plus', 'KP_Add', 'Up'):
            payment.update_cart_item(barcode, quantity + 1)
            reload_cart()
        elif event.keysym in ('minus', 'KP_Subtract', 'Down'):
            if quantity > 1:
                payment.update_cart_item(barcode, quantity - 1)
            else:
                payment.remove_from_cart(barcode)
            reload_cart()
        elif event.keysym == 'Delete':
            payment.remove_from_cart(barcode)
            reload_cart()

    tree_cart.bind('<Key>', on_key_press)
    tree_cart.focus_set()

    def on_double_click(event):
        region = tree_cart.identify('region', event.x, event.y)
        if region != 'cell':
            return
        col = tree_cart.identify_column(event.x)
        col_index = int(col.replace('#', '')) - 1
        if columns[col_index] != 'Số lượng':
            return
        row_id = tree_cart.identify_row(event.y)
        if not row_id:
            return
        x, y, width, height = tree_cart.bbox(row_id, col)
        value = tree_cart.set(row_id, column=col)
        entry = tk.Entry(tree_cart, width=5)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus_set()

        def on_entry_confirm(event=None):
            new_value = entry.get()
            try:
                new_quantity = int(new_value)
                item = tree_cart.item(row_id)
                barcode = item['values'][6]
                if new_quantity <= 0:
                    payment.remove_from_cart(barcode)
                else:
                    payment.update_cart_item(barcode, new_quantity)
                reload_cart()
            except Exception as e:
                print('Lỗi cập nhật số lượng:', e)
            finally:
                entry.destroy()

        entry.bind('<Return>', on_entry_confirm)
        entry.bind('<FocusOut>', on_entry_confirm)

    tree_cart.bind('<Double-1>', on_double_click)

    def on_barcode_enter(event=None):
        barcode = entry_barcode.get().strip()
        if barcode:
            payment.scan_and_add_barcode(lambda: barcode, barcode)
            label_barcode.config(text=f"Barcode: {barcode}")
            reload_cart()

    entry_barcode.bind('<Return>', on_barcode_enter)

    def on_method_selected(event=None):
        method = combobox_method.get()
        if method == 'Tiền mặt':
            total = entry_total.get().replace(',', '').strip()
            try:
                total = float(total)
            except:
                total = 0
            popup = tk.Toplevel(root)
            popup.title('Nhập số tiền khách đưa')
            popup.geometry('300x180')
            ttk.Label(popup, text='Tổng tiền:').pack(pady=5)
            ttk.Label(popup, text=f"{total:,.0f} VND", font=('Arial', 12, 'bold')).pack(pady=5)
            ttk.Label(popup, text='Tiền khách đưa:').pack(pady=5)
            cash_var = tk.StringVar()
            entry_cash = ttk.Entry(popup, textvariable=cash_var, font=('Arial', 12))
            entry_cash.pack(pady=5)
            label_change = ttk.Label(popup, text='', font=('Arial', 11, 'bold'), foreground='blue')
            label_change.pack(pady=5)
            def calc_change(event=None):
                try:
                    cash = float(cash_var.get().replace(',', ''))
                    change = cash - total
                    if change < 0:
                        label_change.config(text=f'Thiếu {abs(change):,.0f} VND', foreground='red')
                    else:
                        label_change.config(text=f'Tiền thừa: {change:,.0f} VND', foreground='blue')
                except:
                    label_change.config(text='Nhập số hợp lệ!', foreground='red')
            entry_cash.bind('<KeyRelease>', calc_change)
            def on_ok():
                try:
                    cash = float(cash_var.get().replace(',', ''))
                    if cash < total:
                        messagebox.showerror('Lỗi', 'Tiền khách đưa không được thấp hơn tổng tiền hóa đơn!')
                        return
                    nonlocal tien_khach_dua, tien_thoi_lai
                    tien_khach_dua = cash
                    tien_thoi_lai = cash - total
                    result['ok'] = True
                    popup.destroy()
                except:
                    messagebox.showerror('Lỗi', 'Nhập số hợp lệ!')
            ttk.Button(popup, text='OK', command=on_ok).pack(pady=10)
            entry_cash.focus_set()
    combobox_method.bind('<<ComboboxSelected>>', on_method_selected)

    def on_pay():
        name = entry_customer.get().strip()
        phone = entry_phone.get().strip()
        method = combobox_method.get().strip()
        cart_items, total = payment.reload_cart()
        if not name or not phone or not cart_items:
            messagebox.showwarning('Thiếu thông tin', 'Vui lòng nhập đầy đủ thông tin và có sản phẩm trong giỏ!')
            return
        if method == 'Tiền mặt':
            popup = tk.Toplevel(root)
            popup.title('Tiền khách đưa')
            popup.geometry('300x150')
            ttk.Label(popup, text=f'Tổng tiền: {total:,.0f} VND').pack(pady=5)
            cash_var = tk.StringVar()
            ttk.Label(popup, text='Tiền khách đưa:').pack()
            entry_cash = ttk.Entry(popup, textvariable=cash_var)
            entry_cash.pack(pady=5)
            result = {'ok': False}
            label_change = ttk.Label(popup, text='', font=('Arial', 11, 'bold'), foreground='blue')
            label_change.pack(pady=5)
            def calc_change(event=None):
                try:
                    cash = float(cash_var.get().replace(',', ''))
                    change = cash - total
                    if change < 0:
                        label_change.config(text=f'Thiếu {abs(change):,.0f} VND', foreground='red')
                    else:
                        label_change.config(text=f'Tiền thừa: {change:,.0f} VND', foreground='blue')
                except:
                    label_change.config(text='Nhập số hợp lệ!', foreground='red')
            entry_cash.bind('<KeyRelease>', calc_change)
            def on_ok():
                try:
                    cash = float(cash_var.get().replace(',', ''))
                    if cash < total:
                        messagebox.showerror('Lỗi', 'Tiền khách đưa không được thấp hơn tổng tiền hóa đơn!')
                        return
                    nonlocal tien_khach_dua, tien_thoi_lai
                    tien_khach_dua = cash
                    tien_thoi_lai = cash - total
                    result['ok'] = True
                    popup.destroy()
                except:
                    messagebox.showerror('Lỗi', 'Nhập số hợp lệ!')
            ttk.Button(popup, text='OK', command=on_ok).pack(pady=10)
            entry_cash.focus_set()
            root.wait_window(popup)
            if not result['ok']:
                return
        success, result = payment.process_payment(name, phone, method, cart_items, total)
        if success:
            payment.clear_cart()
            reload_cart()
            entry_customer.config(state='normal')
            entry_customer.delete(0, tk.END)
            entry_customer.config(state='readonly')
            entry_phone.delete(0, tk.END)
            combobox_method.set('')
            pdf_path = payment.export_invoice_pdf(result, tien_khach_dua, tien_thoi_lai)
            if pdf_path:
                messagebox.showinfo('Thành công', f'Thanh toán thành công! Hóa đơn đã được lưu: {pdf_path}')
                webbrowser.open(pdf_path)
            else:
                messagebox.showinfo('Thành công', f'Thanh toán thành công! (Không tạo được file hóa đơn)')
        else:
            messagebox.showerror('Lỗi', f'Thanh toán thất bại: {result}')
    btn_pay.config(command=on_pay)

    root.mainloop()

if __name__ == '__main__':
    main() 