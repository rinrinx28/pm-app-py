from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,QVBoxLayout,QStackedWidget,QPushButton, QDialog, QGridLayout,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView, QSpinBox, QSplitter,
    QDateEdit, QCheckBox,QMessageBox,QMenu, QScrollArea,QFrame, QButtonGroup
    )
from PySide6.QtGui import Qt, QCursor, QIcon, QColor, QAction, QFont
from PySide6.QtCore import QDate
from Pages.components.stylesheet import (
    css_button_cancel, css_button_submit, css_input, Font, css_lable, SendMessage,
    css_button_view, css_button_normal, css_button_notice,css_title,css_customs_table,
    css_button_checkbox,css_table_header, Note
    )
import json
from Controller.handler import updateBanInsert, updateThongInsert,updateColorInsert,deleteRowBan,deleteFromToBan
import bisect
from functools import partial
class TinhAndMauPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        
        font_ac = QFont()
        font_ac.setPointSize(24)
        font_ac.setBold(True)
        self.font_action = font_ac

        #/ Load Data Bans
        self.bans_path = self.path.path_db()
        with open(self.bans_path, 'r') as file:
            self.bans_db = json.load(file)
        
        self.ban_info = self.bans_db

        #/ Load data Thong and Number
        self.thong_info = None
        self.number_info = None

        #/ Notice
        self.jumpAction = []
        self.noticeView = []

        #/ Config Font
        self.font = Font()

        #/ Config Color
        self.red = QColor(239, 1, 7)
        self.yellow = QColor(255, 215, 0)
        self.cyan = QColor(178, 255, 255)
        
        #/ Navigation Main
        self.navbar_wid_main =QWidget()
        self.navbar_layout = QHBoxLayout(self.navbar_wid_main)
        self.navbar_layout.setSpacing(6)
        self.navbar_layout.setContentsMargins(0,0,0,0)
        self.navbar_wid_main.setFixedHeight(80)
        self.layout.addWidget(self.navbar_wid_main)
        

        self.note_w = QWidget()
        self.note_w.setFont(self.font)
        self.note_l = QHBoxLayout(self.note_w)
        self.note_l.setContentsMargins(0,0,0,0)



        change_number = self.ban_info['meta']['number']
        self.note = QLabel('')
        self.note.setFont(self.font)
        self.note.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.note_l.addWidget(self.note)

        if change_number != 0:
            note = Note[change_number - 1]
            self.note.setText(note)
        else:
            self.note.setText('')

        self.note_color = f'a = sbáo; b = th; c = cột; d = sđếm; ; s = số trong thông; m = sd bmàu'
        self.note_color_label = QLabel()
        self.note_color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.note_l.addWidget(self.note_color_label)

        self.layout.addWidget(self.note_w)

        #/ Widget Main
        self.widget_main = QStackedWidget()
        self.layout.addWidget(self.widget_main)

        #/ Table main
        self.table_main_count = None
        self.table_main_color = None
        self.ranges = []
        self.ranges_current = None
        self.ranges_color = []
        self.ranges_current_color = None

        #/ List Table
        #* Count
        self.frozen_table_count = None
        self.table_scroll_count = None
        # * Color
        self.table_scroll_color = None
        self.frozen_table_color = None

        #/ Button Main
        self.button_wid_main =QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.button_layout.setSpacing(50)
        self.layout.addWidget(self.button_wid_main)

        #/ Show Select Bang and Login into Bang
        self.showSelectBan()   
   
    # TODO handler Render Components
    def loadData(self):
        #/ Load Info thong and Number
        number_change = self.ban_info['meta']['number']
        col_value = self.ban_info['col']
        id_thong = self.ban_info['thong']['id']
        path_thong = self.path.path_thong_with_id_value(id_thong, number_change)
        path_number = self.path.path_number_with_value(number_change)

        with open(path_thong, 'r') as file:
            thong_info = json.load(file)
            self.thong_info = thong_info

        with open(path_number, 'r') as file:
            number_info = json.load(file)
            self.number_info = [number_rang[:col_value] for number_rang in number_info]

    def showSelectBan(self):
        self.loadData()
        self.handlerData()
        self.renderNavigation()
        self.renderTableCount()
        self.renderTableColor()
        self.renderButton()
        # self.showNoticeColorButton()
        self.widget_main.setCurrentWidget(self.table_main_count)
        return

    def renderNavigation(self):
        # Clear previous widgets in the layout
        self.clearLayout(self.navbar_layout)

        lastDate = self.ban_info['data'][-1]['date'] if self.ban_info['data'] else None
        thong_range = self.ban_info['thong']['value']
        thong_range_1, thong_range_2 = thong_range[0] - 1, thong_range[1]

        # Create a widget to contain the buttons
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a scroll area and set its widget to the buttons container
        scroll_area = QScrollArea()
        scroll_area.setFrameStyle(QFrame.NoFrame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(buttons_container)

        self.navbar_layout.addWidget(scroll_area)

        # Create buttons and add them to layout
        for label in range(thong_range_1, thong_range_2):
            button = QPushButton(str(label + 1))
            button.setFixedWidth(60)
            color_find_with_thong = [item for item in self.dataColor if item['thong'] == label and item['notice'] and item['date'] == lastDate]
            if color_find_with_thong:
                button.setStyleSheet(css_button_notice)
                self.addNoticeView(button, label, color_find_with_thong)
                button.clicked.connect(partial(self.handleButtonClick, label))
            else:
                button.setStyleSheet(css_button_normal)
            button.setCursor(Qt.PointingHandCursor)
            buttons_layout.addWidget(button)

        # Add other widgets
        change_number = self.ban_info['meta']['number']
        ban_col = self.ban_info['col']
        ban_thong_value = self.ban_info['thong']['value']
        ban_thong_name = self.ban_info['thong']['name']

        title_text = f'Bảng Tính: {ban_col}C - {ban_thong_value[0]}T đến {ban_thong_value[1]}T - {ban_thong_name} - Bộ Chuyển Đổi {change_number}:'
        title = QLabel(title_text)
        title.setStyleSheet(css_title)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setFixedWidth(900)
        self.navbar_layout.addWidget(title)

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.noticeView = []
        self.jumpAction = []

    def addNoticeView(self, button, label, color_find_with_thong):
        self.noticeView.append({
            "isView": False,
            "label": label,
            "localItem": {
                "row": color_find_with_thong[0]['row'],
                "col": color_find_with_thong[0]['col']
            },
            "button": button,
            "notice": color_find_with_thong[0]['notice']
        })
        
    def handleButtonClick(self, label):
        matching_item = next((item for item in self.noticeView if item['label'] == label))
        if matching_item:
            self.table_scroll_count.clearSelection()
            self.table_scroll_color.clearSelection()
            current_widget = self.widget_main.currentWidget()
            if current_widget != self.table_main_color:
                self.widget_main.setCurrentWidget(self.table_main_color)
            self.TableChange.setText('Bảng Tính')
            self.note_color_label.setText(self.note_color)
            #/ Get Value from Item
            localItem = matching_item['localItem']
            row = localItem['row']
            col = localItem['col']
            button = matching_item['button']
            notice = matching_item['notice']
            #/ Handler Value table
            button.setStyleSheet(css_button_view)
            item_target = self.table_scroll_color.item(row,col)
            self.table_scroll_color.scrollToItem(item_target, hint=QTableWidget.ScrollHint.PositionAtCenter)
            self.setHighlight(item_target,notice)

    # TODO Table Count
    def renderTableCount(self):
        thong_range_1 = self.ban_info['thong']['value'][0]
        #/ Create Widget table
        self.table_main_count = QSplitter(Qt.Horizontal)
        self.table_main_count.setContentsMargins(0,0,0,0)
        self.frozen_table_count = QTableWidget()
        self.table_scroll_count = QTableWidget()
        self.table_main_count.addWidget(self.frozen_table_count)
        self.table_main_count.addWidget(self.table_scroll_count)
        self.widget_main.addWidget(self.table_main_count)

        #/ Config Header
        self.updateHeaderCount()

        self.frozen_table_count.setColumnCount(2)
        for i in range(2):
            if i == 0:
                item = QTableWidgetItem(f'Ngày')
            else:
                item = QTableWidgetItem(f'T.{thong_range_1}')
                item.setForeground(self.red)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_count.setHorizontalHeaderItem(i, item)
        
        #/ Load Row Data
        self.updateTableCount()

        #/ render row
        self.config_frozen_table_count()
        self.config_table_scroll_count()
        self.font_table_count()
        self.connectSignals_count()

    def font_table_count(self):
        #/ Config Font
        font = self.font
        self.frozen_table_count.setFont(font)
        self.frozen_table_count.horizontalHeader().setFont(font)
        self.frozen_table_count.verticalHeader().setFont(font)

        self.table_scroll_count.setFont(self.font)
        self.table_scroll_count.horizontalHeader().setFont(font)
        self.table_scroll_count.verticalHeader().setFont(font)

        self.frozen_table_count.setStyleSheet(
            """
                QTableView {
                    gridline-color: black;
                }
            """
        )
        self.table_scroll_count.setStyleSheet(
            """
                QTableView {
                    gridline-color: black;
                }
            """
        )

    def config_frozen_table_count(self):
        self.frozen_table_count.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.frozen_table_count.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.frozen_table_count.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.frozen_table_count.setMaximumWidth(110 * 2)
        self.frozen_table_count.setMinimumWidth(110 * 2)
        self.frozen_table_count.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.frozen_table_count.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.frozen_table_count.horizontalHeader().setStretchLastSection(True)
        self.frozen_table_count.verticalHeader().hide()
    
    def config_table_scroll_count(self):
        self.table_scroll_count.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_count.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_count.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll_count.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.table_scroll_count.verticalHeader().hide()

    #/ Signals count
    def connectSignals_count(self):
        self.table_scroll_count.horizontalScrollBar().valueChanged.connect(self.update_count)
        self.table_scroll_count.verticalScrollBar().valueChanged.connect(self.syncVerticalScroll_count)
        self.frozen_table_count.verticalScrollBar().valueChanged.connect(self.syncVerticalScroll_count)
        self.table_scroll_count.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_scroll_count.customContextMenuRequested.connect(self.jumpTableWithRow)
    
    def syncVerticalScroll_count(self, value):
        self.frozen_table_count.verticalScrollBar().setValue(value)
        self.table_scroll_count.verticalScrollBar().setValue(value)

    def update_count(self,value):
        # Create a sorted list of range starts and their corresponding indices
        filter_near = [item['start'] for item in self.ranges]
        index_near = bisect.bisect_left(filter_near, value)
        
        if index_near > 0:
            index = index_near - 1
        else:
            index = index_near

        if self.ranges[index]['start'] <= value < self.ranges[index]['end']:
            new_value = value
        elif value < self.ranges[index]['start']:
            new_value = self.ranges[index]['start']
        else:
            # This shouldn't happen, but handle it just in case
            return
        if self.ranges_current == index:
            return
        thong_header = self.ranges[index]['thong']
        self.frozen_table_count.horizontalHeaderItem(1).setText(f'T.{thong_header + 1}')
        for i, item in enumerate(self.ban_info['data']):
            item_thong = item['thong']
            if item_thong > -1:
                thong_value = self.thong_info[thong_header][item_thong]
                self.frozen_table_count.item(i,1).setText(f'{thong_value}')
        self.ranges[index]['value'] = new_value
        self.ranges_current = index

    # TODO Table Color Settings
    def renderTableColor(self):
        thong_range_1 = self.ban_info['thong']['value'][0]
        #/ Create Widget table
        self.table_main_color = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_color)

        #/ Table Create
        # Create a vertical splitter
        self.splitter_left = QSplitter(Qt.Vertical)
        self.frozen_table_left = QTableWidget()
        self.table_scroll_left = QTableWidget()
        self.splitter_left.addWidget(self.frozen_table_left)
        self.splitter_left.addWidget(self.table_scroll_left)
        
        self.table_main_color.addWidget(self.splitter_left)

        # Create a vertical splitter
        self.splitter_right = QSplitter(Qt.Vertical)
        self.frozen_table_color = QTableWidget()
        self.table_scroll_color = QTableWidget()
        self.splitter_right.addWidget(self.frozen_table_color)
        self.splitter_right.addWidget(self.table_scroll_color)

        self.table_main_color.addWidget(self.splitter_right)
        
        #/ Config table
        self.frozen_table_color.setRowCount(1)

        self.frozen_table_left.setRowCount(1)

        self.frozen_table_left.setColumnCount(2)
        self.table_scroll_left.setColumnCount(2)

        #/ Config Header col
        self.updateHeaderColor()
        #/ config header Row
        for i in range(self.frozen_table_left.rowCount()):
            item = QTableWidgetItem(f'Ngày')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_left.setItem(i,0, item)
            item_thong = QTableWidgetItem(f'T.{thong_range_1}')
            item_thong.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_thong.setForeground(QColor(Qt.GlobalColor.red))
            self.frozen_table_left.setItem(i,1, item_thong)
        
        #/ Load Row Data
        self.updateTableColor()

        #/ Config header
        self.font_table_color()
        self.config_header_color()
        self.hide_header_color()
        self.scrollBar_triggers_color()
        self.connectSignals_color()

    def config_header_color(self):
        self.frozen_table_color.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.frozen_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_color.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_color.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.frozen_table_left.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.frozen_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_left.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_scroll_left.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        height_of_row = self.frozen_table_color.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_color.horizontalHeader().sectionSize(0)
        self.frozen_table_color.setMaximumHeight(height_of_row)
        self.frozen_table_color.setMinimumHeight(height_of_row)

        self.frozen_table_left.setMaximumSize(width_of_row + 120, height_of_row)
        self.frozen_table_left.setMinimumSize(width_of_row + 120, height_of_row)

        self.frozen_table_left.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_left.horizontalHeader().setStretchLastSection(True)

    def font_table_color(self):
        #/ Config Font
        font = self.font
        self.frozen_table_color.setFont(font)
        self.frozen_table_color.horizontalHeader().setFont(font)
        self.frozen_table_color.verticalHeader().setFont(font)

        self.table_scroll_color.setFont(font)
        self.table_scroll_color.horizontalHeader().setFont(font)
        self.table_scroll_color.verticalHeader().setFont(font)

        self.frozen_table_left.setFont(font)
        self.frozen_table_left.horizontalHeader().setFont(font)
        self.frozen_table_left.verticalHeader().setFont(font)

        self.table_scroll_left.setFont(font)
        self.table_scroll_left.horizontalHeader().setFont(font)
        self.table_scroll_left.verticalHeader().setFont(font)

        self.frozen_table_color.setStyleSheet(
            """
                QTableView {
                    gridline-color: black;
                }
            """
        )
        
        self.table_scroll_color.setStyleSheet(
            """
                QTableView {
                    gridline-color: black;
                }
            """
        )

    def hide_header_color(self):
        self.frozen_table_color.horizontalHeader().hide()
        self.frozen_table_left.horizontalHeader().hide()
        # self.table_scroll_left.horizontalHeader().hide()

        self.frozen_table_color.verticalHeader().hide()
        self.frozen_table_left.verticalHeader().hide()
        self.table_scroll_color.verticalHeader().hide()
        self.table_scroll_left.verticalHeader().hide()

    def scrollBar_triggers_color(self):
        self.frozen_table_color.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.frozen_table_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_scroll_color.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_scroll_left.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_scroll_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.frozen_table_color.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.frozen_table_left.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll_color.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll_left.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def connectSignals_color(self):
        self.table_scroll_color.horizontalScrollBar().valueChanged.connect(self.update_color)
        self.table_scroll_color.horizontalScrollBar().valueChanged.connect(self.sync_horizontal_scroll_color)
        self.frozen_table_color.horizontalScrollBar().valueChanged.connect(self.sync_horizontal_scroll_color)
        self.table_scroll_color.verticalScrollBar().valueChanged.connect(self.sync_vertical_scroll_color)
        self.table_scroll_left.verticalScrollBar().valueChanged.connect(self.sync_vertical_scroll_color)
        self.table_scroll_color.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_scroll_color.customContextMenuRequested.connect(self.jumpTableWithRow)

    def update_color(self,value):
            # Create a sorted list of range starts and their corresponding indices
            filter_near = [item['start'] for item in self.ranges_color]
            index_near = bisect.bisect_left(filter_near, value)
            
            if index_near > 0:
                index = index_near - 1
            else:
                index = index_near

            if self.ranges_color[index]['start'] <= value < self.ranges_color[index]['end']:
                new_value = value
            elif value < self.ranges_color[index]['start']:
                new_value = self.ranges_color[index]['start']
            else:
                # This shouldn't happen, but handle it just in case
                return
            if self.ranges_current_color == index:
                return
            thong_header = self.ranges_color[index]['thong']
            self.frozen_table_left.item(0, 1).setText(f'T.{thong_header + 1}')
            for i, item in enumerate(self.ban_info['data']):
                item_thong = item['thong']
                if item_thong > -1:
                    thong_value = self.thong_info[thong_header][item_thong]
                    self.table_scroll_left.item(i, 1).setText(f'{thong_value}')
            self.ranges_color[index]['value'] = new_value
            self.ranges_current_color = index
        
    def sync_horizontal_scroll_color(self,vale):
        self.frozen_table_color.horizontalScrollBar().setValue(vale)
        self.table_scroll_color.horizontalScrollBar().setValue(vale)
 
    def sync_vertical_scroll_color(self,vale):
        self.table_scroll_left.verticalScrollBar().setValue(vale)
        self.table_scroll_color.verticalScrollBar().setValue(vale)

    def renderButton(self):
        #/ Delete new row
        DeleteNewRow = QPushButton('Xóa Dòng Mới')
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

        def insertData_Click():
            data = self.ban_info['data']
            if len(data) == 0:
                self.insertData()
                return
            
            if data[-1]['thong'] == -1:
                self.insertThong()
                return
            else:
                self.insertData()
                
        InsertData.clicked.connect(insertData_Click)
        self.TableChange.clicked.connect(self.changeTable)
        SettingTable.clicked.connect(self.changeSettingColor)
        DeleteNewRow.clicked.connect(self.deleteNewRow)
        DeleteFromTo.clicked.connect(self.deleteFromToRow)

    # TODO Handler Button & Dialog
    def insertData(self):
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Bảng Nhập Liệu')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1110,710)
        dialog.show()

        #/ Create Layout
        insert_w = QWidget()
        insert_l = QVBoxLayout(insert_w)
        insert_l.setSpacing(0)
        insert_l.setContentsMargins(0,0,0,0)
        dialog.setLayout(insert_l)

        title_label = QLabel('Bảng Nhập Liệu')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(css_title)
        insert_l.addWidget(title_label)

        layout_w = QWidget()
        layout = QGridLayout(layout_w)
        layout.setSpacing(0)
        insert_l.addWidget(layout_w)

        #/ Table Insert
        insert_thong_table = QTableWidget()
        insert_thong_table.setFixedSize(610, 710)
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
        insert_thong_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

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
        # insert_from_w.setMinimumWidth(530)
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
        insert_ngang_label = QLabel('Dòng Hàng Ngang')
        insert_ngang_label.setStyleSheet(css_lable)

        insert_ngang_grid_w = QWidget()
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
        insert_thong_label = QLabel('Dòng Thông số')
        insert_thong_label.setStyleSheet(css_lable)

        insert_thong_grid_w = QWidget()
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

        virable_two_edit = QCheckBox('CĐ 1 DNgang')
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
        # exit.setFixedWidth(60)

        label_submit = QLabel()
        label_exit = QLabel()
        label_exit.setFixedHeight(220)

        insert_from_l.addWidget(label_submit,6,1)
        insert_from_l.addWidget(submit,7,1)
        insert_from_l.addWidget(label_exit,8,1)
        insert_from_l.addWidget(exit,9,0)

        
        #/ Config Data
        old_data = self.ban_info['data'][-1] if len(self.ban_info['data']) > 0 else None
        data = {}
        data['insert'] = {}
        data['update'] = self.ban_info['meta']['features']

        
        #/ Config Data
        old_data = self.ban_info['data'][-1] if len(self.ban_info['data']) > 0 else None
        data = {}
        data['insert'] = {}
        data['update'] = self.ban_info['meta']['features']

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
            number_value = self.number_info[value - 1]
            insert_ngang_edit_first.setText(f'{number_value[0]}')

        def changeThongTable(value):
            item = value.text()
            changeThongEdit(int(item))
            insert_thong_edit.setValue(int(item))

        def changeThongEdit(value):
            insert_thong_table.clearSelection()
            data['insert']['thong'] = value
            if value == -1:
                insert_thong_edit_first.setText(f'')
                return
            thong_value = self.thong_info[0][value]
            insert_thong_edit_first.setText(f'{thong_value}')

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
                title_label.setText('Bảng Nhập Liệu - Nhập Rời')
            else:
                title_label.setText('Bảng Nhập Liệu - Nhập Liền')
                
        def changeVirableTwo(value):
            data['update']['N=1'] = {
                "status": value,
                "value": insert_ngang_edit.value() - 1 if value else 0
            }
            insert_ngang_edit.setDisabled(value)


        
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
        
        
        #TODO Set Default for insert
        if old_data:
            date_old = old_data['date'].split('/')
            date_old = [int(item) for item in date_old]
            date_def = QDate(date_old[2],date_old[1],date_old[0]).addDays(1)

            insert_day_edit.setDate(date_def)
            data['insert']['date'] = date_def.toString('dd/MM/yyyy')
            
            value = date_def.day()
            data['insert']['ngang'] = value - 1
            insert_ngang_edit.setValue(value)

            thong_value = old_data['thong']
            if thong_value != -1:
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
            title_label.setText('Bảng Nhập Liệu - Nhập Rời')
        else:
            title_label.setText('Bảng Nhập Liệu - Nhập Liền')


        if data['update']['N=1']['status']:
            value = data['update']['N=1']['value']
            insert_ngang_edit.setValue(value + 1)
            insert_ngang_edit.setDisabled(True)
            number_value = self.number_info[value][:2]
            insert_ngang_edit_first.setText(f'{number_value[0]}')
        
        virable_one_edit.setChecked(data['update']['N:2'])
        virable_two_edit.setChecked(data['update']['N=1']['status'])
        data['insert']['thong'] = insert_thong_edit.value()

        exit.clicked.connect(exit_click)
        submit.clicked.connect(lambda: self.submit_insert(data, dialog))

    def submit_insert(self,data,dialog):
        data['id'] = self.ban_info['id']
        data_old = self.ban_info['data']
        msg = updateBanInsert(data)
        if msg['status']:
            dialog.reject()
            if len(data_old) == 0:
                self.renderTableCount()
                self.renderTableColor()
            self.ban_info = msg['data']
            self.widget_main.setCurrentWidget(self.table_main_count)
            self.TableChange.setText('Bảng Màu')
            self.handlerData()
            self.updateTableCount()
            self.updateTableColor()
            self.renderNavigation()
            if data['insert']['thong'] != -1:
                self.questionInsertDate()
        return

    def insertThong(self):
        #/ Config Data
        old_data = self.ban_info['data'][-1] if len(self.ban_info['data']) > 0 else None
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Bảng Nhập Thông')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1110,710)
        dialog.show()

        #/ Create Layout
        insert_w = QWidget()
        insert_l = QVBoxLayout(insert_w)
        insert_l.setSpacing(0)
        insert_l.setContentsMargins(0,0,0,0)
        dialog.setLayout(insert_l)

        title_label = QLabel('Bảng Nhập Thông - Nhập Rời')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(css_lable)
        insert_l.addWidget(title_label)

        layout_w = QWidget()
        layout = QGridLayout(layout_w)
        layout.setSpacing(0)
        insert_l.addWidget(layout_w)

        #/ Table Insert
        insert_thong_table = QTableWidget()
        insert_thong_table.setFixedSize(610, 710)
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
        insert_thong_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

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
        insert_from_w_2 = QWidget()
        insert_from_l_2 = QVBoxLayout(insert_from_w_2)
        insert_from_l_2.setSpacing(100)
        # insert_from_l_2.setContentsMargins(0,5,0,0)
        layout.addWidget(insert_from_w_2, 0, 1)

        insert_from_w = QWidget()
        # insert_from_w.setMinimumWidth(530)
        insert_from_l = QGridLayout(insert_from_w)
        insert_from_l.setSpacing(20)
        insert_from_l_2.addWidget(insert_from_w)

        #/ Title Thong
        insert_thong_title = QLabel('Mời Nhập Thông Số')
        insert_thong_title.setStyleSheet(css_title)
        insert_from_l.addWidget(insert_thong_title, 2,0)


        #/ Insert Thong
        insert_thong_label = QLabel('Dòng Thông')
        insert_thong_label.setStyleSheet(css_lable)
        # insert_thong_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        insert_thong_grid_w = QWidget()
        insert_thong_gird = QGridLayout(insert_thong_grid_w)

        insert_thong_edit = QSpinBox()
        insert_thong_edit.setMinimum(-1)
        insert_thong_edit.setMaximum(120)
        insert_thong_edit.setStyleSheet(css_input)

        insert_thong_edit_first = QLabel('')
        # insert_thong_edit_first.setAlignment(Qt.AlignmentFlag.AlignCenter)
        insert_thong_edit_first.setStyleSheet(
            css_customs_table
        )

        insert_thong_gird.addWidget(insert_thong_edit, 0,0)
        insert_thong_gird.addWidget(insert_thong_edit_first, 0,1)


        insert_from_l.addWidget(insert_thong_label, 3,0)
        insert_from_l.addWidget(insert_thong_grid_w, 3,1)

        #/ Button Insert
        submit = QPushButton('OK Toán')
        submit.setCursor(QCursor(Qt.PointingHandCursor))
        submit.setStyleSheet(css_button_submit)
        submit.setFixedWidth(300)
        submit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        insert_from_l_2.addWidget(submit)

        #/ Button Exit
        exit = QPushButton('Thoát')
        exit.setCursor(QCursor(Qt.PointingHandCursor))
        exit.setStyleSheet(css_button_cancel)
        exit.setFixedWidth(150)
        exit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        insert_from_l_2.addWidget(exit)

        #TODO Set Default for insert
        #TODO Handler Button exit
        def exit_click():
            dialog.reject()

        def changeThongTable(value):
            item = value.text()
            changeThongEdit(int(item))
            insert_thong_edit.setValue(int(item))

        def changeThongEdit(value):
            insert_thong_table.clearSelection()
            old_data['thong'] = value
            if value == -1:
                insert_thong_edit_first.setText('')
                return
            thong_value = self.thong_info[0][value]
            insert_thong_edit_first.setText(f'{thong_value}')

            col = value // 15  # Calculate column index
            row = value % 15  # Calculate row index
            item = insert_thong_table.item(row, col)
            if item:
                item.setSelected(True)

        if old_data:
            thong_value = old_data['thong']
            changeThongEdit(thong_value)
            insert_thong_edit.setValue(thong_value)

        # def cancel_clicked():
        #     dialog.reject()
        #     self.insertData()
        

        # cancel.clicked.connect(cancel_clicked)
        exit.clicked.connect(exit_click)
        submit.clicked.connect(lambda: self.update_thong_insert(old_data, dialog))
        #/ Thong
        insert_thong_table.itemClicked.connect(changeThongTable)
        insert_thong_edit.valueChanged.connect(changeThongEdit)
    
    def update_thong_insert(self, data, dialog):
        data_send = {}
        data_send['thong'] = data
        data_send['id'] = self.ban_info['id']
        msg = updateThongInsert(data_send)
        if msg['status']:
            dialog.reject()
            self.ban_info = msg['data']
            self.widget_main.setCurrentWidget(self.table_main_count)
            self.TableChange.setText('Bảng Màu')
            self.handlerData()
            self.updateTableCount()
            self.updateTableColor()
            self.renderNavigation()
            self.questionInsertDate()
        return

    def questionInsertDate(self):
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        message = QMessageBox()
        message.setWindowTitle('Thông Báo')
        message.setWindowIcon(QIcon(icon))
        message.setText('Nhập liệu dòng mới')
        message.setIcon(QMessageBox.Icon.Question)
        ok_button = message.addButton(QMessageBox.StandardButton.Yes)
        ok_button.setText('OK')
        no_button = message.addButton(QMessageBox.StandardButton.No)
        no_button.setText('Thoát')
        # message.setDefaultButton(ok_button)
        message.setFont(self.font)
        result = message.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.insertData()

    def changeTable(self):
        types = self.TableChange.text()
        if 'Màu' in types:
            self.widget_main.setCurrentWidget(self.table_main_color)
            self.TableChange.setText('Bảng Tính')
            self.note_color_label.setText(self.note_color)
        else:
            self.widget_main.setCurrentWidget(self.table_main_count)
            self.TableChange.setText('Bảng Màu')
            self.note_color_label.setText('')

    def changeSettingColor(self):
        change_data = self.ban_info['meta']['number']
        old_data = self.ban_info['meta']['notice']
        col_e = self.ban_info['meta']['setting']
        col_ngang = self.ban_info
        col_thong = self.ban_info['thong']
        maxRow = self.ban_info['meta']
        buttons = self.ban_info['meta']['buttons']
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Cài đặt bảng')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1000,700)
        dialog.show()

        #/ Create Layout
        layout = QGridLayout()
        layout.setSpacing(6)
        dialog.setLayout(layout)

        #/ Setting Color Table Count
        setting_color_count_w = QWidget()
        setting_color_count_l = QGridLayout(setting_color_count_w)

        setting_color_count_label = QLabel('Cài Đặt Báo Màu Bảng Tính')
        setting_color_count_label.setStyleSheet(css_lable)
        
        setting_color_count_edit_fisrt = QSpinBox()
        setting_color_count_edit_fisrt.setMinimum(0)
        setting_color_count_edit_fisrt.setMaximum(120)
        setting_color_count_edit_fisrt.setStyleSheet(css_input)
        setting_color_count_edit_fisrt.setValue(old_data['count'][0])
        
        setting_color_count_edit_second = QSpinBox()
        setting_color_count_edit_second.setMinimum(0)
        setting_color_count_edit_second.setMaximum(120)
        setting_color_count_edit_second.setStyleSheet(css_input)
        setting_color_count_edit_second.setValue(old_data['count'][1])

        setting_color_count_l.addWidget(setting_color_count_edit_fisrt, 0,0)
        setting_color_count_l.addWidget(setting_color_count_edit_second, 0,1)

        layout.addWidget(setting_color_count_label, 0,0)
        layout.addWidget(setting_color_count_w, 1, 0)

        #/ Setting Color Table Color
        setting_color_color_w = QWidget()
        setting_color_color_l = QGridLayout(setting_color_color_w)

        setting_color_color_label = QCheckBox('Báo Màu Theo Cài Đặt (có là báo)')
        setting_color_color_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        setting_color_color_label.setChecked(buttons[0])
        setting_color_color_label.setStyleSheet(css_lable)
        
        setting_color_color_edit_fisrt = QSpinBox()
        setting_color_color_edit_fisrt.setDisabled(not buttons[0])
        setting_color_color_edit_fisrt.setMinimum(0)
        setting_color_color_edit_fisrt.setMaximum(120)
        setting_color_color_edit_fisrt.setStyleSheet(css_input)
        setting_color_color_edit_fisrt.setValue(old_data['color'][0])
        
        setting_color_color_edit_second = QSpinBox()
        setting_color_color_edit_second.setDisabled(not buttons[0])
        setting_color_color_edit_second.setMinimum(0)
        setting_color_color_edit_second.setMaximum(120)
        setting_color_color_edit_second.setStyleSheet(css_input)
        setting_color_color_edit_second.setValue(old_data['color'][1])

        setting_color_color_l.addWidget(setting_color_color_edit_fisrt, 0,0)
        setting_color_color_l.addWidget(setting_color_color_edit_second, 0,1)

        
        layout.addWidget(setting_color_color_label, 0,1)
        layout.addWidget(setting_color_color_w, 1, 1)

        #/ Setting Thong Change
        setting_thong_change_label = QLabel('Bộ Chuyển Đổi')
        setting_thong_change_label.setStyleSheet(css_lable)
        
        setting_thong_change_edit_fisrt = QSpinBox()
        setting_thong_change_edit_fisrt.setMinimum(0)
        setting_thong_change_edit_fisrt.setMaximum(5)
        setting_thong_change_edit_fisrt.setStyleSheet(css_input)
        setting_thong_change_edit_fisrt.setValue(change_data)

        layout.addWidget(setting_thong_change_label, 2,0)
        layout.addWidget(setting_thong_change_edit_fisrt, 3, 0)

        #/ Setting Buttons Notice
        setting_buttons_notice_label = QCheckBox('Báo Màu Theo Cài Đặt (>= 2 DL)')
        setting_buttons_notice_label.setChecked(buttons[1])
        setting_buttons_notice_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        setting_buttons_notice_label.setStyleSheet(css_lable)

        setting_buttons_notice_edit_w = QWidget()
        setting_buttons_notice_edit_l = QGridLayout(setting_buttons_notice_edit_w)
        
        setting_buttons_notice_edit_fisrt = QSpinBox()
        setting_buttons_notice_edit_fisrt.setMinimum(1)
        setting_buttons_notice_edit_fisrt.setMaximum(120)
        setting_buttons_notice_edit_fisrt.setDisabled(not buttons[1])
        setting_buttons_notice_edit_fisrt.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt.setValue(old_data['color2'][0])
        
        setting_buttons_notice_edit_second = QSpinBox()
        setting_buttons_notice_edit_second.setMinimum(1)
        setting_buttons_notice_edit_second.setMaximum(120)
        setting_buttons_notice_edit_second.setDisabled(not buttons[1])
        setting_buttons_notice_edit_second.setStyleSheet(css_input)
        setting_buttons_notice_edit_second.setValue(old_data['color2'][1])

        setting_buttons_notice_edit_l.addWidget(setting_buttons_notice_edit_fisrt, 0,0)
        setting_buttons_notice_edit_l.addWidget(setting_buttons_notice_edit_second, 0,1)

        layout.addWidget(setting_buttons_notice_label, 2,1)
        layout.addWidget(setting_buttons_notice_edit_w, 3, 1)

        #/ Setting Thong Value
        setting_thong_value_label = QLabel('Số Thông')
        setting_thong_value_label.setStyleSheet(css_lable)

        setting_thong_value_w = QWidget()
        setting_thong_value_l = QGridLayout(setting_thong_value_w)
        
        setting_thong_value_edit_fisrt = QSpinBox()
        setting_thong_value_edit_fisrt.setMinimum(1)
        setting_thong_value_edit_fisrt.setMaximum(420)
        setting_thong_value_edit_fisrt.setStyleSheet(css_input)
        setting_thong_value_edit_fisrt.setValue(col_thong['value'][0])
        
        setting_thong_value_edit_second = QSpinBox()
        setting_thong_value_edit_second.setMinimum(1)
        setting_thong_value_edit_second.setMaximum(420)
        setting_thong_value_edit_second.setStyleSheet(css_input)
        setting_thong_value_edit_second.setValue(col_thong['value'][1])

        setting_thong_value_l.addWidget(setting_thong_value_edit_fisrt, 0,0)
        setting_thong_value_l.addWidget(setting_thong_value_edit_second, 0,1)

        layout.addWidget(setting_thong_value_label, 4,0)
        layout.addWidget(setting_thong_value_w, 5, 0)

        #/ Setting Ngang Value
        setting_ngang_value_label = QLabel('Số Cột Ngang')
        setting_ngang_value_label.setStyleSheet(css_lable)
        
        setting_ngang_value_edit_fisrt = QSpinBox()
        setting_ngang_value_edit_fisrt.setMinimum(1)
        setting_ngang_value_edit_fisrt.setMaximum(600)
        setting_ngang_value_edit_fisrt.setStyleSheet(css_input)
        setting_ngang_value_edit_fisrt.setValue(col_ngang['col'])

        layout.addWidget(setting_ngang_value_label, 4,1)
        layout.addWidget(setting_ngang_value_edit_fisrt, 5, 1)

        #/ Setting Thong Ke D B Tinh
        setting_count_d_label = QLabel('Thông Kê D B Tính')
        setting_count_d_label.setStyleSheet(css_lable)

        setting_count_d_w = QWidget()
        setting_count_d_l = QGridLayout(setting_count_d_w)
        
        setting_count_d_edit_fisrt = QSpinBox()
        setting_count_d_edit_fisrt.setMinimum(2)
        setting_count_d_edit_fisrt.setMaximum(120)
        setting_count_d_edit_fisrt.setStyleSheet(css_input)
        setting_count_d_edit_fisrt.setValue(col_e['col_e'][0])
        
        setting_count_d_edit_second = QSpinBox()
        setting_count_d_edit_second.setMinimum(2)
        setting_count_d_edit_second.setMaximum(120)
        setting_count_d_edit_second.setStyleSheet(css_input)
        setting_count_d_edit_second.setValue(col_e['col_e'][1])

        setting_count_d_l.addWidget(setting_count_d_edit_fisrt, 0,0)
        setting_count_d_l.addWidget(setting_count_d_edit_second, 0,1)

        layout.addWidget(setting_count_d_label, 6,0)
        layout.addWidget(setting_count_d_w, 7, 0)

        #/ Setting Thong Value
        setting_max_row_label = QLabel('Tối Đa Dòng Tồn Tại')
        setting_max_row_label.setStyleSheet(css_lable)
        
        setting_max_row_edit_fisrt = QSpinBox()
        setting_max_row_edit_fisrt.setMinimum(1)
        setting_max_row_edit_fisrt.setMaximum(1000)
        setting_max_row_edit_fisrt.setStyleSheet(css_input)
        setting_max_row_edit_fisrt.setValue(maxRow['maxRow'])

        layout.addWidget(setting_max_row_label, 6,1)
        layout.addWidget(setting_max_row_edit_fisrt, 7, 1)

        #/ Button Save And Exit
        submit_w = QWidget()
        submit_l = QVBoxLayout(submit_w)
        submit = QPushButton('Lưu')
        submit.setStyleSheet(css_button_submit)
        submit_l.addWidget(submit)

        exit_w = QWidget()
        exit_l = QVBoxLayout(exit_w)
        exit = QPushButton('Thoát')
        exit.setStyleSheet(css_button_cancel)
        exit_l.addWidget(exit)

        layout.addWidget(submit_w, 8,0)
        layout.addWidget(exit_w, 8, 1)

        #TODO Handler Button
        def changeColorCount():
            value1 = setting_color_count_edit_fisrt.value()
            value2 = setting_color_count_edit_second.value()
            old_data['count'] = [value1, value2]

        def changeColorColor():
            value1 = setting_color_color_edit_fisrt.value()
            value2 = setting_color_color_edit_second.value()
            old_data['color'] = [value1, value2]

        def changeThong():
            value = setting_thong_change_edit_fisrt.value()
            self.ban_info['meta']['number'] = value
            if value != 0:
                note = Note[value - 1]
                self.note.setText(note)
            else:
                self.note.setText('')
                

        def changeThongValue():
            value_1 = setting_thong_value_edit_fisrt.value()
            value_2 = setting_thong_value_edit_second.value()
            col_thong['value'] = [value_1, value_2]

        def changeNgangValue():
            value = setting_ngang_value_edit_fisrt.value()
            col_ngang['col'] = value

        def changeColunmE():
            value1 = setting_count_d_edit_fisrt.value()
            value2 = setting_count_d_edit_second.value()
            col_e['col_e'] = [value1, value2]

        def changeMaxRow():
            value = setting_max_row_edit_fisrt.value()
            maxRow['maxRow'] = value

        def submit_click():
            data = {
                "id": self.ban_info['id'],
                "notice": old_data,
                "col_e": col_e['col_e'],
                "number": self.ban_info['meta']['number'],
                "col": col_ngang['col'],
                "thong": col_thong,
                "maxRow": maxRow['maxRow'],
                "buttons": self.ban_info['meta']['buttons']
            }
            msg = updateColorInsert(data)
            SendMessage(msg['msg'])
            if msg['status']:
                dialog.reject()
                self.ban_info = msg['data']
                self.widget_main.setCurrentWidget(self.table_main_count)
                self.TableChange.setText('Bảng Màu')
                SendMessage('Xin vui lòng thoát và vào lại bảng tính để cập nhật cài đặt')
            return

        def exit_click():
            dialog.reject()
        
        def changeButtonNotice():
            value1 = setting_buttons_notice_edit_fisrt.value()
            value2 = setting_buttons_notice_edit_second.value()
            old_data['color2'] = [value1, value2]

        def changeButtonsColorTypeOne():
            value1 = setting_color_color_label.isChecked()
            value2 = setting_buttons_notice_label.isChecked()
            if value1:
                setting_color_color_edit_fisrt.setDisabled(False)
                setting_color_color_edit_second.setDisabled(False)

                setting_buttons_notice_label.setChecked(False)
                setting_buttons_notice_edit_fisrt.setDisabled(True)
                setting_buttons_notice_edit_second.setDisabled(True)
                value2 = False
            else:
                setting_color_color_edit_fisrt.setDisabled(True)
                setting_color_color_edit_second.setDisabled(True)

                setting_buttons_notice_label.setChecked(True)
                setting_buttons_notice_edit_fisrt.setDisabled(False)
                setting_buttons_notice_edit_second.setDisabled(False)
                value2 = True

            self.ban_info['meta']['buttons'] = [value1,value2]
        
        def changeButtonsColorTypeTwo():
            value1 = setting_color_color_label.isChecked()
            value2 = setting_buttons_notice_label.isChecked()
            if value2:
                setting_buttons_notice_edit_fisrt.setDisabled(False)
                setting_buttons_notice_edit_second.setDisabled(False)

                setting_color_color_label.setChecked(False)
                setting_color_color_edit_fisrt.setDisabled(True)
                setting_color_color_edit_second.setDisabled(True)
                value1 = False
            else:
                setting_buttons_notice_edit_fisrt.setDisabled(True)
                setting_buttons_notice_edit_second.setDisabled(True)

                setting_color_color_label.setChecked(True)
                setting_color_color_edit_fisrt.setDisabled(False)
                setting_color_color_edit_second.setDisabled(False)
                value1 = True
            
            self.ban_info['meta']['buttons'] = [value1,value2]

            


        #/ Buttons tpye 1 change (Color)
        setting_color_color_edit_fisrt.valueChanged.connect(changeColorColor)
        setting_color_color_edit_second.valueChanged.connect(changeColorColor)
        #/ Buttons Color Count Change
        setting_color_count_edit_fisrt.valueChanged.connect(changeColorCount)
        setting_color_count_edit_second.valueChanged.connect(changeColorCount)
        #/ Change Number
        # setting_ngang_change_edit_fisrt.valueChanged.connect(changeNgang)
        setting_thong_change_edit_fisrt.valueChanged.connect(changeThong)
        #/ Change Value of Thong and Ngang (Column)
        setting_ngang_value_edit_fisrt.valueChanged.connect(changeNgangValue)
        setting_thong_value_edit_fisrt.valueChanged.connect(changeThongValue)
        setting_thong_value_edit_second.valueChanged.connect(changeThongValue)
        #/ Change value of Column Table Color
        setting_count_d_edit_fisrt.valueChanged.connect(changeColunmE)
        setting_count_d_edit_second.valueChanged.connect(changeColunmE)
        #/ Change MaxRow for All Table
        setting_max_row_edit_fisrt.valueChanged.connect(changeMaxRow)
        #/ Buttons Type 2 change (Color)
        setting_buttons_notice_edit_fisrt.valueChanged.connect(changeButtonNotice)
        setting_buttons_notice_edit_second.valueChanged.connect(changeButtonNotice)

        #/ Button Color Type
        setting_buttons_notice_label.stateChanged.connect(changeButtonsColorTypeTwo)
        setting_color_color_label.stateChanged.connect(changeButtonsColorTypeOne)

        submit.clicked.connect(submit_click)
        exit.clicked.connect(exit_click)

    def setHighlight(self, item, isColor):
        if len(self.jumpAction) == 2:
            if self.jumpAction[1]:
                self.jumpAction[0].setBackground(self.jumpAction[1])
            else:
                self.jumpAction[0].setBackground(QColor("#FFFFFF"))
        item.setBackground(self.cyan)
        self.jumpAction = [item, isColor]

    def deleteNewRow(self):
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        message = QMessageBox()
        message.setWindowTitle('Thông Báo')
        message.setWindowIcon(QIcon(icon))
        message.setText('Bạn có muốn xóa dòng mới nhất không?')
        message.setIcon(QMessageBox.Icon.Question)
        message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message.setDefaultButton(QMessageBox.StandardButton.No)
        message.setFont(self.font)
        result = message.exec()

        if result == QMessageBox.StandardButton.Yes:
            #/ delete last data
            self.ban_info['data'] = self.ban_info['data'][:-1]
            msg = deleteRowBan({
                "update": self.ban_info['data'],
                "id": self.ban_info['id']
            })
            #/ Set table count is main
            self.widget_main.setCurrentWidget(self.table_main_count)
            #/ Send Notice Message
            SendMessage(msg)
            #/ re-render all tables
            self.handlerData()
            self.updateTableCount()
            self.updateTableColor()
            self.renderNavigation()

    def deleteFromToRow(self):
        #/ Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle('Cài đặt bảng')
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1000,400)
        dialog.show()

        #/ Default Date
        date = QDate().currentDate()
        date_from = date.addDays(-7)

        #/ Create Layout
        layout = QGridLayout()
        layout.setSpacing(50)
        dialog.setLayout(layout)

        #/ Setting Color Table Count
        delete_from_w = QWidget()
        delete_from_l = QGridLayout(delete_from_w)

        delete_from_label = QLabel('Ngày Bắt Đầu')
        delete_from_label.setStyleSheet(css_lable)
        
        delete_from_edit = QDateEdit()
        delete_from_edit.setCalendarPopup(True)
        delete_from_edit.setStyleSheet(css_input)
        delete_from_edit.setDate(date_from)

        delete_from_l.addWidget(delete_from_edit, 0,0)

        layout.addWidget(delete_from_label, 0,0)
        layout.addWidget(delete_from_w, 1, 0)

        #/ Setting Color Table Color
        delete_to_w = QWidget()
        delete_to_l = QGridLayout(delete_to_w)

        delete_to_label = QLabel('Ngày Kết Thúc')
        delete_to_label.setStyleSheet(css_lable)
        
        delete_to_edit = QDateEdit()
        delete_to_edit.setCalendarPopup(True)
        delete_to_edit.setStyleSheet(css_input)
        delete_to_edit.setDate(date)

        delete_to_l.addWidget(delete_to_edit, 0,0)
        
        layout.addWidget(delete_to_label, 0,1)
        layout.addWidget(delete_to_w, 1, 1)

        #/ Button Save And Exit
        submit_w = QWidget()
        submit_l = QVBoxLayout(submit_w)
        submit = QPushButton('Xóa')
        submit.setStyleSheet(css_button_submit)
        submit_l.addWidget(submit)

        exit_w = QWidget()
        exit_l = QVBoxLayout(exit_w)
        exit = QPushButton('Thoát')
        exit.setStyleSheet(css_button_cancel)
        exit_l.addWidget(exit)

        layout.addWidget(submit_w, 2,0)
        layout.addWidget(exit_w, 2, 1)

        def exit_click():
            dialog.reject()

        def submit_click():
            fromdate = delete_from_edit.date().toString('dd/MM/yyyy')
            todate = delete_to_edit.date().toString('dd/MM/yyyy')
            msg = deleteFromToBan(fromdate, todate, self.ban_info['id'])
            SendMessage(msg['msg'])
            if msg['status']:
                dialog.reject()
                self.ban_info = msg['data']
                self.widget_main.setCurrentWidget(self.table_main_count)
                self.handlerData()
                self.updateTableCount()
                self.updateTableColor()
                self.renderNavigation()

        exit.clicked.connect(exit_click)
        submit.clicked.connect(submit_click)

    def jumpTableWithRow(self, pos):
        self.table_scroll_count.clearSelection()
        self.table_scroll_color.clearSelection()
        current_widget  = self.widget_main.currentWidget()
        color_widget = self.table_main_color
        count_widget = self.table_main_count

        if current_widget == count_widget:
            item_count = self.table_scroll_count.itemAt(pos)
            item_count_data = item_count.data(Qt.ItemDataRole.UserRole)
            if item_count_data:
                menu = QMenu()
                moveTable = QAction('VBM')
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(lambda: self.moveTableWithAction(item_count_data))

                menu.addAction(moveTable)
                menu.exec(self.table_scroll_count.mapToGlobal(pos))
                return
        
        if current_widget == color_widget:
            item_color = self.table_scroll_color.itemAt(pos)
            item_color_data = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_data:
                menu = QMenu()
                moveTable = QAction('VBT')
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(lambda: self.moveTableWithAction(item_color_data))

                menu.addAction(moveTable)
                menu.exec(self.table_scroll_color.mapToGlobal(pos))
                return

    # TODO Handler Data Table
    def updateTableCount(self):
        value_col = self.ban_info['col']
        self.frozen_table_count.setRowCount(0)
        self.table_scroll_count.setRowCount(0)
        ban_info = self.ban_info
        #/ Config table
        rowCount = len(ban_info['data'])
        self.frozen_table_count.setRowCount(rowCount)
        self.table_scroll_count.setRowCount(rowCount)
        thong_range = ban_info['thong']['value']
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1
        for i in range(rowCount):
            date = ban_info['data'][i]['date'].split('/')
            item = QTableWidgetItem(f'{date[0]}/{date[1]}/.')
            self.frozen_table_count.setItem(i,0, item)

        #/ Render Row without Thong
        for item in self.dataCount:
            row_item = item['row']
            col_item = item['col']
            data_item = item['data']
            color_item = item['color']
            notice_item = item['notice']
            item_table = QTableWidgetItem(f'{data_item}')
            item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_table.setForeground(color_item)
            if notice_item:
                item_table.setBackground(notice_item)
            if 'action' in item:
                item_table.setData(Qt.ItemDataRole.UserRole, {"action": item['action'], "isColor": notice_item})
            self.table_scroll_count.setItem(row_item, col_item, item_table)
        
        for i, item in enumerate(ban_info['data']):
            item_thong = item['thong']
            jump_col = 0
            for j in range(thong_ranges):
                if item_thong > - 1:
                    thong_value = self.thong_info[j + thong_range_1][item_thong]
                    if j == 0:
                        item_table = QTableWidgetItem(f'{thong_value}')
                        item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        item_table.setForeground(self.red)
                        self.frozen_table_count.setItem(i, 1, item_table)
                    else:
                        item_table = QTableWidgetItem(f'{thong_value}')
                        item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        item_table.setForeground(self.red)
                        self.table_scroll_count.setItem(i, jump_col, item_table)
                        jump_col += 1
                    jump_col += value_col

        # width_of_row = self.frozen_table_count.horizontalHeader().sectionPosition(0)
        
        # Resize columns to fit content
        # self.frozen_table_count.resizeColumnsToContents()
        # # Get last data
        # if rowCount == 1 and self.ban_info['data'][rowCount - 1]['thong'] == -1:
        #     self.frozen_table_count.setFixedWidth(180)
        # else:
        #     cell_width = 0
        #     for i in range(rowCount):
        #         cell_width = max(cell_width, self.frozen_table_count.visualItemRect(self.frozen_table_count.item(i, 0)).width())
        #     # # Lấy kích thước của header dọc
        #     vertical_header_width = self.frozen_table_count.verticalHeader().width()

        #     # Đặt kích thước cố định cho QTableWidget
        #     self.frozen_table_count.setFixedWidth(cell_width + vertical_header_width)

        self.table_scroll_count.scrollToBottom()
        self.frozen_table_count.scrollToBottom()

    def updateHeaderCount(self):
        self.table_scroll_count.setColumnCount(0)
        self.ranges = []
        cols_arr = []
        total_column = 0
        thong_range = self.ban_info['thong']['value']
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1
        for i in range(thong_ranges):
            range_data = {}
            thong_name = QTableWidgetItem(f'T.{i + thong_range_1 + 1}')
            thong_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            thong_name.setForeground(self.red)
            range_data['start'] = total_column
            range_data['value'] = total_column
            if i != 0:
                cols_arr.append(thong_name)
                total_column += 1
            for j in range(self.ban_info['col']):
                col_name = QTableWidgetItem(f'C.{j + 1}')
                col_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                cols_arr.append(col_name)
                total_column += 1
            range_data['end'] = total_column
            range_data['thong'] = i + thong_range_1
            self.ranges.append(range_data)
        
        self.table_scroll_count.setColumnCount(total_column)

        for i, item in enumerate(cols_arr):
            self.table_scroll_count.setHorizontalHeaderItem(i, item)

    def updateTableColor(self):
        #/ get value setting
        thong_range = self.ban_info['thong']['value']
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1
        col_e = self.ban_info['meta']['setting']['col_e']
        value1 = col_e[0]
        value2 = col_e[1]
        #/ Set RowCount = 0
        self.table_scroll_color.setRowCount(0)
        self.table_scroll_left.setRowCount(0)
        #/ Config rowCount With data 
        rowCount = len(self.ban_info['data'])
        self.table_scroll_color.setRowCount(rowCount)
        self.table_scroll_left.setRowCount(rowCount)
        for i in range(rowCount):
                    data = self.ban_info['data'][i]
                    date = data['date'].split('/')
                    item_thong = data['thong']
                    thong_value = self.thong_info[thong_range_1][item_thong]

                    item = QTableWidgetItem(f'{date[0]}/{date[1]}/.')
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_left.setItem(i,0, item)

                    item_thong_left = QTableWidgetItem(f'{thong_value}')
                    item_thong_left.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item_thong_left.setForeground(QColor(Qt.GlobalColor.red))
                    self.table_scroll_left.setItem(i,1, item_thong_left)

        self.table_scroll_left.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.table_scroll_left.setHorizontalHeaderItem(1, QTableWidgetItem())

        #/ render row defalut
        #/ Tạo cột số đếm ở bảng màu
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for t in range(thong_ranges):
                if t != 0:
                    data = self.ban_info['data'][i]
                    item_thong = data['thong']
                    thong_value = self.thong_info[t + thong_range_1][item_thong]
                    col_thong = QTableWidgetItem(f'{thong_value}')
                    col_thong.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    col_thong.setForeground(QColor(Qt.GlobalColor.red))
                    self.table_scroll_color.setItem(i, total_columns, col_thong)
                    total_columns += 1
                for c in range(value1 - 2, value2 - 1):
                    num_cols = 1  # Số lượng cột tối đa có thể thêm
                    # Thêm tên cột cho hàng header
                    for j in range(num_cols):
                        col_header = QTableWidgetItem(f'*')
                        col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.table_scroll_color.setItem(i,total_columns + j, col_header)
                    # Tạo ô trống ở cột cuối cùng
                    col_null = QTableWidgetItem()
                    col_null.setBackground(QColor(Qt.GlobalColor.white))  # Đặt màu nền là màu trắng
                    self.table_scroll_color.setItem(i,total_columns + num_cols, col_null)
                    # Cập nhật tổng số cột
                    total_columns += num_cols + 1
        
        #/ render row color table
        for item in self.dataColor:
            row_item = item['row']
            col_item = item['col']
            data_item = item['data']
            color_item = item['color']
            notice_item = item['notice']
            action_item = item['action']
            item_insert = QTableWidgetItem(f'{data_item}')
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(Qt.ItemDataRole.UserRole, {"action": action_item, "isColor": notice_item})
            self.table_scroll_color.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_color.columnCount()):
            width = self.table_scroll_color.columnWidth(i)
            self.frozen_table_color.setColumnWidth(i, width)

        self.table_scroll_color.scrollToBottom()
        self.table_scroll_left.scrollToBottom()

    def updateHeaderColor(self):
        thong_range = self.ban_info['thong']['value']
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1
        current_column  = 0
        #/ Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        # step_count = 0

        col_e = self.ban_info['meta']['setting']['col_e']
        value1 = col_e[0]
        value2 = col_e[1]
        for j in range(thong_ranges):
            #/ Tạo cột số đếm ở bảng màu
            for i in range(value1 - 2, value2 - 1):
                current_column  += 2  #/ Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ
            if j != 0:
                current_column += 1

        #/ Thiết lập số lượng cột cho bảng
        self.frozen_table_color.setColumnCount(current_column)
        self.table_scroll_color.setColumnCount(current_column)
        
        #/ Tạo cột số đếm ở bảng màu
        for t in range(thong_ranges):
            range_data = {}
            range_data['start'] = total_columns
            range_data['value'] = total_columns
            if t != 0:
                thong_item = QTableWidgetItem(f"T.{t + thong_range_1 + 1}")
                thong_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                thong_item.setForeground(QColor(Qt.GlobalColor.red))
                self.frozen_table_color.setItem(0, total_columns, thong_item)

                col_null = QTableWidgetItem()
                col_null.setBackground(QColor(Qt.GlobalColor.white))  #/ Đặt màu nền là màu trắng
                self.table_scroll_color.setHorizontalHeaderItem(total_columns, col_null)

                total_columns += 1

            for i in range(value1 - 2, value2  - 1):
                #/ Xác định số lượng cột cho mỗi lần tạo
                num_cols = 1  #/ Số lượng cột tối đa có thể thêm

                #/ Tạo hàng header cho mỗi lần tạo cột
                header_item = QTableWidgetItem(f"D {i + 2}")
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.frozen_table_color.setItem(0, total_columns, header_item)
                # self.frozen_table_color.setSpan(0, total_columns, 1, num_cols)

                #/ Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f'{j + 1}')
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_color.setHorizontalHeaderItem(total_columns + j, col_header)

                #/ Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(QColor(Qt.GlobalColor.white))  #/ Đặt màu nền là màu trắng
                self.table_scroll_color.setHorizontalHeaderItem(total_columns + num_cols, col_null)


                #/ Cập nhật tổng số cột
                total_columns += num_cols + 1
            
            range_data['end'] = total_columns
            range_data['thong'] = t + thong_range_1
            self.ranges_color.append(range_data)
 
    def handlerData(self):
        #/ Config Data
        thong_info = self.thong_info
        ngang_info = self.number_info
        thong_range = self.ban_info['thong']['value']
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1
        ngang = self.ban_info['col']
        data = self.ban_info['data']
        meta = self.ban_info['meta']['notice']
        notice_count = meta['count']
        notice_color1 = meta['color']
        notice_color2 = meta['color2']
        notice_color = []
        buttons = self.ban_info['meta']['buttons']
        if buttons[0]:
            notice_color = notice_color1
        if buttons[1]:
            notice_color = notice_color2
        
        col_e = self.ban_info['meta']['setting']['col_e']
        value1 = col_e[0]
        value2 = col_e[1]

        #/ Setup Variable
        self.count_handler = {} # data so dem (d = Bang tinh, e = Bang mau)
        self.math_isFirst = {} # data toan duoc (c1 = Bang tinh, STT = Bang Mau (Min 3 - Max 4))
        self.isFrits = {} # So dau tien
        self.dataCount = [] # Data Bang tinh
        self.dataColor = [] # Data Bang mau
        #/ Start Render data
        for i, item in enumerate(data):
            item_date = item.get('date')
            item_thong = item.get('thong')
            item_ngang = item.get('ngang')
            total_column = 0
            for t in range(thong_ranges):
                # print(t)
                col_t = thong_info[t + thong_range_1][item_thong] if item_thong > -1 else '*'
                if t != 0:
                    total_column += 1
                for c in range(ngang):
                    col_a = ngang_info[item_ngang][c]
                    stt_cot = c + 1

                    #/ Start Count Handler
                    dem_col_row = f'{stt_cot}:{t}'
                    if not dem_col_row in self.count_handler:
                        self.count_handler[dem_col_row] = 1
                    else:
                        self.count_handler[dem_col_row] += 1
                    #/ End Count Handler
                    col_d = self.count_handler[dem_col_row] # so dem Bang tinh
                    isNoticeCount = self.checkNotice(col_d, notice_count[0], notice_count[1])

                    #/ Start check isFirst
                    isColFisrt = f'{col_a}:{i}:{t}'

                    #/ Check col_a equal col_t
                    isEqual = self.checkColor(str(col_a), str(col_t))

                    if col_d == 1:
                        self.dataCount.append({
                            "row": i,
                            "col": total_column,
                            "color": isEqual,
                            "data": f'{col_a}/{col_d}',
                            "notice": isNoticeCount,
                            "date": item_date,
                            "color_value": col_d,
                        })
                    else:
                        if not isColFisrt in self.isFrits:
                            self.isFrits[isColFisrt] = True

                            #/ Start check col_c is first Like first check
                            maths_c1 = f'{col_d}:{t}:{i}:_color'
                            if not maths_c1 in self.math_isFirst:
                                self.math_isFirst[maths_c1] = 1
                            else:
                                self.math_isFirst[maths_c1] += 1
                            
                            col_c1 = self.math_isFirst[maths_c1]
                            if col_c1 == 1:
                                math_count_handler = f'{col_d}:{i}:{t}:_color'
                                if not math_count_handler in self.count_handler:
                                    self.count_handler[math_count_handler] = 1
                                else:
                                    self.count_handler[math_count_handler] += 1

                                #/ End check col_stt table count
                                stt_count_with_d = self.count_handler[math_count_handler] # So thu tu cua so dem
                                #/ Start count color with col_d
                                if stt_count_with_d == 1:
                                    col_e_count = f'{col_d}:{t}:{stt_count_with_d}:col_e'
                                    if not col_e_count in self.count_handler:
                                        self.count_handler[col_e_count] = 1
                                    else:
                                        self.count_handler[col_e_count] += 1
                                    col_e = self.count_handler[col_e_count] # so dem bang mau
                                    isNoticeColor = self.checkNotice(col_e, notice_color[0], notice_color[1])
                                    #/ End count color with col_d
                                    if col_d >= value1 and col_d <= value2:
                                        step_thong = t
                                        step_col_color = value2 - (value1 - 1)
                                        find_null_color = (1 if col_d - value1 > 0 else 0) * (col_d - value1)
                                        find_stt_color = col_c1 - 1
                                        find_next_color = ( col_d - value1 ) * 1 + step_thong * (step_col_color * 1 + step_col_color + 1)
                                        col_color = find_next_color + find_null_color + find_stt_color  # vi tri col cua item bang mau
                                        #/ Add Data to Table count
                                        self.dataCount.append({
                                            "row": i,
                                            "col": total_column,
                                            "data": f'{col_a}/{t + 1}/{stt_cot}/{col_d}',
                                            "color": isEqual,
                                            "action":{
                                                "name": "color",
                                                "row": i,
                                                "col": col_color
                                            },
                                            "notice": isNoticeCount,
                                            "date": item_date,
                                            "color_value": col_d
                                        })
                                        
                                        #/ Add data to table color
                                        self.dataColor.append({
                                            "row": i,
                                            "col": col_color,
                                            "data": f'{col_a}/{t + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}',
                                            "color": isEqual,
                                            "action":{
                                                "name": 'count',
                                                "row": i,
                                                "col": total_column
                                            },
                                            "notice": isNoticeColor,
                                            "date": item_date,
                                            "color_value": col_e,
                                            "col_d": col_d,
                                            "thong": t
                                        })
                                    
                                    else:
                                        self.dataCount.append({
                                            "row": i,
                                            "col": total_column,
                                            "color": isEqual,
                                            "data": f'{col_a}/{col_d}',
                                            "notice": isNoticeCount,
                                            "color_value": col_d
                                        })

                                    if isEqual:
                                        #/ Reset Col_e with isEqual
                                        self.count_handler[col_e_count] = 0
                                else:
                                    self.dataCount.append({
                                        "row": i,
                                        "col": total_column,
                                        "color": isEqual,
                                        "data": f'{col_a}/{col_d}',
                                        "notice": isNoticeCount,
                                        "date": item_date,
                                        "color_value": col_d
                                    })
                            else:
                                self.dataCount.append({
                                    "row": i,
                                    "col": total_column,
                                    "color": isEqual,
                                    "data": f'{col_a}/{col_d}',
                                    "notice": isNoticeCount,
                                    "date": item_date,
                                    "color_value": col_d
                                })

                        #/ End check col_c is first
                        else:
                            #/ Add Data to Table count without math
                            self.dataCount.append({
                                "row": i,
                                "col": total_column,
                                "color": isEqual,
                                "data": f'{col_a}/{col_d}',
                                "notice": isNoticeCount,
                                "date": item_date,
                                "color_value": col_d
                            })
                        
                    if isEqual:
                        #/ Reset Count col_d if isEqual
                        self.count_handler[dem_col_row] = 0
                    
                    #/ End check isFirst
                    total_column += 1

    def handlerDataColorUpdate(self):
        data_color = self.ban_info['meta']['notice']
        color_count = data_color['count']
        notice_color1 = data_color['color']
        notice_color2 = data_color['color2']
        color_color = []
        buttons = self.ban_info['meta']['buttons']
        if buttons[0]:
            color_color = notice_color1
        if buttons[1]:
            color_color = notice_color2

        # TODO Handler Update Color Table Count
        for i, item in enumerate(self.dataCount):
            color_value = item['color_value']
            isNoticeColor = self.checkNotice(color_value, color_count[0], color_count[1])
            item['notice'] = isNoticeColor
            self.dataCount[i] = item
        
        # TODO Handler Update Color Table Color
        for i, item in enumerate(self.dataColor):
            color_value = item['color_value']
            isNoticeColor = self.checkNotice(color_value, color_color[0], color_color[1])
            item['notice'] = isNoticeColor
            self.dataColor[i] = item
                
    def checkColor(self, value1, value2):
        for char in value1:
            if char in value2:
                return self.red
        return None
            
    def checkNotice(self,value1, notice1, notice2):
        if value1 >= notice1 and value1 <= notice2:
            return self.yellow
        else:
            return None

    def moveTableWithAction(self, data):
        action = data['action']
        name = action['name']
        row = action['row']
        col = action['col']
        if name == 'color':
            self.widget_main.setCurrentWidget(self.table_main_color)
            item = self.table_scroll_color.item(row, col)
            self.table_scroll_color.scrollToItem(item, hint=QTableWidget.ScrollHint.PositionAtCenter)
            self.setHighlight(item, data['isColor'])
            self.TableChange.setText('Bảng Tính')
            self.note_color_label.setText(self.note_color)
        else:
            self.widget_main.setCurrentWidget(self.table_main_count)
            item = self.table_scroll_count.item(row, col)
            self.table_scroll_count.scrollToItem(item, hint=QTableWidget.ScrollHint.PositionAtCenter)
            self.setHighlight(item, data['isColor'])
            self.TableChange.setText('Bảng Màu')
            self.note_color_label.setText('')

    # TODO Handler Widget
    def getWidgetsInLayout(self, layout):
        widgets = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                widgets.append(item.widget())
        return widgets