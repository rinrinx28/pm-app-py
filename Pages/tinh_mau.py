from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,QVBoxLayout,QStackedWidget,QPushButton, QDialog, QGridLayout,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView,QComboBox, QSpinBox, QSplitter,
    QDateEdit, QCheckBox
    )
from PySide6.QtGui import Qt, QCursor, QIcon, QColor
from PySide6.QtCore import QDate
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note, css_lable, SendMessage,
    css_button_view, css_button_normal, css_button_notice,css_title,css_customs_table,
    css_button_checkbox,css_table_header
    )
import json
from Controller.handler import updateBanInsert
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

        #/ Load data Thong and Number
        self.thong_info = None
        self.number_info = None

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
        dialog.setFixedSize(800, 600)
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
            #/ Load Info thong and Number
            change_number = self.ban_info['change']
            col_value = self.ban_info['col']
            id_thong = self.ban_info['thong']['id']
            value_thong = self.ban_info['thong']['value']
            path_thong = self.path.path_thong_with_id_value(id_thong,change_number)
            path_number = self.path.path_number_with_value(change_number)

            with open(path_thong, 'r') as file:
                thong_info = json.load(file)
                self.thong_info = thong_info[:value_thong]
            with open(path_number, 'r') as file:
                number_info = json.load(file)
                self.number_info = [number_rang[:col_value] for number_rang in number_info]

            self.renderNavigation()
            self.renderTableCount()
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
        button_w.setFixedWidth(500)
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

        buttonFor = QPushButton('4')
        buttonFor.setFixedWidth(50)
        buttonFor.setStyleSheet(css_button_normal)
        buttonFor.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(buttonFor)

        #/ Title
        title = QLabel(f'Bảng {ban_name} - {ban_col} Cột - Bảng Thông {ban_thong_name} - Số thông {ban_thong_value}')
        title.setStyleSheet(css_title)
        self.navbar_layout.addWidget(title)

    def renderTableCount(self):
        ban_info = self.ban_info

        #/ Create Widget table
        self.table_main = QSplitter(Qt.Horizontal)
        self.table_main.setContentsMargins(0,0,0,0)
        self.frozen_table_count = QTableWidget()
        self.table_scroll_count = QTableWidget()
        self.table_main.addWidget(self.frozen_table_count)
        self.table_main.addWidget(self.table_scroll_count)
        self.widget_main.addWidget(self.table_main)

        #/ Config table
        rowCount = len(ban_info['data'])
        self.frozen_table_count.setRowCount(rowCount)
        self.table_scroll_count.setRowCount(rowCount)

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

        self.table_scroll_count.setColumnCount(len(cols_arr))
        self.frozen_table_count.setColumnCount(1)
        for i, item in enumerate(cols_arr):
            self.table_scroll_count.setHorizontalHeaderItem(i, item)

        for i in range(self.frozen_table_count.columnCount()):
            item = QTableWidgetItem(f'T.{i + 1}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(self.red)
            self.frozen_table_count.setHorizontalHeaderItem(i, item)
    
        for i in range(rowCount):
            date = ban_info['data'][i]['date'].split('/')
            item = QTableWidgetItem(f'{date[0]}/{date[1]}/.')
            # item = QTableWidgetItem(f'03/04/.')
            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_count.setVerticalHeaderItem(i, item)

        #/ Config Font
        self.frozen_table_count.setFont(self.font)
        self.frozen_table_count.horizontalHeader().setFont(self.font)
        self.frozen_table_count.verticalHeader().setFont(self.font)

        self.table_scroll_count.setFont(self.font)
        self.table_scroll_count.horizontalHeader().setFont(self.font)
        self.table_scroll_count.verticalHeader().setFont(self.font)

        self.frozen_table_count.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.frozen_table_count.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.frozen_table_count.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.frozen_table_count.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)

        self.table_scroll_count.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_count.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.table_scroll_count.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll_count.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)

        # height_of_row = self.table_scroll_count.verticalHeader().sectionSize(0)
        width_of_row = self.table_scroll_count.horizontalHeader().sectionSize(0)

        self.frozen_table_count.setMaximumWidth(width_of_row + 120)
        self.frozen_table_count.setMaximumWidth(width_of_row + 120)

        self.table_scroll_count.verticalHeader().hide()
        
        self.frozen_table_count.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.frozen_table_count.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
            self.frozen_table_count.horizontalHeaderItem(0).setText(f'T.{thong_header + 1}')
            ranges[index]['value'] = new_value
           
        def sync_vertical_scroll(vale):
            self.frozen_table_count.verticalScrollBar().setValue(vale)
            self.table_scroll_count.verticalScrollBar().setValue(vale)

        self.table_scroll_count.horizontalScrollBar().valueChanged.connect(update)

        self.table_scroll_count.verticalScrollBar().valueChanged.connect(sync_vertical_scroll)
        self.frozen_table_count.verticalScrollBar().valueChanged.connect(sync_vertical_scroll)
        
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

        InsertData.clicked.connect(self.insertData)

    # TODO Handler Button
    def insertData(self):
        #/ Config Data
        old_data = self.ban_info['data'][-1] if len(self.ban_info['data']) > 0 else None
        data = {}
        data['insert'] = {}
        data['update'] = self.ban_info['meta']['features']
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Bảng Nhập Liệu')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1270,850)
        dialog.show()

        #/ Create Layout
        layout = QGridLayout()
        layout.setSpacing(0)
        dialog.setLayout(layout)

        #/ Table Insert
        insert_thong_table = QTableWidget()
        insert_thong_table.setFixedSize(720, 850)
        insert_thong_table.setStyleSheet(css_table_header)
        layout.addWidget(insert_thong_table, 0,0,Qt.AlignmentFlag.AlignLeft)
        #/ Config Table
        insert_thong_table.setColumnCount(8)
        insert_thong_table.setRowCount(15)

        insert_thong_table.horizontalHeader().hide()
        insert_thong_table.verticalHeader().hide()

        insert_thong_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        insert_thong_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        insert_thong_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        insert_thong_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        insert_thong_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        insert_thong_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        insert_thong_table.setFont(self.font)
        insert_thong_table.horizontalHeader().setFont(self.font)
        insert_thong_table.verticalHeader().setFont(self.font)

        #/ Render Row Table
        for i in range(15):
            for j in range(8):
                value = i + j * 15
                value = value if value > 9 else f'0{value}'
                item = QTableWidgetItem(f'{value}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                insert_thong_table.setItem(i, j, item)
        
        #/ Insert From
        insert_from_w = QWidget()
        insert_from_w.setMinimumWidth(530)
        insert_from_l = QGridLayout(insert_from_w)
        insert_from_l.setSpacing(20)
        layout.addWidget(insert_from_w, 0, 1, Qt.AlignmentFlag.AlignTop)
        
        #/ Insert Day
        insert_day_label = QLabel('Ngày Tháng')
        insert_day_label.setStyleSheet(css_lable)

        insert_day_edit = QDateEdit()
        insert_day_edit.setStyleSheet(css_input)
        insert_day_edit.setCalendarPopup(True)

        insert_from_l.addWidget(insert_day_label,1,0)
        insert_from_l.addWidget(insert_day_edit,1,1)

        #/ Insert Ngang
        insert_ngang_label = QLabel('Hàng Ngang')
        insert_ngang_label.setStyleSheet(css_lable)

        insert_ngang_grid_w = QWidget()
        # insert_ngang_grid_w.setMinimumWidth(200)
        insert_ngang_gird = QGridLayout(insert_ngang_grid_w)

        insert_ngang_edit = QSpinBox()
        insert_ngang_edit.setMinimum(1)
        insert_ngang_edit.setMaximum(31)
        insert_ngang_edit.setStyleSheet(css_input)

        insert_ngang_edit_first = QLabel('')
        insert_ngang_edit_first.setAlignment(Qt.AlignmentFlag.AlignCenter)
        insert_ngang_edit_first.setStyleSheet(
           css_customs_table
        )

        insert_ngang_gird.addWidget(insert_ngang_edit, 0,0)
        insert_ngang_gird.addWidget(insert_ngang_edit_first, 0,1)

        insert_from_l.addWidget(insert_ngang_label, 2,0)
        insert_from_l.addWidget(insert_ngang_grid_w, 2,1)

        #/ Insert Thong
        insert_thong_label = QLabel('Thông số')
        insert_thong_label.setStyleSheet(css_lable)

        insert_thong_grid_w = QWidget()
        # insert_thong_grid_w.setMinimumWidth(150)
        insert_thong_gird = QGridLayout(insert_thong_grid_w)

        insert_thong_edit = QSpinBox()
        insert_thong_edit.setMinimum(-1)
        insert_thong_edit.setMaximum(120)
        insert_thong_edit.setStyleSheet(css_input)

        insert_thong_edit_first = QLabel('')
        insert_thong_edit_first.setAlignment(Qt.AlignmentFlag.AlignCenter)
        insert_thong_edit_first.setStyleSheet(
            css_customs_table
        )

        insert_thong_gird.addWidget(insert_thong_edit, 0,0)
        insert_thong_gird.addWidget(insert_thong_edit_first, 0,1)


        insert_from_l.addWidget(insert_thong_label, 3,0)
        insert_from_l.addWidget(insert_thong_grid_w, 3,1)

        #/ Features insert
        virable_one_edit = QCheckBox('Kích Hoạt N:2')
        virable_one_edit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        virable_one_edit.setStyleSheet(css_button_checkbox)

        virable_two_edit = QCheckBox('Kích Hoạt N=1')
        virable_two_edit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        virable_two_edit.setStyleSheet(css_button_checkbox)
        
        insert_from_l.addWidget(virable_one_edit, 4,0, Qt.AlignmentFlag.AlignCenter)
        insert_from_l.addWidget(virable_two_edit, 4,1, Qt.AlignmentFlag.AlignCenter)

        #/ Button Insert
        submit = QPushButton('Soát Rồi OK Toán')
        submit.setCursor(QCursor(Qt.PointingHandCursor))
        submit.setStyleSheet(css_button_submit)

        exit = QPushButton('Thoát')
        exit.setCursor(QCursor(Qt.PointingHandCursor))
        exit.setStyleSheet(css_button_cancel)

        label_submit = QLabel()
        label_exit = QLabel()

        insert_from_l.addWidget(label_submit,6,1)
        insert_from_l.addWidget(submit,7,1)
        insert_from_l.addWidget(label_exit,8,1)
        insert_from_l.addWidget(exit,9,1)

        #TODO Handler Button exit
        def exit_click():
            dialog.reject()

        def changeDate(value):
            date = QDate(value)
            data['insert']['date'] = date.toString('dd/MM/yyyy')
            if not data['update']['N=1']['status']:
                day = date.day()
                insert_ngang_edit.setValue(day)

        def changeNgang(value):
            data['insert']['ngang'] = value - 1
            number_value = self.number_info[value - 1][:2]
            insert_ngang_edit_first.setText(f'{number_value[0]}')

        def changeThongTable(value):
            item = value.text()
            insert_thong_edit.setValue(int(item))

        def changeThongEdit(value):
            insert_thong_table.clearSelection()
            if value <= 0 and value >= 120:
                return
            data['insert']['thong'] = value
            thong_value = self.thong_info[value - 1][:2]
            insert_thong_edit_first.setText(f'{thong_value[0]}')

            col = value // 15  # Calculate column index
            row = value % 15  # Calculate row index
            item = insert_thong_table.item(row, col)
            if item:
                item.setSelected(True)

        def changeVirableOne(value):
            data['update']['N:2'] = value
            insert_thong_edit.setDisabled(value)
            insert_thong_table.setDisabled(value)
            if value:
                insert_thong_edit.setValue(-1)
                insert_thong_edit_first.setText('')
                
        def changeVirableTwo(value):
            data['update']['N=1'] = {
                "status": value,
                "value": insert_ngang_edit.value() if value else 0
            }
            insert_ngang_edit.setDisabled(value)

        
        
        #TODO Set Default for insert
        if old_data:
            date_old = old_data['date'].split('/')
            date_old = [int(item) for item in date_old]
            date_def = QDate(date_old[2],date_old[1],date_old[0]).addDays(1)

            insert_day_edit.setDate(date_def)
            data['insert']['date'] = date_def.toString('dd/MM/yyyy')
            
            value = old_data['ngang']
            insert_ngang_edit.setValue(value)
            number_value = self.number_info[value - 1][:2]
            insert_ngang_edit_first.setText(f'{number_value[0]}')

            thong_value = old_data['thong']
            changeThongEdit(thong_value)
            insert_thong_edit.setValue(thong_value)

        else:
            date_def = QDate().currentDate()
            insert_day_edit.setDate(date_def)
            data['insert']['date'] = date_def.toString('dd/MM/yyyy')

            value = date_def.day()
            insert_ngang_edit.setValue(value)
            number_value = self.number_info[value - 1][:2]
            insert_ngang_edit_first.setText(f'{number_value[0]}')

        if data['update']['N:2']:
            insert_thong_edit.setValue(-1)
            insert_thong_edit.setDisabled(True)
            insert_thong_table.setDisabled(True)
        if data['update']['N=1']['status']:
            value = data['update']['N=1']['value']
            insert_ngang_edit.setValue(value)
            insert_ngang_edit.setDisabled(True)
            number_value = self.number_info[value][:2]
            insert_ngang_edit_first.setText(f'{number_value[0]}')
        
        virable_one_edit.setChecked(data['update']['N:2'])
        virable_two_edit.setChecked(data['update']['N=1']['status'])
        data['insert']['thong'] = insert_thong_edit.value()

        exit.clicked.connect(exit_click)
        submit.clicked.connect(lambda: self.submit_insert(data, dialog))
        #/ Thong
        insert_thong_table.itemClicked.connect(changeThongTable)
        insert_thong_edit.valueChanged.connect(changeThongEdit)

        #/ Date
        insert_day_edit.dateChanged.connect(changeDate)

        #/ Ngang
        insert_ngang_edit.valueChanged.connect(changeNgang)

        #/ Features
        virable_one_edit.clicked.connect(changeVirableOne)
        virable_two_edit.clicked.connect(changeVirableTwo)

    def submit_insert(self,data,dialog):
        data['id'] = self.ban_info['id']
        msg = updateBanInsert(data)
        SendMessage(msg['msg'])
        if msg['status']:
            dialog.reject()
            self.ban_info = msg['data']
            self.insertTableCount(len(self.ban_info['data']))
        return

    # TODO Handler Insert table
    def insertTableCount(self, rowCount):
        self.frozen_table_count.setRowCount(rowCount)
        self.table_scroll_count.setRowCount(rowCount)

        data = self.ban_info['data'][-1]
        day = data['date'].split('/')
        self.frozen_table_count.setVerticalHeaderItem(rowCount -1 , QTableWidgetItem(f'{day[0]}/{day[1]}/.'))
