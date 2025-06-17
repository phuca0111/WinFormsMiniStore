# Cấu hình Database
DB_NAME = "ministore_db.sqlite"
DB_PATH = "Database/ministore_db.sqlite"

# Cấu hình kết nối
DB_TIMEOUT = 30  # Thời gian timeout khi kết nối (giây)
DB_CHECK_SAME_THREAD = False  # Cho phép kết nối từ nhiều thread

# Cấu hình backup
BACKUP_DIR = "Database/backups"  # Thư mục lưu trữ backup
BACKUP_PREFIX = "backup_"  # Tiền tố cho file backup 