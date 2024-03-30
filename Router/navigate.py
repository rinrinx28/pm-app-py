from PySide6 import QtWidgets
from PySide6.QtGui import Qt, QCursor
class Navbar(QtWidgets.QWidget):
    def __init__(self, controller):  # Fix the typo here from `seft` to `self`
        super().__init__()
        self.controller = controller
        layout = QtWidgets.QHBoxLayout()

        self.setLayout(layout)  # Set the layout for the widget
        css = "QPushButton {padding: 5px;border-radius: 2px; border-width: 1px; border-color: #E5E7EB; font-size: 24px; color: #111827; background-color: #ffffff;}"
        # Add Button;
        home = QtWidgets.QPushButton("Trang chủ")
        home.setStyleSheet(css+"QPushButton:hover {color: #1D4ED8;background-color: #F3F4F6;}")
        home.setCursor(QCursor(Qt.PointingHandCursor))
    
        layout.addWidget(home)

        b_ngang = QtWidgets.QPushButton('B Ngang')
        b_ngang.setStyleSheet(css+"QPushButton:hover {color: #1D4ED8;background-color: #F3F4F6;}")
        b_ngang.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(b_ngang)

        b_thong_so = QtWidgets.QPushButton('B Thông Số')
        b_thong_so.setStyleSheet(css+"QPushButton:hover {color: #1D4ED8;background-color: #F3F4F6;}")
        b_thong_so.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(b_thong_so)

        # bans = QtWidgets.QPushButton("Danh sách Bản")
        # bans.setStyleSheet(css+"QPushButton:hover {color: #1D4ED8;background-color: #F3F4F6;}")
        # bans.setCursor(QCursor(Qt.PointingHandCursor))
        # layout.addWidget(bans)

        b_tinh_mau = QtWidgets.QPushButton('B Tính Và B Màu')
        b_tinh_mau.setStyleSheet(css+"QPushButton:hover {color: #1D4ED8;background-color: #F3F4F6;}")
        b_tinh_mau.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(b_tinh_mau)

        exit = QtWidgets.QPushButton('Thoát')
        exit.setStyleSheet(css+"QPushButton:hover {color: #1D4ED8;background-color: #F3F4F6;}")
        exit.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(exit)


        # Connect the exit_button's clicked signal to the exit_application function
        exit.clicked.connect(self.exit_application)
        home.clicked.connect(self.homepage)
        b_ngang.clicked.connect(self.ngangpage)
        b_thong_so.clicked.connect(self.thongpage)
        # bans.clicked.connect(self.listbanpage)
        b_tinh_mau.clicked.connect(self.tinhvamaupage)

    def exit_application(self):
        QtWidgets.QApplication.quit()  # Exit the application when the button is clicked
    
    def homepage(self):
        self.controller.show_home_page()

    def ngangpage(self):
        self.controller.show_ngang_page()
    
    def thongpage(self):
        self.controller.show_thong_page()
    
    # def listbanpage(self):
    #     self.controller.show_list_ban_page()
    
    def tinhvamaupage(self):
        self.controller.show_tinh_mau_page()
