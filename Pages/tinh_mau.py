from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,QVBoxLayout,QStackedWidget,QPushButton, QDialog, QGridLayout,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView,QComboBox, QSpinBox, QSplitter
    )
from PySide6.QtGui import Qt, QCursor, QIcon, QColor
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note, css_lable, SendMessage,
    css_button_view, css_button_normal, css_button_notice,css_title
    )
import json
# from Controller.handler import createBan
import os
import bisect
class TinhAndMauPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        #/ Load Data Bans
        self.bans_path = self.path.path_db()
        with open(self.bans_path, 'r') as file:
            self.bans_db = json.load(file)
        
        self.ban_info = None

        #/ Config Font
        self.font = Font()

        #/ Config Color
        self.red = QColor(239, 1, 7)
        self.yellow = QColor(255, 215, 0)
        
        #/ Navigation Main
        self.navbar_wid_main =QWidget()
        self.navbar_layout = QHBoxLayout(self.navbar_wid_main)
        self.navbar_layout.setSpacing(100)
        self.layout.addWidget(self.navbar_wid_main)

        #/ Widget Main
        self.widget_main = QStackedWidget()
        self.layout.addWidget(self.widget_main)

        #/ Table main
        self.table_main = None

        #/ Button Main
        self.button_wid_main =QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.button_layout.setSpacing(50)
        self.layout.addWidget(self.button_wid_main)

        #/ Show Select Bang and Login into Bang
        self.showSelectBan()
    
    # TODO handler Render Components
    def showSelectBan(self):
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Đăng Nhập Vào Bảng Tính và Màu')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(600, 400)
        dialog.show()

        #/ Create Layout
        layout = QGridLayout()
        dialog.setLayout(layout)

        #/ Create From
        from_w = QWidget()
        from_l = QVBoxLayout(from_w)
        layout.addWidget(from_w, 0,0)

        #/ Create Input Value
        #? Name
        name_w = QWidget()
        name_l = QVBoxLayout(name_w)
        from_l.addWidget(name_w)

        label_name = QLabel('Chọn Bảng')
        label_name.setStyleSheet(css_lable)
        name_l.addWidget(label_name)

        input_name = QComboBox()
        input_name.setStyleSheet(css_input)
        input_name.addItem('Chọn Bảng')
        for i in range(len(self.bans_db)):
            name = self.bans_db[i]['name']
            input_name.addItem(f'Bảng {name}')
        name_l.addWidget(input_name)

        #? password
        password_w = QWidget()
        password_l = QVBoxLayout(password_w)
        from_l.addWidget(password_w)

        label_password = QLabel('Nhập Mật Khẩu')
        label_password.setStyleSheet(css_lable)
        password_l.addWidget(label_password)

        input_password = QLineEdit()
        input_password.setStyleSheet(css_input)
        password_l.addWidget(input_password)

        #/ Create Button
        button_w = QWidget()
        button_l = QHBoxLayout(button_w)
        button_l.setSpacing(100)
        layout.addWidget(button_w)

        #? Submit Button
        submit = QPushButton('Đăng Nhập')
        submit.setStyleSheet(css_button_submit)
        submit.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(submit)

        #? Exit Button
        Exit = QPushButton('Thoát')
        Exit.setStyleSheet(css_button_cancel)
        Exit.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(Exit)

        # TODO Handler Button
        def  exit():
            dialog.reject()
        
        def submit_click():
            ban_index = input_name.currentIndex()
            password_value = input_password.text()
            if ban_index == 0 or len(password_value) == 0:
                SendMessage('Xin vui lòng chọn bảng và nhập mật khẩu!')
                return
            ban_value = self.bans_db[ban_index - 1]
            ban_name = ban_value['name']
            ban_password = ban_value['password']
            if password_value not in ban_password:
                SendMessage('Mật khẩu không đúng!')
                return
            self.ban_info = ban_value
            SendMessage(f'Bạn đã đăng nhập thành công vào bảng {ban_name}')
            dialog.reject()
            self.renderNavigation()
            self.renderTableColor()
            self.renderButton()
            return
        
        submit.clicked.connect(submit_click)
        Exit.clicked.connect(exit)

    def renderNavigation(self):
        ban_info = self.ban_info
        ban_name = ban_info['name']
        ban_col = ban_info['col']
        ban_thong_name = ban_info['thong']['name']
        ban_thong_value = ban_info['thong']['value']
        #/ Create Button Notice Color
        button_w = QWidget()
        button_l = QHBoxLayout(button_w)
        button_l.setSpacing(5)
        button_l.setContentsMargins(0,0,0,0)
        button_w.setFixedWidth(400)
        self.navbar_layout.addWidget(button_w)

        buttonColor = QPushButton('Báo Màu M1')
        buttonColor.setStyleSheet(css_button_normal)
        buttonColor.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(buttonColor)

        buttonOne = QPushButton('1')
        buttonOne.setFixedWidth(50)
        buttonOne.setStyleSheet(css_button_normal)
        buttonOne.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(buttonOne)

        buttonTwo = QPushButton('2')
        buttonTwo.setFixedWidth(50)
        buttonTwo.setStyleSheet(css_button_normal)
        buttonTwo.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(buttonTwo)

        buttonThree = QPushButton('3')
        buttonThree.setFixedWidth(50)
        buttonThree.setStyleSheet(css_button_normal)
        buttonThree.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(buttonThree)

        #/ Title
        title = QLabel(f'Bảng {ban_name} - {ban_col} Cột - Bảng Thông {ban_thong_name} - Số thông {ban_thong_value}')
        title.setStyleSheet(css_title)
        self.navbar_layout.addWidget(title)

    def renderTableCount(self):
        ban_info = self.ban_info

        #/ Create Widget table
        self.table_main = QSplitter(Qt.Horizontal)
        self.table_main.setContentsMargins(0,0,0,0)
        self.frozen_table = QTableWidget()
        self.table_scroll = QTableWidget()
        self.table_main.addWidget(self.frozen_table)
        self.table_main.addWidget(self.table_scroll)
        self.widget_main.addWidget(self.table_main)

        #/ Config table
        rowCount = len(ban_info['data'])
        self.frozen_table.setRowCount(rowCount + 50)
        self.table_scroll.setRowCount(rowCount + 50)

        #/ Config Header
        ranges = []
        cols_arr = []
        total_column = 0
        for i in range(ban_info['thong']['value']):
            range_data = {}
            thong_name = QTableWidgetItem(f'T.{i+1}')
            thong_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            thong_name.setForeground(self.red)
            range_data['start'] = total_column
            range_data['value'] = total_column
            if i != 0:
                cols_arr.append(thong_name)
                total_column += 1
            for j in range(ban_info['col']):
                col_name = QTableWidgetItem(f'C.{j + 1}')
                col_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                cols_arr.append(col_name)
                total_column += 1
            range_data['end'] = total_column
            range_data['thong'] = i
            ranges.append(range_data)

        self.table_scroll.setColumnCount(len(cols_arr))
        self.frozen_table.setColumnCount(1)
        for i, item in enumerate(cols_arr):
            self.table_scroll.setHorizontalHeaderItem(i, item)

        for i in range(self.frozen_table.columnCount()):
            item = QTableWidgetItem(f'T.{i + 1}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(self.red)
            self.frozen_table.setHorizontalHeaderItem(i, item)
    
        for i in range(50):
            # date = ban_info['data'][i]['date'].split('/')
            # item = QTableWidgetItem(f'{date[0]}/{date[1]}/.')
            item = QTableWidgetItem(f'03/04/.')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table.setVerticalHeaderItem(i, item)

        #/ Config Font
        self.frozen_table.setFont(self.font)
        self.frozen_table.horizontalHeader().setFont(self.font)
        self.frozen_table.verticalHeader().setFont(self.font)

        self.table_scroll.setFont(self.font)
        self.table_scroll.horizontalHeader().setFont(self.font)
        self.table_scroll.verticalHeader().setFont(self.font)

        self.frozen_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.frozen_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.frozen_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.frozen_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)

        self.table_scroll.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.table_scroll.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)

        # height_of_row = self.table_scroll.verticalHeader().sectionSize(0)
        width_of_row = self.table_scroll.horizontalHeader().sectionSize(0)

        self.frozen_table.setMaximumWidth(width_of_row + 120)
        self.frozen_table.setMaximumWidth(width_of_row + 120)

        self.table_scroll.verticalHeader().hide()
        
        self.frozen_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.frozen_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        def update(value):
            # Create a sorted list of range starts and their corresponding indices
            filter_near = [item['start'] for item in ranges]
            index_near = bisect.bisect_left(filter_near, value)
            
            if index_near > 0:
                index = index_near - 1
            else:
                index = index_near

            if ranges[index]['start'] <= value < ranges[index]['end']:
                new_value = value
            elif value < ranges[index]['start']:
                new_value = ranges[index]['start']
            else:
                # This shouldn't happen, but handle it just in case
                return
            thong_header = ranges[index]['thong']
            self.frozen_table.horizontalHeaderItem(0).setText(f'T.{thong_header + 1}')
            ranges[index]['value'] = new_value
           
        def selectRow(value):
            self.table_scroll.selectRow(value)

        
        def sync_vertical_scroll(vale):
            self.frozen_table.verticalScrollBar().setValue(vale)
            self.table_scroll.verticalScrollBar().setValue(vale)

        self.frozen_table.verticalHeader().sectionClicked.connect(selectRow)
        self.table_scroll.horizontalScrollBar().valueChanged.connect(update)

        self.table_scroll.verticalScrollBar().valueChanged.connect(sync_vertical_scroll)
        self.frozen_table.verticalScrollBar().valueChanged.connect(sync_vertical_scroll)
        
    def renderTableColor(self):
        ban_info = self.ban_info

        #/ Create Widget table
        self.table_main = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main)

        #/ Table Create
        # Create a vertical splitter
        self.splitter_left = QSplitter(Qt.Vertical)
        self.frozen_table_left = QTableWidget()
        self.table_scroll_left = QTableWidget()
        self.splitter_left.addWidget(self.frozen_table_left)
        self.splitter_left.addWidget(self.table_scroll_left)
        self.table_main.addWidget(self.splitter_left)

        # Create a vertical splitter
        self.splitter_right = QSplitter(Qt.Vertical)
        self.frozen_table = QTableWidget()
        self.table_scroll = QTableWidget()
        self.splitter_right.addWidget(self.frozen_table)
        self.splitter_right.addWidget(self.table_scroll)
        self.table_main.addWidget(self.splitter_right)
        
        #/ Config table
        rowCount = len(ban_info['data'])
        self.frozen_table.setRowCount(1)
        self.table_scroll.setRowCount(50)

        self.frozen_table_left.setRowCount(1)
        self.table_scroll_left.setRowCount(50)

        self.frozen_table_left.setColumnCount(1)
        self.table_scroll_left.setColumnCount(1)

        #/ Config Header col
        current_column  = 0
        # Tạo cột từ 0 đến 83
        for i in range(0, 84):
            current_column  += 5  # Số cột tạo cho mỗi lần là 4 cột + 1 cột phụ trợ

        # Tạo cột từ 84 đến 98
        for i in range(84, 99):
            current_column  += 4  # Số cột tạo cho mỗi lần là 3 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table.setColumnCount(current_column)
        self.table_scroll.setColumnCount(current_column)
        
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0
        # Tạo cột từ 0 đến 83
        for i in range(0, 84):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = 4  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"Số Đếm {step_count + 2}")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table.setItem(0, total_columns, header_item)
            self.frozen_table.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f'{j + 1}')
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll.setHorizontalHeaderItem(total_columns + j, col_header)

            
            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(QColor(Qt.GlobalColor.white))  # Đặt màu nền là màu trắng
            self.table_scroll.setHorizontalHeaderItem(total_columns + num_cols, col_null)


            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

        # Tạo cột từ 84 đến 98
        for i in range(84, 99):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = 3  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"Số Đếm {step_count + 2}")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table.setItem(0, total_columns, header_item)
            self.frozen_table.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f'{j + 1}')
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll.setHorizontalHeaderItem(total_columns + j, col_header)

            
            col_null = QTableWidgetItem()
            col_null.setBackground(QColor(Qt.GlobalColor.white))  # Đặt màu nền là màu trắng
            self.table_scroll.setHorizontalHeaderItem(total_columns + num_cols, col_null)

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        
        #/ config header Row
        for i in range(rowCount):
            date = ban_info['data'][i]['date'].split('/')
            item = QTableWidgetItem(f'{date[0]}/{date[1]}/.')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll.setVerticalHeaderItem(i + 2, item)
        self.table_scroll_left.setHorizontalHeaderItem(0, QTableWidgetItem())
        #/ Render Row for table left
        for i in range(self.table_scroll_left.rowCount()):
            item = QTableWidgetItem(f'03/04/.')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_left.setItem(i,0, item)
            
        for i in range(self.frozen_table_left.rowCount()):
            item = QTableWidgetItem(f'Ngày')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_left.setItem(i,0, item)
        

        #/ Config Font
        self.frozen_table.setFont(self.font)
        self.frozen_table.verticalHeader().setFont(self.font)
        self.frozen_table.horizontalHeader().setFont(self.font)

        self.table_scroll.setFont(self.font)
        self.table_scroll.verticalHeader().setFont(self.font)
        self.table_scroll.horizontalHeader().setFont(self.font)
        
        self.frozen_table_left.setFont(self.font)
        self.frozen_table_left.verticalHeader().setFont(self.font)
        self.frozen_table_left.horizontalHeader().setFont(self.font)

        self.table_scroll_left.setFont(self.font)
        self.table_scroll_left.verticalHeader().setFont(self.font)
        self.table_scroll_left.horizontalHeader().setFont(self.font)

        #/ Config header
        self.frozen_table.horizontalHeader().hide()
        self.frozen_table.verticalHeader().hide()
        self.table_scroll.verticalHeader().hide()
        
        self.frozen_table_left.horizontalHeader().hide()
        self.frozen_table_left.verticalHeader().hide()
        # self.table_scroll_left.horizontalHeader().hide()
        self.table_scroll_left.verticalHeader().hide()

        self.frozen_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.frozen_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.frozen_table_left.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.frozen_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_left.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_left.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        height_of_row = self.frozen_table.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table.horizontalHeader().sectionSize(0)
        self.frozen_table.setMaximumHeight(height_of_row)
        self.frozen_table.setMinimumHeight(height_of_row)

        self.frozen_table_left.setMaximumSize(width_of_row + 30, height_of_row)
        self.frozen_table_left.setMinimumSize(width_of_row + 30, height_of_row)

        self.frozen_table_left.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_left.horizontalHeader().setStretchLastSection(True)

        self.frozen_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.frozen_table_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_scroll_left.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_scroll_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.frozen_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.frozen_table_left.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll_left.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        def sync_horizontal_scroll(vale):
            self.frozen_table.horizontalScrollBar().setValue(vale)
            self.table_scroll.horizontalScrollBar().setValue(vale)

        
        def sync_vertical_scroll(vale):
            self.table_scroll_left.verticalScrollBar().setValue(vale)
            self.table_scroll.verticalScrollBar().setValue(vale)

        self.table_scroll.horizontalScrollBar().valueChanged.connect(sync_horizontal_scroll)
        self.frozen_table.horizontalScrollBar().valueChanged.connect(sync_horizontal_scroll)
        self.table_scroll.verticalScrollBar().valueChanged.connect(sync_vertical_scroll)
        self.table_scroll_left.verticalScrollBar().valueChanged.connect(sync_vertical_scroll)

        for i in range(self.table_scroll.columnCount()):
            width = self.table_scroll.columnWidth(i)
            self.frozen_table.setColumnWidth(i, width)

    def renderButton(self):
        #/ Delete new row
        DeleteNewRow = QPushButton('Xóa dòng mới nhất')
        DeleteNewRow.setStyleSheet(css_button_cancel)
        DeleteNewRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(DeleteNewRow)
        
        #/ Delete from to
        DeleteFromTo = QPushButton('Xóa Từ Ngày')
        DeleteFromTo.setStyleSheet(css_button_cancel)
        DeleteFromTo.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(DeleteFromTo)

        #/ Insert Data row
        InsertData = QPushButton('Nhập Liệu')
        InsertData.setStyleSheet(css_button_submit)
        InsertData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(InsertData)
        
        #/ Insert Thong row
        InsertThong = QPushButton('Nhập Thông')
        InsertThong.setStyleSheet(css_button_submit)
        InsertThong.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(InsertThong)
        
        #/ Setting Table
        SettingTable = QPushButton('Cài Đặt Bảng')
        SettingTable.setStyleSheet(css_button_cancel)
        SettingTable.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(SettingTable)

        #/ Bảng Màu
        self.TableChange = QPushButton('Bảng Màu')
        self.TableChange.setStyleSheet(css_button_submit)
        self.TableChange.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(self.TableChange)

