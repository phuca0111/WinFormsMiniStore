import sqlite3
from typing import List, Tuple, Optional
from models.inventory_model import Inventory
import tkinter as tk
from tkinter import messagebox
from Core.barcode_scanner import scan_barcode

def add_inventory(bienthe_id, soluong):
    inventory = Inventory(bienthe_id=bienthe_id, soluong=soluong)
    inventory.save()
    print(f"Đã thêm tồn kho cho biến thể id: {bienthe_id}")

def update_inventory(id, bienthe_id, soluong):
    inventory = Inventory.get_by_id(id)
    if inventory:
        inventory.bienthe_id = bienthe_id
        inventory.soluong = soluong
        inventory.save()
        print(f"Đã cập nhật tồn kho id {id}")
        return True
    else:
        print(f"Không tìm thấy tồn kho với id: {id}")
        return False

def delete_inventory(id):
    inventory = Inventory.get_by_id(id)
    if inventory:
        inventory.delete()
        print(f"Đã xóa tồn kho id: {id}")
        return True
    else:
        print(f"Không tìm thấy tồn kho với id: {id}")
        return False

def get_all_inventory():
    # Lấy danh sách các bản ghi tồn kho từ database
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tk.id, sp.ten, spbt.ten_bienthe, spbt.barcode, tk.soluong, tk.bienthe_id
        FROM tonkho tk
        JOIN sanpham_bienthe spbt ON tk.bienthe_id = spbt.id
        JOIN sanpham sp ON spbt.sanpham_id = sp.id
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_variants():
    # Lấy danh sách biến thể sản phẩm cho combobox
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT spbt.id, sp.ten, spbt.ten_bienthe, spbt.barcode
        FROM sanpham_bienthe spbt
        JOIN sanpham sp ON spbt.sanpham_id = sp.id
    ''')
    variants = cursor.fetchall()
    conn.close()
    return variants

def add_inventory_logic(combobox_variant, entry_soluong, entry_barcode, tree, label_sanpham):
    # Xử lý thêm tồn kho
    # TODO: Bổ sung code thêm tồn kho
    pass

def update_inventory_logic(tree, combobox_variant, entry_soluong, entry_barcode, label_sanpham):
    # Xử lý cập nhật tồn kho
    # TODO: Bổ sung code cập nhật tồn kho
    pass

def delete_inventory_logic(tree, combobox_variant, entry_soluong, entry_barcode, label_sanpham):
    # Xử lý xóa tồn kho
    # TODO: Bổ sung code xóa tồn kho
    pass

def on_barcode_entered_logic(barcode, combobox_variant, label_sanpham):
    # Xử lý khi nhập barcode xong
    # TODO: Bổ sung code xử lý barcode
    pass

def check_existing_variant(barcode: str) -> Optional[Tuple]:
    """Kiểm tra biến thể đã tồn tại theo barcode"""
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sanpham_bienthe WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    return result

def check_existing_inventory(bienthe_id: int) -> Optional[Tuple]:
    """Kiểm tra tồn kho đã tồn tại theo biến thể"""
    conn = sqlite3.connect('Database/ministore_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id, soluong FROM tonkho WHERE bienthe_id = ?", (bienthe_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def add_product_variant(sanpham_id: int, ten_bienthe: str, barcode: str) -> Optional[int]:
    """Thêm mới biến thể sản phẩm"""
    try:
        conn = sqlite3.connect('Database/ministore_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sanpham_bienthe (sanpham_id, ten_bienthe, barcode)
            VALUES (?, ?, ?)
        """, (sanpham_id, ten_bienthe, barcode))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
    except Exception as e:
        print(f"Lỗi khi thêm biến thể: {e}")
        return None

# Các hàm logic xử lý chức năng tồn kho

def load_inventory(tree):
    """Load dữ liệu tồn kho vào treeview"""
    from Core.inventory import get_all_inventory
    for item in tree.get_children():
        tree.delete(item)
    rows = get_all_inventory()
    for row in rows:
        tree.insert('', 'end', values=row)

def load_variant_combobox(combobox):
    """Load dữ liệu biến thể vào combobox"""
    from Core.inventory import get_all_variants
    variants = get_all_variants()
    combobox['values'] = [f"{v[0]} - {v[1]} - {v[2]} - {v[3]}" for v in variants]
    return {v[0]: (v[1], v[2], v[3]) for v in variants}

def on_add(combobox_variant, entry_soluong, entry_barcode, tree):
    from Core.inventory import check_existing_variant, check_existing_inventory, add_inventory, update_inventory
    variant_str = combobox_variant.get()
    soluong = entry_soluong.get().strip()
    barcode = entry_barcode.get().strip()
    if not barcode:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập barcode!')
        return
    if not soluong:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập số lượng!')
        return
    try:
        soluong = int(soluong)
    except:
        messagebox.showwarning('Cảnh báo', 'Số lượng phải là số nguyên!')
        return
    variant = check_existing_variant(barcode)
    if variant:
        bienthe_id = variant[0]
        inventory = check_existing_inventory(bienthe_id)
        if inventory:
            inventory_id, current_quantity = inventory
            new_quantity = current_quantity + soluong
            update_inventory(inventory_id, bienthe_id, new_quantity)
        else:
            add_inventory(bienthe_id, soluong)
    else:
        # KHÔNG tự thêm biến thể mới, chỉ cảnh báo
        messagebox.showwarning('Thông báo', 'Sản phẩm này chưa tồn tại! Vui lòng thêm sản phẩm bên bảng biến thể sản phẩm trước.')
        return
    entry_soluong.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)
    combobox_variant.set('')
    load_inventory(tree)

def on_update(tree, combobox_variant, entry_soluong, entry_barcode):
    from Core.inventory import update_inventory
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn tồn kho để sửa!')
        return
    variant_str = combobox_variant.get()
    soluong = entry_soluong.get().strip()
    barcode = entry_barcode.get().strip()
    if not variant_str or not soluong or not barcode:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin!')
        return
    try:
        soluong = int(soluong)
    except:
        messagebox.showwarning('Cảnh báo', 'Số lượng phải là số nguyên!')
        return
    item = tree.item(selected[0])
    id = item['values'][0]
    bienthe_id = int(variant_str.split(' - ')[0])
    if update_inventory(id, bienthe_id, soluong):
        messagebox.showinfo('Thông báo', 'Đã cập nhật tồn kho thành công!')
    else:
        messagebox.showerror('Lỗi', 'Không thể cập nhật tồn kho!')
    entry_soluong.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)
    combobox_variant.set('')
    load_inventory(tree)

def on_delete(tree, combobox_variant, entry_soluong, entry_barcode):
    from Core.inventory import delete_inventory
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn tồn kho để xóa!')
        return
    if messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn xóa tồn kho này?'):
        item = tree.item(selected[0])
        id = item['values'][0]
        if delete_inventory(id):
            messagebox.showinfo('Thông báo', 'Đã xóa tồn kho thành công!')
        else:
            messagebox.showerror('Lỗi', 'Không thể xóa tồn kho!')
        entry_soluong.delete(0, tk.END)
        entry_barcode.delete(0, tk.END)
        combobox_variant.set('')
        load_inventory(tree)

def on_select(event, tree, combobox_variant, entry_soluong, entry_barcode):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        entry_soluong.delete(0, tk.END)
        entry_soluong.insert(0, item['values'][4])  # Số lượng
        entry_barcode.delete(0, tk.END)
        entry_barcode.insert(0, item['values'][3])  # Barcode
        bienthe_id = item['values'][5]
        for v in combobox_variant['values']:
            if v.startswith(str(bienthe_id) + ' -'):
                combobox_variant.set(v)
                break

def on_scan_barcode(entry_barcode, combobox_variant, label_sanpham):
    barcode = scan_barcode()
    if barcode:
        entry_barcode.delete(0, tk.END)
        entry_barcode.insert(0, barcode)
        on_barcode_entered(barcode, combobox_variant, label_sanpham)

def on_barcode_entered(barcode, combobox_variant, label_sanpham=None):
    from Core.inventory import check_existing_variant, get_all_variants
    import tkinter.messagebox as messagebox
    variants = get_all_variants()
    combobox_variant['values'] = [f"{v[0]} - {v[1]} - {v[2]} - {v[3]}" for v in variants]
    variant = check_existing_variant(barcode)
    if variant:
        bienthe_id = variant[0]
        for v in combobox_variant['values']:
            if v.startswith(str(bienthe_id) + ' -'):
                combobox_variant.set(v)
                if label_sanpham is not None:
                    label_sanpham.config(text=v.split(' - ')[1])
                break
    else:
        messagebox.showwarning('Thông báo', 'Sản phẩm không tồn tại, vui lòng nhập sản phẩm bên Sản phẩm!')
        combobox_variant.set('')
        if label_sanpham is not None:
            label_sanpham.config(text='') 