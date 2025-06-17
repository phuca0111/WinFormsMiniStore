import sqlite3
import os
from datetime import datetime, timedelta
#
class AccountModel:
    def __init__(self, db_path=None):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Database', 'ministore_db.sqlite')

    def log_login(self, nhanvien_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Lấy giờ Việt Nam
            vn_time = datetime.utcnow() + timedelta(hours=7)
            vn_time_str = vn_time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO nhanvien_login_log (nhanvien_id, login_time) VALUES (?, ?)', (nhanvien_id, vn_time_str))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('Lỗi ghi log đăng nhập:', e)
            return False 