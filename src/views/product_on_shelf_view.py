import tkinter as tk
from tkinter import ttk, messagebox
from src.models.product_on_shelf_model import ProductOnShelfModel
from models.inventory_model import Inventory

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

class ProductOnShelfView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.db_path = db_path
        self.model = ProductOnShelfModel(db_path)
        self.window = tk.Toplevel(parent)
        self.window.title("Quản lý sản phẩm trên kệ")
        self.window.geometry("600x400")
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=("kehang_id", "ten_ke", "ten_bienthe", "soluong"), show="headings")
        self.tree.heading("kehang_id", text="ID Kệ")
        self.tree.heading("ten_ke", text="Tên kệ")
        self.tree.heading("ten_bienthe", text="Tên biến thể")
        self.tree.heading("soluong", text="Số lượng")
        self.tree.column("kehang_id", width=60)
        self.tree.column("ten_ke", width=120)
        self.tree.column("ten_bienthe", width=180)
        self.tree.column("soluong", width=80)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        entry_frame = ttk.Frame(frame)
        entry_frame.pack(fill=tk.X, pady=5)
        ttk.Label(entry_frame, text="Kệ:").pack(side=tk.LEFT)
        self.combobox_ke = ttk.Combobox(entry_frame, state="readonly")
        self.combobox_ke.pack(side=tk.LEFT, padx=5)
        ttk.Label(entry_frame, text="Biến thể:").pack(side=tk.LEFT)
        self.combobox_bienthe = ttk.Combobox(entry_frame, state="readonly", width=30)
        self.combobox_bienthe.pack(side=tk.LEFT, padx=5)
        ttk.Label(entry_frame, text="Số lượng:").pack(side=tk.LEFT)
        self.entry_soluong = ttk.Entry(entry_frame, width=7)
        self.entry_soluong.pack(side=tk.LEFT, padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Thêm", command=self.add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Sửa", command=self.update).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Xóa", command=self.delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Làm mới", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        self.shelves = self.model.get_all_shelves()
        self.combobox_ke['values'] = [f"{k[0]} - {k[1]}" for k in self.shelves]
        self.variants = self.model.get_all_variants()
        self.combobox_bienthe['values'] = [f"{v[0]} - {v[1]} - {v[2]}" for v in self.variants]
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.model.get_all():
            # row: (kehang_id, ten_ke, bienthe_id, ten_sp, ten_bienthe, soluong)
            self.tree.insert('', tk.END, values=(row[0], row[1], row[4], row[5]))
        self.combobox_ke.set("")
        self.combobox_bienthe.set("")
        self.entry_soluong.delete(0, tk.END)
        self.selected_ke = None
        self.selected_bienthe = None

    def add(self):
        ke_idx = self.combobox_ke.current()
        bienthe_idx = self.combobox_bienthe.current()
        soluong = self.entry_soluong.get().strip()
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
        ke_idx = self.combobox_ke.current()
        bienthe_idx = self.combobox_bienthe.current()
        soluong = self.entry_soluong.get().strip()
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
                    self.combobox_ke.current(i)
                    break
            for i, v in enumerate(self.variants):
                if v[2] == ten_bienthe:
                    self.combobox_bienthe.current(i)
                    break
            self.entry_soluong.delete(0, tk.END)
            self.entry_soluong.insert(0, soluong)
            self.selected_ke = ke_id
            # Lấy đúng bienthe_id từ combobox variant
            self.selected_bienthe = self.variants[self.combobox_bienthe.current()][0] if self.combobox_bienthe.current() >= 0 else None 