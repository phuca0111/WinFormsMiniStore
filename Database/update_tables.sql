-- Xóa bảng thanhtoan nếu tồn tại
DROP TABLE IF EXISTS thanhtoan;

-- Xóa bảng hoadon_chitiet cũ
DROP TABLE IF EXISTS hoadon_chitiet;

-- Tạo bảng hoadon_chitiet mới với đầy đủ cột
CREATE TABLE hoadon_chitiet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hoadon_id INTEGER,
    bienthe_id INTEGER,
    ten_hang TEXT,
    soluong INTEGER,
    dongia REAL,
    thanh_tien REAL,
    gia_nhap REAL,
    loi_lo REAL,
    FOREIGN KEY (hoadon_id) REFERENCES hoadon(id),
    FOREIGN KEY (bienthe_id) REFERENCES sanpham_bienthe(id)
);

-- Thêm cột gia_nhap vào bảng nhacungcap_sanpham
ALTER TABLE nhacungcap_sanpham ADD COLUMN gia_nhap REAL; 