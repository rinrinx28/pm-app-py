from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QPushButton,
    QDialog,
    QGridLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSpinBox,
    QSplitter,
    QDateEdit,
    QCheckBox,
    QMessageBox,
    QMenu,
    QScrollArea,
    QFrame,
    QApplication,
    QSizePolicy,
)
from PySide6.QtGui import Qt, QCursor, QIcon, QColor, QAction, QFont
from PySide6.QtCore import QDate, QTimer
from Pages.components.stylesheet import (
    css_button_cancel,
    css_button_submit,
    css_input,
    Font,
    css_lable,
    SendMessage,
    css_button_view,
    css_button_normal,
    css_button_notice,
    css_title,
    css_customs_table,
    css_button_checkbox,
    css_table_header,
    Note,
)
import json
from Controller.handler import (
    updateBanInsert,
    updateThongInsert,
    updateColorInsert,
    deleteRowBan,
    deleteFromToBan,
    TachVaGhep,
)
import bisect
from functools import partial
import os
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread
from Pages.components.setting import SettingTable


class TinhAndMauPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # / Load Title and Icon Page
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam"
        )
        logo_path = self.path.path_logo()
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)

        font_ac = QFont()
        font_ac.setPointSize(24)
        font_ac.setBold(True)
        self.font_action = font_ac

        # / Load Data Bans
        self.bans_path = self.path.path_db()
        with open(self.bans_path, "r") as file:
            self.bans_db = json.load(file)

        self.ban_info = self.bans_db

        # / Load data Thong and Number
        self.thong_info = None
        self.number_info = None

        # / Notice
        self.jumpAction = {}
        self.noticeView = []
        self.analysis_data = ""

        # / Config LoadingScreen
        self.loadingScreen = LoadingScreen(self.path.path_loading())

        # / Config Font
        self.font = Font()

        # / Config Color
        self.red = QColor(255, 0, 0)
        self.yellow = QColor(255, 215, 0)
        self.cyan = QColor(178, 255, 255)
        self.normal = QColor("#FFFFFF")
        self.stt_highlight = QColor("#EDEADE")

        # / Navigation Main
        self.navbar_wid_main = QWidget()
        self.navbar_layout = QVBoxLayout(self.navbar_wid_main)
        self.navbar_layout.setSpacing(6)
        self.navbar_layout.setContentsMargins(0, 0, 0, 0)
        self.navbar_wid_main.setMaximumHeight(120)
        self.layout.addWidget(self.navbar_wid_main)

        self.note_w = QWidget()
        self.note_w.setFont(self.font)
        self.note_l = QHBoxLayout(self.note_w)
        self.note_l.setContentsMargins(0, 0, 0, 0)

        change_number = self.ban_info["meta"]["number"]
        self.note = QLabel("")
        self.note.setFont(self.font)
        self.note.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.note)

        if change_number != 0:
            note = Note[change_number - 1]
            self.note.setText(note)
        else:
            self.note.setText("")

        self.note_color = f"a = sbáo; b = th; c = cột; d = sđếm; s = số trong thông; m1; m2; m3; m4; m5; m6; m7; m8; m9; m10"
        self.note_color_label = QLabel(self.note_color)
        self.note_color_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.note_l.addWidget(self.note_color_label)

        self.layout.addWidget(self.note_w)

        # / Widget Main
        self.widget_main = QStackedWidget()
        self.layout.addWidget(self.widget_main)

        # / Table main
        self.table_main_count = None
        self.table_main_color = None
        self.table_main_colorM2 = None
        self.table_main_colorM3 = None
        self.table_main_colorM4 = None
        self.table_main_colorM5 = None
        self.table_main_colorM6 = None
        self.table_main_colorM7 = None
        self.table_main_colorM8 = None
        self.table_main_colorM9 = None
        self.table_main_colorM10 = None
        self.ranges = []
        self.ranges_current = None

        # / List Table
        # * Count
        self.frozen_table_count = None
        self.table_scroll_count = None
        # * Color
        self.table_scroll_color = None
        self.frozen_table_color = None
        # * Color M2
        self.table_scroll_colorM2 = None
        self.frozen_table_colorM2 = None
        # * Color M3
        self.table_scroll_colorM3 = None
        self.frozen_table_colorM3 = None
        # * Color M4
        self.table_scroll_colorM4 = None
        self.frozen_table_colorM4 = None
        # * Color M5
        self.table_scroll_colorM5 = None
        self.frozen_table_colorM5 = None
        # * Color M6
        self.table_scroll_colorM6 = None
        self.frozen_table_colorM6 = None
        # * Color M7
        self.table_scroll_colorM7 = None
        self.frozen_table_colorM7 = None
        # * Color M8
        self.table_scroll_colorM8 = None
        self.frozen_table_colorM8 = None
        # * Color M8
        self.table_scroll_colorM8 = None
        self.frozen_table_colorM8 = None
        # * Color M10
        self.table_scroll_colorM10 = None
        self.frozen_table_colorM10 = None

        # / Button Main
        self.button_wid_main = QWidget()
        self.button_layout = QVBoxLayout(self.button_wid_main)
        # self.button_layout.setSpacing(50)
        self.layout.addWidget(self.button_wid_main)

        # / Show Select Bang and Login into Bang
        self.showSelectBan()

    # TODO handler Render Components
    def loadData(self):
        # / Load Info thong and Number
        number_change = self.ban_info["meta"]["number"]
        col_value = self.ban_info["col"]
        id_thong = self.ban_info["thong"]["id"]
        path_thong = self.path.path_thong_with_id_value(id_thong, number_change)
        path_number = self.path.path_number_with_value(number_change)

        with open(path_thong, "r") as file:
            thong_info = json.load(file)
            self.thong_info = thong_info

        with open(path_number, "r") as file:
            number_info = json.load(file)
            self.number_info = [
                number_rang[col_value[0] - 1 : col_value[1]]
                for number_rang in number_info
            ]

        # / Load data thong
        thong_path = self.path.path_thong()

        with open(os.path.join(thong_path, "thongs.json"), "r") as file:
            self.thong_db = json.load(file)

    def showSelectBan(self):
        self.loadData()
        self.handlerData()
        self.renderNavigation()
        self.renderTableCount()
        for i in range(10):
            data = self.ban_info["meta"]["tables"][i]
            if data["enable"]:
                self.start_render_tables(i)
        self.renderButton()
        self.render_table_thong()
        self.widget_main.setCurrentWidget(self.table_main_count)
        return

    def renderNavigation(self, type=None):
        # Clear previous widgets in the layout
        self.clearLayout(self.navbar_layout)
        if type is None:
            table_enabel = [
                i for i, x in enumerate(self.ban_info["meta"]["tables"]) if x["enable"]
            ]
            last_index = table_enabel[-1] if table_enabel else None
            type = f"m{last_index + 1}"

        # / Config Ban info
        ban_info = self.ban_info
        lastDate = ban_info["data"][-1]["date"] if ban_info["data"] else None
        filter_data = [entry for entry in ban_info["data"] if not entry["isDeleted"]]
        row_count = len(filter_data)
        max_row = ban_info["meta"]["maxRow"]
        change_number = ban_info["meta"]["number"]
        ban_col = ban_info["col"]
        ban_thong_value = ban_info["thong"]["value"]
        ban_thong_name = ban_info["thong"]["name"]

        title_text = (
            f"{ban_thong_name}/30 ** Bảng Tính ** C{ban_col[0]} đến C{ban_col[1]} ** T{ban_thong_value[0]} đến "
            + f"T{ban_thong_value[1]} **  Bộ Chuyển Đổi: {change_number} ** "
            + f"Số dòng: {row_count}/{max_row}"
        )

        self.status_w = QWidget()
        self.status_l = QVBoxLayout(self.status_w)

        self.title = QLabel(title_text)
        self.title.setStyleSheet(css_title)
        self.status_l.addWidget(self.title)

        self.navbar_layout.addWidget(self.status_w)

        # / Create a widget to contain the buttons 2
        buttons_container_2 = QWidget()
        buttons_container_2.setMaximumHeight(90)
        buttons_layout_2 = QHBoxLayout(buttons_container_2)
        buttons_layout_2.setAlignment(Qt.AlignmentFlag.AlignTop)

        # / Create a scroll area and set its widget to the buttons container 2
        self.scroll_area_2 = QScrollArea()
        self.scroll_area_2.setFrameStyle(QFrame.NoFrame)
        self.scroll_area_2.setWidgetResizable(True)
        self.scroll_area_2.setWidget(buttons_container_2)

        self.navbar_layout.addWidget(self.scroll_area_2)

        data_color = None
        if type == "m1":
            data_color = self.dataColor
        elif type == "m2":
            data_color = self.dataColor2
        elif type == "m3":
            data_color = self.dataColor3
        elif type == "m4":
            data_color = self.dataColor4
        elif type == "m5":
            data_color = self.dataColor5
        elif type == "m6":
            data_color = self.dataColor6
        elif type == "m7":
            data_color = self.dataColor7
        elif type == "m8":
            data_color = self.dataColor8
        elif type == "m9":
            data_color = self.dataColor9
        else:
            data_color = self.dataColor10

        color_find_with_dCount = [
            item for item in data_color if item["date"] == lastDate and item["notice"]
        ]

        color_sorted = sorted(color_find_with_dCount, key=lambda x: x["col_d"])
        self.color_list = color_sorted

        for label in range(6):
            if label < len(self.color_list):
                isColor = self.color_list[label]
            else:
                isColor = None  # Or any default value
            if isColor:
                # / Add button to list of buttons
                btn_label = isColor["data"]
                btn = QPushButton(btn_label)
                btn.setStyleSheet(css_button_notice)
                btn.setCursor(Qt.PointingHandCursor)
                buttons_layout_2.addWidget(btn)
                self.addNoticeView(btn, f"{btn_label}_{type}", isColor)
                btn.clicked.connect(
                    partial(self.handleButtonClick, f"{btn_label}_{type}")
                )
                # / Set the maximum width for all buttons
                # btn.setFixedWidth(300)
                # TODO set color text if isEqual
                if isColor["color"]:
                    btn.setStyleSheet(
                        f"{css_button_notice}"
                        + """
                        QPushButton {
                            color: red;
                        }
                    
                        """
                    )

            else:
                # / Add button to list of buttons
                btn_label = str(label + 1)
                btn = QPushButton(btn_label)
                btn.setFixedWidth(60)
                btn.setStyleSheet(css_button_normal)
                btn.setCursor(Qt.PointingHandCursor)
                buttons_layout_2.addWidget(btn)

        # / reRender Data Analysis Color D
        value_input = self.analysis_data
        if len(value_input) > 0:
            if "," in value_input:
                value_input = value_input.split(",")
            else:
                value_input = [value_input]
            self.handler_data_analysis(value_input)

    def renderTableCount(self):
        thong_range_1 = self.ban_info["thong"]["value"][0]

        # Create Widget table
        self.table_main_count = QSplitter(Qt.Horizontal)
        self.table_main_count.setContentsMargins(0, 0, 0, 0)
        self.frozen_table_count = QTableWidget()
        self.table_scroll_count = QTableWidget()
        self.table_main_count.addWidget(self.frozen_table_count)
        self.table_main_count.addWidget(self.table_scroll_count)
        self.widget_main.addWidget(self.table_main_count)

        # Config Header
        self.updateHeaderCount()

        # Set column count and header items for frozen_table_count
        self.frozen_table_count.setColumnCount(2)
        headers = ["Ngày", f"T.{thong_range_1}"]
        for i, header_text in enumerate(headers):
            item = QTableWidgetItem(header_text)
            item.setForeground(self.red) if i == 1 else None
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_count.setHorizontalHeaderItem(i, item)

        # Set font and style for tables
        tables = [self.frozen_table_count, self.table_scroll_count]
        for table in tables:
            table.setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )

        self.frozen_table_count.horizontalHeader().setStretchLastSection(True)
        # Set properties for frozen_table_count
        self.frozen_table_count.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.frozen_table_count.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.frozen_table_count.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectItems
        )
        self.frozen_table_count.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.frozen_table_count.verticalHeader().hide()
        self.frozen_table_count.setMaximumWidth(150 * 2)
        self.frozen_table_count.setMinimumWidth(150 * 2)
        self.frozen_table_count.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.frozen_table_count.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Set properties for table_scroll_count
        self.table_scroll_count.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_scroll_count.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_scroll_count.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_scroll_count.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectItems
        )
        self.table_scroll_count.verticalHeader().hide()

        # Connect signal handlers
        self.table_scroll_count.horizontalScrollBar().valueChanged.connect(
            self.update_count
        )
        for scroll_bar in [
            self.table_scroll_count.verticalScrollBar(),
            self.frozen_table_count.verticalScrollBar(),
        ]:
            scroll_bar.valueChanged.connect(self.sync_vertical_scroll_count)
        self.table_scroll_count.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_count.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        # Render row
        self.updateTableCount()

    # / Update function for horizontal scrollbar value change

    def update_count(self, value):
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        index_near = bisect.bisect_left([item["start"] for item in self.ranges], value)
        index = max(0, index_near - 1)
        if self.ranges[index]["start"] <= value < self.ranges[index]["end"]:
            new_value = value
        elif value < self.ranges[index]["start"]:
            new_value = self.ranges[index]["start"]
        else:
            return
        if self.ranges_current == index:
            return
        thong_header = self.ranges[index]["thong"]
        self.frozen_table_count.horizontalHeaderItem(1).setText(f"T.{thong_header + 1}")
        for i, item in enumerate(filter_data):
            item_thong = item["thong"]
            if item_thong > -1:
                thong_value = self.thong_info[thong_header][item_thong]
                self.frozen_table_count.item(i, 1).setText(f"{thong_value}")
        self.ranges[index]["value"] = new_value
        self.ranges_current = index

    # TODO Function to sync vertical scrollbar
    def sync_vertical_scroll_count(self, value):
        self.frozen_table_count.verticalScrollBar().setValue(value)
        self.table_scroll_count.verticalScrollBar().setValue(value)

    # TODO Handle Table M1

    def renderTableColor(self):
        # / Create Widget table
        self.table_main_color = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_color)

        # / Table Create
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

        # / Config table
        self.frozen_table_color.setRowCount(1)

        self.frozen_table_left.setRowCount(1)

        self.frozen_table_left.setColumnCount(1)
        self.table_scroll_left.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColor()
        # / config header Row
        for i in range(self.frozen_table_left.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_left.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_color()

        height_of_row = self.frozen_table_color.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_color.horizontalHeader().sectionSize(0)
        self.frozen_table_color.setMaximumHeight(height_of_row)
        self.frozen_table_color.setMinimumHeight(height_of_row)

        self.frozen_table_left.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_left.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_left.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_left.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_color.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_left.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_left.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_left.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scroll(vale):
            self.frozen_table_color.horizontalScrollBar().setValue(vale)
            self.table_scroll_color.horizontalScrollBar().setValue(vale)

        def sync_vertical_scroll(vale):
            self.table_scroll_left.verticalScrollBar().setValue(vale)
            self.table_scroll_color.verticalScrollBar().setValue(vale)

        self.table_scroll_color.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scroll
        )
        self.frozen_table_color.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scroll
        )
        self.table_scroll_color.verticalScrollBar().valueChanged.connect(
            sync_vertical_scroll
        )
        self.table_scroll_left.verticalScrollBar().valueChanged.connect(
            sync_vertical_scroll
        )

        self.table_scroll_color.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_color.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColor()

    def configheader_table_color(self):
        for table in [
            self.frozen_table_color,
            self.frozen_table_left,
            self.table_scroll_color,
            self.table_scroll_left,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_color, self.frozen_table_left]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_color:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handler Button PM
    def renderButton(self):
        button_main_1_w = QWidget()
        button_main_1_l = QHBoxLayout(button_main_1_w)
        self.button_layout.addWidget(button_main_1_w)
        button_main_2_w = QWidget()
        button_main_2_l = QHBoxLayout(button_main_2_w)
        self.button_layout.addWidget(button_main_2_w)

        # / Delete new row
        DeleteNewRow = QPushButton("Xóa Dòng Mới")
        DeleteNewRow.setStyleSheet(css_button_submit)
        DeleteNewRow.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(DeleteNewRow)

        # / Delete from to
        DeleteFromTo = QPushButton("Xóa Từ Ngày")
        DeleteFromTo.setStyleSheet(css_button_submit)
        DeleteFromTo.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(DeleteFromTo)

        # / Setting Table
        SettingTable = QPushButton("Cài Đặt Bảng")
        SettingTable.setStyleSheet(css_button_submit)
        SettingTable.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(SettingTable)

        # / Insert Data row
        InsertData = QPushButton("Nhập Liệu")
        InsertData.setStyleSheet(
            """
                QPushButton {
                    padding: 10px;
                    border-radius: 8px; 
                    font-size: 24px;
                    line-height: 32px;
                    font-weight: 600; 
                    color: #ffffff; 
                    background-color: #7CFC00;
                }
            """
        )
        InsertData.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(InsertData)

        # / Bảng Màu
        self.TableChange = QPushButton("Bảng Tính")
        self.TableChange.setStyleSheet(css_button_submit)
        self.TableChange.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(self.TableChange)

        def insertData_Click():
            data = self.ban_info["data"]
            if len(data) == 0:
                self.insertData()
                return

            if data[-1]["thong"] == -1:
                self.insertThong()
                return
            else:
                self.insertData()

        def changeTable():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_count)
            self.renderNavigation()
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Tính")
                    self.title.setText(new_title)
                    return

        def changeTableM1():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_color)
            self.renderNavigation("m1")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 1")
                    self.title.setText(new_title)
                    return

        def changeTableM2():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM2)
            self.renderNavigation("m2")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 2")
                    self.title.setText(new_title)

        def changeTableM3():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM3)
            self.renderNavigation("m3")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 3")
                    self.title.setText(new_title)

        def changeTableM4():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM4)
            self.renderNavigation("m4")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 4")
                    self.title.setText(new_title)

        def changeTableM5():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM5)
            self.renderNavigation("m5")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 5")
                    self.title.setText(new_title)

        def changeTableM6():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM6)
            self.renderNavigation("m6")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 6")
                    self.title.setText(new_title)

        def changeTableM7():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM7)
            self.renderNavigation("m7")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 7")
                    self.title.setText(new_title)

        def changeTableM8():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM8)
            self.renderNavigation("m8")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 8")
                    self.title.setText(new_title)

        def changeTableM9():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM9)
            self.renderNavigation("m9")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 9")
                    self.title.setText(new_title)

        def changeTableM10():
            old_title = self.title.text()
            self.widget_main.setCurrentWidget(self.table_main_colorM10)
            self.renderNavigation("m10")
            for text in sorted(
                [
                    "Bảng Màu 10",
                    "Bảng Màu 9",
                    "Bảng Màu 8",
                    "Bảng Màu 7",
                    "Bảng Màu 6",
                    "Bảng Màu 5",
                    "Bảng Màu 4",
                    "Bảng Màu 3",
                    "Bảng Màu 2",
                    "Bảng Màu 1",
                    "Bảng Tính",
                ],
                key=len,
                reverse=True,
            ):
                if text in old_title:
                    new_title = old_title.replace(text, "Bảng Màu 10")
                    self.title.setText(new_title)

        for i in range(10):
            info_data = self.ban_info["meta"]["tables"][i]
            if info_data["enable"]:
                match i:
                    case 0:
                        # / Bảng Màu 1
                        self.TableM1 = QPushButton("BM M1")
                        self.TableM1.setStyleSheet(css_button_submit)
                        self.TableM1.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM1)
                        self.TableM1.clicked.connect(changeTableM1)
                    case 1:

                        # / BM 2
                        self.TableM2 = QPushButton("BM M2")
                        self.TableM2.setStyleSheet(css_button_submit)
                        self.TableM2.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM2)
                        self.TableM2.clicked.connect(changeTableM2)
                    case 2:
                        # / BM 3
                        self.TableM3 = QPushButton("BM M3")
                        self.TableM3.setStyleSheet(css_button_submit)
                        self.TableM3.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM3)
                        self.TableM3.clicked.connect(changeTableM3)
                    case 3:
                        # / BM 4
                        self.TableM4 = QPushButton("BM M4")
                        self.TableM4.setStyleSheet(css_button_submit)
                        self.TableM4.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM4)
                        self.TableM4.clicked.connect(changeTableM4)
                    case 4:
                        # / BM 5
                        self.TableM5 = QPushButton("BM M5")
                        self.TableM5.setStyleSheet(css_button_submit)
                        self.TableM5.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM5)
                        self.TableM5.clicked.connect(changeTableM5)
                    case 5:
                        # / BM 6
                        self.TableM6 = QPushButton("BM M6")
                        self.TableM6.setStyleSheet(css_button_submit)
                        self.TableM6.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM6)
                        self.TableM6.clicked.connect(changeTableM6)
                    case 6:
                        # / BM 7
                        self.TableM7 = QPushButton("BM M7")
                        self.TableM7.setStyleSheet(css_button_submit)
                        self.TableM7.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM7)
                        self.TableM7.clicked.connect(changeTableM7)
                    case 7:
                        # / BM 8
                        self.TableM8 = QPushButton("BM M8")
                        self.TableM8.setStyleSheet(css_button_submit)
                        self.TableM8.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM8)
                        self.TableM8.clicked.connect(changeTableM8)
                    case 8:
                        # / BM 9
                        self.TableM9 = QPushButton("BM M9")
                        self.TableM9.setStyleSheet(css_button_submit)
                        self.TableM9.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM9)
                        self.TableM9.clicked.connect(changeTableM9)
                    case 9:
                        # / BM 10
                        self.TableM10 = QPushButton("BM M10")
                        self.TableM10.setStyleSheet(css_button_submit)
                        self.TableM10.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM10)
                        self.TableM10.clicked.connect(changeTableM10)
                    case _:
                        pass

        InsertData.clicked.connect(insertData_Click)
        self.TableChange.clicked.connect(changeTable)
        SettingTable.clicked.connect(self.changeSettingColor)
        DeleteNewRow.clicked.connect(self.deleteNewRow)
        DeleteFromTo.clicked.connect(self.deleteFromToRow)
        # JumpFisrtColumn.clicked.connect(self.jump_fisrt_column)

    # TODO Handle Table M2

    def renderTableColorM2(self):
        # / Create Widget table
        self.table_main_colorM2 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM2)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM2 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM2 = QTableWidget()
        self.table_scroll_leftM2 = QTableWidget()
        self.splitter_leftM2.addWidget(self.frozen_table_leftM2)
        self.splitter_leftM2.addWidget(self.table_scroll_leftM2)

        self.table_main_colorM2.addWidget(self.splitter_leftM2)

        # Create a vertical splitter
        self.splitter_rightM2 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM2 = QTableWidget()
        self.table_scroll_colorM2 = QTableWidget()
        self.splitter_rightM2.addWidget(self.frozen_table_colorM2)
        self.splitter_rightM2.addWidget(self.table_scroll_colorM2)

        self.table_main_colorM2.addWidget(self.splitter_rightM2)

        # / Config table
        self.frozen_table_colorM2.setRowCount(1)

        self.frozen_table_leftM2.setRowCount(1)

        self.frozen_table_leftM2.setColumnCount(1)
        self.table_scroll_leftM2.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM2()
        # / config header Row
        for i in range(self.frozen_table_leftM2.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM2.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM2()

        height_of_row = self.frozen_table_colorM2.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM2.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM2.setMaximumHeight(height_of_row)
        self.frozen_table_colorM2.setMinimumHeight(height_of_row)

        self.frozen_table_leftM2.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM2.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM2.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM2.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM2.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM2.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM2.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM2.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM2(vale):
            self.frozen_table_colorM2.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM2.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM2(vale):
            self.table_scroll_leftM2.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM2.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM2.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM2
        )
        self.frozen_table_colorM2.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM2
        )
        self.table_scroll_colorM2.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM2
        )
        self.table_scroll_leftM2.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM2
        )

        self.table_scroll_colorM2.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM2.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM2()

    def configheader_table_colorM2(self):
        for table in [
            self.frozen_table_colorM2,
            self.frozen_table_leftM2,
            self.table_scroll_colorM2,
            self.table_scroll_leftM2,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM2, self.frozen_table_leftM2]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM2:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M3

    def renderTableColorM3(self):
        # / Create Widget table
        self.table_main_colorM3 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM3)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM3 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM3 = QTableWidget()
        self.table_scroll_leftM3 = QTableWidget()
        self.splitter_leftM3.addWidget(self.frozen_table_leftM3)
        self.splitter_leftM3.addWidget(self.table_scroll_leftM3)

        self.table_main_colorM3.addWidget(self.splitter_leftM3)

        # Create a vertical splitter
        self.splitter_rightM3 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM3 = QTableWidget()
        self.table_scroll_colorM3 = QTableWidget()
        self.splitter_rightM3.addWidget(self.frozen_table_colorM3)
        self.splitter_rightM3.addWidget(self.table_scroll_colorM3)

        self.table_main_colorM3.addWidget(self.splitter_rightM3)

        # / Config table
        self.frozen_table_colorM3.setRowCount(1)

        self.frozen_table_leftM3.setRowCount(1)

        self.frozen_table_leftM3.setColumnCount(1)
        self.table_scroll_leftM3.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM3()
        # / config header Row
        for i in range(self.frozen_table_leftM3.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM3.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM3()

        height_of_row = self.frozen_table_colorM3.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM3.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM3.setMaximumHeight(height_of_row)
        self.frozen_table_colorM3.setMinimumHeight(height_of_row)

        self.frozen_table_leftM3.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM3.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM3.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM3.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM3.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM3.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM3.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM3.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM3(vale):
            self.frozen_table_colorM3.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM3.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM3(vale):
            self.table_scroll_leftM3.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM3.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM3.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM3
        )
        self.frozen_table_colorM3.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM3
        )
        self.table_scroll_colorM3.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM3
        )
        self.table_scroll_leftM3.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM3
        )

        self.table_scroll_colorM3.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM3.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM3()

    def configheader_table_colorM3(self):
        for table in [
            self.frozen_table_colorM3,
            self.frozen_table_leftM3,
            self.table_scroll_colorM3,
            self.table_scroll_leftM3,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM3, self.frozen_table_leftM3]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM3:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M6

    def renderTableColorM4(self):
        # / Create Widget table
        self.table_main_colorM4 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM4)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM4 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM4 = QTableWidget()
        self.table_scroll_leftM4 = QTableWidget()
        self.splitter_leftM4.addWidget(self.frozen_table_leftM4)
        self.splitter_leftM4.addWidget(self.table_scroll_leftM4)

        self.table_main_colorM4.addWidget(self.splitter_leftM4)

        # Create a vertical splitter
        self.splitter_rightM4 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM4 = QTableWidget()
        self.table_scroll_colorM4 = QTableWidget()
        self.splitter_rightM4.addWidget(self.frozen_table_colorM4)
        self.splitter_rightM4.addWidget(self.table_scroll_colorM4)

        self.table_main_colorM4.addWidget(self.splitter_rightM4)

        # / Config table
        self.frozen_table_colorM4.setRowCount(1)

        self.frozen_table_leftM4.setRowCount(1)

        self.frozen_table_leftM4.setColumnCount(1)
        self.table_scroll_leftM4.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM4()
        # / config header Row
        for i in range(self.frozen_table_leftM4.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM4.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM4()

        height_of_row = self.frozen_table_colorM4.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM4.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM4.setMaximumHeight(height_of_row)
        self.frozen_table_colorM4.setMinimumHeight(height_of_row)

        self.frozen_table_leftM4.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM4.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM4.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM4.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM4.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM4.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM4.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM4.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM4(vale):
            self.frozen_table_colorM4.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM4.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM4(vale):
            self.table_scroll_leftM4.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM4.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM4.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM4
        )
        self.frozen_table_colorM4.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM4
        )
        self.table_scroll_colorM4.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM4
        )
        self.table_scroll_leftM4.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM4
        )

        self.table_scroll_colorM4.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM4.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM4()

    def configheader_table_colorM4(self):
        for table in [
            self.frozen_table_colorM4,
            self.frozen_table_leftM4,
            self.table_scroll_colorM4,
            self.table_scroll_leftM4,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM4, self.frozen_table_leftM4]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM4:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M5

    def renderTableColorM5(self):
        # / Create Widget table
        self.table_main_colorM5 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM5)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM5 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM5 = QTableWidget()
        self.table_scroll_leftM5 = QTableWidget()
        self.splitter_leftM5.addWidget(self.frozen_table_leftM5)
        self.splitter_leftM5.addWidget(self.table_scroll_leftM5)

        self.table_main_colorM5.addWidget(self.splitter_leftM5)

        # Create a vertical splitter
        self.splitter_rightM5 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM5 = QTableWidget()
        self.table_scroll_colorM5 = QTableWidget()
        self.splitter_rightM5.addWidget(self.frozen_table_colorM5)
        self.splitter_rightM5.addWidget(self.table_scroll_colorM5)

        self.table_main_colorM5.addWidget(self.splitter_rightM5)

        # / Config table
        self.frozen_table_colorM5.setRowCount(1)

        self.frozen_table_leftM5.setRowCount(1)

        self.frozen_table_leftM5.setColumnCount(1)
        self.table_scroll_leftM5.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM5()
        # / config header Row
        for i in range(self.frozen_table_leftM5.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM5.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM5()

        height_of_row = self.frozen_table_colorM5.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM5.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM5.setMaximumHeight(height_of_row)
        self.frozen_table_colorM5.setMinimumHeight(height_of_row)

        self.frozen_table_leftM5.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM5.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM5.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM5.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM5.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM5.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM5.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM5.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM5(vale):
            self.frozen_table_colorM5.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM5.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM5(vale):
            self.table_scroll_leftM5.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM5.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM5.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM5
        )
        self.frozen_table_colorM5.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM5
        )
        self.table_scroll_colorM5.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM5
        )
        self.table_scroll_leftM5.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM5
        )

        self.table_scroll_colorM5.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM5.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM5()

    def configheader_table_colorM5(self):
        for table in [
            self.frozen_table_colorM5,
            self.frozen_table_leftM5,
            self.table_scroll_colorM5,
            self.table_scroll_leftM5,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM5, self.frozen_table_leftM5]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM5:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M6

    def renderTableColorM6(self):
        # / Create Widget table
        self.table_main_colorM6 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM6)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM6 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM6 = QTableWidget()
        self.table_scroll_leftM6 = QTableWidget()
        self.splitter_leftM6.addWidget(self.frozen_table_leftM6)
        self.splitter_leftM6.addWidget(self.table_scroll_leftM6)

        self.table_main_colorM6.addWidget(self.splitter_leftM6)

        # Create a vertical splitter
        self.splitter_rightM6 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM6 = QTableWidget()
        self.table_scroll_colorM6 = QTableWidget()
        self.splitter_rightM6.addWidget(self.frozen_table_colorM6)
        self.splitter_rightM6.addWidget(self.table_scroll_colorM6)

        self.table_main_colorM6.addWidget(self.splitter_rightM6)

        # / Config table
        self.frozen_table_colorM6.setRowCount(1)

        self.frozen_table_leftM6.setRowCount(1)

        self.frozen_table_leftM6.setColumnCount(1)
        self.table_scroll_leftM6.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM6()
        # / config header Row
        for i in range(self.frozen_table_leftM6.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM6.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM6()

        height_of_row = self.frozen_table_colorM6.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM6.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM6.setMaximumHeight(height_of_row)
        self.frozen_table_colorM6.setMinimumHeight(height_of_row)

        self.frozen_table_leftM6.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM6.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM6.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM6.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM6.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM6.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM6.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM6.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM6(vale):
            self.frozen_table_colorM6.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM6.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM6(vale):
            self.table_scroll_leftM6.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM6.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM6.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM6
        )
        self.frozen_table_colorM6.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM6
        )
        self.table_scroll_colorM6.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM6
        )
        self.table_scroll_leftM6.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM6
        )

        self.table_scroll_colorM6.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM6.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM6()

    def configheader_table_colorM6(self):
        for table in [
            self.frozen_table_colorM6,
            self.frozen_table_leftM6,
            self.table_scroll_colorM6,
            self.table_scroll_leftM6,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM6, self.frozen_table_leftM6]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM6:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M7

    def renderTableColorM7(self):
        # / Create Widget table
        self.table_main_colorM7 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM7)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM7 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM7 = QTableWidget()
        self.table_scroll_leftM7 = QTableWidget()
        self.splitter_leftM7.addWidget(self.frozen_table_leftM7)
        self.splitter_leftM7.addWidget(self.table_scroll_leftM7)

        self.table_main_colorM7.addWidget(self.splitter_leftM7)

        # Create a vertical splitter
        self.splitter_rightM7 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM7 = QTableWidget()
        self.table_scroll_colorM7 = QTableWidget()
        self.splitter_rightM7.addWidget(self.frozen_table_colorM7)
        self.splitter_rightM7.addWidget(self.table_scroll_colorM7)

        self.table_main_colorM7.addWidget(self.splitter_rightM7)

        # / Config table
        self.frozen_table_colorM7.setRowCount(1)

        self.frozen_table_leftM7.setRowCount(1)

        self.frozen_table_leftM7.setColumnCount(1)
        self.table_scroll_leftM7.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM7()
        # / config header Row
        for i in range(self.frozen_table_leftM7.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM7.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM7()

        height_of_row = self.frozen_table_colorM7.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM7.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM7.setMaximumHeight(height_of_row)
        self.frozen_table_colorM7.setMinimumHeight(height_of_row)

        self.frozen_table_leftM7.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM7.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM7.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM7.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM7.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM7.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM7.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM7.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM7(vale):
            self.frozen_table_colorM7.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM7.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM7(vale):
            self.table_scroll_leftM7.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM7.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM7.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM7
        )
        self.frozen_table_colorM7.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM7
        )
        self.table_scroll_colorM7.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM7
        )
        self.table_scroll_leftM7.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM7
        )

        self.table_scroll_colorM7.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM7.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM7()

    def configheader_table_colorM7(self):
        for table in [
            self.frozen_table_colorM7,
            self.frozen_table_leftM7,
            self.table_scroll_colorM7,
            self.table_scroll_leftM7,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM7, self.frozen_table_leftM7]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM7:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M8

    def renderTableColorM8(self):
        # / Create Widget table
        self.table_main_colorM8 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM8)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM8 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM8 = QTableWidget()
        self.table_scroll_leftM8 = QTableWidget()
        self.splitter_leftM8.addWidget(self.frozen_table_leftM8)
        self.splitter_leftM8.addWidget(self.table_scroll_leftM8)

        self.table_main_colorM8.addWidget(self.splitter_leftM8)

        # Create a vertical splitter
        self.splitter_rightM8 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM8 = QTableWidget()
        self.table_scroll_colorM8 = QTableWidget()
        self.splitter_rightM8.addWidget(self.frozen_table_colorM8)
        self.splitter_rightM8.addWidget(self.table_scroll_colorM8)

        self.table_main_colorM8.addWidget(self.splitter_rightM8)

        # / Config table
        self.frozen_table_colorM8.setRowCount(1)

        self.frozen_table_leftM8.setRowCount(1)

        self.frozen_table_leftM8.setColumnCount(1)
        self.table_scroll_leftM8.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM8()
        # / config header Row
        for i in range(self.frozen_table_leftM8.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM8.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM8()

        height_of_row = self.frozen_table_colorM8.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM8.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM8.setMaximumHeight(height_of_row)
        self.frozen_table_colorM8.setMinimumHeight(height_of_row)

        self.frozen_table_leftM8.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM8.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM8.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM8.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM8.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM8.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM8.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM8.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM8(vale):
            self.frozen_table_colorM8.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM8.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM8(vale):
            self.table_scroll_leftM8.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM8.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM8.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM8
        )
        self.frozen_table_colorM8.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM8
        )
        self.table_scroll_colorM8.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM8
        )
        self.table_scroll_leftM8.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM8
        )

        self.table_scroll_colorM8.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM8.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM8()

    def configheader_table_colorM8(self):
        for table in [
            self.frozen_table_colorM8,
            self.frozen_table_leftM8,
            self.table_scroll_colorM8,
            self.table_scroll_leftM8,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM8, self.frozen_table_leftM8]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM8:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M9

    def renderTableColorM9(self):
        # / Create Widget table
        self.table_main_colorM9 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM9)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM9 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM9 = QTableWidget()
        self.table_scroll_leftM9 = QTableWidget()
        self.splitter_leftM9.addWidget(self.frozen_table_leftM9)
        self.splitter_leftM9.addWidget(self.table_scroll_leftM9)

        self.table_main_colorM9.addWidget(self.splitter_leftM9)

        # Create a vertical splitter
        self.splitter_rightM9 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM9 = QTableWidget()
        self.table_scroll_colorM9 = QTableWidget()
        self.splitter_rightM9.addWidget(self.frozen_table_colorM9)
        self.splitter_rightM9.addWidget(self.table_scroll_colorM9)

        self.table_main_colorM9.addWidget(self.splitter_rightM9)

        # / Config table
        self.frozen_table_colorM9.setRowCount(1)

        self.frozen_table_leftM9.setRowCount(1)

        self.frozen_table_leftM9.setColumnCount(1)
        self.table_scroll_leftM9.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM9()
        # / config header Row
        for i in range(self.frozen_table_leftM9.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM9.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM9()

        height_of_row = self.frozen_table_colorM9.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM9.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM9.setMaximumHeight(height_of_row)
        self.frozen_table_colorM9.setMinimumHeight(height_of_row)

        self.frozen_table_leftM9.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM9.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM9.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM9.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM9.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM9.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM9.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM9.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM9(vale):
            self.frozen_table_colorM9.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM9.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM9(vale):
            self.table_scroll_leftM9.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM9.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM9.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM9
        )
        self.frozen_table_colorM9.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM9
        )
        self.table_scroll_colorM9.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM9
        )
        self.table_scroll_leftM9.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM9
        )

        self.table_scroll_colorM9.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM9.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM9()

    def configheader_table_colorM9(self):
        for table in [
            self.frozen_table_colorM9,
            self.frozen_table_leftM9,
            self.table_scroll_colorM9,
            self.table_scroll_leftM9,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM9, self.frozen_table_leftM9]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM9:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handle Table M10

    def renderTableColorM10(self):
        # / Create Widget table
        self.table_main_colorM10 = QSplitter(Qt.Horizontal)
        self.widget_main.addWidget(self.table_main_colorM10)

        # / Table Create
        # Create a vertical splitter
        self.splitter_leftM10 = QSplitter(Qt.Vertical)
        self.frozen_table_leftM10 = QTableWidget()
        self.table_scroll_leftM10 = QTableWidget()
        self.splitter_leftM10.addWidget(self.frozen_table_leftM10)
        self.splitter_leftM10.addWidget(self.table_scroll_leftM10)

        self.table_main_colorM10.addWidget(self.splitter_leftM10)

        # Create a vertical splitter
        self.splitter_rightM10 = QSplitter(Qt.Vertical)
        self.frozen_table_colorM10 = QTableWidget()
        self.table_scroll_colorM10 = QTableWidget()
        self.splitter_rightM10.addWidget(self.frozen_table_colorM10)
        self.splitter_rightM10.addWidget(self.table_scroll_colorM10)

        self.table_main_colorM10.addWidget(self.splitter_rightM10)

        # / Config table
        self.frozen_table_colorM10.setRowCount(1)

        self.frozen_table_leftM10.setRowCount(1)

        self.frozen_table_leftM10.setColumnCount(1)
        self.table_scroll_leftM10.setColumnCount(1)

        # / Config Header col
        self.updateHeaderColorM10()
        # / config header Row
        for i in range(self.frozen_table_leftM10.rowCount()):
            item = QTableWidgetItem(f"Ngày")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_leftM10.setItem(i, 0, item)

        # / Config Header
        self.configheader_table_colorM10()

        height_of_row = self.frozen_table_colorM10.verticalHeader().sectionSize(0)
        width_of_row = self.frozen_table_colorM10.horizontalHeader().sectionSize(0)
        self.frozen_table_colorM10.setMaximumHeight(height_of_row)
        self.frozen_table_colorM10.setMinimumHeight(height_of_row)

        self.frozen_table_leftM10.setMaximumSize(width_of_row + 90, height_of_row)
        self.frozen_table_leftM10.setMinimumSize(width_of_row + 90, height_of_row)

        self.frozen_table_leftM10.horizontalHeader().setStretchLastSection(True)
        self.table_scroll_leftM10.horizontalHeader().setStretchLastSection(True)

        self.frozen_table_colorM10.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table_leftM10.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # self.table_scroll_color.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        # )
        self.table_scroll_leftM10.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.table_scroll_leftM10.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        def sync_horizontal_scrollM10(vale):
            self.frozen_table_colorM10.horizontalScrollBar().setValue(vale)
            self.table_scroll_colorM10.horizontalScrollBar().setValue(vale)

        def sync_vertical_scrollM10(vale):
            self.table_scroll_leftM10.verticalScrollBar().setValue(vale)
            self.table_scroll_colorM10.verticalScrollBar().setValue(vale)

        self.table_scroll_colorM10.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM10
        )
        self.frozen_table_colorM10.horizontalScrollBar().valueChanged.connect(
            sync_horizontal_scrollM10
        )
        self.table_scroll_colorM10.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM10
        )
        self.table_scroll_leftM10.verticalScrollBar().valueChanged.connect(
            sync_vertical_scrollM10
        )

        self.table_scroll_colorM10.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_scroll_colorM10.customContextMenuRequested.connect(
            self.jumpTableWithRow
        )

        self.updateTableColorM10()

    def configheader_table_colorM10(self):
        for table in [
            self.frozen_table_colorM10,
            self.frozen_table_leftM10,
            self.table_scroll_colorM10,
            self.table_scroll_leftM10,
        ]:

            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            # / Font
            table.setFont(self.font)
            table.verticalHeader().setFont(self.font)
            table.horizontalHeader().setFont(self.font)
            table.setStyleSheet(
                """
                QTableView {
                    gridline-color: black;
                }
            """
            )
            # / Header
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            if table not in [self.frozen_table_colorM10, self.frozen_table_leftM10]:
                table.verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
            else:
                if table == self.frozen_table_colorM10:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.ResizeToContents
                    )
                else:
                    table.verticalHeader().setSectionResizeMode(
                        QHeaderView.ResizeMode.Stretch
                    )

    # TODO Handler Button

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.noticeView = []
        self.jumpAction = {}

    def addNoticeView(self, button, label, itemColor):
        self.noticeView.append(
            {
                "isView": False,
                "label": label,
                "localItem": {
                    "row": itemColor["row"],
                    "col": itemColor["col"],
                },
                "button": button,
                "notice": itemColor["notice"],
                "thong": itemColor["thong"],
                "col_d": itemColor["col_d"],
                "color_value": itemColor["color_value"],
            }
        )

    def handleButtonClick(self, label):
        matching_item = next(
            (item for item in self.noticeView if label == item["label"])
        )
        current_widget = self.widget_main.currentWidget()
        if matching_item:
            self.table_scroll_count.clearSelection()
            for i in range(10):
                data = self.ban_info["meta"]["tables"][i]
                if data["enable"]:
                    self.start_clear_tables_row(i)
            # / Get Value from Item
            localItem = matching_item["localItem"]
            row = localItem["row"]
            col = localItem["col"]
            button = matching_item["button"]
            notice = matching_item["notice"]

            if "_m10" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 10", "Bảng Màu 10")
                if current_widget != self.table_main_colorM10:
                    self.widget_main.setCurrentWidget(self.table_main_colorM10)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM10.item(row, col)
                self.table_scroll_colorM10.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m1" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 1", "Bảng Màu 1")
                if current_widget != self.table_main_color:
                    self.widget_main.setCurrentWidget(self.table_main_color)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_color.item(row, col)
                self.table_scroll_color.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m2" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 2", "Bảng Màu 2")
                if current_widget != self.table_main_colorM2:
                    self.widget_main.setCurrentWidget(self.table_main_colorM2)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM2.item(row, col)
                self.table_scroll_colorM2.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m3" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 3", "Bảng Màu 3")
                if current_widget != self.table_main_colorM3:
                    self.widget_main.setCurrentWidget(self.table_main_colorM3)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM3.item(row, col)
                self.table_scroll_colorM3.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m4" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 4", "Bảng Màu 4")
                if current_widget != self.table_main_colorM4:
                    self.widget_main.setCurrentWidget(self.table_main_colorM4)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM4.item(row, col)
                self.table_scroll_colorM4.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m5" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 5", "Bảng Màu 5")
                if current_widget != self.table_main_colorM5:
                    self.widget_main.setCurrentWidget(self.table_main_colorM5)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM5.item(row, col)
                self.table_scroll_colorM5.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m6" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 6", "Bảng Màu 6")
                if current_widget != self.table_main_colorM6:
                    self.widget_main.setCurrentWidget(self.table_main_colorM6)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM6.item(row, col)
                self.table_scroll_colorM6.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m7" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 7", "Bảng Màu 7")
                if current_widget != self.table_main_colorM7:
                    self.widget_main.setCurrentWidget(self.table_main_colorM7)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM7.item(row, col)
                self.table_scroll_colorM7.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m8" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 8", "Bảng Màu 8")
                if current_widget != self.table_main_colorM8:
                    self.widget_main.setCurrentWidget(self.table_main_colorM8)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM8.item(row, col)
                self.table_scroll_colorM8.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            if "_m9" in matching_item["label"]:
                self.changeStatusBar("Bảng Màu 9", "Bảng Màu 9")
                if current_widget != self.table_main_colorM9:
                    self.widget_main.setCurrentWidget(self.table_main_colorM9)
                button.setStyleSheet(css_button_view)
                item_target = self.table_scroll_colorM9.item(row, col)
                self.table_scroll_colorM9.scrollToItem(
                    item_target, hint=QTableWidget.ScrollHint.PositionAtCenter
                )
                new_data = {
                    "current": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                    "next": {
                        "item": item_target,
                        "color": (notice if notice is not None else self.normal),
                    },
                }
                self.setHighlight(new_data)
                return

            return

    def signal_scrollbar(self, value):
        self.scroll_area.horizontalScrollBar().setValue(value)
        self.scroll_area_second.horizontalScrollBar().setValue(value)

    def jump_fisrt_column(self):
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        row_aline = len(filter_data)
        current_widget = self.TableChange.text()
        if current_widget == "Bảng Màu":
            item = self.table_scroll_count.item(row_aline - 1, 0)
            self.table_scroll_count.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
        else:
            item = self.table_scroll_color.item(row_aline - 1, 0)
            self.table_scroll_color.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )

    def insertData(self):
        # / Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog()
        dialog.setWindowTitle("Bảng Nhập Liệu")
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1300, 850)
        dialog.show()

        # / Create Layout
        insert_w = QWidget()
        insert_l = QVBoxLayout(insert_w)
        insert_l.setSpacing(0)
        insert_l.setContentsMargins(0, 0, 0, 0)
        dialog.setLayout(insert_l)

        title_label = QLabel("Bảng Nhập Liệu")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(css_title)
        insert_l.addWidget(title_label)

        layout_w = QWidget()
        layout = QGridLayout(layout_w)
        layout.setSpacing(0)
        insert_l.addWidget(layout_w)

        # / Table Insert
        insert_thong_table = QTableWidget()
        insert_thong_table.setFixedWidth(750)
        insert_thong_table.setFixedHeight(780)
        insert_thong_table.setStyleSheet(css_table_header)
        layout.addWidget(insert_thong_table, 0, 0, Qt.AlignmentFlag.AlignLeft)
        # / Config Table
        insert_thong_table.setColumnCount(8)
        insert_thong_table.setRowCount(15)

        insert_thong_table.horizontalHeader().hide()
        insert_thong_table.verticalHeader().hide()

        insert_thong_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectItems
        )
        insert_thong_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        insert_thong_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        insert_thong_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        insert_thong_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        insert_thong_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        insert_thong_table.setFont(self.font)
        insert_thong_table.horizontalHeader().setFont(self.font)
        insert_thong_table.verticalHeader().setFont(self.font)

        # / Render Row Table
        for i in range(15):
            for j in range(8):
                value = i + j * 15
                value = value if value > 9 else f"0{value}"
                item = QTableWidgetItem(f"{value}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                insert_thong_table.setItem(i, j, item)

        # / Insert From
        insert_from_w = QWidget()
        # insert_from_w.setMinimumWidth(530)
        insert_from_l = QGridLayout(insert_from_w)
        insert_from_l.setSpacing(20)
        layout.addWidget(insert_from_w, 0, 1, Qt.AlignmentFlag.AlignTop)

        # / Insert Day
        insert_day_label = QLabel("Ngày Tháng")
        insert_day_label.setStyleSheet(css_lable)

        insert_day_edit = QDateEdit()
        font = QFont()
        font.setPointSize(20)
        insert_day_edit.setFont(font)
        insert_day_edit.setWrapping(False)
        insert_day_edit.setCalendarPopup(True)

        insert_from_l.addWidget(insert_day_label, 1, 0)
        insert_from_l.addWidget(insert_day_edit, 1, 1)

        # / Insert Ngang
        insert_ngang_label = QLabel("Dòng Hàng Ngang")
        insert_ngang_label.setStyleSheet(css_lable)

        insert_ngang_grid_w = QWidget()
        insert_ngang_gird = QGridLayout(insert_ngang_grid_w)

        insert_ngang_edit = QSpinBox()
        insert_ngang_edit.setMinimum(1)
        insert_ngang_edit.setMaximum(31)
        insert_ngang_edit.setStyleSheet(css_input)

        insert_ngang_edit_first = QLabel("")
        insert_ngang_edit_first.setAlignment(Qt.AlignmentFlag.AlignCenter)
        insert_ngang_edit_first.setStyleSheet(css_customs_table)

        insert_ngang_gird.addWidget(insert_ngang_edit, 0, 0)
        insert_ngang_gird.addWidget(insert_ngang_edit_first, 0, 1)

        insert_from_l.addWidget(insert_ngang_label, 2, 0)
        insert_from_l.addWidget(insert_ngang_grid_w, 2, 1)

        # / Insert Thong
        insert_thong_label = QLabel("Dòng Thông số")
        insert_thong_label.setStyleSheet(css_lable)

        insert_thong_grid_w = QWidget()
        insert_thong_gird = QGridLayout(insert_thong_grid_w)

        insert_thong_edit = QSpinBox()
        insert_thong_edit.setMinimum(-1)
        insert_thong_edit.setMaximum(120)
        insert_thong_edit.setStyleSheet(css_input)

        insert_thong_edit_first = QLabel("")
        insert_thong_edit_first.setAlignment(Qt.AlignmentFlag.AlignCenter)
        insert_thong_edit_first.setStyleSheet(css_customs_table)

        insert_thong_gird.addWidget(insert_thong_edit, 0, 0)
        insert_thong_gird.addWidget(insert_thong_edit_first, 0, 1)

        insert_from_l.addWidget(insert_thong_label, 3, 0)
        insert_from_l.addWidget(insert_thong_grid_w, 3, 1)

        # / Features insert
        virable_one_edit = QCheckBox("Kích Hoạt N:2")
        virable_one_edit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        virable_one_edit.setStyleSheet(css_button_checkbox)

        virable_two_edit = QCheckBox("CĐ 1 DNgang")
        virable_two_edit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        virable_two_edit.setStyleSheet(css_button_checkbox)

        insert_from_l.addWidget(virable_one_edit, 4, 0, Qt.AlignmentFlag.AlignCenter)
        insert_from_l.addWidget(virable_two_edit, 4, 1, Qt.AlignmentFlag.AlignCenter)

        # / Button Insert
        submit = QPushButton("Soát Rồi OK Toán")
        submit.setCursor(QCursor(Qt.PointingHandCursor))
        submit.setStyleSheet(css_button_submit)

        exit = QPushButton("Thoát")
        exit.setCursor(QCursor(Qt.PointingHandCursor))
        exit.setStyleSheet(css_button_cancel)
        # exit.setFixedWidth(60)

        label_submit = QLabel()
        label_exit = QLabel()
        # label_exit.setFixedHeight(220)

        insert_from_l.addWidget(label_submit, 6, 1)
        insert_from_l.addWidget(submit, 7, 1)
        insert_from_l.addWidget(label_exit, 8, 1)
        insert_from_l.addWidget(exit, 9, 0)

        # / Config Data
        old_data = self.ban_info["data"][-1] if len(self.ban_info["data"]) > 0 else None
        data = {}
        data["insert"] = {}
        data["update"] = self.ban_info["meta"]["features"]

        # / Config Data
        # old_data = self.ban_info["data"][-1] if len(self.ban_info["data"]) > 0 else None
        # data = {}
        # data["insert"] = {}
        # data["update"] = self.ban_info["meta"]["features"]

        # TODO Handler Button exit
        def exit_click():
            dialog.reject()

        def changeDate(value):
            date = QDate(value)
            data["insert"]["date"] = date.toString("dd/MM/yyyy")
            if not data["update"]["N=1"]["status"]:
                day = date.day()
                insert_ngang_edit.setValue(day)

        def changeNgang(value):
            data["insert"]["ngang"] = value - 1
            number_value = self.number_info[value - 1]
            insert_ngang_edit_first.setText(f"{number_value[0]}")

        def changeThongTable(value):
            item = value.text()
            changeThongEdit(int(item))
            insert_thong_edit.setValue(int(item))

        def changeThongEdit(value):
            insert_thong_table.clearSelection()
            data["insert"]["thong"] = value
            if value == -1:
                insert_thong_edit_first.setText(f"")
                return
            thong_value = self.thong_info[0][value]
            insert_thong_edit_first.setText(f"{thong_value}")

            col = value // 15  # Calculate column index
            row = value % 15  # Calculate row index
            item = insert_thong_table.item(row, col)
            if item:
                item.setSelected(True)

        def changeVirableOne(value):
            data["update"]["N:2"] = value
            insert_thong_edit.setDisabled(value)
            insert_thong_table.setDisabled(value)
            if value:
                insert_thong_edit.setValue(-1)
                insert_thong_edit_first.setText("")
                title_label.setText("Bảng Nhập Liệu - Nhập Rời")
            else:
                title_label.setText("Bảng Nhập Liệu - Nhập Liền")

        def changeVirableTwo(value):
            data["update"]["N=1"] = {
                "status": value,
                "value": insert_ngang_edit.value() - 1 if value else 0,
            }
            insert_ngang_edit.setDisabled(value)

        # / Thong
        insert_thong_table.itemClicked.connect(changeThongTable)
        insert_thong_edit.valueChanged.connect(changeThongEdit)

        # / Date
        insert_day_edit.dateChanged.connect(changeDate)

        # / Ngang
        insert_ngang_edit.valueChanged.connect(changeNgang)

        # / Features
        virable_one_edit.clicked.connect(changeVirableOne)
        virable_two_edit.clicked.connect(changeVirableTwo)

        # TODO Set Default for insert
        if old_data:
            date_old = old_data["date"].split("/")
            date_old = [int(item) for item in date_old]
            date_def = QDate(date_old[2], date_old[1], date_old[0]).addDays(1)

            insert_day_edit.setDate(date_def)
            data["insert"]["date"] = date_def.toString("dd/MM/yyyy")

            value = date_def.day()
            data["insert"]["ngang"] = value - 1
            insert_ngang_edit.setValue(value)

            thong_value = old_data["thong"]
            if thong_value != -1:
                changeThongEdit(thong_value)
                insert_thong_edit.setValue(thong_value)

        else:
            date_def = QDate().currentDate()
            insert_day_edit.setDate(date_def)
            data["insert"]["date"] = date_def.toString("dd/MM/yyyy")

            value = date_def.day()
            insert_ngang_edit.setValue(value)
            number_value = self.number_info[value - 1][:2]
            insert_ngang_edit_first.setText(f"{number_value[0]}")
            data["insert"]["ngang"] = value - 1

        if data["update"]["N:2"]:
            insert_thong_edit.setValue(-1)
            insert_thong_edit.setDisabled(True)
            insert_thong_table.setDisabled(True)
            title_label.setText("Bảng Nhập Liệu - Nhập Rời")
        else:
            title_label.setText("Bảng Nhập Liệu - Nhập Liền")

        if data["update"]["N=1"]["status"]:
            value = data["update"]["N=1"]["value"]
            insert_ngang_edit.setValue(value + 1)
            insert_ngang_edit.setDisabled(True)
            number_value = self.number_info[value][:2]
            insert_ngang_edit_first.setText(f"{number_value[0]}")
            data["insert"]["ngang"] = value

        virable_one_edit.setChecked(data["update"]["N:2"])
        virable_two_edit.setChecked(data["update"]["N=1"]["status"])
        data["insert"]["thong"] = insert_thong_edit.value()

        exit.clicked.connect(exit_click)
        submit.clicked.connect(lambda: self.submit_insert(data, dialog))
        # Move and set the dialog size
        self.move_to_right(dialog)

    def submit_insert(self, data, dialog):
        data["id"] = self.ban_info["id"]
        msg = updateBanInsert(data)
        if msg["status"]:
            dialog.reject()
            if self.widget_main.currentWidget() != self.table_main_count:
                self.widget_main.setCurrentWidget(self.table_main_count)
            self.ban_info = msg["data"]
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.reload_widget])
            )
            self.thread.start()
            if data["insert"]["thong"] != -1:
                # self.questionInsertDate()
                self.thread.task_completed.connect(lambda: self.questionInsertDate())
        return

    def insertThong(self):
        # / Config Data
        old_data = self.ban_info["data"][-1] if len(self.ban_info["data"]) > 0 else None
        # / Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog()
        dialog.setWindowTitle("Bảng Nhập Thông")
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1200, 850)
        dialog.show()

        # / Create Layout
        insert_w = QWidget()
        insert_l = QVBoxLayout(insert_w)
        insert_l.setSpacing(0)
        insert_l.setContentsMargins(0, 0, 0, 0)
        dialog.setLayout(insert_l)

        title_label = QLabel("Bảng Nhập Thông - Nhập Rời")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(css_lable)
        insert_l.addWidget(title_label)

        layout_w = QWidget()
        layout = QGridLayout(layout_w)
        layout.setSpacing(0)
        insert_l.addWidget(layout_w)

        # / Table Insert
        insert_thong_table = QTableWidget()
        insert_thong_table.setFixedWidth(750)
        insert_thong_table.setFixedHeight(780)
        insert_thong_table.setStyleSheet(css_table_header)
        layout.addWidget(insert_thong_table, 0, 0, Qt.AlignmentFlag.AlignLeft)
        # / Config Table
        insert_thong_table.setColumnCount(8)
        insert_thong_table.setRowCount(15)

        insert_thong_table.horizontalHeader().hide()
        insert_thong_table.verticalHeader().hide()

        insert_thong_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectItems
        )
        insert_thong_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        insert_thong_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        insert_thong_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        insert_thong_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        insert_thong_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        insert_thong_table.setFont(self.font)
        insert_thong_table.horizontalHeader().setFont(self.font)
        insert_thong_table.verticalHeader().setFont(self.font)

        # / Render Row Table
        for i in range(15):
            for j in range(8):
                value = i + j * 15
                value = value if value > 9 else f"0{value}"
                item = QTableWidgetItem(f"{value}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                insert_thong_table.setItem(i, j, item)

        # / Insert From
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

        # / Title Thong
        insert_thong_title = QLabel("Mời Nhập Thông Số")
        insert_thong_title.setStyleSheet(css_title)
        insert_from_l.addWidget(insert_thong_title, 2, 0)

        # / Insert Thong
        insert_thong_label = QLabel("Dòng Thông")
        insert_thong_label.setStyleSheet(css_lable)
        # insert_thong_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        insert_thong_grid_w = QWidget()
        insert_thong_gird = QGridLayout(insert_thong_grid_w)

        insert_thong_edit = QSpinBox()
        insert_thong_edit.setMinimum(-1)
        insert_thong_edit.setMaximum(120)
        insert_thong_edit.setStyleSheet(css_input)

        insert_thong_edit_first = QLabel("")
        # insert_thong_edit_first.setAlignment(Qt.AlignmentFlag.AlignCenter)
        insert_thong_edit_first.setStyleSheet(css_customs_table)

        insert_thong_gird.addWidget(insert_thong_edit, 0, 0)
        insert_thong_gird.addWidget(insert_thong_edit_first, 0, 1)

        insert_from_l.addWidget(insert_thong_label, 3, 0)
        insert_from_l.addWidget(insert_thong_grid_w, 3, 1)

        # / Button Insert
        submit = QPushButton("OK Toán")
        submit.setCursor(QCursor(Qt.PointingHandCursor))
        submit.setStyleSheet(css_button_submit)
        submit.setFixedWidth(300)
        submit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        insert_from_l_2.addWidget(submit)

        # / Button Exit
        exit = QPushButton("Thoát")
        exit.setCursor(QCursor(Qt.PointingHandCursor))
        exit.setStyleSheet(css_button_cancel)
        exit.setFixedWidth(150)
        exit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        insert_from_l_2.addWidget(exit)

        # TODO Set Default for insert
        # TODO Handler Button exit
        def exit_click():
            dialog.reject()

        def changeThongTable(value):
            item = value.text()
            changeThongEdit(int(item))
            insert_thong_edit.setValue(int(item))

        def changeThongEdit(value):
            insert_thong_table.clearSelection()
            old_data["thong"] = value
            if value == -1:
                insert_thong_edit_first.setText("")
                return
            thong_value = self.thong_info[0][value]
            insert_thong_edit_first.setText(f"{thong_value}")

            col = value // 15  # Calculate column index
            row = value % 15  # Calculate row index
            item = insert_thong_table.item(row, col)
            if item:
                item.setSelected(True)

        if old_data:
            thong_value = old_data["thong"]
            changeThongEdit(thong_value)
            insert_thong_edit.setValue(thong_value)

        def submit_click():
            self.update_thong_insert(old_data, dialog)
            return

        # def cancel_clicked():
        #     dialog.reject()
        #     self.insertData()

        # cancel.clicked.connect(cancel_clicked)
        exit.clicked.connect(exit_click)
        submit.clicked.connect(submit_click)
        # / Thong
        insert_thong_table.itemClicked.connect(changeThongTable)
        insert_thong_edit.valueChanged.connect(changeThongEdit)

        self.move_to_right(dialog)

    def update_thong_insert(self, data, dialog):
        data_send = {}
        data_send["thong"] = data
        msg = updateThongInsert(data_send)
        if msg["status"]:
            dialog.reject()
            if self.widget_main.currentWidget() != self.table_main_count:
                self.widget_main.setCurrentWidget(self.table_main_count)
            self.ban_info = msg["data"]
            # self.reload_widget()
            # sleep(0.5)
            # self.questionInsertDate()
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.reload_widget, self.questionInsertDate])
            )
            self.thread.start()
        return

    def questionInsertDate(self):
        # / Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        message = QMessageBox()
        message.setWindowTitle("Thông Báo")
        message.setWindowIcon(QIcon(icon))
        message.setText("Nhập liệu dòng mới")
        message.setIcon(QMessageBox.Icon.Question)
        ok_button = message.addButton(QMessageBox.StandardButton.Yes)
        ok_button.setText("OK")
        no_button = message.addButton(QMessageBox.StandardButton.No)
        no_button.setText("Thoát")
        # message.setDefaultButton(ok_button)
        message.setFont(self.font)
        result = message.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.insertData()

    def changeSettingColor(self):
        SettingTable(self.ban_info)

    def setHighlight(self, data):
        # / Handler prev item
        if "prev" in self.jumpAction:
            item_prev = self.jumpAction["prev"]["item"]
            item_prev_color = self.jumpAction["prev"]["color"]
            item_prev.setBackground(item_prev_color)

        current = data["current"]
        i_next = data["next"]
        i_next["item"].setBackground(self.cyan)
        self.jumpAction = {
            "prev": {"item": current["item"], "color": current["color"]},
            "next": {"item": i_next["item"], "color": i_next["color"]},
        }

    def reload_color_item(self):
        if "prev" in self.jumpAction:
            item = self.jumpAction["prev"]["item"]
            color = self.jumpAction["prev"]["color"]
            item.setBackground(color)
            # / Swap prev to next
            if "next" in self.jumpAction:
                prev_item = self.jumpAction["next"]
                del self.jumpAction["next"]
                self.jumpAction["prev"] = prev_item

    def setHighlight_Thong(self, data):
        self.table_main_thong.clearSelection()
        col = data["col"]
        value = data["value"]
        isCol_a = data["isCol_a"]
        thong_info = self.ban_info["thong"]
        name_thong = thong_info["name"]
        type_count = 1 if "1." in name_thong else 2 if "2." in name_thong else 0
        thong_data = self.thong_info
        value_thong = thong_info["value"]
        thong_index_thong = value_thong[0] - 1 + int(col) - 5
        thong_index_row = []
        for i in range(121):
            v = thong_data[thong_index_thong][i]
            if type_count == 1:
                if str(v) == str(value):
                    thong_index_row.append(i)
            else:
                if type_count == 2:
                    if isCol_a:
                        isEqual = self.checkColorThong(str(value), str(v))
                        if isEqual:
                            thong_index_row.append(i)
                    else:
                        if v == value:
                            thong_index_row.append(i)

                else:
                    isEqual = self.checkColorThong(str(value), str(v))
                    if isEqual:
                        thong_index_row.append(i)

        self.table_main_thong.selectColumn(int(col))

        for i in thong_index_row:
            self.table_main_thong.selectRow(i)

    def deleteNewRow(self):
        # / Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        message = QMessageBox()
        message.setWindowTitle("Thông Báo")
        message.setWindowIcon(QIcon(icon))
        message.setText("Bạn có muốn xóa dòng mới nhất không?")
        message.setIcon(QMessageBox.Icon.Question)
        message.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        message.setDefaultButton(QMessageBox.StandardButton.No)
        message.setFont(self.font)
        result = message.exec()

        if result == QMessageBox.StandardButton.Yes:
            # / delete last data
            self.ban_info["data"] = self.ban_info["data"][:-1]
            msg = deleteRowBan(
                {"update": self.ban_info["data"], "id": self.ban_info["id"]}
            )
            # / Set table count is main
            self.widget_main.setCurrentWidget(self.table_main_count)
            # / re-render all tables

            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.reload_widget])
            )
            self.thread.task_completed.connect(lambda: SendMessage(msg))
            self.thread.start()
            # / Send Notice Message

    def deleteFromToRow(self):
        # / Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle("Cài đặt bảng")
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1000, 400)
        dialog.show()

        # / Default Date
        date = QDate().currentDate()
        date_from = date.addDays(-7)

        # / Create Layout
        layout = QGridLayout()
        layout.setSpacing(50)
        dialog.setLayout(layout)

        # / Setting Color Table Count
        delete_from_w = QWidget()
        delete_from_l = QGridLayout(delete_from_w)

        delete_from_label = QLabel("Ngày Bắt Đầu")
        delete_from_label.setStyleSheet(css_lable)

        delete_from_edit = QDateEdit()
        font = QFont()
        font.setPointSize(20)
        delete_from_edit.setFont(font)
        delete_from_edit.setWrapping(False)
        delete_from_edit.setCalendarPopup(True)
        delete_from_edit.setDate(date_from)

        delete_from_l.addWidget(delete_from_edit, 0, 0)

        layout.addWidget(delete_from_label, 0, 0)
        layout.addWidget(delete_from_w, 1, 0)

        # / Setting Color Table Color
        delete_to_w = QWidget()
        delete_to_l = QGridLayout(delete_to_w)

        delete_to_label = QLabel("Ngày Kết Thúc")
        delete_to_label.setStyleSheet(css_lable)

        delete_to_edit = QDateEdit()
        delete_to_edit.setFont(font)
        delete_to_edit.setWrapping(False)
        delete_to_edit.setCalendarPopup(True)
        delete_to_edit.setDate(date)

        delete_to_l.addWidget(delete_to_edit, 0, 0)

        layout.addWidget(delete_to_label, 0, 1)
        layout.addWidget(delete_to_w, 1, 1)

        # delete_all_w = QWidget()
        # delete_all_l = QGridLayout(delete_all_w)

        delete_all_day = QCheckBox("Xóa Tất Cả")
        delete_all_day.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        delete_all_day.setStyleSheet(css_button_checkbox)

        layout.addWidget(delete_all_day, 2, 0)

        # / Button Save And Exit
        submit_w = QWidget()
        submit_l = QVBoxLayout(submit_w)
        submit = QPushButton("Xóa")
        submit.setStyleSheet(css_button_submit)
        submit_l.addWidget(submit)

        exit_w = QWidget()
        exit_l = QVBoxLayout(exit_w)
        exit = QPushButton("Thoát")
        exit.setStyleSheet(css_button_cancel)
        exit_l.addWidget(exit)

        layout.addWidget(submit_w, 3, 0)
        layout.addWidget(exit_w, 3, 1)

        def exit_click():
            dialog.reject()

        def submit_click():
            fromdate = delete_from_edit.date().toString("dd/MM/yyyy")
            todate = delete_to_edit.date().toString("dd/MM/yyyy")
            isDeleteAll = delete_all_day.isChecked()
            msg = deleteFromToBan(fromdate, todate, self.ban_info["id"], isDeleteAll)
            if msg["status"]:
                dialog.reject()
                self.ban_info = msg["data"]
                self.widget_main.setCurrentWidget(self.table_main_count)

                self.show_loading_screen()
                self.thread = Thread()
                self.thread.task_completed.connect(
                    lambda: self.updateWidget([self.reload_widget])
                )
                self.thread.task_completed.connect(lambda: SendMessage(msg["msg"]))
                self.thread.start()

        exit.clicked.connect(exit_click)
        submit.clicked.connect(submit_click)

    def jumpTableWithRow(self, pos):
        self.table_scroll_count.clearSelection()
        for i in range(10):
            data = self.ban_info["meta"]["tables"][i]
            if data["enable"]:
                self.start_clear_tables_row(i)
        current_widget = self.widget_main.currentWidget()
        color_widgetM2 = self.table_main_colorM2
        color_widgetM3 = self.table_main_colorM3
        color_widgetM4 = self.table_main_colorM4
        color_widgetM5 = self.table_main_colorM5
        color_widgetM6 = self.table_main_colorM6
        color_widgetM7 = self.table_main_colorM7
        color_widgetM8 = self.table_main_colorM8
        color_widgetM9 = self.table_main_colorM9
        color_widgetM10 = self.table_main_colorM10
        color_widget = self.table_main_color
        count_widget = self.table_main_count

        if current_widget == count_widget:
            item_count = self.table_scroll_count.itemAt(pos)
            item_count_data = item_count.data(Qt.ItemDataRole.UserRole)
            if item_count_data:
                menu = QMenu()
                moveTable = QAction("VBM1")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_count_data, "vbm1")
                )

                if item_count_data["actionM2"] is not None:
                    moveTable2 = QAction("VBM2")
                    moveTable2.setFont(self.font_action)
                    moveTable2.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm2")
                    )
                    menu.addAction(moveTable2)

                if item_count_data["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_count_data["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_count_data["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_count_data["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_count_data["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_count_data["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_count_data["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_count_data["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_count_data, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_count_data, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_count.mapToGlobal(pos))
                return

        if current_widget == color_widget:
            item_color = self.table_scroll_color.itemAt(pos)
            item_color_data = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_data:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_data, "vbt")
                )

                if item_color_data["actionM2"] is not None:
                    moveTable2 = QAction("VBM2")
                    moveTable2.setFont(self.font_action)
                    moveTable2.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm2")
                    )
                    menu.addAction(moveTable2)

                if item_color_data["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_data["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_data["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_data["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_data["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_data["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_data["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_color_data["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_data, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_data, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_color.mapToGlobal(pos))
                return

        if current_widget == color_widgetM2:
            item_color = self.table_scroll_colorM2.itemAt(pos)
            item_color_dataM2 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM2:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM2, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM2, "vbm1")
                )

                if item_color_dataM2["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_dataM2["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM2["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM2["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM2["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM2["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM2["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_color_dataM2["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM2, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM2, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_color.mapToGlobal(pos))
                return

        if current_widget == color_widgetM3:
            item_color = self.table_scroll_colorM3.itemAt(pos)
            item_color_dataM3 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM3:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM3, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM3, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM3, "vbm2")
                )

                if item_color_dataM3["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM3, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM3["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM3, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM3["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM3, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM3["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM3, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM3["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM3, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM3["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM3, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_color_dataM3["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM3, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM3, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM3.mapToGlobal(pos))
                return

        if current_widget == color_widgetM4:
            item_color = self.table_scroll_colorM4.itemAt(pos)
            item_color_dataM4 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM4:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM4, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM4, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM4, "vbm2")
                )

                if item_color_dataM4["actionM3"] is not None:
                    moveTable4 = QAction("VBM3")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM4, "vbm3")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM4["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM4, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM4["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM4, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM4["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM4, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM4["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM4, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM4["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM4, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_color_dataM4["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM4, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM4, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM4.mapToGlobal(pos))
                return

        if current_widget == color_widgetM5:
            item_color = self.table_scroll_colorM5.itemAt(pos)
            item_color_dataM5 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM5:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM5, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM5, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM5, "vbm2")
                )

                if item_color_dataM5["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM5, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_dataM5["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM5, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM5["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM5, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM5["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM5, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM5["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM5, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM5["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM5, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_color_dataM5["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM5, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM5, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM5.mapToGlobal(pos))
                return

        if current_widget == color_widgetM6:
            item_color = self.table_scroll_colorM6.itemAt(pos)
            item_color_dataM6 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM6:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM6, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM6, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM6, "vbm2")
                )

                if item_color_dataM6["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM6, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_dataM6["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM6, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM6["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM6, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM6["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM6, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM6["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM6, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM6["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM6, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_color_dataM6["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM6, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM6, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM6.mapToGlobal(pos))
                return

        if current_widget == color_widgetM7:
            item_color = self.table_scroll_colorM7.itemAt(pos)
            item_color_dataM7 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM7:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM7, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM7, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM7, "vbm2")
                )

                if item_color_dataM7["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM7, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_dataM7["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM7, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM7["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM7, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM7["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM7, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM7["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM7, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM7["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM7, "vbm9")
                    )
                    menu.addAction(moveTable9)

                if item_color_dataM7["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM7, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM7, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM7.mapToGlobal(pos))
                return

        if current_widget == color_widgetM8:
            item_color = self.table_scroll_colorM8.itemAt(pos)
            item_color_dataM8 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM8:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM8, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM8, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM8, "vbm2")
                )

                if item_color_dataM8["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM8, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_dataM8["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM8, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM8["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM8, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM8["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM8, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM8["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM8, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM8["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM8, "vbm9")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM8["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM8, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM8, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM8.mapToGlobal(pos))
                return

        if current_widget == color_widgetM9:
            item_color = self.table_scroll_colorM9.itemAt(pos)
            item_color_dataM9 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM9:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM9, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM9, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM9, "vbm2")
                )

                if item_color_dataM9["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM9, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_dataM9["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM9, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM9["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM9, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM9["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM9, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM9["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM9, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM9["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM9, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM9["actionM10"] is not None:
                    moveTable10 = QAction("VBM10")
                    moveTable10.setFont(self.font_action)
                    moveTable10.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM9, "vbm10")
                    )
                    menu.addAction(moveTable10)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM9, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM9.mapToGlobal(pos))
                return

        if current_widget == color_widgetM10:
            item_color = self.table_scroll_colorM10.itemAt(pos)
            item_color_dataM10 = item_color.data(Qt.ItemDataRole.UserRole)
            if item_color_dataM10:
                menu = QMenu()
                moveTable = QAction("VBT")
                moveTable.setFont(self.font_action)
                moveTable.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM10, "vbt")
                )

                moveTable1 = QAction("VBM1")
                moveTable1.setFont(self.font_action)
                moveTable1.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM10, "vbm1")
                )

                moveTable2 = QAction("VBM2")
                moveTable2.setFont(self.font_action)
                moveTable2.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM10, "vbm2")
                )

                if item_color_dataM10["actionM3"] is not None:
                    moveTable3 = QAction("VBM3")
                    moveTable3.setFont(self.font_action)
                    moveTable3.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM10, "vbm3")
                    )
                    menu.addAction(moveTable3)

                if item_color_dataM10["actionM4"] is not None:
                    moveTable4 = QAction("VBM4")
                    moveTable4.setFont(self.font_action)
                    moveTable4.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM10, "vbm4")
                    )
                    menu.addAction(moveTable4)

                if item_color_dataM10["actionM5"] is not None:
                    moveTable5 = QAction("VBM5")
                    moveTable5.setFont(self.font_action)
                    moveTable5.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM10, "vbm5")
                    )
                    menu.addAction(moveTable5)

                if item_color_dataM10["actionM6"] is not None:
                    moveTable6 = QAction("VBM6")
                    moveTable6.setFont(self.font_action)
                    moveTable6.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM10, "vbm6")
                    )
                    menu.addAction(moveTable6)

                if item_color_dataM10["actionM7"] is not None:
                    moveTable7 = QAction("VBM7")
                    moveTable7.setFont(self.font_action)
                    moveTable7.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM10, "vbm7")
                    )
                    menu.addAction(moveTable7)

                if item_color_dataM10["actionM8"] is not None:
                    moveTable8 = QAction("VBM8")
                    moveTable8.setFont(self.font_action)
                    moveTable8.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM10, "vbm8")
                    )
                    menu.addAction(moveTable8)

                if item_color_dataM10["actionM9"] is not None:
                    moveTable9 = QAction("VBM9")
                    moveTable9.setFont(self.font_action)
                    moveTable9.triggered.connect(
                        partial(self.moveTableWithAction, item_color_dataM10, "vbm9")
                    )
                    menu.addAction(moveTable9)

                moveTable_thong = QAction("VBThong")
                moveTable_thong.setFont(self.font_action)
                moveTable_thong.triggered.connect(
                    partial(self.moveTableWithAction, item_color_dataM10, "vbthong")
                )

                menu.addAction(moveTable)
                menu.addAction(moveTable1)
                menu.addAction(moveTable2)
                menu.addAction(moveTable_thong)
                menu.exec(self.table_scroll_colorM10.mapToGlobal(pos))
                return

    # TODO Handler Data Table
    # / Table Bang Tinh
    def updateTableCount(self):
        ban_info = self.ban_info
        value_col = ban_info["col"][1] - (ban_info["col"][0] - 1)
        filter_data = [entry for entry in ban_info["data"] if not entry["isDeleted"]]
        rowCount = len(filter_data)
        # Xóa tất cả các item trong bảng trước khi đặt lại số lượng hàng
        self.frozen_table_count.setRowCount(0)
        self.table_scroll_count.setRowCount(0)

        # / Config table
        self.frozen_table_count.setRowCount(rowCount)
        self.table_scroll_count.setRowCount(rowCount)
        thong_range = ban_info["thong"]["value"]
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1

        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            self.frozen_table_count.setItem(i, 0, item)

        # / Render Row without Thong
        for item in self.dataCount:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            item_table = QTableWidgetItem(f"{data_item}")
            item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_table.setForeground(color_item)
            if notice_item:
                item_table.setBackground(notice_item)
            if "actionM1" in item:
                item_table.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "actionM1": item["actionM1"],
                        "actionM2": (item["actionM2"] if "actionM2" in item else None),
                        "actionM3": (item["actionM3"] if "actionM3" in item else None),
                        "actionM4": (item["actionM4"] if "actionM4" in item else None),
                        "actionM5": (item["actionM5"] if "actionM5" in item else None),
                        "actionM6": (item["actionM6"] if "actionM6" in item else None),
                        "actionM7": (item["actionM7"] if "actionM7" in item else None),
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_table,
                    },
                )
            self.table_scroll_count.setItem(row_item, col_item, item_table)

        for i, item in enumerate(filter_data):
            item_thong = item["thong"]
            jump_col = 0
            for j in range(thong_ranges):
                if item_thong > -1:
                    thong_value = self.thong_info[j + thong_range_1][item_thong]
                    if j == 0:
                        item_table = QTableWidgetItem(f"{thong_value}")
                        item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        item_table.setForeground(self.red)
                        self.frozen_table_count.setItem(i, 1, item_table)
                    else:
                        item_table = QTableWidgetItem(f"{thong_value}")
                        item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        item_table.setForeground(self.red)
                        self.table_scroll_count.setItem(i, jump_col, item_table)
                        jump_col += 1
                    jump_col += value_col

        # Đảm bảo cập nhật giao diện của bảng
        # self.frozen_table_count.viewport().update()
        # self.table_scroll_count.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_count.scrollToBottom)
        QTimer.singleShot(0, self.frozen_table_count.scrollToBottom)

        self.frozen_table_count.setColumnWidth(0, 120)

        # sleep(0.5)
        # self.table_scroll_count.scrollToBottom()
        # self.frozen_table_count.scrollToBottom()

        # self.frozen_table_count.resizeRowsToContents()
        # self.table_scroll_count.resizeRowsToContents()

    def updateHeaderCount(self):
        self.table_scroll_count.setColumnCount(0)
        self.ranges = []
        cols_arr = []
        total_column = 0
        thong_range = self.ban_info["thong"]["value"]
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1
        for i in range(thong_ranges):
            range_data = {}
            thong_name = QTableWidgetItem(f"T.{i + thong_range_1 + 1}")
            thong_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            thong_name.setForeground(self.red)
            range_data["start"] = total_column
            range_data["value"] = total_column
            if i != 0:
                cols_arr.append(thong_name)
                total_column += 1
            for j in range(self.ban_info["col"][0] - 1, self.ban_info["col"][1]):
                col_name = QTableWidgetItem(f"C.{j + 1}")
                col_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                cols_arr.append(col_name)
                total_column += 1
            range_data["end"] = total_column
            range_data["thong"] = i + thong_range_1
            self.ranges.append(range_data)

        self.table_scroll_count.setColumnCount(total_column)

        for i, item in enumerate(cols_arr):
            self.table_scroll_count.setHorizontalHeaderItem(i, item)

    # / Table Bang M1
    def updateTableColor(self):
        # / Set RowCount = 0
        self.table_scroll_color.setRowCount(0)
        self.table_scroll_left.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_color.setRowCount(rowCount)
        self.table_scroll_left.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_left.setItem(i, 0, item)
        self.table_scroll_left.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e"]
        col_d = self.ban_info["meta"]["tables"][0]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_color.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_color.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM2": (item["actionM2"] if "actionM2" in item else None),
                        "actionM3": (item["actionM3"] if "actionM3" in item else None),
                        "actionM4": (item["actionM4"] if "actionM4" in item else None),
                        "actionM5": (item["actionM5"] if "actionM5" in item else None),
                        "actionM6": (item["actionM6"] if "actionM6" in item else None),
                        "actionM7": (item["actionM7"] if "actionM7" in item else None),
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_color.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_color.columnCount()):
            width = self.table_scroll_color.columnWidth(i)
            self.frozen_table_color.setColumnWidth(i, width)

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_left.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_color.scrollToBottom)

    def updateHeaderColor(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e"]
        col_d = self.ban_info["meta"]["tables"][0]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_color.setColumnCount(current_column)
        self.table_scroll_color.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M1")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_color.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_color.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_color.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_color.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M2
    def updateTableColorM2(self):
        # / Set RowCount = 0
        self.table_scroll_colorM2.setRowCount(0)
        self.table_scroll_leftM2.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM2.setRowCount(rowCount)
        self.table_scroll_leftM2.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM2.setItem(i, 0, item)
        self.table_scroll_leftM2.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e2"]
        col_d = self.ban_info["meta"]["tables"][1]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM2.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM2.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor2:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM3": (item["actionM3"] if "actionM3" in item else None),
                        "actionM4": (item["actionM4"] if "actionM4" in item else None),
                        "actionM5": (item["actionM5"] if "actionM5" in item else None),
                        "actionM6": (item["actionM6"] if "actionM6" in item else None),
                        "actionM7": (item["actionM7"] if "actionM7" in item else None),
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM2.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM2.columnCount()):
            width = self.table_scroll_colorM2.columnWidth(i)
            self.frozen_table_colorM2.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM2.viewport().update()
        # self.table_scroll_leftM2.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM2.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM2.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM2.scrollToBottom()
        # self.table_scroll_colorM2.scrollToBottom()

    def updateHeaderColorM2(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e2"]
        col_d = self.ban_info["meta"]["tables"][1]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM2.setColumnCount(current_column)
        self.table_scroll_colorM2.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M2")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM2.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM2.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM2.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM2.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M3
    def updateTableColorM3(self):
        # / Set RowCount = 0
        self.table_scroll_colorM3.setRowCount(0)
        self.table_scroll_leftM3.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM3.setRowCount(rowCount)
        self.table_scroll_leftM3.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM3.setItem(i, 0, item)
        self.table_scroll_leftM3.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e3"]
        col_d = self.ban_info["meta"]["tables"][2]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM3.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM3.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor3:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM4": (item["actionM4"] if "actionM4" in item else None),
                        "actionM5": (item["actionM5"] if "actionM5" in item else None),
                        "actionM6": (item["actionM6"] if "actionM6" in item else None),
                        "actionM7": (item["actionM7"] if "actionM7" in item else None),
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM3.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM3.columnCount()):
            width = self.table_scroll_colorM3.columnWidth(i)
            self.frozen_table_colorM3.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM3.viewport().update()
        # self.table_scroll_leftM3.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM3.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM3.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM3.scrollToBottom()
        # self.table_scroll_colorM3.scrollToBottom()

    def updateHeaderColorM3(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e3"]
        col_d = self.ban_info["meta"]["tables"][2]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM3.setColumnCount(current_column)
        self.table_scroll_colorM3.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M3")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM3.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM3.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM3.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM3.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M4
    def updateTableColorM4(self):
        # / Set RowCount = 0
        self.table_scroll_colorM4.setRowCount(0)
        self.table_scroll_leftM4.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM4.setRowCount(rowCount)
        self.table_scroll_leftM4.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM4.setItem(i, 0, item)
        self.table_scroll_leftM4.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e4"]
        col_d = self.ban_info["meta"]["tables"][3]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM4.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM4.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor4:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM3": item["actionM3"],
                        "actionM5": (item["actionM5"] if "actionM5" in item else None),
                        "actionM6": (item["actionM6"] if "actionM6" in item else None),
                        "actionM7": (item["actionM7"] if "actionM7" in item else None),
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM4.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM4.columnCount()):
            width = self.table_scroll_colorM4.columnWidth(i)
            self.frozen_table_colorM4.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM4.viewport().update()
        # self.table_scroll_leftM4.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM4.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM4.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM4.scrollToBottom()
        # self.table_scroll_colorM4.scrollToBottom()

    def updateHeaderColorM4(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e4"]
        col_d = self.ban_info["meta"]["tables"][3]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM4.setColumnCount(current_column)
        self.table_scroll_colorM4.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M4")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM4.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM4.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM4.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM4.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M5
    def updateTableColorM5(self):
        # / Set RowCount = 0
        self.table_scroll_colorM5.setRowCount(0)
        self.table_scroll_leftM5.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM5.setRowCount(rowCount)
        self.table_scroll_leftM5.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM5.setItem(i, 0, item)
        self.table_scroll_leftM5.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e5"]
        col_d = self.ban_info["meta"]["tables"][4]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM5.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM5.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor5:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM3": item["actionM3"],
                        "actionM4": item["actionM4"],
                        "actionM6": (item["actionM6"] if "actionM6" in item else None),
                        "actionM7": (item["actionM7"] if "actionM7" in item else None),
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM5.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM5.columnCount()):
            width = self.table_scroll_colorM5.columnWidth(i)
            self.frozen_table_colorM5.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM5.viewport().update()
        # self.table_scroll_leftM5.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM5.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM5.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM5.scrollToBottom()
        # self.table_scroll_colorM5.scrollToBottom()

    def updateHeaderColorM5(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e5"]
        col_d = self.ban_info["meta"]["tables"][4]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM5.setColumnCount(current_column)
        self.table_scroll_colorM5.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M5")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM5.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM5.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM5.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM5.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M6
    def updateTableColorM6(self):
        # / Set RowCount = 0
        self.table_scroll_colorM6.setRowCount(0)
        self.table_scroll_leftM6.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM6.setRowCount(rowCount)
        self.table_scroll_leftM6.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM6.setItem(i, 0, item)
        self.table_scroll_leftM6.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e6"]
        col_d = self.ban_info["meta"]["tables"][5]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM6.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM6.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor6:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM3": item["actionM3"],
                        "actionM4": item["actionM4"],
                        "actionM5": item["actionM5"],
                        "actionM7": (item["actionM7"] if "actionM7" in item else None),
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM6.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM6.columnCount()):
            width = self.table_scroll_colorM6.columnWidth(i)
            self.frozen_table_colorM6.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM6.viewport().update()
        # self.table_scroll_leftM6.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM6.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM6.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM6.scrollToBottom()
        # self.table_scroll_colorM6.scrollToBottom()

    def updateHeaderColorM6(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e6"]
        col_d = self.ban_info["meta"]["tables"][5]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM6.setColumnCount(current_column)
        self.table_scroll_colorM6.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M6")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM6.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM6.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM6.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM6.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M7
    def updateTableColorM7(self):
        # / Set RowCount = 0
        self.table_scroll_colorM7.setRowCount(0)
        self.table_scroll_leftM7.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM7.setRowCount(rowCount)
        self.table_scroll_leftM7.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM7.setItem(i, 0, item)
        self.table_scroll_leftM7.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e7"]
        col_d = self.ban_info["meta"]["tables"][6]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM7.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM7.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor7:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM3": item["actionM3"],
                        "actionM4": item["actionM4"],
                        "actionM5": item["actionM5"],
                        "actionM6": item["actionM6"],
                        "actionM8": (item["actionM8"] if "actionM8" in item else None),
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM7.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM7.columnCount()):
            width = self.table_scroll_colorM7.columnWidth(i)
            self.frozen_table_colorM7.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM7.viewport().update()
        # self.table_scroll_leftM7.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM7.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM7.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM7.scrollToBottom()
        # self.table_scroll_colorM7.scrollToBottom()

    def updateHeaderColorM7(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e7"]
        col_d = self.ban_info["meta"]["tables"][6]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM7.setColumnCount(current_column)
        self.table_scroll_colorM7.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M7")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM7.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM7.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM7.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM7.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M8
    def updateTableColorM8(self):
        # / Set RowCount = 0
        self.table_scroll_colorM8.setRowCount(0)
        self.table_scroll_leftM8.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM8.setRowCount(rowCount)
        self.table_scroll_leftM8.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM8.setItem(i, 0, item)
        self.table_scroll_leftM8.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e8"]
        col_d = self.ban_info["meta"]["tables"][7]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM8.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM8.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor8:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM3": item["actionM3"],
                        "actionM4": item["actionM4"],
                        "actionM5": item["actionM5"],
                        "actionM6": item["actionM6"],
                        "actionM7": item["actionM7"],
                        "actionM9": (item["actionM9"] if "actionM9" in item else None),
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM8.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM8.columnCount()):
            width = self.table_scroll_colorM8.columnWidth(i)
            self.frozen_table_colorM8.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM8.viewport().update()
        # self.table_scroll_leftM8.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM8.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM8.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM8.scrollToBottom()
        # self.table_scroll_colorM8.scrollToBottom()

    def updateHeaderColorM8(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e8"]
        col_d = self.ban_info["meta"]["tables"][7]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM8.setColumnCount(current_column)
        self.table_scroll_colorM8.setColumnCount(current_column)

        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M8")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM8.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM8.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM8.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM8.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M9
    def updateTableColorM9(self):
        # / Set RowCount = 0
        self.table_scroll_colorM9.setRowCount(0)
        self.table_scroll_leftM9.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM9.setRowCount(rowCount)
        self.table_scroll_leftM9.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM9.setItem(i, 0, item)
        self.table_scroll_leftM9.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e9"]
        col_d = self.ban_info["meta"]["tables"][8]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 93
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM9.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM9.setItem(i, total_columns + num_cols, col_null)
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor9:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM3": item["actionM3"],
                        "actionM4": item["actionM4"],
                        "actionM5": item["actionM5"],
                        "actionM6": item["actionM6"],
                        "actionM7": item["actionM7"],
                        "actionM8": item["actionM8"],
                        "actionM10": (
                            item["actionM10"] if "actionM10" in item else None
                        ),
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM9.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM9.columnCount()):
            width = self.table_scroll_colorM9.columnWidth(i)
            self.frozen_table_colorM9.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM9.viewport().update()
        # self.table_scroll_leftM9.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM9.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM9.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM9.scrollToBottom()
        # self.table_scroll_colorM9.scrollToBottom()

    def updateHeaderColorM9(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e9"]
        col_d = self.ban_info["meta"]["tables"][8]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 93
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM9.setColumnCount(current_column)
        self.table_scroll_colorM9.setColumnCount(current_column)

        # Tạo cột từ 0 đến 93
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M9")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM9.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM9.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM9.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM9.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Table Bang M10
    def updateTableColorM10(self):
        # / Set RowCount = 0
        self.table_scroll_colorM10.setRowCount(0)
        self.table_scroll_leftM10.setRowCount(0)
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        self.table_scroll_colorM10.setRowCount(rowCount)
        self.table_scroll_leftM10.setRowCount(rowCount)
        for i in range(rowCount):
            # date = filter_data[i]["date"].split("/")
            # item = QTableWidgetItem(f"{date[0]}/{date[1]}/.")
            date = filter_data[i]["date"]
            item = QTableWidgetItem(f"{date}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_scroll_leftM10.setItem(i, 0, item)
        self.table_scroll_leftM10.setHorizontalHeaderItem(0, QTableWidgetItem())

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e10"]
        col_d = self.ban_info["meta"]["tables"][9]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 103
        for i in range(rowCount):
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    col_header = QTableWidgetItem(f"*")
                    col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_scroll_colorM10.setItem(i, total_columns + j, col_header)
                # Tạo ô trống ở cột cuối cùng
                col_null = QTableWidgetItem()
                col_null.setBackground(
                    QColor(Qt.GlobalColor.white)
                )  # Đặt màu nền là màu trắng
                self.table_scroll_colorM10.setItem(
                    i, total_columns + num_cols, col_null
                )
                # Cập nhật tổng số cột
                total_columns += num_cols + 1

        # / render row color table
        for item in self.dataColor10:
            row_item = item["row"]
            col_item = item["col"]
            data_item = item["data"]
            color_item = item["color"]
            notice_item = item["notice"]
            action_item = item["action"]
            item_insert = QTableWidgetItem(f"{data_item}")
            item_insert.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if color_item:
                item_insert.setForeground(color_item)
            if notice_item:
                item_insert.setBackground(notice_item)
            if action_item:
                item_insert.setData(
                    Qt.ItemDataRole.UserRole,
                    {
                        "action": action_item,
                        "actionM1": item["actionM1"],
                        "actionM2": item["actionM2"],
                        "actionM3": item["actionM3"],
                        "actionM4": item["actionM4"],
                        "actionM5": item["actionM5"],
                        "actionM6": item["actionM6"],
                        "actionM7": item["actionM7"],
                        "actionM8": item["actionM8"],
                        "actionM9": item["actionM9"],
                        "isColor": notice_item,
                        "thong": item["thong"],
                        "item": item_insert,
                    },
                )
            self.table_scroll_colorM10.setItem(row_item, col_item, item_insert)

        for i in range(self.table_scroll_colorM10.columnCount()):
            width = self.table_scroll_colorM10.columnWidth(i)
            self.frozen_table_colorM10.setColumnWidth(i, width)

        # Đảm bảo cập nhật giao diện của bảng
        # self.table_scroll_colorM10.viewport().update()
        # self.table_scroll_leftM10.viewport().update()

        # Thêm nđộ trễ nhỏ trước khi cuộn
        QTimer.singleShot(0, self.table_scroll_leftM10.scrollToBottom)
        QTimer.singleShot(0, self.table_scroll_colorM10.scrollToBottom)

        # sleep(0.5)
        # self.table_scroll_leftM10.scrollToBottom()
        # self.table_scroll_colorM10.scrollToBottom()

    def updateHeaderColorM10(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e10"]
        col_d = self.ban_info["meta"]["tables"][9]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 103
        for i in range(value1 - 1, value2):
            current_column += (
                col_d[i] + 1
            )  # Số cột tạo cho mỗi lần là 1 cột + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        self.frozen_table_colorM10.setColumnCount(current_column)
        self.table_scroll_colorM10.setColumnCount(current_column)

        # Tạo cột từ 0 đến 103
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Tạo hàng header cho mỗi lần tạo cột
            header_item = QTableWidgetItem(f"D {i + 1}/M10")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.frozen_table_colorM10.setItem(0, total_columns, header_item)
            if num_cols > 1:
                self.frozen_table_colorM10.setSpan(0, total_columns, 1, num_cols)

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                col_header = QTableWidgetItem(f"{j + 1}")
                col_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_scroll_colorM10.setHorizontalHeaderItem(
                    total_columns + j, col_header
                )

            # Tạo ô trống ở cột cuối cùng
            col_null = QTableWidgetItem()
            col_null.setBackground(
                QColor(Qt.GlobalColor.white)
            )  # Đặt màu nền là màu trắng
            self.table_scroll_colorM10.setHorizontalHeaderItem(
                total_columns + num_cols, col_null
            )

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1

    # / Handler Data
    def handlerData(self):
        # / Config Data
        ban_info = self.ban_info
        thong_info = self.thong_info
        ngang_info = self.number_info
        thong_range = ban_info["thong"]["value"]
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1
        ngangs = ban_info["col"][1] - (ban_info["col"][0] - 1)
        data = ban_info["data"]
        meta = ban_info["meta"]["notice"]
        notice_count = meta["count"]
        notice_color1 = meta["color"]
        notice_color2 = meta["color2"]
        notice_colorM2 = meta["colorM2"]
        notice_colorM3 = meta["colorM3"]
        notice_colorM4 = meta["colorM4"]
        notice_colorM5 = meta["colorM5"]
        notice_colorM6 = meta["colorM6"]
        notice_colorM7 = meta["colorM7"]
        notice_colorM8 = meta["colorM8"]
        notice_colorM9 = meta["colorM9"]
        notice_colorM10 = meta["colorM10"]
        notice_color = []
        buttons = ban_info["meta"]["buttons"]
        if buttons[0]:
            notice_color = notice_color1
        if buttons[1]:
            notice_color = notice_color2

        col_e = ban_info["meta"]["setting"]["col_e"]
        value1 = col_e[0]
        value2 = col_e[1]

        col_e2 = ban_info["meta"]["setting"]["col_e2"]
        value1_2 = col_e2[0]
        value2_2 = col_e2[1]

        col_e3 = ban_info["meta"]["setting"]["col_e3"]
        value1_3 = col_e3[0]
        value2_3 = col_e3[1]

        col_e4 = ban_info["meta"]["setting"]["col_e4"]
        value1_4 = col_e4[0]
        value2_4 = col_e4[1]

        col_e5 = ban_info["meta"]["setting"]["col_e5"]
        value1_5 = col_e5[0]
        value2_5 = col_e5[1]

        col_e6 = ban_info["meta"]["setting"]["col_e6"]
        value1_6 = col_e6[0]
        value2_6 = col_e6[1]

        col_e7 = ban_info["meta"]["setting"]["col_e7"]
        value1_7 = col_e7[0]
        value2_7 = col_e7[1]

        col_e8 = ban_info["meta"]["setting"]["col_e8"]
        value1_8 = col_e8[0]
        value2_8 = col_e8[1]

        col_e9 = ban_info["meta"]["setting"]["col_e9"]
        value1_9 = col_e9[0]
        value2_9 = col_e9[1]

        col_e10 = ban_info["meta"]["setting"]["col_e10"]
        value1_10 = col_e10[0]
        value2_10 = col_e10[1]

        # / Setup tables
        tables = self.ban_info["meta"]["tables"]

        # / Setup Variable
        self.count_handler = {}  # data so dem (d = Bang tinh, e = Bang mau)
        self.math_isFirst = (
            {}
        )  # data toan duoc (c1 = Bang tinh, STT = Bang Mau (Min 3 - Max 4))
        self.isFrits = {}  # So dau tien
        self.dataCount = []  # Data Bang tinh
        self.dataColor = []  # Data Bang Mau M1
        self.dataColor2 = []  # Data Bang Mau M2
        self.dataColor3 = []  # Data Bang Mau M3
        self.dataColor4 = []  # Data Bang Mau M4
        self.dataColor5 = []  # Data Bang Mau M5
        self.dataColor6 = []  # Data Bang Mau M6
        self.dataColor7 = []  # Data Bang Mau M7
        self.dataColor8 = []  # Data Bang Mau M8
        self.dataColor9 = []  # Data Bang Mau M9
        self.dataColor10 = []  # Data Bang Mau M10
        countRow = 0
        isCountRow = 0
        # / Start Render data
        for i, item in enumerate(data):
            item_date = item.get("date")
            item_thong = item.get("thong")
            item_ngang = item.get("ngang")
            isDeleted = item.get("isDeleted")
            total_column = 0
            if not isDeleted:
                countRow = isCountRow
                isCountRow += 1
            else:
                countRow = -1
            for t in range(thong_ranges):
                col_t = (
                    thong_info[t + thong_range_1][item_thong]
                    if item_thong > -1
                    else f"?"
                )
                if t != 0:
                    total_column += 1
                for c in range(ngangs):
                    col_a = ngang_info[item_ngang][c]
                    stt_cot = c + 1

                    # / Start Count Handler
                    dem_col_row = f"{stt_cot}:{t}"
                    if not dem_col_row in self.count_handler:
                        self.count_handler[dem_col_row] = 1
                    else:
                        self.count_handler[dem_col_row] += 1
                    # / End Count Handler
                    col_d = self.count_handler[dem_col_row]  # so dem Bang tinh
                    isNoticeCount = self.checkNotice(
                        col_d, notice_count[0], notice_count[1]
                    )

                    # / Start check isFirst
                    isColFisrt = f"{col_a}:{i}:{col_d}"

                    # / Check col_a equal col_t
                    isEqual = (
                        self.checkColor(str(col_a), str(col_t))
                        if item_thong > -1
                        else None
                    )

                    if col_d == 1:
                        self.dataCount.append(
                            {
                                "row": countRow,
                                "col": total_column,
                                "color": isEqual,
                                "data": f"{col_a}/{col_d}",
                                "notice": isNoticeCount,
                                "date": item_date,
                                "color_value": col_d,
                                "isDeleted": isDeleted,
                            }
                        )
                    else:
                        # / End count color with col_d
                        if value1 <= col_d <= value2:
                            if not isColFisrt in self.isFrits:
                                self.isFrits[isColFisrt] = True
                                # / Start check col_stt table count min 3 and max 4 with every count_handler
                                math_count_handler = f"{col_d}:{i}:_color"
                                if not math_count_handler in self.count_handler:
                                    self.count_handler[math_count_handler] = 1
                                else:
                                    self.count_handler[math_count_handler] += 1

                                # / End check col_stt table count
                                stt_count_with_d = self.count_handler[
                                    math_count_handler
                                ]  # So thu tu cua so dem

                                # / Config number col_d M1
                                number_col_d_m1 = tables[0]["col_d"][col_d - 1]

                                # / Start Check count handler with if and else
                                if stt_count_with_d <= number_col_d_m1:

                                    # / Start count color with col_d
                                    col_e_count = f"{col_d}:{stt_count_with_d}:col_e"
                                    if not col_e_count in self.count_handler:
                                        self.count_handler[col_e_count] = 1
                                    else:
                                        self.count_handler[col_e_count] += 1
                                    col_e = self.count_handler[
                                        col_e_count
                                    ]  # so dem bang mau
                                    isNoticeColor = self.checkNotice(
                                        col_e, notice_color[0], notice_color[1]
                                    )
                                    # find_null_color = (
                                    #             1 if col_d - value1 > 0 else 0
                                    #         ) * (col_d - value1)
                                    find_stt_color = stt_count_with_d - 1
                                    find_next_color = self.find_column_by_index(
                                        tables[0]["col_d"],
                                        col_d - value1,
                                        value1 - 1,
                                        value2,
                                    )
                                    col_color = (
                                        find_next_color + 0 + find_stt_color
                                    )  # vi tri col cua item bang mau
                                    row_thong = item_thong
                                    if row_thong < 0:
                                        row_thong = self.find_row_thong_with_col_a(
                                            col_a, thong_info[t + thong_range_1]
                                        )
                                    # / Add Data to Table count
                                    dataCount = {
                                        "row": countRow,
                                        "col": total_column,
                                        "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d}",
                                        "color": isEqual,
                                        "actionM1": {
                                            "name": "color",
                                            "row": countRow,
                                            "col": col_color,
                                            "isColor": isNoticeColor,
                                        },
                                        "notice": isNoticeCount,
                                        "date": item_date,
                                        "color_value": col_d,
                                        "thong": {
                                            "row": row_thong,
                                            "col": t + 5,
                                            "col_a": col_t if col_t != "?" else col_a,
                                            "isCol_a": False if col_t != "?" else True,
                                        },
                                        "isDeleted": isDeleted,
                                    }

                                    dataColorM1 = {
                                        "row": countRow,
                                        "col": col_color,
                                        "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}",
                                        "color": isEqual,
                                        "action": {
                                            "name": "count",
                                            "row": countRow,
                                            "col": total_column,
                                            "isColor": isNoticeCount,
                                        },
                                        "notice": isNoticeColor,
                                        "date": item_date,
                                        "color_value": col_e,
                                        "col_d": col_d,
                                        "thong": {
                                            "row": row_thong,
                                            "col": t + 5,
                                            "col_a": col_t if col_t != "?" else col_a,
                                            "isCol_a": False if col_t != "?" else True,
                                        },
                                        "isDeleted": isDeleted,
                                    }

                                    dataColorM2 = None

                                    dataColorM3 = None

                                    dataColorM4 = None

                                    dataColorM5 = None

                                    dataColorM6 = None

                                    dataColorM7 = None

                                    dataColorM8 = None

                                    dataColorM9 = None

                                    dataColorM10 = None

                                    # / M2 Start
                                    if value1_2 <= col_e <= value2_2:
                                        math_count_handler_m2 = f"{col_e}:{i}:_color_m2"
                                        if (
                                            not math_count_handler_m2
                                            in self.count_handler
                                        ):
                                            self.count_handler[
                                                math_count_handler_m2
                                            ] = 1
                                        else:
                                            self.count_handler[
                                                math_count_handler_m2
                                            ] += 1

                                        # / End check col_stt table count
                                        stt_count_with_d_m2 = self.count_handler[
                                            math_count_handler_m2
                                        ]  # So thu tu cua so dem

                                        # / Config number col_d M1
                                        number_col_d_m2 = tables[1]["col_d"][col_e - 1]

                                        if stt_count_with_d_m2 <= number_col_d_m2:
                                            # / Start count color with col_e
                                            col_e_count_m2 = f"{col_e}:{stt_count_with_d_m2}:col_e_m2"
                                            if not col_e_count_m2 in self.count_handler:
                                                self.count_handler[col_e_count_m2] = 1
                                            else:
                                                self.count_handler[col_e_count_m2] += 1
                                            col_e_m2 = self.count_handler[
                                                col_e_count_m2
                                            ]  # so dem bang mau
                                            isNoticeColor_m2 = self.checkNotice(
                                                col_e_m2,
                                                notice_colorM2[0],
                                                notice_colorM2[1],
                                            )
                                            find_null_color_m2 = 0
                                            find_stt_color_m2 = stt_count_with_d_m2 - 1
                                            find_next_color_m2 = (
                                                self.find_column_by_index(
                                                    tables[1]["col_d"],
                                                    col_e - value1_2,
                                                    value1_2 - 1,
                                                    value2_2,
                                                )
                                            )
                                            col_color_m2 = (
                                                find_next_color_m2
                                                + find_null_color_m2
                                                + find_stt_color_m2
                                            )  # vi tri col cua item bang mau
                                            # / Add data to table color
                                            dataColorM2 = {
                                                "row": countRow,
                                                "col": col_color_m2,
                                                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}",
                                                "color": isEqual,
                                                "action": {
                                                    "name": "count",
                                                    "row": countRow,
                                                    "col": total_column,
                                                    "isColor": isNoticeCount,
                                                },
                                                "actionM1": {
                                                    "name": "color",
                                                    "row": countRow,
                                                    "col": col_color,
                                                    "isColor": isNoticeColor,
                                                },
                                                "notice": isNoticeColor_m2,
                                                "date": item_date,
                                                "color_value": col_e2,
                                                "col_d": col_e,
                                                "thong": {
                                                    "row": row_thong,
                                                    "col": t + 5,
                                                    "col_a": (
                                                        col_t if col_t != "?" else col_a
                                                    ),
                                                    "isCol_a": (
                                                        False if col_t != "?" else True
                                                    ),
                                                },
                                                "isDeleted": isDeleted,
                                            }

                                            if isEqual:
                                                self.count_handler[col_e_count_m2] = 0

                                            # / M3 start
                                            if value1_3 <= col_e_m2 <= value2_3:
                                                math_count_handler_m3 = (
                                                    f"{col_e_m2}:{i}:_color_m3"
                                                )
                                                if (
                                                    not math_count_handler_m3
                                                    in self.count_handler
                                                ):
                                                    self.count_handler[
                                                        math_count_handler_m3
                                                    ] = 1
                                                else:
                                                    self.count_handler[
                                                        math_count_handler_m3
                                                    ] += 1

                                                # / End check col_stt table count
                                                stt_count_with_d_m3 = (
                                                    self.count_handler[
                                                        math_count_handler_m3
                                                    ]
                                                )  # So thu tu cua so dem
                                                number_col_d_m3 = tables[2]["col_d"][
                                                    col_e_m2 - 1
                                                ]

                                                if (
                                                    stt_count_with_d_m3
                                                    <= number_col_d_m3
                                                ):
                                                    # / Start count color with col_e
                                                    col_e_count_m3 = f"{col_e_m2}:{stt_count_with_d_m3}:col_e_m3"
                                                    if (
                                                        not col_e_count_m3
                                                        in self.count_handler
                                                    ):
                                                        self.count_handler[
                                                            col_e_count_m3
                                                        ] = 1
                                                    else:
                                                        self.count_handler[
                                                            col_e_count_m3
                                                        ] += 1
                                                    col_e_m3 = self.count_handler[
                                                        col_e_count_m3
                                                    ]  # so dem bang mau
                                                    isNoticeColor_m3 = self.checkNotice(
                                                        col_e_m3,
                                                        notice_colorM3[0],
                                                        notice_colorM3[1],
                                                    )
                                                    find_null_color_m3 = 0
                                                    find_stt_color_m3 = (
                                                        stt_count_with_d_m3 - 1
                                                    )
                                                    find_next_color_m3 = (
                                                        self.find_column_by_index(
                                                            tables[2]["col_d"],
                                                            col_e_m2 - value1_3,
                                                            value1_3 - 1,
                                                            value2_3,
                                                        )
                                                    )
                                                    col_color_m3 = (
                                                        find_next_color_m3
                                                        + find_null_color_m3
                                                        + find_stt_color_m3
                                                    )  # vi tri col cua item bang mau
                                                    # / Add data to table color 3
                                                    dataColorM3 = {
                                                        "row": countRow,
                                                        "col": col_color_m3,
                                                        "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}",
                                                        "color": isEqual,
                                                        "action": {
                                                            "name": "count",
                                                            "row": countRow,
                                                            "col": total_column,
                                                            "isColor": isNoticeCount,
                                                        },
                                                        "actionM1": {
                                                            "name": "color",
                                                            "row": countRow,
                                                            "col": col_color,
                                                            "isColor": isNoticeColor,
                                                        },
                                                        "actionM2": {
                                                            "name": "color",
                                                            "row": countRow,
                                                            "col": col_color_m2,
                                                            "isColor": isNoticeColor_m2,
                                                        },
                                                        "notice": isNoticeColor_m3,
                                                        "date": item_date,
                                                        "color_value": col_e3,
                                                        "col_d": col_e_m2,
                                                        "thong": {
                                                            "row": row_thong,
                                                            "col": t + 5,
                                                            "col_a": (
                                                                col_t
                                                                if col_t != "?"
                                                                else col_a
                                                            ),
                                                            "isCol_a": (
                                                                False
                                                                if col_t != "?"
                                                                else True
                                                            ),
                                                        },
                                                        "isDeleted": isDeleted,
                                                    }

                                                    if isEqual:
                                                        self.count_handler[
                                                            col_e_count_m3
                                                        ] = 0
                                                    # / M4 start
                                                    if value1_4 <= col_e_m3 <= value2_4:
                                                        data_m4 = self.handler_data_m4(
                                                            i,
                                                            t,
                                                            col_e_m3,
                                                            notice_colorM4,
                                                            value1_4,
                                                            value2_4,
                                                            countRow,
                                                            col_a,
                                                            thong_range_1,
                                                            stt_cot,
                                                            col_d,
                                                            col_t,
                                                            col_e,
                                                            col_e_m2,
                                                            isEqual,
                                                            total_column,
                                                            isNoticeCount,
                                                            col_color,
                                                            col_color_m2,
                                                            col_color_m3,
                                                            isNoticeColor,
                                                            isNoticeColor_m2,
                                                            isNoticeColor_m3,
                                                            item_date,
                                                            col_e4,
                                                            row_thong,
                                                            isDeleted,
                                                        )
                                                        if data_m4:
                                                            m4, object_m4 = (
                                                                data_m4["m4"],
                                                                data_m4["object"],
                                                            )
                                                            (
                                                                col_e_m4,
                                                                isNoticeColor_m4,
                                                                col_color_m4,
                                                            ) = (
                                                                object_m4["col_e_m4"],
                                                                object_m4[
                                                                    "isNoticeColor_m4"
                                                                ],
                                                                object_m4[
                                                                    "col_color_m4"
                                                                ],
                                                            )
                                                            dataColorM4 = m4
                                                            # / M5 start
                                                            if (
                                                                value1_5
                                                                <= col_e_m4
                                                                <= value2_5
                                                            ):
                                                                data_m5 = self.handler_data_m5(
                                                                    i,
                                                                    t,
                                                                    col_e_m3,
                                                                    notice_colorM5,
                                                                    value1_5,
                                                                    value2_5,
                                                                    countRow,
                                                                    col_a,
                                                                    thong_range_1,
                                                                    stt_cot,
                                                                    col_d,
                                                                    col_t,
                                                                    col_e,
                                                                    col_e_m2,
                                                                    col_e_m4,
                                                                    isEqual,
                                                                    total_column,
                                                                    isNoticeCount,
                                                                    col_color,
                                                                    col_color_m2,
                                                                    col_color_m3,
                                                                    col_color_m4,
                                                                    isNoticeColor,
                                                                    isNoticeColor_m2,
                                                                    isNoticeColor_m3,
                                                                    isNoticeColor_m4,
                                                                    item_date,
                                                                    col_e5,
                                                                    row_thong,
                                                                    isDeleted,
                                                                )
                                                                if data_m5:
                                                                    m5, object_m5 = (
                                                                        data_m5["m5"],
                                                                        data_m5[
                                                                            "object"
                                                                        ],
                                                                    )
                                                                    (
                                                                        col_e_m5,
                                                                        isNoticeColor_m5,
                                                                        col_color_m5,
                                                                    ) = (
                                                                        object_m5[
                                                                            "col_e_m5"
                                                                        ],
                                                                        object_m5[
                                                                            "isNoticeColor_m5"
                                                                        ],
                                                                        object_m5[
                                                                            "col_color_m5"
                                                                        ],
                                                                    )
                                                                    dataColorM5 = m5
                                                                    # / M6 start
                                                                    if (
                                                                        value1_6
                                                                        <= col_e_m5
                                                                        <= value2_6
                                                                    ):
                                                                        data_m6 = self.handler_data_m6(
                                                                            i,
                                                                            t,
                                                                            col_e_m3,
                                                                            notice_colorM6,
                                                                            value1_6,
                                                                            value2_6,
                                                                            countRow,
                                                                            col_a,
                                                                            thong_range_1,
                                                                            stt_cot,
                                                                            col_d,
                                                                            col_t,
                                                                            col_e,
                                                                            col_e_m2,
                                                                            col_e_m4,
                                                                            col_e_m5,
                                                                            isEqual,
                                                                            total_column,
                                                                            isNoticeCount,
                                                                            col_color,
                                                                            col_color_m2,
                                                                            col_color_m3,
                                                                            col_color_m4,
                                                                            col_color_m5,
                                                                            isNoticeColor,
                                                                            isNoticeColor_m2,
                                                                            isNoticeColor_m3,
                                                                            isNoticeColor_m4,
                                                                            isNoticeColor_m5,
                                                                            item_date,
                                                                            col_e6,
                                                                            row_thong,
                                                                            isDeleted,
                                                                        )
                                                                        if data_m6:
                                                                            (
                                                                                m6,
                                                                                object_m6,
                                                                            ) = (
                                                                                data_m6[
                                                                                    "m6"
                                                                                ],
                                                                                data_m6[
                                                                                    "object"
                                                                                ],
                                                                            )
                                                                            dataColorM6 = (
                                                                                m6
                                                                            )

                                                                            (
                                                                                col_e_m6,
                                                                                isNoticeColor_m6,
                                                                                col_color_m6,
                                                                            ) = (
                                                                                object_m6[
                                                                                    "col_e_m6"
                                                                                ],
                                                                                object_m6[
                                                                                    "isNoticeColor_m6"
                                                                                ],
                                                                                object_m6[
                                                                                    "col_color_m6"
                                                                                ],
                                                                            )
                                                                            # / M7 Start
                                                                            if (
                                                                                value1_7
                                                                                <= col_e_m6
                                                                                <= value2_7
                                                                            ):
                                                                                data_m7 = self.handler_data_m7(
                                                                                    i,
                                                                                    t,
                                                                                    notice_colorM7,
                                                                                    value1_7,
                                                                                    value2_7,
                                                                                    countRow,
                                                                                    col_a,
                                                                                    thong_range_1,
                                                                                    stt_cot,
                                                                                    col_d,
                                                                                    col_t,
                                                                                    col_e,
                                                                                    col_e_m2,
                                                                                    col_e_m3,
                                                                                    col_e_m4,
                                                                                    col_e_m5,
                                                                                    col_e_m6,
                                                                                    isEqual,
                                                                                    total_column,
                                                                                    isNoticeCount,
                                                                                    col_color,
                                                                                    col_color_m2,
                                                                                    col_color_m3,
                                                                                    col_color_m4,
                                                                                    col_color_m5,
                                                                                    col_color_m6,
                                                                                    isNoticeColor,
                                                                                    isNoticeColor_m2,
                                                                                    isNoticeColor_m3,
                                                                                    isNoticeColor_m4,
                                                                                    isNoticeColor_m5,
                                                                                    isNoticeColor_m6,
                                                                                    item_date,
                                                                                    col_e7,
                                                                                    row_thong,
                                                                                    isDeleted,
                                                                                )
                                                                                if data_m7:
                                                                                    (
                                                                                        m7,
                                                                                        object_m7,
                                                                                    ) = (
                                                                                        data_m7[
                                                                                            "m7"
                                                                                        ],
                                                                                        data_m7[
                                                                                            "object"
                                                                                        ],
                                                                                    )
                                                                                    dataColorM7 = m7

                                                                                    (
                                                                                        col_e_m7,
                                                                                        isNoticeColor_m7,
                                                                                        col_color_m7,
                                                                                    ) = (
                                                                                        object_m7[
                                                                                            "col_e_m7"
                                                                                        ],
                                                                                        object_m7[
                                                                                            "isNoticeColor_m7"
                                                                                        ],
                                                                                        object_m7[
                                                                                            "col_color_m7"
                                                                                        ],
                                                                                    )
                                                                                    # / M8 Start
                                                                                    if (
                                                                                        value1_8
                                                                                        <= col_e_m7
                                                                                        <= value2_8
                                                                                    ):
                                                                                        data_m8 = self.handler_data_m8(
                                                                                            i,
                                                                                            t,
                                                                                            col_e_m3,
                                                                                            notice_colorM8,
                                                                                            value1_8,
                                                                                            value2_8,
                                                                                            countRow,
                                                                                            col_a,
                                                                                            thong_range_1,
                                                                                            stt_cot,
                                                                                            col_d,
                                                                                            col_t,
                                                                                            col_e,
                                                                                            col_e_m2,
                                                                                            col_e_m4,
                                                                                            col_e_m5,
                                                                                            col_e_m6,
                                                                                            col_e_m7,
                                                                                            isEqual,
                                                                                            total_column,
                                                                                            isNoticeCount,
                                                                                            col_color,
                                                                                            col_color_m2,
                                                                                            col_color_m3,
                                                                                            col_color_m4,
                                                                                            col_color_m5,
                                                                                            col_color_m6,
                                                                                            col_color_m7,
                                                                                            isNoticeColor,
                                                                                            isNoticeColor_m2,
                                                                                            isNoticeColor_m3,
                                                                                            isNoticeColor_m4,
                                                                                            isNoticeColor_m5,
                                                                                            isNoticeColor_m6,
                                                                                            isNoticeColor_m7,
                                                                                            item_date,
                                                                                            col_e8,
                                                                                            row_thong,
                                                                                            isDeleted,
                                                                                        )
                                                                                        if data_m8:
                                                                                            (
                                                                                                m8,
                                                                                                object_m8,
                                                                                            ) = (
                                                                                                data_m8[
                                                                                                    "m8"
                                                                                                ],
                                                                                                data_m8[
                                                                                                    "object"
                                                                                                ],
                                                                                            )
                                                                                            dataColorM8 = m8

                                                                                            (
                                                                                                col_e_m8,
                                                                                                isNoticeColor_m8,
                                                                                                col_color_m8,
                                                                                            ) = (
                                                                                                object_m8[
                                                                                                    "col_e_m8"
                                                                                                ],
                                                                                                object_m8[
                                                                                                    "isNoticeColor_m8"
                                                                                                ],
                                                                                                object_m8[
                                                                                                    "col_color_m8"
                                                                                                ],
                                                                                            )
                                                                                            # / M9 start;
                                                                                            if (
                                                                                                value1_9
                                                                                                <= col_e_m8
                                                                                                <= value2_9
                                                                                            ):
                                                                                                data_m9 = self.handler_data_m9(
                                                                                                    i,
                                                                                                    t,
                                                                                                    col_e_m3,
                                                                                                    notice_colorM9,
                                                                                                    value1_9,
                                                                                                    value2_9,
                                                                                                    countRow,
                                                                                                    col_a,
                                                                                                    thong_range_1,
                                                                                                    stt_cot,
                                                                                                    col_d,
                                                                                                    col_t,
                                                                                                    col_e,
                                                                                                    col_e_m2,
                                                                                                    col_e_m4,
                                                                                                    col_e_m5,
                                                                                                    col_e_m6,
                                                                                                    col_e_m7,
                                                                                                    col_e_m8,
                                                                                                    isEqual,
                                                                                                    total_column,
                                                                                                    isNoticeCount,
                                                                                                    col_color,
                                                                                                    col_color_m2,
                                                                                                    col_color_m3,
                                                                                                    col_color_m4,
                                                                                                    col_color_m5,
                                                                                                    col_color_m6,
                                                                                                    col_color_m7,
                                                                                                    col_color_m8,
                                                                                                    isNoticeColor,
                                                                                                    isNoticeColor_m2,
                                                                                                    isNoticeColor_m3,
                                                                                                    isNoticeColor_m4,
                                                                                                    isNoticeColor_m5,
                                                                                                    isNoticeColor_m6,
                                                                                                    isNoticeColor_m7,
                                                                                                    isNoticeColor_m8,
                                                                                                    item_date,
                                                                                                    col_e9,
                                                                                                    row_thong,
                                                                                                    isDeleted,
                                                                                                )
                                                                                                if data_m9:
                                                                                                    (
                                                                                                        m9,
                                                                                                        object_m9,
                                                                                                    ) = (
                                                                                                        data_m9[
                                                                                                            "m9"
                                                                                                        ],
                                                                                                        data_m9[
                                                                                                            "object"
                                                                                                        ],
                                                                                                    )
                                                                                                    dataColorM9 = m9

                                                                                                    (
                                                                                                        col_e_m9,
                                                                                                        isNoticeColor_m9,
                                                                                                        col_color_m9,
                                                                                                    ) = (
                                                                                                        object_m9[
                                                                                                            "col_e_m9"
                                                                                                        ],
                                                                                                        object_m9[
                                                                                                            "isNoticeColor_m9"
                                                                                                        ],
                                                                                                        object_m9[
                                                                                                            "col_color_m9"
                                                                                                        ],
                                                                                                    )
                                                                                                    # / M10 Start;
                                                                                                    if (
                                                                                                        value1_10
                                                                                                        <= col_e_m9
                                                                                                        <= value2_10
                                                                                                    ):
                                                                                                        data_m10 = self.handler_data_m10(
                                                                                                            i,
                                                                                                            t,
                                                                                                            col_e_m3,
                                                                                                            notice_colorM10,
                                                                                                            value1_10,
                                                                                                            value2_10,
                                                                                                            countRow,
                                                                                                            col_a,
                                                                                                            thong_range_1,
                                                                                                            stt_cot,
                                                                                                            col_d,
                                                                                                            col_t,
                                                                                                            col_e,
                                                                                                            col_e_m2,
                                                                                                            col_e_m4,
                                                                                                            col_e_m5,
                                                                                                            col_e_m6,
                                                                                                            col_e_m7,
                                                                                                            col_e_m8,
                                                                                                            col_e_m9,
                                                                                                            isEqual,
                                                                                                            total_column,
                                                                                                            isNoticeCount,
                                                                                                            col_color,
                                                                                                            col_color_m2,
                                                                                                            col_color_m3,
                                                                                                            col_color_m4,
                                                                                                            col_color_m5,
                                                                                                            col_color_m6,
                                                                                                            col_color_m7,
                                                                                                            col_color_m8,
                                                                                                            col_color_m9,
                                                                                                            isNoticeColor,
                                                                                                            isNoticeColor_m2,
                                                                                                            isNoticeColor_m3,
                                                                                                            isNoticeColor_m4,
                                                                                                            isNoticeColor_m5,
                                                                                                            isNoticeColor_m6,
                                                                                                            isNoticeColor_m7,
                                                                                                            isNoticeColor_m8,
                                                                                                            isNoticeColor_m9,
                                                                                                            item_date,
                                                                                                            col_e10,
                                                                                                            row_thong,
                                                                                                            isDeleted,
                                                                                                        )
                                                                                                        if data_m10:
                                                                                                            m10 = data_m10[
                                                                                                                "m10"
                                                                                                            ]
                                                                                                            dataColorM10 = m10

                                    if dataColorM10 and self.ban_info["meta"]["tables"][9]["enable"] == True:
                                        self.dataColor10.append(dataColorM10)
                                        dataCount["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM1["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM2["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM3["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM4["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM5["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM6["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM7["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM8["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM9["actionM10"] = {
                                                            "name": "colorM10",
                                                            "row": countRow,
                                                            "col": dataColorM10["col"],
                                                            "isColor": dataColorM10[
                                                                "notice"
                                                            ],
                                                        }
  
                                    if dataColorM9 and self.ban_info["meta"]["tables"][8]["enable"] == True:
                                        self.dataColor9.append(dataColorM9)
                                        dataCount["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM1["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM2["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM3["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM4["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM5["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM6["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM7["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM8["actionM9"] = {
                                                            "name": "colorM9",
                                                            "row": countRow,
                                                            "col": dataColorM9["col"],
                                                            "isColor": dataColorM9[
                                                                "notice"
                                                            ],
                                                        }
                                        
                                    if dataColorM8 and self.ban_info["meta"]["tables"][7]["enable"] == True:
                                        self.dataColor8.append(dataColorM8)
                                        dataCount["actionM8"] = {
                                            "name": "colorM8",
                                            "row": countRow,
                                            "col": dataColorM8["col"],
                                            "isColor": dataColorM8["notice"],
                                        }
                                        dataColorM1["actionM8"] = {
                                                            "name": "colorM8",
                                                            "row": countRow,
                                                            "col": dataColorM8["col"],
                                                            "isColor": dataColorM8[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM2["actionM8"] = {
                                                            "name": "colorM8",
                                                            "row": countRow,
                                                            "col": dataColorM8["col"],
                                                            "isColor": dataColorM8[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM3["actionM8"] = {
                                                            "name": "colorM8",
                                                            "row": countRow,
                                                            "col": dataColorM8["col"],
                                                            "isColor": dataColorM8[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM4["actionM8"] = {
                                                            "name": "colorM8",
                                                            "row": countRow,
                                                            "col": dataColorM8["col"],
                                                            "isColor": dataColorM8[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM5["actionM8"] = {
                                                            "name": "colorM8",
                                                            "row": countRow,
                                                            "col": dataColorM8["col"],
                                                            "isColor": dataColorM8[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM6["actionM8"] = {
                                                            "name": "colorM8",
                                                            "row": countRow,
                                                            "col": dataColorM8["col"],
                                                            "isColor": dataColorM8[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM7["actionM8"] = {
                                                            "name": "colorM8",
                                                            "row": countRow,
                                                            "col": dataColorM8["col"],
                                                            "isColor": dataColorM8[
                                                                "notice"
                                                            ],
                                                        }

                                    if dataColorM7 and self.ban_info["meta"]["tables"][6]["enable"] == True:
                                        self.dataColor7.append(dataColorM7)
                                        dataCount["actionM7"] = {
                                            "name": "colorM7",
                                            "row": countRow,
                                            "col": dataColorM7["col"],
                                            "isColor": dataColorM7["notice"],
                                        }
                                        dataColorM1["actionM7"] = {
                                                            "name": "colorM7",
                                                            "row": countRow,
                                                            "col": dataColorM7["col"],
                                                            "isColor": dataColorM7[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM2["actionM7"] = {
                                                            "name": "colorM7",
                                                            "row": countRow,
                                                            "col": dataColorM7["col"],
                                                            "isColor": dataColorM7[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM3["actionM7"] = {
                                                            "name": "colorM7",
                                                            "row": countRow,
                                                            "col": dataColorM7["col"],
                                                            "isColor": dataColorM7[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM4["actionM7"] = {
                                                            "name": "colorM7",
                                                            "row": countRow,
                                                            "col": dataColorM7["col"],
                                                            "isColor": dataColorM7[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM5["actionM7"] = {
                                                            "name": "colorM7",
                                                            "row": countRow,
                                                            "col": dataColorM7["col"],
                                                            "isColor": dataColorM7[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM6["actionM7"] = {
                                                            "name": "colorM7",
                                                            "row": countRow,
                                                            "col": dataColorM7["col"],
                                                            "isColor": dataColorM7[
                                                                "notice"
                                                            ],
                                                        }

                                    if dataColorM6 and self.ban_info["meta"]["tables"][5]["enable"] == True:
                                        self.dataColor6.append(dataColorM6)
                                        dataCount["actionM6"] = {
                                            "name": "colorM6",
                                            "row": countRow,
                                            "col": dataColorM6["col"],
                                            "isColor": dataColorM6["notice"],
                                        }
                                        dataColorM1["actionM6"] = {
                                                            "name": "colorM6",
                                                            "row": countRow,
                                                            "col": dataColorM6["col"],
                                                            "isColor": dataColorM6[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM2["actionM6"] = {
                                                            "name": "colorM6",
                                                            "row": countRow,
                                                            "col": dataColorM6["col"],
                                                            "isColor": dataColorM6[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM3["actionM6"] = {
                                                            "name": "colorM6",
                                                            "row": countRow,
                                                            "col": dataColorM6["col"],
                                                            "isColor": dataColorM6[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM4["actionM6"] = {
                                                            "name": "colorM6",
                                                            "row": countRow,
                                                            "col": dataColorM6["col"],
                                                            "isColor": dataColorM6[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM5["actionM6"] = {
                                                            "name": "colorM6",
                                                            "row": countRow,
                                                            "col": dataColorM6["col"],
                                                            "isColor": dataColorM6[
                                                                "notice"
                                                            ],
                                                        }

                                    if dataColorM5 and self.ban_info["meta"]["tables"][4]["enable"] == True:
                                        self.dataColor5.append(dataColorM5)
                                        dataCount["actionM5"] = {
                                            "name": "colorM5",
                                            "row": countRow,
                                            "col": dataColorM5["col"],
                                            "isColor": dataColorM5["notice"],
                                        }
                                        dataColorM1["actionM5"] = {
                                                            "name": "colorM5",
                                                            "row": countRow,
                                                            "col": dataColorM5["col"],
                                                            "isColor": dataColorM5[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM2["actionM5"] = {
                                                            "name": "colorM5",
                                                            "row": countRow,
                                                            "col": dataColorM5["col"],
                                                            "isColor": dataColorM5[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM3["actionM5"] = {
                                                            "name": "colorM5",
                                                            "row": countRow,
                                                            "col": dataColorM5["col"],
                                                            "isColor": dataColorM5[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM4["actionM5"] = {
                                                            "name": "colorM5",
                                                            "row": countRow,
                                                            "col": dataColorM5["col"],
                                                            "isColor": dataColorM5[
                                                                "notice"
                                                            ],
                                                        }

                                    if dataColorM4 and self.ban_info["meta"]["tables"][3]["enable"] == True:
                                        self.dataColor4.append(dataColorM4)
                                        dataCount["actionM4"] = {
                                            "name": "colorM4",
                                            "row": countRow,
                                            "col": dataColorM4["col"],
                                            "isColor": dataColorM4["notice"],
                                        }
                                        dataColorM1["actionM4"] = {
                                                            "name": "colorM4",
                                                            "row": countRow,
                                                            "col": dataColorM4["col"],
                                                            "isColor": dataColorM4[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM2["actionM4"] = {
                                                            "name": "colorM4",
                                                            "row": countRow,
                                                            "col": dataColorM4["col"],
                                                            "isColor": dataColorM4[
                                                                "notice"
                                                            ],
                                                        }
                                        dataColorM3["actionM4"] = {
                                                            "name": "colorM4",
                                                            "row": countRow,
                                                            "col": dataColorM4["col"],
                                                            "isColor": dataColorM4[
                                                                "notice"
                                                            ],
                                                        }

                                    if dataColorM3 and self.ban_info["meta"]["tables"][2]["enable"] == True:
                                        self.dataColor3.append(dataColorM3)
                                        dataCount["actionM3"] = {
                                            "name": "colorM3",
                                            "row": countRow,
                                            "col": dataColorM3["col"],
                                            "isColor": dataColorM3["notice"],
                                        }

                                        dataColorM1["actionM3"] = {
                                                            "name": "colorM3",
                                                            "row": countRow,
                                                            "col": dataColorM3["col"],
                                                            "isColor": dataColorM3[
                                                                "notice"
                                                            ],
                                                        }

                                        dataColorM2["actionM3"] = {
                                                            "name": "colorM3",
                                                            "row": countRow,
                                                            "col": dataColorM3["col"],
                                                            "isColor": dataColorM3[
                                                                "notice"
                                                            ],
                                                        }

                                    if dataColorM2 and self.ban_info["meta"]["tables"][1]["enable"] == True:
                                        self.dataColor2.append(dataColorM2)
                                        dataCount["actionM2"] = {
                                            "name": "colorM2",
                                            "row": countRow,
                                            "col": dataColorM2["col"],
                                            "isColor": dataColorM2["notice"],
                                        }
                                        dataColorM1["actionM2"] = {
                                            "name": "colorM2",
                                            "row": countRow,
                                            "col": dataColorM2["col"],
                                            "isColor": dataColorM2["notice"],
                                        }

                                    self.dataCount.append(dataCount)

                                    # / Add data to table color
                                    self.dataColor.append(dataColorM1)

                                    if isEqual:
                                        # / Reset Col_e with isEqual
                                        self.count_handler[col_e_count] = 0

                                else:
                                    # / Add Data to Table count without math
                                    self.dataCount.append(
                                        {
                                            "row": countRow,
                                            "col": total_column,
                                            "color": isEqual,
                                            "data": f"{col_a}/{col_d}",
                                            "notice": isNoticeCount,
                                            "date": item_date,
                                            "color_value": col_d,
                                            "isDeleted": isDeleted,
                                        }
                                    )
                            # / End check col_c is first
                            else:
                                # / Add Data to Table count without math
                                self.dataCount.append(
                                    {
                                        "row": countRow,
                                        "col": total_column,
                                        "color": isEqual,
                                        "data": f"{col_a}/{col_d}",
                                        "notice": isNoticeCount,
                                        "date": item_date,
                                        "color_value": col_d,
                                        "isDeleted": isDeleted,
                                    }
                                )

                        else:
                            self.dataCount.append(
                                {
                                    "row": countRow,
                                    "col": total_column,
                                    "color": isEqual,
                                    "data": f"{col_a}/{col_d}",
                                    "notice": isNoticeCount,
                                    "color_value": col_d,
                                    "isDeleted": isDeleted,
                                }
                            )
                    if isEqual:
                        # / Reset Count col_d if isEqual
                        self.count_handler[dem_col_row] = 0

                    # / End check isFirst
                    total_column += 1

        # / filter data isDeleted
        old_dataCount = self.dataCount
        new_dataCount = [entry for entry in old_dataCount if not entry["isDeleted"]]
        self.dataCount = new_dataCount

        old_dataColor = self.dataColor
        new_dataColor = [entry for entry in old_dataColor if not entry["isDeleted"]]
        self.dataColor = new_dataColor

        old_dataColorM2 = self.dataColor2
        new_dataColorM2 = [entry for entry in old_dataColorM2 if not entry["isDeleted"]]
        self.dataColor2 = new_dataColorM2

        old_dataColorM3 = self.dataColor3
        new_dataColorM3 = [entry for entry in old_dataColorM3 if not entry["isDeleted"]]
        self.dataColor3 = new_dataColorM3

        old_dataColorM4 = self.dataColor4
        new_dataColorM4 = [entry for entry in old_dataColorM4 if not entry["isDeleted"]]
        self.dataColor4 = new_dataColorM4

        old_dataColorM5 = self.dataColor5
        new_dataColorM5 = [entry for entry in old_dataColorM5 if not entry["isDeleted"]]
        self.dataColor5 = new_dataColorM5

        old_dataColorM6 = self.dataColor6
        new_dataColorM6 = [entry for entry in old_dataColorM6 if not entry["isDeleted"]]
        self.dataColor6 = new_dataColorM6

        old_dataColorM7 = self.dataColor7
        new_dataColorM7 = [entry for entry in old_dataColorM7 if not entry["isDeleted"]]
        self.dataColor7 = new_dataColorM7

        old_dataColorM8 = self.dataColor8
        new_dataColorM8 = [entry for entry in old_dataColorM8 if not entry["isDeleted"]]
        self.dataColor8 = new_dataColorM8

        old_dataColorM9 = self.dataColor9
        new_dataColorM9 = [entry for entry in old_dataColorM9 if not entry["isDeleted"]]
        self.dataColor9 = new_dataColorM9

        old_dataColorM10 = self.dataColor10
        new_dataColorM10 = [
            entry for entry in old_dataColorM10 if not entry["isDeleted"]
        ]
        self.dataColor10 = new_dataColorM10

    def checkColor(self, value1, value2):
        for char in value1:
            if char in value2:
                return self.red
        return None

    def checkColorThong(self, value1, value2):
        for char in value1:
            if char in value2:
                return True
        return False

    def checkNotice(self, value1, notice1, notice2):
        if value1 >= notice1 and value1 <= notice2:
            return self.yellow
        else:
            return None

    def moveTableWithAction(self, data, ac):
        self.reload_color_item()

        if ac == "vbm1":
            action = data["actionM1"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_color)
            item = self.table_scroll_color.item(row, col)
            self.table_scroll_color.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m1")
            self.changeStatusBar("Bảng Màu 1", "Bảng Màu 1")
            return
        elif ac == "vbm2":
            action = data["actionM2"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM2)
            item = self.table_scroll_colorM2.item(row, col)
            self.table_scroll_colorM2.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m2")
            self.changeStatusBar("Bảng Màu 2", "Bảng Màu 2")
            # self.note_color_label.setText(self.note_color)
        elif ac == "vbm3":
            action = data["actionM3"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM3)
            item = self.table_scroll_colorM3.item(row, col)
            self.table_scroll_colorM3.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m3")
            self.changeStatusBar("Bảng Màu 3", "Bảng Màu 3")
        elif ac == "vbm4":
            action = data["actionM4"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM4)
            item = self.table_scroll_colorM4.item(row, col)
            self.table_scroll_colorM4.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m4")
            self.changeStatusBar("Bảng Màu 4", "Bảng Màu 4")
        elif ac == "vbm5":
            action = data["actionM5"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM5)
            item = self.table_scroll_colorM5.item(row, col)
            self.table_scroll_colorM5.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m5")
            self.changeStatusBar("Bảng Màu 5", "Bảng Màu 5")
        elif ac == "vbm6":
            action = data["actionM6"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM6)
            item = self.table_scroll_colorM6.item(row, col)
            self.table_scroll_colorM6.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m6")
            self.changeStatusBar("Bảng Màu 6", "Bảng Màu 6")
        elif ac == "vbm7":
            action = data["actionM7"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM7)
            item = self.table_scroll_colorM7.item(row, col)
            self.table_scroll_colorM7.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m7")
            self.changeStatusBar("Bảng Màu 7", "Bảng Màu 7")
        elif ac == "vbm8":
            action = data["actionM8"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM8)
            item = self.table_scroll_colorM8.item(row, col)
            self.table_scroll_colorM8.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m8")
            self.changeStatusBar("Bảng Màu 8", "Bảng Màu 8")
        elif ac == "vbm9":
            action = data["actionM9"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM9)
            item = self.table_scroll_colorM9.item(row, col)
            self.table_scroll_colorM9.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m9")
            self.changeStatusBar("Bảng Màu 9", "Bảng Màu 9")
        elif ac == "vbm10":
            action = data["actionM10"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_colorM10)
            item = self.table_scroll_colorM10.item(row, col)
            self.table_scroll_colorM10.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation("m10")
            self.changeStatusBar("Bảng Màu 10", "Bảng Màu 10")
        elif ac == "vbt":

            action = data["action"]
            row = action["row"]
            col = action["col"]
            isColor = action["isColor"]
            self.widget_main.setCurrentWidget(self.table_main_count)
            item = self.table_scroll_count.item(row, col)
            self.table_scroll_count.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "current": {
                    "item": data["item"],
                    "color": (
                        data["isColor"] if data["isColor"] is not None else self.normal
                    ),
                },
                "next": {
                    "item": item,
                    "color": isColor if isColor is not None else self.normal,
                },
            }
            self.setHighlight(new_data)
            # / Config status bar
            self.renderNavigation()
            self.changeStatusBar("Bảng Tính", "Bảng Tính")
            # self.note_color_label.setText("")
        else:
            thong = data["thong"]
            row_thong = thong["row"]
            col_thong = thong["col"]
            self.widget_main.setCurrentWidget(self.table_main_thong)
            item = self.table_main_thong.item(row_thong, col_thong)
            self.table_main_thong.scrollToItem(
                item, hint=QTableWidget.ScrollHint.PositionAtCenter
            )
            new_data = {
                "col": col_thong,
                "value": thong["col_a"],
                "isCol_a": thong["isCol_a"],
            }
            self.setHighlight_Thong(new_data)
            # / Config status bar
            self.renderNavigation()
            self.changeStatusBar("Bảng Thông", "Bảng Thông")
        return

    # TODO Add-on: GUI Thong Table

    def render_table_thong(self):
        """
        TODO Gui thong table
        !DES: Make a Thong table with features will show the item had result after render
        !: and highlight them into table.
        ? Features available:
        ? 1. Swap Button Notice to Thong Table
        ? 2. Swap between item in table color and Thong Table
        """
        # / Config func
        self.start_col = 1
        self.value_col = 1
        number_change = self.ban_info["meta"]["number"]
        thong_info = self.ban_info["thong"]
        stt = self.thong_db["stt"][number_change]
        data_value = self.thong_db["data"]
        thong_data = self.thong_info

        # / Create widget main thong table
        self.table_main_thong = QTableWidget()
        self.widget_main.addWidget(self.table_main_thong)

        # / Config table
        value_thong = thong_info["value"]
        thong_ranges = value_thong[1] - value_thong[0] + 1
        colCount = thong_ranges + 5  #! 5 is the number of columns outside
        rowCount = 121
        # / Column
        self.table_main_thong.setColumnCount(colCount)
        self.table_main_thong.setRowCount(rowCount)

        # / Config Font
        self.table_main_thong.setFont(self.font)
        self.table_main_thong.horizontalHeader().setFont(self.font)
        self.table_main_thong.verticalHeader().setFont(self.font)

        self.table_main_thong.setStyleSheet(
            """
                QTableView {
                    gridline-color: black;
                }
            """
        )

        self.table_main_thong.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_main_thong.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_main_thong.horizontalScrollBar().valueChanged.connect(
            self.freeze_col_stt
        )
        self.table_main_thong.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_main_thong.setSelectionMode(
            QTableWidget.SelectionMode.MultiSelection
        )

        # / config header and render header

        for i in range(thong_ranges):
            if i == 0:
                item_stt = QTableWidgetItem(f"STT")
                item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setHorizontalHeaderItem(0, item_stt)

                item_zero = QTableWidgetItem(f"Cột 0")
                item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setHorizontalHeaderItem(1, item_zero)

                item_a = QTableWidgetItem(f"A")
                item_a.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setHorizontalHeaderItem(2, item_a)

                item_b = QTableWidgetItem(f"B")
                item_b.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setHorizontalHeaderItem(3, item_b)

                item_c = QTableWidgetItem(f"C")
                item_c.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setHorizontalHeaderItem(4, item_c)

                item = QTableWidgetItem(f"T.{i+ value_thong[0]}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setHorizontalHeaderItem(i + 5, item)
            else:
                item = QTableWidgetItem(f"T.{i + value_thong[0]}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setHorizontalHeaderItem(i + 5, item)
        # / render rows
        # ? Render Rows STT First
        for i in range(rowCount):
            zero_value = f"{i:02}."
            item_zero = QTableWidgetItem(f"{zero_value}")
            item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main_thong.setItem(i, 0, item_zero)

            stt_value = stt[i]
            item = QTableWidgetItem(f"{stt_value}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(self.stt_highlight)
            self.table_main_thong.setItem(i, 1, item)

        # ? Change data value with number change
        if number_change != 0:
            data_value_new = map(
                lambda values: list(
                    map(lambda value: TachVaGhep(number_change, value), values)
                ),
                data_value,
            )
            data_value = list(data_value_new)
        # ? Render Rows Custom First
        for i in range(len(data_value)):
            value_col = data_value[i]
            for j in range(121):
                item = QTableWidgetItem(f"{value_col[j]}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setItem(j, i + 2, item)
                if i + 2 == 2 or i + 2 == 4:
                    item.setBackground(self.stt_highlight)
        # ? Render Rows
        for i in range(thong_ranges):
            thong_row = thong_data[i + value_thong[0] - 1]
            for j in range(121):
                item = QTableWidgetItem(f"{thong_row[j]}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main_thong.setItem(j, i + 5, item)

    def freeze_col_stt(self, value):
        if value >= self.start_col:
            self.table_main_thong.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value
        elif value < self.start_col:
            value = self.start_col
            self.table_main_thong.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value

    def changeStatusBar(self, status, next):
        old_title = self.title.text()
        for text in sorted(
            [
                "Bảng Màu 10",
                "Bảng Màu 9",
                "Bảng Màu 8",
                "Bảng Màu 7",
                "Bảng Màu 6",
                "Bảng Màu 5",
                "Bảng Màu 4",
                "Bảng Màu 3",
                "Bảng Màu 2",
                "Bảng Màu 1",
                "Bảng Tính",
            ],
            key=len,
            reverse=True,
        ):
            if text in old_title:
                new_title = old_title.replace(text, status)
                self.title.setText(new_title)
                return

    def reload_widget(self):
        self.handlerData()
        self.renderNavigation()
        self.updateTableCount()
        for i in range(10):
            data = self.ban_info["meta"]["tables"][i]
            if data["enable"]:
                self.start_render_tables_row(i)

    def find_row_thong_with_col_a(self, col_a, thong_data):
        for i in range(len(thong_data)):
            val = thong_data[i]
            if str(col_a) in str(val):
                return i

    def show_loading_screen(self):
        self.loadingScreen.show()
        self.loadingScreen.start()

    def hide_loading_screen(self):
        self.loadingScreen.stop()
        self.loadingScreen.hide()

    def updateWidget(self, widgets):
        self.hide_loading_screen()
        # sleep(0.5)
        for widget in widgets:
            widget()
            # sleep(0.5)

    # TODO Handler Move

    def move_to_right(self, dialog):
        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().geometry()

        # Set fixed size for the dialog
        dialog_width = 1300
        dialog_height = 1050

        # Calculate the x and y position to move the dialog to the right
        x_pos = (
            screen_geometry.width() - dialog_width - 20
        )  # 20px padding from right edge
        y_pos = (screen_geometry.height() - dialog_height) // 2  # Center vertically

        # Move and set the dialog size
        dialog.setGeometry(x_pos, y_pos, dialog_width, dialog_height)

    def move_to_center(self, dialog):
        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().geometry()

        # Set fixed size for the dialog
        dialog_width = 1200
        dialog_height = 1050

        # Calculate the x and y position to move the dialog to the right
        x_pos = (
            screen_geometry.width() - dialog_width
        ) // 2  # 20px padding from right edge
        y_pos = (screen_geometry.height() - dialog_height) // 2  # Center vertically

        # Move and set the dialog size
        dialog.setGeometry(x_pos, y_pos, dialog_width, dialog_height)

    # TODO Handler Color Table
    # / M4 start
    def handler_data_m4(
        self,
        i,
        t,
        col_e_m3,
        notice_colorM4,
        value1_4,
        value2_4,
        countRow,
        col_a,
        thong_range_1,
        stt_cot,
        col_d,
        col_t,
        col_e,
        col_e_m2,
        isEqual,
        total_column,
        isNoticeCount,
        col_color,
        col_color_m2,
        col_color_m3,
        isNoticeColor,
        isNoticeColor_m2,
        isNoticeColor_m3,
        item_date,
        col_e4,
        row_thong,
        isDeleted,
    ):
        math_count_handler_m4 = f"{col_e_m3}:{i}:_color_m4"
        if not math_count_handler_m4 in self.count_handler:
            self.count_handler[math_count_handler_m4] = 1
        else:
            self.count_handler[math_count_handler_m4] += 1

        # / End check col_stt table count
        stt_count_with_d_m4 = self.count_handler[
            math_count_handler_m4
        ]  # So thu tu cua so dem
        number_of_col_d = self.ban_info["meta"]["tables"][3]["col_d"][col_e_m3 - 1]
        if stt_count_with_d_m4 <= number_of_col_d:
            # / Start count color with col_e
            col_e_count_m4 = f"{col_e_m3}:{stt_count_with_d_m4}:col_e_m4"
            if not col_e_count_m4 in self.count_handler:
                self.count_handler[col_e_count_m4] = 1
            else:
                self.count_handler[col_e_count_m4] += 1
            col_e_m4 = self.count_handler[col_e_count_m4]  # so dem bang mau
            isNoticeColor_m4 = self.checkNotice(
                col_e_m4,
                notice_colorM4[0],
                notice_colorM4[1],
            )
            find_null_color_m4 = 0
            find_stt_color_m4 = stt_count_with_d_m4 - 1
            find_next_color_m4 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][3]["col_d"],
                col_e_m3 - value1_4,
                value1_4 - 1,
                value2_4,
            )
            col_color_m4 = (
                find_next_color_m4 + find_null_color_m4 + find_stt_color_m4
            )  # vi tri col cua item bang mau

            if isEqual:
                self.count_handler[col_e_count_m4] = 0
            # / Add data to table color 4
            dataColorM4 = {
                "row": countRow,
                "col": col_color_m4,
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color,
                    "isColor": isNoticeColor,
                } if self.ban_info["meta"]["tables"][0]["enable"] else None,
                "actionM2": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m2,
                    "isColor": isNoticeColor_m2,
                } if self.ban_info["meta"]["tables"][1]["enable"] else None,
                "actionM3": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m3,
                    "isColor": isNoticeColor_m3,
                } if self.ban_info["meta"]["tables"][2]["enable"] else None,
                "notice": isNoticeColor_m4,
                "date": item_date,
                "color_value": col_e4,
                "col_d": col_e_m3,
                "thong": {
                    "row": row_thong,
                    "col": t + 5,
                    "col_a": (col_t if col_t != "?" else col_a),
                    "isCol_a": (False if col_t != "?" else True),
                },
                "isDeleted": isDeleted,
            }
            return {
                "m4": dataColorM4,
                "object": {
                    "col_e_m4": col_e_m4,
                    "isNoticeColor_m4": isNoticeColor_m4,
                    "col_color_m4": col_color_m4,
                },
            }

    # / M5 start
    def handler_data_m5(
        self,
        i,
        t,
        col_e_m3,
        notice_colorM5,
        value1_5,
        value2_5,
        countRow,
        col_a,
        thong_range_1,
        stt_cot,
        col_d,
        col_t,
        col_e,
        col_e_m2,
        col_e_m4,
        isEqual,
        total_column,
        isNoticeCount,
        col_color,
        col_color_m2,
        col_color_m3,
        col_color_m4,
        isNoticeColor,
        isNoticeColor_m2,
        isNoticeColor_m3,
        isNoticeColor_m4,
        item_date,
        col_e5,
        row_thong,
        isDeleted,
    ):
        math_count_handler_m5 = f"{col_e_m4}:{i}:_color_m5"
        if not math_count_handler_m5 in self.count_handler:
            self.count_handler[math_count_handler_m5] = 1
        else:
            self.count_handler[math_count_handler_m5] += 1

        # / End check col_stt table count
        stt_count_with_d_m5 = self.count_handler[
            math_count_handler_m5
        ]  # So thu tu cua so dem
        number_of_col_d = self.ban_info["meta"]["tables"][4]["col_d"][col_e_m4 - 1]
        if stt_count_with_d_m5 <= number_of_col_d:
            # / Start count color with col_e
            col_e_count_m5 = f"{col_e_m4}:{stt_count_with_d_m5}:col_e_m5"
            if not col_e_count_m5 in self.count_handler:
                self.count_handler[col_e_count_m5] = 1
            else:
                self.count_handler[col_e_count_m5] += 1
            col_e_m5 = self.count_handler[col_e_count_m5]  # so dem bang mau
            isNoticeColor_m5 = self.checkNotice(
                col_e_m5,
                notice_colorM5[0],
                notice_colorM5[1],
            )
            find_null_color_m5 = 0
            find_stt_color_m5 = stt_count_with_d_m5 - 1
            find_next_color_m5 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][4]["col_d"],
                col_e_m4 - value1_5,
                value1_5 - 1,
                value2_5,
            )
            col_color_m5 = (
                find_next_color_m5 + find_null_color_m5 + find_stt_color_m5
            )  # vi tri col cua item bang mau

            if isEqual:
                self.count_handler[col_e_count_m5] = 0
            # / Add data to table color 5
            dataColorM5 = {
                "row": countRow,
                "col": col_color_m5,
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color,
                    "isColor": isNoticeColor,
                } if self.ban_info["meta"]["tables"][0]["enable"] else None,
                "actionM2": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m2,
                    "isColor": isNoticeColor_m2,
                }if self.ban_info["meta"]["tables"][1]["enable"] else None,
                "actionM3": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m3,
                    "isColor": isNoticeColor_m3,
                }if self.ban_info["meta"]["tables"][2]["enable"] else None,
                "actionM4": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m4,
                    "isColor": isNoticeColor_m4,
                }if self.ban_info["meta"]["tables"][3]["enable"] else None,
                "notice": isNoticeColor_m5,
                "date": item_date,
                "color_value": col_e5,
                "col_d": col_e_m4,
                "thong": {
                    "row": row_thong,
                    "col": t + 5,
                    "col_a": (col_t if col_t != "?" else col_a),
                    "isCol_a": (False if col_t != "?" else True),
                },
                "isDeleted": isDeleted,
            }
            return {
                "m5": dataColorM5,
                "object": {
                    "col_e_m5": col_e_m5,
                    "isNoticeColor_m5": isNoticeColor_m5,
                    "col_color_m5": col_color_m5,
                },
            }

    # / M6 start
    def handler_data_m6(
        self,
        i,
        t,
        col_e_m3,
        notice_colorM6,
        value1_6,
        value2_6,
        countRow,
        col_a,
        thong_range_1,
        stt_cot,
        col_d,
        col_t,
        col_e,
        col_e_m2,
        col_e_m4,
        col_e_m5,
        isEqual,
        total_column,
        isNoticeCount,
        col_color,
        col_color_m2,
        col_color_m3,
        col_color_m4,
        col_color_m5,
        isNoticeColor,
        isNoticeColor_m2,
        isNoticeColor_m3,
        isNoticeColor_m4,
        isNoticeColor_m5,
        item_date,
        col_e6,
        row_thong,
        isDeleted,
    ):
        math_count_handler_m6 = f"{col_e_m5}:{i}:_color_m6"
        if not math_count_handler_m6 in self.count_handler:
            self.count_handler[math_count_handler_m6] = 1
        else:
            self.count_handler[math_count_handler_m6] += 1

        # / End check col_stt table count
        stt_count_with_d_m6 = self.count_handler[
            math_count_handler_m6
        ]  # So thu tu cua so dem
        number_of_col_d = self.ban_info["meta"]["tables"][5]["col_d"][col_e_m5 - 1]
        if stt_count_with_d_m6 <= number_of_col_d:
            # / Start count color with col_e
            col_e_count_m6 = f"{col_e_m5}:{stt_count_with_d_m6}:col_e_m6"
            if not col_e_count_m6 in self.count_handler:
                self.count_handler[col_e_count_m6] = 1
            else:
                self.count_handler[col_e_count_m6] += 1
            col_e_m6 = self.count_handler[col_e_count_m6]  # so dem bang mau
            isNoticeColor_m6 = self.checkNotice(
                col_e_m6,
                notice_colorM6[0],
                notice_colorM6[1],
            )
            find_null_color_m6 = 0
            find_stt_color_m6 = stt_count_with_d_m6 - 1
            find_next_color_m6 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][5]["col_d"],
                col_e_m5 - value1_6,
                value1_6 - 1,
                value2_6,
            )
            col_color_m6 = (
                find_next_color_m6 + find_null_color_m6 + find_stt_color_m6
            )  # vi tri col cua item bang mau

            if isEqual:
                self.count_handler[col_e_count_m6] = 0
            # / Add data to table color 6
            dataColorM6 = {
                "row": countRow,
                "col": col_color_m6,
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color,
                    "isColor": isNoticeColor,
                } if self.ban_info["meta"]["tables"][0]["enable"] else None,
                "actionM2": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m2,
                    "isColor": isNoticeColor_m2,
                }if self.ban_info["meta"]["tables"][1]["enable"] else None,
                "actionM3": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m3,
                    "isColor": isNoticeColor_m3,
                }if self.ban_info["meta"]["tables"][2]["enable"] else None,
                "actionM4": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m4,
                    "isColor": isNoticeColor_m4,
                }if self.ban_info["meta"]["tables"][3]["enable"] else None,
                "actionM5": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m5,
                    "isColor": isNoticeColor_m5,
                }if self.ban_info["meta"]["tables"][4]["enable"] else None,
                "notice": isNoticeColor_m6,
                "date": item_date,
                "color_value": col_e6,
                "col_d": col_e_m5,
                "thong": {
                    "row": row_thong,
                    "col": t + 6,
                    "col_a": (col_t if col_t != "?" else col_a),
                    "isCol_a": (False if col_t != "?" else True),
                },
                "isDeleted": isDeleted,
            }
            return {
                "m6": dataColorM6,
                "object": {
                    "col_e_m6": col_e_m6,
                    "isNoticeColor_m6": isNoticeColor_m6,
                    "col_color_m6": col_color_m6,
                },
            }

    # / M7 start
    def handler_data_m7(
        self,
        i,
        t,
        notice_colorM7,
        value1_7,
        value2_7,
        countRow,
        col_a,
        thong_range_1,
        stt_cot,
        col_d,
        col_t,
        col_e,
        col_e_m2,
        col_e_m3,
        col_e_m4,
        col_e_m5,
        col_e_m6,
        isEqual,
        total_column,
        isNoticeCount,
        col_color,
        col_color_m2,
        col_color_m3,
        col_color_m4,
        col_color_m5,
        col_color_m6,
        isNoticeColor,
        isNoticeColor_m2,
        isNoticeColor_m3,
        isNoticeColor_m4,
        isNoticeColor_m5,
        isNoticeColor_m6,
        item_date,
        col_e7,
        row_thong,
        isDeleted,
    ):
        math_count_handler_m7 = f"{col_e_m6}:{i}:_color_m7"
        if not math_count_handler_m7 in self.count_handler:
            self.count_handler[math_count_handler_m7] = 1
        else:
            self.count_handler[math_count_handler_m7] += 1

        # / End check col_stt table count
        stt_count_with_d_m7 = self.count_handler[
            math_count_handler_m7
        ]  # So thu tu cua so dem
        number_of_col_d = self.ban_info["meta"]["tables"][6]["col_d"][col_e_m6 - 1]
        if stt_count_with_d_m7 <= number_of_col_d:
            # / Start count color with col_e
            col_e_count_m7 = f"{col_e_m6}:{stt_count_with_d_m7}:col_e_m7"
            if not col_e_count_m7 in self.count_handler:
                self.count_handler[col_e_count_m7] = 1
            else:
                self.count_handler[col_e_count_m7] += 1
            col_e_m7 = self.count_handler[col_e_count_m7]  # so dem bang mau
            isNoticeColor_m7 = self.checkNotice(
                col_e_m7,
                notice_colorM7[0],
                notice_colorM7[1],
            )
            find_null_color_m7 = 0
            find_stt_color_m7 = stt_count_with_d_m7 - 1
            find_next_color_m7 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][6]["col_d"],
                col_e_m6 - value1_7,
                value1_7 - 1,
                value2_7,
            )
            col_color_m7 = (
                find_next_color_m7 + find_null_color_m7 + find_stt_color_m7
            )  # vi tri col cua item bang mau

            if isEqual:
                self.count_handler[col_e_count_m7] = 0
            # / Add data to table color 6
            dataColorM7 = {
                "row": countRow,
                "col": col_color_m7,
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color,
                    "isColor": isNoticeColor,
                } if self.ban_info["meta"]["tables"][0]["enable"] else None,
                "actionM2": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m2,
                    "isColor": isNoticeColor_m2,
                }if self.ban_info["meta"]["tables"][1]["enable"] else None,
                "actionM3": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m3,
                    "isColor": isNoticeColor_m3,
                }if self.ban_info["meta"]["tables"][2]["enable"] else None,
                "actionM4": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m4,
                    "isColor": isNoticeColor_m4,
                }if self.ban_info["meta"]["tables"][3]["enable"] else None,
                "actionM5": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m5,
                    "isColor": isNoticeColor_m5,
                }if self.ban_info["meta"]["tables"][4]["enable"] else None,
                "actionM6": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m6,
                    "isColor": isNoticeColor_m6,
                }if self.ban_info["meta"]["tables"][5]["enable"] else None,
                "notice": isNoticeColor_m7,
                "date": item_date,
                "color_value": col_e7,
                "col_d": col_e_m6,
                "thong": {
                    "row": row_thong,
                    "col": t + 6,
                    "col_a": (col_t if col_t != "?" else col_a),
                    "isCol_a": (False if col_t != "?" else True),
                },
                "isDeleted": isDeleted,
            }
            return {
                "m7": dataColorM7,
                "object": {
                    "col_e_m7": col_e_m7,
                    "isNoticeColor_m7": isNoticeColor_m7,
                    "col_color_m7": col_color_m7,
                },
            }

    # / M8 start
    def handler_data_m8(
        self,
        i,
        t,
        col_e_m3,
        notice_colorM8,
        value1_8,
        value2_8,
        countRow,
        col_a,
        thong_range_1,
        stt_cot,
        col_d,
        col_t,
        col_e,
        col_e_m2,
        col_e_m4,
        col_e_m5,
        col_e_m6,
        col_e_m7,
        isEqual,
        total_column,
        isNoticeCount,
        col_color,
        col_color_m2,
        col_color_m3,
        col_color_m4,
        col_color_m5,
        col_color_m6,
        col_color_m7,
        isNoticeColor,
        isNoticeColor_m2,
        isNoticeColor_m3,
        isNoticeColor_m4,
        isNoticeColor_m5,
        isNoticeColor_m6,
        isNoticeColor_m7,
        item_date,
        col_e8,
        row_thong,
        isDeleted,
    ):
        math_count_handler_m8 = f"{col_e_m7}:{i}:_color_m8"
        if not math_count_handler_m8 in self.count_handler:
            self.count_handler[math_count_handler_m8] = 1
        else:
            self.count_handler[math_count_handler_m8] += 1

        # / End check col_stt table count
        stt_count_with_d_m8 = self.count_handler[
            math_count_handler_m8
        ]  # So thu tu cua so dem
        number_of_col_d = self.ban_info["meta"]["tables"][7]["col_d"][col_e_m7 - 1]
        if stt_count_with_d_m8 <= number_of_col_d:
            # / Start count color with col_e
            col_e_count_m8 = f"{col_e_m7}:{stt_count_with_d_m8}:col_e_m8"
            if not col_e_count_m8 in self.count_handler:
                self.count_handler[col_e_count_m8] = 1
            else:
                self.count_handler[col_e_count_m8] += 1
            col_e_m8 = self.count_handler[col_e_count_m8]  # so dem bang mau
            isNoticeColor_m8 = self.checkNotice(
                col_e_m8,
                notice_colorM8[0],
                notice_colorM8[1],
            )
            find_null_color_m8 = 0
            find_stt_color_m8 = stt_count_with_d_m8 - 1
            find_next_color_m8 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][7]["col_d"],
                col_e_m7 - value1_8,
                value1_8 - 1,
                value2_8,
            )
            col_color_m8 = (
                find_next_color_m8 + find_null_color_m8 + find_stt_color_m8
            )  # vi tri col cua item bang mau

            if isEqual:
                self.count_handler[col_e_count_m8] = 0
            # / Add data to table color 6
            dataColorM8 = {
                "row": countRow,
                "col": col_color_m8,
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}/{col_e_m8}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color,
                    "isColor": isNoticeColor,
                }if self.ban_info["meta"]["tables"][0]["enable"] else None,
                "actionM2": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m2,
                    "isColor": isNoticeColor_m2,
                }if self.ban_info["meta"]["tables"][1]["enable"] else None,
                "actionM3": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m3,
                    "isColor": isNoticeColor_m3,
                }if self.ban_info["meta"]["tables"][2]["enable"] else None,
                "actionM4": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m4,
                    "isColor": isNoticeColor_m4,
                }if self.ban_info["meta"]["tables"][3]["enable"] else None,
                "actionM5": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m5,
                    "isColor": isNoticeColor_m5,
                }if self.ban_info["meta"]["tables"][4]["enable"] else None,
                "actionM6": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m6,
                    "isColor": isNoticeColor_m6,
                }if self.ban_info["meta"]["tables"][5]["enable"] else None,
                "actionM7": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m7,
                    "isColor": isNoticeColor_m7,
                }if self.ban_info["meta"]["tables"][6]["enable"] else None,
                "notice": isNoticeColor_m8,
                "date": item_date,
                "color_value": col_e8,
                "col_d": col_e_m7,
                "thong": {
                    "row": row_thong,
                    "col": t + 6,
                    "col_a": (col_t if col_t != "?" else col_a),
                    "isCol_a": (False if col_t != "?" else True),
                },
                "isDeleted": isDeleted,
            }
            return {
                "m8": dataColorM8,
                "object": {
                    "col_e_m8": col_e_m8,
                    "isNoticeColor_m8": isNoticeColor_m8,
                    "col_color_m8": col_color_m8,
                },
            }

    # / M9 start
    def handler_data_m9(
        self,
        i,
        t,
        col_e_m3,
        notice_colorM9,
        value1_9,
        value2_9,
        countRow,
        col_a,
        thong_range_1,
        stt_cot,
        col_d,
        col_t,
        col_e,
        col_e_m2,
        col_e_m4,
        col_e_m5,
        col_e_m6,
        col_e_m7,
        col_e_m8,
        isEqual,
        total_column,
        isNoticeCount,
        col_color,
        col_color_m2,
        col_color_m3,
        col_color_m4,
        col_color_m5,
        col_color_m6,
        col_color_m7,
        col_color_m8,
        isNoticeColor,
        isNoticeColor_m2,
        isNoticeColor_m3,
        isNoticeColor_m4,
        isNoticeColor_m5,
        isNoticeColor_m6,
        isNoticeColor_m7,
        isNoticeColor_m8,
        item_date,
        col_e9,
        row_thong,
        isDeleted,
    ):
        math_count_handler_m9 = f"{col_e_m8}:{i}:_color_m9"
        if not math_count_handler_m9 in self.count_handler:
            self.count_handler[math_count_handler_m9] = 1
        else:
            self.count_handler[math_count_handler_m9] += 1

        # / End check col_stt table count
        stt_count_with_d_m9 = self.count_handler[
            math_count_handler_m9
        ]  # So thu tu cua so dem
        number_of_col_d = self.ban_info["meta"]["tables"][8]["col_d"][col_e_m8 - 1]
        if stt_count_with_d_m9 <= number_of_col_d:
            # / Start count color with col_e
            col_e_count_m9 = f"{col_e_m8}:{stt_count_with_d_m9}:col_e_m9"
            if not col_e_count_m9 in self.count_handler:
                self.count_handler[col_e_count_m9] = 1
            else:
                self.count_handler[col_e_count_m9] += 1
            col_e_m9 = self.count_handler[col_e_count_m9]  # so dem bang mau
            isNoticeColor_m9 = self.checkNotice(
                col_e_m9,
                notice_colorM9[0],
                notice_colorM9[1],
            )
            find_null_color_m9 = 0
            find_stt_color_m9 = stt_count_with_d_m9 - 1
            find_next_color_m9 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][8]["col_d"],
                col_e_m8 - value1_9,
                value1_9 - 1,
                value2_9,
            )
            col_color_m9 = (
                find_next_color_m9 + find_null_color_m9 + find_stt_color_m9
            )  # vi tri col cua item bang mau

            if isEqual:
                self.count_handler[col_e_count_m9] = 0
            # / Add data to table color 6
            dataColorM9 = {
                "row": countRow,
                "col": col_color_m9,
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}/{col_e_m8}/{col_e_m9}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                
                "actionM1": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color,
                    "isColor": isNoticeColor,
                }if self.ban_info["meta"]["tables"][0]["enable"] else None,
                "actionM2": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m2,
                    "isColor": isNoticeColor_m2,
                }if self.ban_info["meta"]["tables"][1]["enable"] else None,
                "actionM3": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m3,
                    "isColor": isNoticeColor_m3,
                }if self.ban_info["meta"]["tables"][2]["enable"] else None,
                "actionM4": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m4,
                    "isColor": isNoticeColor_m4,
                }if self.ban_info["meta"]["tables"][3]["enable"] else None,
                "actionM5": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m5,
                    "isColor": isNoticeColor_m5,
                }if self.ban_info["meta"]["tables"][4]["enable"] else None,
                "actionM6": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m6,
                    "isColor": isNoticeColor_m6,
                }if self.ban_info["meta"]["tables"][5]["enable"] else None,
                "actionM7": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m7,
                    "isColor": isNoticeColor_m7,
                }if self.ban_info["meta"]["tables"][6]["enable"] else None,
                "actionM8": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m8,
                    "isColor": isNoticeColor_m8,
                }if self.ban_info["meta"]["tables"][7]["enable"] else None,
                "notice": isNoticeColor_m9,
                "date": item_date,
                "color_value": col_e9,
                "col_d": col_e_m8,
                "thong": {
                    "row": row_thong,
                    "col": t + 6,
                    "col_a": (col_t if col_t != "?" else col_a),
                    "isCol_a": (False if col_t != "?" else True),
                },
                "isDeleted": isDeleted,
            }
            return {
                "m9": dataColorM9,
                "object": {
                    "col_e_m9": col_e_m9,
                    "isNoticeColor_m9": isNoticeColor_m9,
                    "col_color_m9": col_color_m9,
                },
            }

    # / M10 start
    def handler_data_m10(
        self,
        i,
        t,
        col_e_m3,
        notice_colorM10,
        value1_10,
        value2_10,
        countRow,
        col_a,
        thong_range_1,
        stt_cot,
        col_d,
        col_t,
        col_e,
        col_e_m2,
        col_e_m4,
        col_e_m5,
        col_e_m6,
        col_e_m7,
        col_e_m8,
        col_e_m9,
        isEqual,
        total_column,
        isNoticeCount,
        col_color,
        col_color_m2,
        col_color_m3,
        col_color_m4,
        col_color_m5,
        col_color_m6,
        col_color_m7,
        col_color_m8,
        col_color_m9,
        isNoticeColor,
        isNoticeColor_m2,
        isNoticeColor_m3,
        isNoticeColor_m4,
        isNoticeColor_m5,
        isNoticeColor_m6,
        isNoticeColor_m7,
        isNoticeColor_m8,
        isNoticeColor_m9,
        item_date,
        col_e10,
        row_thong,
        isDeleted,
    ):
        math_count_handler_m10 = f"{col_e_m9}:{i}:_color_m10"
        if not math_count_handler_m10 in self.count_handler:
            self.count_handler[math_count_handler_m10] = 1
        else:
            self.count_handler[math_count_handler_m10] += 1

        # / End check col_stt table count
        stt_count_with_d_m10 = self.count_handler[
            math_count_handler_m10
        ]  # So thu tu cua so dem
        number_of_col_d = self.ban_info["meta"]["tables"][9]["col_d"][col_e_m9 - 1]
        if stt_count_with_d_m10 <= number_of_col_d:
            # / Start count color with col_e
            col_e_count_m10 = f"{col_e_m9}:{stt_count_with_d_m10}:col_e_m10"
            if not col_e_count_m10 in self.count_handler:
                self.count_handler[col_e_count_m10] = 1
            else:
                self.count_handler[col_e_count_m10] += 1
            col_e_m10 = self.count_handler[col_e_count_m10]  # so dem bang mau
            isNoticeColor_m10 = self.checkNotice(
                col_e_m10,
                notice_colorM10[0],
                notice_colorM10[1],
            )
            find_null_color_m10 = 0
            find_stt_color_m10 = stt_count_with_d_m10 - 1
            find_next_color_m10 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][9]["col_d"],
                col_e_m8 - value1_10,
                value1_10 - 1,
                value2_10,
            )
            col_color_m10 = (
                find_next_color_m10 + find_null_color_m10 + find_stt_color_m10
            )  # vi tri col cua item bang mau

            if isEqual:
                self.count_handler[col_e_count_m10] = 0
            # / Add data to table color 6
            dataColorM10 = {
                "row": countRow,
                "col": col_color_m10,
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}/{col_e_m8}/{col_e_m9}/{col_e_m10}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                 "actionM1": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color,
                    "isColor": isNoticeColor,
                }if self.ban_info["meta"]["tables"][0]["enable"] else None,
                "actionM2": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m2,
                    "isColor": isNoticeColor_m2,
                }if self.ban_info["meta"]["tables"][1]["enable"] else None,
                "actionM3": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m3,
                    "isColor": isNoticeColor_m3,
                }if self.ban_info["meta"]["tables"][2]["enable"] else None,
                "actionM4": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m4,
                    "isColor": isNoticeColor_m4,
                }if self.ban_info["meta"]["tables"][3]["enable"] else None,
                "actionM5": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m5,
                    "isColor": isNoticeColor_m5,
                }if self.ban_info["meta"]["tables"][4]["enable"] else None,
                "actionM6": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m6,
                    "isColor": isNoticeColor_m6,
                }if self.ban_info["meta"]["tables"][5]["enable"] else None,
                "actionM7": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m7,
                    "isColor": isNoticeColor_m7,
                }if self.ban_info["meta"]["tables"][6]["enable"] else None,
                "actionM8": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m8,
                    "isColor": isNoticeColor_m8,
                }if self.ban_info["meta"]["tables"][7]["enable"] else None,
                "actionM9": {
                    "name": "color",
                    "row": countRow,
                    "col": col_color_m9,
                    "isColor": isNoticeColor_m9,
                }if self.ban_info["meta"]["tables"][8]["enable"] else None,
                "notice": isNoticeColor_m10,
                "date": item_date,
                "color_value": col_e10,
                "col_d": col_e_m9,
                "thong": {
                    "row": row_thong,
                    "col": t + 6,
                    "col_a": (col_t if col_t != "?" else col_a),
                    "isCol_a": (False if col_t != "?" else True),
                },
                "isDeleted": isDeleted,
            }
            return {
                "m10": dataColorM10,
                "object": {
                    "col_e_m10": col_e_m10,
                    "isNoticeColor_m10": isNoticeColor_m10,
                    "col_color_m10": col_color_m10,
                },
            }

    def start_render_tables(self, index):
        match index:
            case 0:
                self.renderTableColor()
            case 1:
                self.renderTableColorM2()
            case 2:
                self.renderTableColorM3()
            case 3:
                self.renderTableColorM4()
            case 4:
                self.renderTableColorM5()
            case 5:
                self.renderTableColorM6()
            case 6:
                self.renderTableColorM7()
            case 7:
                self.renderTableColorM8()
            case 8:
                self.renderTableColorM9()
            case 9:
                self.renderTableColorM10()
            case _:
                pass

    def find_column_by_index(self, arr, target_index, start, end):
        total_columns = 0

        # Iterate through the array and calculate the column placement
        for i, value in enumerate(arr[start:end]):
            # Check if we've reached the target index
            if i == target_index:
                return total_columns

            # Add the value to the total columns
            total_columns += value

            # After each value, add 1 (except for the last index)
            if i != len(arr[start:end]) - 1:
                total_columns += 1

        # If index is out of range
        return -1

    def start_render_tables_row(self, index):
        match index:
            case 0:
                self.updateTableColor()
            case 1:
                self.updateTableColorM2()
            case 2:
                self.updateTableColorM3()
            case 3:
                self.updateTableColorM4()
            case 4:
                self.updateTableColorM5()
            case 5:
                self.updateTableColorM6()
            case 6:
                self.updateTableColorM7()
            case 7:
                self.updateTableColorM8()
            case 8:
                self.updateTableColorM9()
            case 9:
                self.updateTableColorM10()
            case _:
                pass

    def start_clear_tables_row(self, index):
        match index:
            case 0:
                self.table_scroll_color.clearSelection()
            case 1:
                self.table_scroll_colorM2.clearSelection()
            case 2:
                self.table_scroll_colorM3.clearSelection()
            case 3:
                self.table_scroll_colorM4.clearSelection()
            case 4:
                self.table_scroll_colorM5.clearSelection()
            case 5:
                self.table_scroll_colorM6.clearSelection()
            case 6:
                self.table_scroll_colorM7.clearSelection()
            case 7:
                self.table_scroll_colorM8.clearSelection()
            case 8:
                self.table_scroll_colorM9.clearSelection()
            case 9:
                self.table_scroll_colorM10.clearSelection()
            case _:
                pass
