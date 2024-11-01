import sys, os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
)
from PySide6.QtGui import QIcon
from Router.navigate import Navbar
from Controller.main import Controller
from Pages.components.path import Path
from Pages.components.stylesheet import css_button_submit, css_lable, css_title

basedir = os.path.dirname(__file__)
APP_NAME = "Project Management"

try:
    from ctypes import windll  # Only exists on Windows

    myappid = "rindev.projectmanager.subprojectmanager.1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class AppSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        file_path = os.path.join(basedir, "type_pm.txt")
        with open(file_path, "r") as file:
            content = file.read().strip()  # Read the file content and strip whitespace
            self.type_pm = int(content)
        logo_path = Path().path_logo()
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )

        type_count = (
            "1a Số"
            if self.type_pm == 1
            else (
                "2 Số"
                if self.type_pm == 2
                else "trắng" if self.type_pm == 0 else "1b Số"
            )
        )

        type_count_label = (
            "1a"
            if self.type_pm == 1
            else ("2" if self.type_pm == 2 else "0" if self.type_pm == 0 else "1b")
        )
        layout = QVBoxLayout(self)
        label = QLabel(
            f"Đây là bảng chọn của Bộ {type_count}\nXin vui lòng chọn PM để sử dụng:"
        )
        label.setStyleSheet(css_title)
        layout.addWidget(label)

        # Create a QListWidget for the list of apps
        self.app_list = QListWidget()
        self.app_list.setStyleSheet(css_lable)
        layout.addWidget(self.app_list)

        # Add 30 apps to the list
        for i in range(1, 31):
            self.app_list.addItem(f"PM {type_count_label}.{i}/30")

        # Button to confirm selection
        self.confirm_button = QPushButton("Khởi Chạy PM")
        self.confirm_button.setStyleSheet(css_button_submit)
        layout.addWidget(self.confirm_button)

        # Connect button to accept and save selected app
        self.confirm_button.clicked.connect(self.select_app)

        self.selected_app = None
        self.selected_index = None

    def select_app(self):
        selected_item = self.app_list.currentItem()
        if selected_item:
            self.selected_app = selected_item.text()
            self.selected_index = self.app_list.currentRow()
            self.accept()


class FullScreenApp(QMainWindow):
    def __init__(self, index):
        super().__init__()
        file_path = os.path.join(basedir, "type_pm.txt")
        with open(file_path, "r") as file:
            content = file.read().strip()  # Read the file content and strip whitespace
            self.type_pm = int(content)
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout containing stacked widget and navbar
        main_layout = QVBoxLayout(self.central_widget)
        logo_path = Path().path_logo()
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)

        type_count = (
            "1a Số"
            if self.type_pm == 1
            else (
                "2 Số"
                if self.type_pm == 2
                else "trắng" if self.type_pm == 0 else "1b Số"
            )
        )

        label = QLabel(f"Bộ {type_count} - PM {index}/30")
        label.setStyleSheet(css_title)
        main_layout.addWidget(label)

        # Stacked widget to manage pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Controller to manage page switching
        self.controller = Controller(self.stacked_widget)

        # Add Navbar widget
        navbar = Navbar(self.controller)
        main_layout.addWidget(navbar)
        self.setFocus()

        # Make the window fullscreen
        self.show()


def modify_text_file(index, type_count):
    # Modify a file based on the selected index
    file_path = os.path.join(basedir, "path_file.txt")
    skip = (
        0
        if type_count == 1
        else 30 if type_count == 2 else 60 if type_count == 3 else 90
    )
    with open(file_path, "w") as file:
        file.write(f"C:/data/{index + skip}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show the app selection dialog
    selection_dialog = AppSelectionDialog()
    if selection_dialog.exec() == QDialog.Accepted:
        # Run main application only if the user made a selection
        if selection_dialog.selected_app:
            index = selection_dialog.selected_index + 1
            type_count = selection_dialog.type_pm
            modify_text_file(index, type_count)
            mainWindow = FullScreenApp(index)
            sys.exit(app.exec())
