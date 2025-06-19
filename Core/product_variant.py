from models.product_variant_model import ProductVariant
import sqlite3

def is_barcode_exists(barcode, exclude_id=None):
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    if exclude_id:
        cursor.execute("SELECT id FROM sanpham_bienthe WHERE barcode = ? AND id != ?", (barcode, exclude_id))
    else:
        cursor.execute("SELECT id FROM sanpham_bienthe WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_product_variant(sanpham_id, ten_bienthe, gia, barcode):
    if is_barcode_exists(barcode):
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Mã vạch đã tồn tại!")
        return False
    variant = ProductVariant(sanpham_id=sanpham_id, ten_bienthe=ten_bienthe, gia=gia, barcode=barcode)
    variant.save()
    print(f"Đã thêm biến thể sản phẩm: {ten_bienthe}")
    return True

def update_product_variant(id, sanpham_id, ten_bienthe, gia, barcode):
    if is_barcode_exists(barcode, id):
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Mã vạch đã tồn tại ở biến thể khác!")
        return False
    variant = ProductVariant.get_by_id(id)
    if variant:
        variant.sanpham_id = sanpham_id
        variant.ten_bienthe = ten_bienthe
        variant.gia = gia
        variant.barcode = barcode
        variant.save()
        print(f"Đã cập nhật biến thể id {id} thành: {ten_bienthe}")
        return True
    else:
        print(f"Không tìm thấy biến thể với id: {id}")
        return False

def delete_product_variant(id):
    variant = ProductVariant.get_by_id(id)
    if variant:
        variant.delete()
        print(f"Đã xóa biến thể id: {id}")
    else:
        print(f"Không tìm thấy biến thể với id: {id}")

def get_all_product_variants():
    return ProductVariant.get_all() 