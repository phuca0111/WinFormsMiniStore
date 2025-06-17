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
from Core.edit_delete_log_core import log_ban_hang

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

def get_fifo_gia_nhap_and_update(cursor, bienthe_id, soluong_ban):
    '''
    Trả về giá nhập trung bình theo FIFO cho số lượng bán của một biến thể sản phẩm,
    đồng thời cập nhật so_luong_con_lai cho từng lô.
    '''
    cursor.execute('''
        SELECT id, so_luong_con_lai, gia_nhap
        FROM nhacungcap_sanpham
        WHERE bienthe_id = ? AND so_luong_con_lai > 0
        ORDER BY ngaynhap ASC, id ASC
    ''', (bienthe_id,))
    rows = cursor.fetchall()
    so_luong_can = soluong_ban
    tong_chi_phi = 0
    tong_so_luong = 0
    for row in rows:
        lo_id = row[0]
        so_luong_con_lai = row[1]
        gia_nhap = row[2]
        if so_luong_can <= 0:
            break
        lay_tu_lo = min(so_luong_can, so_luong_con_lai)
        tong_chi_phi += lay_tu_lo * gia_nhap
        tong_so_luong += lay_tu_lo
        # Cập nhật lại số lượng còn lại của lô
        cursor.execute('UPDATE nhacungcap_sanpham SET so_luong_con_lai = so_luong_con_lai - ? WHERE id = ?', (lay_tu_lo, lo_id))
        so_luong_can -= lay_tu_lo
    if tong_so_luong == 0:
        return 0
    return tong_chi_phi / tong_so_luong

def process_payment(customer_name, phone, payment_method, cart_items, total, tien_khach_dua=0, tien_thoi_lai=0, nhanvien_id=1, store_id=None):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Tính tổng số lượng từng biến thể trong giỏ hàng
        variant_qty = {}
        variant_name = {}
        for item in cart_items:
            barcode = item[6]
            soluong = item[3]
            # Lấy id biến thể sản phẩm
            cursor.execute('SELECT id, ten_bienthe FROM sanpham_bienthe WHERE barcode = ?', (barcode,))
            bienthe_row = cursor.fetchone()
            if not bienthe_row:
                continue
            bienthe_id = bienthe_row[0]
            ten_bienthe = bienthe_row[1]
            if bienthe_id not in variant_qty:
                variant_qty[bienthe_id] = 0
                variant_name[bienthe_id] = ten_bienthe
            variant_qty[bienthe_id] += soluong
        # Kiểm tra tổng số lượng từng biến thể với tồn kho
        for bienthe_id, tong_soluong in variant_qty.items():
            cursor.execute('SELECT soluong FROM tonkho WHERE bienthe_id = ?', (bienthe_id,))
            row = cursor.fetchone()
            tonkho = row[0] if row else 0
            if tong_soluong > tonkho:
                return False, f"Tổng số lượng thanh toán của biến thể '{variant_name[bienthe_id]}' vượt quá tồn kho ({tonkho})!"
        # 1. Lưu khách hàng nếu có thông tin
        customer_id = None
        if phone:
            cursor.execute('SELECT id FROM khachhang WHERE sdt = ?', (phone,))
            row = cursor.fetchone()
            if row:
                customer_id = row[0]
            else:
                cursor.execute('INSERT INTO khachhang (ten, sdt) VALUES (?, ?)', (customer_name, phone))
                customer_id = cursor.lastrowid

        # 2. Tạo mã hóa đơn
        cursor.execute('SELECT COUNT(*) FROM hoadon')
        count = cursor.fetchone()[0]
        ma_hoa_don = f"HD{datetime.now().strftime('%Y%m%d')}{count+1:04d}"

        # Lấy thời gian hiện tại theo giờ Việt Nam
        vn_now = (datetime.utcnow() + timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')

        # 3. Lưu hóa đơn (thêm khachhang_id, store_id)
        cursor.execute('''
            INSERT INTO hoadon (
                ma_hoa_don, nhanvien_id, khachhang_id, ngay, tongtien, 
                tien_lam_tron, tien_khach_dua, tien_thoi_lai, store_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ma_hoa_don, nhanvien_id, customer_id, vn_now, total, round(total), tien_khach_dua, tien_thoi_lai, store_id))
        hoadon_id = cursor.lastrowid

        # 4. Lưu chi tiết hóa đơn, cập nhật tồn kho
        for item in cart_items:
            # item: (stt, ten_sanpham, ten_bienthe, soluong, dongia, thanhtien, barcode)
            barcode = item[6]
            soluong = item[3]
            dongia = item[4]
            thanh_tien = item[5]
            ten_hang = f"{item[1]} ({item[2]})"  # Tên sản phẩm (Tên biến thể)

            # Lấy id biến thể sản phẩm
            cursor.execute('SELECT id FROM sanpham_bienthe WHERE barcode = ?', (barcode,))
            bienthe_row = cursor.fetchone()
            if not bienthe_row:
                continue
            bienthe_id = bienthe_row[0]

            # Tính giá nhập FIFO và cập nhật tồn kho từng lô
            gia_nhap_fifo = get_fifo_gia_nhap_and_update(cursor, bienthe_id, soluong)

            # Lưu chi tiết hóa đơn
            cursor.execute('''
                INSERT INTO hoadon_chitiet (
                    hoadon_id, bienthe_id, ten_hang, soluong, dongia, thanh_tien, gia_nhap
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (hoadon_id, bienthe_id, ten_hang, soluong, dongia, thanh_tien, gia_nhap_fifo))

            # Không cần trừ tồn kho tổng nữa vì đã trừ theo lô

        # 5. Cập nhật điểm tích lũy nếu có khách hàng
        if customer_id:
            diem = int(total // 10000)
            cursor.execute('UPDATE khachhang SET diem_tich_luy = diem_tich_luy + ? WHERE id = ?', (diem, customer_id))

        conn.commit()
        # Lấy tên nhân viên thao tác từ nhanvien_id
        cursor.execute('SELECT ten FROM nhanvien WHERE id = ?', (nhanvien_id,))
        row_nv = cursor.fetchone()
        nguoi_thao_tac = row_nv[0] if row_nv else 'Chưa xác định'
        # Ghi log bán hàng cho từng sản phẩm
        for item in cart_items:
            # item: (stt, ten_sanpham, ten_bienthe, soluong, dongia, thanhtien, barcode)
            ma_san_pham = item[6]
            ten_san_pham = f"{item[1]} ({item[2]})"
            so_luong = item[3]
            don_gia = item[4]
            thanh_tien = item[5]
            loai_xuat = 'bán'
            log_ban_hang(nguoi_thao_tac, ma_san_pham, ten_san_pham, so_luong, don_gia, thanh_tien, loai_xuat)
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
    # Lấy thông tin hóa đơn (thêm store_id)
    cursor.execute('''
        SELECT hd.id, hd.ngay, hd.tongtien, kh.ten, kh.sdt, tk.username, nv.ten, hd.store_id
        FROM hoadon hd
        LEFT JOIN nhanvien nv ON hd.nhanvien_id = nv.id
        LEFT JOIN taikhoan tk ON tk.nhanvien_id = nv.id
        LEFT JOIN khachhang kh ON hd.khachhang_id = kh.id
        WHERE hd.id = ?
    ''', (hoadon_id,))
    hoadon = cursor.fetchone()
    if not hoadon:
        conn.close()
        return None
    store_id = hoadon[7]
    # Lấy thông tin cửa hàng từ bảng thongtincuahang
    store_name = "CỬA HÀNG MINI STORE"
    store_address = ""
    store_phone = ""
    if store_id:
        cursor.execute("SELECT ten_cua_hang, dia_chi, so_dien_thoai FROM thongtincuahang WHERE id = ?", (store_id,))
        store_info = cursor.fetchone()
        if store_info:
            store_name, store_address, store_phone = store_info
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
    c.drawCentredString(width/2, y, f"PHIẾU THANH TOÁN {store_name.upper()}")
    y -= 8*mm
    c.setFont("DejaVu", 10)
    c.drawCentredString(width/2, y, (store_address or "") + (f" | ĐT: {store_phone}" if store_phone else ""))
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
    # Thông tin khách hàng
    khach_hang = hoadon[3] if hoadon[3] else "---"
    sdt = hoadon[4] if hoadon[4] else ""
    c.drawString(15*mm, y, f"Khách hàng: {khach_hang}{(' - ' + sdt) if sdt else ''}")
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