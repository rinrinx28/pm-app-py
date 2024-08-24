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
    css_title,
)
import json
from Controller.handler import (
    saveThong,
    backupThong,
    saveAllThong,
    typeWithRecipe,
    TachVaGhep,
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
            "Bảng Thông - Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam"
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

        with open(os.path.join(self.thong_path, "thongs.json"), "r") as file:
            self.thong_db = json.load(file)
        # / Config LoadingScreen
        self.loadingScreen = LoadingScreen(self.path.path_loading())

        # / Config Secleted item
        self.selected_row_indices = None
        self.current_select = []
        self.prev_selected_row = None
        self.cyan = QColor(178, 255, 255)
        self.normal = QColor("#FFFFFF")
        self.stt_highlight = QColor("#EDEADE")

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

        # / Button Main
        self.button_wid_main = QWidget()
        self.button_layout = QHBoxLayout(self.button_wid_main)
        self.button_layout.setSpacing(100)
        self.layout_thong.addWidget(self.button_wid_main)

        # / Render Component
        self.changeDataThongWithNumber(0)
        self.renderThongButton()
        self.renderThongTable()

    # TODO Handler Render Component
    def renderThongTable(self):
        self.start_col = 1
        self.value_col = 1
        colCount = self.thong_db["value"]
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

        title_text = (
            f"{ban_thong_name} / C{ban_col[0]} đến C{ban_col[1]} / T{ban_thong_value[0]} đến "
            + f"T{ban_thong_value[1]} /  Bộ Chuyển Đổi: {change_number} / "
            + f"Số dòng: {row_count}/{max_row} / "
            + f"Bảng Thông: {value_thong} Thông"
        )
        title = QLabel(title_text)
        title.setStyleSheet(css_title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_table.addWidget(title)

        # / Note
        self.note = QLabel("")
        self.note.setFont(self.font)
        layout_table.addWidget(self.note)

        # / Hidden or show
        self.hidden = QPushButton("Hiện ABC Gốc")
        self.hidden.setStyleSheet(css_button_submit)
        self.hidden.setCursor(Qt.PointingHandCursor)
        self.hidden.clicked.connect(self.button_show_abc)
        self.hidden.setFixedWidth(200)
        layout_table.addWidget(self.hidden)

        self.table_main = QTableWidget()
        layout_table.addWidget(self.table_main)
        self.table_main.setColumnCount(colCount + 5)

        # self.updateHeaderRow()

        for i in range(colCount):
            if i == 0:
                item_stt = QTableWidgetItem(f"STT")
                item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(0, item_stt)

                item_zero = QTableWidgetItem(f"Cột 0")
                item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(1, item_zero)

                item_a = QTableWidgetItem(f"A")
                item_a.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(2, item_a)

                item_b = QTableWidgetItem(f"B")
                item_b.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(3, item_b)

                item_c = QTableWidgetItem(f"C")
                item_c.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(4, item_c)

                item = QTableWidgetItem(f"T.{i+1}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 5, item)
            else:
                item = QTableWidgetItem(f"T.{i+1}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i + 5, item)

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

        self.table_main.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_main.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.table_main.horizontalScrollBar().valueChanged.connect(self.freeze_col_stt)

        self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_main.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

        # / Handler Events
        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                if column > 4:
                    item = self.table_main.item(row, column)
                    # filter_db = [
                    #     item
                    #     for item in self.thong_db["change"]
                    #     if item["row"] != row
                    #     and item["column"] != column - 5
                    #     and item["number"] != self.ChangeNumber.currentIndex()
                    # ]
                    # filter_data = [
                    #     item
                    #     for item in self.thong_db["change"]
                    #     if item["row"] == row
                    #     and item["column"] == column - 5
                    #     and item["number"] == self.ChangeNumber.currentIndex()
                    # ]
                    # if len(filter_data) > 0:
                    #     filter_data[0]["new"] = item.text()
                    #     self.thong_db["change"] = filter_db + filter_data
                    # if filter_data[0]["new"] != filter_data[0]["old"]:
                    #     item.setBackground(self.cyan)
                    # else:
                    #     item.setBackground(self.normal)
                    # else:
                    #     self.thong_db["change"].append(
                    #         {
                    #             "row": row,
                    #             "column": column - 5,
                    #             "number": self.ChangeNumber.currentIndex(),
                    #             "new": item.text(),
                    #             "old": self.thong_data[column - 5][row],
                    #         }
                    #     )
                    #     # item.setBackground(self.cyan)
                    self.thong_data[column - 5][row] = item.text()

                if 1 < column < 5:
                    item = self.table_main.item(row, column)
                    self.thong_db["data"][column - 2][row] = item.text()

        def selectedRow():
            selected_items = self.table_main.selectedItems()
            if selected_items:
                self.selected_row_indices = set()
                for item in selected_items:
                    self.selected_row_indices.add(item.row())

            selected_indexes = self.table_main.selectedIndexes()
            if selected_indexes:
                # / Find is first selected item
                current_selected_row = selected_indexes[0].row()
                if (
                    self.prev_selected_row is None
                    or current_selected_row != self.prev_selected_row
                ):
                    self.prev_selected_row = current_selected_row

                # / get all selelected items
                selected_rows = set()
                for i in range(len(selected_indexes)):
                    rows = selected_indexes[i].row()
                    selected_rows.add(rows)
                self.current_select = list(selected_rows)

        self.table_main.cellChanged.connect(changeValue)
        self.table_main.itemSelectionChanged.connect(selectedRow)

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
        # / Create MathCount
        swapRow = QPushButton("Đổi Dòng DL")
        swapRow.setStyleSheet(css_button_cancel)
        swapRow.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(swapRow, 0, 0)

        # / Copy Row Button
        CopyRow = QPushButton("Chép Dòng DL")
        CopyRow.setStyleSheet(css_button_cancel)
        CopyRow.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(CopyRow, 0, 1)

        # / Create Delete
        DeleteRow = QPushButton("Xóa DL dòng")
        DeleteRow.setStyleSheet(css_button_cancel)
        DeleteRow.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(DeleteRow, 0, 2)

        # / Create Delete
        Delete = QPushButton("Xóa tất cả DL")
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(Delete, 0, 3)

        # / Create Delete
        DeleteColor = QPushButton("Xóa Màu")
        DeleteColor.setStyleSheet(css_button_cancel)
        DeleteColor.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(DeleteColor, 0, 4)

        # / Create ChangeNumber
        self.ChangeNumber = QComboBox()
        self.ChangeNumber.setStyleSheet(css_input)
        self.ChangeNumber.setCursor(QCursor(Qt.PointingHandCursor))
        self.ChangeNumber.addItem("Chuyển Đổi 0")
        for i in range(5):
            self.ChangeNumber.addItem(f"Chuyển Đổi {i+1}")
        layout.addWidget(self.ChangeNumber, 0, 5)

        # TODO Line 2

        # / Create Backup
        BackUp = QPushButton("Khôi phục DL gốc")
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(BackUp, 1, 0)

        # / Create AutoSaveFiles
        SaveFile = QPushButton("Đồng Bộ DL")
        SaveFile.setStyleSheet(css_button_submit)
        SaveFile.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(SaveFile, 1, 1)

        # / Create Backup
        ButtonType = QPushButton("Nhập Công Thức")
        ButtonType.setStyleSheet(css_button_submit)
        ButtonType.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(ButtonType, 1, 2)

        # / Create HandlerData
        type_input = "Tắt Tùy Chỉnh"
        self.HandlerData = QPushButton(type_input)
        self.HandlerData.setStyleSheet(css_button_submit)
        self.HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.HandlerData, 1, 3)

        # / Create SaveData
        SaveData = QPushButton("Lưu")
        SaveData.setStyleSheet(css_button_submit)
        SaveData.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(SaveData, 1, 4)

        # / Create SaveData
        SettingType = QPushButton("Cài Đặt")
        SettingType.setStyleSheet(css_button_submit)
        SettingType.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(SettingType, 1, 5)

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
            self.saveThongRow()

        def changeTableNumber():
            value = self.ChangeNumber.currentIndex()
            self.changeDataThongWithNumber(value)
            self.updateRowAndColumns()
            if value != 0:
                note = Note[value - 1]
                self.note.setText(f"{note}")
                self.note.setScaledContents(True)
            else:
                self.note.setText("")
                self.note.setScaledContents(False)

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
            data["number"] = self.ChangeNumber.currentIndex()
            data["stt"] = self.thong_db["stt"]
            data["change"] = self.thong_db["change"]
            data["type_count"] = self.thong_db["type_count"]
            msg = saveAllThong(data)
            self.delete_color_click()
            SendMessage(msg)

        def type_with_button():
            if self.thong_db["setting"] == 0:
                SendMessage(
                    "Loại Nhập hiện tại là 0 (Trắng), xin vui lòng chọn loại khác để tiến hành nhập công thức"
                )
                return
            if self.selected_row_indices:
                # / Find Select Row
                data_select = list(self.selected_row_indices)
                if len(data_select) < 1:
                    SendMessage("Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!")
                    return
                for row in data_select:
                    data = {}
                    data["row"] = row
                    data["number"] = self.ChangeNumber.currentIndex()
                    data["setting"] = self.thong_db["setting"]
                    data["stt"] = self.thong_db["stt"]
                    data["update"] = self.thong_data
                    result = typeWithRecipe(data)
                    self.thong_data = result["update"]
                    self.updateRowAndColumns()
                self.selected_row_indices = None

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

    # TODO Handler Widgets
    def delete_color_click(self):
        self.table_main.clearSelection()
        self.selected_row_indices = None
        self.prev_selected_row = None
        self.current_select = []

    def freeze_col_stt(self, value):
        if value >= self.start_col:
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value
        elif value < self.start_col:
            value = self.start_col
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value

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

    def updateRowAndColumns(self):
        stt = self.thong_db["stt"][self.ChangeNumber.currentIndex()]
        data_value = self.thong_db["data"]
        thong_data = self.thong_data
        # / Table Config
        self.table_main.clearContents()
        self.table_main.setRowCount(0)
        rowCount = len(self.thong_data[0])
        # / Add Header Table
        self.table_main.setRowCount(rowCount)

        # * Render Rows STT First
        for i in range(rowCount):
            zero_value = f"{i:02}."
            item_zero = QTableWidgetItem(f"{zero_value}")
            item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # item_zero.setBackground(self.stt_highlight)
            self.table_main.setItem(i, 0, item_zero)

            stt_value = stt[i]
            item = QTableWidgetItem(f"{stt_value}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(self.stt_highlight)
            self.table_main.setItem(i, 1, item)

        # * Change data value with number change
        number_change = self.ChangeNumber.currentIndex()
        if number_change != 0 and not self.isShow:
            data_value_new = map(
                lambda values: list(
                    map(lambda value: TachVaGhep(number_change, value), values)
                ),
                data_value,
            )
            data_value = list(data_value_new)

        # * Render Rows Custom First
        for i in range(len(data_value)):
            value_col = data_value[i]
            for j in range(len(value_col)):
                item = QTableWidgetItem(f"{value_col[j]}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setItem(j, i + 2, item)
                if i + 2 == 2 or i + 2 == 4:
                    item.setBackground(self.stt_highlight)

        # * Render Rows
        for i in range(len(thong_data)):
            thong_row = thong_data[i]
            for j in range(len(thong_row)):
                item = QTableWidgetItem(f"{thong_row[j]}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # filter_changed = [
                #     item
                #     for item in self.thong_db["change"]
                #     if item["row"] == j
                #     and item["column"] == i
                #     and item["number"] == self.ChangeNumber.currentIndex()
                # ]
                # if len(filter_changed) > 0:
                #     item_new = filter_changed[0]["new"]
                #     item_old = filter_changed[0]["old"]
                # if item_new != item_old:
                # item.setBackground(self.cyan)
                self.table_main.setItem(j, i + 5, item)
        self.delete_color_click()

    def delete_all_rows(self):
        rowCount = len(self.thong_data[0])
        stt = self.thong_db["stt"][self.ChangeNumber.currentIndex()]
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
        self.table_main.setRowCount(0)
        self.table_main.setRowCount(rowCount)

        for i in range(len(self.thong_data)):
            for j in range(len(self.thong_data[i])):
                self.thong_data[i][j] = ""

        # * Render Rows STT First
        for i in range(rowCount):
            zero_value = f"{i}" if i > 9 else f"0{i}"
            item_zero = QTableWidgetItem(f"{zero_value}")
            item_zero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 0, item_zero)

            item = QTableWidgetItem(f"{stt[i]}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 1, item)

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([]))
        self.thread.start()

    def backUpRows(self):
        # / Load BackUp File with ID
        id = self.thong_db["id"]
        data = backupThong({"number": self.ChangeNumber.currentIndex(), "id": id})
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
        self.thread.start()

    def saveThongRow(self):
        data = {}
        data["update"] = self.thong_data
        data["custom"] = self.thong_db["data"]
        data["id"] = self.thong_db["id"]
        data["number"] = self.ChangeNumber.currentIndex()
        data["stt"] = self.thong_db["stt"]
        data["change"] = self.thong_db["change"]
        data["setting"] = self.thong_db["setting"]
        msg = saveThong(data)
        SendMessage(msg)

    def swapThongRow(self):
        # / Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
        # / Thong Data and Thong info
        stt = self.thong_db["stt"][self.ChangeNumber.currentIndex()]
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

        self.thong_db["stt"][self.ChangeNumber.currentIndex()] = shifted_stt
        self.thong_data = shifted_data
        SendMessage("Đã đổi dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại")
        # self.updateHeaderRow()

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.updateRowAndColumns])
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
        if len(data_select) != 1:
            SendMessage("Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!")
            return
        for row in data_select:
            for i in range(5, self.table_main.columnCount()):
                self.thong_data[i - 5][row] = ""
        SendMessage("Đã xóa dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại")
        # self.updateHeaderRow()

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(
            lambda: self.updateWidget([self.updateRowAndColumns])
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

        SendMessage(f"Đã mở Bộ chuyển đổi {number}")

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
        self.thread.start()
        SendMessage(f"Đã copy dữ liệu từ dòng {row1_h} sang dòng {row2_h} thành công!")
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

        type_label = QLabel("Loại Công Thức (0: Trắng; 1: 1 Số; 2: 2 Số)")
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
            self.hidden.setText("Hiện ABC Gốc")
            self.isShow = False
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: self.updateWidget([self.updateRowAndColumns])
            )
            self.thread.start()
        else:
            self.hidden.setText("Ẩn ABC Gốc")
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
