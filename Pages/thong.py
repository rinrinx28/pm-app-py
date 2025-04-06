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
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QSpinBox,
)
from PySide6.QtGui import Qt, QCursor, QIcon, QColor
from Pages.components.stylesheet import (
    css_button_cancel,
    css_button_submit,
    css_input,
    Font,
    Note,
    css_lable,
    SendMessage,
    css_title,css_button_start
)
import json
from Controller.handler import (
    saveThong,
    backupThong,
    saveAllThong,
    typeWithRecipe,
    saveBackupThong,convert_string_format,convert_string_format_type,changeThongPerLuot
)
import os
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread
import xlwings as xw
import pandas as pd
import math


class ThongPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()

        self.layout_thong = QVBoxLayout(self)
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )
        logo_path = self.path.path_logo()
        icon = QIcon(logo_path)
        # Setting application icon
        self.setWindowIcon(icon)

        # / Kết nối với Excel
        self.app = xw.App(visible=True)  # Mở Excel
        self.wb = self.app.books.active  # Workbook hiện tại
        self.sheet = self.wb.sheets[0]   # Sheet đầu tiên
        
        # Xác định phạm vi bảng (tự động tìm kích thước bảng)
        last_row = self.sheet.range("A1").end("down").row
        last_col = self.sheet.range("A1").end("right").column
        self.table_range = self.sheet.range((1, 1), (last_row, last_col))

        # 🌟 **Áp dụng định dạng cho toàn bảng**
        self.table_range.api.Font.Name = "Arial"  # Font chữ
        self.table_range.api.Font.Size = 24  # Cỡ chữ
        self.table_range.api.HorizontalAlignment = -4108  # Căn giữa
        self.table_range.api.VerticalAlignment = -4107  # Căn giữa theo chiều dọc
        self.table_range.api.Borders.Weight = 2  # Độ dày đường viền
        self.table_range.api.Font.Bold = True  # In đậm tiêu đề
        self.table_range.api.NumberFormat = "@"

        self.pwd = "rindev-pm"

        # / Load Data Bans
        self.bans_path = self.path.path_db()
        with open(self.bans_path, "r") as file:
            self.bans_db = json.load(file)

        self.ban_info = self.bans_db

        # / Load data thong
        self.thong_path = self.path.path_thong()
        self.current_dir = self.path.current_dir

        with open(os.path.join(self.thong_path, "thongs.json"), "r") as file:
            self.thong_db = json.load(file)

        thong_sp_path = self.path.path_thong_sp_with_id(self.thong_db["id"])
        with open(thong_sp_path, 'r') as file:
            self.thong_sp = json.load(file)
            
        with open(os.path.join(self.current_dir, "db", 'stay.json'), "r") as file:
            self.stay = json.load(file)
        # / Config LoadingScreen
        self.loadingScreen = LoadingScreen(self.path.path_loading())

        # / Config Secleted item
        self.selected_row_indices = None
        self.current_select = []
        self.prev_selected_row = None
        self.cyan = QColor(178, 255, 255)
        self.normal = QColor("#FFFFFF")
        self.stt_highlight = QColor("#EDEADE")
        self.color_col_stt = QColor("#fb80ff")

        # / Config Font
        self.font = Font()
        self.layout_thong.setSpacing(0)
        # / Widget Main
        self.widget_main = QStackedWidget()
        self.layout_thong.addWidget(self.widget_main)

        # / Config ABC Setting
        self.isShow = False

        # / Table Main
        self.table_main = None

        # / handler count thong
        self.handler = []
        self.word = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]

        # / Button Main
        self.button_wid_main = QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.button_layout.setSpacing(100)
        self.layout_thong.addWidget(self.button_wid_main)

        # / Render Component
        current_number = self.stay.get('thong', 0)
        if current_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            current_number = current_ban_info_number
        self.changeDataThongWithNumber(current_number)
        self.update_excel()
        self.renderInfoPage()
        self.renderThongButton()

    # TODO Handler Render Component
    def renderInfoPage(self):
        value_thong = self.thong_db["value"]
        self.start_col = 0
        self.value_col = 0
        colCount = value_thong
        # / Title and table
        widget_table = QWidget()
        layout_table = QVBoxLayout(widget_table)
        self.widget_main.addWidget(widget_table)

        layout_table.setSpacing(0)
        layout_table.setContentsMargins(0, 0, 0, 0)
        # / Title
        ban_info = self.ban_info
        filter_data = [entry for entry in ban_info["data"] if not entry["isDeleted"]]
        row_count = len(filter_data)
        max_row = ban_info["meta"]["maxRow"]
        change_number = ban_info["meta"]["number"]
        ban_col = ban_info["col"]
        ban_thong_value = ban_info["thong"]["value"]
        ban_thong_name = ban_info["thong"]["name"]

        
        name = convert_string_format(ban_thong_name)
        self.name = convert_string_format_type(ban_thong_name)
        co_so = change_number if change_number != 0 else "gốc"
        title_text_stt = (
            f"Trạng Thái Bảng Tính: C{ban_col[0]} đến C{ban_col[1]} / T{ban_thong_value[0]} đến "
            + f"T{ban_thong_value[1]} /  Cơ {co_so} / "
            + f"Số dòng: {row_count}/{max_row}"
        )
        title_stt = QLabel(title_text_stt)
        title_stt.setStyleSheet(css_title)
        title_stt.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_text_table = f"Bảng Thông: {name} - {colCount} Thông"
        title_table = QLabel(title_text_table)
        title_table.setStyleSheet(css_title)
        title_table.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_table.addWidget(title_table)
        layout_table.addWidget(title_stt)

        # / Note
        current_number = self.stay.get('thong', 0)
        if current_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            current_number = current_ban_info_number
        if current_number != 0:
           current_number -= 1
        else:
            current_number = 10
        note = Note[current_number]
        note_name = current_number if change_number != 0 else "gốc"
        self.note = QLabel(f"Cơ {note_name} - {note}")
        self.note.setFont(self.font)
        layout_table.addWidget(self.note)

    def renderThongButton(self):
        self.button_wid_main = QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.layout_thong.addWidget(self.button_wid_main)
        self.showButtonThong()

    def showButtonThong(self):
        layout_w = QWidget()
        layout = QGridLayout(layout_w)
        layout.setSpacing(6)
        self.button_layout.addWidget(layout_w)

        # TODO Line 1
        # / Back to first row
        backToFirst = QPushButton("Về Cột Đầu")
        backToFirst.setStyleSheet(css_button_start)
        backToFirst.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(backToFirst, 0, 0)
        # / Create MathCount
        swapRow = QPushButton("Đổi Dòng DL")
        swapRow.setStyleSheet(css_button_cancel)
        swapRow.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(swapRow, 0, 1)

        # / Copy Row Button
        CopyRow = QPushButton("Chép Dòng DL")
        CopyRow.setStyleSheet(css_button_cancel)
        CopyRow.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(CopyRow, 0, 2)
        

        # / Skip to mid row
        skipToMind = QPushButton("Về Cột Giữa")
        skipToMind.setStyleSheet(css_button_start)
        skipToMind.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(skipToMind, 0, 3)

        # / Create Delete
        DeleteRow = QPushButton("Xóa DL dòng")
        DeleteRow.setStyleSheet(css_button_cancel)
        DeleteRow.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(DeleteRow, 0, 4)

        # / Create Delete
        Delete = QPushButton("Xóa tất cả DL")
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(Delete, 0, 5)

        # / Create Delete
        DeleteColor = QPushButton("Xóa Màu")
        DeleteColor.setStyleSheet(css_button_cancel)
        DeleteColor.setCursor(QCursor(Qt.PointingHandCursor))
        # layout.addWidget(DeleteColor, 0, 6)

        # / Create ChangeNumber
        self.ChangeNumber = QComboBox()
        self.ChangeNumber.setStyleSheet("font-size: 24px;line-height: 32px;")
        self.ChangeNumber.setCursor(QCursor(Qt.PointingHandCursor))
        self.ChangeNumber.addItem(f"Cơ gốc")
        for i in range(1, 11):
            self.ChangeNumber.addItem(f"Cơ {i}")
        layout.addWidget(self.ChangeNumber, 0, 6)

        # / Skip to end row
        skipToEnd = QPushButton("Về Cột Cuối")
        skipToEnd.setStyleSheet(css_button_start)
        skipToEnd.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(skipToEnd, 0, 7)

        # TODO Line 2

        # / Create Backup
        save_back_up = QPushButton("Đặt DL gốc")
        save_back_up.setStyleSheet(css_button_submit)
        save_back_up.setCursor(QCursor(Qt.PointingHandCursor))
        # layout.addWidget(save_back_up, 1, 0)
        # / Backup
        BackUp = QPushButton("Khôi phục DL gốc")
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        # layout.addWidget(BackUp, 1, 1)

        # / Create AutoSaveFiles
        SaveFile = QPushButton("Đồng Bộ DL")
        SaveFile.setStyleSheet(css_button_submit)
        SaveFile.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(SaveFile, 1, 0)

        # / Create HandlerData
        type_input = "Tắt Tùy Chỉnh"
        self.HandlerData = QPushButton(type_input)
        self.HandlerData.setStyleSheet(css_button_submit)
        self.HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.HandlerData, 1, 1)

        # / Create SaveData
        SaveData = QPushButton("Lưu")
        SaveData.setStyleSheet(css_button_submit)
        SaveData.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(SaveData, 1, 2)

        # / Create Backup
        ThongInput = QPushButton("Nhập Liệu B Thông")
        ThongInput.setStyleSheet(css_button_submit)
        ThongInput.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(ThongInput, 1, 3)

        # / Hidden or show
        self.hidden = QPushButton("Hiện ABCD Gốc")
        self.hidden.setStyleSheet(css_button_submit)
        self.hidden.setCursor(Qt.PointingHandCursor)
        self.hidden.clicked.connect(self.button_show_abc)
        self.hidden.setFixedWidth(200)
        # layout.addWidget(self.hidden, 1, 4)

        # / Create SaveData
        SettingType = QPushButton("Cài Đặt Thông")
        SettingType.setStyleSheet(css_button_submit)
        SettingType.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(SettingType, 1, 4)

        def changeTypeCount():
            types = self.HandlerData.text()
            if types == "Tắt Tùy Chỉnh":
                self.toggle_editable(True)
                self.HandlerData.setText("Bật Tùy Chỉnh")
            else:
                self.toggle_editable(False)
                self.HandlerData.setText("Tắt Tùy Chỉnh")

        def saveChange():
            self.toggle_editable(False)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
            if self.ChangeNumber.currentIndex() == 0:
                self.saveBackUp()
            else:
                self.saveThongRow()

        def changeTableNumber():
            # / Check isEditor
            self.toggle_editable(True)
            self.HandlerData.setText("Tắt Tùy Chỉnh")

            value = self.ChangeNumber.currentIndex()
            text = self.ChangeNumber.currentText()
            self.save_stay(value)
            self.changeDataThongWithNumber(value)
            self.update_excel()
            if value != 0:
                note = Note[value - 1]
                self.note.setText(f"Cơ {value} - {note}")
            else:
                note = Note[10]
                self.note.setText(f"Cơ gốc - {note}")
            SendMessage(f"Bạn đã mở {text}")

        def copyRow_Click():
            # Lấy đối tượng App từ Workbook
            app = self.sheet.book.app
            try:
                # Lấy vùng được chọn
                selection = app.selection
                if selection is None:
                    SendMessage("Vui lòng chọn ít nhất một dòng!")
                    return None

                # Lấy tất cả các dòng từ các vùng chọn, giữ nguyên thứ tự
                selected_rows = []
                seen_rows = set()  # Để kiểm tra trùng lặp mà không thay đổi thứ tự
                for area in selection.api.Areas:  # Duyệt qua từng vùng chọn riêng lẻ
                    for row in area.Rows:  # Duyệt qua từng dòng trong vùng
                        row_num = row.Row  # Không trừ 1 để giữ nguyên số dòng Excel
                        if row_num not in seen_rows:  # Chỉ thêm nếu chưa gặp
                            selected_rows.append(row_num)
                            seen_rows.add(row_num)

                # In danh sách dòng và kiểm tra số lượng
                print(f"Các dòng được chọn (theo thứ tự): {selected_rows}")
                if len(selected_rows) != 2:  # Yêu cầu đúng 2 dòng
                    SendMessage("Xin vui lòng chọn đúng 2 dòng để tiến hành sao chép dữ liệu!")
                    return None

                # Gọi hàm sao chép với danh sách dòng giữ nguyên thứ tự
                self.copyRowThong(selected_rows)
                return selected_rows

            except AttributeError as e:
                print(f"Lỗi truy cập vùng chọn: {e}")
                SendMessage("Không thể truy cập vùng chọn. Vui lòng thử lại!")
                return None
            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")
                SendMessage("Không thể sao chép dữ liệu. Vui lòng thử lại!")
                return None
            
        def saveFile_click():
            self.showQuestion()

        def type_with_button():
            # / Check isEditor
            self.toggle_editable(True)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
            number_thong = self.ChangeNumber.currentIndex()
            if number_thong != 0:
                SendMessage("Chú ý khi nhập liệu phải về bảng thông gốc!")
                return
            
            # Lấy đối tượng App từ Workbook
            app = self.sheet.book.app
            try:
                # Lấy vùng được chọn
                selection = app.selection
                if selection is None:
                    SendMessage("Vui lòng chọn ít nhất một dòng!")
                    return None

                # Lấy tất cả các dòng từ các vùng chọn, giữ nguyên thứ tự
                selected_rows = []
                seen_rows = set()  # Để kiểm tra trùng lặp mà không thay đổi thứ tự
                for area in selection.api.Areas:  # Duyệt qua từng vùng chọn riêng lẻ
                    for row in area.Rows:  # Duyệt qua từng dòng trong vùng
                        row_num = row.Row  # Không trừ 1 để giữ nguyên số dòng Excel
                        if row_num not in seen_rows:  # Chỉ thêm nếu chưa gặp
                            selected_rows.append(row_num)
                            seen_rows.add(row_num)

                # In danh sách dòng và kiểm tra số lượng
                if len(selected_rows) < 1:  # Yêu cầu đúng 2 dòng
                    SendMessage("Xin vui lòng chọn tối thiểu 1 dòng để tiến hành nhập dữ liệu!")
                    return None

                # Gọi hàm sao chép với danh sách dòng giữ nguyên thứ tự
                self.get_change_history()
                for row in selected_rows:
                    row_index = row - 3
                    # setting = 1 if self.thong_db["type_count"] == 3 else 1 if self.thong_db["type_count"] == 0 else self.thong_db["type_count"]
                    data = {}
                    data["row"] = row_index
                    data["number"] = self.ban_info["meta"]['number']
                    data["setting"] = 1
                    data["stt"] = self.thong_db["stt"]
                    data["type_count"] = self.thong_db["type_count"]
                    data["value"] = self.thong_db["value"]
                    data["thong_per_luot"] = self.thong_db["thong_per_luot"]
                    data["update"] = self.thong_data
                    data["thong_sp"] = self.thong_sp

                    result = typeWithRecipe(data)
                    self.thong_data = result["update"]
                    self.thong_sp = result["thong_sp"]

                self.show_loading_screen()
                self.thread = Thread()
                self.thread.task_completed.connect(
                    lambda: self.updateWidget([self.update_excel])
                )
                self.thread.task_completed.connect(
                    lambda: SendMessage("Bạn đã nhập liệu thành công")
                )
                self.thread.start()

            except AttributeError as e:
                print(f"Lỗi truy cập vùng chọn: {e}")
                SendMessage("Không thể truy cập vùng chọn. Vui lòng thử lại!")
                return None
            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")
                SendMessage("Không thể nhập dữ liệu tự động. Vui lòng thử lại!")
                return None

        def move_cursor(position: str):
            """
            Di chuyển con trỏ đến vị trí được chỉ định trong cột: "first", "middle", "last"
            """
            self.get_change_history()
            data_range = self.sheet.range("F2").expand("right")  # Lấy phạm vi dữ liệu theo cột
            total_cols = data_range.columns.count  # Số cột trong bảng

            if total_cols == 0:
                return  # Không có dữ liệu thì không làm gì cả

            if position == "first":
                col_index = 6  # Cột đầu tiên (A)
            elif position == "middle":
                col_index = (int(total_cols) / 2) + 1  # Cột giữa
            elif position == "last":
                col_index = total_cols  # Cột cuối cùng
            else:
                SendMessage("Vị trí không hợp lệ!")
                return

            cell = self.sheet.cells(2, col_index)  # Chọn ô đầu tiên của cột tương ứng (hàng 2)
            cell.api.Activate()  # Di chuyển con trỏ đến ô đó

        backToFirst.clicked.connect(lambda: move_cursor("first")) # Về Cột Đầu
        swapRow.clicked.connect(self.swapThongRow) # Đổi Dòng DL
        CopyRow.clicked.connect(copyRow_Click) # Chép Dòng DL
        skipToMind.clicked.connect(lambda: move_cursor("middle")) # Về Cột Giữa
        DeleteRow.clicked.connect(self.DeleteThongRow) # Xóa DL dòng
        Delete.clicked.connect(self.delete_all_rows) # Xóa tất cả DL
        DeleteColor.clicked.connect(self.delete_color_click) # Xóa Màu (Bỏ)
        self.ChangeNumber.currentIndexChanged.connect(changeTableNumber) # Chọn bộ chuyển đổi
        skipToEnd.clicked.connect(lambda: move_cursor("last")) # Về cột cuối
        save_back_up.clicked.connect(self.saveBackUp) # Đặt DL gốc (Bỏ)
        BackUp.clicked.connect(self.backUpRows) # Khôi phục DL gốc (Bỏ)
        SaveFile.clicked.connect(saveFile_click) # Đồng Bộ DL
        self.HandlerData.clicked.connect(changeTypeCount) # Bật/Tắt Tùy Chỉnh
        SaveData.clicked.connect(saveChange) # Lưu
        ThongInput.clicked.connect(type_with_button) # Nhập liệu Thông
        SettingType.clicked.connect(self.setting_type_click) # Cài đặt thông

        
        # Default value
        current_number = self.stay.get('thong', 0)
        if current_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            current_number = current_ban_info_number
        self.ChangeNumber.setCurrentIndex(current_number)
    
    def save_stay(self, value):
        self.ban_info["meta"]['number'] = int(value)
        self.stay['thong'] = int(value)
        with open(os.path.join(self.current_dir, "db", 'stay.json'), "w") as file:
            json.dump(self.stay, file)

    # TODO Handler Widgets
    def delete_color_click(self):
        self.table_main.clearSelection()
        self.selected_row_indices = None
        self.prev_selected_row = None
        self.current_select = []

    def updateHeaderRow(self):
        value_thong = self.thong_db["value"]
        thong_per_luot = self.thong_db["thong_per_luot"]
        isThong_one = 200

        # Setting header Thong

        steps = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 0, 1, 2, 3],
            [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],
            [7, 8, 9, 0, 1, 2, 3, 4, 5, 6],
            [8, 9, 0, 1, 2, 3, 4, 5, 6, 7],
            [2, 3, 4, 5, 6, 7, 8, 9, 0, 1],
            [5, 6, 7, 8, 9, 0, 1, 2, 3, 4],
            [9, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        ]

        # Initialize modifications for array a in each step
        modifications_a = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        ]
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
            num_sets = 10
            # Số lượt trong mỗi tập
            rounds_per_set = 10
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
            thong_header_label = [f"T.{thong + 1}" for thong in range(total_columns)]
        
        header_labels = ["A", "B", "C", "D"] + thong_header_label
        return header_labels

    def updateRowAndColumns(self):
        # Lấy dữ liệu cần thiết
        meta_number = self.stay.get('thong', 0)
        if meta_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            meta_number = current_ban_info_number

        stt = self.thong_db["stt"][meta_number]
        data_value = self.thong_db["data"]
        thong_data = self.thong_data

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
        for tap_index in range(10):
            for luot_title in range(10):  # Mỗi tập có 10 lượt
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
            for tap_index in range(10):
                for luot in range(10):
                    luot_index = tap_index * 10 + luot
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

    def delete_all_rows(self):
        rowCount = len(self.thong_data[0])
        self.toggle_editable(True)
        self.HandlerData.setText("Tắt Tùy Chỉnh")

        # * Delete du lieu Thong data * thong sp
        for row in range(rowCount):
            for i in range(len(self.thong_data)):
                self.thong_data[i][row] = ""

            isThong_one = True
            if isThong_one:
                for i in range(len(self.thong_sp[0])):
                    self.thong_sp[row][i] = ["",""]

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.update_excel]))
        self.thread.task_completed.connect(
            lambda: SendMessage("Bạn đã xóa toàn bộ dữ liệu thành công")
        )
        self.thread.start()
    
    def delete_all_row_custom(self):
        data_value = self.thong_db["data"]
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")

        for i in range(len(self.thong_data)):
            for j in range(len(self.thong_data[i])):
                self.thong_data[i][j] = ""

        for i in range(len(data_value)):
            value_col = data_value[i]
            for j in range(len(value_col)):
                item = self.table_main.item(j, i)
                item.setText(value_col[j])

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([]))
        self.thread.task_completed.connect(
            lambda: SendMessage("Bạn đã xóa toàn bộ dữ liệu thành công")
        )
        self.thread.start()

    def saveBackUp(self):
        number = self.ban_info["meta"]['number']
        if number != 0:
            SendMessage(f"Không thể đặt DL gốc ở bộ chuyển đổi {number}")
            return
        self.get_change_history()
        data = {}
        data["data"] = self.thong_db
        data["thong_data"] = self.thong_data
        data["thong_sp"] = self.thong_sp

        res = saveBackupThong(data)
        self.thong_data = res["thong_data"]
        self.thong_db = res["thong_info"]

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([])
        )
        self.thread.task_completed.connect(
            lambda: SendMessage("Bạn đã lưu DL gốc thành công")
        )
        self.thread.start()

    def backUpRows(self):
        # / Load BackUp File with ID
        id = self.thong_db["id"]
        data = backupThong({"number": self.ban_info["meta"]['number'], "id": id})
        self.thong_db = data["thong_info"]
        self.thong_data = data["thong_data"]

        # / Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")

        # / Render Rows table

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.updateRowAndColumns])
        )
        self.thread.task_completed.connect(
            lambda: SendMessage("Bạn đã khôi phục toàn bộ dữ liệu thành công")
        )
        self.thread.start()

    def saveThongRow(self):
        self.get_change_history()
        data = {}
        data["data"] = self.thong_db
        data["update"] = self.thong_data
        data["number"] = self.ban_info["meta"]['number']

        msg = saveThong(data)

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([])
        )
        self.thread.task_completed.connect(
            lambda: SendMessage(msg)
        )
        self.thread.start()

    def swapThongRow(self):
        # / Check isEditor
        self.toggle_editable(True)
        self.HandlerData.setText("Tắt Tùy Chỉnh")
        # / Thong Data and Thong info
        current_number = self.ChangeNumber.currentIndex()
        stt = self.thong_db["stt"][current_number]
        data = self.thong_data
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

        # shifted of thong sp
        thong_sp = self.thong_sp
        part1_thong_sp = thong_sp[:100]
        part2_thong_sp = thong_sp[100:]
        shifted_thong_sp_part1 = [None] * len(part1_thong_sp)
        for i in range(len(part1_thong_sp)):
            shifted_thong_sp_part1[(i + 1) % len(part1_thong_sp)] = part1_thong_sp[i]

        shifted_thong_sp = shifted_thong_sp_part1 + part2_thong_sp

        current_number = self.ChangeNumber.currentIndex()
        self.thong_db["stt"][current_number] = shifted_stt
        self.thong_data = shifted_data
        self.thong_sp = shifted_thong_sp

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.update_excel])
        )
        self.thread.task_completed.connect(
            lambda: SendMessage(
                "Đã đổi dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại"
            )
        )
        self.thread.start()
        return

    def DeleteThongRow(self):
        # / Check isEditor
        self.toggle_editable(True)  # Cho phép chỉnh sửa trước khi xóa
        self.HandlerData.setText("Tắt Tùy Chỉnh")
        # Lấy đối tượng App từ Workbook
        app = self.sheet.book.app  

        try:
            # Lấy vùng được chọn
            selection = app.selection
            if selection is None:
                SendMessage("Vui lòng chọn ít nhất một dòng!")
                return None

            # Lấy tất cả các dòng từ các vùng chọn, giữ nguyên thứ tự
            selected_rows = []
            seen_rows = set()  # Để kiểm tra trùng lặp mà không thay đổi thứ tự
            for area in selection.api.Areas:  # Duyệt qua từng vùng chọn riêng lẻ
                for row in area.Rows:  # Duyệt qua từng dòng trong vùng
                    row_num = row.Row  # Không trừ 1 để giữ nguyên số dòng Excel
                    if row_num not in seen_rows:  # Chỉ thêm nếu chưa gặp
                        selected_rows.append(row_num)
                        seen_rows.add(row_num)

            # Xóa dòng
            for row in selected_rows:
                for i in range(len(self.thong_data[0])):
                    self.thong_data[i][row - 3] = ""

                isThong_one = True
                if isThong_one:
                    for i in range(len(self.thong_sp[0])):
                        self.thong_sp[row - 3][i] = ["",""]

            # Cập nhật giao diện
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(lambda: self.updateWidget([self.update_excel]))
            self.thread.task_completed.connect(lambda: SendMessage(f"Đã xóa dòng {selected_rows.join(", ")} thành công, xin vui lòng lưu dữ liệu lại"))
            self.thread.start()

        except Exception as e:
            print(f"Lỗi khi xóa dòng: {e}")
            SendMessage("Không thể xóa dòng. Vui lòng thử lại!")

        return

    def changeDataThongWithNumber(self, number):
        self.thong_data = None
        id = self.thong_db["id"]
        with open(
            os.path.join(self.thong_path, f"thong_{id}_{number}.json"), "r"
        ) as file:
            data = json.load(file)
            self.thong_data = data

    def copyRowThong(self, selceted_rows):
        # / Check isEditor
        self.toggle_editable(True)
        self.HandlerData.setText("Tắt Tùy Chỉnh")

        row1 = selceted_rows[0] - 3
        row2 = selceted_rows[1] - 3
        # / Check row2 selected, if it not null is return
        for i in range(len(self.thong_data)):
            item = self.thong_data[i][row2]
            if len(str(item)) != 0:
                SendMessage(f"Dòng nhận chưa được xóa dữ liệu! (Dòng {selceted_rows[1]})")
                return
        for i in range(len(self.thong_data)):
            sender = self.thong_data[i][row1]
            self.thong_data[i][row2] = sender

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.update_excel])
        )
        self.thread.task_completed.connect(
            lambda: SendMessage(
                f"Đã copy dữ liệu từ dòng {selceted_rows[0]} sang dòng {selceted_rows[1]} thành công!"
            )
        )
        self.thread.start()

        return

    def setting_type_click(self):
        setting = self.thong_db["thong_per_luot"]
        # / Config Icon Windows
        icon = self.path.path_logo()

        # / Create Dialog Windows
        dialog = QDialog(self)
        dialog.setWindowTitle("Cài Đặt Bảng Thông")
        dialog.setWindowIcon(QIcon(icon))
        dialog.show()

        # / Dialog Main Layout
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        # / Dialog setting Layout
        setting_dialog_w = QWidget()
        setting_dialog_l = QGridLayout(setting_dialog_w)
        dialog_layout.addWidget(setting_dialog_w)

        type_label = QLabel("Số thông mỗi lượt:")
        type_label.setStyleSheet(css_lable)
        setting_dialog_l.addWidget(type_label, 0, 0)

        type_input = QSpinBox()
        type_input.setFixedWidth(100)
        type_input.setStyleSheet(css_input)
        type_input.setMinimum(1)
        type_input.setMaximum(9999)
        type_input.setValue(setting)
        setting_dialog_l.addWidget(type_input, 1, 0)

        # / Dialog Button layout
        button_dialog_w = QWidget()
        button_dialog_l = QHBoxLayout(button_dialog_w)
        dialog_layout.addWidget(button_dialog_w)

        submit = QPushButton("Lưu")
        submit.setStyleSheet(css_button_submit)
        button_dialog_l.addWidget(submit)

        cancel = QPushButton("Thoát")
        cancel.setStyleSheet(css_button_cancel)
        button_dialog_l.addWidget(cancel)

        # TODO Handler Button
        def submit_click():
            value = type_input.value()
            self.thong_db["thong_per_luot"] = value
            self.thong_db["value"] = value * 100 # 100 là tổng lượt toán
            dialog.reject()
            SendMessage("Xin vui lòng mở lại bảng thông")
            changeThongPerLuot({"data": self.thong_db, "update": self.thong_data})

        def cancel_click():
            dialog.reject()

        submit.clicked.connect(submit_click)
        cancel.clicked.connect(cancel_click)

    def button_show_abc(self):
        # / Check isEditor
        self.toggle_editable(True)
        self.HandlerData.setText("Tắt Tùy Chỉnh")
            
        if self.isShow:
            self.hidden.setText("Hiện ABCD Gốc")
            self.isShow = False
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.update_excel])
            )
            self.thread.start()
        else:
            self.hidden.setText("Ẩn ABCD Gốc")
            self.isShow = True
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.update_excel])
            )
            self.thread.start()

    def show_loading_screen(self):
        self.loadingScreen.show()
        self.loadingScreen.start()

    def hide_loading_screen(self):
        self.loadingScreen.stop()
        self.loadingScreen.hide()

    def updateWidget(self, widgets):
        self.hide_loading_screen()
        for widget in widgets:
            widget()

    # TODO Handler Question
    def showQuestion(self):
        icon = Path().path_logo()
        message = QMessageBox()
        message.setWindowTitle("Thông Báo")
        message.setText(f"Bạn có chắc chắn đồng bộ dữ liệu bảng thông {self.name}")
        message.setWindowIcon(QIcon(icon))  # Thay bằng đường dẫn đến icon của bạn
        message.setFont(self.font)
        message.setIcon(QMessageBox.Icon.Question)
        message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message.setDefaultButton(QMessageBox.No)  # Đặt nút "No" làm mặc định

        # Hiển thị hộp thoại và lấy kết quả
        result = message.exec()

        if result == QMessageBox.Yes:
            self.get_change_history()
            data = {}
            data["update"] = self.thong_data
            data["number"] = self.ban_info["meta"]['number']
            data["thong_sp"] = self.thong_sp
            data["data"] = self.thong_db
            # data["custom"] = self.thong_db["data"]
            # data["name"] = self.thong_db["name"]
            # data["stt"] = self.thong_db["stt"]
            # data["change"] = self.thong_db["change"]
            # data["type_count"] = self.thong_db["type_count"]
            # data["pm"] = self.thong_db["pm"]

            msg = saveAllThong(data)
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([])
            )
            self.thread.task_completed.connect(
                lambda: SendMessage(msg)
            )
            
            self.thread.start()

    # TODO Excel Function
    def get_change_history(self):
        thong_per_luot = self.thong_db["thong_per_luot"]
        meta_number = self.stay.get('thong', 0)
        if meta_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            meta_number = current_ban_info_number
        # Đọc dữ liệu từ bảng
        data_stt = pd.DataFrame(self.sheet.range("A3").expand().value)
        data_all = pd.DataFrame(self.sheet.range("B2").expand().value)
        # Bỏ hàng đầu tiên (index 0)
        data_all = data_all.drop(index=0)

        # Nếu bạn muốn reset lại index sau khi bỏ hàng
        data_all.reset_index(drop=True, inplace=True)
        data_all = data_all.fillna("")
        
        thong_custom = data_all.iloc[:, :4]
        stt = data_stt.iloc[:, 0]
        thong_data = []
        thong_sp = []
        # Xử lý phần còn lại của dữ liệu
        remaining_data = data_all.iloc[:, 4:]
        value_group = thong_per_luot + 2
        for index, row in remaining_data.iterrows():
            row_thong_sp = []
            row_thong_data = []
            
            # Xử lý từng nhóm 17 cột
            for i in range(0, len(row), value_group):
                group = row.iloc[i:i+value_group]
                
                luot_thong_sp = [group.iloc[0], group.iloc[1]]  # 2 cột đầu
                row_thong_sp.append(luot_thong_sp)
                
                # Thêm các cột còn lại vào thong_data
                row_thong_data.extend(group.iloc[2:])
            
            thong_sp.append(row_thong_sp)
            thong_data.append(row_thong_data)

        # Chuyển đổi thành DataFrame để dễ xử lý
        df_thong_data = pd.DataFrame(thong_data)
        df_thong_custom = thong_custom.T.values.tolist()
        df_thong_stt = stt.T.values.tolist()

        # Gán dữ liệu cho self.thong_data (chuyển đổi lại thành định dạng bạn cần)
        number_change = []
        for j, thong in enumerate(df_thong_data.T.values.tolist()):
            thong_index = []
            for k, item in enumerate(thong):
                if item != "":
                    # Chuyển chuỗi thành số thực (float) trước
                    item = float(item)
                    # Sau đó áp dụng math.floor()
                    item = math.floor(item)
                    thong_index.append(item)
                else:
                    thong_index.append(item)
            number_change.append(thong_index)
        
        self.thong_data = number_change  # Chuyển vị ma trận
        self.thong_sp = thong_sp
        self.thong_db["data"] = df_thong_custom
        self.thong_db["stt"][meta_number] = df_thong_stt

    def update_excel(self):
        header_lables = self.updateHeaderRow()
        data_row = self.updateRowAndColumns()
        data_headers = data_row.get("headers")
        data_stt = data_row.get("data_stt")
        data_custom = data_row.get("custom")
        data_thong = data_row.get("data_thong")
        if data_headers:
            for header in data_headers:
                lable = header.get("text")
                start_col_letter = header.get("start_col_letter")
                self.sheet.range(f"{start_col_letter}1").value = lable

        self.sheet.range("A2").value = [["STT"] + header_lables]  # Tiêu đề
        self.sheet.range("A3:A3").value = data_stt
        self.sheet.range("B3:E3").value = data_custom
        self.sheet.range("F3").value = data_thong

        for i, (row, col) in enumerate(self.e_positions):
            # Get the column letter
            col_letter = self.sheet.cells(1, col).address.split('$')[1]
            # Color the entire column (or a specific range in that column)
            column_range = f"{col_letter}:{col_letter}"  # Entire column
            # Or specify a range like: f"{col_letter}2:{col_letter}100"
            
            # Apply color
            if self.e_indices[i] % 10 == 0:
                self.sheet.range(column_range).color = (255, 255, 102)
            else:
                self.sheet.range(column_range).color =  (77, 147, 217)

        # Similar for H positions
        for i, (row, col) in enumerate(self.h_positions):
            col_letter = self.sheet.cells(1, col).address.split('$')[1]
            column_range = f"{col_letter}:{col_letter}"
            
            if self.h_indices[i] % 10 == 0:
                self.sheet.range(column_range).color = (255, 255, 102)
            else:
                self.sheet.range(column_range).color = (77, 147, 217)

        # Tự động căn chỉnh kích thước cột dựa trên nội dung
        self.sheet.autofit('c')  # 'c' để autofit các cột

        # # Chọn ô B1 (Excel sẽ đóng băng tất cả cột bên trái ô này, tức là cột A)
        self.sheet.range("F3").select()

        # # Đóng băng cột A
        self.wb.app.api.ActiveWindow.FreezePanes = True
        self.toggle_editable(False)

    def toggle_editable(self, enable_edit: bool):
        """Bật/Tắt chế độ chỉnh sửa nhưng vẫn cho phép thay đổi định dạng"""
        self.sheet.api.Unprotect(Password=self.pwd)  # Bỏ bảo vệ sheet trước khi thay đổi

        if enable_edit:
            self.table_range.api.Locked = False  # Mở khóa để chỉnh sửa dữ liệu
        else:
            self.table_range.api.Locked = True  # Khóa dữ liệu nhưng không khóa định dạng

        # Bảo vệ sheet nhưng cho phép định dạng (AllowFormattingCells=True)
        self.sheet.api.Protect(Password=self.pwd, AllowFormattingCells=True, AllowFormattingColumns=True, AllowFormattingRows=True)

    def closeEvent(self, event):
        """Xử lý khi cửa sổ PySide6 đóng"""
        if self.wb:
            self.wb.close()  # Đóng workbook mà không lưu
        if self.app:
            self.app.quit()  # Đóng Excel ngay lập tức
        event.accept()  # Chấp nhận sự kiện đóng

