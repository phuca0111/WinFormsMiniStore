import tkinter as tk
from tkinter import ttk

class HuongDanView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        label = ttk.Label(self, text="HƯỚNG DẪN SỬ DỤNG PHẦN MỀM QUẢN LÝ MINI STORE", font=("Arial", 16, "bold"), foreground="blue")
        label.pack(pady=10)
        # Nội dung hướng dẫn mẫu
        huongdan_text = (
            "1. Đăng nhập bằng tài khoản được cấp.\n"
            "2. nếu thấy dữ liệu chưa được load cần tắt chức năng đó và mở lại\n"
            "3. Để nhập hàng: Vào menu 'Nhập hàng', chọn nhà cung cấp, biến thể sản phẩm, nhập số lượng và giá nhập, sau đó nhấn 'Thêm'.\n"
            "4. Để sửa hoặc xóa: Chọn dòng cần sửa/xóa và nhấn nút tương ứng.\n"
            "5. mật khẩu mặc định là 123456.\n"
            "6. Nếu gặp khó khăn, liên hệ quản trị viên để được hỗ trợ."
            
        )
        text = tk.Text(self, wrap=tk.WORD, font=("Arial", 12), height=15)
        text.insert(tk.END, huongdan_text)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10) 