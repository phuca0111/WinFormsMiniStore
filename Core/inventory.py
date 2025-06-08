from models.inventory_model import Inventory

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
    else:
        print(f"Không tìm thấy tồn kho với id: {id}")

def delete_inventory(id):
    inventory = Inventory.get_by_id(id)
    if inventory:
        inventory.delete()
        print(f"Đã xóa tồn kho id: {id}")
    else:
        print(f"Không tìm thấy tồn kho với id: {id}")

def get_all_inventory():
    return Inventory.get_all() 