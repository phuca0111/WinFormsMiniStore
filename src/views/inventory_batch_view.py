import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox
from datetime import datetime

class InventoryBatchView(ttk.Frame):
    def __init__(self, parent, db_path='Database/ministore_db.sqlite'):
        super().__init__(parent)
        self.db_path = db_path
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Style đẹp cho bảng
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading",
            background="#fff", foreground="#232a36", font=("Segoe UI", 13, "bold"),
            borderwidth=0, relief="flat"
        )
        style.configure("Custom.Treeview",
            font=("Segoe UI", 12),
            rowheight=36,
            background="#fff",
            fieldbackground="#fff",
            borderwidth=0,
            relief="flat"
        )
        style.map("Custom.Treeview",
            background=[("selected", "#e3e8ee")],
            foreground=[("selected", "#232a36")]
        )
        # Zebra striping
        # Border bo tròn giả lập
        table_frame = tk.Frame(self, bg="#F5F7FA")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(32, 32))
        table_border = tk.Frame(table_frame, bg="#EEF2F6", bd=0)
        table_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        columns = ("Sản phẩm", "Biến thể", "Mã lô", "Ngày nhập", "Hạn sử dụng", "Số lượng còn lại", "Tiêu hủy")
        self.tree = ttk.Treeview(table_inner, columns=columns, show="headings", style="Custom.Treeview")
        for col in columns:
            anchor = tk.W if col in ("Sản phẩm", "Biến thể", "Mã lô") else tk.CENTER
            self.tree.heading(col, text=col, anchor=anchor)
            self.tree.column(col, anchor=anchor, width=180 if col in ("Sản phẩm", "Biến thể", "Mã lô") else 140, stretch=True)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8, side=tk.LEFT)
        self.tree.tag_configure('oddrow', background='#fff')
        self.tree.tag_configure('evenrow', background='#f7f9fa')
        self.tree.bind('<ButtonRelease-1>', self.on_tree_click)
        # Thêm thanh cuộn ngang
        xscroll = tk.Scrollbar(table_inner, orient=tk.HORIZONTAL, command=self.tree.xview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=xscroll.set)
        # Thêm thanh cuộn dọc (nếu muốn)
        yscroll = tk.Scrollbar(table_inner, orient=tk.VERTICAL, command=self.tree.yview)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=yscroll.set)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sp.ten, spbt.ten_bienthe, nsp.ma_lo, nsp.ngaynhap, nsp.han_su_dung, nsp.so_luong_con_lai, nsp.id, nsp.bienthe_id, nsp.gia_nhap
            FROM nhacungcap_sanpham nsp
            JOIN sanpham_bienthe spbt ON nsp.bienthe_id = spbt.id
            JOIN sanpham sp ON spbt.sanpham_id = sp.id
            ORDER BY sp.ten, spbt.ten_bienthe, nsp.ngaynhap
        ''')
        rows = cursor.fetchall()
        conn.close()
        today = datetime.now().date()
        for row in rows:
            han_su_dung = row[4]
            so_luong_con_lai = row[5]
            id_lo = row[6]
            bienthe_id = row[7]
            gia_nhap = row[8]
            is_expired = False
            try:
                if han_su_dung:
                    han = datetime.strptime(han_su_dung, '%Y-%m-%d').date()
                    if han < today:
                        is_expired = True
            except:
                pass
            values = row[:6] + ("Tiêu hủy" if is_expired and so_luong_con_lai > 0 else "",)
            item_id = self.tree.insert('', tk.END, values=values)
            if is_expired:
                self.tree.item(item_id, tags=("expired",))
        self.tree.tag_configure("expired", background="#ffcccc")

    def on_tree_click(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not item or col != '#7':
            return
        values = self.tree.item(item, 'values')
        if values[6] != "Tiêu hủy":
            return
        # Xác nhận tiêu hủy
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn tiêu hủy lô {values[2]} không?"):
            return
        # Thực hiện tiêu hủy
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Lấy id, bienthe_id, gia_nhap
        cursor.execute('SELECT id, bienthe_id, gia_nhap FROM nhacungcap_sanpham WHERE ma_lo = ?', (values[2],))
        row = cursor.fetchone()
        if not row:
            conn.close()
            messagebox.showerror("Lỗi", "Không tìm thấy lô hàng!")
            return
        id_lo, bienthe_id, gia_nhap = row
        # Lấy số lượng còn lại
        cursor.execute('SELECT so_luong_con_lai FROM nhacungcap_sanpham WHERE id = ?', (id_lo,))
        so_luong_con_lai = cursor.fetchone()[0]
        if so_luong_con_lai <= 0:
            conn.close()
            messagebox.showinfo("Thông báo", "Lô này đã được tiêu hủy hoặc hết hàng!")
            return
        # Cập nhật số lượng còn lại về 0
        cursor.execute('UPDATE nhacungcap_sanpham SET so_luong_con_lai = 0 WHERE id = ?', (id_lo,))
        # Ghi nhận vào bảng phiếu tiêu hủy
        cursor.execute('''
            INSERT INTO phieu_tieu_huy (ma_lo, bienthe_id, so_luong_huy, gia_nhap, ngay_huy, nhanvien_id, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (values[2], bienthe_id, so_luong_con_lai, gia_nhap, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1, 'Tiêu hủy do hết hạn'))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thành công", f"Đã tiêu hủy lô {values[2]} thành công!")
        self.load_data()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tồn kho chi tiết theo lô')
    root.geometry('900x500')
    InventoryBatchView(root)
    root.mainloop() 