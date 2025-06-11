# Core/payment.py

import os
from models.payment_model import CartItem
from models.customer_model import CustomerModel
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import pytz
from datetime import datetime, timedelta
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

cart = []

def get_db_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Database', 'ministore_db.sqlite')

def get_customer_by_phone(phone):
    db_path = get_db_path()
    customer_model = CustomerModel(db_path)
    return customer_model.get_customer_by_phone(phone)

def create_customer_by_phone(name, phone):
    db_path = get_db_path()
    customer_model = CustomerModel(db_path)
    return customer_model.add_customer(name, phone, '', '', '', '')

def reload_cart():
    return get_cart_items(), calculate_total()

def scan_and_add_barcode(scan_barcode_func, barcode=None):
    if barcode is None:
        barcode = scan_barcode_func()
    if barcode:
        add_to_cart(barcode, 1)
    return barcode

def get_product_by_barcode(barcode):
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

def process_payment(customer_name, phone, payment_method, cart_items, total):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # 1. Lưu khách hàng nếu chưa có
        cursor.execute('SELECT id FROM khachhang WHERE sdt = ?', (phone,))
        row = cursor.fetchone()
        if row:
            customer_id = row[0]
        else:
            cursor.execute('INSERT INTO khachhang (ten, sdt) VALUES (?, ?)', (customer_name, phone))
            customer_id = cursor.lastrowid
        # 2. Lưu hóa đơn
        cursor.execute('INSERT INTO hoadon (nhanvien_id, ngay, tongtien) VALUES (?, datetime("now"), ?)', (1, total)) # nhanvien_id tạm thời là 1
        hoadon_id = cursor.lastrowid
        # 3. Lưu chi tiết hóa đơn, cập nhật tồn kho
        for item in cart_items:
            # item: (stt, ten_sanpham, ten_bienthe, soluong, dongia, thanhtien, barcode)
            barcode = item[6]
            soluong = item[3]
            # Lấy id biến thể sản phẩm
            cursor.execute('SELECT id FROM sanpham_bienthe WHERE barcode = ?', (barcode,))
            bienthe_row = cursor.fetchone()
            if not bienthe_row:
                continue
            bienthe_id = bienthe_row[0]
            cursor.execute('INSERT INTO hoadon_chitiet (hoadon_id, bienthe_id, soluong, dongia) VALUES (?, ?, ?, ?)',
                           (hoadon_id, bienthe_id, soluong, item[4]))
            # Trừ tồn kho
            cursor.execute('UPDATE tonkho SET soluong = soluong - ? WHERE bienthe_id = ?', (soluong, bienthe_id))
        # 4. Cập nhật điểm tích lũy (giả sử 1 điểm = 10.000đ)
        diem = int(total // 10000)
        cursor.execute('UPDATE khachhang SET diem_tich_luy = diem_tich_luy + ? WHERE id = ?', (diem, customer_id))
        conn.commit()
        return True, hoadon_id
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

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

def export_invoice_pdf(hoadon_id, tien_khach_dua=None, tien_thoi_lai=None, save_path=None):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Lấy thông tin hóa đơn
    cursor.execute('''
        SELECT hd.id, hd.ngay, hd.tongtien, kh.ten, kh.sdt, tk.username, hd.nhanvien_id
        FROM hoadon hd
        LEFT JOIN nhanvien nv ON hd.nhanvien_id = nv.id
        LEFT JOIN taikhoan tk ON tk.nhanvien_id = nv.id
        LEFT JOIN khachhang kh ON kh.id = (
            SELECT id FROM khachhang WHERE sdt = (
                SELECT sdt FROM khachhang WHERE id = kh.id LIMIT 1
            ) LIMIT 1
        )
        WHERE hd.id = ?
    ''', (hoadon_id,))
    hoadon = cursor.fetchone()
    if not hoadon:
        conn.close()
        return None
    # Lấy chi tiết hóa đơn
    cursor.execute('''
        SELECT sp.ten, bt.ten_bienthe, ct.soluong, ct.dongia
        FROM hoadon_chitiet ct
        JOIN sanpham_bienthe bt ON ct.bienthe_id = bt.id
        JOIN sanpham sp ON bt.sanpham_id = sp.id
        WHERE ct.hoadon_id = ?
    ''', (hoadon_id,))
    chitiet = cursor.fetchall()
    print('Chi tiết hóa đơn:', chitiet)
    conn.close()
    # Thông tin cửa hàng
    store_name = "CỬA HÀNG MINI STORE"
    store_address = "123 Đường ABC, Quận 1, TP.HCM"
    store_phone = "0123 456 789"
    # Tạo file pdf
    if not save_path:
        # Tạo thư mục hoadon nếu chưa tồn tại
        if not os.path.exists('hoadon'):
            os.makedirs('hoadon')
        save_path = os.path.join('hoadon', f"hoadon_{hoadon_id}.pdf")
    c = canvas.Canvas(save_path, pagesize=A4)
    width, height = A4
    y = height - 20*mm
    c.setFont("DejaVu", 16)
    c.drawCentredString(width/2, y, "PHIẾU THANH TOÁN MINI STORE")
    y -= 8*mm
    c.setFont("DejaVu", 10)
    c.drawCentredString(width/2, y, store_address + " | ĐT: " + store_phone)
    y -= 8*mm
    c.setFont("DejaVu", 10)
    c.drawString(15*mm, y, f"Số HĐ: {hoadon[0]}")
    # Chuyển đổi ngày sang múi giờ Việt Nam nếu có
    ngay_str = hoadon[1]
    try:
        dt_utc = datetime.strptime(ngay_str, '%Y-%m-%d %H:%M:%S')
        dt_vn = dt_utc + timedelta(hours=7)
        ngay_vn = dt_vn.strftime('%d/%m/%Y %H:%M:%S')
    except Exception:
        ngay_vn = ngay_str
    c.drawString(70*mm, y, f"Ngày: {ngay_vn}")
    c.drawString(130*mm, y, f"NV: {hoadon[5] if hoadon[5] else hoadon[6]}")
    y -= 8*mm
    c.drawString(15*mm, y, f"Khách hàng: {hoadon[3]} - {hoadon[4]}")
    y -= 8*mm
    c.line(15*mm, y, 195*mm, y)
    y -= 6*mm
    c.setFont("DejaVu-Bold", 11)
    c.drawString(15*mm, y, "SL")
    c.drawString(25*mm, y, "Tên sản phẩm")
    c.drawString(100*mm, y, "Giá bán")
    c.drawString(140*mm, y, "Thành tiền")
    y -= 6*mm
    c.setFont("DejaVu", 10)
    for sp, bienthe, sl, dongia in chitiet:
        c.drawString(15*mm, y, str(sl))
        c.drawString(25*mm, y, f"{sp} ({bienthe})")
        c.drawString(100*mm, y, f"{dongia:,.0f}")
        c.drawString(140*mm, y, f"{sl*dongia:,.0f}")
        y -= 6*mm
        if y < 30*mm:
            c.showPage()
            y = height - 30*mm
    y -= 4*mm
    c.line(15*mm, y, 195*mm, y)
    y -= 8*mm
    c.setFont("DejaVu-Bold", 12)
    c.drawString(100*mm, y, f"Phải thanh toán: {hoadon[2]:,.0f} VND")
    y -= 8*mm
    if tien_khach_dua is not None:
        c.setFont("DejaVu", 11)
        c.drawString(100*mm, y, f"Tiền khách đưa: {tien_khach_dua:,.0f} VND")
        y -= 6*mm
    if tien_thoi_lai is not None:
        c.setFont("DejaVu", 11)
        c.drawString(100*mm, y, f"Tiền thối lại: {tien_thoi_lai:,.0f} VND")
        y -= 6*mm
    y -= 8*mm
    c.setFont("DejaVu", 10)
    c.drawString(15*mm, y, "Cảm ơn Quý khách đã mua hàng tại Mini Store!")
    y -= 6*mm
    c.setFont("DejaVu", 9)
    c.drawString(15*mm, y, "Lưu ý: Quý khách vui lòng kiểm tra hàng hóa và tiền thối lại trước khi rời khỏi quầy.")
    c.save()
    return save_path

pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf')) 