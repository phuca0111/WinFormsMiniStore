from models.producer_model import Producer

def add_producer(ten):
    producer = Producer(ten=ten)
    producer.save()
    print(f"Đã thêm hãng sản xuất: {ten}")

def update_producer(id, ten_moi):
    producer = Producer.get_by_id(id)
    if producer:
        producer.ten = ten_moi
        producer.save()
        print(f"Đã cập nhật hãng sản xuất id {id} thành: {ten_moi}")
    else:
        print(f"Không tìm thấy hãng sản xuất với id: {id}")

def delete_producer(id):
    producer = Producer.get_by_id(id)
    if producer:
        producer.delete()
        print(f"Đã xóa hãng sản xuất id: {id}")
    else:
        print(f"Không tìm thấy hãng sản xuất với id: {id}")

def get_all_producers():
    return Producer.get_all() 