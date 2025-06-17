import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core.order import OrderCore


class OrderView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.parent = parent
        self.db_path = db_path
        self.core = OrderCore(self.db_path)
        self.selected_order_id = None

        # Cấu hình grid cho self.frame
        self.frame.grid_rowconfigure(2, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.load_orders()

    def create_widgets(self):
        row_idx = 0

        # Tiêu đề "Quản lý đơn hàng"
        label = ttk.Label(self.frame, text='Quản lý đơn hàng', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=2, padx=20, pady=5, sticky=tk.N)
        row_idx += 1
        # Khung nút chức năng
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1 # Increment row_idx after placing button frame
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(btn_frame, text='Chi tiết đơn hàng', command=self.show_order_details).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text='Xóa đơn hàng', command=self.delete_order).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text='Làm mới', command=self.load_orders).grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)

        # Khung danh sách đơn hàng
        frame_list = ttk.LabelFrame(self.frame, padding=5)
        frame_list.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        row_idx += 1
        frame_list.grid_rowconfigure(1, weight=1) # Row 1 for Treeview to expand
        frame_list.grid_columnconfigure(0, weight=1)

        # Add a separate label for the title inside the LabelFrame
        list_title_label = ttk.Label(frame_list, text='Danh sách đơn hàng', font=("Arial", 14, "bold"))
        list_title_label.grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.N)

        columns = ('ID', 'Mã hóa đơn', 'Nhân viên', 'Khách hàng', 'Ngày', 'Tổng tiền')
        self.tree = ttk.Treeview(frame_list, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.column('ID', width=50)
        self.tree.column('Mã hóa đơn', width=100)
        self.tree.column('Nhân viên', width=150)
        self.tree.column('Khách hàng', width=150)
        self.tree.column('Ngày', width=150)
        self.tree.column('Tổng tiền', width=100)

        self.tree.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        
    def load_orders(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        orders = self.core.get_all_orders()
        for order in orders:
            self.tree.insert('', tk.END, values=order)
        self.selected_order_id = None

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            self.selected_order_id = values[0] # ID của đơn hàng

    def show_order_details(self):
        if self.selected_order_id is None:
            messagebox.showwarning("Chọn đơn hàng", "Vui lòng chọn một đơn hàng để xem chi tiết.")
            return

        details = self.core.get_order_details(self.selected_order_id)
        if not details:
            messagebox.showinfo("Chi tiết đơn hàng", "Không có chi tiết cho đơn hàng này.")
            return

        detail_window = tk.Toplevel(self.parent)
        detail_window.title(f"Chi tiết đơn hàng #{self.selected_order_id}")
        detail_window.geometry("600x400")

        detail_tree = ttk.Treeview(detail_window, columns=('STT', 'Tên hàng', 'Số lượng', 'Đơn giá', 'Thành tiền'), show='headings')
        detail_tree.heading('STT', text='STT')
        detail_tree.heading('Tên hàng', text='Tên hàng')
        detail_tree.heading('Số lượng', text='Số lượng')
        detail_tree.heading('Đơn giá', text='Đơn giá')
        detail_tree.heading('Thành tiền', text='Thành tiền')

        detail_tree.column('STT', width=50)
        detail_tree.column('Tên hàng', width=200)
        detail_tree.column('Số lượng', width=80)
        detail_tree.column('Đơn giá', width=100)
        detail_tree.column('Thành tiền', width=100)

        detail_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i, item in enumerate(details, 1):
            detail_tree.insert('', tk.END, values=(i, item.ten_hang, item.soluong, item.dongia, item.thanh_tien))

    def delete_order(self):
        if self.selected_order_id is None:
            messagebox.showwarning("Chọn đơn hàng", "Vui lòng chọn một đơn hàng để xóa.")
            return

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa đơn hàng ID: {self.selected_order_id} không?"):
            if self.core.delete_order(self.selected_order_id):
                messagebox.showinfo("Thành công", "Đơn hàng đã được xóa.")
                self.load_orders()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa đơn hàng.")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)