import sys
import os
from datetime import datetime, timedelta
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QDialog,
    QLabel,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QLineEdit,
)
from PySide6.QtGui import QIcon
from PySide6.QtGui import Qt, QCursor
from Router.navigate import Navbar
from Controller.main import Controller
from Pages.components.path import Path
from Pages.components.stylesheet import (
    css_button_submit,
    css_title,
    SendMessage,
)
import json

# from PySide6.QtCore import QRect

basedir = os.path.dirname(__file__)
data_sp_dir = "C:/data_sp"
APP_NAME = "Project Management"

# Set up unique application ID on Windows
try:
    from ctypes import windll  # Only exists on Windows

    myappid = "rindev.projectmanager.subprojectmanager.1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

css_custom_view = """
    QPushButton {
        border-radius: 8px;
        font-size: 32px;
        line-height: 32px;
        font-weight: 600;
        background-color: rgb(178, 255, 255);
        padding: 8px;
        color: #000;
    }
"""

css_custom_btn_pwd = """
    QPushButton {
        border-radius: 8px;
        font-size: 24px;
        font-weight: 600;
        background-color: rgb(178, 255, 255);
        padding: 4px;
        color: #000;
    }
"""
css_custom_normal = """
    QPushButton {
        border-radius: 8px;
        font-size: 32px;
        line-height: 32px;
        font-weight: 600;
        background-color: #D3D3D3;
        padding: 8px;
        color: #000;
    }
"""
css_custom_opened = """
    QPushButton {
        border-radius: 8px;
        font-size: 32px;
        line-height: 32px;
        font-weight: 600;
        background-color: #FFD700;
        padding: 8px;
        color: #000;
    }
"""


class AppSelectionDialog(QDialog):
    def __init__(self, opened_apps):
        super().__init__()
        # List to keep track of opened apps
        self.opened_apps = opened_apps
        file_path = os.path.join(basedir, "type_pm.txt")
        with open(file_path, "r") as file:
            content = file.read().strip()  # Read the file content and strip whitespace
            self.type_pm = int(content)
        logo_path = Path().path_logo()
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com - Số Điện Thoại: 0964636709 - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên"
        )
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2  # Canh giữa theo chiều ngang
        y = (screen_geometry.height() - self.height()) // 2  # Canh giữa theo chiều dọc
        self.move(x, y)

        self.layout_dialog = QVBoxLayout(self)
        widget_hearder = QWidget()
        self.header_layout = QVBoxLayout(widget_hearder)
        self.layout_dialog.addWidget(widget_hearder)

        # Login App Controller
        self.widget_login = QWidget()
        login_layout = QVBoxLayout(self.widget_login)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.header_layout.addWidget(self.widget_login)

        # UI Login
        self.isLogin = False
        # Password Lable
        self.widget_pwd = QWidget()
        login_layout.addWidget(self.widget_pwd)
        pwd_layout = QVBoxLayout(self.widget_pwd)

        label_pwd = QLabel("Nhập mật khẩu")
        label_pwd.setStyleSheet(
            """
                font-size: 32px;
            """
        )
        pwd_layout.addWidget(label_pwd)

        input_pwd = QLineEdit()
        input_pwd.setStyleSheet(
            """
                QLineEdit{
                    font-size: 32px;
                    width: 100px;
                }
            """
        )
        input_pwd.setEchoMode(QLineEdit.Password)  # Set echo mode to Password
        input_pwd.setPlaceholderText(
            "Xin mời nhập mật khẩu"
        )  # Optional placeholder text

        pwd_layout.addWidget(input_pwd)
        # Button pwd Lable
        label_btn_pwd = QPushButton("Đăng Nhập")
        label_btn_pwd.setStyleSheet(css_custom_btn_pwd)
        label_btn_pwd.setCursor(QCursor(Qt.PointingHandCursor))
        pwd_layout.addWidget(label_btn_pwd)

        type_count = (
            "1a"
            if self.type_pm == 1
            else ("2" if self.type_pm == 2 else "trắng" if self.type_pm == 0 else "1b")
        )

        self.label = QLabel(f"Bộ {type_count}, Mời chọn App:")
        self.label.setStyleSheet(css_title)
        self.header_layout.addWidget(self.label)
        # Grid layout for 30 buttons in 5 columns
        self.grid_layout = QGridLayout()
        self.buttons = []

        # Load button history from file
        self.opened_apps_today = self.load_opened_apps()

        # Clean up old opened apps history
        self.cleanup_opened_apps_history()

        # Create 30 buttons, marking any that have been opened today
        for i in range(30):
            button = QPushButton()
            button.setCheckable(True)
            button.setDisabled(True)

            # Check if the button has been opened today
            if i in self.opened_apps_today:
                last_opened_time = self.opened_apps_today[i]
                button_text = f"A{i+1} - {last_opened_time}"  # Show last opened time
                button.setStyleSheet(css_custom_opened)  # Style for opened buttons
            else:
                button_text = f"A{i+1}"
                button.setStyleSheet(css_custom_normal)  # Style for unopened buttons

            button.setText(button_text)
            button.clicked.connect(
                lambda _, index=i: self.create_button_click_handler(index)
            )  # Pass index
            button.setCursor(QCursor(Qt.PointingHandCursor))
            self.grid_layout.addWidget(button, i % 6, i // 6)
            self.buttons.append(button)

        # Container widget for all app buttons
        self.button_container = QWidget()
        self.button_container.setLayout(self.grid_layout)
        self.layout_dialog.addWidget(self.button_container)

        # Horizontal layout for toggle buttons
        toggle_layout = QHBoxLayout()

        # Confirm button
        self.confirm_button = QPushButton("Khởi Chạy")
        self.confirm_button.setStyleSheet(css_button_submit)
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setCursor(QCursor(Qt.PointingHandCursor))
        toggle_layout.addWidget(self.confirm_button)

        # Change pwd button
        self.change_pwd_btn = QPushButton("Đổi Mật Khẩu")
        self.change_pwd_btn.setStyleSheet(css_button_submit)
        self.change_pwd_btn.setCursor(QCursor(Qt.PointingHandCursor))
        toggle_layout.addWidget(self.change_pwd_btn)

        # Add the horizontal toggle layout to the main layout
        self.layout_dialog.addLayout(toggle_layout)

        # self.style_toggle_buttons()

        # Track the selected app
        self.selected_app_index = None

        self.value_pwd = ""

        def input_pwd_value(value):
            self.value_pwd = value

        def btn_login():
            self.login_app(self.value_pwd)

        def show_dialog_change_pwd():
            dialog_change_pwd = ChangePwd(self)
            dialog_change_pwd.exec()

        input_pwd.textChanged.connect(input_pwd_value)
        label_btn_pwd.clicked.connect(btn_login)
        self.change_pwd_btn.clicked.connect(show_dialog_change_pwd)

        verticalSpacer2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout_dialog.addItem(verticalSpacer2)

        if not self.isLogin:
            self.show_app_controll(True)
        self.setFocus()
        self.show()

    def login_app(self, value):
        pwd_path = os.path.join("C:/data_pwd", f"{self.type_pm}", "pwd.txt")
        with open(pwd_path, "r") as file:
            pwd = file.read().strip()

        pwd = pwd if pwd != "" else "151020%"
        if pwd == value:
            for btn in self.buttons:
                btn.setDisabled(False)
            SendMessage("Bạn đã đăng nhập thành công")
            self.widget_pwd.hide()
            self.isLogin = True
            self.show_app_controll(False)
        else:
            SendMessage("Mật khẩu của bạn nhập không đúng")

    def show_app_controll(self, isShow):
        self.button_container.setHidden(isShow)
        # self.show_all_button.setHidden(isShow)
        # self.show_recent_button.setHidden(isShow)
        self.confirm_button.setHidden(isShow)
        self.label.setHidden(isShow)
        self.change_pwd_btn.setHidden(isShow)

    def style_toggle_buttons(self):
        button_style = """
            QPushButton {
                padding: 10px;
                border-radius: 8px; 
                font-size: 24px;
                line-height: 32px;
                font-weight: 600; 
                color: #ffffff; 
                background-color: #1D4ED8;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color: #45a049;
            }
            QPushButton:checked {
                background-color: #2E7D32;
                color: #E8F5E9;
            }
        """
        # self.show_all_button.setStyleSheet(button_style)
        # self.show_recent_button.setStyleSheet(button_style)

    def create_button_click_handler(self, index):
        def handle_click():
            # Clear selection style from all buttons
            for i, button in enumerate(self.buttons):
                button.setStyleSheet(
                    css_custom_opened
                    if i in self.opened_apps_today
                    else css_custom_normal
                )

            # Apply selection style to the clicked button
            self.buttons[index].setStyleSheet(css_custom_view)
            self.selected_app_index = index

        handle_click()
        return

    def confirm_selection(self):
        def handle_click(index):
            # Clear selection style from all buttons
            button = self.buttons[index]
            current_time = self.opened_apps_today[index]
            button.setText(f"App {int(index) + 1} - {current_time}")

        # Only proceed if an app is selected
        if self.selected_app_index is not None:
            # Get the current time in HH:mm format
            current_time = datetime.now().strftime("%H:%M")

            # Mark the app as opened with the current time
            self.opened_apps_today[self.selected_app_index] = current_time
            self.update_opened_apps_file()
            handle_click(self.selected_app_index)

            # Close the dialog to launch the main app
            # self.accept()
            self.open_app(self.selected_app_index + 1, self.type_pm)
        else:
            SendMessage("Xin vui lòng chọn APP")

    def toggle_all_buttons(self):
        # Uncheck the recent button if "Show/Hide All" is checked
        if self.show_all_button.isChecked():
            self.show_recent_button.setChecked(False)
            # Show all buttons
            for button in self.buttons:
                button.setVisible(True)
        else:
            # Hide all buttons if both buttons are unchecked
            for button in self.buttons:
                button.setVisible(False)

    def toggle_recent_buttons(self):
        # Uncheck the all button if "Show/Hide Recently Opened" is checked
        if self.show_recent_button.isChecked():
            self.show_all_button.setChecked(False)
            # Show only recently opened buttons
            for i, button in enumerate(self.buttons):
                button.setVisible(i in self.opened_apps_today)
        else:
            # Hide all buttons if both buttons are unchecked
            for button in self.buttons:
                button.setVisible(False)

    def cleanup_opened_apps_history(self):
        """Remove opened apps history older than a specified date."""
        file_path = os.path.join(data_sp_dir, f"{self.type_pm}", "button_clicks.txt")
        today = datetime.today().isoformat(sep=" ")[:10]  # Current date only
        cutoff_date = (datetime.today() - timedelta(days=1)).isoformat(sep=" ")[
            :10
        ]  # 1 day ago, date only
        opened_today = set()

        # Read the existing history
        try:
            with open(file_path, "r") as file:
                new_lines = []
                for line in file:
                    date_time, idx = line.strip().rsplit(
                        ":", 1
                    )  # Split only at the last ":"
                    if date_time[:10] == today:  # Check by date only
                        opened_today.add(int(idx))  # Keep today's opened apps
                        new_lines.append(line.strip())
                    elif date_time[:10] >= cutoff_date:
                        new_lines.append(
                            line.strip()
                        )  # Keep apps opened in the last day

            # Rewrite the file with updated history, removing old lines
            with open(file_path, "w") as file:
                for line in new_lines:
                    file.write(f"{line}\n")

        except FileNotFoundError:
            pass  # If the file does not exist, no apps have been opened

        return opened_today

    def load_opened_apps(self):
        """Load and display the last open time (HH:mm) for each app accessed today."""
        file_path = os.path.join(data_sp_dir, f"{self.type_pm}", "button_clicks.txt")
        today = datetime.today().isoformat(sep=" ")[:10]  # Current date only
        opened_today = {}

        try:
            with open(file_path, "r") as file:
                for line in file:
                    date_time, idx = line.strip().rsplit(
                        ":", 1
                    )  # Split only at the last ":"
                    if date_time[:10] == today:  # Check by date only
                        # Extract just the time in HH:mm format
                        open_time = datetime.fromisoformat(date_time).strftime("%H:%M")
                        opened_today[int(idx)] = (
                            open_time  # Store last open time for each app
                        )
        except FileNotFoundError:
            pass  # If the file does not exist, no apps have been opened today

        # Display each app and its last open time in HH:mm format
        # for app_id, last_opened in opened_today.items():
        #     print(f"App {app_id} was last opened at {last_opened}")

        return opened_today

    def update_opened_apps_file(self):
        file_path = os.path.join(data_sp_dir, f"{self.type_pm}", "button_clicks.txt")
        today = datetime.today().isoformat(sep=" ")  # Current date and time
        with open(file_path, "w") as file:
            for idx in sorted(self.opened_apps_today):
                file.write(f"{today}:{idx}\n")

    def modify_text_file(self, index, type_count):
        # Update file based on selected index
        file_path = os.path.join(basedir, "path_file.txt")
        skip = (
            0
            if type_count == 1
            else 30 if type_count == 2 else 60 if type_count == 3 else 90
        )
        with open(file_path, "w") as file:
            file.write(f"C:/data/{index + skip}")

    def open_app(self, index, type_count):
        self.modify_text_file(index, type_count)
        # Modify your logic here if needed
        full_screen_app = FullScreenApp(index, self.opened_apps)
        if len(self.opened_apps) > 0:
            for i in range(len(self.opened_apps)):
                app = self.opened_apps[i]
                app.close()
            self.opened_apps.clear()
        self.opened_apps.append(full_screen_app)  # Store reference to keep it alive


class ChangePwd(QDialog):
    def __init__(self, main):
        super().__init__()
        logo_path = Path().path_logo()
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com - Số Điện Thoại: 0964636709 - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên"
        )

        self.main = main
        self.value_pwd = ""
        # Center the dialog on the screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        # Dialog layout
        self.layout_dialog = QVBoxLayout(self)

        # Password Reset Section
        self.widget_pwd_change = QWidget()
        self.layout_dialog.addWidget(self.widget_pwd_change)
        change_pwd_layout = QVBoxLayout(self.widget_pwd_change)

        label_pwd_change = QLabel("Đặt lại mật khẩu")
        label_pwd_change.setStyleSheet("font-size: 16px;")
        change_pwd_layout.addWidget(label_pwd_change)

        input_pwd_change = QLineEdit()
        input_pwd_change.setStyleSheet("font-size: 16px;")
        input_pwd_change.setEchoMode(QLineEdit.Password)  # Set echo mode to Password
        input_pwd_change.setPlaceholderText("Xin mời đặt lại mật khẩu")
        change_pwd_layout.addWidget(input_pwd_change)

        # Change Password Button
        label_btn_pwd_change = QPushButton("Đổi Mật Khẩu")
        label_btn_pwd_change.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )
        label_btn_pwd_change.setCursor(QCursor(Qt.PointingHandCursor))
        change_pwd_layout.addWidget(label_btn_pwd_change)

        def input_pwd_event(value):
            self.value_pwd = value

        def change_pwd_btn():
            self.change_pwd(self.value_pwd)

        input_pwd_change.textChanged.connect(input_pwd_event)
        label_btn_pwd_change.clicked.connect(change_pwd_btn)

    def change_pwd(self, value):
        print(self.main.type_pm)
        pwd_path = os.path.join("C:/data_pwd", f"{self.main.type_pm}", "pwd.txt")
        with open(pwd_path, "w") as file:
            file.write(value)
        SendMessage("Xin vui lòng đăng nhập lại!")
        self.main.reject()
        self.reject()


class FullScreenApp(QMainWindow):
    def __init__(self, index, open_apps):
        super().__init__()

        self.open_apps = open_apps

        # Load type_pm from file
        file_path = os.path.join(basedir, "type_pm.txt")
        with open(file_path, "r") as file:
            self.type_pm = int(file.read().strip())

        # Set window properties
        logo_path = Path().path_logo()
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )

        # Set up main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2  # Canh giữa theo chiều ngang
        y = (screen_geometry.height() - self.height()) // 5  # Canh giữa theo chiều dọc
        self.move(x, y)

        # Main layout containing stacked widget and navbar
        main_layout = QVBoxLayout(self.central_widget)

        # Display app type and index
        type_count = (
            "1a"
            if self.type_pm == 1
            else ("2" if self.type_pm == 2 else "Trắng" if self.type_pm == 0 else "1b")
        )

        type_app = (
            "Tập 1" if int(index) < 11 else "Tập 2" if int(index) < 21 else "Tập 3"
        )
        label = QLabel(f"Bộ {type_count} - {type_app} - A{index}")
        label.setStyleSheet(css_title)
        main_layout.addWidget(label)

        # Stacked widget to manage pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Controller to manage page switching
        self.controller = Controller(self.stacked_widget)

        # Add Navbar widget
        navbar = Navbar(self.controller, self)
        main_layout.addWidget(navbar)
        self.setFocus()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # List to keep track of opened apps
    opened_apps = []

    # Show the selection dialog
    AppSelectionDialog(opened_apps)

    sys.exit(app.exec())
