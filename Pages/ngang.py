from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,QLabel
                               )
from PySide6.QtGui import Qt, QCursor
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note,SendMessage, css_title
    )
import json
import os
from Controller.handler import backUpNgang, saveNgang

class NgangPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout_ngang = QVBoxLayout(self)
        self.ngang_path = self.path.path_number()
        self.layout_ngang.setSpacing(0)
        #/ Config Font
        self.font = Font()

        #/ Config STT 
        self.ngang_info = None
        self.stt_ngang = None
        with open(os.path.join(self.ngang_path, 'number.json'), 'r') as file:
            self.ngang_info = json.load(file)
        self.stt_ngang = self.ngang_info['stt']
        self.selected_row_indices = -1

        #/ Title
        title = QLabel('Bảng Ngang')
        title.setStyleSheet(css_title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_ngang.addWidget(title)

        #/ Note
        self.note = QLabel('')
        self.note.setFont(self.font)
        self.layout_ngang.addWidget(self.note)
        
        #/ Widget Main
        self.widget_main = QStackedWidget()
        self.layout_ngang.addWidget(self.widget_main)
        
        #/ Table main
        self.table_main = None
        self.ngang_data = None

        #/ Button main
        button_Wid_main = QWidget()
        self.button_layout = QHBoxLayout(button_Wid_main)
        self.layout_ngang.addWidget(button_Wid_main)

        #/ Render Component
        self.changeDataNgangWithNumber(0)
        self.renderButton()
        self.renderTable()

    # TODO Handler render component
    def renderButton(self):
        #/ SwapLine Button
        SwapLine = QPushButton('Đổi Dòng DL')
        SwapLine.setStyleSheet(css_button_cancel)
        SwapLine.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(SwapLine)

        #/ Create Delete
        DeleteRow = QPushButton('Xóa DL dòng')
        DeleteRow.setStyleSheet(css_button_cancel)
        DeleteRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(DeleteRow)

        #/ Delete Button
        Delete = QPushButton('Xóa Tất Cả DL')
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Delete)

        #/ Change_number Button
        # TODO Config Change Number
        number = 6
        self.Change_number = QComboBox()
        self.Change_number.setStyleSheet(css_input)
        self.Change_number.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(self.Change_number)
        for i in range(number):
            self.Change_number.addItem(f'Chuyển Đổi {i}')

        #/ BackUp Button
        BackUp = QPushButton('Khôi Phục DL Gốc')
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(BackUp)

        #/ Create HandlerData
        type_input = 'Tắt Tùy Chỉnh'
        self.HandlerData = QPushButton(type_input)
        self.HandlerData.setStyleSheet(css_button_submit)
        self.HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(self.HandlerData)

        #/ Save Button
        Save = QPushButton('Lưu')
        Save.setStyleSheet(css_button_submit)
        Save.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Save)

        # TODO Handler Button
        def change_number_selected():
            value = self.Change_number.currentIndex()
            self.changeDataNgangWithNumber(value)
            self.updateRows()
            if value != 0:
                note = Note[value - 1]
                self.note.setText(f'{note}')
                self.note.setScaledContents(True)
            else:
                self.note.setText('')
                self.note.setScaledContents(False)

        def changeTypeCount():
            types = self.HandlerData.text()
            if types == 'Tắt Tùy Chỉnh':
                self.table_main.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
                self.HandlerData.setText('Bật Tùy Chỉnh')
            else:
                self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                self.HandlerData.setText('Tắt Tùy Chỉnh')
            
        def saveChange():
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')
            self.saveRowNgang()

        def backupNgang():
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')
            self.backUpNgang()

        def deleteRows():
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')
            self.deleteRowNgang()

        self.Change_number.currentIndexChanged.connect(change_number_selected)
        SwapLine.clicked.connect(self.swapNgangRow)
        self.HandlerData.clicked.connect(changeTypeCount)
        Save.clicked.connect(saveChange)
        BackUp.clicked.connect(backupNgang)
        Delete.clicked.connect(deleteRows)
        DeleteRow.clicked.connect(self.DeleteThongRow)

    def renderTable(self):
        data = self.ngang_data
        #TODO Data configuration
        colCount = len(data[0])
        self.start_col = 0
        self.value_col = 0

        self.table_main = QTableWidget()
        self.widget_main.addWidget(self.table_main)
        
        # TODO Config table
        self.table_main.setColumnCount(colCount + 1) #/ Add STT into col
        
        #/ Render Rows
        self.updateRows()
        # TODO Render Header Table
        for i in range(colCount):
            if i == 0:
                item = QTableWidgetItem(f'STT')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i, item)
            
            item = QTableWidgetItem(f'C.{i+1}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setHorizontalHeaderItem(i + 1, item)

        # TODO Add Font
        self.table_main.setFont(self.font)
        self.table_main.horizontalHeader().setFont(self.font)
        self.table_main.verticalHeader().setFont(self.font)

        self.table_main.setStyleSheet(
            """
                QTableView {
                    gridline-color: black;
                }
            """
        )

        # TODO Config table Width
        self.table_main.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # TODO Freeze Col STT Table

        self.table_main.horizontalScrollBar().valueChanged.connect(self.freeze_col_stt)
        
        self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        def selectedRow():
            selected_items = self.table_main.selectedItems()
            if selected_items:
                for item in selected_items:
                    self.selected_row_indices = item.row()
        
        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                if column > 0:
                    item = self.table_main.item(row, column)
                    self.ngang_data[row][column - 1] = item.text()
        
        self.table_main.itemSelectionChanged.connect(selectedRow)
        self.table_main.cellChanged.connect(changeValue)

    # TODO Handler Events
    def freeze_col_stt(self, value):
        if value >= self.start_col:
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value
        elif value < self.start_col:
            value = self.start_col
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value

    def swapNgangRow(self):
        #/ Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')
        #/ Ngang Data and Ngang stt
        stt = self.stt_ngang[self.Change_number.currentIndex()]
        data = self.ngang_data
        #/ Find Select Row
        data_select = self.selected_row_indices
        if data_select == -1:
            SendMessage('Xin vui lòng chọn 1 dòng để hoán đổi dữ liệu!')
            return
        
        # Make sure the index is within range
        if data_select < 0 or data_select >= len(stt):
            SendMessage('Xin vui lòng chọn 1 dòng để hoán đổi dữ liệu!')
            return
        # Tạo một danh sách mới để lưu trữ các phần tử sau khi dịch chuyển
        shifted_stt = [None] * len(stt)
        shifted_data = [None] * len(data)

        # Dịch chuyển các phần tử xuống một vị trí và cập nhật vào danh sách mới
        for i in range(len(stt)):
            shifted_stt[(i + 1) % len(stt)] = stt[i]

        for i in range(len(data)):
            shifted_data[(i + 1) % len(stt)] = data[i]

        self.stt_ngang[self.Change_number.currentIndex()] = shifted_stt
        self.ngang_data = shifted_data
        SendMessage('Đã đổi dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại')
        self.updateRows()
        self.table_main.selectRow(data_select + 1)
        return

    def changeDataNgangWithNumber(self, number):
        self.ngang_data = None
        with open(os.path.join(self.ngang_path, f'number_{number}.json'), 'r') as file:
                data = json.load(file)
                self.ngang_data = data
        SendMessage(f'Đã mở Bộ chuyển đổi {number}')
    
    def updateRows(self):
        data = self.ngang_data
        stt = self.stt_ngang[self.Change_number.currentIndex()]
        colCount = len(data[0])
        rowCount = len(data)
        self.table_main.setRowCount(0)
        self.table_main.setRowCount(rowCount)

        # TODO Render Rows
        for i in range(rowCount):
            stt_value = stt[i]
            item_stt = QTableWidgetItem(f'{stt_value}')
            item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,0,item_stt)
            for j in range(colCount):
                value = data[i][j]
                item = QTableWidgetItem(f'{value}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(i,j + 1,item)
        
    def backUpNgang(self):
        data = {}
        data['number'] = self.Change_number.currentIndex()
        result = backUpNgang(data)

        self.ngang_info = result['stt']

        self.stt_ngang =  self.ngang_info['stt']
        self.ngang_data = result['ngang_data']

        self.updateRows()
        SendMessage('Đã khôi phục dữ liệu thành công!')
    
    def saveRowNgang(self):
        data = {}
        data['update'] = self.ngang_data
        data['number'] = self.Change_number.currentIndex()
        data['stt'] = self.stt_ngang
        saveNgang(data)
        SendMessage('Đã lưu dữ liệu thành công!')

    def deleteRowNgang(self):
        rowCount = len(self.ngang_data)
        stt = self.stt_ngang[self.Change_number.currentIndex()]
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')
        
        self.table_main.setRowCount(0)
        self.table_main.setRowCount(rowCount)
        
        #* Render Rows STT First
        for i in range(rowCount):
            item = QTableWidgetItem(f'{stt[i]}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,0, item)

    def DeleteThongRow(self):
        #/ Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')

        #/ Find Select Row
        data_select = self.selected_row_indices
        if data_select == -1:
            SendMessage('Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!')
            return
        for i in range(len(self.ngang_data[data_select])):
            self.ngang_data[data_select][i] = ''
            
                
        SendMessage('Đã xóa dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại')
        self.updateRows()
        return

