import tkinter as tk
from tkinter import ttk, messagebox, END
from models.product_on_shelf_model import ProductOnShelfModel
from models.inventory_model import Inventory
from models.product_variant_model import ProductVariant
import cv2
from pyzbar import pyzbar
from Core.barcode_scanner import scan_barcode

class ProductOnShelfCore:
    def __init__(self, db_path):
        self.model = ProductOnShelfModel(db_path)

    def get_all(self):
        return self.model.get_all()

    def add(self, ke_id, sanpham_id):
        self.model.add(ke_id, sanpham_id)

    def update(self, id_, ke_id, sanpham_id):
        self.model.update(id_, ke_id, sanpham_id)

    def delete(self, id_):
        self.model.delete(id_)

class ProductOnShelfView(tk.Frame):
    def __init__(self, parent, db_path):
        super().__init__(parent)
        self.configure(bg="#F5F7FA")
        self.db_path = db_path
        self.model = ProductOnShelfModel(db_path)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#F5F7FA", relief="flat")
        style.configure("Custom.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#F5F7FA")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")
        style.configure("TCombobox", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")

        # Khung nhập thông tin
        input_frame = tk.LabelFrame(self, text="Nhập thông tin sản phẩm trên kệ", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222", bd=0)
        input_frame.pack(fill=tk.X, padx=32, pady=(24, 8))
        tk.Label(input_frame, text="Barcode:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222").grid(row=0, column=0, sticky="e", padx=8, pady=8)
        self.entry_barcode = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_barcode.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        self.entry_barcode.bind('<Return>', self.on_barcode_entered)
        self.btn_scan = tk.Button(input_frame, text="Quét mã vạch (Camera)", font=("Segoe UI", 12, "bold"), command=self.scan_barcode)
        self.btn_scan.grid(row=0, column=2, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Tên kệ:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222").grid(row=1, column=0, sticky="e", padx=8, pady=8)
        self.combo_product = ttk.Combobox(input_frame, font=("Segoe UI", 12))
        self.combo_product.grid(row=1, column=1, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Biến thể:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222").grid(row=1, column=2, sticky="e", padx=8, pady=8)
        self.combo_variant = ttk.Combobox(input_frame, font=("Segoe UI", 12))
        self.combo_variant.grid(row=1, column=3, sticky="ew", padx=8, pady=8)
        tk.Label(input_frame, text="Số lượng:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#222").grid(row=2, column=0, sticky="e", padx=8, pady=8)
        self.entry_qty = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry_qty.grid(row=2, column=1, sticky="ew", padx=8, pady=8)
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(2, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # Nút chức năng pastel bo tròn
        btn_frame = tk.Frame(self, bg="#F5F7FA")
        btn_frame.pack(fill=tk.X, padx=32, pady=(0, 16))
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Thêm', command=self.add)
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_update = tk.Button(btn_frame, text='Sửa', command=self.update)
        style_btn(btn_update, "#f9e7cf", "#f6cba3")
        btn_update.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=self.delete)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.load_data)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=16)

        # Bảng bo tròn giả lập
        table_frame = tk.Frame(self, bg="#F5F7FA")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(0, 32))
        table_border = tk.Frame(table_frame, bg="#DDE2E6", bd=0)
        table_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        columns = ('ID', 'Tên kệ', 'Tên biến thể', 'Barcode', 'Số lượng')
        self.tree = ttk.Treeview(table_inner, columns=columns, show='headings', height=12, style="Custom.Treeview")
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Tên kệ', width=180, anchor="w")
        self.tree.column('Tên biến thể', width=180, anchor="w")
        self.tree.column('Barcode', width=160, anchor="center")
        self.tree.column('Số lượng', width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        scrollbar = tk.Scrollbar(table_inner, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_data(self):
        self.shelves = self.model.get_all_shelves()
        self.combo_product['values'] = [f"{k[0]} - {k[1]}" for k in self.shelves]
        self.variants = self.model.get_all_variants()
        self.combo_variant['values'] = [f"{v[0]} - {v[1]} - {v[2]}" for v in self.variants]
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.model.get_all():
            # row: (kehang_id, ten_ke, bienthe_id, ten_sp, ten_bienthe, soluong)
            self.tree.insert('', tk.END, values=(row[0], row[1], row[4], row[5]))
        self.combo_product.set("")
        self.combo_variant.set("")
        self.entry_qty.delete(0, tk.END)
        self.selected_ke = None
        self.selected_bienthe = None

    def add(self):
        ke_idx = self.combo_product.current()
        bienthe_idx = self.combo_variant.current()
        soluong = self.entry_qty.get().strip()
        if ke_idx < 0 or bienthe_idx < 0 or not soluong:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn kệ, biến thể và nhập số lượng!")
            return
        ke_id = self.shelves[ke_idx][0]
        bienthe_id = self.variants[bienthe_idx][0]
        try:
            soluong = int(soluong)
        except:
            messagebox.showwarning("Lỗi", "Số lượng phải là số!")
            return
        # Kiểm tra tổng số lượng trên kệ không vượt quá tồn kho
        tonkho = 0
        for inv in Inventory.get_all():
            if inv.bienthe_id == bienthe_id:
                tonkho = inv.soluong
                break
        tong_tren_ke = self.model.get_total_on_shelves_by_variant(bienthe_id)
        if tong_tren_ke + soluong > tonkho:
            messagebox.showerror("Lỗi", f"Tổng số lượng trên kệ ({tong_tren_ke + soluong}) không được vượt quá tồn kho ({tonkho})!")
            return
        self.model.add(ke_id, bienthe_id, soluong)
        self.load_data()

    def update(self):
        if self.selected_ke is None or self.selected_bienthe is None:
            messagebox.showwarning("Chọn dòng", "Vui lòng chọn dòng để sửa!")
            return
        ke_idx = self.combo_product.current()
        bienthe_idx = self.combo_variant.current()
        soluong = self.entry_qty.get().strip()
        if ke_idx < 0 or bienthe_idx < 0 or not soluong:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn kệ, biến thể và nhập số lượng!")
            return
        ke_id = self.shelves[ke_idx][0]
        bienthe_id = self.variants[bienthe_idx][0]
        try:
            soluong = int(soluong)
        except:
            messagebox.showwarning("Lỗi", "Số lượng phải là số!")
            return
        # Kiểm tra tổng số lượng trên kệ không vượt quá tồn kho (trừ đi số lượng cũ của dòng đang sửa)
        tonkho = 0
        for inv in Inventory.get_all():
            if inv.bienthe_id == bienthe_id:
                tonkho = inv.soluong
                break
        tong_tren_ke = self.model.get_total_on_shelves_by_variant(bienthe_id)
        # Lấy số lượng cũ của dòng đang sửa
        old_soluong = 0
        for item in self.tree.get_children():
            vals = self.tree.item(item)['values']
            if vals[0] == ke_id and vals[2] == self.variants[bienthe_idx][2]:
                old_soluong = int(vals[3])
                break
        if tong_tren_ke - old_soluong + soluong > tonkho:
            messagebox.showerror("Lỗi", f"Tổng số lượng trên kệ ({tong_tren_ke - old_soluong + soluong}) không được vượt quá tồn kho ({tonkho})!")
            return
        self.model.update(ke_id, bienthe_id, soluong)
        self.load_data()

    def delete(self):
        if self.selected_ke is None or self.selected_bienthe is None:
            messagebox.showwarning("Chọn dòng", "Vui lòng chọn dòng để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa?"):
            self.model.delete(self.selected_ke, self.selected_bienthe)
            self.load_data()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            ke_id, ten_ke, ten_bienthe, soluong = values
            for i, k in enumerate(self.shelves):
                if k[0] == ke_id:
                    self.combo_product.current(i)
                    break
            for i, v in enumerate(self.variants):
                if v[2] == ten_bienthe:
                    self.combo_variant.current(i)
                    break
            self.entry_qty.delete(0, tk.END)
            self.entry_qty.insert(0, soluong)
            self.selected_ke = ke_id
            # Lấy đúng bienthe_id từ combobox variant
            self.selected_bienthe = self.variants[self.combo_variant.current()][0] if self.combo_variant.current() >= 0 else None

    def scan_barcode(self):
        barcode_data = scan_barcode()
        if barcode_data:
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, barcode_data)
            self.on_barcode_entered()
        else:
            messagebox.showwarning("Không tìm thấy", "Không quét được mã vạch nào!")

    def on_barcode_entered(self, event=None):
        from models.product_variant_model import ProductVariant
        barcode = self.entry_barcode.get().strip()
        if not barcode:
            return
        # Truy vấn lại database để lấy biến thể mới nhất
        variant = ProductVariant.get_by_barcode(barcode)
        self.variants = self.model.get_all_variants()
        self.combo_variant['values'] = [f"{v[0]} - {v[1]} - {v[2]}" for v in self.variants]
        if variant:
            # Tìm index của biến thể trong combobox
            for i, v in enumerate(self.variants):
                if v[0] == variant.id:
                    self.combo_variant.current(i)
                    break
        else:
            messagebox.showwarning("Không tìm thấy", "Không tìm thấy biến thể với barcode này!") 