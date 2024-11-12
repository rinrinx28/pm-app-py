from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QLabel,
)
from PySide6.QtGui import Qt, QCursor, QColor, QIcon
from Pages.components.stylesheet import (
    css_button_cancel,
    css_button_submit,
    css_input,
    Font,
    Note,
    SendMessage,
    css_title,
)
import json
import os
from Controller.handler import backUpNgang, saveNgang, convert_string_format
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread

prev_selected_rows = set()


class NgangPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.layout_ngang = QVBoxLayout(self)
        self.setWindowTitle(
            "Phần Mềm Hỗ Trợ Dự Án Làm Sạch Môi Trường Thềm Lục Địa Biển Việt Nam - maikien06091966@gmail.com  - Chủ sáng lập, thiết kế và mã hóa dữ liệu: Mai Đình Kiên - Số Điện Thoại: 0964636709"
        )
        logo_path = self.path.path_logo()
        icon = QIcon(logo_path)
        # Setting application icon
        self.setWindowIcon(icon)
        self.ngang_path = self.path.path_number()
        self.thong_path = self.path.path_thong()
        self.layout_ngang.setSpacing(0)
        # / Config LoadingScreen
        self.loadingScreen = LoadingScreen(self.path.path_loading())
        # / Config Font
        self.font = Font()

        # / Load Data Bans
        self.bans_path = self.path.path_db()
        with open(self.bans_path, "r") as file:
            self.bans_db = json.load(file)

        self.ban_info = self.bans_db

        # / Config STT
        self.ngang_info = None
        self.stt_ngang = None
        with open(os.path.join(self.ngang_path, "number.json"), "r") as file:
            self.ngang_info = json.load(file)
        self.stt_ngang = self.ngang_info["stt"]

        self.selected_row_indices = -1
        self.current_select = []
        self.prev_selected_row = None
        self.cyan = QColor(178, 255, 255)
        self.normal = QColor("#FFFFFF")

        with open(os.path.join(self.thong_path, "thongs.json"), "r") as file:
            self.thong_db = json.load(file)

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
        title_text = (
            f"{name} / C{ban_col[0]} đến C{ban_col[1]} / T{ban_thong_value[0]} đến "
            + f"T{ban_thong_value[1]} /  Bộ Chuyển Đổi: {change_number} / "
            + f"Số dòng: {row_count}/{max_row} / "
            + f"Bảng Ngang 600 Cột"
        )
        title = QLabel(title_text)
        title.setStyleSheet(css_title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_ngang.addWidget(title)

        # / Note
        self.note = QLabel("")
        self.note.setFont(self.font)
        self.layout_ngang.addWidget(self.note)

        # / Widget Main
        self.widget_main = QStackedWidget()
        self.layout_ngang.addWidget(self.widget_main)

        # / Table main
        self.table_main = None
        self.ngang_data = None

        # / Button main
        button_Wid_main = QWidget()
        self.button_layout = QHBoxLayout(button_Wid_main)
        self.layout_ngang.addWidget(button_Wid_main)

        # / Render Component
        self.changeDataNgangWithNumber(0)
        self.renderButton()
        self.renderTable()

    # TODO Handler render component
    def renderButton(self):
        # / SwapLine Button
        SwapLine = QPushButton("Đổi Dòng DL")
        SwapLine.setStyleSheet(css_button_cancel)
        SwapLine.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(SwapLine)

        # / Copy Row Button
        CopyRow = QPushButton("Chép Dòng DL")
        CopyRow.setStyleSheet(css_button_cancel)
        CopyRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(CopyRow)

        # / Create Delete
        DeleteRow = QPushButton("Xóa DL dòng")
        DeleteRow.setStyleSheet(css_button_cancel)
        DeleteRow.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(DeleteRow)

        # / Delete Button
        Delete = QPushButton("Xóa Tất Cả DL")
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(Delete)

        # / Delete Button
        DeleteColor = QPushButton("Xóa Màu")
        DeleteColor.setStyleSheet(css_button_cancel)
        DeleteColor.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(DeleteColor)

        # / Change_number Button
        # TODO Config Change Number
        number = 11
        self.Change_number = QComboBox()
        self.Change_number.setStyleSheet("font-size: 24px;line-height: 32px;")
        self.Change_number.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(self.Change_number)
        self.Change_number.addItem(f"Bộ chuyển đổi gốc")
        for i in range(1, number):
            self.Change_number.addItem(f"Bộ chuyển Đổi {i}")

        # / BackUp Button
        BackUp = QPushButton("Khôi Phục DL Gốc")
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(BackUp)

        # / Create HandlerData
        type_input = "Tắt Tùy Chỉnh"
        self.HandlerData = QPushButton(type_input)
        self.HandlerData.setStyleSheet(css_button_submit)
        self.HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_layout.addWidget(self.HandlerData)

        # / Save Button
        Save = QPushButton("Lưu")
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
                self.note.setText(f"Bộ chuyển đổi {value} - {note}")
                self.note.setScaledContents(True)
            else:
                self.note.setText("")
                self.note.setScaledContents(False)

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
            self.saveRowNgang()

        def backupNgang():
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
            self.backUpNgang()

        def deleteRows():
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
            self.delete_all_row()

        def copyRow_Click():
            if len(self.current_select) < 2 or len(self.current_select) > 2:
                SendMessage("Xin vui lòng chọn dòng chép và nhận!")
                return
            sender = self.prev_selected_row
            receiver = [item for item in self.current_select if item != sender][0]
            self.copyRowNgang([sender, receiver])

        self.Change_number.currentIndexChanged.connect(change_number_selected)
        SwapLine.clicked.connect(self.swapNgangRow)
        self.HandlerData.clicked.connect(changeTypeCount)
        Save.clicked.connect(saveChange)
        BackUp.clicked.connect(backupNgang)
        Delete.clicked.connect(deleteRows)
        DeleteRow.clicked.connect(self.delete_one_row)
        CopyRow.clicked.connect(copyRow_Click)
        DeleteColor.clicked.connect(self.delete_color_click)

    def renderTable(self):
        data = self.ngang_data
        # TODO Data configuration
        colCount = len(data[0])
        self.start_col = 0
        self.value_col = 0

        self.table_main = QTableWidget()
        self.widget_main.addWidget(self.table_main)

        # TODO Config table
        self.table_main.setColumnCount(colCount + 1)  # / Add STT into col

        # / Render Rows
        self.updateRows()
        # TODO Render Header Table
        for i in range(colCount):
            if i == 0:
                item = QTableWidgetItem(f"STT")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_main.setHorizontalHeaderItem(i, item)

            item = QTableWidgetItem(f"C.{i+1}")
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
        self.table_main.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_main.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

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

        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                if column > 0:
                    item = self.table_main.item(row, column)
                    filter_db = [
                        item
                        for item in self.ngang_info["change"]
                        if item["row"] != row
                        and item["column"] != column - 1
                        and item["number"] != self.Change_number.currentIndex()
                    ]
                    filter_data = [
                        item
                        for item in self.ngang_info["change"]
                        if item["row"] == row
                        and item["column"] == column - 1
                        and item["number"] == self.Change_number.currentIndex()
                    ]
                    if len(filter_data) > 0:
                        filter_data[0]["new"] = item.text()
                        self.ngang_info["change"] = filter_db + filter_data
                        if filter_data[0]["new"] != filter_data[0]["old"]:
                            item.setBackground(self.cyan)
                        else:
                            item.setBackground(self.normal)
                    else:
                        self.ngang_info["change"].append(
                            {
                                "row": row,
                                "column": column - 1,
                                "number": self.Change_number.currentIndex(),
                                "new": item.text(),
                                "old": self.ngang_data[row][column - 1],
                            }
                        )
                        item.setBackground(self.cyan)
                    self.ngang_data[row][column - 1] = item.text()

        self.table_main.itemSelectionChanged.connect(selectedRow)
        self.table_main.cellChanged.connect(changeValue)

    # TODO Handler Events
    def delete_color_click(self):
        self.table_main.clearSelection()
        self.prev_selected_row = None
        self.selected_row_indices = None
        self.current_select = []

    def freeze_col_stt(self, value):
        if value >= self.start_col:
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value
        elif value < self.start_col:
            value = self.start_col
            self.table_main.horizontalHeader().moveSection(self.value_col, value)
            self.value_col = value

    def swapNgangRow(self):
        # / Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
        # / Ngang Data and Ngang stt
        stt = self.stt_ngang[self.Change_number.currentIndex()]
        data = self.ngang_data
        # Tạo một danh sách mới để lưu trữ các phần tử sau khi dịch chuyển
        # Tạo 2 danh sách mới để lưu trữ các phần tử
        part1_stt = stt[:31]
        part2_stt = stt[31:]
        shifted_stt_part1 = [None] * len(part1_stt)

        # Dịch chuyển các phần tử xuống một vị trí và cập nhật vào danh sách mới
        for i in range(len(part1_stt)):
            shifted_stt_part1[(i + 1) % len(part1_stt)] = part1_stt[i]

        shifted_stt = shifted_stt_part1 + part2_stt

        part1_data = data[:31]
        part2_data = data[31:]
        shifted_part1_data = [None] * len(part1_data)
        for i in range(len(part1_data)):
            shifted_part1_data[(i + 1) % len(part1_data)] = part1_data[i]

        shifted_data = shifted_part1_data + part2_data

        self.stt_ngang[self.Change_number.currentIndex()] = shifted_stt
        self.ngang_data = shifted_data
        SendMessage("Đã đổi dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại")

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.updateRows]))
        self.thread.start()
        return

    def changeDataNgangWithNumber(self, number):
        self.ngang_data = None
        with open(os.path.join(self.ngang_path, f"number_{number}.json"), "r") as file:
            data = json.load(file)
            self.ngang_data = data
        # SendMessage(f"Đã mở Bộ chuyển đổi {number}")

    def updateRows(self):
        self.table_main.clearSelection()
        data = self.ngang_data
        stt = self.stt_ngang[self.Change_number.currentIndex()]
        colCount = len(data[0])
        rowCount = len(data)
        self.table_main.setRowCount(0)
        self.table_main.setRowCount(rowCount)

        # TODO Render Rows
        for i in range(rowCount):
            stt_value = stt[i]
            item_stt = QTableWidgetItem(f"{stt_value}")
            item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 0, item_stt)
            for j in range(colCount):
                value = data[i][j]
                item = QTableWidgetItem(f"{value}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                filter_changed = [
                    item
                    for item in self.ngang_info["change"]
                    if item["row"] == i
                    and item["column"] == j
                    and item["number"] == self.Change_number.currentIndex()
                ]
                if len(filter_changed) > 0:
                    item_new = filter_changed[0]["new"]
                    item_old = filter_changed[0]["old"]
                    if item_new != item_old:
                        item.setBackground(self.cyan)
                self.table_main.setItem(i, j + 1, item)
        self.delete_color_click()

    def backUpNgang(self):
        data = {}
        data["number"] = self.Change_number.currentIndex()
        result = backUpNgang(data)

        self.ngang_info = result["stt"]

        self.stt_ngang = self.ngang_info["stt"]
        self.ngang_data = result["ngang_data"]

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.updateRows]))
        self.thread.start()
        SendMessage("Đã khôi phục dữ liệu thành công!")

    def saveRowNgang(self):
        data = {}
        data["update"] = self.ngang_data
        data["number"] = self.Change_number.currentIndex()
        data["stt"] = self.stt_ngang
        data["change"] = self.ngang_info["change"]
        saveNgang(data)
        self.delete_color_click()
        SendMessage("Đã lưu dữ liệu thành công!")

    def delete_all_row(self):
        rowCount = len(self.ngang_data)
        stt = self.stt_ngang[self.Change_number.currentIndex()]
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")

        self.table_main.setRowCount(0)
        self.table_main.setRowCount(rowCount)

        # * Render Rows STT First
        for i in range(rowCount):
            item = QTableWidgetItem(f"{stt[i]}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_main.setItem(i, 0, item)

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([]))
        self.thread.start()

    def delete_one_row(self):
        # / Check isEditor
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")

        # / Find Select Row
        data_select = self.selected_row_indices
        if data_select == -1:
            SendMessage("Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!")
            return
        for i in range(len(self.ngang_data[data_select])):
            self.ngang_data[data_select][i] = ""

        SendMessage("Đã xóa dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại")

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.updateRows]))
        self.thread.start()
        return

    def copyRowNgang(self, selceted_rows):
        row1 = selceted_rows[0]
        row2 = selceted_rows[1]
        row1_h = f"{row1 + 1:02}"  # Ensure proper formatting for display
        row2_h = f"{row2 + 1:02}"
        # / Check row2 selected, if it not null is return
        data_row2 = self.ngang_data[row2]
        for i, item in enumerate(data_row2):
            if len(str(item)) != 0:
                SendMessage(f"Dòng nhận chưa được xóa dữ liệu! (Dòng {row2_h})")
                return
        sender = self.ngang_data[row1][:]
        self.ngang_data[row2] = sender  # / Copy from sender to receiver
        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.updateRows]))
        self.thread.start()
        SendMessage(f"Đã copy dữ liệu từ dòng {row1_h} sang dòng {row2_h} thành công!")
        return

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
