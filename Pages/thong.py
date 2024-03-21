from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,QVBoxLayout,QStackedWidget,QPushButton, QDialog, QGridLayout,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView,QComboBox
    )
from PySide6.QtGui import Qt, QCursor, QIcon
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note, css_lable, SendMessage
    )
import json
from Controller.handler import createThong, find_files_by_pattern, getFileWithOutBackUp
import os

class ThongPage(QWidget):
    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout_thong = QVBoxLayout(self)

        #/ Load data thong
        self.thong_path = self.path.path_thong()

        with open(os.path.join(self.thong_path, 'thongs.json'), 'r') as file:
            self.thong_db = json.load(file)

        #/ Config Font
        self.font = Font()

        #/ Widget Main
        self.widget_main = QStackedWidget()
        self.layout_thong.addWidget(self.widget_main)

        #/ Table Main
        self.table_main = None

        #/ Button Main
        self.button_wid_main = QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.button_layout.setSpacing(100)
        self.layout_thong.addWidget(self.button_wid_main)

        #/ Render Component
        self.renderButton()
        self.renderTable()

    # TODO Handler Render Component
    def renderTable(self):
        #/ Create Widget table
        self.table_main = QTableWidget()
        self.widget_main.addWidget(self.table_main)
        
        #/ Config table
        rowCount = len(self.thong_db)
        colCount = 2

        self.table_main.setColumnCount(colCount)
        self.table_main.setRowCount(rowCount)

        #/ Config Header
        for i in range(colCount):
            name = 'Tên Bảng' if i == 0 else 'Số Thông'
            item = QTableWidgetItem(f'{name}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setHorizontalHeaderItem(i, item)
        
        #/ Render Rows Table
        for i in range(rowCount):
            data = self.thong_db[i]
            name = data.get('name')
            value = data.get('value')
            item_name = QTableWidgetItem(f'{name}')
            item_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 0, item_name)
            item_value = QTableWidgetItem(f'{value}')
            item_value.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 1, item_value)

        #/ Config Font
        self.table_main.setFont(self.font)
        self.table_main.horizontalHeader().setFont(self.font)
        self.table_main.verticalHeader().setFont(self.font)

        self.table_main.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.horizontalHeader().setStretchLastSection(True)
        
    def renderButton(self):
        #/ Create new Thong
        OpenThong = QPushButton('Mở Bảng Thông')
        OpenThong.setStyleSheet(css_button_submit)
        OpenThong.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(OpenThong)

        #/ Create new Thong
        CreateNew = QPushButton('Tạo Bảng Thông Mới')
        CreateNew.setStyleSheet(css_button_submit)
        CreateNew.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(CreateNew)
        
        #/ Delete Thong
        Delete = QPushButton('Xóa Bảng Thông')
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Delete)

        CreateNew.clicked.connect(self.create_thong)
        OpenThong.clicked.connect(self.open_thong)

    def renderThongTable(self, number):
        self.table_main = QTableWidget()
        self.widget_main.addWidget(self.table_main)

        #/ Find file like id in thong folder
        find_files = find_files_by_pattern(self.thong_path, f'*{self.id}*.json')
        filename = getFileWithOutBackUp(find_files)
        if len(filename) < 2:
            with open(os.path.join(self.thong_path, filename[0]), 'r') as file:
                data = json.load(file)
            self.thong_data = data
        else:
            file = [file for file in filename if f'{self.id}_{number}' in file]
            with open(os.path.join(self.thong_path, file[0]), 'r') as file:
                data = json.load(file)
            self.thong_data = data
        
        #/ Table Config 
        rowCount = len(self.thong_data[0])
        colCount = len(self.thong_data)

        self.table_main.setRowCount(rowCount)
        self.table_main.setColumnCount(colCount + 3)
        
        #/ Add Header Table
        for i in range(colCount):
            if i == 0:
                item_a = QTableWidgetItem(f'A')
                item_a.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(0, item_a)
                
                item_b = QTableWidgetItem(f'B')
                item_b.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(1, item_b)
                
                item_c = QTableWidgetItem(f'C')
                item_c.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(2, item_c)

                item = QTableWidgetItem(f'T.{i+1}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 3, item)
            else:
                item = QTableWidgetItem(f'T.{i+1}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 3, item)

        for i in range(rowCount):
            value = i if i > 9 else f'0{i}'
            item = QTableWidgetItem(f'{value}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setVerticalHeaderItem(i, item)

        #/ Render Rows table
        
        #* Render Rows Custom First
        thong_data_value = [item for item in self.thong_db if item.get('id') == self.id]
        data_value = thong_data_value[0].get('data')
        for i in range(len(data_value)):
            value_col = data_value[i]
            for j in range(len(value_col)):
                item = QTableWidgetItem(f'{value_col[j]}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j,i, item)
        
        #* Render Rows
        for i in range(len(self.thong_data)):
            thong_row = self.thong_data[i]
            for j in range(len(thong_row)):
                item = QTableWidgetItem(f'{thong_row[j]}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j, i + 3, item)
        
        #/ Config Font
        self.table_main.setFont(self.font)
        self.table_main.horizontalHeader().setFont(self.font)
        self.table_main.verticalHeader().setFont(self.font)

        self.table_main.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        #/ Handler Events
        def changeValue(row, column):
            if column > 2:
                item = self.table_main.item(row, column)
                self.thong_data[column - 3][row] = item.text()
            else:
                item = self.table_main.item(row, column)
                data_value[column][row] = item.text()
              
        
        self.table_main.cellChanged.connect(changeValue)
    
    def renderThongButton(self):
        self.button_wid_main = QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.layout_thong.addWidget(self.button_wid_main)
        self.showButtonThong()

    def showButtonThong(self):
        #/ Create Delete
        Delete = QPushButton('Xóa tất cả dữ liệu')
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Delete)

        #/ Create Backup
        BackUp = QPushButton('Khôi phục dữ liệu gốc')
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(BackUp)

        #/ Create ChangeNumber
        ChangeNumber = QPushButton('Bộ Chuyển Đổi')
        ChangeNumber.setStyleSheet(css_button_submit)
        ChangeNumber.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(ChangeNumber)

        #/ Create HandlerData
        HandlerData = QPushButton('Toán')
        HandlerData.setStyleSheet(css_button_submit)
        HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(HandlerData)

        #/ Create SaveData
        SaveData = QPushButton('Lưu')
        SaveData.setStyleSheet(css_button_submit)
        SaveData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(SaveData)

    # TODO Handler Button
    def create_thong(self):
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Tạo Bảng Thông Mới')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(600, 600)
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

        label_name = QLabel('Nhập Tên Thông')
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
        from_l.addWidget(value_thong_w)

        label_value_thong = QLabel('Nhập Số Thông')
        label_value_thong.setStyleSheet(css_lable)
        value_thong_l.addWidget(label_value_thong)

        input_value_thong = QLineEdit()
        input_value_thong.setStyleSheet(css_input)
        value_thong_l.addWidget(input_value_thong)

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
        submit.clicked.connect(lambda: self.submit_button_from(input_name.text(), input_value_thong.text(), input_password.text(),dialog))
        Exit.clicked.connect(exit)

    def submit_button_from(self,name,value, password,dialog):
        if len(name) == 0 and len(value) == 0 and len(password) == 0:
            SendMessage('Xin vui lòng nhập tên bảng, mật khẩu và điền thông số !')
            return
        elif len(name) > 0 and len(value) == 0:
            SendMessage('Xin vui lòng điền thông số!')
            return
        elif len(name) == 0 and len(value) > 0:
            SendMessage('Xin vui lòng nhập tên bảng!')
            return
        
        data = {}
        data['name'] = name
        data['value'] = value
        data['password'] = password
        data_create = createThong(data)
        filter_db = [item for item in self.thong_db if item['id'] != data_create.get('id') and item['name'] != data_create.get('name')]
        filter_db.append(data)
        self.thong_db = filter_db
        # / Close Dialogs From
        dialog.reject()

        #/ Render Table Thong DB
        if self.table_main:
            self.table_main.deleteLater()
            self.widget_main.layout().removeWidget(self.table_main)
            self.table_main = None
        self.renderTable()

        #/ Send Message for client
        SendMessage('Bạn đã tạo bảng thông mới thành công!')
        return

    def open_thong(self):
         #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Mở Bảng Thông')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(600, 600)
        dialog.show()

        #/ Create Layout
        layout = QGridLayout()
        dialog.setLayout(layout)

        #/ Select Thong
        select_w = QWidget()
        select_l = QVBoxLayout(select_w)
        layout.addWidget(select_w)

        select_label = QLabel('Chọn Bảng Thông Để Mở')
        select_label.setStyleSheet(css_lable)
        select_l.addWidget(select_label)

        select_input = QComboBox()
        select_input.setStyleSheet(css_input)
        select_input.setCursor(QCursor(Qt.PointingHandCursor))
        select_input.addItem('Chưa Chọn Bảng Thông')

        for i in range(len(self.thong_db)):
            name = self.thong_db[i]['name']
            select_input.addItem(f'Bảng Thông {name}')
        
        select_l.addWidget(select_input)

        

        #/ Đăng Nhập Thong
        password_w = QWidget()
        password_l = QVBoxLayout(password_w)
        layout.addWidget(password_w)

        password_label = QLabel('Nhập Mật Khẩu Bảng Thông')
        password_label.setStyleSheet(css_lable)
        password_l.addWidget(password_label)

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setStyleSheet(css_input)
        password_input.setCursor(QCursor(Qt.PointingHandCursor))
        password_l.addWidget(password_input)


        #/ Create Button
        button_w = QWidget()
        button_l = QHBoxLayout(button_w)
        button_l.setSpacing(100)
        layout.addWidget(button_w)

        Submit = QPushButton('Đăng Nhập')
        Submit.setStyleSheet(css_button_submit)
        Submit.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(Submit)

        Exit = QPushButton('Thoát')
        Exit.setStyleSheet(css_button_cancel)
        Exit.setCursor(QCursor(Qt.PointingHandCursor))
        button_l.addWidget(Exit)

        #TODO Handler Button Events
        def exit_click():
            dialog.reject()
        
        def submit_click():
            password = password_input.text()
            thong_index = select_input.currentIndex()
            if thong_index > 0:
                thong_data = self.thong_db[thong_index - 1]
                password_thong  = thong_data.get('password')
                if password_thong == password:
                    self.login_thong({"id": thong_data.get('id')}, dialog)
                    return
                else:
                    SendMessage('Mật khẩu không đúng, xin vui lòng thử lại!')
                    return
            else:
                SendMessage('Xin vui lòng chọn thông để mở bảng thông!')
                return
            
        Exit.clicked.connect(exit_click)
        Submit.clicked.connect(submit_click)

    def login_thong(self, data, dialog):
        #/ Delete Dialog
        dialog.reject()
        
        #/ Delete old widgets thongs data and buttons
        self.deleteOldWidgetThongs()

        self.id = data.get('id')
        self.renderThongTable(0)
        self.renderThongButton()
            
    # TODO Handler Widgets
    def deleteOldWidgetThongs(self):
        #/ Delete old table main and buttons
        if self.table_main:
            self.table_main.deleteLater()
            self.widget_main.layout().removeWidget(self.table_main)
            self.table_main = None
        if self.button_wid_main:
            self.button_wid_main.deleteLater()
            self.layout_thong.layout().removeWidget(self.button_wid_main)
            self.button_wid_main = None
        
        