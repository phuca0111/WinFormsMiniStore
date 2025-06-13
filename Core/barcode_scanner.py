import cv2
from pyzbar import pyzbar

def scan_barcode():
    cap = cv2.VideoCapture(0)
    barcode_data = None
    window_name = 'Barcode Scanner'
    print("Đưa mã vạch vào trước camera... (Nhấn phím 1 hoặc đóng cửa sổ để thoát)")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        # Kiểm tra nếu cửa sổ bị đóng bằng dấu X
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
        if key == ord('1'):
            break
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow(window_name, frame)
            print(f"Đã quét được mã vạch: {barcode_data}")
            cap.release()
            cv2.destroyAllWindows()
            return barcode_data
    cap.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    result = scan_barcode()
    print("Kết quả mã vạch:", result)