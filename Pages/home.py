from Pages.components.path import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from PySide6.QtGui import QPixmap

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout = QVBoxLayout(self)
        label = QLabel()
        pixmap = QPixmap(self.path.path_wel())
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        