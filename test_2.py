import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView


class FrozenHeaderTable(QTableWidget):
    def __init__(self):
        super().__init__()

        # Tạo bảng
        self.setRowCount(100)
        #/ Config Header col
        current_column  = 0
        # Tạo cột từ 0 đến 83
        for i in range(0, 84):
            current_column  += 5  # Số cột tạo cho mỗi lần là 4 cột + 1 cột phụ trợ

        # Tạo cột từ 84 đến 98
        for i in range(84, 99):
            current_column  += 4  # Số cột tạo cho mỗi lần là 3 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.setColumnCount(current_column)
        
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0
        # Tạo cột từ 0 đến 83
        for i in range(0, 84):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = 4  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"Số Đếm {step_count + 2}")
            # header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(0, total_columns, header_item)
            self.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_name = QTableWidgetItem(f'{j + 1}')
                # col_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(1, total_columns + j, col_name)

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

        # Tạo cột từ 84 đến 98
        for i in range(84, 99):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = 3  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"Số Đếm {step_count + 2}")
            # header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(0, total_columns, header_item)
            self.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_name = QTableWidgetItem(f'{j + 1}')
                # col_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(1, total_columns + j, col_name)

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        #/ config header Row   
        for i in range(2):
            item = QTableWidgetItem(f'')
            self.setVerticalHeaderItem(i, item)

        self.ranges = [
            {'start': 0, "end": current_column, "value": 0},
            # {'start': 1, "end": current_column - 1, "value": 1},
        ]

        # Cài đặt sự kiện cuộn bảng
        def scroll_headers(value):
            for i, col_range in enumerate(self.ranges):
                if col_range['start'] <= value:
                    # Di chuyển cả hai hàng tiêu đề
                    self.verticalHeader().moveSection(col_range['value'], value)
                    col_range['value'] = value
                elif value < col_range['start']:
                    value = col_range['start']
                    # Di chuyển cả hai hàng tiêu đề
                    self.verticalHeader().moveSection(col_range['value'], value)
                    col_range['value'] = value

        self.horizontalHeader().hide()
        self.verticalScrollBar().valueChanged.connect(scroll_headers)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FrozenHeaderTable()
    window.show()
    sys.exit(app.exec_())
