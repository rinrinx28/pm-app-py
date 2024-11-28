from PySide6 import QtWidgets
from PySide6.QtGui import Qt, QCursor

css_custom_view = """
    QPushButton {
        border-radius: 8px;
        font-size: 24px;
        line-height: 32px;
        font-weight: 600;
        background-color: rgb(178, 255, 255);
        padding: 8px;
        color: #000;
    }
"""


class Navbar(QtWidgets.QWidget):
    def __init__(self, controller, main):  # Fix the typo here from `seft` to `self`
        super().__init__()
        self.controller = controller
        self.main = main
        layout = QtWidgets.QHBoxLayout()

        self.setLayout(layout)  # Set the layout for the widget
        # Add Button;
        home = QtWidgets.QPushButton("Trang chủ")
        home.setStyleSheet(css_custom_view)
        home.setCursor(QCursor(Qt.PointingHandCursor))

        b_ngang = QtWidgets.QPushButton("B Ngang")
        b_ngang.setStyleSheet(css_custom_view)
        b_ngang.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(b_ngang)

        b_thong_so = QtWidgets.QPushButton("B Thông Số")
        b_thong_so.setStyleSheet(css_custom_view)
        b_thong_so.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(b_thong_so)

        b_tinh_mau = QtWidgets.QPushButton("B Tính Và B Màu")
        b_tinh_mau.setStyleSheet(css_custom_view)
        b_tinh_mau.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(b_tinh_mau)

        exit = QtWidgets.QPushButton("Thoát")
        exit.setStyleSheet(css_custom_view)
        exit.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(exit)

        # Connect the exit_button's clicked signal to the exit_application function
        exit.clicked.connect(self.exit_application)
        home.clicked.connect(self.homepage)
        b_ngang.clicked.connect(self.ngangpage)
        b_thong_so.clicked.connect(self.thongpage)
        b_tinh_mau.clicked.connect(self.tinhvamaupage)

    def exit_application(self):
        self.main.open_apps.clear()
        self.main.close()

    def homepage(self):
        self.controller.show_home_page()

    def ngangpage(self):
        self.controller.show_ngang_page()

    def thongpage(self):
        self.controller.show_thong_page()

    def tinhvamaupage(self):
        self.controller.show_tinh_mau_page()
