import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Core.customer import CustomerCore

class CustomerView:
    def __init__(self, parent, db_path):
        self.parent = parent
        self.core = CustomerCore(db_path)
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search frame
        search_frame = ttk.LabelFrame(self.main_frame, text="Search")
        search_frame.pack(fill=tk.X, pady=5)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        search_entry.bind('<Return>', lambda e: self.search())

        search_btn = ttk.Button(search_frame, text="Search", command=self.search)
        search_btn.pack(side=tk.LEFT, padx=5)

        # Customer information frame
        info_frame = ttk.LabelFrame(self.main_frame, text="Customer Information")
        info_frame.pack(fill=tk.X, pady=5)

        # Grid layout for information fields
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Phone:").grid(row=0, column=2, padx=5, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.phone_var).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(info_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.email_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Address:").grid(row=1, column=2, padx=5, pady=5)
        self.address_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.address_var).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(info_frame, text="Birth Date:").grid(row=2, column=0, padx=5, pady=5)
        self.birthdate_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.birthdate_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Gender:").grid(row=2, column=2, padx=5, pady=5)
        self.gender_var = tk.StringVar()
        ttk.Combobox(info_frame, textvariable=self.gender_var, values=["Male", "Female"]).grid(row=2, column=3, padx=5, pady=5)

        # Button frame
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="New", command=self.new).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)

        # Treeview for customer list
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Phone", "Email", "Address", "Birth Date", "Gender"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Birth Date", text="Birth Date")
        self.tree.heading("Gender", text="Gender")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Phone", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Address", width=200)
        self.tree.column("Birth Date", width=100)
        self.tree.column("Gender", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
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

def main():
    # Create main window
    root = tk.Tk()
    root.title("Customer Management")
    root.geometry("1000x600")

    # Get database path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "Database", "ministore_db.sqlite")

    # Initialize customer interface
    app = CustomerView(root, db_path)

    # Run application
    root.mainloop()

if __name__ == "__main__":
    main()