import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core.customer import CustomerCore

class CustomerView:
    def __init__(self, parent, db_path=None):
        self.frame = ttk.Frame(parent)
        # Cấu hình grid cho self.frame (áp dụng cho các widget con bên trong frame này)
        self.frame.grid_rowconfigure(4, weight=1) # Row for treeview to expand
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.parent = parent
        self.core = CustomerCore(db_path)
        self.setup_ui()
      
    def setup_ui(self):
        row_idx = 0

        # Tiêu đề "Khách hàng"
        label = ttk.Label(self.frame, text='Khách hàng', font=("Arial", 18))
        label.grid(row=row_idx, column=0, columnspan=4, padx=20, pady=5, sticky=tk.N)
        row_idx += 1

        # Search frame
        search_frame = ttk.LabelFrame(self.frame, text="Tìm kiếm")
        search_frame.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=0, sticky=tk.NSEW)
        row_idx += 1
        # Configure internal grid for search_frame
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        search_entry.bind('<Return>', lambda e: self.search())

        search_btn = ttk.Button(search_frame, text="Tìm kiếm", command=self.search)
        search_btn.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        # Customer information frame
        info_frame = ttk.LabelFrame(self.frame, text="Thông tin khách hàng")
        info_frame.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=0, sticky=tk.NSEW)
        row_idx += 1

        # Grid layout for information fields (inside info_frame)
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Row 0
        ttk.Label(info_frame, text="Tên:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(info_frame, text="Số điện thoại:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.phone_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.phone_var, width=40).grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)

        # Row 1
        ttk.Label(info_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.email_var, width=40).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(info_frame, text="Địa chỉ:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.address_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.address_var, width=40).grid(row=1, column=3, padx=5, pady=5, sticky=tk.EW)

        # Row 2
        ttk.Label(info_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.birthdate_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.birthdate_var, width=40).grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(info_frame, text="Giới tính:").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.gender_var = tk.StringVar()
        ttk.Combobox(info_frame, textvariable=self.gender_var, values=["Nam", "Nữ"], width=37).grid(row=2, column=3, padx=5, pady=5, sticky=tk.EW)

        # Button frame
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=0, sticky=tk.NSEW)
        row_idx += 1
        # Configure internal grid for btn_frame
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)

        ttk.Button(btn_frame, text="Mới", command=self.new).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text="Lưu", command=self.save).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text="Xóa", command=self.delete).grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(btn_frame, text="Làm mới", command=self.refresh).grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)

        # Treeview for customer list
        tree_frame = ttk.Frame(self.frame)
        tree_frame.grid(row=row_idx, column=0, columnspan=4, padx=10, pady=0, sticky=tk.NSEW)
        # Configure tree_frame to expand within its grid cell
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Tên", "Số điện thoại", "Email", "Địa chỉ", "Ngày sinh", "Giới tính"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Địa chỉ", text="Địa chỉ")
        self.tree.heading("Ngày sinh", text="Ngày sinh")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Tên", width=150)
        self.tree.column("Số điện thoại", width=100, anchor=tk.CENTER)
        self.tree.column("Email", width=150,anchor=tk.CENTER)
        self.tree.column("Địa chỉ", width=200,anchor=tk.CENTER)
        self.tree.column("Ngày sinh", width=100, anchor=tk.CENTER)
        self.tree.column("Giới tính", width=100, anchor=tk.CENTER)
        self.tree.grid(row=0, column=0, sticky=tk.NSEW) # Treeview inside tree_frame uses grid
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Load initial data
        self.load_data()

    def load_data(self):
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get and display new data
        customer_list = self.core.get_all_customers()
        for customer in customer_list:
            self.tree.insert("", tk.END, values=customer)

    def new(self):
        self.refresh()

    def save(self):
        # Get data from input fields
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_var.get()
        birthdate = self.birthdate_var.get()
        gender = self.gender_var.get()

        # Check if adding new or updating
        selected_item = self.tree.selection()
        if selected_item:
            # Update
            customer_id = self.tree.item(selected_item[0])['values'][0]
            success, message = self.core.update_customer(customer_id, name, phone, email, address, birthdate, gender)
        else:
            # Add new
            success, message = self.core.add_customer(name, phone, email, address, birthdate, gender)

        if success:
            messagebox.showinfo("Thành công", message)
            self.load_data()
        else:
            messagebox.showerror("Lỗi", message)

    def delete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng này?"):
            customer_id = self.tree.item(selected_item[0])['values'][0]
            success, message = self.core.delete_customer(customer_id)
            if success:
                messagebox.showinfo("Thành công", message)
                self.load_data()
            else:
                messagebox.showerror("Lỗi", message)

    def refresh(self):
        self.search_var.set("") # Clear search field as well
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.birthdate_var.set("")
        self.gender_var.set("")
        self.tree.selection_remove(*self.tree.selection())
        self.load_data() # Reload data after refresh

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            self.name_var.set(values[1])
            self.phone_var.set(values[2])
            self.email_var.set(values[3])
            self.address_var.set(values[4])
            self.birthdate_var.set(values[5])
            self.gender_var.set(values[6])

    def search(self):
        keyword = self.search_var.get()
        if not keyword:
            self.load_data()
            return

        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Search and display results
        results = self.core.search_customers(keyword)
        if not results:
            messagebox.showinfo("Thông báo", f"Không tìm thấy khách hàng nào với từ khóa: {keyword}")
        for customer in results:
            self.tree.insert("", tk.END, values=customer)

# Remove main function for standalone execution as it's now embedded
# def main():
#     # Create main window
#     root = tk.Tk()
#     root.title("Customer Management")
#     root.geometry("1000x600")

#     # Get database path
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     db_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "Database", "ministore_db.sqlite")

#     # Initialize customer interface
#     app = CustomerView(root, db_path)

#     # Run application
#     root.mainloop()

# if __name__ == "__main__":
#     main()