import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import pandas as pd
from datetime import datetime
from tkcalendar import DateEntry

class PhieuTieuHuyReportView(tk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.configure(bg="#EEF2F6")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Top filter đẹp
        frame_top = tk.Frame(self, bg="#EEF2F6")
        frame_top.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(frame_top, text="Từ ngày:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT, padx=(0, 4))
        self.entry_from = DateEntry(frame_top, width=12, font=("Segoe UI", 12), date_pattern='yyyy-mm-dd', background='#eafaf1', foreground='#222', borderwidth=2)
        self.entry_from.pack(side=tk.LEFT, padx=(0, 16))
        tk.Label(frame_top, text="Đến ngày:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT, padx=(0, 4))
        self.entry_to = DateEntry(frame_top, width=12, font=("Segoe UI", 12), date_pattern='yyyy-mm-dd', background='#eafaf1', foreground='#222', borderwidth=2)
        self.entry_to.pack(side=tk.LEFT, padx=(0, 16))
        btn_filter = tk.Button(frame_top, text="Lọc", font=("Segoe UI", 12, "bold"), bg="#eafaf1", fg="#222", activebackground="#d1f2eb", relief="flat", bd=0, padx=18, pady=6, cursor="hand2", highlightthickness=0)
        btn_filter.pack(side=tk.LEFT, padx=(0, 16))
        btn_filter.configure(command=self.on_filter)
        btn_excel = tk.Button(frame_top, text="Xuất Excel", font=("Segoe UI", 12, "bold"), bg="#eafaf1", fg="#1ca97a", activebackground="#b6f5c1", relief="flat", bd=0, padx=18, pady=6, cursor="hand2", highlightthickness=0)
        btn_excel.pack(side=tk.LEFT)
        btn_excel.configure(command=self.export_excel)
        btn_excel.bind("<Enter>", lambda e: btn_excel.configure(bg="#b6f5c1"))
        btn_excel.bind("<Leave>", lambda e: btn_excel.configure(bg="#eafaf1"))

        # Style bảng
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TieuHuy.Treeview.Heading", font=("Segoe UI", 12, "bold"), foreground="#222", background="#EEF2F6", relief="flat")
        style.configure("TieuHuy.Treeview", font=("Segoe UI", 11), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.map("TieuHuy.Treeview", background=[("selected", "#e3e8ee")], foreground=[("selected", "#232a36")])

        # Border bo tròn giả lập
        table_frame = tk.Frame(self, bg="#EEF2F6")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(0, 32))
        table_border = tk.Frame(table_frame, bg="#EEF2F6", bd=0)
        table_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        columns = ("Sản phẩm", "Biến thể", "Mã lô", "Số lượng tiêu hủy", "Giá nhập", "Tổng giá trị", "Ngày tiêu hủy", "Nhân viên", "Ghi chú")
        self.tree = ttk.Treeview(table_inner, columns=columns, show="headings", style="TieuHuy.Treeview")
        for col in columns:
            if col == "Sản phẩm":
                self.tree.heading(col, text=col, anchor=tk.W)
                self.tree.column(col, anchor=tk.W, width=180, stretch=True)
            elif col == "Biến thể":
                self.tree.heading(col, text=col, anchor=tk.W)
                self.tree.column(col, anchor=tk.W, width=180, stretch=True)
            elif col == "Ghi chú":
                self.tree.heading(col, text=col, anchor=tk.W)
                self.tree.column(col, anchor=tk.W, width=220, stretch=True)
            elif col == "Mã lô":
                self.tree.heading(col, text=col, anchor=tk.CENTER)
                self.tree.column(col, anchor=tk.CENTER, width=140)
            elif col in ("Số lượng tiêu hủy", "Giá nhập", "Tổng giá trị"):
                self.tree.heading(col, text=col, anchor=tk.CENTER)
                self.tree.column(col, anchor=tk.CENTER, width=120)
            elif col == "Ngày tiêu hủy":
                self.tree.heading(col, text=col, anchor=tk.CENTER)
                self.tree.column(col, anchor=tk.CENTER, width=150)
            elif col == "Nhân viên":
                self.tree.heading(col, text=col, anchor=tk.CENTER)
                self.tree.column(col, anchor=tk.CENTER, width=110)
            else:
                self.tree.heading(col, text=col, anchor=tk.CENTER)
                self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        # Zebra striping
        self.tree.tag_configure('oddrow', background='#fff')
        self.tree.tag_configure('evenrow', background='#f7f9fa')
        # Thanh cuộn dọc
        scrollbar = tk.Scrollbar(table_inner, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        # Thêm thanh cuộn ngang nếu bảng bị tràn
        xscroll = tk.Scrollbar(table_inner, orient=tk.HORIZONTAL, command=self.tree.xview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=xscroll.set)

    def load_data(self, from_date=None, to_date=None):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
            SELECT sp.ten, spbt.ten_bienthe, pth.ma_lo, pth.so_luong_huy, pth.gia_nhap, 
                   (pth.so_luong_huy * pth.gia_nhap) as tong_gia_tri, pth.ngay_huy, nv.ten, pth.ghi_chu
            FROM phieu_tieu_huy pth
            JOIN sanpham_bienthe spbt ON pth.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            LEFT JOIN nhanvien nv ON pth.nhanvien_id = nv.id
            WHERE 1=1
        '''
        params = []
        if from_date:
            query += " AND date(pth.ngay_huy) >= date(?)"
            params.append(from_date)
        if to_date:
            query += " AND date(pth.ngay_huy) <= date(?)"
            params.append(to_date)
        query += " ORDER BY pth.ngay_huy DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        self.current_data = []
        for row in rows:
            self.tree.insert('', tk.END, values=row)
            self.current_data.append(row)

    def on_filter(self):
        from_date = self.entry_from.get_date()
        to_date = self.entry_to.get_date()
        self.load_data(from_date or None, to_date or None)

    def export_excel(self):
        if not hasattr(self, 'current_data') or not self.current_data:
            messagebox.showwarning("Chưa có dữ liệu", "Không có dữ liệu để xuất!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(self.current_data, columns=["Sản phẩm", "Biến thể", "Mã lô", "Số lượng tiêu hủy", "Giá nhập", "Tổng giá trị", "Ngày tiêu hủy", "Nhân viên", "Ghi chú"])
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file: {file_path}")

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Báo cáo tiêu hủy lô hàng')
    root.geometry('1100x500')
    PhieuTieuHuyReportView(root)
    root.mainloop() 