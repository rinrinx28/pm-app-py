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
    css_button_start,
    Font,
    Note,
    SendMessage,
    css_title,
)
import json
import os
from Controller.handler import backUpNgang, saveNgang, convert_string_format,sync_ngang, save_ngang_backup,convert_string_to_type_count
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread

prev_selected_rows = set()


class NgangPage(QWidget):

    def __init__(self):
        super().__init__()
        self.path = Path()
        self.current_dir = self.path.current_dir
        
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
            
        with open(os.path.join(self.current_dir, "db", 'stay.json'), "r") as file:
            self.stay = json.load(file)

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

        self.name = convert_string_format(ban_thong_name)
        co_so = change_number if change_number != 0 else "gốc"
        title_text = (
            f"Trạng Thái Bảng Tính: C{ban_col[0]} đến C{ban_col[1]} / T{ban_thong_value[0]} đến "
            + f"T{ban_thong_value[1]} /  Cơ {co_so} / "
            + f"Số dòng: {row_count}/{max_row}"
        )
        title = QLabel(title_text)
        title.setStyleSheet(css_title)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_text_table = f"Bảng Ngang: {self.name} - 600 Cột"
        title_table = QLabel(title_text_table)
        title_table.setStyleSheet(css_title)
        title_table.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout_ngang.addWidget(title_table)

        self.layout_ngang.addWidget(title)

        current_number = self.stay.get('ngang', 0)
        if current_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            current_number = current_ban_info_number
        # / Note
        if current_number != 0:
           current_number -= 1
        else:
            current_number = 10
        note = Note[current_number]
        note_name = current_number if change_number != 0 else "gốc"
        self.note = QLabel(f"Cơ {note_name} - {note}")
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
        self.changeDataNgangWithNumber(self.stay.get('ngang', 0))   
        self.renderButton()
        self.renderTable()

    # TODO Handler render component
    def renderButton(self):
        group_button_widget = QWidget()
        self.button_layout.addWidget(group_button_widget)
        group_button_layout = QVBoxLayout(group_button_widget)

        widget_button_first = QWidget()
        group_button_layout.addWidget(widget_button_first)
        widget_button_first_layout = QHBoxLayout(widget_button_first)
        # / Back to first row
        backToFirst = QPushButton("Về Cột Đầu")
        backToFirst.setStyleSheet(css_button_start)
        backToFirst.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(backToFirst)

        # / SwapLine Button
        SwapLine = QPushButton("Đổi Dòng DL")
        SwapLine.setStyleSheet(css_button_cancel)
        SwapLine.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(SwapLine)

        # / Copy Row Button
        CopyRow = QPushButton("Chép Dòng DL")
        CopyRow.setStyleSheet(css_button_cancel)
        CopyRow.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(CopyRow)
        

        # / Skip to mid row
        skipToMind = QPushButton("Về Cột Giữa")
        skipToMind.setStyleSheet(css_button_start)
        skipToMind.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(skipToMind)

        # / Create Delete
        DeleteRow = QPushButton("Xóa DL dòng")
        DeleteRow.setStyleSheet(css_button_cancel)
        DeleteRow.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(DeleteRow)

        # / Delete Button
        Delete = QPushButton("Xóa Tất Cả DL")
        Delete.setStyleSheet(css_button_cancel)
        Delete.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(Delete)

        # / Delete Button
        DeleteColor = QPushButton("Xóa Màu")
        DeleteColor.setStyleSheet(css_button_cancel)
        DeleteColor.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(DeleteColor)

        # / Skip to end row
        skipToEnd = QPushButton("Về Cột Cuối")
        skipToEnd.setStyleSheet(css_button_start)
        skipToEnd.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_first_layout.addWidget(skipToEnd)

        
        widget_button_second = QWidget()
        group_button_layout.addWidget(widget_button_second)
        widget_button_second_layout = QHBoxLayout(widget_button_second)

        # / Change_number Button
        # TODO Config Change Number
        number = 11
        self.Change_number = QComboBox()
        self.Change_number.setStyleSheet("font-size: 24px;line-height: 32px;")
        self.Change_number.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_second_layout.addWidget(self.Change_number)
        self.Change_number.addItem(f"Cơ gốc")
        for i in range(1, number):
            self.Change_number.addItem(f"Cơ {i}")

        # / BackUp Button
        BackUp = QPushButton("Khôi Phục DL Gốc")
        BackUp.setStyleSheet(css_button_submit)
        BackUp.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_second_layout.addWidget(BackUp)

        # / Create AutoSaveFiles
        SaveFile = QPushButton("Đồng Bộ DL")
        SaveFile.setStyleSheet(css_button_submit)
        SaveFile.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_second_layout.addWidget(SaveFile)

        # / Create HandlerData
        type_input = "Tắt Tùy Chỉnh"
        self.HandlerData = QPushButton(type_input)
        self.HandlerData.setStyleSheet(css_button_submit)
        self.HandlerData.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_second_layout.addWidget(self.HandlerData)

        # / Save Button
        Save = QPushButton("Lưu")
        Save.setStyleSheet(css_button_submit)
        Save.setCursor(QCursor(Qt.PointingHandCursor))
        widget_button_second_layout.addWidget(Save)

        # TODO Handler Button
        def change_number_selected():
            value = self.Change_number.currentIndex()
            self.save_stay(value)
            self.changeDataNgangWithNumber(value)
            self.updateRows()
            if value != 0:
                note = Note[value - 1]
                self.note.setText(f"Cơ {value} - {note}")
                self.note.setScaledContents(True)
            else:
                note = Note[10]
                self.note.setText(f"Cơ gốc - {note}")
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
        
        def saveFile_click():
            type_count = convert_string_to_type_count(self.ban_info["thong"]["name"])
            data = {}
            data["update"] = self.ngang_data
            data["number"] = self.ban_info["meta"]['number']
            data["stt"] = self.ngang_info["stt"]
            data["change"] = self.ngang_info["change"]
            data["type_count"] = type_count if type_count == 0 else 1 if type_count == '1a' else 3 if type_count == '1b' else 2
            data['name'] = self.ban_info['thong']['name']
            msg = sync_ngang(data)
            self.delete_color_click()
            SendMessage(f'{msg} {self.name}')

        def back_to_first():
            row = self.table_main.rowCount() - 2  # Get the current row
            item = self.table_main.item(0, 0)  # Get the first column item
            self.table_main.scrollToItem(item, QHeaderView.ScrollHint.PositionAtCenter)
            return

        def skip_to_end():
            row = self.table_main.rowCount() - 2  # Get the current row
            col = self.table_main.columnCount() - 1  # Get the current row
            item = self.table_main.item(0, col)  # Get the first column item
            self.table_main.scrollToItem(item, QHeaderView.ScrollHint.PositionAtCenter)
            return
        
        def skip_to_mid():
            row = self.table_main.rowCount() - 2  # Get the current row
            col = self.table_main.columnCount() - 1  # Get the current row
            item = self.table_main.item(0, col // 2)  # Get the first column item
            self.table_main.scrollToItem(item, QHeaderView.ScrollHint.PositionAtCenter)
            return


        self.Change_number.currentIndexChanged.connect(change_number_selected)
        SwapLine.clicked.connect(self.swapNgangRow)
        self.HandlerData.clicked.connect(changeTypeCount)
        Save.clicked.connect(saveChange)
        BackUp.clicked.connect(backupNgang)
        Delete.clicked.connect(deleteRows)
        DeleteRow.clicked.connect(self.delete_one_row)
        CopyRow.clicked.connect(copyRow_Click)
        DeleteColor.clicked.connect(self.delete_color_click)
        SaveFile.clicked.connect(saveFile_click)
        backToFirst.clicked.connect(back_to_first)
        skipToEnd.clicked.connect(skip_to_end)
        skipToMind.clicked.connect(skip_to_mid)

        # Default value
        current_number = self.stay.get('ngang', 0)
        if current_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            current_number = current_ban_info_number
        self.Change_number.setCurrentIndex(current_number)

    def renderTable(self):
        data = self.ngang_data
        # TODO Data configuration
        colCount = len(data[0][:300])
        self.start_col = 0
        self.value_col = 0

        self.table_main = QTableWidget()
        self.widget_main.addWidget(self.table_main)

        # TODO Config table
        self.table_main.setColumnCount(colCount)  # / Add STT into col

        # / Render Rows
        self.updateRows()
        # TODO Render Header Table
        header_lables = [f"C.{i+1}" for i in range(colCount)]
        self.table_main.setHorizontalHeaderLabels(header_lables)

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

        # self.table_main.horizontalScrollBar().valueChanged.connect(self.freeze_col_stt)

        self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.table_main.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

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

        def changeValue(row, column):
            isEdit = self.table_main.editTriggers()
            if isEdit == QTableWidget.EditTrigger.NoEditTriggers:
                return
            else:
                item = self.table_main.item(row, column)
                filter_db = [
                    item
                    for item in self.ngang_info["change"]
                    if item["row"] != row
                    and item["column"] != column
                    and item["number"] != self.ban_info["meta"]['number']
                ]
                filter_data = [
                    item
                    for item in self.ngang_info["change"]
                    if item["row"] == row
                    and item["column"] == column
                    and item["number"] == self.ban_info["meta"]['number']
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
                            "column": column,
                            "number": self.ban_info["meta"]['number'],
                            "new": item.text(),
                            "old": self.ngang_data[row][column],
                        }
                    )
                    item.setBackground(self.cyan)
                self.ngang_data[row][column] = item.text()
                    

        self.table_main.itemSelectionChanged.connect(selectedRow)
        self.table_main.cellChanged.connect(changeValue)

    def save_stay(self, value):
        self.ban_info["meta"]['number'] = int(value)
        self.stay['ngang'] = int(value)
        with open(os.path.join(self.current_dir, "db", 'stay.json'), "w") as file:
            json.dump(self.stay, file)
    
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
        stt = self.stt_ngang[self.ban_info["meta"]['number']]
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

        self.stt_ngang[self.ban_info["meta"]['number']] = shifted_stt
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
        if self.table_main is None:
            return
        self.table_main.clearSelection()
        meta_number = self.stay.get('ngang', 0)
        if meta_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            meta_number = current_ban_info_number
        data = self.ngang_data
        rowCount = len(data[:35])
        self.table_main.setRowCount(0)
        # Thiết lập số hàng
        self.table_main.setRowCount(rowCount)

        # TODO: Render Rows
        for i in range(rowCount):
            # Thêm giá trị từng cột
            for j, value in enumerate(data[i]):
                item = QTableWidgetItem(f"{value}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Kiểm tra thay đổi
                change_info = next(
                    (change for change in self.ngang_info["change"]
                    if change["row"] == i and change["column"] == j and change["number"] == meta_number),
                    None
                )
                if change_info and change_info["new"] != change_info["old"]:
                    item.setBackground(self.cyan)

                # Đặt vào bảng
                self.table_main.setItem(i, j, item)

    def backUpNgang(self):
        data = {}
        data["number"] = self.ban_info["meta"]['number']
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
        isEditor = self.table_main.editTriggers()
        if isEditor != QTableWidget.EditTrigger.NoEditTriggers:
            self.table_main.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.HandlerData.setText("Tắt Tùy Chỉnh")

        # self.table_main.setRowCount(0)
        # self.table_main.setRowCount(rowCount)
        self.table_main.clearContents()

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
        data_select = list(self.selected_row_indices)
        if len(data_select) == -1:
            SendMessage("Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!")
            return
        for row in data_select:
            for i in range(len(self.ngang_data[row])):
                self.ngang_data[row][i] = ""

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
