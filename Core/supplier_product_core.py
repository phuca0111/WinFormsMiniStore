import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.supplier_product_model import SupplierProduct
from models.supplier_model import Supplier
from models.product_variant_model import ProductVariant

class SupplierProductCore:
    @staticmethod
    def get_all_supplier_products():
        return SupplierProduct.get_all()

    @staticmethod
    def get_supplier_product_by_id(id):
        return SupplierProduct.get_by_id(id)

    @staticmethod
    def create_supplier_product(nhacungcap_id, bienthe_id, soluong_nhap, gia_nhap):
        supplier_product = SupplierProduct(
            nhacungcap_id=nhacungcap_id,
            bienthe_id=bienthe_id,
            soluong_nhap=soluong_nhap,
            gia_nhap=gia_nhap
        )
        supplier_product.save()
        return supplier_product

    @staticmethod
    def update_supplier_product(id, nhacungcap_id, bienthe_id, soluong_nhap, gia_nhap):
        supplier_product = SupplierProduct.get_by_id(id)
        if supplier_product:
            supplier_product.nhacungcap_id = nhacungcap_id
            supplier_product.bienthe_id = bienthe_id
            supplier_product.soluong_nhap = soluong_nhap
            supplier_product.gia_nhap = gia_nhap
            supplier_product.save()
            return True
        return False

    @staticmethod
    def delete_supplier_product(id):
        supplier_product = SupplierProduct.get_by_id(id)
        if supplier_product:
            supplier_product.delete()
            return True
        return False

    @staticmethod
    def get_all_suppliers():
        return Supplier.get_all()

    @staticmethod
    def get_all_product_variants():
        return ProductVariant.get_all() 