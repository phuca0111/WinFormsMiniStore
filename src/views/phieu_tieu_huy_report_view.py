import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import pandas as pd
from datetime import datetime

class PhieuTieuHuyReportView(ttk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_top = ttk.Frame(self)
        frame_top.pack(fill=tk.X, pady=5)
        ttk.Label(frame_top, text="Từ ngày:").pack(side=tk.LEFT, padx=5)
        self.entry_from = ttk.Entry(frame_top, width=12)
        self.entry_from.pack(side=tk.LEFT)
        ttk.Label(frame_top, text="Đến ngày:").pack(side=tk.LEFT, padx=5)
        self.entry_to = ttk.Entry(frame_top, width=12)
        self.entry_to.pack(side=tk.LEFT)
        btn_filter = ttk.Button(frame_top, text="Lọc", command=self.on_filter)
        btn_filter.pack(side=tk.LEFT, padx=5)
        btn_excel = ttk.Button(frame_top, text="Xuất Excel", command=self.export_excel)
        btn_excel.pack(side=tk.LEFT, padx=5)

        columns = ("Sản phẩm", "Biến thể", "Mã lô", "Số lượng tiêu hủy", "Giá nhập", "Tổng giá trị", "Ngày tiêu hủy", "Nhân viên", "Ghi chú")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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
        from_date = self.entry_from.get().strip()
        to_date = self.entry_to.get().strip()
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