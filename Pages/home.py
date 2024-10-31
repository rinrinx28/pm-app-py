from Pages.components.path import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - chủ sáng lập, thiết kế và mã hóa dữ liệu, Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )
        self.path = Path()
        self.layout = QVBoxLayout(self)
        label = QLabel()
        pixmap = QPixmap(self.path.path_wel())
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
