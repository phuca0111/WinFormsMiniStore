import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from models.thongke_loilo_model import ThongKeLoiLoModel

class ThongKeTongHopView(tk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.model = ThongKeLoiLoModel(db_path)
        self.configure(bg="#EEF2F6")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#EEF2F6", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 12, "bold"), padding=[16, 8], background="#EEF2F6", foreground="#232a36")
        style.map("TNotebook.Tab", background=[("selected", "#fff")], foreground=[("selected", "#1ca97a")])
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#eafaf1")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")
        style.configure("TCombobox", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff", fieldbackground="#fff")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        # Tạo các tab với frame nền #eef2f6
        def pastel_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=8, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        # Tab 1: Biểu đồ doanh thu
        frame_doanhthu = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_doanhthu, text="Biểu đồ doanh thu")
        filter_frame = tk.Frame(frame_doanhthu, bg="#EEF2F6")
        filter_frame.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(filter_frame, text="Thống kê theo:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT)
        self.combo_type_dt = ttk.Combobox(filter_frame, values=["Ngày", "Tháng", "Năm"], state="readonly", width=10, font=("Segoe UI", 12))
        self.combo_type_dt.current(0)
        self.combo_type_dt.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        btn_xem_dt = tk.Button(filter_frame, text="Xem", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_xem_dt, "#eafaf1", "#b6f5c1")
        btn_xem_dt.pack(side=tk.LEFT, padx=8)
        btn_xem_dt.configure(command=self.load_doanhthu_chart)
        self.frame_chart_dt = tk.Frame(frame_doanhthu, bg="#EEF2F6")
        self.frame_chart_dt.pack(fill=tk.BOTH, expand=True)
        self.load_doanhthu_chart()
        # Tab 2: Biểu đồ lợi nhuận
        frame_loinhuan = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_loinhuan, text="Biểu đồ lợi nhuận")
        filter_frame2 = tk.Frame(frame_loinhuan, bg="#EEF2F6")
        filter_frame2.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(filter_frame2, text="Thống kê theo:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT)
        self.combo_type_ln = ttk.Combobox(filter_frame2, values=["Ngày", "Tháng", "Năm"], state="readonly", width=10, font=("Segoe UI", 12))
        self.combo_type_ln.current(0)
        self.combo_type_ln.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        btn_xem_ln = tk.Button(filter_frame2, text="Xem", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_xem_ln, "#f9e7cf", "#f6cba3")
        btn_xem_ln.pack(side=tk.LEFT, padx=8)
        btn_xem_ln.configure(command=self.load_loinhuan_chart)
        self.frame_chart_ln = tk.Frame(frame_loinhuan, bg="#EEF2F6")
        self.frame_chart_ln.pack(fill=tk.BOTH, expand=True)
        self.load_loinhuan_chart()
        # Tab 3: Biểu đồ tồn kho
        frame_tonkho = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_tonkho, text="Biểu đồ tồn kho")
        filter_frame_tk = tk.Frame(frame_tonkho, bg="#EEF2F6")
        filter_frame_tk.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(filter_frame_tk, text="Kiểu thống kê:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT)
        self.combo_type_tk = ttk.Combobox(filter_frame_tk, values=["Theo sản phẩm", "Theo biến thể"], state="readonly", width=15, font=("Segoe UI", 12))
        self.combo_type_tk.current(0)
        self.combo_type_tk.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        btn_xem_tk = tk.Button(filter_frame_tk, text="Xem", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_xem_tk, "#eafaf1", "#b6f5c1")
        btn_xem_tk.pack(side=tk.LEFT, padx=8)
        btn_xem_tk.configure(command=self.load_tonkho_chart)
        self.frame_chart_tk = tk.Frame(frame_tonkho, bg="#EEF2F6")
        self.frame_chart_tk.pack(fill=tk.BOTH, expand=True)
        self.load_tonkho_chart()
        # Tab 4: Biểu đồ bán chạy
        frame_banchay = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_banchay, text="Biểu đồ bán chạy")
        filter_frame_bc = tk.Frame(frame_banchay, bg="#EEF2F6")
        filter_frame_bc.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(filter_frame_bc, text="Top:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT, padx=5)
        self.combo_top_bc = ttk.Combobox(filter_frame_bc, values=[5, 10], state="readonly", width=5, font=("Segoe UI", 12))
        self.combo_top_bc.current(0)
        self.combo_top_bc.pack(side=tk.LEFT, padx=5)
        tk.Label(filter_frame_bc, text="Loại biểu đồ:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT, padx=5)
        self.combo_chart_bc = ttk.Combobox(filter_frame_bc, values=["Cột", "Tròn"], state="readonly", width=7, font=("Segoe UI", 12))
        self.combo_chart_bc.current(0)
        self.combo_chart_bc.pack(side=tk.LEFT, padx=5)
        btn_xem_bc = tk.Button(filter_frame_bc, text="Xem", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_xem_bc, "#eafaf1", "#b6f5c1")
        btn_xem_bc.pack(side=tk.LEFT, padx=5)
        btn_xem_bc.configure(command=self.load_banchay_chart)
        self.frame_chart_bc = tk.Frame(frame_banchay, bg="#EEF2F6")
        self.frame_chart_bc.pack(fill=tk.BOTH, expand=True)
        self.load_banchay_chart()
        # Tab 5: Biểu đồ sắp hết hạn
        frame_hethan = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_hethan, text="Biểu đồ sắp hết hạn")
        filter_frame_he = tk.Frame(frame_hethan, bg="#EEF2F6")
        filter_frame_he.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(filter_frame_he, text="Sắp hết hạn trong (ngày):", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT, padx=5)
        self.combo_days_he = ttk.Combobox(filter_frame_he, values=[7, 15, 30], state="readonly", width=5, font=("Segoe UI", 12))
        self.combo_days_he.current(0)
        self.combo_days_he.pack(side=tk.LEFT, padx=5)
        btn_xem_he = tk.Button(filter_frame_he, text="Xem", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_xem_he, "#eafaf1", "#b6f5c1")
        btn_xem_he.pack(side=tk.LEFT, padx=5)
        btn_xem_he.configure(command=self.load_hethan_chart)
        self.frame_chart_he = tk.Frame(frame_hethan, bg="#EEF2F6")
        self.frame_chart_he.pack(fill=tk.BOTH, expand=True)
        self.load_hethan_chart()
        # Tab 6: Cảnh báo sắp hết hạn
        frame_canhbao = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_canhbao, text="Cảnh báo sắp hết hạn")
        filter_frame_cb = tk.Frame(frame_canhbao, bg="#EEF2F6")
        filter_frame_cb.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(filter_frame_cb, text="Cảnh báo sản phẩm sắp hết hạn trước:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT, padx=5)
        self.combo_days_cb = ttk.Combobox(filter_frame_cb, values=[7, 15, 30], state="readonly", width=5, font=("Segoe UI", 12))
        self.combo_days_cb.current(0)
        self.combo_days_cb.pack(side=tk.LEFT, padx=5)
        btn_xem = tk.Button(filter_frame_cb, text="Xem", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_xem, "#eafaf1", "#b6f5c1")
        btn_xem.pack(side=tk.LEFT, padx=5)
        btn_xem.configure(command=self.load_canhbao_table)
        columns = ("Sản phẩm", "Biến thể", "Hạn sử dụng", "Số lượng còn lại", "Kệ")
        self.tree_canhbao = ttk.Treeview(frame_canhbao, columns=columns, show="headings")
        for col in columns:
            self.tree_canhbao.heading(col, text=col)
            self.tree_canhbao.column(col, anchor=tk.CENTER, width=150)
        self.tree_canhbao.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_canhbao_table()
        # Tab 7: Bảng lãi/lỗ
        frame_loilo = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_loilo, text="Bảng lãi/lỗ")
        filter_frame_loilo = tk.Frame(frame_loilo, bg="#EEF2F6")
        filter_frame_loilo.pack(fill=tk.X, pady=16, padx=32)
        tk.Label(filter_frame_loilo, text="Thống kê theo:", font=("Segoe UI", 12), bg="#EEF2F6").pack(side=tk.LEFT)
        self.combo_type_loilo = ttk.Combobox(filter_frame_loilo, values=["Ngày", "Tuần", "Tháng", "Năm"], state="readonly", width=10, font=("Segoe UI", 12))
        self.combo_type_loilo.current(0)
        self.combo_type_loilo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        btn_xem_loilo = tk.Button(filter_frame_loilo, text="Xem", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_xem_loilo, "#eafaf1", "#b6f5c1")
        btn_xem_loilo.pack(side=tk.LEFT, padx=8)
        btn_xem_loilo.configure(command=self.load_loilo_table)
        columns_loilo = ("Thời gian", "Doanh thu", "Chi phí nhập", "Lời", "Lỗ")
        self.tree_loilo = ttk.Treeview(frame_loilo, columns=columns_loilo, show="headings")
        for col in columns_loilo:
            self.tree_loilo.heading(col, text=col)
            self.tree_loilo.column(col, anchor=tk.CENTER, width=120)
        self.tree_loilo.pack(fill=tk.BOTH, expand=True)
        self.load_loilo_table()
        # Tab 8: Bảng bán hàng
        frame_banhang = tk.Frame(self.notebook, bg="#EEF2F6")
        self.notebook.add(frame_banhang, text="Bảng bán hàng")
        columns_bh = ("Ngày", "Sản phẩm", "Số lượng", "Doanh thu", "Khách hàng")
        self.tree_banhang = ttk.Treeview(frame_banhang, columns=columns_bh, show="headings")
        for col in columns_bh:
            self.tree_banhang.heading(col, text=col)
            self.tree_banhang.column(col, anchor=tk.CENTER, width=140)
        self.tree_banhang.pack(fill=tk.BOTH, expand=True)
        btn_reload_bh = tk.Button(frame_banhang, text="Tải lại bảng bán hàng", font=("Segoe UI", 12, "bold"))
        pastel_btn(btn_reload_bh, "#eafaf1", "#b6f5c1")
        btn_reload_bh.pack(pady=5)
        btn_reload_bh.configure(command=self.load_banhang_data)
        self.load_banhang_data()

    def _load_chart(self, frame, data_func, title, chart_title, y_label, color='blue'):
        for widget in frame.winfo_children():
            widget.destroy()
        data = data_func(self.combo_type_dt.get().lower())
        if not data:
            ttk.Label(frame, text="Không có dữ liệu").pack()
            return
        thoigian = [str(row[0]) for row in data]
        data_values = [row[1] for row in data]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(thoigian, data_values, marker='o', color=color, label=title)
        ax.set_title(chart_title)
        ax.set_xlabel('Thời gian')
        ax.set_ylabel(y_label)
        ax.grid(True)
        ax.legend()
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_doanhthu_data(self, kieu):
        return self.model.get_doanhthu_data(kieu)

    def get_loinhuan_data(self, kieu):
        return self.model.get_loinhuan_data(kieu)

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

    def get_banchay_data(self, top_n):
        return self.model.get_banchay_data(top_n)

    def get_hethan_data(self, days):
        return self.model.get_hethan_data(days)

    def get_loilo_data(self, kieu):
        return self.model.get_loilo_data(kieu)

    def load_loilo_table(self):
        self.tree_loilo.delete(*self.tree_loilo.get_children())
        kieu = self.combo_type_loilo.get().lower()
        data = self.get_loilo_data(kieu)
        for row in data:
            self.tree_loilo.insert('', tk.END, values=row)

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

    def load_doanhthu_chart(self):
        self._load_chart(self.frame_chart_dt, self.get_doanhthu_data, 'Doanh thu', 'Biểu đồ doanh thu theo thời gian', 'Doanh thu (VNĐ)')

    def load_loinhuan_chart(self):
        self._load_chart(self.frame_chart_ln, self.get_loinhuan_data, 'Lợi nhuận', 'Biểu đồ lợi nhuận theo thời gian', 'Lợi nhuận (VNĐ)', color='green')

    def load_tonkho_chart(self):
        # Tồn kho là biểu đồ cột
        for widget in self.frame_chart_tk.winfo_children():
            widget.destroy()
        kieu = self.combo_type_tk.get()
        data = self.get_tonkho_data(kieu)
        if not data:
            tk.Label(self.frame_chart_tk, text="Không có dữ liệu", bg="#EEF2F6").pack()
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

    def load_banchay_chart(self):
        for widget in self.frame_chart_bc.winfo_children():
            widget.destroy()
        top_n = int(self.combo_top_bc.get())
        chart_type = self.combo_chart_bc.get()
        data = self.get_banchay_data(top_n)
        if not data:
            tk.Label(self.frame_chart_bc, text="Không có dữ liệu", bg="#EEF2F6").pack()
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

    def load_hethan_chart(self):
        for widget in self.frame_chart_he.winfo_children():
            widget.destroy()
        days = int(self.combo_days_he.get())
        data = self.get_hethan_data(days)
        if not data:
            tk.Label(self.frame_chart_he, text="Không có dữ liệu", bg="#EEF2F6").pack()
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