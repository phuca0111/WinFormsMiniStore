import cv2
from pyzbar import pyzbar

def scan_barcode():
    cap = cv2.VideoCapture(0)
    barcode_data = None
    print("Đưa mã vạch vào trước camera...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow('Barcode Scanner', frame)
            print(f"Đã quét được mã vạch: {barcode_data}")
            cap.release()
            cv2.destroyAllWindows()
            return barcode_data
        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    result = scan_barcode()
    print("Kết quả mã vạch:", result)