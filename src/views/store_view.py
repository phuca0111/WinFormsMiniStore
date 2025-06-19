import tkinter as tk
from tkinter import ttk, messagebox
from models.store_model import StoreModel
from Core.store import StoreCore

class StoreView(tk.Frame):
    def __init__(self, parent, db_path: str):
        super().__init__(parent, bg="#eef2f6")
        self.db_path = db_path
        self.store_model = StoreModel(db_path)
        self.store_core = StoreCore(db_path)
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Store.Treeview.Heading", font=("Segoe UI", 13, "bold"), foreground="#222", background="#eef2f6", relief="flat")
        style.configure("Store.Treeview", font=("Segoe UI", 12), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        # Khung danh sách
        frame_list = tk.LabelFrame(self, text='Danh sách cửa hàng', font=("Segoe UI", 12, "bold"), bg="#eef2f6", fg="#232a36", bd=0)
        frame_list.pack(fill=tk.BOTH, expand=True, padx=24, pady=(24, 8))
        columns = ("ID", "Tên cửa hàng", "Địa chỉ", "Số điện thoại", "Mã số thuế", "Website", "Ghi chú")
        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings", height=12, style="Store.Treeview")
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Tên cửa hàng', width=180, anchor="w")
        self.tree.column('Địa chỉ', width=220, anchor="w")
        self.tree.column('Số điện thoại', width=120, anchor="center")
        self.tree.column('Mã số thuế', width=100, anchor="center")
        self.tree.column('Website', width=120, anchor="center")
        self.tree.column('Ghi chú', width=220, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        # Border bo tròn giả lập
        frame_list.config(highlightbackground="#dde2e6", highlightthickness=2)
        # Thanh cuộn
        scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        # Nút chức năng pastel
        btn_frame = tk.Frame(self, bg="#eef2f6")
        btn_frame.pack(pady=16)
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_add = tk.Button(btn_frame, text='Thêm mới', command=self.show_add_dialog)
        style_btn(btn_add, "#eafaf1", "#d1f2eb")
        btn_add.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_edit = tk.Button(btn_frame, text='Sửa', command=self.show_edit_dialog)
        style_btn(btn_edit, "#f9e7cf", "#f6cba3")
        btn_edit.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_delete = tk.Button(btn_frame, text='Xóa', command=self.delete_store)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_refresh = tk.Button(btn_frame, text='Làm mới', command=self.refresh_data)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
        btn_select = tk.Button(btn_frame, text='Chọn cửa hàng', command=self.select_store_dialog)
        style_btn(btn_select, "#eafaf1", "#d1f2eb")
        btn_select.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        stores = self.store_model.get_all_stores()
        for store in stores:
            self.tree.insert("", tk.END, values=store)

    def show_add_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Thêm cửa hàng mới")
        dialog.geometry("400x300")
        ttk.Label(dialog, text="Tên cửa hàng:").grid(row=0, column=0, padx=5, pady=5)
        ten_cua_hang = ttk.Entry(dialog, width=30)
        ten_cua_hang.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Địa chỉ:").grid(row=1, column=0, padx=5, pady=5)
        dia_chi = ttk.Entry(dialog, width=30)
        dia_chi.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Số điện thoại:").grid(row=2, column=0, padx=5, pady=5)
        so_dien_thoai = ttk.Entry(dialog, width=30)
        so_dien_thoai.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Mã số thuế:").grid(row=3, column=0, padx=5, pady=5)
        ma_so_thue = ttk.Entry(dialog, width=30)
        ma_so_thue.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Website:").grid(row=4, column=0, padx=5, pady=5)
        website = ttk.Entry(dialog, width=30)
        website.grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Ghi chú:").grid(row=5, column=0, padx=5, pady=5)
        ghi_chu = ttk.Entry(dialog, width=30)
        ghi_chu.grid(row=5, column=1, padx=5, pady=5)
        def save():
            if not ten_cua_hang.get():
                messagebox.showerror("Lỗi", "Tên cửa hàng không được để trống!")
                return
            try:
                self.store_model.add_store(
                    ten_cua_hang.get(),
                    dia_chi.get() or None,
                    so_dien_thoai.get() or None,
                    ma_so_thue.get() or None,
                    website.get() or None,
                    ghi_chu.get() or None
                )
                messagebox.showinfo("Thành công", "Thêm cửa hàng mới thành công!")
                dialog.destroy()
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm cửa hàng: {str(e)}")
        ttk.Button(dialog, text="Lưu", command=save).grid(row=6, column=0, padx=5, pady=20)
        ttk.Button(dialog, text="Hủy", command=dialog.destroy).grid(row=6, column=1, padx=5, pady=20)

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cửa hàng cần sửa!")
            return
        store_id = self.tree.item(selected[0])['values'][0]
        store = self.store_model.get_store_by_id(store_id)
        if not store:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin cửa hàng!")
            return
        dialog = tk.Toplevel(self)
        dialog.title("Sửa thông tin cửa hàng")
        dialog.geometry("400x300")
        ttk.Label(dialog, text="Tên cửa hàng:").grid(row=0, column=0, padx=5, pady=5)
        ten_cua_hang = ttk.Entry(dialog, width=30)
        ten_cua_hang.insert(0, store[1])
        ten_cua_hang.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Địa chỉ:").grid(row=1, column=0, padx=5, pady=5)
        dia_chi = ttk.Entry(dialog, width=30)
        dia_chi.insert(0, store[2] or "")
        dia_chi.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Số điện thoại:").grid(row=2, column=0, padx=5, pady=5)
        so_dien_thoai = ttk.Entry(dialog, width=30)
        so_dien_thoai.insert(0, store[3] or "")
        so_dien_thoai.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Mã số thuế:").grid(row=3, column=0, padx=5, pady=5)
        ma_so_thue = ttk.Entry(dialog, width=30)
        ma_so_thue.insert(0, store[4] or "")
        ma_so_thue.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Website:").grid(row=4, column=0, padx=5, pady=5)
        website = ttk.Entry(dialog, width=30)
        website.insert(0, store[5] or "")
        website.grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Ghi chú:").grid(row=5, column=0, padx=5, pady=5)
        ghi_chu = ttk.Entry(dialog, width=30)
        ghi_chu.insert(0, store[6] or "")
        ghi_chu.grid(row=5, column=1, padx=5, pady=5)
        def save():
            if not ten_cua_hang.get():
                messagebox.showerror("Lỗi", "Tên cửa hàng không được để trống!")
                return
            try:
                self.store_model.update_store(
                    store_id,
                    ten_cua_hang.get(),
                    dia_chi.get() or None,
                    so_dien_thoai.get() or None,
                    ma_so_thue.get() or None,
                    website.get() or None,
                    ghi_chu.get() or None
                )
                messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
                dialog.destroy()
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật thông tin: {str(e)}")
        ttk.Button(dialog, text="Lưu", command=save).grid(row=6, column=0, padx=5, pady=20)
        ttk.Button(dialog, text="Hủy", command=dialog.destroy).grid(row=6, column=1, padx=5, pady=20)

    def delete_store(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cửa hàng cần xóa!")
            return
        store_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa cửa hàng này?"):
            try:
                if self.store_model.delete_store(store_id):
                    messagebox.showinfo("Thành công", "Xóa cửa hàng thành công!")
                    self.refresh_data()
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa cửa hàng!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa cửa hàng: {str(e)}")

    def select_store_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Chọn cửa hàng hoạt động")
        dialog.geometry("350x200")
        ttk.Label(dialog, text="Chọn cửa hàng muốn sử dụng:").pack(pady=10)
        stores = self.store_model.get_all_stores()
        store_names = [f"{s[1]} (ID: {s[0]})" for s in stores]
        store_ids = [s[0] for s in stores]
        selected_var = tk.StringVar()
        combobox = ttk.Combobox(dialog, values=store_names, textvariable=selected_var, state="readonly")
        combobox.pack(pady=10)
        if store_names:
            combobox.current(0)
        def on_ok():
            idx = combobox.current()
            if idx < 0:
                tk.messagebox.showwarning("Chưa chọn", "Vui lòng chọn cửa hàng!")
                return
            store_id = store_ids[idx]
            from Core.setting import SettingCore
            db_path = self.db_path
            setting = SettingCore(db_path)
            setting.set_setting("selected_store_id", str(store_id))
            tk.messagebox.showinfo("Thành công", f"Đã chọn cửa hàng ID: {store_id}")
            dialog.destroy() 