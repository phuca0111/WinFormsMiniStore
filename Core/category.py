from models.category_model import Category

def add_category(ten):
    category = Category(ten=ten)
    category.save()
    print(f"Đã thêm thể loại: {ten}")

def update_category(id, ten_moi):
    category = Category.get_by_id(id)
    if category:
        category.ten = ten_moi
        category.save()
        print(f"Đã cập nhật thể loại id {id} thành: {ten_moi}")
    else:
        print(f"Không tìm thấy thể loại với id: {id}")

def delete_category(id):
    category = Category.get_by_id(id)
    if category:
        category.delete()
        print(f"Đã xóa thể loại id: {id}")
    else:
        print(f"Không tìm thấy thể loại với id: {id}")

def get_all_categories():
    return Category.get_all()
