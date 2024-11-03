import sys
import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
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
)


class FullScreenApp(QMainWindow):
    def __init__(self, index):
        super().__init__()

        self.setWindowTitle(f"Application {index}")
        self.setGeometry(0, 0, 1920, 1080)  # Set size to full HD (adjust as needed)
        self.showFullScreen()  # Show in full screen

        # Example: Add any widgets or layout to your main window
        # self.setCentralWidget(QWidget())  # If you want to set a central widget


class AppSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Applications to Open")
        self.selected_app_indices = []  # To store selected indices
        self.type_pm = 1  # Example: you might want to set this based on your logic

        self.layout = QVBoxLayout(self)

        # List Widget for applications
        self.app_list_widget = QListWidget(self)
        self.populate_app_list()  # Populate the list with application names
        self.layout.addWidget(self.app_list_widget)

        # Open Selected Apps Button
        open_button = QPushButton("Open Selected Apps")
        open_button.clicked.connect(self.open_selected_apps)
        self.layout.addWidget(open_button)

        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.reject)  # Closes the dialog
        self.layout.addWidget(exit_button)

        # Connect selection change
        self.app_list_widget.itemChanged.connect(self.update_selection)

    def populate_app_list(self):
        # Example application names
        for i in range(30):
            item = QListWidgetItem(f"App {i + 1}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # Allow checkbox
            item.setCheckState(Qt.Unchecked)  # Start unchecked
            self.app_list_widget.addItem(item)

    def update_selection(self):
        self.selected_app_indices = [
            row
            for row in range(self.app_list_widget.count())
            if self.app_list_widget.item(row).checkState() == Qt.Checked
        ]

    def open_selected_apps(self):
        selected_app_indices = self.selected_app_indices  # Get selected indices
        type_count = self.type_pm  # Example: retrieve type count

        # Open each selected app
        for index in selected_app_indices:
            open_app(
                index + 1, type_count
            )  # Call the open_app function with adjusted index

        # Optionally, provide feedback to the user that the apps were opened
        print(
            "Opened apps:", [index + 1 for index in selected_app_indices]
        )  # Replace with a message box if needed


def open_app(index, type_count):
    # modify_text_file(index, type_count)
    mainWindow = FullScreenApp(index)  # Create the full screen app
    mainWindow.show()  # Show the main window in full screen


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show the selection dialog
    selection_dialog = AppSelectionDialog()
    selection_dialog.exec()  # Keep the dialog open until the user closes it

    sys.exit(app.exec())
