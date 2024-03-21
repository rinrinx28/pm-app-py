from Pages.components.path import Path
from PySide6.QtWidgets import (QWidget, QHBoxLayout)
class TinhAndMauPage(QWidget):
    def __init__(self):
        super().__init__()
        self.path = Path()
        layout = QHBoxLayout(self)