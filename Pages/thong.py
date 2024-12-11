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
    QLineEdit,
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
    TachVaGhep,
    saveBackupThong,convert_string_format,convert_string_format_type
)
import os
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread


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
        self.renderThongTable()
        self.renderThongButton()

    # TODO Handler Render Component
    def renderThongTable(self):
        self.start_col = 0
        self.value_col = 0
        colCount = 600
        # / Title and table
        widget_table = QWidget()
        layout_table = QVBoxLayout(widget_table)
        self.widget_main.addWidget(widget_table)

        layout_table.setSpacing(0)
        layout_table.setContentsMargins(0, 0, 0, 0)

        value_thong = self.thong_db["value"]
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
        # layout_table.addWidget(self.hidden)

        self.table_main = QTableWidget()
        layout_table.addWidget(self.table_main)
        # Setup Header
        self.updateHeaderRow()
        # Setup row
        self.updateRowAndColumns()

        # / Config Font
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

        self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_main.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

        # / Handler Events
        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                if column > 3:
                    item = self.table_main.item(row, column)
                    self.thong_data[column - 4][row] = item.text()

                if column < 4:
                    item = self.table_main.item(row, column)
                    # Đảm bảo `self.thong_db["data"]` đủ dài
                    while len(self.thong_db["data"]) <= column:
                        # Khởi tạo cột mới với dữ liệu mẫu 131 dòng, mỗi dòng là chuỗi rỗng
                        self.thong_db["data"].append(["" for _ in range(132)])

                    self.thong_db["data"][column][row] = item.text()

        def selectedRow():
            # Lấy các hàng được chọn từ các mục được chọn
            selected_items = self.table_main.selectedItems()
            self.selected_row_indices = {item.row() for item in selected_items} if selected_items else set()

            # Lấy chỉ số của các mục được chọn
            selected_indexes = self.table_main.selectedIndexes()
            if selected_indexes:
                # Xác định hàng hiện tại được chọn
                current_selected_row = selected_indexes[0].row()
                if current_selected_row != getattr(self, 'prev_selected_row', None):
                    self.prev_selected_row = current_selected_row

                # Lưu danh sách các hàng được chọn
                self.current_select = list({index.row() for index in selected_indexes})

        # Kết nối sự kiện
        self.table_main.itemSelectionChanged.connect(selectedRow)

        self.table_main.cellChanged.connect(changeValue)

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
        layout.addWidget(DeleteColor, 0, 6)

        # / Create ChangeNumber
        self.ChangeNumber = QComboBox()
        self.ChangeNumber.setStyleSheet("font-size: 24px;line-height: 32px;")
        self.ChangeNumber.setCursor(QCursor(Qt.PointingHandCursor))
        self.ChangeNumber.addItem(f"Cơ gốc")
        for i in range(1, 11):
            self.ChangeNumber.addItem(f"Cơ {i}")
        layout.addWidget(self.ChangeNumber, 0, 7)

        # / Skip to end row
        skipToEnd = QPushButton("Về Cột Cuối")
        skipToEnd.setStyleSheet(css_button_start)
        skipToEnd.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(skipToEnd, 0, 8)

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
        ButtonType = QPushButton("Nhập Liệu B Thông")
        ButtonType.setStyleSheet(css_button_submit)
        ButtonType.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(ButtonType, 1, 3)

        # / Hidden or show
        self.hidden = QPushButton("Hiện ABCD Gốc")
        self.hidden.setStyleSheet(css_button_submit)
        self.hidden.setCursor(Qt.PointingHandCursor)
        self.hidden.clicked.connect(self.button_show_abc)
        self.hidden.setFixedWidth(200)
        layout.addWidget(self.hidden, 1, 4)

        # / Create SaveData
        SettingType = QPushButton("Cài Đặt App")
        SettingType.setStyleSheet(css_button_submit)
        SettingType.setCursor(QCursor(Qt.PointingHandCursor))
        # layout.addWidget(SettingType, 1, 4)

        def changeTypeCount():
            types = self.HandlerData.text()
            if types == "Tắt Tùy Chỉnh":
                self.table_main.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
                self.HandlerData.setText("Bật Tùy Chỉnh")
            else:
                self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                self.HandlerData.setText("Tắt Tùy Chỉnh")

        def saveChange():
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
            if self.ChangeNumber.currentIndex() == 0:
                self.saveBackUp()
            else:
                self.saveThongRow()

        def changeTableNumber():
            value = self.ChangeNumber.currentIndex()
            text = self.ChangeNumber.currentText()
            self.save_stay(value)
            self.changeDataThongWithNumber(value)
            self.table_main.clearContents()
            # self.updateHeaderRow()
            # self.updateRow()
            self.updateRowAndColumns()
            SendMessage(f"Bạn đã mở {text}")
            if value != 0:
                note = Note[value - 1]
                self.note.setText(f"Cơ {value} - {note}")
                # self.note.setScaledContents(True)
            else:
                note = Note[10]
                self.note.setText(f"Cơ gốc - {note}")
                # self.note.setScaledContents(False)

        def copyRow_Click():
            if len(self.current_select) < 2 or len(self.current_select) > 2:
                SendMessage("Xin vui lòng chọn dòng chép và nhận!")
                return
            sender = self.prev_selected_row
            receiver = [item for item in self.current_select if item != sender][0]
            self.copyRowThong([sender, receiver])

        def saveFile_click():
            data = {}
            data["update"] = self.thong_data
            data["custom"] = self.thong_db["data"]
            data["name"] = self.thong_db["name"]
            data["number"] = self.ban_info["meta"]['number']
            data["stt"] = self.thong_db["stt"]
            data["change"] = self.thong_db["change"]
            data["type_count"] = self.thong_db["type_count"]
            data["type_count"] = self.thong_db["type_count"]
            msg = saveAllThong(data)
            self.delete_color_click()
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([])
            )
            self.thread.task_completed.connect(
                lambda: SendMessage(msg)
            )
            self.thread.start()

        def type_with_button():
            if self.selected_row_indices:
                # / Find Select Row
                data_select = list(self.selected_row_indices)
                if len(data_select) < 1:
                    SendMessage("Xin vui lòng chọn dòng để nhập liệu")
                    return
                for row in data_select:
                    setting = 1 if self.thong_db["type_count"] == 3 else 1 if self.thong_db["type_count"] == 0 else self.thong_db["type_count"]
                    data = {}
                    data["row"] = row
                    data["number"] = self.ban_info["meta"]['number']
                    data["setting"] = setting
                    data["stt"] = self.thong_db["stt"]
                    data["update"] = self.thong_data 
                    result = typeWithRecipe(data)
                    self.thong_data = result["update"]

                self.show_loading_screen()
                self.thread = Thread()
                self.thread.task_completed.connect(
                    lambda: self.updateWidget([self.updateRowAndColumns])
                )
                self.thread.task_completed.connect(
                    lambda: SendMessage("Bạn đã nhập liệu thành công")
                )
                self.thread.start()
                self.selected_row_indices = None

        def back_to_first():
            # row = self.table_main.rowCount() - 2  # Get the current row
            item = self.table_main.item(0, 0)  # Get the first column item
            self.table_main.scrollToItem(item, QHeaderView.ScrollHint.PositionAtCenter)
            return

        def skip_to_end():
            # row = self.table_main.rowCount() - 2  # Get the current row
            col = self.table_main.columnCount() - 1  # Get the current row
            item = self.table_main.item(0, col)  # Get the first column item
            self.table_main.scrollToItem(item, QHeaderView.ScrollHint.PositionAtCenter)
            return
        
        def skip_to_mid():
            # row = self.table_main.rowCount() - 2  # Get the current row
            col = self.table_main.columnCount() - 1  # Get the current row
            item = self.table_main.item(0, col // 2)  # Get the first column item
            self.table_main.scrollToItem(item, QHeaderView.ScrollHint.PositionAtCenter)
            return


        self.HandlerData.clicked.connect(changeTypeCount)
        SaveData.clicked.connect(saveChange)
        self.ChangeNumber.currentIndexChanged.connect(changeTableNumber)
        BackUp.clicked.connect(self.backUpRows)
        Delete.clicked.connect(self.delete_all_rows)
        DeleteRow.clicked.connect(self.DeleteThongRow)
        swapRow.clicked.connect(self.swapThongRow)
        CopyRow.clicked.connect(copyRow_Click)
        DeleteColor.clicked.connect(self.delete_color_click)
        SaveFile.clicked.connect(saveFile_click)
        SettingType.clicked.connect(self.setting_type_click)
        ButtonType.clicked.connect(type_with_button)
        save_back_up.clicked.connect(self.saveBackUp)
        backToFirst.clicked.connect(back_to_first)
        skipToEnd.clicked.connect(skip_to_end)
        skipToMind.clicked.connect(skip_to_mid)

        
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

    def freeze_col_stt(self, value):
        pass
        # if value >= self.start_col:
        #     self.table_main.horizontalHeader().moveSection(self.value_col, value)
        #     self.value_col = value
        # elif value < self.start_col:
        #     value = self.start_col
        #     self.table_main.horizontalHeader().moveSection(self.value_col, value)
        #     self.value_col = value

    def deleteOldWidgetThongs(self):
        # / Delete old table main and buttons
        if self.table_main:
            self.table_main.deleteLater()
            self.widget_main.layout().removeWidget(self.table_main)
            self.table_main = None
        if self.button_wid_main:
            self.button_wid_main.deleteLater()
            self.layout_thong.layout().removeWidget(self.button_wid_main)
            self.button_wid_main = None

    def updateHeaderRow(self):
        colCount = 600
        self.table_main.setColumnCount(0)
        self.table_main.setColumnCount(colCount + 4)
        
        header_labels = ["A", "B", "C", "D"] + [f"T.{i + 1}" for i in range(colCount)]
        self.table_main.setHorizontalHeaderLabels(header_labels)

        setting = 1 if self.thong_db["type_count"] == 3 else 1 if self.thong_db["type_count"] == 0 else self.thong_db["type_count"]
        if setting == 1:
            for i in range(0, colCount, 60):
                for k in range(60):
                    if k == 0:
                        item = self.table_main.horizontalHeaderItem(i + k + 4)
                        item.setBackground(QColor("#ffd867"))
                    elif k == 1:
                        item = self.table_main.horizontalHeaderItem(i + k + 4)
                        item.setBackground(QColor("#ffd867"))
        else:
            for i in range(0, colCount, 10):
                for k in range(10):
                    if k == 0:
                        item = self.table_main.horizontalHeaderItem(i + k + 4)
                        item.setBackground(QColor("#ffd867"))

    def updateRowAndColumns(self):
        if self.table_main is None:
            return

        # Lấy dữ liệu cần thiết
        meta_number = self.stay.get('thong', 0)
        if meta_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            meta_number = current_ban_info_number
        stt = self.thong_db["stt"][meta_number]
        data_value = self.thong_db["data"]
        thong_data = self.thong_data
        row_count = len(thong_data[0])

        # Cấu hình bảng
        self.table_main.clearContents()
        self.table_main.setRowCount(0)
        self.table_main.setRowCount(row_count)

        # Hàm hỗ trợ tạo QTableWidgetItem
        def create_table_item(value, alignment=Qt.AlignmentFlag.AlignCenter, background=None):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(alignment)
            if background:
                item.setBackground(background)
            return item

        # * Cập nhật tiêu đề hàng (STT)
        vertica_header = [f'{i:02}' for i in range(row_count)]
        self.table_main.setVerticalHeaderLabels(vertica_header)

        # * Xử lý dữ liệu nếu cần thay đổi số
        if meta_number != 0 and not self.isShow:
            data_value = [
                [TachVaGhep(meta_number, value) for value in row]
                for row in data_value
            ]

        # * Cập nhật dữ liệu từ data_value
        for i, col_values in enumerate(data_value):
            for j, cell_value in enumerate(col_values):
                background = self.stt_highlight if i in (0, 2) else None
                item = create_table_item(cell_value, background=background)
                self.table_main.setItem(j, i, item)

        # * Cập nhật dữ liệu từ thong_data
        for i, thong_row in enumerate(thong_data):
            for j, cell_value in enumerate(thong_row):
                item = create_table_item(cell_value)
                self.table_main.setItem(j, i + 4, item)

        
        # * To mau du lieu
        setting = 1 if self.thong_db["type_count"] == 3 else 1 if self.thong_db["type_count"] == 0 else self.thong_db["type_count"]
        if setting == 1:
            for i in range(0, 600, 60):
                for k in range(60):
                    if k == 0:
                        for r in range(row_count):
                            item = self.table_main.item(r, i + k + 4)
                            item.setBackground(QColor("#ffd867"))
                    elif k == 1:
                        for r in range(row_count):
                            item = self.table_main.item(r, i + k + 4)
                            item.setBackground(QColor("#ffd867"))
        else:
            for i in range(0, 600, 10):
                for k in range(10):
                    if k == 0:
                        for r in range(row_count):
                            item = self.table_main.item(r, i + k + 4)
                            item.setBackground(QColor("#ffd867"))

        # Xóa màu click
        self.delete_color_click()
        print('Done upload Row')

    def delete_all_rows(self):
        rowCount = len(self.thong_data[0])
        data_value = self.thong_db["data"]
        stt = self.thong_db["stt"][self.ban_info["meta"]['number']]
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
        self.table_main.setRowCount(0)
        self.table_main.setRowCount(rowCount)

        for i in range(len(data_value)):
            value_col = data_value[i]
            for j in range(len(value_col)):
                item = QTableWidgetItem(f"{value_col[j]}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j, i, item)
                if i == 0 or i == 2:
                    item.setBackground(self.stt_highlight)

        # * Render Rows STT First
        for i in range(rowCount):
            stt_value = stt[i]
            item = QTableWidgetItem(
                f"{stt_value}{self.word[i - 100] if  0 <= i - 100 < 26 else ''}"
            )
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(self.color_col_stt)
            item.setBackground(self.stt_highlight)
            self.table_main.setVerticalHeaderItem(i, item)

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([]))
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
        data = {}
        data["id"] = self.thong_db["id"]
        data["thong_data"] = self.thong_data
        data["custom"] = self.thong_db["data"]

        # / Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")

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
        data = {}
        data["update"] = self.thong_data
        data["custom"] = self.thong_db["data"]
        data["id"] = self.thong_db["id"]
        data["number"] = self.ban_info["meta"]['number']
        data["stt"] = self.thong_db["stt"]
        data["change"] = self.thong_db["change"]
        data["setting"] = self.thong_db["setting"]

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
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
        # / Thong Data and Thong info
        stt = self.thong_db["stt"][self.ban_info["meta"]['number']]
        data = self.thong_data
        # / Find Select Row
        # data_select = list(self.selected_row_indices)
        # if len(data_select) == -1:
        #     SendMessage('Xin vui lòng chọn 1 dòng để hoán đổi dữ liệu!')
        #     return
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

        self.thong_db["stt"][self.ban_info["meta"]['number']] = shifted_stt
        self.thong_data = shifted_data
        # self.updateHeaderRow()

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.updateRowAndColumns])
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
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
        if self.selected_row_indices is None:
            SendMessage("Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!")
            return

        # / Find Select Row
        data_select = list(self.selected_row_indices)
        # if len(data_select) != 1:
        #     SendMessage("Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!")
        #     return
        for row in data_select:
            for i in range(4, self.table_main.columnCount()):
                self.thong_data[i - 4][row] = ""
        # self.updateHeaderRow()

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.updateRowAndColumns])
        )
        self.thread.task_completed.connect(
            lambda: SendMessage(
                "Đã xóa dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại"
            )
        )
        self.thread.start()
        return

    def changeDataThongWithNumber(self, number):
        self.thong_data = None
        id = self.thong_db["id"]
        with open(
            os.path.join(self.thong_path, f"thong_{id}_{number}.json"), "r"
        ) as file:
            data = json.load(file)
            self.thong_data = data

        # SendMessage(f"Đã mở Bộ chuyển đổi {number}")

    def copyRowThong(self, selceted_rows):
        row1 = selceted_rows[0]
        row2 = selceted_rows[1]
        row1_h = f"{row1 + 1:02}"  # Ensure proper formatting for display
        row2_h = f"{row2 + 1:02}"
        # / Check row2 selected, if it not null is return
        for i in range(len(self.thong_data)):
            item = self.thong_data[i][row2]
            if len(str(item)) != 0:
                SendMessage(f"Dòng nhận chưa được xóa dữ liệu! (Dòng {row2_h})")
                return
        for i in range(len(self.thong_data)):
            sender = self.thong_data[i][row1]
            self.thong_data[i][row2] = sender

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.updateRowAndColumns])
        )
        self.thread.task_completed.connect(
            lambda: SendMessage(
                f"Đã copy dữ liệu từ dòng {row1_h} sang dòng {row2_h} thành công!"
            )
        )
        self.thread.start()

        return

    def setting_type_click(self):
        setting = self.thong_db["setting"]
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

        type_label = QLabel("Tên App (0: App Trắng; 1: App 1 Số; 2: App 2 Số)")
        type_label.setStyleSheet(css_lable)
        setting_dialog_l.addWidget(type_label, 0, 0)

        type_input = QSpinBox()
        type_input.setFixedWidth(100)
        type_input.setStyleSheet(css_input)
        type_input.setMinimum(0)
        type_input.setMaximum(2)
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
            self.thong_db["setting"] = type_input.value()
            dialog.reject()

        def cancel_click():
            dialog.reject()

        submit.clicked.connect(submit_click)
        cancel.clicked.connect(cancel_click)

    def button_show_abc(self):
        if self.isShow:
            self.hidden.setText("Hiện ABCD Gốc")
            self.isShow = False
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.updateRowAndColumns])
            )
            self.thread.start()
        else:
            self.hidden.setText("Ẩn ABCD Gốc")
            self.isShow = True
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.updateRowAndColumns])
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
