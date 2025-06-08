from models.product_variant_model import ProductVariant

def add_product_variant(sanpham_id, ten_bienthe, gia, barcode):
    variant = ProductVariant(sanpham_id=sanpham_id, ten_bienthe=ten_bienthe, gia=gia, barcode=barcode)
    variant.save()
    print(f"Đã thêm biến thể sản phẩm: {ten_bienthe}")

def update_product_variant(id, sanpham_id, ten_bienthe, gia, barcode):
    variant = ProductVariant.get_by_id(id)
    if variant:
        variant.sanpham_id = sanpham_id
        variant.ten_bienthe = ten_bienthe
        variant.gia = gia
        variant.barcode = barcode
        variant.save()
        print(f"Đã cập nhật biến thể id {id} thành: {ten_bienthe}")
    else:
        print(f"Không tìm thấy biến thể với id: {id}")

def delete_product_variant(id):
    variant = ProductVariant.get_by_id(id)
    if variant:
        variant.delete()
        print(f"Đã xóa biến thể id: {id}")
    else:
        print(f"Không tìm thấy biến thể với id: {id}")

def get_all_product_variants():
    return ProductVariant.get_all() 