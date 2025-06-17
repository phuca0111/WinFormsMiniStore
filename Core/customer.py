from models.customer_model import CustomerModel

class CustomerCore:
    def __init__(self, db_path):
        self.model = CustomerModel(db_path)

    def add_customer(self, name, phone, email=None, address=None, birthdate=None, gender=None):
        # Validate input data
        if not name or not phone:
            return False, "Name and phone number are required!"
        
        # Validate name format (only letters and spaces)
        if not all(c.isalpha() or c.isspace() for c in name):
            return False, "Name must contain only letters and spaces!"
        
        # Validate phone number format
        if not phone.isdigit():
            return False, "Phone number must contain only digits!"

        # Add customer
        try:
            customer_id = self.model.add_customer(name, phone, email, address, birthdate, gender)
            if customer_id:
                return True, "Customer added successfully!"
            return False, "Failed to add customer!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def update_customer(self, id, name=None, phone=None, email=None, address=None, birthdate=None, gender=None):
        # Validate input data
        if name and not all(c.isalpha() or c.isspace() for c in name):
            return False, "Name must contain only letters and spaces!"
        
        if phone and not phone.isdigit():
            return False, "Phone number must contain only digits!"

        try:
            if self.model.update_customer(id, name, phone, email, address, birthdate, gender):
                return True, "Customer updated successfully!"
            return False, "Failed to update customer!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def delete_customer(self, id):
        try:
            if self.model.delete_customer(id):
                return True, "Customer deleted successfully!"
            return False, "Failed to delete customer!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_all_customers(self):
        try:
            return self.model.get_all_customers()
        except Exception as e:
            print(f"Error getting all customers: {e}")
            return []

    def search_customers(self, keyword):
        try:
            return self.model.search_customers(keyword)
        except Exception as e:
            print(f"Error searching customers: {e}")
            return []

    def get_customer_by_id(self, id):
        try:
            return self.model.get_customer_by_id(id)
        except Exception as e:
            print(f"Error getting customer by ID: {e}")
            return None

    def get_all_customers_sample(self):
        # Trả về danh sách khách hàng mẫu (id, tên, sdt)
        return [
            (1, "Nguyễn Văn A", "0123456789"),
            (2, "Trần Thị B", "0987654321"),
            (3, "Lê Văn C", "0912345678"),
        ] 