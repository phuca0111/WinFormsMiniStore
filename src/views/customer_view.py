import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core.customer import CustomerCore

class CustomerView(tk.Frame):
    def __init__(self, parent, db_path):
        super().__init__(parent)
        self.db_path = db_path
        self.core = CustomerCore(db_path)
        self.configure(bg="#EEF2F6")
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Customer.Treeview.Heading", font=("Segoe UI", 12, "bold"), foreground="#222", background="#EEF2F6", relief="flat")
        style.configure("Customer.Treeview", font=("Segoe UI", 11), rowheight=32, background="#fff", fieldbackground="#fff", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 12), padding=10, borderwidth=0, relief="flat", background="#eafaf1")
        style.configure("TEntry", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff")
        style.configure("TCombobox", font=("Segoe UI", 12), padding=8, borderwidth=1, relief="groove", background="#fff", fieldbackground="#fff")

        # Search frame
        search_frame = tk.Frame(self, bg="#EEF2F6")
        search_frame.pack(fill=tk.X, pady=8, padx=32)
        tk.Label(search_frame, text="Search", font=("Segoe UI", 12, "bold"), bg="#EEF2F6").pack(side=tk.LEFT, padx=(0, 12))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 12))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        search_entry.bind('<Return>', lambda e: self.search())
        search_btn = tk.Button(search_frame, text="Search", font=("Segoe UI", 12, "bold"), bg="#eafaf1", fg="#222", activebackground="#d1f2eb", relief="flat", bd=0, padx=18, pady=6, cursor="hand2", highlightthickness=0, command=self.search)
        search_btn.pack(side=tk.LEFT, padx=5)

        # Customer information frame
        info_frame = tk.LabelFrame(self, text="Customer Information", font=("Segoe UI", 12, "bold"), bg="#EEF2F6", fg="#222", bd=0)
        info_frame.pack(fill=tk.X, pady=8, padx=32)
        tk.Label(info_frame, text="Name:", font=("Segoe UI", 12), bg="#EEF2F6").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.name_var, font=("Segoe UI", 12)).grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        tk.Label(info_frame, text="Phone:", font=("Segoe UI", 12), bg="#EEF2F6").grid(row=0, column=2, padx=8, pady=8, sticky="e")
        self.phone_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.phone_var, font=("Segoe UI", 12)).grid(row=0, column=3, padx=8, pady=8, sticky="ew")
        tk.Label(info_frame, text="Email:", font=("Segoe UI", 12), bg="#EEF2F6").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.email_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.email_var, font=("Segoe UI", 12)).grid(row=1, column=1, padx=8, pady=8, sticky="ew")
        tk.Label(info_frame, text="Address:", font=("Segoe UI", 12), bg="#EEF2F6").grid(row=1, column=2, padx=8, pady=8, sticky="e")
        self.address_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.address_var, font=("Segoe UI", 12)).grid(row=1, column=3, padx=8, pady=8, sticky="ew")
        tk.Label(info_frame, text="Birth Date:", font=("Segoe UI", 12), bg="#EEF2F6").grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.birthdate_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.birthdate_var, font=("Segoe UI", 12)).grid(row=2, column=1, padx=8, pady=8, sticky="ew")
        tk.Label(info_frame, text="Gender:", font=("Segoe UI", 12), bg="#EEF2F6").grid(row=2, column=2, padx=8, pady=8, sticky="e")
        self.gender_var = tk.StringVar()
        ttk.Combobox(info_frame, textvariable=self.gender_var, values=["Male", "Female"], font=("Segoe UI", 12), state='readonly', style="TCombobox").grid(row=2, column=3, padx=8, pady=8, sticky="ew")
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Button frame
        btn_frame = tk.Frame(self, bg="#EEF2F6")
        btn_frame.pack(fill=tk.X, pady=8, padx=32)
        def style_btn(btn, color, hover):
            btn.configure(bg=color, fg="#222", activebackground=hover, activeforeground="#222", relief="flat", bd=0, font=("Segoe UI", 12, "bold"), cursor="hand2", padx=18, pady=10, highlightthickness=0, borderwidth=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn_new = tk.Button(btn_frame, text="New", command=self.new)
        style_btn(btn_new, "#eafaf1", "#b6f5c1")
        btn_new.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        btn_save = tk.Button(btn_frame, text="Save", command=self.save)
        style_btn(btn_save, "#f9e7cf", "#f6cba3")
        btn_save.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        btn_delete = tk.Button(btn_frame, text="Delete", command=self.delete)
        style_btn(btn_delete, "#fdeaea", "#f6bebe")
        btn_delete.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        btn_refresh = tk.Button(btn_frame, text="Refresh", command=self.refresh)
        style_btn(btn_refresh, "#e8eaf6", "#c5cae9")
        btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)

        # Border bo tròn giả lập cho bảng
        table_frame = tk.Frame(self, bg="#EEF2F6")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=(0, 32))
        table_border = tk.Frame(table_frame, bg="#EEF2F6", bd=0)
        table_border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        table_inner = tk.Frame(table_border, bg="#fff")
        table_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        columns = ("ID", "Name", "Phone", "Email", "Address", "Birth Date", "Gender")
        self.tree = ttk.Treeview(table_inner, columns=columns, show="headings", style="Customer.Treeview")
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5, padx=8)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        # Thanh cuộn dọc
        scrollbar = tk.Scrollbar(table_inner, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
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
            messagebox.showinfo("Success", message)
            self.load_data()
        else:
            messagebox.showerror("Error", message)

    def delete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a customer to delete!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            customer_id = self.tree.item(selected_item[0])['values'][0]
            success, message = self.core.delete_customer(customer_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_data()
            else:
                messagebox.showerror("Error", message)

    def refresh(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.birthdate_var.set("")
        self.gender_var.set("")
        self.tree.selection_remove(*self.tree.selection())

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
        for customer in results:
            self.tree.insert("", tk.END, values=customer)