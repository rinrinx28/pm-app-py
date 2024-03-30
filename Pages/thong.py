from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,QVBoxLayout,QStackedWidget,QPushButton, QDialog, QGridLayout,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView,QComboBox,QSpinBox
    )
from PySide6.QtGui import Qt, QCursor, QIcon, QColor
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note, css_lable, SendMessage, css_title
    )
import json
from Controller.handler import saveThong,backupThong
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
        self.layout_thong.setSpacing(0)
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

        #/ Render Component
        self.changeDataThongWithNumber(0)
        self.renderThongButton()
        self.renderThongTable()

    # TODO Handler Render Component
    def renderThongTable(self):
        self.start_col = 1
        self.value_col = 1
        colCount = self.thong_db['value']
        #/ Title and table
        widget_table = QWidget()
        layout_table = QVBoxLayout(widget_table)
        self.widget_main.addWidget(widget_table)

        layout_table.setSpacing(0)
        layout_table.setContentsMargins(0, 0, 0, 0)

        value_thong = self.thong_db['value']

        title = QLabel(f'Bảng Thông  - {value_thong} Thông')
        title.setStyleSheet(css_title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_table.addWidget(title)

        #/ Note
        self.note = QLabel('')
        self.note.setFont(self.font)
        layout_table.addWidget(self.note)

        self.table_main = QTableWidget()
        layout_table.addWidget(self.table_main)
        self.table_main.setColumnCount(colCount + 5)

        # self.updateHeaderRow()
        

        for i in range(colCount):
            if i == 0:
                item_stt = QTableWidgetItem(f'STT')
                item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(0, item_stt)

                item_zero = QTableWidgetItem(f'Cột 0')
                item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(1, item_zero)

                item_a = QTableWidgetItem(f'A')
                item_a.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(2, item_a)
                
                item_b = QTableWidgetItem(f'B')
                item_b.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(3, item_b)
                
                item_c = QTableWidgetItem(f'C')
                item_c.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(4, item_c)

                item = QTableWidgetItem(f'T.{i+1}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 5, item)
            else:
                item = QTableWidgetItem(f'T.{i+1}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 5, item)

        
        self.updateRowAndColumns()
        
        #/ Config Font
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

        self.table_main.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        

        self.table_main.horizontalScrollBar().valueChanged.connect(self.freeze_col_stt)

        self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        #/ Handler Events
        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                if column > 4:
                    item = self.table_main.item(row, column)
                    self.thong_data[column - 5][row] = item.text()
                if 1 < column < 5:
                    item = self.table_main.item(row, column)
                    self.thong_db['data'][column - 2][row] = item.text()

        def selectedRow():
            selected_items = self.table_main.selectedItems()
            if selected_items:
                self.selected_row_indices = set()
                for item in selected_items:
                    self.selected_row_indices.add(item.row())

        self.table_main.cellChanged.connect(changeValue)
        self.table_main.itemSelectionChanged.connect(selectedRow)

    def renderThongButton(self):
        self.button_wid_main = QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.layout_thong.addWidget(self.button_wid_main)
        self.showButtonThong()

    def showButtonThong(self):

        #/ Create MathCount
        swapRow = QPushButton('Đổi Dòng DL')
        swapRow.setStyleSheet(css_button_cancel)
        swapRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(swapRow)

        #/ Create Delete
        DeleteRow = QPushButton('Xóa DL dòng')
        DeleteRow.setStyleSheet(css_button_cancel)
        DeleteRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(DeleteRow)

        #/ Create Delete
        Delete = QPushButton('Xóa tất cả DL')
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Delete)

        #/ Create ChangeNumber
        self.ChangeNumber = QComboBox()
        self.ChangeNumber.setStyleSheet(css_input)
        self.ChangeNumber.setCursor(QCursor(Qt.PointingHandCursor))
        self.ChangeNumber.addItem('Bộ Chuyển Đổi 0')
        for i in range(5):
            self.ChangeNumber.addItem(f'Bộ Chuyển Đổi {i+1}')
        self.button_layout.addWidget(self.ChangeNumber)

        #/ Create Backup
        BackUp = QPushButton('Khôi phục DL gốc')
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(BackUp)


        #/ Create HandlerData
        type_input = 'Tắt Tùy Chỉnh'
        self.HandlerData = QPushButton(type_input)
        self.HandlerData.setStyleSheet(css_button_submit)
        self.HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(self.HandlerData)

        #/ Create SaveData
        SaveData = QPushButton('Lưu')
        SaveData.setStyleSheet(css_button_submit)
        SaveData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(SaveData)

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
        DeleteRow.clicked.connect(self.DeleteThongRow)
        swapRow.clicked.connect(self.swapThongRow)

    # TODO Handler Widgets
    def freeze_col_stt(self, value):
        if value >= self.start_col:
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value
        elif value < self.start_col:
            value = self.start_col
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value

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
        self.table_main.clearContents()
        self.table_main.setRowCount(0)
        rowCount = len(self.thong_data[0])
        #/ Add Header Table
        self.table_main.setRowCount(rowCount)

        #* Render Rows STT First
        for i in range(rowCount):
            zero_value = f'{i}' if i > 9 else f'0{i}'
            item_zero = QTableWidgetItem(f'{zero_value}')
            item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,0, item_zero)

            stt_value = stt[i]
            item = QTableWidgetItem(f'{stt_value}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,1, item)
        
        #* Render Rows Custom First
        for i in range(len(data_value)):
            value_col = data_value[i]
            for j in range(len(value_col)):
                item = QTableWidgetItem(f'{value_col[j]}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j,i + 2, item)
        
        #* Render Rows
        for i in range(len(thong_data)):
            thong_row = thong_data[i]
            for j in range(len(thong_row)):
                item = QTableWidgetItem(f'{thong_row[j]}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j, i + 5, item)
        
    def deleteAllRows(self):
        rowCount = len(self.thong_data[0])
        stt = self.thong_db['stt'][self.ChangeNumber.currentIndex()]
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')
        self.table_main.setRowCount(0)
        self.table_main.setRowCount(rowCount)

        for i in range(len(self.thong_data)):
            for j in range(len(self.thong_data[i])):
                self.thong_data[i][j] = ''
        
        #* Render Rows STT First
        for i in range(rowCount):
            zero_value = f'{i}' if i > 9 else f'0{i}'
            item_zero = QTableWidgetItem(f'{zero_value}')
            item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,0, item_zero)

            item = QTableWidgetItem(f'{stt[i]}')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i,1, item)

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
            self.HandlerData.setText('Tắt Tùy Chỉnh')

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
            self.HandlerData.setText('Tắt Tùy Chỉnh')
        #/ Thong Data and Thong info
        stt = self.thong_db['stt'][self.ChangeNumber.currentIndex()]
        data = self.thong_data
        #/ Find Select Row
        data_select = list(self.selected_row_indices)
        if len(data_select) == -1:
            SendMessage('Xin vui lòng chọn 1 dòng để hoán đổi dữ liệu!')
            return
        # Swap items in the 'data' list based on the row indices
        # Ensure indices are within bounds
        part1_stt = stt[:100]
        part2_stt = stt[100:]
        shifted_stt_part1 = [None] * len(part1_stt)
        for i in range(len(part1_stt)):
            shifted_stt_part1[(i + 1) % len(part1_stt)] = part1_stt[i]
        
        shifted_stt = shifted_stt_part1 + part2_stt 
        
        shifted_data = [None] * len(data)

        for i in range(len(data)):
            part1_data = data[i][:100]
            part2_data = data[i][100:]
            shifted_data_part1 = [None] * len(part1_data)

            for j in range(len(part1_data)):
                shifted_data_part1[(j + 1) % len(part1_data)] = part1_data[j]
            
            shifted_data[i] = shifted_data_part1 + part2_data
        

        self.thong_db['stt'][self.ChangeNumber.currentIndex()] = shifted_stt
        self.thong_data = shifted_data
        SendMessage('Đã đổi dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại')
        # self.updateHeaderRow()
        self.updateRowAndColumns()
        return
    
    def DeleteThongRow(self):
        #/ Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText('Tắt Tùy Chỉnh')

        #/ Find Select Row
        data_select = list(self.selected_row_indices)
        if len(data_select) != 1:
            SendMessage('Xin vui lòng chọn 2 dòng để tiến hành xóa dữ liệu!')
            return
        for row in data_select:
            for i in range(5, self.table_main.columnCount()):
                self.thong_data[i - 5][row] = ''
        SendMessage('Đã xóa dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại')
        # self.updateHeaderRow()
        self.updateRowAndColumns()
        return

    def changeDataThongWithNumber(self, number):
        self.thong_data = None
        id = self.thong_db['id']
        with open(os.path.join(self.thong_path, f'thong_{id}_{number}.json'), 'r') as file:
                data = json.load(file)
                self.thong_data = data
        
        SendMessage(f'Đã mở Bộ chuyển đổi {number}')