import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database.database import Database

def test_database_connection():
    """Kiểm tra kết nối database"""
    print("\n=== Kiểm tra kết nối database ===")
    db = Database()
    
    # Kiểm tra xem file database có tồn tại không
    if os.path.exists(db.db_file):
        print(f"✓ File database tồn tại tại: {db.db_file}")
    else:
        print(f"✗ Không tìm thấy file database tại: {db.db_file}")
        return False
    
    # Kiểm tra kết nối
    if db.conn:
        print("✓ Kết nối database thành công")
    else:
        print("✗ Không thể kết nối đến database")
        return False
    
    return True

def test_create_tables():
    """Kiểm tra tạo bảng"""
    print("\n=== Kiểm tra tạo bảng ===")
    db = Database()
    
    # Đọc file SQL
    try:
        with open('Database/database.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
            print("✓ Đọc file SQL thành công")
    except Exception as e:
        print(f"✗ Lỗi khi đọc file SQL: {e}")
        return False
    
    # Thực thi script SQL
    try:
        db.conn.executescript(sql_script)
        print("✓ Tạo bảng thành công")
    except Exception as e:
        print(f"✗ Lỗi khi tạo bảng: {e}")
        return False
    
    return True

def test_crud_operations():
    """Kiểm tra các thao tác CRUD cơ bản"""
    print("\n=== Kiểm tra thao tác CRUD ===")
    db = Database()
    
    # Test INSERT
    print("\n1. Kiểm tra thêm dữ liệu:")
    cuahang_data = {
        'ten': 'Cửa hàng test'
    }
    try:
        id = db.insert_data('cuahang', cuahang_data)
        print(f"✓ Thêm cửa hàng thành công với ID: {id}")
    except Exception as e:
        print(f"✗ Lỗi khi thêm cửa hàng: {e}")
        return False
    
    # Test SELECT
    print("\n2. Kiểm tra đọc dữ liệu:")
    try:
        result = db.fetch_all("SELECT * FROM cuahang WHERE id = ?", [id])
        if result:
            print(f"✓ Đọc dữ liệu thành công: {result}")
        else:
            print("✗ Không tìm thấy dữ liệu")
            return False
    except Exception as e:
        print(f"✗ Lỗi khi đọc dữ liệu: {e}")
        return False
    
    # Test UPDATE
    print("\n3. Kiểm tra cập nhật dữ liệu:")
    update_data = {'ten': 'Cửa hàng test (đã cập nhật)'}
    condition = {'id': id}
    try:
        rows = db.update_data('cuahang', update_data, condition)
        print(f"✓ Cập nhật thành công {rows} bản ghi")
    except Exception as e:
        print(f"✗ Lỗi khi cập nhật dữ liệu: {e}")
        return False
    
    # Test DELETE
    print("\n4. Kiểm tra xóa dữ liệu:")
    try:
        rows = db.delete_data('cuahang', {'id': id})
        print(f"✓ Xóa thành công {rows} bản ghi")
    except Exception as e:
        print(f"✗ Lỗi khi xóa dữ liệu: {e}")
        return False
    
    return True

def main():
    """Hàm chính để chạy tất cả các test"""
    print("=== Bắt đầu kiểm tra database ===\n")
    
    # Kiểm tra kết nối
    if not test_database_connection():
        print("\n✗ Kiểm tra kết nối thất bại")
        return
    
    # Kiểm tra tạo bảng
    if not test_create_tables():
        print("\n✗ Kiểm tra tạo bảng thất bại")
        return
    
    # Kiểm tra CRUD
    if not test_crud_operations():
        print("\n✗ Kiểm tra CRUD thất bại")
        return
    
    print("\n=== Tất cả các kiểm tra đã hoàn thành thành công! ===")

if __name__ == "__main__":
    main() 