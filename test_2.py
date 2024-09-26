from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QGridLayout
        layout = QGridLayout()

        # Add table headers (labels)
        layout.addWidget(QLabel("Row/Col"), 0, 0)
        layout.addWidget(QLabel("Column 1"), 0, 1)
        layout.addWidget(QLabel("Column 2"), 0, 2)

        # Add table-like rows (labels and buttons)
        layout.addWidget(QLabel("Row 1"), 1, 0)
        layout.addWidget(QPushButton("Cell 1,1"), 1, 1)
        layout.addWidget(QPushButton("Cell 1,2"), 1, 2)

        layout.addWidget(QLabel("Row 2"), 2, 0)
        layout.addWidget(QPushButton("Cell 2,1"), 2, 1)
        layout.addWidget(QPushButton("Cell 2,2"), 2, 2)

        layout.addWidget(QLabel("Row 3"), 3, 0)
        layout.addWidget(QPushButton("Cell 3,1"), 3, 1)
        layout.addWidget(QPushButton("Cell 3,2"), 3, 2)

        # Apply a style sheet to the whole window
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                background-color: #333;
                color: #fff;
                padding: 5px;
                border: 1px solid #999;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: 1px solid #999;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )

        # Set the layout for the QWidget
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("Styled QGridLayout Table-like Layout")
        self.resize(400, 200)


if __name__ == "__main__":
    app = QApplication([])

    window = Window()
    window.show()

    app.exec()
