from models.product_model import Product

def add_product(ten, theloai_id, hangsanxuat_id):
    product = Product(ten=ten, theloai_id=theloai_id, hangsanxuat_id=hangsanxuat_id)
    product.save()
    print(f"Đã thêm sản phẩm: {ten}")

def update_product(id, ten_moi, theloai_id_moi, hangsanxuat_id_moi):
    product = Product.get_by_id(id)
    if product:
        product.ten = ten_moi
        product.theloai_id = theloai_id_moi
        product.hangsanxuat_id = hangsanxuat_id_moi
        product.save()
        print(f"Đã cập nhật sản phẩm id {id} thành: {ten_moi}")
    else:
        print(f"Không tìm thấy sản phẩm với id: {id}")

def delete_product(id):
    product = Product.get_by_id(id)
    if product:
        product.delete()
        print(f"Đã xóa sản phẩm id: {id}")
    else:
        print(f"Không tìm thấy sản phẩm với id: {id}")

def get_all_products():
    return Product.get_all()
