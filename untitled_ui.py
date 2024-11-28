from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, QSplitter, QWidget, QVBoxLayout
)
from PySide6.QtCore import Qt

class FreezeTableExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Freeze Columns Example")
        self.resize(800, 400)

        # Tạo hai bảng
        self.frozen_table = QTableWidget(10, 2)  # Freeze 2 cột
        self.main_table = QTableWidget(10, 8)  # Bảng chính với các cột còn lại

        # Thêm dữ liệu mẫu
        for row in range(10):
            for col in range(10):
                item = QTableWidgetItem(f"Cell {row + 1},{col + 1}")
                if col < 2:  # Thêm dữ liệu vào bảng frozen
                    self.frozen_table.setItem(row, col, item)
                else:  # Thêm dữ liệu vào bảng chính
                    self.main_table.setItem(row, col - 2, item)

        # Cấu hình bảng frozen
        self.frozen_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Không cuộn ngang
        self.frozen_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozen_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.frozen_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Cấu hình bảng chính
        self.main_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Không cuộn ngang
        self.main_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Đồng bộ cuộn dọc giữa hai bảng
        self.frozen_table.verticalScrollBar().valueChanged.connect(
            self.main_table.verticalScrollBar().setValue
        )
        self.main_table.verticalScrollBar().valueChanged.connect(
            self.frozen_table.verticalScrollBar().setValue
        )

        # Kết hợp hai bảng bằng QSplitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.frozen_table)
        splitter.addWidget(self.main_table)
        splitter.setStretchFactor(0, 1)  # Freeze cột không co dãn
        splitter.setStretchFactor(1, 3)  # Bảng chính co dãn

        # Hiển thị giao diện
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication([])
    window = FreezeTableExample()
    window.show()
    app.exec()
