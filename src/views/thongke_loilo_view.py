import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from models.thongke_loilo_model import ThongKeLoiLoModel

class ThongKeTongHopView(ttk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.model = ThongKeLoiLoModel(db_path)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        # Tab 1: Biểu đồ doanh thu
        frame_doanhthu = ttk.Frame(self.notebook)
        self.notebook.add(frame_doanhthu, text="Biểu đồ doanh thu")
        self._add_doanhthu_tab(frame_doanhthu)
        # Tab 2: Biểu đồ lợi nhuận
        frame_loinhuan = ttk.Frame(self.notebook)
        self.notebook.add(frame_loinhuan, text="Biểu đồ lợi nhuận")
        self._add_loinhuan_tab(frame_loinhuan)
        # Tab 3: Biểu đồ tồn kho
        frame_tonkho = ttk.Frame(self.notebook)
        self.notebook.add(frame_tonkho, text="Biểu đồ tồn kho")
        self._add_tonkho_tab(frame_tonkho)
        # Tab 4: Biểu đồ bán chạy
        frame_banchay = ttk.Frame(self.notebook)
        self.notebook.add(frame_banchay, text="Biểu đồ bán chạy")
        self._add_banchay_tab(frame_banchay)
        # Tab 5: Biểu đồ sắp hết hạn
        frame_hethan = ttk.Frame(self.notebook)
        self.notebook.add(frame_hethan, text="Biểu đồ sắp hết hạn")
        self._add_hethan_tab(frame_hethan)
        # Tab 6: Cảnh báo sắp hết hạn
        frame_canhbao = ttk.Frame(self.notebook)
        self.notebook.add(frame_canhbao, text="Cảnh báo sắp hết hạn")
        self._add_canhbao_tab(frame_canhbao)
        # Tab 7: Bảng lãi/lỗ
        frame_loilo = ttk.Frame(self.notebook)
        self.notebook.add(frame_loilo, text="Bảng lãi/lỗ")
        self._add_loilo_table_tab(frame_loilo)
        # Tab 8: Bảng bán hàng
        frame_banhang = ttk.Frame(self.notebook)
        self.notebook.add(frame_banhang, text="Bảng bán hàng")
        self._add_banhang_table_tab(frame_banhang)

    # --- Tab Doanh thu ---
    def _add_doanhthu_tab(self, frame):
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Thống kê theo:").pack(side=tk.LEFT, padx=5)
        self.combo_type_dt = ttk.Combobox(filter_frame, values=["Ngày", "Tháng", "Năm"], state="readonly", width=10)
        self.combo_type_dt.current(0)
        self.combo_type_dt.pack(side=tk.LEFT, padx=5)
        btn_xem_dt = ttk.Button(filter_frame, text="Xem", command=self.load_doanhthu_chart)
        btn_xem_dt.pack(side=tk.LEFT, padx=5)
        self.frame_chart_dt = ttk.Frame(frame)
        self.frame_chart_dt.pack(fill=tk.BOTH, expand=True)
        self.load_doanhthu_chart()

    def load_doanhthu_chart(self):
        for widget in self.frame_chart_dt.winfo_children():
            widget.destroy()
        kieu = self.combo_type_dt.get().lower()
        data = self.get_doanhthu_data(kieu)
        if not data:
            ttk.Label(self.frame_chart_dt, text="Không có dữ liệu").pack()
            return
        thoigian = [str(row[0]) for row in data]
        doanh_thu = [row[1] for row in data]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(thoigian, doanh_thu, marker='o', color='blue', label='Doanh thu')
        ax.set_title('Biểu đồ doanh thu theo thời gian')
        ax.set_xlabel('Thời gian')
        ax.set_ylabel('Doanh thu (VNĐ)')
        ax.grid(True)
        ax.legend()
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart_dt)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_doanhthu_data(self, kieu):
        return self.model.get_doanhthu_data(kieu)

    # --- Tab Lợi nhuận ---
    def _add_loinhuan_tab(self, frame):
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Thống kê theo:").pack(side=tk.LEFT, padx=5)
        self.combo_type_ln = ttk.Combobox(filter_frame, values=["Ngày", "Tháng", "Năm"], state="readonly", width=10)
        self.combo_type_ln.current(0)
        self.combo_type_ln.pack(side=tk.LEFT, padx=5)
        btn_xem_ln = ttk.Button(filter_frame, text="Xem", command=self.load_loinhuan_chart)
        btn_xem_ln.pack(side=tk.LEFT, padx=5)
        self.frame_chart_ln = ttk.Frame(frame)
        self.frame_chart_ln.pack(fill=tk.BOTH, expand=True)
        self.load_loinhuan_chart()

    def load_loinhuan_chart(self):
        for widget in self.frame_chart_ln.winfo_children():
            widget.destroy()
        kieu = self.combo_type_ln.get().lower()
        data = self.get_loinhuan_data(kieu)
        if not data:
            ttk.Label(self.frame_chart_ln, text="Không có dữ liệu").pack()
            return
        thoigian = [str(row[0]) for row in data]
        loinhuan = [row[1] for row in data]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(thoigian, loinhuan, marker='o', color='green', label='Lợi nhuận')
        ax.set_title('Biểu đồ lợi nhuận theo thời gian')
        ax.set_xlabel('Thời gian')
        ax.set_ylabel('Lợi nhuận (VNĐ)')
        ax.grid(True)
        ax.legend()
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart_ln)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_loinhuan_data(self, kieu):
        return self.model.get_loinhuan_data(kieu)

    # --- Tab Tồn kho ---
    def _add_tonkho_tab(self, frame):
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Kiểu thống kê:").pack(side=tk.LEFT, padx=5)
        self.combo_type_tk = ttk.Combobox(filter_frame, values=["Theo sản phẩm", "Theo biến thể"], state="readonly", width=15)
        self.combo_type_tk.current(0)
        self.combo_type_tk.pack(side=tk.LEFT, padx=5)
        btn_xem_tk = ttk.Button(filter_frame, text="Xem", command=self.load_tonkho_chart)
        btn_xem_tk.pack(side=tk.LEFT, padx=5)
        self.frame_chart_tk = ttk.Frame(frame)
        self.frame_chart_tk.pack(fill=tk.BOTH, expand=True)
        self.load_tonkho_chart()

    def load_tonkho_chart(self):
        for widget in self.frame_chart_tk.winfo_children():
            widget.destroy()
        kieu = self.combo_type_tk.get()
        data = self.get_tonkho_data(kieu)
        if not data:
            ttk.Label(self.frame_chart_tk, text="Không có dữ liệu").pack()
            return
        ten = [row[0] for row in data]
        so_luong = [row[1] for row in data]
        fig, ax = plt.subplots(figsize=(max(8, len(ten)*0.7), 5))
        ax.bar(ten, so_luong, color="#4a90e2")
        ax.set_ylabel("Số lượng tồn kho")
        ax.set_title(f"Tồn kho theo {'biến thể' if kieu=='Theo biến thể' else 'sản phẩm'}")
        for i, v in enumerate(so_luong):
            ax.text(i, v, str(v), ha='center', va='bottom')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart_tk)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_tonkho_data(self, kieu):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if kieu == "Theo sản phẩm":
            cursor.execute('''
                SELECT sp.ten, SUM(nsp.so_luong_con_lai)
                FROM nhacungcap_sanpham nsp
                JOIN sanpham_bienthe spbt ON nsp.bienthe_id = spbt.id
                JOIN sanpham sp ON spbt.sanpham_id = sp.id
                WHERE nsp.so_luong_con_lai > 0
                GROUP BY sp.id
            ''')
            rows = cursor.fetchall()
        else:
            cursor.execute('''
                SELECT sp.ten || ' - ' || spbt.ten_bienthe, SUM(nsp.so_luong_con_lai)
                FROM nhacungcap_sanpham nsp
                JOIN sanpham_bienthe spbt ON nsp.bienthe_id = spbt.id
                JOIN sanpham sp ON spbt.sanpham_id = sp.id
                WHERE nsp.so_luong_con_lai > 0
                GROUP BY spbt.id
            ''')
            rows = cursor.fetchall()
        conn.close()
        return rows

    # --- Tab Bán chạy ---
    def _add_banchay_tab(self, frame):
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Top:").pack(side=tk.LEFT, padx=5)
        self.combo_top_bc = ttk.Combobox(filter_frame, values=[5, 10], state="readonly", width=5)
        self.combo_top_bc.current(0)
        self.combo_top_bc.pack(side=tk.LEFT, padx=5)
        ttk.Label(filter_frame, text="Loại biểu đồ:").pack(side=tk.LEFT, padx=5)
        self.combo_chart_bc = ttk.Combobox(filter_frame, values=["Cột", "Tròn"], state="readonly", width=7)
        self.combo_chart_bc.current(0)
        self.combo_chart_bc.pack(side=tk.LEFT, padx=5)
        btn_xem_bc = ttk.Button(filter_frame, text="Xem", command=self.load_banchay_chart)
        btn_xem_bc.pack(side=tk.LEFT, padx=5)
        self.frame_chart_bc = ttk.Frame(frame)
        self.frame_chart_bc.pack(fill=tk.BOTH, expand=True)
        self.load_banchay_chart()

    def load_banchay_chart(self):
        for widget in self.frame_chart_bc.winfo_children():
            widget.destroy()
        top_n = int(self.combo_top_bc.get())
        chart_type = self.combo_chart_bc.get()
        data = self.get_banchay_data(top_n)
        if not data:
            ttk.Label(self.frame_chart_bc, text="Không có dữ liệu").pack()
            return
        ten_sp = [row[0] for row in data]
        so_luong = [row[1] for row in data]
        fig, ax = plt.subplots(figsize=(8, 6))
        if chart_type == "Cột":
            ax.bar(ten_sp, so_luong, color="#4a90e2")
            ax.set_ylabel("Số lượng bán ra")
            ax.set_title(f"Top {top_n} sản phẩm bán chạy")
            for i, v in enumerate(so_luong):
                ax.text(i, v, str(v), ha='center', va='bottom')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        else:
            ax.pie(so_luong, labels=ten_sp, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Tỷ lệ top {top_n} sản phẩm bán chạy")
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart_bc)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_banchay_data(self, top_n):
        return self.model.get_banchay_data(top_n)

    # --- Tab Sắp hết hạn ---
    def _add_hethan_tab(self, frame):
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Sắp hết hạn trong (ngày):").pack(side=tk.LEFT, padx=5)
        self.combo_days_he = ttk.Combobox(filter_frame, values=[7, 15, 30], state="readonly", width=5)
        self.combo_days_he.current(0)
        self.combo_days_he.pack(side=tk.LEFT, padx=5)
        btn_xem_he = ttk.Button(filter_frame, text="Xem", command=self.load_hethan_chart)
        btn_xem_he.pack(side=tk.LEFT, padx=5)
        self.frame_chart_he = ttk.Frame(frame)
        self.frame_chart_he.pack(fill=tk.BOTH, expand=True)
        self.load_hethan_chart()

    def load_hethan_chart(self):
        for widget in self.frame_chart_he.winfo_children():
            widget.destroy()
        days = int(self.combo_days_he.get())
        data = self.get_hethan_data(days)
        if not data:
            ttk.Label(self.frame_chart_he, text="Không có dữ liệu").pack()
            return
        ten_sp = [row[0] for row in data]
        so_luong = [row[1] for row in data]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(ten_sp, so_luong, color="#e26a4a")
        ax.set_ylabel("Số lượng sắp hết hạn")
        ax.set_title(f"Sản phẩm/lô sắp hết hạn trong {days} ngày tới")
        for i, v in enumerate(so_luong):
            ax.text(i, v, str(v), ha='center', va='bottom')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart_he)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_hethan_data(self, days):
        return self.model.get_hethan_data(days)

    def _add_loilo_table_tab(self, frame):
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Thống kê theo:").pack(side=tk.LEFT, padx=5)
        self.combo_type_loilo = ttk.Combobox(filter_frame, values=["Ngày", "Tuần", "Tháng", "Năm"], state="readonly", width=10)
        self.combo_type_loilo.current(0)
        self.combo_type_loilo.pack(side=tk.LEFT, padx=5)
        btn_xem = ttk.Button(filter_frame, text="Xem", command=self.load_loilo_table)
        btn_xem.pack(side=tk.LEFT, padx=5)
        columns = ("Thời gian", "Doanh thu", "Chi phí nhập", "Lời", "Lỗ")
        self.tree_loilo = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_loilo.heading(col, text=col)
            self.tree_loilo.column(col, anchor=tk.CENTER, width=120)
        self.tree_loilo.pack(fill=tk.BOTH, expand=True)
        self.load_loilo_table()

    def load_loilo_table(self):
        self.tree_loilo.delete(*self.tree_loilo.get_children())
        kieu = self.combo_type_loilo.get().lower()
        data = self.get_loilo_data(kieu)
        for row in data:
            self.tree_loilo.insert('', tk.END, values=row)

    def get_loilo_data(self, kieu):
        return self.model.get_loilo_data(kieu)

    def _add_banhang_table_tab(self, frame):
        columns_bh = ("Ngày", "Sản phẩm", "Số lượng", "Doanh thu", "Khách hàng")
        self.tree_banhang = ttk.Treeview(frame, columns=columns_bh, show="headings")
        for col in columns_bh:
            self.tree_banhang.heading(col, text=col)
            self.tree_banhang.column(col, anchor=tk.CENTER, width=140)
        self.tree_banhang.pack(fill=tk.BOTH, expand=True)
        btn_reload_bh = ttk.Button(frame, text="Tải lại bảng bán hàng", command=self.load_banhang_data)
        btn_reload_bh.pack(pady=5)
        self.load_banhang_data()

    def load_banhang_data(self):
        self.tree_banhang.delete(*self.tree_banhang.get_children())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT hd.ngay, sp.ten, hdct.soluong, hdct.soluong * hdct.dongia, IFNULL(kh.ten, '')
            FROM hoadon_chitiet hdct
            JOIN hoadon hd ON hdct.hoadon_id = hd.id
            JOIN sanpham_bienthe spbt ON hdct.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            LEFT JOIN khachhang kh ON hd.khachhang_id = kh.id
            ORDER BY hd.ngay DESC, hd.id DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.tree_banhang.insert('', tk.END, values=row)

    def _add_canhbao_tab(self, frame):
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Cảnh báo sản phẩm sắp hết hạn trước:").pack(side=tk.LEFT, padx=5)
        self.combo_days_cb = ttk.Combobox(filter_frame, values=[7, 15, 30], state="readonly", width=5)
        self.combo_days_cb.current(0)
        self.combo_days_cb.pack(side=tk.LEFT, padx=5)
        btn_xem = ttk.Button(filter_frame, text="Xem", command=self.load_canhbao_table)
        btn_xem.pack(side=tk.LEFT, padx=5)
        columns = ("Sản phẩm", "Biến thể", "Hạn sử dụng", "Số lượng còn lại", "Kệ")
        self.tree_canhbao = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_canhbao.heading(col, text=col)
            self.tree_canhbao.column(col, anchor=tk.CENTER, width=150)
        self.tree_canhbao.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_canhbao_table()

    def load_canhbao_table(self):
        self.tree_canhbao.delete(*self.tree_canhbao.get_children())
        days = int(self.combo_days_cb.get())
        data = self.get_expiry_data(days)
        for row in data:
            self.tree_canhbao.insert('', tk.END, values=row)

    def get_expiry_data(self, days):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        from datetime import datetime, timedelta
        today = datetime.now().date()
        future = today + timedelta(days=days)
        query = '''
            SELECT sp.ten, spbt.ten_bienthe, nsp.han_su_dung, nsp.so_luong_con_lai, k.ten, nsp.id
            FROM nhacungcap_sanpham nsp
            JOIN sanpham_bienthe spbt ON nsp.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            LEFT JOIN kehang_sanpham ks ON ks.bienthe_id = spbt.id
            LEFT JOIN kehang k ON ks.kehang_id = k.id
            WHERE nsp.so_luong_con_lai > 0
                AND nsp.han_su_dung IS NOT NULL
                AND nsp.han_su_dung != ''
            ORDER BY nsp.han_su_dung ASC, nsp.id ASC
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        filtered = []
        ids_seen = set()
        for r in rows:
            try:
                han = datetime.strptime(r[2], '%Y-%m-%d').date()
                if today <= han <= future:
                    # Đảm bảo không bị trùng lô (nếu có nhiều kệ, chỉ lấy lô đầu tiên)
                    if r[5] not in ids_seen:
                        filtered.append((r[0], r[1], r[2], r[3], r[4] if r[4] else ''))
                        ids_seen.add(r[5])
            except Exception as e:
                pass
        return filtered 