# models/payment_model.py

class CartItem:
    def __init__(self, stt, ten_sanpham, ten_bienthe, soluong, dongia, thanhtien, barcode):
        self.stt = stt
        self.ten_sanpham = ten_sanpham
        self.ten_bienthe = ten_bienthe
        self.soluong = soluong
        self.dongia = dongia
        self.thanhtien = thanhtien
        self.barcode = barcode

class Payment:
    def __init__(self, customer_name, phone, total, payment_method, cart_items):
        self.customer_name = customer_name
        self.phone = phone
        self.total = total
        self.payment_method = payment_method
        self.cart_items = cart_items 

    def update_cart_item(self, barcode, new_quantity):
        for item in self.cart_items:
            if str(item.barcode).strip() == str(barcode).strip():
                item.soluong = new_quantity
                item.thanhtien = item.soluong * item.dongia
                break 

    def remove_from_cart(self, barcode):
        self.cart_items = [item for item in self.cart_items if str(item.barcode).strip() != str(barcode).strip()]
        # Cập nhật lại STT
        for i, item in enumerate(self.cart_items, 1):
            item.stt = i 