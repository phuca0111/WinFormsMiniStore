import tkinter as tk
from tkinter import ttk

class BaseView:
    def __init__(self, parent):
        self.parent = parent
        self.current_view = None
        self.views = {}
        self.content_frame = self.parent

    def add_view(self, name, view_instance):
        """Thêm một view instance vào danh sách quản lý"""
        self.views[name] = view_instance
        # Đặt view mới vào content_frame
        view_instance.frame.pack_forget()  # Ẩn view nếu đang hiển thị
        
    def show_view(self, name):
        """Hiển thị view được chọn và ẩn các view khác"""
        if name in self.views:
            # Ẩn tất cả các view
            for view in self.views.values():
                view.frame.pack_forget()
            
            # Hiển thị view được chọn
            view = self.views[name]
            view.frame.pack(fill=tk.BOTH, expand=True)
            self.current_view = view
        
    def hide_current_view(self):
        """Ẩn view hiện tại"""
        if self.current_view:
            self.current_view.frame.pack_forget()
            self.current_view = None