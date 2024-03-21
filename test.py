from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtGui import QStandardItem, QStandardItemModel

class StickyColumnApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sticky Column App")
        # Tạo QTableView
        self.table_view = QTableWidget(100,100)

        # Thêm dữ liệu mẫu
        for row in range(100):
            for column in range(100):
                item = QTableWidgetItem(f"Row {row}, Col {column}")
                self.table_view.setItem(row, column, item)

        # Cố định cột đầu tiên
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)

        # Kết nối sự kiện cuộn ngang
        self.table_view.horizontalScrollBar().valueChanged.connect(self.update)
        self.max_value = self.table_view.horizontalScrollBar().maximum()

        self.ranges = [
            {'start': 0, "end": 19, "value": 0},
            {'start': 19, "end": 39, "value": 19},
            {'start': 39, "end": 59, "value": 39},
            {'start': 59, "end": 79, "value": 59},
            {'start': 79, "end": 99, "value": 79},
        ]

        
        self.setCentralWidget(self.table_view)
        self.table_view.scrollToItem(self.table_view.item(2,75), hint=QTableWidget.ScrollHint.PositionAtCenter)

    def update(self, value):
        for col_range in self.ranges:
            if col_range['start'] <= value < col_range['end']:
                self.table_view.horizontalHeader().moveSection(col_range['value'], value)
                col_range['value'] = value
            elif value < col_range['start']:
                value = col_range['start']
                self.table_view.horizontalHeader().moveSection(col_range['value'], value)
                col_range['value'] = value


def main():
    app = QApplication([])
    window = StickyColumnApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
