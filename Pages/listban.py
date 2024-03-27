from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,QVBoxLayout,QStackedWidget,QPushButton, QDialog, QGridLayout,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView,QComboBox, QSpinBox
    )
from PySide6.QtGui import Qt, QCursor, QIcon
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note, css_lable, SendMessage
    )
import json
from Controller.handler import createBan
import os
class ListBanPage(QWidget):
    
    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout_list = QVBoxLayout(self)

        #/ Load Data Bans
        self.bans_path = self.path.path_db()
        with open(self.bans_path, 'r') as file:
            self.bans_db = json.load(file)

        #/ Load Data Thong
        self.thong_path = self.path.path_thong()
        with open(os.path.join(self.thong_path, 'thongs.json'), 'r') as file:
            self.thong_db = json.load(file)

        #/ Config Font
        self.font = Font()

        #/ Widget Main
        self.widget_main = QStackedWidget()
        self.layout_list.addWidget(self.widget_main)

        #/ Table main
        self.table_main = None

        #/ Button Main
        self.button_wid_main =QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.button_layout.setSpacing(100)
        self.layout_list.addWidget(self.button_wid_main)

        #/ Render Components
        self.renderTable()
        self.renderButton()
    
    # TODO Handler Render Components
    def renderTable(self):
        #/ Create Widget Table
        self.table_main = QTableWidget()
        self.widget_main.addWidget(self.table_main)

        #/ Config table
        rowCount = len(self.bans_db)
        colCount = 4

        self.table_main.setRowCount(rowCount)
        self.table_main.setColumnCount(colCount)

        #/ Config Header
        for i in range(colCount):
            name = ['Tên Bảng', 'Số Cột Sử Dụng', 'Số Thông Sử Dụng','Bộ Chuyển Đổi Sử Dụng']
            item = QTableWidgetItem(f'{name[i]}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setHorizontalHeaderItem(i, item)

        for i in range(rowCount):
            data = self.bans_db[i]
            name = data['name']
            col_value = data['col']
            thong_value = data['thong']['value']
            thong_name = data['thong']['name']
            change_value = data['change']
            
            item_name = QTableWidgetItem(f'Bảng {name}')
            item_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 0, item_name)

            item_col = QTableWidgetItem(f'{col_value}')
            item_col.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 1, item_col)

            item_thong = QTableWidgetItem(f'Bảng Thông {thong_name} - {thong_value}')
            item_thong.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 2, item_thong)

            item_change = QTableWidgetItem(f'{change_value}')
            item_change.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 3, item_change)

        #/ Config Font
        self.table_main.setFont(self.font)
        self.table_main.horizontalHeader().setFont(self.font)
        self.table_main.verticalHeader().setFont(self.font)

        self.table_main.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.horizontalHeader().setStretchLastSection(True)
    
    def renderButton(self):
        #/ Create new Thong
        CreateNew = QPushButton('Tạo Bảng Mới')
        CreateNew.setStyleSheet(css_button_submit)
        CreateNew.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(CreateNew)
        
        #/ Delete Thong
        Delete = QPushButton('Xóa Bảng')
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Delete)

        CreateNew.clicked.connect(self.create_ban)
    

    # TODO Handler Button
    def create_ban(self):
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Tạo Bảng Mới')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(700, 1000)
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

        label_name = QLabel('Nhập Tên Bảng')
        label_name.setStyleSheet(css_lable)
        name_l.addWidget(label_name)

        input_name = QLineEdit()
        input_name.setStyleSheet(css_input)
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

        #? Số Thông
        value_thong_w = QWidget()
        value_thong_l = QVBoxLayout(value_thong_w)
        value_thong_l.setSpacing(5)
        from_l.addWidget(value_thong_w)

        label_value_thong = QLabel('Chọn Bảng Thông và Số Thông')
        label_value_thong.setStyleSheet(css_lable)
        value_thong_l.addWidget(label_value_thong)

        #* From Thong Input
        input_from_w =QWidget()
        input_from_l = QHBoxLayout(input_from_w)
        input_from_l.setSpacing(0)
        value_thong_l.addWidget(input_from_w)

        input_select_thong = QComboBox()
        input_select_thong.setStyleSheet(css_input)
        input_select_thong.addItem('Chọn Bảng Thông')
        for i in range(len(self.thong_db)):
            name = self.thong_db[i]['name']
            input_select_thong.addItem(f'Bảng Thông {name}')
        input_from_l.addWidget(input_select_thong)

        input_value_thong = QSpinBox()
        input_value_thong.setStyleSheet(css_input)
        input_value_thong.setMinimum(0)
        input_value_thong.setMaximum(0)
        input_from_l.addWidget(input_value_thong)

        
        #? Cot Ngang hang
        ngang_number_w = QWidget()
        ngang_number_l = QVBoxLayout(ngang_number_w)
        from_l.addWidget(ngang_number_w)

        label_ngang_number = QLabel('Chọn Số Cột Ngang')
        label_ngang_number.setStyleSheet(css_lable)
        ngang_number_l.addWidget(label_ngang_number)

        input_ngang_number = QSpinBox()
        input_ngang_number.setMinimum(0)
        input_ngang_number.setMaximum(600)
        input_ngang_number.setStyleSheet(css_input)
        ngang_number_l.addWidget(input_ngang_number)

        
        #? Bo chuyen doi
        change_number_w = QWidget()
        change_number_l = QVBoxLayout(change_number_w)
        from_l.addWidget(change_number_w)

        label_change_number = QLabel('Chọn Bộ Chuyển Đổi')
        label_change_number.setStyleSheet(css_lable)
        change_number_l.addWidget(label_change_number)

        input_change_number = QSpinBox()
        input_change_number.setMinimum(0)
        input_change_number.setMaximum(5)
        input_change_number.setStyleSheet(css_input)
        change_number_l.addWidget(input_change_number)

        #/ Create Button
        button_w = QWidget()
        button_l = QHBoxLayout(button_w)
        button_l.setSpacing(100)
        layout.addWidget(button_w)

        #? Submit Button
        submit = QPushButton('Khởi Tạo')
        submit.setStyleSheet(css_button_submit)
        submit.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(submit)

        #? Exit Button
        Exit = QPushButton('Tắt')
        Exit.setStyleSheet(css_button_cancel)
        Exit.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(Exit)

        # TODO Handler Button
        def  exit():
            dialog.reject()

        def changeSelectThong(value):
            if value ==0:
                input_value_thong.setMaximum(0)
            if value != 0:
                value_thong = self.thong_db[value - 1]['value']
                input_value_thong.setMaximum(int(value_thong))

        def submit_click():
            name_value = input_name.text()
            password_value = input_password.text()
            thong_index = input_select_thong.currentIndex() - 1 # Default 0 is not selected
            thong_value = input_value_thong.value()
            ngang_value = input_ngang_number.value()
            change_value = input_change_number.value()
            #/ Check Miss OR
            if (len(name_value) == 0 or 
                    len(password_value) == 0 or 
                    thong_index == -1 or 
                    thong_value == 0 or 
                    ngang_value == 0 or
                    change_value == 0):
                SendMessage('Xin vui lòng nhập đầy đủ dữ kiện!')
                return
            data_create = {}
            data_create['name'] = name_value
            data_create['password'] = password_value
            data_create['col'] = ngang_value
            data_create['thong'] = {}
            data_create['thong']['name'] = self.thong_db[thong_index]['name']
            data_create['thong']['value'] = thong_value
            data_create['thong']['id'] = self.thong_db[thong_index]['id']
            data_create['change'] = change_value
            data_create['meta'] = {
                "notice": { "count": [0, 0], "color": [0, 0] },
                "features": { "N:2": True, "N=1": { "status": False, "value": 0 } },
                "setting": { "col_e": 0}
		    }
            data_create['data'] = []
            msg = self.submit_create_ban(data_create)
            SendMessage(msg)
            dialog.reject()

        
        input_select_thong.currentIndexChanged.connect(changeSelectThong)
        submit.clicked.connect(submit_click)
        Exit.clicked.connect(exit)

    def submit_create_ban(self, data):
        result = createBan(data)
        if type(result) == str:
            return result
        else:
            self.bans_db = result
            #/ Render Table Ban DB
            if self.table_main:
                self.table_main.deleteLater()
                self.widget_main.layout().removeWidget(self.table_main)
                self.table_main = None
            self.renderTable()
            return 'Bạn đã tạo thành công bảng mới'
    