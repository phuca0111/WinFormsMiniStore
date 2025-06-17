import os
from models.order_model import OrderModel

def get_db_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Database', 'ministore_db.sqlite')

class OrderCore:
    def __init__(self, db_path=None):
        self.db_path = db_path or get_db_path()
        self.model = OrderModel(self.db_path)

    def get_all_orders(self):
        return self.model.get_all_orders()

    def get_order_details(self, order_id):
        return self.model.get_order_details(order_id)

    def delete_order(self, order_id):
        return self.model.delete_order(order_id) 