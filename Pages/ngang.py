from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,QLabel
                               )
from PySide6.QtGui import Qt, QCursor, QColor
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note,SendMessage, css_title
    )
import json
import os
from Controller.handler import backUpNgang, saveNgang

prev_selected_rows = set()

class NgangPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout_ngang = QVBoxLayout(self)
        self.ngang_path = self.path.path_number()
        self.thong_path = self.path.path_thong()
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
        self.current_select = []
        self.prev_selected_row = None
        self.cyan = QColor(178, 255, 255)
        self.normal = QColor("#FFFFFF")

        with open(os.path.join(self.thong_path, 'thongs.json'), 'r') as file:
            self.thong_db = json.load(file)

        #/ Title
        name_thong = self.thong_db['name']
        title = QLabel(f'Bảng Ngang - 600 Cột - {name_thong}')
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

        #/ Copy Row Button
        CopyRow = QPushButton('Chép Dòng DL')
        CopyRow.setStyleSheet(css_button_cancel)
        CopyRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(CopyRow)

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

        #/ Delete Button
        DeleteColor = QPushButton('Xóa Màu')
        DeleteColor.setStyleSheet(css_button_cancel)
        DeleteColor.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(DeleteColor)

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

        def copyRow_Click():
            if len(self.current_select) > 2:
                SendMessage('Xin vui lòng chọn dòng chép và nhận!')
                return
            sender = self.prev_selected_row
            receiver = [item for item in self.current_select if item != sender][0]
            self.copyRowNgang([sender, receiver])
            
        def delete_color_click():
            self.table_main.clearSelection()

        self.Change_number.currentIndexChanged.connect(change_number_selected)
        SwapLine.clicked.connect(self.swapNgangRow)
        self.HandlerData.clicked.connect(changeTypeCount)
        Save.clicked.connect(saveChange)
        BackUp.clicked.connect(backupNgang)
        Delete.clicked.connect(deleteRows)
        DeleteRow.clicked.connect(self.DeleteThongRow)
        CopyRow.clicked.connect(copyRow_Click)
        DeleteColor.clicked.connect(delete_color_click)

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

        self.table_main.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

        def selectedRow():
            selected_items = self.table_main.selectedItems()
            if selected_items:
                for item in selected_items:
                    self.selected_row_indices = item.row()
            
            selected_indexes = self.table_main.selectedIndexes()
            if selected_indexes:
                #/ Find is first selected item
                current_selected_row = selected_indexes[0].row()
                if self.prev_selected_row is None or current_selected_row != self.prev_selected_row:
                    self.prev_selected_row = current_selected_row
                
                #/ get all selelected items
                selected_rows = set()
                for i in range(len(selected_indexes)):
                    rows = selected_indexes[i].row()
                    selected_rows.add(rows)
                self.current_select = list(selected_rows)
        
        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                if column > 0:
                    item = self.table_main.item(row, column)
                    filter_db = [item for item in self.ngang_info['change'] 
                                 if item['row'] != row 
                                 and item['column'] != column - 1 
                                 and item['number'] != self.Change_number.currentIndex()]
                    filter_data = [item for item in self.ngang_info['change'] 
                                   if item['row'] == row 
                                   and item['column'] == column - 1 
                                   and item['number'] == self.Change_number.currentIndex()]
                    if len(filter_data) > 0:
                        filter_data[0]['new'] = item.text()
                        self.ngang_info['change'] = filter_db + filter_data
                        if filter_data[0]['new'] != filter_data[0]['old']:
                            item.setBackground(self.cyan)
                        else:
                            item.setBackground(self.normal)
                    else:
                        self.ngang_info['change'].append({
                            "row": row, 
                            "column": column - 1, 
                            "number": self.Change_number.currentIndex(), 
                            "new": item.text(), 
                            "old": self.ngang_data[row][column - 1]
                        })
                        item.setBackground(self.cyan)
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
                filter_changed = [item for item in self.ngang_info['change'] 
                                  if item['row'] == i 
                                  and item['column'] == j 
                                  and item['number'] == self.Change_number.currentIndex()]
                if len(filter_changed) > 0:
                    item_new = filter_changed[0]['new']
                    item_old = filter_changed[0]['old']
                    if item_new != item_old:
                        item.setBackground(self.cyan)
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
        data['change'] = self.ngang_info['change']
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

    def copyRowNgang(self, selceted_rows):
        row1 = selceted_rows[0]
        row2 = selceted_rows[1]    
        row1_h = f'{row1 + 1:02}'  # Ensure proper formatting for display
        row2_h = f'{row2 + 1:02}'
        #/ Check row2 selected, if it not null is return
        data_row2 = self.ngang_data[row2]
        for i, item in enumerate(data_row2):
            if len(str(item)) != 0:
                SendMessage(f'Dòng nhận chưa được xóa dữ liệu! (Dòng {row2_h})')
                return
        sender = self.ngang_data[row1][:]
        self.ngang_data[row2] = sender #/ Copy from sender to receiver
        self.updateRows()
        SendMessage(f'Đã copy dữ liệu từ dòng {row1_h} sang dòng {row2_h} thành công!')
        return
        
        
