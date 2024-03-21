from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,QLabel
                               )
from PySide6.QtGui import Qt, QCursor
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, Note
    )
import json

class NgangPage(QWidget):
    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout_ngang = QVBoxLayout(self)

        #/ Config Font
        self.font = Font()

        #/ Widget Main
        self.widget_main = QStackedWidget()
        self.layout_ngang.addWidget(self.widget_main)
        
        #/ Table main
        self.table_main = None

        #/ Button main
        button_Wid_main = QWidget()
        self.button_layout = QHBoxLayout(button_Wid_main)
        self.layout_ngang.addWidget(button_Wid_main)

        #/ Note
        self.note = QLabel('')
        self.note.setFont(self.font)
        self.layout_ngang.addWidget(self.note)

        #/ Render Component
        self.renderButton()
        self.renderTable(0)


    # TODO Handler render component
    def renderButton(self):
        #/ SwapLine Button
        SwapLine = QPushButton('Đổi Dòng Dữ Liệu')
        SwapLine.setStyleSheet(css_button_cancel)
        SwapLine.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(SwapLine)

        #/ Delete Button
        Delete = QPushButton('Xóa Tất Cả Dữ Liệu')
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Delete)

        #/ BackUp Button
        BackUp = QPushButton('Khôi Phục dữ liệu Gốc')
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(BackUp)

        #/ Change_number Button
        # TODO Config Change Number
        number = 6
        Change_number = QComboBox()
        Change_number.setStyleSheet(css_input)
        Change_number.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Change_number)
        for i in range(number):
            if i == 0:
                Change_number.addItem(f'Gốc')
            else:
                Change_number.addItem(f'Chuyển Đổi {i}')

        #/ Save Button
        Save = QPushButton('Lưu')
        Save.setStyleSheet(css_button_submit)
        Save.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Save)

        # TODO Handler Button
        def change_number_selected():
            value = Change_number.currentIndex()
            if not self.table_main == None:
                    self.table_main.deleteLater()
                    self.widget_main.layout().removeWidget(self.table_main)
            self.renderTable(value)
            if value != 0:
                note = Note[value - 1]
                self.note.setText(f'{note}')
                self.note.setScaledContents(True)
            else:
                self.note.setText('')
                self.note.setScaledContents(False)

        Change_number.currentIndexChanged.connect(change_number_selected)
        
    def renderTable(self, number):
        # Load data number
        path = self.path.path_number_with_value(number)
        with open(path, 'r') as file:
            data = json.load(file)
        
        #TODO Data configuration
        rowCount = len(data)
        colCount = len(data[0])
        self.start_col = 0
        self.value_col = 0

        self.table_main = QTableWidget()
        self.widget_main.addWidget(self.table_main)
        
        # TODO Config table
        self.table_main.setColumnCount(colCount + 1) #/ Add STT into col
        self.table_main.setRowCount(rowCount)

        # TODO Render Rows
        for i in range(rowCount):
            for j in range(colCount):
                if j == 0:
                    item = QTableWidgetItem(f'{i + 1}')
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_main.setItem(i,j,item)
                value = data[i][j]
                item = QTableWidgetItem(f'{value}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(i,j + 1,item)
        
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

        # TODO Config table Width
        self.table_main.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_main.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # TODO Freeze Col STT Table

        self.table_main.horizontalScrollBar().valueChanged.connect(self.freeze_col_stt)

    # TODO Handler Events
    def freeze_col_stt(self, value):
        if value >= self.start_col:
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value
        elif value < self.start_col:
            value = self.start_col
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value




