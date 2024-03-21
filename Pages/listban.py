from Pages.components.path import Path
from PySide6.QtWidgets import (QWidget, QHBoxLayout)
class ListBanPage(QWidget):
    def __init__(self):
        super().__init__()
        self.path = Path()
        print(self.path.path_db)
        layout = QHBoxLayout(self)