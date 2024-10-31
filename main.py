import sys, os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtGui import QIcon
from Router.navigate import Navbar
from Controller.main import Controller
from Pages.components.path import Path

from datetime import datetime, timedelta

basedir = os.path.dirname(__file__)

APP_NAME = "Project Management"

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = "rindev.projectmanager.subprojectmanager.1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class FullScreenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout containing stacked widget and navbar
        main_layout = QVBoxLayout(self.central_widget)
        logo_path = Path().path_logo()
        icon = QIcon(logo_path)
        # Setting application icon
        self.setWindowIcon(icon)

        # Stacked widget to manage pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Controller to manage page switching
        self.controller = Controller(self.stacked_widget)
        # self.controller.set_main_widget()

        # Initially show the home page
        # self.controller.show_home_page()

        # Add Navbar widget
        navbar = Navbar(self.controller)
        main_layout.addWidget(navbar)
        # Set focus to the main window or another widget to remove focus from the button
        self.setFocus()

        # Make the window fullscreen
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FullScreenApp()
    sys.exit(app.exec())
