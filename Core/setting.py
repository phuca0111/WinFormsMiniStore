from models.setting_model import SettingModel

class SettingCore:
    def __init__(self, db_path):
        self.model = SettingModel(db_path, table_name='tienich_caidat')

    def get_setting(self, key):
        return self.model.get(key)

    def set_setting(self, key, value):
        self.model.set(key, value) 