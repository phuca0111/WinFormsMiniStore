import sys
import os

# Thêm đường dẫn gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.supplier_model import Supplier

class SupplierCore:
    @staticmethod
    def validate_supplier(ten, sdt=None, gmail=None):
        """Kiểm tra tính hợp lệ của dữ liệu nhà cung cấp"""
        errors = []
        
        if not ten or len(ten.strip()) == 0:
            errors.append("Tên nhà cung cấp không được để trống")
            
        if sdt and not sdt.isdigit():
            errors.append("Số điện thoại phải là số")
            
        if gmail and '@' not in gmail:
            errors.append("Email không hợp lệ")
            
        return errors

    @staticmethod
    def get_all_suppliers():
        """Lấy danh sách tất cả nhà cung cấp"""
        return Supplier.get_all()

    @staticmethod
    def get_supplier_by_id(id):
        """Lấy thông tin nhà cung cấp theo ID"""
        return Supplier.get_by_id(id)

    @staticmethod
    def add_supplier(ten, diachi=None, sdt=None, gmail=None):
        """Thêm nhà cung cấp mới"""
        errors = SupplierCore.validate_supplier(ten, sdt, gmail)
        if errors:
            return False, errors

        supplier = Supplier(ten=ten, diachi=diachi, sdt=sdt, gmail=gmail)
        supplier.save()
        return True, "Thêm nhà cung cấp thành công"

    @staticmethod
    def update_supplier(id, ten, diachi=None, sdt=None, gmail=None):
        """Cập nhật thông tin nhà cung cấp"""
        errors = SupplierCore.validate_supplier(ten, sdt, gmail)
        if errors:
            return False, errors

        supplier = Supplier.get_by_id(id)
        if not supplier:
            return False, ["Không tìm thấy nhà cung cấp"]

        supplier.ten = ten
        supplier.diachi = diachi
        supplier.sdt = sdt
        supplier.gmail = gmail
        supplier.save()
        return True, "Cập nhật thành công"

    @staticmethod
    def delete_supplier(id):
        """Xóa nhà cung cấp"""
        supplier = Supplier.get_by_id(id)
        if not supplier:
            return False, "Không tìm thấy nhà cung cấp"

        supplier.delete()
        return True, "Xóa thành công" 