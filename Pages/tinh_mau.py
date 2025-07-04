import bisect
import json
import os
from functools import partial
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QDate, QTimer, QRect
from PySide6.QtGui import QAction, QColor, QCursor, QFont, QIcon, Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDateEdit,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from Controller.handler import (
    TachVaGhep,
    deleteFromToBan,
    deleteRowBan,
    updateBanInsert,
    convert_string_format,
    updateThongInsert,convert_string_to_type_count
)
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread
from Pages.components.path import Path
from Pages.components.setting import SettingTable
from Pages.components.stylesheet import (
    Font,
    Note,
    SendMessage,
    css_button_cancel,
    css_button_checkbox,
    css_button_normal,
    css_button_notice,
    css_button_submit,
    css_button_view,
    css_customs_table,
    css_input,
    css_lable,
    css_table_header,
    css_title,css_button_start
)
from time import sleep
import xlwings as xw
import pandas as pd
from Pages.components.tableFormatter import TableFormatter



css_custom_btn_insert = """
    QPushButton {
        padding: 10px;
        border-radius: 8px; 
        font-size: 24px;
        line-height: 32px;
        font-weight: 600; 
        background-color: rgb(178, 255, 255);
        color: #000;
    }
"""


class TinhAndMauPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # / Load Title and Icon Page
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )
        logo_path = self.path.path_logo()
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)

        # / Load Data Bans
        self.bans_path = self.path.path_db()
        with open(self.bans_path, "r") as file:
            self.bans_db = json.load(file)

        self.ban_info = self.bans_db
        self.ban_info['size'] = self.bans_db.get('size', 28)

        font_ac = QFont()
        font_ac.setPointSize(24)
        font_ac.setBold(True)
        self.font_action = font_ac

        # / Load data Thong and Number
        self.thong_info = None
        self.number_info = None

        # / Kết nối với Excel
        self.app = xw.App(visible=True)  # Mở Excel
        self.wb = self.app.books.active  # Workbook hiện tại
        self.add_vba_code()
        self.sheet_bt = self.wb.sheets[0]
        self.sheet_bt.name = "Bang tinh"
        
        self.sheet_m1 = self.wb.sheets.add(after=self.wb.sheets[0], name="Bang mau M1")
        self.sheet_m2 = self.wb.sheets.add(after=self.wb.sheets[1], name="Bang mau M2")
        self.sheet_m3 = self.wb.sheets.add(after=self.wb.sheets[2], name="Bang mau M3")
        self.sheet_m4 = self.wb.sheets.add(after=self.wb.sheets[3], name="Bang mau M4")
        self.sheet_m5 = self.wb.sheets.add(after=self.wb.sheets[4], name="Bang mau M5")
        self.sheet_m6 = self.wb.sheets.add(after=self.wb.sheets[5], name="Bang mau M6")
        self.sheet_m7 = self.wb.sheets.add(after=self.wb.sheets[6], name="Bang mau M7")
        self.sheet_m8 = self.wb.sheets.add(after=self.wb.sheets[7], name="Bang mau M8")
        self.sheet_m9 = self.wb.sheets.add(after=self.wb.sheets[8], name="Bang mau M9")
        self.sheet_m10 = self.wb.sheets.add(after=self.wb.sheets[9], name="Bang mau M10")
        self.sheet_bangThong = self.wb.sheets.add(after=self.wb.sheets[10], name="Bang Thong")

        self.pwd = "rindev-pm"

        # / Notice
        self.jumpAction = {}
        self.noticeView = []
        self.analysis_data = ""

        # / Mau cua o du lieu cu
        self.lastSheetName = ""
        self.lastAddress = ""
        self.lastColor = ""
        self.lastFontColor = ""

        # / Current name table
        self.current_table = "Bảng Tính"

        # / Config LoadingScreen
        self.loadingScreen = LoadingScreen(self.path.path_loading())

        # / Config Font
        font = QFont()
        font.setWeight(QFont.DemiBold)
        font.setPointSize(self.ban_info.get('size', 28))
        self.font = font

        # / Config Color
        self.red = (255, 0, 0)
        self.yellow = (255, 215, 0)
        self.cyan = QColor(178, 255, 255)
        self.normal = QColor("#FFFFFF")
        self.stt_highlight = QColor("#EDEADE")

        # / Navigation Main
        self.navbar_wid_main = QWidget()
        self.navbar_layout = QVBoxLayout(self.navbar_wid_main)
        self.navbar_layout.setSpacing(6)
        self.navbar_layout.setContentsMargins(0, 0, 0, 0)
        self.navbar_wid_main.setMaximumHeight(200)
        self.layout.addWidget(self.navbar_wid_main)

        self.note_w = QWidget()
        self.note_w.setFont(self.font)
        self.note_l = QHBoxLayout(self.note_w)
        self.note_l.setContentsMargins(0, 0, 0, 0)

        change_number = self.ban_info["meta"]["number"]
        self.note = QLabel("")
        self.note.setFont(self.font)
        self.note.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.note_l.addWidget(self.note)

        if change_number != 0:
            note = Note[change_number - 1]
            self.note.setText(note)
        else:
            note = Note[10]
            self.note.setText(note)

        self.note_color = f"a = sbáo; b = th; c = cột; d = sđếm; s = số trong thông"
        self.note_color_label = QLabel(self.note_color)
        self.note_color_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.note_l.addWidget(self.note_color_label)

        self.layout.addWidget(self.note_w)

        # / Widget Main
        self.widget_main = QStackedWidget()
        self.layout.addWidget(self.widget_main)

        # / Table main
        self.table_main_thong = None
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
        self.start_col = 0
        self.value_col = 0

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
        
        thong_sp_path = self.path.path_thong_sp_with_id(self.thong_db["id"])
        with open(thong_sp_path, 'r') as file:
            self.thong_sp = json.load(file)

    def showSelectBan(self):
        self.loadData()
        # /Render Sheet Excel
        self.reload_widget()
        self.renderTableThong()
        self.add_vba_code_sheets()
        self.focus_sheet()
        self.renderButton()
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

        title_text = self.get_title_text(type)

        

        self.status_w = QWidget()
        self.status_l = QVBoxLayout(self.status_w)

        self.title = QLabel(title_text)
        self.title.setStyleSheet(css_title)
        self.status_l.addWidget(self.title)

        self.navbar_layout.addWidget(self.status_w)

        # / Create a widget to contain the buttons 2
        buttons_container_2 = QWidget()
        buttons_container_2.setMaximumHeight(260)
        buttons_layout_2 = QGridLayout(buttons_container_2)

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

        notice_color_name = "m10"
        index_setting_btn_notice = 9
        if type == "m1":
            notice_color_name = "m1"
            index_setting_btn_notice = 0
        elif type == "m2":
            notice_color_name = "m2"
            index_setting_btn_notice = 1
        elif type == "m3":
            notice_color_name = "m3"
            index_setting_btn_notice = 2
        elif type == "m4":
            notice_color_name = "m4"
            index_setting_btn_notice = 3
        elif type == "m5":
            notice_color_name = "m5"
            index_setting_btn_notice = 4
        elif type == "m6":
            notice_color_name = "m6"
            index_setting_btn_notice = 5
        elif type == "m7":
            notice_color_name = "m7"
            index_setting_btn_notice = 6
        elif type == "m8":
            notice_color_name = "m8"
            index_setting_btn_notice =7
        elif type == "m9":
            notice_color_name = "m9"
            index_setting_btn_notice = 8
        else:
            notice_color_name = "m10"
            index_setting_btn_notice = 9

        setting_btn_notice = self.ban_info["meta"]["tables"][index_setting_btn_notice]["number_btn_notice"] if "number_btn_notice" in self.ban_info["meta"]["tables"][index_setting_btn_notice] else 10
        number_btn = setting_btn_notice
        
        for label in range(number_btn):
            if label < len(self.color_list):
                isColor = self.color_list[label]
            else:
                isColor = None  # Or any default value
            if isColor:
                # / Add button to list of buttons
                btn_name_label = f"{notice_color_name}: | ({label + 1})" if label == 0 else f"({label + 1})"
                btn_label = f'{btn_name_label} {isColor["data"]}'
                btn = QPushButton(btn_label)
                btn.setStyleSheet(css_button_notice)
                btn.setCursor(Qt.PointingHandCursor)
                if label < 6:
                    buttons_layout_2.addWidget(btn, 0, label)
                if 6 <= label < 12:
                    buttons_layout_2.addWidget(btn, 1, label - 6)
                if 12 <= label < 18:
                    buttons_layout_2.addWidget(btn, 2, label - 12)
                if 18 <= label < 24:
                    buttons_layout_2.addWidget(btn, 3, label - 18)
                # if 20 <= label < 25:
                #     buttons_layout_2.addWidget(btn, 4, label - 20)

                    
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
                btn_label = str(f'({label + 1})')
                btn = QPushButton(btn_label)
                btn.setFixedWidth(60)
                btn.setStyleSheet(css_button_normal)
                btn.setCursor(Qt.PointingHandCursor)
                if label < 6:
                    buttons_layout_2.addWidget(btn, 0, label)
                if 6 <= label < 12:
                    buttons_layout_2.addWidget(btn, 1, label - 6)
                if 12 <= label < 18:
                    buttons_layout_2.addWidget(btn, 2, label - 12)
                if 18 <= label < 24:
                    buttons_layout_2.addWidget(btn, 3, label - 18)
        

        # / Create a scroll area and set its widget to the buttons container 2
        self.scroll_area_2 = QScrollArea()
        self.scroll_area_2.setFrameStyle(QFrame.NoFrame)
        self.scroll_area_2.setWidgetResizable(True)
        self.scroll_area_2.setWidget(buttons_container_2)

        self.navbar_layout.addWidget(self.scroll_area_2)

        # / reRender Data Analysis Color D
        value_input = self.analysis_data
        if len(value_input) > 0:
            if "," in value_input:
                value_input = value_input.split(",")
            else:
                value_input = [value_input]
            self.handler_data_analysis(value_input)

    # TODO Handler Button PM
    def renderButton(self):
        button_main_1_w = QWidget()
        button_main_1_l = QHBoxLayout(button_main_1_w)
        self.button_layout.addWidget(button_main_1_w)
        button_main_2_w = QWidget()
        button_main_2_l = QHBoxLayout(button_main_2_w)
        self.button_layout.addWidget(button_main_2_w)

        # / Back to first row
        backToFirst = QPushButton("Về Cột Đầu")
        backToFirst.setStyleSheet(css_button_start)
        backToFirst.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(backToFirst)

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
        

        # / Skip to mid row
        skipToMind = QPushButton("Về Cột Giữa")
        skipToMind.setStyleSheet(css_button_start)
        skipToMind.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(skipToMind)

        # / Bảng Màu 1
        self.TableM1 = QPushButton("m1")
        self.TableM1.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border-radius: 8px; 
                font-size: 24px;
                line-height: 32px;
                font-weight: 600; 
                color: #fff; 
                background-color: #09de89;
            } 
            QPushButton:hover {
                background-color: #00ce7c;
            }
        """)
        self.TableM1.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(self.TableM1)

        # / Setting Table
        SettingTable = QPushButton("Cài Đặt Bảng")
        SettingTable.setStyleSheet(css_button_submit)
        SettingTable.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(SettingTable)

        # / Insert Data row
        InsertData = QPushButton("Nhập Liệu")
        InsertData.setStyleSheet(css_custom_btn_insert)
        InsertData.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(InsertData)

        # / Bảng Màu
        self.TableChange = QPushButton("Bảng Tính")
        self.TableChange.setStyleSheet(css_button_submit)
        self.TableChange.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(self.TableChange)

        # / Skip to end row
        skipToEnd = QPushButton("Về Cột Cuối")
        skipToEnd.setStyleSheet(css_button_start)
        skipToEnd.setCursor(QCursor(Qt.PointingHandCursor))
        button_main_1_l.addWidget(skipToEnd)

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
            self.focus_sheet()
            self.current_table = "Bảng Tính"
            self.renderNavigation()
            return

        def changeTableM1():
            self.focus_sheet(1)
            self.current_table = "Bảng màu 1"
            self.renderNavigation("m1")
            return

        def changeTableM2():
            self.focus_sheet(2)
            self.current_table = "Bảng màu 2"
            self.renderNavigation("m2")
            return

        def changeTableM3():
            self.focus_sheet(3)
            self.current_table = "Bảng màu 3"
            self.renderNavigation("m3")
            return

        def changeTableM4():
            self.focus_sheet(4)
            self.current_table = "Bảng màu 4"
            self.renderNavigation("m4")
            return

        def changeTableM5():
            self.focus_sheet(5)
            self.current_table = "Bảng màu 5"
            self.renderNavigation("m5")
            return

        def changeTableM6():
            self.focus_sheet(6)
            self.current_table = "Bảng màu 6"
            self.renderNavigation("m6")
            return

        def changeTableM7():
            self.focus_sheet(7)
            self.current_table = "Bảng màu 7"
            self.renderNavigation("m7")
            return

        def changeTableM8():
            self.focus_sheet(8)
            self.current_table = "Bảng màu 8"
            self.renderNavigation("m8")
            return

        def changeTableM9():
            self.focus_sheet(9)
            self.current_table = "Bảng màu 9"
            self.renderNavigation("m9")
            return

        def changeTableM10():
            self.focus_sheet(10)
            self.current_table = "Bảng màu 10"
            self.renderNavigation("m10")
            return

        for i in range(10):
            info_data = self.ban_info["meta"]["tables"][i]
            if info_data["enable"]:
                match i:
                    case 0:
                        pass
                    case 1:
                        # / BM 2
                        self.TableM2 = QPushButton("m2")
                        self.TableM2.setStyleSheet(css_button_submit)
                        self.TableM2.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM2)
                        self.TableM2.clicked.connect(changeTableM2)
                    case 2:
                        # / BM 3
                        self.TableM3 = QPushButton("m3")
                        self.TableM3.setStyleSheet(css_button_submit)
                        self.TableM3.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM3)
                        self.TableM3.clicked.connect(changeTableM3)
                    case 3:
                        # / BM 4
                        self.TableM4 = QPushButton("m4")
                        self.TableM4.setStyleSheet(css_button_submit)
                        self.TableM4.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM4)
                        self.TableM4.clicked.connect(changeTableM4)
                    case 4:
                        # / BM 5
                        self.TableM5 = QPushButton("m5")
                        self.TableM5.setStyleSheet(css_button_submit)
                        self.TableM5.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM5)
                        self.TableM5.clicked.connect(changeTableM5)
                    case 5:
                        # / BM 6
                        self.TableM6 = QPushButton("m6")
                        self.TableM6.setStyleSheet(css_button_submit)
                        self.TableM6.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM6)
                        self.TableM6.clicked.connect(changeTableM6)
                    case 6:
                        # / BM 7
                        self.TableM7 = QPushButton("m7")
                        self.TableM7.setStyleSheet(css_button_submit)
                        self.TableM7.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM7)
                        self.TableM7.clicked.connect(changeTableM7)
                    case 7:
                        # / BM 8
                        self.TableM8 = QPushButton("m8")
                        self.TableM8.setStyleSheet(css_button_submit)
                        self.TableM8.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM8)
                        self.TableM8.clicked.connect(changeTableM8)
                    case 8:
                        # / BM 9
                        self.TableM9 = QPushButton("m9")
                        self.TableM9.setStyleSheet(css_button_submit)
                        self.TableM9.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM9)
                        self.TableM9.clicked.connect(changeTableM9)
                    case 9:
                        # / BM 10
                        self.TableM10 = QPushButton("m10")
                        self.TableM10.setStyleSheet(css_button_submit)
                        self.TableM10.setCursor(QCursor(Qt.PointingHandCursor))
                        button_main_2_l.addWidget(self.TableM10)
                        self.TableM10.clicked.connect(changeTableM10)
                    case _:
                        pass

        def move_cursor(pos):
            # Lấy sheet hiện tại
            active_sheet = self.wb.sheets.active
            data_range = active_sheet.range("A1").expand("right")
            total_cols = data_range.columns.count
            if total_cols == 0:
                return  # Không có dữ liệu thì không làm gì cả
            if pos == "fisrt":
                col_index = 2  # Cột đầu tiên (A)
            elif pos == "midle":
                col_index = (int(total_cols) / 2) + 1  # Cột giữa
            else:
                col_index = total_cols  # Cột cuối cùng

            cell = active_sheet.cells(1, col_index)  # Chọn ô đầu tiên của cột tương ứng (hàng 1)
            cell.api.Activate()  # Di chuyển con trỏ đến ô đó

        InsertData.clicked.connect(insertData_Click)
        self.TableChange.clicked.connect(changeTable)
        SettingTable.clicked.connect(self.changeSettingColor)
        DeleteNewRow.clicked.connect(self.deleteNewRow)
        DeleteFromTo.clicked.connect(self.deleteFromToRow)
        backToFirst.clicked.connect(lambda: move_cursor("fisrt"))
        skipToMind.clicked.connect(lambda: move_cursor("midle"))
        skipToEnd.clicked.connect(lambda: move_cursor("last"))
        self.TableM1.clicked.connect(changeTableM1)

    def renderTableCount(self):
        try:
            last_row = self.sheet_bt.range("A1").end("down").row
            last_col = self.sheet_bt.range("A1").end("right").column
            table_range = self.sheet_bt.range((1, 1), (last_row, last_col))
            table_range.clear_contents()
            table_range.clear_formats()

            formatter = TableFormatter(self.sheet_bt)
            # Config Header
            header_thong =  self.updateHeaderCount()
            # Render row
            data_row = self.updateTableCount()
            date_d = data_row.get("date_d")
            data_r = data_row.get("data_r")

            headers = [["Ngày"] + header_thong]
            self.sheet_bt.range("A1").value = headers # Tiêu đề
            self.sheet_bt.range("A2:A2").value = date_d
            self.sheet_bt.range("B2").value = data_r

            # Chuẩn bị format rules và data menu
            format_rules = []
            for item in self.dataCount:
                col = item['col'] + 3
                row = item['row'] + 2

                format_rules.append({
                    'row': row,
                    'col': col,
                    'color': item.get('color'),
                    'notice': item.get('notice')
                })
            # Áp dụng định dạng một lần
            formatter.apply_formats(headers, format_rules)

            self.sheet_bt.range("B2").select()

            self.wb.app.api.ActiveWindow.FreezePanes = True
        except Exception as e:
            print(f"Đã xảy ra lỗi khi cố găng Tải Dữ liệu bảng Tính {e}")
            return False

    def get_title_text(self, type=None):
        if type is None:
            table_enabel = [
            i for i, x in enumerate(self.ban_info["meta"]["tables"]) if x["enable"]
            ]
            last_index = table_enabel[-1] if table_enabel else None
            current_color = last_index
        else:
            current_color = int(type.split('m')[1]) - 1
        # / Config Ban info
        ban_info = self.ban_info
        filter_data = [entry for entry in ban_info["data"] if not entry["isDeleted"]]
        row_count = len(filter_data)
        max_row = ban_info["meta"]["maxRow"]
        change_number = ban_info["meta"]["number"]
        ban_col = ban_info["col"]
        ban_thong_value = ban_info["thong"]["value"]
        ban_thong_name = ban_info["thong"]["name"]
        co_so = change_number if change_number != 0 else "gốc"
        index = current_color + 1 if current_color != 0 else ''
        thong_ke_d_m = self.ban_info['meta']['setting'][f'col_e{index}']
        list_table_color = [
            f"m{i+1}" for i, v in enumerate(ban_info["meta"]["tables"]) if v["enable"]
        ]
        name = convert_string_format(ban_thong_name)
        return (
            f"{self.current_table}: {name} ** C{ban_col[0]} đến C{ban_col[1]} ** T{ban_thong_value[0]} đến "
            + f"T{ban_thong_value[1]} **  Cơ: {co_so} ** "
            + f"Số dòng: {row_count}/{max_row} ** Thống kê d m{current_color + 1}: {' đến '.join(map(str, thong_ke_d_m))} ** Toán màu: {list_table_color[0]} đến {list_table_color[-1]}"
        )

    # TODO Handle Table M1
    def renderTableColor(self):
        try:
            last_row = self.sheet_m1.range("A1").end("down").row
            last_col = self.sheet_m1.range("A1").end("right").column
            table_range = self.sheet_m1.range((1, 1), (last_row, last_col))
            table_range.clear_contents()
            table_range.clear_formats()

            formatter = TableFormatter(self.sheet_m1)

            # Config Header
            header_thong =  self.updateHeaderColor()
            # Render row
            data_row = self.updateTableColor()
            date_d = data_row.get("date_d")
            data_r = data_row.get("data_r")

            headers = [["Ngày"] + header_thong]
            self.sheet_m1.range("A1").value = headers # Tiêu đề
            self.sheet_m1.range("A2:A2").value = date_d
            self.sheet_m1.range("B2").value = data_r

            # Chuẩn bị format rules
            format_rules = []
            for item in self.dataColor:
                format_rules.append({
                    'row': item['row'] + 2,
                    'col': item['col'] + 2,
                    'color': item.get('color'),
                    'notice': item.get('notice')
                })
            
            # Áp dụng định dạng một lần
            formatter.apply_formats(headers, format_rules)

            self.sheet_m1.range("B2").select()

            self.wb.app.api.ActiveWindow.FreezePanes = True
        except Exception as e:
            print(f"Lỗi trong quá trình Render Bảng M1: {e}")
            return False
        
    # TODO Handle Table M2
    def renderTableColorM2(self):
        try:
            last_row = self.sheet_m2.range("A1").end("down").row
            last_col = self.sheet_m2.range("A1").end("right").column
            table_range = self.sheet_m2.range((1, 1), (last_row, last_col))
            table_range.clear_contents()
            table_range.clear_formats()

            formatter = TableFormatter(self.sheet_m2)

            # Config Header
            header_thong =  self.updateHeaderColorM2()
            # Render row
            data_row = self.updateTableColorM2()
            date_d = data_row.get("date_d")
            data_r = data_row.get("data_r")

            headers = [["Ngày"] + header_thong]
            self.sheet_m2.range("A1").value = headers # Tiêu đề
            self.sheet_m2.range("A2:A2").value = date_d
            self.sheet_m2.range("B2").value = data_r

            # Chuẩn bị format rules
            format_rules = []
            for item in self.dataColor2:
                format_rules.append({
                    'row': item['row'] + 2,
                    'col': item['col'] + 2,
                    'color': item.get('color'),
                    'notice': item.get('notice')
                })
            
            # Áp dụng định dạng một lần
            formatter.apply_formats(headers, format_rules)

            self.sheet_m2.range("B2").select()

            self.wb.app.api.ActiveWindow.FreezePanes = True
        except Exception as e:
            print(f"Đã xảy ra lỗi khi cố găng tải dữ liệu bảng M2 {e}")
            return False
    
    # TODO Handle Table M3
    def renderTableColorM3(self):
        last_row = self.sheet_m3.range("A1").end("down").row
        last_col = self.sheet_m3.range("A1").end("right").column
        table_range = self.sheet_m3.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m3)

        # Config Header
        header_thong =  self.updateHeaderColorM3()
        # Render row
        data_row = self.updateTableColorM3()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m3.range("A1").value = headers # Tiêu đề
        self.sheet_m3.range("A2:A2").value = date_d
        self.sheet_m3.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor3:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m3.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
        
    # TODO Handle Table M4
    def renderTableColorM4(self):
        last_row = self.sheet_m4.range("A1").end("down").row
        last_col = self.sheet_m4.range("A1").end("right").column
        table_range = self.sheet_m4.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m4)

        # Config Header
        header_thong =  self.updateHeaderColorM4()
        # Render row
        data_row = self.updateTableColorM4()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m4.range("A1").value = headers # Tiêu đề
        self.sheet_m4.range("A2:A2").value = date_d
        self.sheet_m4.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor4:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m4.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
        
    # TODO Handle Table M5
    def renderTableColorM5(self):
        last_row = self.sheet_m5.range("A1").end("down").row
        last_col = self.sheet_m5.range("A1").end("right").column
        table_range = self.sheet_m5.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m5)

        # Config Header
        header_thong =  self.updateHeaderColorM5()
        # Render row
        data_row = self.updateTableColorM5()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m5.range("A1").value = headers # Tiêu đề
        self.sheet_m5.range("A2:A2").value = date_d
        self.sheet_m5.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor5:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m5.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
        
    # TODO Handle Table M6
    def renderTableColorM6(self):
        last_row = self.sheet_m6.range("A1").end("down").row
        last_col = self.sheet_m6.range("A1").end("right").column
        table_range = self.sheet_m6.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m6)

        # Config Header
        header_thong =  self.updateHeaderColorM6()
        # Render row
        data_row = self.updateTableColorM6()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m6.range("A1").value = headers # Tiêu đề
        self.sheet_m6.range("A2:A2").value = date_d
        self.sheet_m6.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor6:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m6.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
        
    # TODO Handle Table M7
    def renderTableColorM7(self):
        last_row = self.sheet_m7.range("A1").end("down").row
        last_col = self.sheet_m7.range("A1").end("right").column
        table_range = self.sheet_m7.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m7)

        # Config Header
        header_thong =  self.updateHeaderColorM7()
        # Render row
        data_row = self.updateTableColorM7()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m7.range("A1").value = headers # Tiêu đề
        self.sheet_m7.range("A2:A2").value = date_d
        self.sheet_m7.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor7:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m7.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
        
    # TODO Handle Table M8
    def renderTableColorM8(self):
        last_row = self.sheet_m8.range("A1").end("down").row
        last_col = self.sheet_m8.range("A1").end("right").column
        table_range = self.sheet_m8.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m8)

        # Config Header
        header_thong =  self.updateHeaderColorM8()
        # Render row
        data_row = self.updateTableColorM8()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m8.range("A1").value = headers # Tiêu đề
        self.sheet_m8.range("A2:A2").value = date_d
        self.sheet_m8.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor8:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m8.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
        
    # TODO Handle Table M9
    def renderTableColorM9(self):
        last_row = self.sheet_m9.range("A1").end("down").row
        last_col = self.sheet_m9.range("A1").end("right").column
        table_range = self.sheet_m9.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m9)

        # Config Header
        header_thong =  self.updateHeaderColorM9()
        # Render row
        data_row = self.updateTableColorM9()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m9.range("A1").value = headers # Tiêu đề
        self.sheet_m9.range("A2:A2").value = date_d
        self.sheet_m9.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor9:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m9.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
        
    # TODO Handle Table M10
    def renderTableColorM10(self):
        last_row = self.sheet_m10.range("A1").end("down").row
        last_col = self.sheet_m10.range("A1").end("right").column
        table_range = self.sheet_m10.range((1, 1), (last_row, last_col))
        table_range.clear_contents()
        table_range.clear_formats()
        formatter = TableFormatter(self.sheet_m10)

        # Config Header
        header_thong =  self.updateHeaderColorM10()
        # Render row
        data_row = self.updateTableColorM10()
        date_d = data_row.get("date_d")
        data_r = data_row.get("data_r")

        headers = [["Ngày"] + header_thong]
        self.sheet_m10.range("A1").value = headers # Tiêu đề
        self.sheet_m10.range("A2:A2").value = date_d
        self.sheet_m10.range("B2").value = data_r

        # Chuẩn bị format rules
        format_rules = []
        for item in self.dataColor10:
            format_rules.append({
                'row': item['row'] + 2,
                'col': item['col'] + 2,
                'color': item.get('color'),
                'notice': item.get('notice')
            })
        
        # Áp dụng định dạng một lần
        formatter.apply_formats(headers, format_rules)

        self.sheet_m10.range("B2").select()

        self.wb.app.api.ActiveWindow.FreezePanes = True
    
    # TODO Hanle Table Thong
    def renderTableThong(self):
        try:
            # Focus Sheet
            self.sheet_bangThong.select()
            self.sheet_bangThong.activate()

            # Format Cells
            # Xác định phạm vi bảng (tự động tìm kích thước bảng)
            last_row = self.sheet_bangThong.range("A1").end("down").row
            last_col = self.sheet_bangThong.range("A1").end("right").column
            table_range = self.sheet_bangThong.range((1, 1), (last_row, last_col))

            # 🌟 **Áp dụng định dạng cho toàn bảng**
            table_range.api.Font.Name = "Arial"  # Font chữ
            table_range.api.Font.Size = 24  # Cỡ chữ
            table_range.api.HorizontalAlignment = -4108  # Căn giữa
            table_range.api.VerticalAlignment = -4107  # Căn giữa theo chiều dọc
            table_range.api.Borders.Weight = 2  # Độ dày đường viền
            table_range.api.Font.Bold = True  # In đậm tiêu đề
            table_range.api.NumberFormat = "@"

            header_lables = self.updateHeaderRowThong()
            data_row = self.updateRowAndColumnsThong()
            data_headers = data_row.get("headers")
            data_stt = data_row.get("data_stt")
            data_custom = data_row.get("custom")
            data_thong = data_row.get("data_thong")
            if data_headers:
                for header in data_headers:
                    lable = header.get("text")
                    start_col_letter = header.get("start_col_letter")
                    self.sheet_bangThong.range(f"{start_col_letter}1").value = lable

            self.sheet_bangThong.range("A2").value = [["STT"] + header_lables]  # Tiêu đề
            self.sheet_bangThong.range("A3:A3").value = data_stt
            self.sheet_bangThong.range("B3:E3").value = data_custom
            self.sheet_bangThong.range("F3").value = data_thong

            for i, (row, col) in enumerate(self.e_positions):
                # Get the column letter
                col_letter = self.sheet_bangThong.cells(1, col).address.split('$')[1]
                # Color the entire column (or a specific range in that column)
                column_range = f"{col_letter}:{col_letter}"  # Entire column
                # Or specify a range like: f"{col_letter}2:{col_letter}100"
                
                # Apply color
                if self.e_indices[i] % 10 == 0:
                    self.sheet_bangThong.range(column_range).color = (255, 255, 102)
                else:
                    self.sheet_bangThong.range(column_range).color =  (77, 147, 217)

            # Similar for H positions
            for i, (row, col) in enumerate(self.h_positions):
                col_letter = self.sheet_bangThong.cells(1, col).address.split('$')[1]
                column_range = f"{col_letter}:{col_letter}"
                
                if self.h_indices[i] % 10 == 0:
                    self.sheet_bangThong.range(column_range).color = (255, 255, 102)
                else:
                    self.sheet_bangThong.range(column_range).color = (77, 147, 217)

            # Tự động căn chỉnh kích thước cột dựa trên nội dung
            self.sheet_bangThong.autofit('c')  # 'c' để autofit các cột

            # # Chọn ô F3
            self.sheet_bangThong.range("F3").select()

            # # Đóng băng cột A
            self.wb.app.api.ActiveWindow.FreezePanes = True
            self.toggle_editable(False)

        except Exception as e:
                print(f"Lỗi trong quá trình focus sheet: {e}")
                return False
    
    # TODO Update HeaderRowThong
    def updateHeaderRowThong(self):
        value_thong = self.thong_db["value"]
        thong_per_luot = self.thong_db["thong_per_luot"]
        isThong_one = 200

        # Setting header Thong
        with open(self.path.path_config_steps(), "r") as file:
            steps = json.load(file)
        
        with open(self.path.path_config_modifications(), "r") as file:
            modifications_a = json.load(file)

        thong_header_label = []  # Lưu nhãn tiêu đề
        self.e_positions = []
        self.h_positions = []
        self.e_indices = []
        self.h_indices = []

        # Biến số lượng cột và các giá trị liên quan
        total_columns = value_thong

        if isThong_one != 0:
            # Số cột tổng cộng
            # Số tập
            num_sets = 1
            # Số lượt trong mỗi tập
            rounds_per_set = 3
            # Số thông trong mỗi lượt
            columns_per_round = thong_per_luot

            # Lặp qua từng tập
            for set_index in range(num_sets):
                # Lặp qua từng lượt trong mỗi tập
                for round_index in range(rounds_per_set):
                    # Calculate index for coloring
                    current_index = set_index * rounds_per_set + round_index
                    # Tính chỉ số cột bắt đầu và kết thúc của lượt
                    start_col = (set_index * rounds_per_set * columns_per_round) + (round_index * columns_per_round)
                    end_col = start_col + columns_per_round
                    current_pos = len(thong_header_label) + 5
                    
                    # Thêm cột e và h trước mỗi lượt
                    e = f"E + {modifications_a[set_index][round_index]}"
                    h = f"H + {steps[set_index][round_index]}"

                    self.e_positions.append((2, current_pos + 1))  # +1 because positions are 1-based in xlwings
                    self.h_positions.append((2, current_pos + 2))
                
                    # Store indices for color determination
                    self.e_indices.append(current_index)
                    self.h_indices.append(current_index)
                    thong_header_label.append(e)
                    thong_header_label.append(h)
                    
                    # Thêm các cột thông
                    for thong in range(start_col, end_col):
                        thong_header_label.append(f"T. {thong + 1}")
        else:
            thong_header_label = [f"T. {thong + 1}" for thong in range(total_columns)]
        
        header_labels = ["A", "B", "C", "D"] + thong_header_label
        return header_labels
    
    # TODO Update HeaderRowThong
    def updateRowAndColumnsThong(self):
        # Lấy dữ liệu cần thiết
        meta_number = self.bans_db["meta"]["number"]

        stt = self.thong_db["stt"][meta_number]
        data_value = self.thong_db["data"]
        thong_data = self.thong_info

        # * Cập nhật tiêu đề hàng (STT)
        data_stt = []
        for i, stt_value in enumerate(stt):
            item = []
            item.append(stt_value)
            data_stt.append(item)

        # * Xử lý dữ liệu nếu cần thay đổi số
        # if meta_number != 0 and not self.isShow:
        #     data_value = [
        #         [TachVaGhep(meta_number, value) for value in row]
        #         for row in data_value
        #     ]

        data_custom = []
        # * Cập nhật dữ liệu từ data_value
        for i in range(131):
            row_items = []
            for j, cell_value in enumerate(data_value):
                row_items.append(cell_value[i])
            data_custom.append(row_items)

        # * Cập nhật dữ liệu từ thong_data
        info_headers = []
        data_thong = []
        thong_per_luot = self.thong_db["thong_per_luot"]
        isThong_step = thong_per_luot
        # if isThong_step == 15:
        count_luot = 0

        # Duyệt qua các tập (10 tập)
        for tap_index in range(1):
            for luot_title in range(3):  # Mỗi tập có 10 lượt
                span_start_col = 6 + count_luot * (isThong_step + 2)  # Cộng thêm 2 cột E và H
                span_colspan = isThong_step + 2  # Gồm 5 cột thong và 2 cột E, H
                tap = f"Tập {tap_index + 1} - " if luot_title == 0 else ""  # Gắn nhãn tập nếu là lượt đầu của tập
                
                header_text = f"{tap}Lượt {count_luot + 1}"
                # Excel range string
                start_col_letter = xw.utils.col_name(span_start_col)
                end_col_letter = xw.utils.col_name(span_start_col + span_colspan - 1)
                range_str = f"{start_col_letter}1:{end_col_letter}1"

                info_headers.append({
                    'text': header_text,
                    'range': range_str,
                    'start_col_letter': start_col_letter,
                    'end_col_letter': end_col_letter,
                    'tap_index': tap_index,
                    'luot_index': count_luot
                })
                count_luot += 1

        for row in range(131):  # Số lượng hàng (131 là ví dụ)
            data_row_thong = []
            # Duyệt qua từng tập và lượt
            for tap_index in range(1):
                for luot in range(3):
                    luot_index = tap_index * 3 + luot
                    start_col = 4 + luot_index * (isThong_step + 2)  # Vị trí bắt đầu cho lượt (bao gồm E và H)

                    # Thêm cột E và H
                    if row < len(self.thong_sp) and luot_index < len(self.thong_sp[row]):

                        # E column
                        e_row = self.thong_sp[row][luot_index][0]
                        data_row_thong.append(e_row)

                        # H column
                        h_row = self.thong_sp[row][luot_index][1]
                        data_row_thong.append(h_row)

                    # Thêm 10 cột thong
                    thong_start_index = luot_index * isThong_step  # Tính chỉ số bắt đầu cho thong_data
                    for thong_col in range(isThong_step):
                        thong_index = thong_start_index + thong_col
                        if thong_index < len(thong_data) and row < len(thong_data[thong_index]):
                            thong_row = thong_data[thong_index][row]
                            data_row_thong.append(thong_row)
            data_thong.append(data_row_thong)
        return {
            'headers': info_headers,
            "custom": data_custom,
            "data_thong": data_thong,
            "data_stt": data_stt
        }

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
        if matching_item:
            localItem = matching_item.get("localItem")
            row = localItem.get("row")
            col = localItem.get("col")
            colname = self.get_column_name(col + 2)
            if "_m10" in label:
                self.focus_sheet(10)
                item = self.sheet_m10.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m10)
                return
            elif "_m9" in label:
                self.focus_sheet(9)
                item = self.sheet_m9.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m9)
                return
            elif "_m8" in label:
                self.focus_sheet(8)
                item = self.sheet_m8.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m8)
                return
            elif "_m7" in label:
                self.focus_sheet(7)
                item = self.sheet_m7.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m7)
                return
            elif "_m6" in label:
                self.focus_sheet(6)
                item = self.sheet_m6.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m6)
                return
            elif "_m5" in label:
                self.focus_sheet(5)
                item = self.sheet_m5.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m5)
                return
            elif "_m4" in label:
                self.focus_sheet(4)
                item = self.sheet_m4.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m4)
                return
            elif "_m3" in label:
                self.focus_sheet(3)
                item = self.sheet_m3.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m3)
                return
            elif "_m2" in label:
                self.focus_sheet(2)
                item = self.sheet_m2.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m2)
                return
            else:
                self.focus_sheet(1)
                item = self.sheet_m1.range(f"${colname}${row+2}")
                self.save_color_old_cell(item, self.sheet_m1)
                return

    def insertData(self):
        # / Config Icon Windows
        icon = self.path.path_logo()

        self.isEnable_table_thong = True

        # / Create Dialog Windows
        dialog = QDialog()
        dialog.setWindowTitle("Bảng Nhập Liệu")
        dialog.setWindowIcon(QIcon(icon))
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
        insert_day_edit.setWrapping(False)
        insert_day_edit.setCalendarPopup(True)
        insert_day_edit.setStyleSheet(
            """
                QDateEdit {
                    background-color: pink;
                    color:#000
                };
                font-size: 24px; /* Set font size */
            """
        )

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
        exit.setFixedWidth(100)
        
        submit_span = QLabel("")
        submit_span.setFixedHeight(100)
        insert_from_l.addWidget(submit_span, 5, 0)
        insert_from_l.addWidget(submit, 6, 1)
        
        exit_span = QLabel("")
        exit_span.setFixedHeight(150)
        insert_from_l.addWidget(exit_span, 7, 0)
        insert_from_l.addWidget(exit, 8, 0)

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
            else:
                if old_data is None or old_data["date"] != date.toString("dd/MM/yyyy"):
                    insert_day_edit.setStyleSheet(
                        "background-color: pink;font-size:24px;"
                    )
                else:
                    insert_day_edit.setStyleSheet("font-size:24px;")

        def changeNgang(value):
            data["insert"]["ngang"] = value - 1
            number_value = self.number_info[value - 1]
            insert_ngang_edit_first.setText(f"{number_value[0]}")
            if old_data is None or old_data["ngang"] != value - 1:
                insert_ngang_edit.setStyleSheet(
                    "background-color: pink;font-size:24px;"
                )
            else:
                insert_ngang_edit.setStyleSheet("font-size:24px;")

        def changeThongTable(value):
            if self.isEnable_table_thong:
                item = value.text()
                changeThongEdit(int(item))
                insert_thong_edit.setValue(int(item))
            else:
                insert_thong_table.clearSelection()
                SendMessage("Bạn không thể nhập thông rời tại đây!")

        def changeThongEdit(value):
            insert_thong_table.clearSelection()
            data["insert"]["thong"] = value
            if value == -1:
                insert_thong_edit_first.setText(f"")
                return

            if old_data is None or old_data["thong"] != value:
                insert_thong_edit.setStyleSheet(
                    "background-color: pink;font-size:24px;"
                )
            else:
                insert_thong_edit.setStyleSheet("font-size:24px;")

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
            # insert_thong_table.setDisabled(value)
            isEnable_table_thong_not = not self.isEnable_table_thong
            self.isEnable_table_thong = isEnable_table_thong_not
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
            # insert_thong_table.setDisabled(True)
            self.isEnable_table_thong = False
            title_label.setText("Bảng Nhập Liệu - Nhập Rời")
        else:
            title_label.setText("Bảng Nhập Liệu - Nhập Liền")

        if data["update"]["N=1"]["status"]:
            value = data["update"]["N=1"]["value"]
            insert_ngang_edit.setValue(value + 1)
            insert_ngang_edit.setDisabled(True)
            number_value = self.number_info[value][:2]
            insert_ngang_edit_first.setText(f"{number_value[0]}")
            insert_ngang_edit.setStyleSheet(
                "background-color: pink;font-size:24px;"
            )
            data["insert"]["ngang"] = value

        virable_one_edit.setChecked(data["update"]["N:2"])
        virable_two_edit.setChecked(data["update"]["N=1"]["status"])
        data["insert"]["thong"] = insert_thong_edit.value()

        exit.clicked.connect(exit_click)
        submit.clicked.connect(lambda: self.submit_insert(data, dialog))
        # Move and set the dialog size
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        dialog_width = 1000 + 300  # Use the dialog's width (e.g., from table)
        dialog_height = 780 + 100  # Add space for other content
        x = (screen_geometry.width() - dialog_width) // 2
        y = (screen_geometry.height() - dialog_height) // 2
        dialog.setFixedSize(dialog_width, dialog_height)  # Fix size
        dialog.move(x, y)

    def submit_insert(self, data, dialog):
        data["id"] = self.ban_info["id"]
        msg = updateBanInsert(data)
        if msg["status"]:
            dialog.reject()
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
        # dialog.setFixedSize(1200, 850)
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
        layout.addWidget(insert_from_w_2, 0, 1)

        insert_from_w = QWidget()
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

        # / Button Exit
        exit = QPushButton("Thoát")
        exit.setCursor(QCursor(Qt.PointingHandCursor))
        exit.setStyleSheet(css_button_cancel)
        exit.setFixedWidth(150)
        exit.setLayoutDirection(Qt.LayoutDirection.LeftToRight)


        submit_span = QLabel("")
        submit_span.setFixedHeight(100)
        insert_from_l_2.addWidget(submit_span)
        insert_from_l_2.addWidget(submit)

        exit_span = QLabel("")
        exit_span.setFixedHeight(150)
        insert_from_l_2.addWidget(exit_span)
        insert_from_l_2.addWidget(exit)

        verticalSpacer2 = QSpacerItem(
            20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        insert_from_l_2.addItem(verticalSpacer2)

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

        # Move and set the dialog size
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        dialog_width = 1000 + 300  # Use the dialog's width (e.g., from table)
        dialog_height = 780 + 100  # Add space for other content
        x = (screen_geometry.width() - dialog_width) // 2
        y = (screen_geometry.height() - dialog_height) // 2
        dialog.setFixedSize(dialog_width, dialog_height)  # Fix size
        dialog.move(x, y)

    def update_thong_insert(self, data, dialog):
        data_send = {}
        data_send["thong"] = data
        msg = updateThongInsert(data_send)
        if msg["status"]:
            dialog.reject()
            self.ban_info = msg["data"]
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
        message.setFont(self.font)
        result = message.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.insertData()

    def changeSettingColor(self):
        SettingTable(self.ban_info, self.thong_db)

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
        # Extract the old delete dates
        old_delete = self.ban_info.get('lastDelete', [])
        old_from_date = QDate().currentDate().addDays(-7)  # Default if not provided
        old_to_date = QDate().currentDate()               # Default if not provided

        if len(old_delete) == 2:
            old_from_date = QDate.fromString(old_delete[0], "dd/MM/yyyy")
            old_to_date = QDate.fromString(old_delete[1], "dd/MM/yyyy")

        # / Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle("Cài đặt bảng")
        dialog.setWindowIcon(QIcon(icon))
        dialog.setFixedSize(1000, 400)
        dialog.show()

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
        delete_from_edit.setDate(old_from_date)

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
        delete_to_edit.setDate(old_to_date)

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

    # TODO Handler Data Table
    # / Table Bang Tinh
    def updateTableCount(self):
        ban_info = self.ban_info
        value_col = ban_info["col"][1] - (ban_info["col"][0] - 1)
        filter_data = [entry for entry in ban_info["data"] if not entry["isDeleted"]]
        rowCount = len(filter_data)

        # / Config table
        thong_range = ban_info["thong"]["value"]
        thong_range_1 = thong_range[0] - 1
        thong_range_2 = thong_range[1]
        thong_ranges = thong_range_2 - thong_range_1

        date_d = []
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])
            
        data_r = []
        for i, item in enumerate(filter_data):
            row_r = []
            item_thong = item["thong"]
            data_filter = [item for item in self.dataCount if item["row"] == i]
            for j in range(thong_ranges):
                thong_value = self.thong_info[j + thong_range_1][item_thong]
                row_r.append(thong_value)
                group = [item["data"] for item in data_filter if item['thong']['col'] == j + 4]
                row_r.extend(group)
                    
            data_r.append(row_r)

        return {
            "date_d": date_d,
            "data_r": data_r
        }

    def updateHeaderCount(self):
        header_thong = []

        thong_range_1 = self.ban_info["thong"]["value"][0] - 1
        thong_range_2 = self.ban_info["thong"]["value"][1]
        thong_ranges = thong_range_2 - thong_range_1

        col_start, col_end = self.ban_info["col"]
        for i in range(thong_ranges):
            # Tạo tiêu đề cho "T.x"
            header_thong.append(f"T.{i + thong_range_1 + 1}")
            # Tạo tiêu đề cho các cột "C.x"
            for j in range(col_start - 1, col_end):
                header_thong.append(f"C.{j + 1}")
        
        return header_thong

    # / Table Bang M1
    def updateTableColor(self):
        # / Config rowCount With data
        date_d = []
        data_r = []
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e"]
        col_d = self.ban_info["meta"]["tables"][0]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)

        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m1: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables
    
    # / Table Bang M2
    def updateTableColorM2(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e2"]
        col_d = self.ban_info["meta"]["tables"][1]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor2 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m2: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M3
    def updateTableColorM3(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e3"]
        col_d = self.ban_info["meta"]["tables"][2]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor3 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m3: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M4
    def updateTableColorM4(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e4"]
        col_d = self.ban_info["meta"]["tables"][3]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor4 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m4: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M5
    def updateTableColorM5(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e5"]
        col_d = self.ban_info["meta"]["tables"][4]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor5 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m5: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M6
    def updateTableColorM6(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e6"]
        col_d = self.ban_info["meta"]["tables"][5]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor6 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m6: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M7
    def updateTableColorM7(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e7"]
        col_d = self.ban_info["meta"]["tables"][6]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor7 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m7: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M8
    def updateTableColorM8(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e8"]
        col_d = self.ban_info["meta"]["tables"][7]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor8 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

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
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m8: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M9
    def updateTableColorM9(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e9"]
        col_d = self.ban_info["meta"]["tables"][8]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 93
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor9 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

    def updateHeaderColorM9(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e9"]
        col_d = self.ban_info["meta"]["tables"][8]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m9: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

    # / Table Bang M10
    def updateTableColorM10(self):
        # / Set RowCount = 0
        date_d = []
        data_r = []
        # / Config rowCount With data
        filter_data = [
            entry for entry in self.ban_info["data"] if not entry["isDeleted"]
        ]
        rowCount = len(filter_data)
        for i in range(rowCount):
            date = filter_data[i]["date"]
            date_d.append([date])

        # / render row defalut
        col_e = self.ban_info["meta"]["setting"]["col_e10"]
        col_d = self.ban_info["meta"]["tables"][9]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 103
        for i in range(rowCount):
            row_r = []
            data_filter = [item for item in self.dataColor10 if item["row"] == i]
            # Khởi tạo biến để theo dõi tổng số cột
            total_columns = 0
            for c in range(value1 - 1, value2):
                num_cols = col_d[c]  # Số lượng cột tối đa có thể thêm
                # Thêm tên cột cho hàng header
                for j in range(num_cols):
                    current_col = total_columns + j
                    # Tìm dữ liệu khớp với row và column hiện tại
                    matching_data = next(
                        (item["data"] for item in data_filter if item["col"] == current_col),
                        "*"  # Giá trị mặc định nếu không tìm thấy
                    )
                    row_r.append(matching_data)
                # Tạo ô trống ở cột cuối cùng
                row_r.append("//")
                # Cập nhật tổng số cột
                total_columns += num_cols + 1
            data_r.append(row_r)
        
        return {
            "date_d": date_d,
            "data_r": data_r
        }

    def updateHeaderColorM10(self):
        current_column = 0
        # Khởi tạo biến để theo dõi tổng số cột
        total_columns = 0
        step_count = 0

        col_e = self.ban_info["meta"]["setting"]["col_e10"]
        col_d = self.ban_info["meta"]["tables"][9]["col_d"]
        value1 = col_e[0]
        value2 = col_e[1]
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            current_column += col_d[i] + 1  # Số cột tạo cho mỗi lần + 1 cột phụ trợ

        # Thiết lập số lượng cột cho bảng
        header_lables = []
        # Tạo cột từ 0 đến 83
        for i in range(value1 - 1, value2):
            # Xác định số lượng cột cho mỗi lần tạo
            num_cols = col_d[i]  # Số lượng cột tối đa có thể thêm

            # Thêm tên cột cho hàng header
            for j in range(num_cols):
                # Tạo hàng header cho mỗi lần tạo cột
                header_lables.append(f"m10: {j+1}/d{i + 1}")
            
            header_lables.append(f"//")

            # Cập nhật tổng số cột
            total_columns += num_cols + 1
            step_count += 1
        return header_lables

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
        notice_colorM1 = meta["colorM1"]
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
                    isColFisrt = f"{col_a}:{i}:{t}"

                    # / Check col_a equal col_t
                    isEqual = (
                        self.checkColor(str(col_a), str(col_t))
                        if item_thong > -1
                        else None
                    )
                    
                    row_thong = item_thong
                    if row_thong < 0:
                        row_thong = self.find_row_thong_with_col_a(
                            col_a, thong_info[t + thong_range_1]
                        )
                    # / End count color with col_d
                    if value1 <= col_d <= value2:
                        if not isColFisrt in self.isFrits:
                            self.isFrits[isColFisrt] = True
                            # / Start check col_c is first Like first check
                            maths_c1 = f"{col_d}:{t}:{i}:_color"
                            if not maths_c1 in self.math_isFirst:
                                self.math_isFirst[maths_c1] = 1
                            else:
                                self.math_isFirst[maths_c1] += 1

                            col_c1 = self.math_isFirst[maths_c1]
                            if col_c1 == 1: # !=0 danh cho ban toan theo dong, ko quan tam thong, == 1 danh cho ban toan theo thong
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
                                btn_notice_m1 = tables[0]["btn_notice"] if "btn_notice" in tables[0] else [[8, 36] for _ in range(1500)]
                                number_color_m1 = btn_notice_m1[col_d - 1] #! Ban toan theo thong
                                # number_color_m1 = notice_colorM1 #! Ban toan theo dong

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
                                        col_e, number_color_m1[0], number_color_m1[1]
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
                                            "col": t + 4,
                                            "col_a": col_t if col_t != "?" else col_a,
                                            "isCol_a": False if col_t != "?" else True,
                                            "col_t": col_t
                                        },
                                        "isDeleted": isDeleted,
                                    }

                                    dataColorM1 = {
                                        "row": countRow,
                                        "col": col_color,
                                        "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}",
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
                                            "col": t + 4,
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
                                        btn_notice_m2 = tables[1]["btn_notice"] if "btn_notice" in tables[1] else [[8, 36] for _ in range(1500)]
                                        number_color_m2 = btn_notice_m2[col_e - 1] #! Ban toan theo thong
                                        # number_color_m2 = notice_colorM2 #! Ban toan theo dong

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
                                                number_color_m2[0],
                                                number_color_m2[1],
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
                                                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}",
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
                                                    "col": t + 4,
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
                                                btn_notice_m3 = tables[2]["btn_notice"] if "btn_notice" in tables[2] else [[8, 36] for _ in range(1500)]
                                                number_color_m3 = btn_notice_m3[col_e_m2 - 1] #! Ban toan theo thong
                                                # number_color_m3 = notice_colorM3 #! Ban toan theo dong

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
                                                        number_color_m3[0],
                                                        number_color_m3[1],
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
                                                        "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}",
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
                                                            "col": t + 4,
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

                                    if (
                                        dataColorM10
                                        and self.ban_info["meta"]["tables"][9]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM2["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM3["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM4["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM5["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM6["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM7["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM8["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }
                                        dataColorM9["actionM10"] = {
                                            "name": "colorM10",
                                            "row": countRow,
                                            "col": dataColorM10["col"],
                                            "isColor": dataColorM10["notice"],
                                        }

                                    if (
                                        dataColorM9
                                        and self.ban_info["meta"]["tables"][8]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM2["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM3["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM4["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM5["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM6["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM7["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }
                                        dataColorM8["actionM9"] = {
                                            "name": "colorM9",
                                            "row": countRow,
                                            "col": dataColorM9["col"],
                                            "isColor": dataColorM9["notice"],
                                        }

                                    if (
                                        dataColorM8
                                        and self.ban_info["meta"]["tables"][7]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM8["notice"],
                                        }
                                        dataColorM2["actionM8"] = {
                                            "name": "colorM8",
                                            "row": countRow,
                                            "col": dataColorM8["col"],
                                            "isColor": dataColorM8["notice"],
                                        }
                                        dataColorM3["actionM8"] = {
                                            "name": "colorM8",
                                            "row": countRow,
                                            "col": dataColorM8["col"],
                                            "isColor": dataColorM8["notice"],
                                        }
                                        dataColorM4["actionM8"] = {
                                            "name": "colorM8",
                                            "row": countRow,
                                            "col": dataColorM8["col"],
                                            "isColor": dataColorM8["notice"],
                                        }
                                        dataColorM5["actionM8"] = {
                                            "name": "colorM8",
                                            "row": countRow,
                                            "col": dataColorM8["col"],
                                            "isColor": dataColorM8["notice"],
                                        }
                                        dataColorM6["actionM8"] = {
                                            "name": "colorM8",
                                            "row": countRow,
                                            "col": dataColorM8["col"],
                                            "isColor": dataColorM8["notice"],
                                        }
                                        dataColorM7["actionM8"] = {
                                            "name": "colorM8",
                                            "row": countRow,
                                            "col": dataColorM8["col"],
                                            "isColor": dataColorM8["notice"],
                                        }

                                    if (
                                        dataColorM7
                                        and self.ban_info["meta"]["tables"][6]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM7["notice"],
                                        }
                                        dataColorM2["actionM7"] = {
                                            "name": "colorM7",
                                            "row": countRow,
                                            "col": dataColorM7["col"],
                                            "isColor": dataColorM7["notice"],
                                        }
                                        dataColorM3["actionM7"] = {
                                            "name": "colorM7",
                                            "row": countRow,
                                            "col": dataColorM7["col"],
                                            "isColor": dataColorM7["notice"],
                                        }
                                        dataColorM4["actionM7"] = {
                                            "name": "colorM7",
                                            "row": countRow,
                                            "col": dataColorM7["col"],
                                            "isColor": dataColorM7["notice"],
                                        }
                                        dataColorM5["actionM7"] = {
                                            "name": "colorM7",
                                            "row": countRow,
                                            "col": dataColorM7["col"],
                                            "isColor": dataColorM7["notice"],
                                        }
                                        dataColorM6["actionM7"] = {
                                            "name": "colorM7",
                                            "row": countRow,
                                            "col": dataColorM7["col"],
                                            "isColor": dataColorM7["notice"],
                                        }

                                    if (
                                        dataColorM6
                                        and self.ban_info["meta"]["tables"][5]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM6["notice"],
                                        }
                                        dataColorM2["actionM6"] = {
                                            "name": "colorM6",
                                            "row": countRow,
                                            "col": dataColorM6["col"],
                                            "isColor": dataColorM6["notice"],
                                        }
                                        dataColorM3["actionM6"] = {
                                            "name": "colorM6",
                                            "row": countRow,
                                            "col": dataColorM6["col"],
                                            "isColor": dataColorM6["notice"],
                                        }
                                        dataColorM4["actionM6"] = {
                                            "name": "colorM6",
                                            "row": countRow,
                                            "col": dataColorM6["col"],
                                            "isColor": dataColorM6["notice"],
                                        }
                                        dataColorM5["actionM6"] = {
                                            "name": "colorM6",
                                            "row": countRow,
                                            "col": dataColorM6["col"],
                                            "isColor": dataColorM6["notice"],
                                        }

                                    if (
                                        dataColorM5
                                        and self.ban_info["meta"]["tables"][4]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM5["notice"],
                                        }
                                        dataColorM2["actionM5"] = {
                                            "name": "colorM5",
                                            "row": countRow,
                                            "col": dataColorM5["col"],
                                            "isColor": dataColorM5["notice"],
                                        }
                                        dataColorM3["actionM5"] = {
                                            "name": "colorM5",
                                            "row": countRow,
                                            "col": dataColorM5["col"],
                                            "isColor": dataColorM5["notice"],
                                        }
                                        dataColorM4["actionM5"] = {
                                            "name": "colorM5",
                                            "row": countRow,
                                            "col": dataColorM5["col"],
                                            "isColor": dataColorM5["notice"],
                                        }

                                    if (
                                        dataColorM4
                                        and self.ban_info["meta"]["tables"][3]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM4["notice"],
                                        }
                                        dataColorM2["actionM4"] = {
                                            "name": "colorM4",
                                            "row": countRow,
                                            "col": dataColorM4["col"],
                                            "isColor": dataColorM4["notice"],
                                        }
                                        dataColorM3["actionM4"] = {
                                            "name": "colorM4",
                                            "row": countRow,
                                            "col": dataColorM4["col"],
                                            "isColor": dataColorM4["notice"],
                                        }

                                    if (
                                        dataColorM3
                                        and self.ban_info["meta"]["tables"][2]["enable"]
                                        == True
                                    ):
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
                                            "isColor": dataColorM3["notice"],
                                        }

                                        dataColorM2["actionM3"] = {
                                            "name": "colorM3",
                                            "row": countRow,
                                            "col": dataColorM3["col"],
                                            "isColor": dataColorM3["notice"],
                                        }

                                    if (
                                        dataColorM2
                                        and self.ban_info["meta"]["tables"][1]["enable"]
                                        == True
                                    ):
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
                                            "thong": {
                                                "row": row_thong,
                                                "col": t + 4,
                                                "col_a": col_t if col_t != "?" else col_a,
                                                "isCol_a": False if col_t != "?" else True,
                                                "col_t": col_t
                                            },
                                        }
                                    )
                                # / End check col_c is first
                            else:
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
                                        "thong": {
                                            "row": row_thong,
                                            "col": t + 4,
                                            "col_a": col_t if col_t != "?" else col_a,
                                            "isCol_a": False if col_t != "?" else True,
                                            "col_t": col_t
                                        },
                                    }
                                )
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
                                    "thong": {
                                        "row": row_thong,
                                        "col": t + 4,
                                        "col_a": col_t if col_t != "?" else col_a,
                                        "isCol_a": False if col_t != "?" else True,
                                        "col_t": col_t
                                    },
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
                                "thong": {
                                    "row": row_thong,
                                    "col": t + 4,
                                    "col_a": col_t if col_t != "?" else col_a,
                                    "isCol_a": False if col_t != "?" else True,
                                    "col_t": col_t
                                },
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

    # TODO Add-on: GUI Thong Table
    def changeStatusBar(self, status, next):
        self.current_table = status
        title_text = self.get_title_text(next)
        self.title.setText(title_text)
        return

    def reload_widget(self):
        try:
            self.toggle_editable(True)
            self.handlerData()
            self.renderNavigation()
            self.renderTableCount()
            for i in range(10):
                data = self.ban_info["meta"]["tables"][i]
                if data["enable"]:
                    self.start_render_tables(i)
            self.focus_sheet()
        finally:
            self.toggle_editable(False)

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
        btn_notice = self.ban_info["meta"]["tables"][3]["btn_notice"] if "btn_notice" in self.ban_info["meta"]["tables"][3] else [[8, 36] for _ in range(120)]
        number_color = btn_notice[col_e_m3 - 1] #! Ban toan theo thong
        # number_color = notice_colorM4 #! Ban toan theo dong
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
                number_color[0],
                number_color[1],
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
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color,
                        "isColor": isNoticeColor,
                    }
                    if self.ban_info["meta"]["tables"][0]["enable"]
                    else None
                ),
                "actionM2": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m2,
                        "isColor": isNoticeColor_m2,
                    }
                    if self.ban_info["meta"]["tables"][1]["enable"]
                    else None
                ),
                "actionM3": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m3,
                        "isColor": isNoticeColor_m3,
                    }
                    if self.ban_info["meta"]["tables"][2]["enable"]
                    else None
                ),
                "notice": isNoticeColor_m4,
                "date": item_date,
                "color_value": col_e4,
                "col_d": col_e_m3,
                "thong": {
                    "row": row_thong,
                    "col": t + 4,
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
        btn_notice = self.ban_info["meta"]["tables"][4]["btn_notice"] if "btn_notice" in self.ban_info["meta"]["tables"][4] else [[8, 36] for _ in range(120)]
        number_color = btn_notice[col_e_m4 - 1]  #! Ban toan theo thong
        # number_color = notice_colorM5 #! Ban toan theo dong
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
                number_color[0],
                number_color[1],
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
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color,
                        "isColor": isNoticeColor,
                    }
                    if self.ban_info["meta"]["tables"][0]["enable"]
                    else None
                ),
                "actionM2": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m2,
                        "isColor": isNoticeColor_m2,
                    }
                    if self.ban_info["meta"]["tables"][1]["enable"]
                    else None
                ),
                "actionM3": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m3,
                        "isColor": isNoticeColor_m3,
                    }
                    if self.ban_info["meta"]["tables"][2]["enable"]
                    else None
                ),
                "actionM4": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m4,
                        "isColor": isNoticeColor_m4,
                    }
                    if self.ban_info["meta"]["tables"][3]["enable"]
                    else None
                ),
                "notice": isNoticeColor_m5,
                "date": item_date,
                "color_value": col_e5,
                "col_d": col_e_m4,
                "thong": {
                    "row": row_thong,
                    "col": t + 4,
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
        btn_notice = self.ban_info["meta"]["tables"][5]["btn_notice"] if "btn_notice" in self.ban_info["meta"]["tables"][5] else [[8, 36] for _ in range(120)]
        number_color = btn_notice[col_e_m5 - 1] #! Ban toan theo thong
        # number_color = notice_colorM6 #! Ban toan theo dong
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
                number_color[0],
                number_color[1],
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
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color,
                        "isColor": isNoticeColor,
                    }
                    if self.ban_info["meta"]["tables"][0]["enable"]
                    else None
                ),
                "actionM2": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m2,
                        "isColor": isNoticeColor_m2,
                    }
                    if self.ban_info["meta"]["tables"][1]["enable"]
                    else None
                ),
                "actionM3": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m3,
                        "isColor": isNoticeColor_m3,
                    }
                    if self.ban_info["meta"]["tables"][2]["enable"]
                    else None
                ),
                "actionM4": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m4,
                        "isColor": isNoticeColor_m4,
                    }
                    if self.ban_info["meta"]["tables"][3]["enable"]
                    else None
                ),
                "actionM5": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m5,
                        "isColor": isNoticeColor_m5,
                    }
                    if self.ban_info["meta"]["tables"][4]["enable"]
                    else None
                ),
                "notice": isNoticeColor_m6,
                "date": item_date,
                "color_value": col_e6,
                "col_d": col_e_m5,
                "thong": {
                    "row": row_thong,
                    "col": t + 4,
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
        btn_notice = self.ban_info["meta"]["tables"][6]["btn_notice"] if "btn_notice" in self.ban_info["meta"]["tables"][6] else [[8, 36] for _ in range(120)]
        number_color = btn_notice[col_e_m6 - 1] #! Ban toan theo thong
        # number_color = notice_colorM7 #! Ban toan theo dong
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
                number_color[0],
                number_color[1],
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
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color,
                        "isColor": isNoticeColor,
                    }
                    if self.ban_info["meta"]["tables"][0]["enable"]
                    else None
                ),
                "actionM2": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m2,
                        "isColor": isNoticeColor_m2,
                    }
                    if self.ban_info["meta"]["tables"][1]["enable"]
                    else None
                ),
                "actionM3": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m3,
                        "isColor": isNoticeColor_m3,
                    }
                    if self.ban_info["meta"]["tables"][2]["enable"]
                    else None
                ),
                "actionM4": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m4,
                        "isColor": isNoticeColor_m4,
                    }
                    if self.ban_info["meta"]["tables"][3]["enable"]
                    else None
                ),
                "actionM5": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m5,
                        "isColor": isNoticeColor_m5,
                    }
                    if self.ban_info["meta"]["tables"][4]["enable"]
                    else None
                ),
                "actionM6": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m6,
                        "isColor": isNoticeColor_m6,
                    }
                    if self.ban_info["meta"]["tables"][5]["enable"]
                    else None
                ),
                "notice": isNoticeColor_m7,
                "date": item_date,
                "color_value": col_e7,
                "col_d": col_e_m6,
                "thong": {
                    "row": row_thong,
                    "col": t + 4,
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
        btn_notice = self.ban_info["meta"]["tables"][7]["btn_notice"] if "btn_notice" in self.ban_info["meta"]["tables"][7] else [[8, 36] for _ in range(120)]
        number_color = btn_notice[col_e_m7 - 1] #! Ban toan theo thong
        # number_color = notice_colorM8 #! Ban toan theo dong
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
                number_color[0],
                number_color[1],
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
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}/{col_e_m8}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color,
                        "isColor": isNoticeColor,
                    }
                    if self.ban_info["meta"]["tables"][0]["enable"]
                    else None
                ),
                "actionM2": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m2,
                        "isColor": isNoticeColor_m2,
                    }
                    if self.ban_info["meta"]["tables"][1]["enable"]
                    else None
                ),
                "actionM3": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m3,
                        "isColor": isNoticeColor_m3,
                    }
                    if self.ban_info["meta"]["tables"][2]["enable"]
                    else None
                ),
                "actionM4": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m4,
                        "isColor": isNoticeColor_m4,
                    }
                    if self.ban_info["meta"]["tables"][3]["enable"]
                    else None
                ),
                "actionM5": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m5,
                        "isColor": isNoticeColor_m5,
                    }
                    if self.ban_info["meta"]["tables"][4]["enable"]
                    else None
                ),
                "actionM6": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m6,
                        "isColor": isNoticeColor_m6,
                    }
                    if self.ban_info["meta"]["tables"][5]["enable"]
                    else None
                ),
                "actionM7": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m7,
                        "isColor": isNoticeColor_m7,
                    }
                    if self.ban_info["meta"]["tables"][6]["enable"]
                    else None
                ),
                "notice": isNoticeColor_m8,
                "date": item_date,
                "color_value": col_e8,
                "col_d": col_e_m7,
                "thong": {
                    "row": row_thong,
                    "col": t + 4,
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
        btn_notice = self.ban_info["meta"]["tables"][8]["btn_notice"] if "btn_notice" in self.ban_info["meta"]["tables"][8] else [[8, 36] for _ in range(120)]
        number_color = btn_notice[col_e_m8 - 1] #! Ban toan theo thong
        # number_color = notice_colorM9 #! Ban toan theo dong
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
                number_color[0],
                number_color[1],
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
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}/{col_e_m8}/{col_e_m9}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color,
                        "isColor": isNoticeColor,
                    }
                    if self.ban_info["meta"]["tables"][0]["enable"]
                    else None
                ),
                "actionM2": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m2,
                        "isColor": isNoticeColor_m2,
                    }
                    if self.ban_info["meta"]["tables"][1]["enable"]
                    else None
                ),
                "actionM3": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m3,
                        "isColor": isNoticeColor_m3,
                    }
                    if self.ban_info["meta"]["tables"][2]["enable"]
                    else None
                ),
                "actionM4": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m4,
                        "isColor": isNoticeColor_m4,
                    }
                    if self.ban_info["meta"]["tables"][3]["enable"]
                    else None
                ),
                "actionM5": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m5,
                        "isColor": isNoticeColor_m5,
                    }
                    if self.ban_info["meta"]["tables"][4]["enable"]
                    else None
                ),
                "actionM6": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m6,
                        "isColor": isNoticeColor_m6,
                    }
                    if self.ban_info["meta"]["tables"][5]["enable"]
                    else None
                ),
                "actionM7": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m7,
                        "isColor": isNoticeColor_m7,
                    }
                    if self.ban_info["meta"]["tables"][6]["enable"]
                    else None
                ),
                "actionM8": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m8,
                        "isColor": isNoticeColor_m8,
                    }
                    if self.ban_info["meta"]["tables"][7]["enable"]
                    else None
                ),
                "notice": isNoticeColor_m9,
                "date": item_date,
                "color_value": col_e9,
                "col_d": col_e_m8,
                "thong": {
                    "row": row_thong,
                    "col": t + 4,
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
        btn_notice = self.ban_info["meta"]["tables"][9]["btn_notice"] if "btn_notice" in self.ban_info["meta"]["tables"][9] else [[8, 36] for _ in range(120)]
        number_color = btn_notice[col_e_m9 - 1] #! Ban toan theo thong
        # number_color = notice_colorM10 #! Ban toan theo dong
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
                number_color[0],
                number_color[1],
            )
            find_null_color_m10 = 0
            find_stt_color_m10 = stt_count_with_d_m10 - 1
            find_next_color_m10 = self.find_column_by_index(
                self.ban_info["meta"]["tables"][9]["col_d"],
                col_e_m9 - value1_10,
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
                "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t if col_t else "?"}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}/{col_e_m5}/{col_e_m6}/{col_e_m7}/{col_e_m8}/{col_e_m9}/{col_e_m10}",
                "color": isEqual,
                "action": {
                    "name": "count",
                    "row": countRow,
                    "col": total_column,
                    "isColor": isNoticeCount,
                },
                "actionM1": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color,
                        "isColor": isNoticeColor,
                    }
                    if self.ban_info["meta"]["tables"][0]["enable"]
                    else None
                ),
                "actionM2": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m2,
                        "isColor": isNoticeColor_m2,
                    }
                    if self.ban_info["meta"]["tables"][1]["enable"]
                    else None
                ),
                "actionM3": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m3,
                        "isColor": isNoticeColor_m3,
                    }
                    if self.ban_info["meta"]["tables"][2]["enable"]
                    else None
                ),
                "actionM4": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m4,
                        "isColor": isNoticeColor_m4,
                    }
                    if self.ban_info["meta"]["tables"][3]["enable"]
                    else None
                ),
                "actionM5": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m5,
                        "isColor": isNoticeColor_m5,
                    }
                    if self.ban_info["meta"]["tables"][4]["enable"]
                    else None
                ),
                "actionM6": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m6,
                        "isColor": isNoticeColor_m6,
                    }
                    if self.ban_info["meta"]["tables"][5]["enable"]
                    else None
                ),
                "actionM7": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m7,
                        "isColor": isNoticeColor_m7,
                    }
                    if self.ban_info["meta"]["tables"][6]["enable"]
                    else None
                ),
                "actionM8": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m8,
                        "isColor": isNoticeColor_m8,
                    }
                    if self.ban_info["meta"]["tables"][7]["enable"]
                    else None
                ),
                "actionM9": (
                    {
                        "name": "color",
                        "row": countRow,
                        "col": col_color_m9,
                        "isColor": isNoticeColor_m9,
                    }
                    if self.ban_info["meta"]["tables"][8]["enable"]
                    else None
                ),
                "notice": isNoticeColor_m10,
                "date": item_date,
                "color_value": col_e10,
                "col_d": col_e_m9,
                "thong": {
                    "row": row_thong,
                    "col": t + 4,
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
        try:
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
        finally:
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

    # TODO Excel Function
    def toggle_editable(self, enable_edit: bool):
        """Bật/Tắt chế độ chỉnh sửa nhưng vẫn cho phép thay đổi định dạng"""
        try:
            # Tắt screen updating để tăng tốc độ
            self.wb.app.screen_updating = False
            self.wb.app.enable_events = False
            
            for sheet in self.wb.sheets:
                try:
                    # Bỏ bảo vệ sheet hiện tại
                    sheet.api.Unprotect(Password=self.pwd)
                except:
                    # Bỏ qua nếu sheet không được bảo vệ
                    pass
                
                # Lấy vùng dữ liệu
                last_row = sheet.range("A1").end("down").row
                last_col = sheet.range("A1").end("right").column
                table_range = sheet.range((1, 1), (last_row, last_col))
                
                if enable_edit:
                    # Mở khóa toàn bộ sheet
                    table_range.api.Locked = False
                    # Không bảo vệ lại sheet khi enable_edit=True
                else:
                    # Khóa toàn bộ sheet
                    table_range.api.Locked = True
                    # Bảo vệ lại sheet với các tùy chọn
                    sheet.api.Protect(
                        Password=self.pwd,
                        AllowFormattingCells=True,
                        AllowFormattingColumns=True,
                        AllowFormattingRows=True,
                        UserInterfaceOnly=True  # Cho phép VBA/Python thay đổi
                    )
        finally:
            # Bật lại screen updating
            self.wb.app.screen_updating = True
            self.wb.app.enable_events = True

    def closeEvent(self, event):
        try:
            """Xử lý khi cửa sổ PySide6 đóng"""
            if self.wb:
                self.wb.close()  # Đóng workbook mà không lưu
            if self.app:
                self.app.quit()  # Đóng Excel ngay lập tức
            event.accept()  # Chấp nhận sự kiện đóngB
        except Exception as e:
            print(f"Lỗi khi đóng Excel: {str(e)}")

    def focus_sheet(self, sheet_index=0):
        """
        Focus vào sheet được chỉ định
        :param sheet_index: index của sheet (mặc định là 0 - sheet đầu tiên)
        """
        try:
            self.wb.app.screen_updating = False
            
            # Kiểm tra index hợp lệ
            if sheet_index < 0 or sheet_index >= len(self.wb.sheets):
                print(f"Sheet index {sheet_index} không hợp lệ")
                return False
                
            target_sheet = self.wb.sheets[sheet_index]
            
            # Focus vào sheet
            try:
                target_sheet.select()
                target_sheet.activate()
            except Exception as e:
                print(f"Không thể focus vào sheet: {e}")
                return False
                
            # Scroll về ô A1 (tùy chọn)
            try:
                target_sheet.range('A1').select()
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"Lỗi trong quá trình focus sheet: {e}")
            return False
            
        finally:
            self.wb.app.screen_updating = True

    def get_column_name(self, col_num):
        """Chuyển đổi số cột thành tên cột Excel (A, B, C, ..., AA, AB, ...)"""
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + 65) + result
            col_num //= 26
        return result

    def add_vba_code(self):
        try:
            basedir = os.path.dirname(__file__)
            file_path = os.path.join(basedir,"..", "module.txt")
            with open(file_path, "r", encoding="utf-8") as file:
                vba_code = file.read().strip()  # Read the file content and strip whitespace
            self.wb.api.VBProject.VBComponents.Add(1).CodeModule.AddFromString(vba_code)
            return True
        except Exception as e:
            print(f"Không thể add Module vào VBA: {e}")
            return False

    def add_vba_code_sheets(self):
        try:
            basedir = os.path.dirname(__file__)
            file_path = os.path.join(basedir, "..", "sheet.txt")
            
            with open(file_path, "r", encoding="utf-8") as file:
                vba_code = file.read().strip()

            for sheet in self.wb.sheets:
                sheetIndex = sheet.api.Index
                code_module = self.wb.api.VBProject.VBComponents.Item(f"Sheet{sheetIndex}").CodeModule
                code_module.AddFromString(vba_code)

        except Exception as e:
            print(f"Không thể add VBA Code vào Sheet: {e}")
            return False

    def save_color_old_cell(self, item, sheet):
        # / Khoi phuc du lieu mau neu co
        if self.lastAddress != "":
            lastItem = self.lastSheetName.range(self.lastAddress)
            lastItem.color = self.lastColor
            lastItem.font.color = self.lastFontColor

        # / Save du lieu mau o cu
        self.lastAddress = item.address
        self.lastSheetName = sheet
        self.lastColor = item.color
        self.lastFontColor = item.font.color

        item.font.color = (255, 255, 255)
        item.color = (255, 0, 0)
        item.select()
