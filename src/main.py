import tkinter as tk
from views.main_window import MainWindow
from views.login_view import show_login
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def main():
    def start_main(user_info):
        root = tk.Tk()
        app = MainWindow(root, user_info)
        root.mainloop()
    show_login(start_main)

pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))

if __name__ == "__main__":
    main()