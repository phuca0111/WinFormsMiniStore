-- Tạo bảng phân quyền
CREATE TABLE phanquyen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenquyen TEXT UNIQUE NOT NULL
);

-- Tạo bảng nhân viên
CREATE TABLE nhanvien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL,
    sdt TEXT,
    gmail TEXT,
    gioitinh TEXT,
    ngaysinh DATE,
    phanquyen_id INTEGER,
    FOREIGN KEY (phanquyen_id) REFERENCES phanquyen(id)
);

-- Tạo bảng tài khoản đăng nhập
CREATE TABLE taikhoan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nhanvien_id INTEGER NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    trangthai TEXT DEFAULT 'active',
    FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id)
);

-- Tạo bảng khách hàng
CREATE TABLE khachhang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL,
    sdt TEXT UNIQUE,
    gmail TEXT,
    diachi TEXT,
    ngaysinh DATE,
    gioitinh TEXT,
    diem_tich_luy INTEGER DEFAULT 0
);

-- Tạo bảng kệ hàng
-- id: tự động tăng
-- ten: tên kệ hàng
-- tên kệ A-2 kệ A hàng 2 từ dưới đếm lên
CREATE TABLE kehang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL
);

-- Tạo bảng hãng sản xuất
CREATE TABLE hangsanxuat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL
);

-- Tạo bảng thể loại sản phẩm
CREATE TABLE theloai (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL
);

-- Tạo bảng sản phẩm
CREATE TABLE sanpham (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL,
    theloai_id INTEGER,
    hangsanxuat_id INTEGER,
    FOREIGN KEY (theloai_id) REFERENCES theloai(id),
    FOREIGN KEY (hangsanxuat_id) REFERENCES hangsanxuat(id)
);

-- Tạo bảng biến thể sản phẩm
CREATE TABLE sanpham_bienthe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sanpham_id INTEGER NOT NULL,
    ten_bienthe TEXT,
    gia REAL,
    barcode TEXT,
    FOREIGN KEY (sanpham_id) REFERENCES sanpham(id)
);

-- Tạo bảng sản phẩm trên kệ
CREATE TABLE kehang_sanpham (
    kehang_id INTEGER,
    sanpham_id INTEGER,
    soluong INTEGER DEFAULT 0,
    PRIMARY KEY (kehang_id, sanpham_id),
    FOREIGN KEY (kehang_id) REFERENCES kehang(id),
    FOREIGN KEY (sanpham_id) REFERENCES sanpham(id)
);

-- Tạo bảng nhà cung cấp
CREATE TABLE nhacungcap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL,
    diachi TEXT,
    sdt TEXT,
    gmail TEXT
);

-- Tạo bảng sản phẩm của nhà cung cấp
CREATE TABLE nhacungcap_sanpham (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nhacungcap_id INTEGER,
    bienthe_id INTEGER,
    ngaynhap DATETIME DEFAULT CURRENT_TIMESTAMP,
    soluong_nhap INTEGER DEFAULT 0,
    FOREIGN KEY (nhacungcap_id) REFERENCES nhacungcap(id),
    FOREIGN KEY (bienthe_id) REFERENCES sanpham_bienthe(id)
);

-- Tạo bảng tồn kho
CREATE TABLE tonkho (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bienthe_id INTEGER NOT NULL,
    soluong INTEGER DEFAULT 0,
    FOREIGN KEY (bienthe_id) REFERENCES sanpham_bienthe(id),
    UNIQUE (bienthe_id)
);

-- Tạo bảng hóa đơn
CREATE TABLE hoadon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ma_hoa_don TEXT,
    nhanvien_id INTEGER,
    ngay DATETIME DEFAULT CURRENT_TIMESTAMP,
    tongtien REAL,
    tien_lam_tron INTEGER,
    tien_khach_dua INTEGER,
    tien_thoi_lai INTEGER,
    FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id)
);

-- Tạo bảng chi tiết hóa đơn
CREATE TABLE hoadon_chitiet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hoadon_id INTEGER,
    bienthe_id INTEGER,
    ten_hang TEXT,
    soluong INTEGER,
    dongia REAL,
    thanh_tien REAL,
    FOREIGN KEY (hoadon_id) REFERENCES hoadon(id),
    FOREIGN KEY (bienthe_id) REFERENCES sanpham_bienthe(id)
);

-- Tạo bảng log đăng nhập nhân viên
CREATE TABLE nhanvien_login_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nhanvien_id INTEGER NOT NULL,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id)
);

-- Tạo bảng log truy cập sản phẩm
CREATE TABLE sanpham_login_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sanpham_id INTEGER NOT NULL,
    nhanvien_id INTEGER,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sanpham_id) REFERENCES sanpham(id),
    FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id)
); 