import sys
import os
from datetime import datetime, timedelta
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
)
from PySide6.QtGui import QIcon
from PySide6.QtGui import Qt, QCursor
from Router.navigate import Navbar
from Controller.main import Controller
from Pages.components.path import Path
from Pages.components.stylesheet import (
    css_button_submit,
    css_title,
    css_button_normal,
    css_button_notice,
    css_button_view,
    SendMessage,
)

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
            f"Đây là bảng chọn của Bộ {type_count}, Xin vui lòng chọn PM để sử dụng:"
        )
        label.setStyleSheet(css_title)
        layout.addWidget(label)

        # Grid layout for 30 buttons in 5 columns
        self.grid_layout = QGridLayout()
        self.buttons = []

        # Load button history from file
        self.opened_apps_today = self.load_opened_apps()

        # Clean up old opened apps history
        self.cleanup_opened_apps_history()

        # Create 30 buttons, marking any that have been opened today
        for i in range(30):
            button = QPushButton(f"Bản {type_count_label}.{i+1}")
            button.setCheckable(True)
            button.setStyleSheet(
                css_button_notice if i in self.opened_apps_today else css_button_normal
            )
            button.clicked.connect(
                lambda _, index=i: self.create_button_click_handler(index)
            )  # Pass index
            button.setCursor(QCursor(Qt.PointingHandCursor))
            self.grid_layout.addWidget(button, i % 6, i // 6)
            self.buttons.append(button)

        # Container widget for all app buttons
        self.button_container = QWidget()
        self.button_container.setLayout(self.grid_layout)
        layout.addWidget(self.button_container)

        # Horizontal layout for toggle buttons
        toggle_layout = QHBoxLayout()

        # "Show/Hide All" Button
        self.show_all_button = QPushButton("Ẩn Hiện Tất Cả PM")
        self.show_all_button.setCheckable(True)
        self.show_all_button.clicked.connect(self.toggle_all_buttons)
        self.show_all_button.setCursor(QCursor(Qt.PointingHandCursor))
        toggle_layout.addWidget(self.show_all_button)

        # "Show/Hide Recently Opened" Button
        self.show_recent_button = QPushButton("Ẩn Hiện PM đã mở gần đây")
        self.show_recent_button.setCheckable(True)
        self.show_recent_button.clicked.connect(self.toggle_recent_buttons)
        self.show_recent_button.setCursor(QCursor(Qt.PointingHandCursor))
        toggle_layout.addWidget(self.show_recent_button)

        # Add the horizontal toggle layout to the main layout
        layout.addLayout(toggle_layout)

        self.style_toggle_buttons()

        # Confirm button
        self.confirm_button = QPushButton("Khởi Chạy PM")
        self.confirm_button.setStyleSheet(css_button_submit)
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.confirm_button)

        # Track the selected app
        self.selected_app_index = None
        self.show()

    def style_toggle_buttons(self):
        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 8px;
                color: #000;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:checked {
                background-color: #2E7D32;
                color: #E8F5E9;
                font-weight: bold;
            }
        """
        self.show_all_button.setStyleSheet(button_style)
        self.show_recent_button.setStyleSheet(button_style)

    def create_button_click_handler(self, index):
        def handle_click():
            # Clear selection style from all buttons
            for i, button in enumerate(self.buttons):
                button.setStyleSheet(
                    css_button_notice
                    if i in self.opened_apps_today
                    else css_button_normal
                )

            # Apply selection style to the clicked button
            self.buttons[index].setStyleSheet(css_button_view)
            self.selected_app_index = index

        handle_click()
        return

    def confirm_selection(self):
        # Only proceed if an app is selected
        if self.selected_app_index is not None:
            # Mark the app as opened in the file and update the button style
            self.opened_apps_today.add(self.selected_app_index)
            self.update_opened_apps_file()

            # Close the dialog to launch the main app
            # self.accept()
            self.open_app(self.selected_app_index + 1, self.type_pm)
            return
        else:
            SendMessage("Xin vui lòng chọn APP")
            return

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
        today = datetime.today().date().isoformat()
        cutoff_date = (
            (datetime.today() - timedelta(days=1)).date().isoformat()
        )  # 1 day ago
        opened_today = set()

        # Read the existing history
        try:
            with open(file_path, "r") as file:
                new_lines = []
                for line in file:
                    date, idx = line.strip().split(":")
                    if date == today:
                        opened_today.add(int(idx))  # Keep today's opened apps
                        new_lines.append(line.strip())
                    elif date >= cutoff_date:
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
        file_path = os.path.join(data_sp_dir, f"{self.type_pm}", "button_clicks.txt")
        today = datetime.today().date().isoformat()
        opened_today = set()

        try:
            with open(file_path, "r") as file:
                for line in file:
                    date, idx = line.strip().split(":")
                    if date == today:
                        opened_today.add(int(idx))
        except FileNotFoundError:
            pass  # If the file does not exist, no apps have been opened today

        return opened_today

    def update_opened_apps_file(self):
        file_path = os.path.join(data_sp_dir, f"{self.type_pm}", "button_clicks.txt")
        today = datetime.today().date().isoformat()

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

        # Main layout containing stacked widget and navbar
        main_layout = QVBoxLayout(self.central_widget)

        # Display app type and index
        type_count = (
            "1a"
            if self.type_pm == 1
            else ("2" if self.type_pm == 2 else "0" if self.type_pm == 0 else "1b")
        )
        label = QLabel(f"PM{type_count} - Bản {type_count}.{index}/30")
        label.setStyleSheet(css_title)
        main_layout.addWidget(label)

        # Stacked widget to manage pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Controller to manage page switching
        self.controller = Controller(self.stacked_widget)
        # self.controller.set_main_widget()

        # Initially show the home page
        # self.controller.show_home_page()

        # Add Navbar widget
        navbar = Navbar(self.controller, self)
        main_layout.addWidget(navbar)
        # Set focus to the main window or another widget to remove focus from the button
        self.setFocus()

        # Make the window fullscreen
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # List to keep track of opened apps
    opened_apps = []

    # Show the selection dialog
    AppSelectionDialog(opened_apps)

    sys.exit(app.exec())
