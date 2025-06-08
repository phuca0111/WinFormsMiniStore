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

-- Tạo bảng kệ hàng
CREATE TABLE kehang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL
);

-- Tạo bảng sản phẩm
CREATE TABLE sanpham (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL,
    gia REAL NOT NULL,
    theloai_id INTEGER,
    FOREIGN KEY (theloai_id) REFERENCES theloai(id)
);
-- mã vạch sản phẩm (mã vạch EAN/UPC) dùng để định danh duy nhất một loại sản phẩm 
--cụ thể. Tất cả các gói mì cùng loại, cùng hương vị, cùng trọng lượng, và cùng nhà sản xuất thì sẽ có cùng một mã vạch.
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

-- Tạo bảng thể loại sản phẩm
CREATE TABLE theloai (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL
);

-- Tạo bảng sản phẩm của nhà cung cấp
CREATE TABLE nhacungcap_sanpham (
    nhacungcap_id INTEGER,
    sanpham_id INTEGER,
    ngaynhap DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nhacungcap_id, sanpham_id),
    FOREIGN KEY (nhacungcap_id) REFERENCES nhacungcap(id),
    FOREIGN KEY (sanpham_id) REFERENCES sanpham(id)
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
    nhanvien_id INTEGER,
    ngay DATETIME DEFAULT CURRENT_TIMESTAMP,
    tongtien REAL,
    FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id)
);

-- Tạo bảng chi tiết hóa đơn
CREATE TABLE hoadon_chitiet (
    hoadon_id INTEGER,
    bienthe_id INTEGER,
    soluong INTEGER,
    dongia REAL,
    PRIMARY KEY (hoadon_id, bienthe_id),
    FOREIGN KEY (hoadon_id) REFERENCES hoadon(id),
    FOREIGN KEY (bienthe_id) REFERENCES sanpham_bienthe(id)
);

-- Tạo bảng thanh toán
CREATE TABLE thanhtoan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nhanvien_id INTEGER,
    sanpham_id INTEGER,
    soluong INTEGER,
    ngay DATETIME,
    FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id),
    FOREIGN KEY (sanpham_id) REFERENCES sanpham(id)
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