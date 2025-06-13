import tkinter as tk
from tkinter import ttk, messagebox
from models.store_model import StoreModel
from Core.store import StoreCore

class StoreView:
    def __init__(self, parent, db_path: str):
        self.parent = parent
        self.db_path = db_path
        self.store_model = StoreModel(db_path)
        self.store_core = StoreCore(db_path)
        
        # Tạo cửa sổ mới
        self.window = tk.Toplevel(parent)
        self.window.title("Quản lý thông tin cửa hàng")
        self.window.geometry("800x600")
        
        # Tạo frame chính
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tạo Treeview để hiển thị danh sách cửa hàng
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Tên cửa hàng", "Địa chỉ", "Số điện thoại", 
                                                          "Mã số thuế", "Website", "Ghi chú"), show="headings")
        
        # Định dạng các cột
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên cửa hàng", text="Tên cửa hàng")
        self.tree.heading("Địa chỉ", text="Địa chỉ")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Mã số thuế", text="Mã số thuế")
        self.tree.heading("Website", text="Website")
        self.tree.heading("Ghi chú", text="Ghi chú")
        
        # Đặt độ rộng cột
        self.tree.column("ID", width=50)
        self.tree.column("Tên cửa hàng", width=150)
        self.tree.column("Địa chỉ", width=150)
        self.tree.column("Số điện thoại", width=100)
        self.tree.column("Mã số thuế", width=100)
        self.tree.column("Website", width=100)
        self.tree.column("Ghi chú", width=150)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí các widget
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Frame cho các nút
        button_frame = ttk.Frame(self.main_frame, padding="5")
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Tạo các nút
        ttk.Button(button_frame, text="Thêm mới", command=self.show_add_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.show_edit_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_store).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm mới", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Chọn cửa hàng", command=self.select_store_dialog).pack(side=tk.LEFT, padx=5)
        
        # Load dữ liệu ban đầu
        self.refresh_data()
        
    def refresh_data(self):
        """Làm mới dữ liệu hiển thị"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Lấy và hiển thị dữ liệu mới
        stores = self.store_model.get_all_stores()
        for store in stores:
            self.tree.insert("", tk.END, values=store)
            
    def show_add_dialog(self):
        """Hiển thị dialog thêm cửa hàng mới"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Thêm cửa hàng mới")
        dialog.geometry("400x300")
        
        # Tạo các trường nhập liệu
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
            """Lưu thông tin cửa hàng mới"""
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
                
        # Nút lưu và hủy
        ttk.Button(dialog, text="Lưu", command=save).grid(row=6, column=0, padx=5, pady=20)
        ttk.Button(dialog, text="Hủy", command=dialog.destroy).grid(row=6, column=1, padx=5, pady=20)
        
    def show_edit_dialog(self):
        """Hiển thị dialog sửa thông tin cửa hàng"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cửa hàng cần sửa!")
            return
            
        store_id = self.tree.item(selected[0])['values'][0]
        store = self.store_model.get_store_by_id(store_id)
        if not store:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin cửa hàng!")
            return
            
        dialog = tk.Toplevel(self.window)
        dialog.title("Sửa thông tin cửa hàng")
        dialog.geometry("400x300")
        
        # Tạo các trường nhập liệu
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
            """Lưu thông tin đã sửa"""
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
                
        # Nút lưu và hủy
        ttk.Button(dialog, text="Lưu", command=save).grid(row=6, column=0, padx=5, pady=20)
        ttk.Button(dialog, text="Hủy", command=dialog.destroy).grid(row=6, column=1, padx=5, pady=20)
        
    def delete_store(self):
        """Xóa cửa hàng đã chọn"""
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
        dialog = tk.Toplevel(self.window)
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
            # Lưu vào settings
            from Core.setting import SettingCore
            db_path = self.db_path
            setting = SettingCore(db_path)
            setting.set_setting("selected_store_id", str(store_id))
            tk.messagebox.showinfo("Thành công", f"Đã chọn cửa hàng: {store_names[idx]}")
            dialog.destroy()
        
        # Nút OK căn giữa
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Xác nhận", command=on_ok).pack() 