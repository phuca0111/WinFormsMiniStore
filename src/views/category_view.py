import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from tkinter import ttk, messagebox
from Core.category import get_all_categories, add_category, update_category, delete_category

class CategoryView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        self.parent = parent
        self.db_path = db_path

        # Cấu hình grid cho self.frame (áp dụng cho các widget con bên trong frame này)
        self.frame.grid_rowconfigure(3, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        row_idx = 0

        # Tiêu đề "Quản lý thể loại sản phẩm"
        label = ttk.Label(self.frame, text='Quản lý thể loại sản phẩm', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=4, padx=20, pady=5, sticky=tk.N)
        row_idx += 1

        # Entry for category name
        entry_frame = ttk.Frame(self.frame)
        entry_frame.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=5, sticky=tk.NSEW)
        row_idx += 1
        entry_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(entry_frame, text="Tên thể loại:").grid(padx=0, pady=0, sticky=tk.W)
        self.entry = tk.Entry(entry_frame, font=('Arial', 12), width=50)
        self.entry.grid( padx=0, pady=0, sticky=tk.W)

        # Button frame
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=10, sticky=tk.NSEW)
        row_idx += 1
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)

        ttk.Button(btn_frame, text='Thêm', command=self.on_add).grid(row=0, column=0, padx=2, pady=2, sticky=tk.EW)
        ttk.Button(btn_frame, text='Sửa', command=self.on_update).grid(row=0, column=1, padx=2, pady=2, sticky=tk.EW)
        ttk.Button(btn_frame, text='Xóa', command=self.on_delete).grid(row=0, column=2, padx=2, pady=2, sticky=tk.EW)
        ttk.Button(btn_frame, text='Làm mới', command=self.load_categories).grid(row=0, column=3, padx=2, pady=2, sticky=tk.EW)

        # Treeview to display categories
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Tên thể loại'), show='headings', height=10)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tên thể loại', text='Tên thể loại')
        self.tree.column('ID',anchor=tk.CENTER)
        self.tree.column('Tên thể loại',anchor=tk.CENTER)
        self.tree.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=5, sticky=tk.NSEW)
        self.tree.bind('<<TreeviewSelect>>', lambda e: self.on_select(e))

        # Initial data load
        self.load_categories()

    def load_categories(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Lấy danh sách thể loại và hiển thị
        categories = get_all_categories()
        for cat in categories:
            self.tree.insert('', 'end', values=(cat.id, cat.ten))

    def on_add(self):
        ten = self.entry.get().strip()
        if not ten:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên thể loại!')
            return
        add_category(ten)
        self.entry.delete(0, tk.END)
        self.load_categories()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn thể loại để xóa!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        delete_category(id)
        self.entry.delete(0, tk.END)
        self.load_categories()

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn thể loại để sửa!')
            return
        ten_moi = self.entry.get().strip()
        if not ten_moi:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập tên thể loại mới!')
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        update_category(id, ten_moi)
        self.entry.delete(0, tk.END)
        self.load_categories()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, item['values'][1])

# Remove main function for standalone execution as it's now embedded
# def main():
#     root = tk.Tk()
#     root.title('Quản lý thể loại sản phẩm')
#     root.geometry('420x400')
#     app = CategoryView(root)
#     app.frame.pack(fill=tk.BOTH, expand=True)
#     root.mainloop()

# if __name__ == '__main__':
#     main() 