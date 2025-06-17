import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ThongKeLoiLoView(ttk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data('ngay')

    def create_widgets(self):
        # Chọn kiểu thống kê
        frame_top = ttk.Frame(self)
        frame_top.pack(fill=tk.X, pady=5)
        ttk.Label(frame_top, text="Thống kê lời lỗ theo:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.combo_type = ttk.Combobox(frame_top, values=["Ngày", "Tuần", "Tháng", "Năm"], state="readonly", width=10)
        self.combo_type.current(0)
        self.combo_type.pack(side=tk.LEFT, padx=5)
        btn_xem = ttk.Button(frame_top, text="Xem", command=self.on_xem)
        btn_xem.pack(side=tk.LEFT, padx=5)
        btn_excel = ttk.Button(frame_top, text="Xuất Excel", command=self.export_excel)
        btn_excel.pack(side=tk.LEFT, padx=5)
        btn_chart = ttk.Button(frame_top, text="Hiển thị biểu đồ", command=self.show_chart_window)
        btn_chart.pack(side=tk.LEFT, padx=5)

        # Bảng dữ liệu
        columns = ("Thời gian", "Doanh thu", "Chi phí nhập", "Lời", "Lỗ")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def on_xem(self):
        kieu = self.combo_type.get().lower()
        self.load_data(kieu)

    def load_data(self, kieu):
        self.tree.delete(*self.tree.get_children())
        data = self.get_loilo_data(kieu)
        for row in data:
            self.tree.insert('', tk.END, values=row)
        self.current_data = data

    def get_loilo_data(self, kieu):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if kieu == 'ngày':
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
        elif kieu == 'tháng':
            group = "strftime('%Y-%m', hd.ngay)"
            select = "strftime('%Y-%m', hd.ngay)"
        elif kieu == 'năm':
            group = "strftime('%Y', hd.ngay)"
            select = "strftime('%Y', hd.ngay)"
        elif kieu == 'tuần':
            group = "strftime('%Y-%W', hd.ngay)"
            select = "strftime('%Y-%W', hd.ngay)"
        else:
            group = "DATE(hd.ngay)"
            select = "DATE(hd.ngay)"
        query = f'''
            SELECT {select} as thoigian,
                IFNULL(SUM(hdct.soluong * hdct.dongia), 0) AS doanh_thu,
                IFNULL(SUM(hdct.soluong * hdct.gia_nhap), 0) AS chi_phi_nhap,
                CASE 
                    WHEN (IFNULL(SUM(hdct.soluong * hdct.dongia), 0) - IFNULL(SUM(hdct.soluong * hdct.gia_nhap), 0)) > 0 
                    THEN (IFNULL(SUM(hdct.soluong * hdct.dongia), 0) - IFNULL(SUM(hdct.soluong * hdct.gia_nhap), 0)) 
                    ELSE 0 
                END AS loi,
                CASE 
                    WHEN (IFNULL(SUM(hdct.soluong * hdct.dongia), 0) - IFNULL(SUM(hdct.soluong * hdct.gia_nhap), 0)) < 0 
                    THEN (IFNULL(SUM(hdct.soluong * hdct.dongia), 0) - IFNULL(SUM(hdct.soluong * hdct.gia_nhap), 0)) 
                    ELSE 0 
                END AS lo
            FROM hoadon hd
            LEFT JOIN hoadon_chitiet hdct ON hd.id = hdct.hoadon_id
            GROUP BY {group}
            ORDER BY {group} DESC
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def export_excel(self):
        if not hasattr(self, 'current_data') or not self.current_data:
            messagebox.showwarning("Chưa có dữ liệu", "Không có dữ liệu để xuất!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(self.current_data, columns=["Thời gian", "Doanh thu", "Chi phí nhập", "Lời", "Lỗ"])
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file: {file_path}")

    def show_chart_window(self):
        if not hasattr(self, 'current_data') or not self.current_data:
            messagebox.showwarning("Chưa có dữ liệu", "Không có dữ liệu để vẽ biểu đồ!")
            return
        chart_win = tk.Toplevel(self)
        chart_win.title("Biểu đồ thống kê lời/lỗ")
        chart_win.geometry("800x500")
        # Chọn loại biểu đồ
        chart_type = tk.StringVar(value="bar")
        def draw_chart():
            for widget in chart_frame.winfo_children():
                widget.destroy()
            fig, ax = plt.subplots(figsize=(7,4))
            thoigian = [str(row[0]) for row in self.current_data]
            loi = [row[3] for row in self.current_data]
            lo = [abs(row[4]) for row in self.current_data]
            if chart_type.get() == "bar":
                ax.bar(thoigian, loi, label="Lời", color="green")
                ax.bar(thoigian, lo, label="Lỗ", color="red", bottom=loi)
                ax.set_ylabel("Số tiền")
                ax.set_xlabel("Thời gian")
                ax.set_title("Biểu đồ cột: Lời/Lỗ theo thời gian")
                ax.legend()
            else:
                # Biểu đồ tròn tổng lời/lỗ
                total_loi = sum(loi)
                total_lo = sum(lo)
                labels = []
                sizes = []
                colors = []
                if total_loi > 0:
                    labels.append("Lời")
                    sizes.append(total_loi)
                    colors.append("green")
                if total_lo > 0:
                    labels.append("Lỗ")
                    sizes.append(total_lo)
                    colors.append("red")
                ax.pie(sizes, labels=labels, autopct='%1.2f%%', colors=colors, startangle=90)
                ax.set_title("Biểu đồ tròn: Tỷ lệ lời/lỗ")
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # Giao diện chọn loại biểu đồ
        top_frame = ttk.Frame(chart_win)
        top_frame.pack(fill=tk.X, pady=5)
        ttk.Label(top_frame, text="Chọn loại biểu đồ:").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(top_frame, text="Biểu đồ cột", variable=chart_type, value="bar", command=draw_chart).pack(side=tk.LEFT)
        ttk.Radiobutton(top_frame, text="Biểu đồ tròn", variable=chart_type, value="pie", command=draw_chart).pack(side=tk.LEFT)
        chart_frame = ttk.Frame(chart_win)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        draw_chart() 