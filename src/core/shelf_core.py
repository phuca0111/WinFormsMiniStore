from src.models.shelf_model import ShelfModel

class ShelfCore:
    def __init__(self, db_path):
        self.model = ShelfModel(db_path)

    def get_all_shelves(self):
        return self.model.get_all_shelves()

    def add_shelf(self, ten):
        self.model.add_shelf(ten)

    def update_shelf(self, shelf_id, ten):
        self.model.update_shelf(shelf_id, ten)

    def delete_shelf(self, shelf_id):
        self.model.delete_shelf(shelf_id) 