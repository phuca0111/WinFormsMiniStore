from models.store_model import StoreModel

class StoreCore:
    def __init__(self, db_path):
        self.model = StoreModel(db_path)

    def get_all_stores(self):
        return self.model.get_all_stores()

    def add_store(self, ten_cua_hang, dia_chi=None, so_dien_thoai=None, ma_so_thue=None, website=None, ghi_chu=None):
        # Có thể thêm validate dữ liệu ở đây
        return self.model.add_store(ten_cua_hang, dia_chi, so_dien_thoai, ma_so_thue, website, ghi_chu)

    def update_store(self, store_id, **kwargs):
        return self.model.update_store(store_id, **kwargs)

    def delete_store(self, store_id):
        return self.model.delete_store(store_id) 