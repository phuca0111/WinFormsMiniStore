-- Tạo bảng trung gian phân quyền nhiều-nhiều cho nhân viên
CREATE TABLE IF NOT EXISTS nhanvien_phanquyen (
    nhanvien_id INTEGER,
    phanquyen_id INTEGER,
    PRIMARY KEY (nhanvien_id, phanquyen_id),
    FOREIGN KEY (nhanvien_id) REFERENCES nhanvien(id),
    FOREIGN KEY (phanquyen_id) REFERENCES phanquyen(id)
); 