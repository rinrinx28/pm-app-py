from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,QVBoxLayout,QStackedWidget,QPushButton, QDialog, QGridLayout,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView,QComboBox,QSpinBox
    )
from PySide6.QtGui import Qt, QCursor, QIcon
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note, css_lable, SendMessage, css_title
    )
import json
from Controller.handler import createThong, saveThong,backupThong
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

        #/ handler count thong
        self.handler = []

        #/ Button Main
        self.button_wid_main = QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.button_layout.setSpacing(100)
        self.layout_thong.addWidget(self.button_wid_main)

        #/ Note
        self.note = QLabel('')
        self.note.setFont(self.font)
        self.layout_thong.addWidget(self.note)

        #/ Render Component
        self.changeDataThongWithNumber(0)
        self.renderThongButton()
        self.renderThongTable()

    # TODO Handler Render Component
    def renderThongTable(self):
        colCount = self.thong_db['value']
        #/ Title and table
        widget_table = QWidget()
        layout_table = QVBoxLayout(widget_table)
        self.widget_main.addWidget(widget_table)
        rowCount = len(self.thong_db['stt'][0])

        layout_table.setSpacing(0)
        layout_table.setContentsMargins(0, 0, 0, 0)

        name_thong = self.thong_db['name']
        value_thong = self.thong_db['value']

        title = QLabel(f'Bảng Thông {name_thong} - Sô Thông {value_thong}')
        title.setStyleSheet(css_title)
        layout_table.addWidget(title)

        self.table_main = QTableWidget()
        layout_table.addWidget(self.table_main)
        self.table_main.setColumnCount(colCount + 5)
        
        #/ Add Header Table

        for i in range(colCount):
            if i == 0:
                item_stt = QTableWidgetItem(f'STT')
                item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(0, item_stt)

                item_a = QTableWidgetItem(f'A')
                item_a.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(1, item_a)
                
                item_b = QTableWidgetItem(f'B')
                item_b.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(2, item_b)
                
                item_c = QTableWidgetItem(f'C')
                item_c.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(3, item_c)
                
                item_d = QTableWidgetItem(f'D')
                item_d.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(4, item_d)

                item = QTableWidgetItem(f'T.{i+1}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 5, item)
            else:
                item = QTableWidgetItem(f'T.{i+1}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 5, item)
        
        #/ Config Font
        self.table_main.setFont(self.font)
        self.table_main.horizontalHeader().setFont(self.font)
        self.table_main.verticalHeader().setFont(self.font)

        self.table_main.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        #/ Handler Events
        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                if column > 4:
                    item = self.table_main.item(row, column)
                    self.thong_data[column - 4][row] = item.text()
                if 0 < column < 5:
                    item = self.table_main.item(row, column)
                    self.thong_db['data'][column - 1][row] = item.text()

        def selectedRow():
            selected_items = self.table_main.selectedItems()
            if selected_items:
                self.selected_row_indices = set()
                for item in selected_items:
                    self.selected_row_indices.add(item.row())

        self.table_main.cellChanged.connect(changeValue)
        self.table_main.itemSelectionChanged.connect(selectedRow)
        self.updateRowAndColumns()

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
        self.ChangeNumber = QComboBox()
        self.ChangeNumber.setStyleSheet(css_input)
        self.ChangeNumber.setCursor(QCursor(Qt.PointingHandCursor))
        self.ChangeNumber.addItem('Bộ Chuyển Đổi 0')
        for i in range(5):
            self.ChangeNumber.addItem(f'Bộ Chuyển Đổi {i+1}')
        self.button_layout.addWidget(self.ChangeNumber)

        #/ Create HandlerData
        type_input = 'Bật Nhập Tay'
        self.HandlerData = QPushButton(type_input)
        self.HandlerData.setStyleSheet(css_button_submit)
        self.HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(self.HandlerData)

        #/ Create MathCount
        swapRow = QPushButton('Đổi Dòng Dữ Liệu')
        swapRow.setStyleSheet(css_button_cancel)
        swapRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(swapRow)

        #/ Create SaveData
        SaveData = QPushButton('Lưu')
        SaveData.setStyleSheet(css_button_submit)
        SaveData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(SaveData)

        def changeTypeCount():
            types = self.HandlerData.text()
            if types == 'Bật Nhập Tay':
                self.table_main.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
                self.HandlerData.setText('Tắt Nhập Tay')
            else:
                self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                self.HandlerData.setText('Bật Nhập Tay')
        
        def saveChange():
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Bật Nhập Tay')
            self.saveThongRow()

        def changeTableNumber():
            value = self.ChangeNumber.currentIndex()
            self.changeDataThongWithNumber(value)
            self.updateRowAndColumns()
            if value != 0:
                note = Note[value - 1]
                self.note.setText(f'{note}')
                self.note.setScaledContents(True)
            else:
                self.note.setText('')
                self.note.setScaledContents(False)

        self.HandlerData.clicked.connect(changeTypeCount)
        SaveData.clicked.connect(saveChange)
        self.ChangeNumber.currentIndexChanged.connect(changeTableNumber)
        BackUp.clicked.connect(self.backUpRows)
        Delete.clicked.connect(self.deleteAllRows)
        swapRow.clicked.connect(self.swapThongRow)

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

    def updateRowAndColumns(self):
        stt = self.thong_db['stt'][self.ChangeNumber.currentIndex()]
        data_value = self.thong_db['data']
        thong_data = self.thong_data
        #/ Table Config
        self.table_main.setRowCount(0)
        rowCount = len(self.thong_data[0])
        self.table_main.setRowCount(rowCount)
        
        #/ Render Rows table
        for i in range(rowCount):
            value = i if i > 9 else f'0{i}'
            item = QTableWidgetItem(f'{value}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setVerticalHeaderItem(i, item)
        #* Render Rows STT First
        for i in range(rowCount):
            stt_value = stt[i]
            item = QTableWidgetItem(f'{stt_value}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,0, item)
        
        #* Render Rows Custom First
        for i in range(len(data_value)):
            value_col = data_value[i]
            for j in range(len(value_col)):
                item = QTableWidgetItem(f'{value_col[j]}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j,i + 1, item)
        
        #* Render Rows
        for i in range(len(thong_data)):
            thong_row = thong_data[i]
            for j in range(len(thong_row)):
                item = QTableWidgetItem(f'{thong_row[j]}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j, i + 5, item)
        
        SendMessage(f'Đã mở Bộ chuyển đổi {self.ChangeNumber.currentIndex()}')

    def deleteAllRows(self):
        rowCount = len(self.thong_data[0])
        stt = self.thong_db['stt'][self.ChangeNumber.currentIndex()]
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Bật Nhập Tay')
        
        self.table_main.clearContents()

        for i in range(len(self.thong_data)):
            for j in range(len(self.thong_data[i])):
                self.thong_data[i][j] = ''
        
        #* Render Rows STT First
        for i in range(rowCount):
            item = QTableWidgetItem(f'{stt[i]}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,0, item)

    def backUpRows(self):
        #/ Load BackUp File with ID
        id = self.thong_db['id']
        data = backupThong({
            "number": self.ChangeNumber.currentIndex(),
            "id": id
        })
        self.thong_db = data['thong_info']
        self.thong_data = data['thong_data']
        
        #/ Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Bật Nhập Tay')

        #/ Render Rows table
        self.updateRowAndColumns()
        
    def saveThongRow(self):
        data = {}
        data['update'] = self.thong_data
        data['custom'] = self.thong_db['data']
        data['id'] = self.thong_db['id']
        data['number'] = self.ChangeNumber.currentIndex()
        data['stt'] = self.thong_db['stt']
        msg = saveThong(data)
        SendMessage(msg)

    def swapThongRow(self):
        #/ Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Bật Nhập Tay')
        #/ Thong Data and Thong info
        stt = self.thong_db['stt'][self.ChangeNumber.currentIndex()]
        data = self.thong_data
        #/ Find Select Row
        data_select = list(self.selected_row_indices)
        if len(data_select) != 2:
            SendMessage('Xin vui lòng chọn 2 dòng để hoán đổi dữ liệu!')
            return
        # Swap items in the 'data' list based on the row indices
        # Ensure indices are within bounds
        if all(0 <= idx <= len(data) for idx in data_select):
            # Create a copy of the data list
            swapped_data_stt = stt.copy()
            swapped_data = data.copy()
            
            # Swap items in the 'swapped_data_stt' list based on the row indices
            for i in range(len(data_select) // 2):
                # Calculate the indices in the 'swapped_data_stt' list
                idx1 = data_select[i]
                idx2 = data_select[-(i + 1)]
                # Swap items using tuple unpacking
                swapped_data_stt[idx1], swapped_data_stt[idx2] = swapped_data_stt[idx2], swapped_data_stt[idx1]
                for j in range(len(swapped_data)):
                    for k in range(len(swapped_data[j])):
                        swapped_data[j][idx1], swapped_data[j][idx2] = swapped_data[j][idx2], swapped_data[j][idx1]

            stt = swapped_data_stt
            data = swapped_data

        self.thong_db['stt'][self.ChangeNumber.currentIndex()] = stt
        self.thong_data = data
        SendMessage('Đã đổi dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại')
        self.updateRowAndColumns()
        return

    def changeDataThongWithNumber(self, number):
        self.thong_data = None
        id = self.thong_db['id']
        with open(os.path.join(self.thong_path, f'thong_{id}_{number}.json'), 'r') as file:
                data = json.load(file)
                self.thong_data = data