from models.payment_model import CartItem

cart = []

def get_product_by_barcode(barcode):
    import sqlite3
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sp.ten, spbt.ten_bienthe, spbt.barcode, spbt.gia
        FROM sanpham_bienthe spbt
        JOIN sanpham sp ON spbt.sanpham_id = sp.id
        WHERE spbt.barcode = ?
    ''', (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result:
        ten_sanpham, ten_bienthe, barcode, dongia = result
        return {
            'ten_sanpham': ten_sanpham,
            'ten_bienthe': ten_bienthe,
            'barcode': barcode,
            'dongia': dongia if dongia else 0
        }
    return None

def add_to_cart(barcode, quantity):
    product = get_product_by_barcode(barcode)
    if product:
        for item in cart:
            if str(item.barcode).strip() == str(barcode).strip():
                item.soluong += quantity
                item.thanhtien = item.soluong * item.dongia
                return
        stt = len(cart) + 1
        dongia = product['dongia']
        thanhtien = quantity * dongia
        cart.append(CartItem(stt, product['ten_sanpham'], product['ten_bienthe'], quantity, dongia, thanhtien, barcode))

def get_cart_items():
    return [(
        item.stt, item.ten_sanpham, item.ten_bienthe, item.soluong, item.dongia, item.thanhtien, item.barcode
    ) for item in cart]

def calculate_total():
    return sum(item.thanhtien for item in cart)

def clear_cart():
    global cart
    cart = []

def update_cart_item(barcode, new_quantity):
    for item in cart:
        if str(item.barcode).strip() == str(barcode).strip():
            item.soluong = new_quantity
            item.thanhtien = item.soluong * item.dongia
            break

def remove_from_cart(barcode):
    global cart
    cart = [item for item in cart if str(item.barcode).strip() != str(barcode).strip()]
    for i, item in enumerate(cart, 1):
        item.stt = i 