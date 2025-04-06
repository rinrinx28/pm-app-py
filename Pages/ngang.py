from Pages.components.path import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QPushButton,
    QComboBox,
    QLabel,QMessageBox
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
from Controller.handler import backUpNgang, saveNgang, convert_string_format,sync_ngang
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread
import xlwings as xw
import math
import pandas as pd


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

        # / Kết nối với Excel
        self.app = xw.App(visible=True)  # Mở Excel
        self.wb = self.app.books.active  # Workbook hiện tại
        self.sheet = self.wb.sheets[0]   # Sheet đầu tiên

        self.pwd = "rindev-pm"
        
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
        self.update_excel()

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
        # widget_button_first_layout.addWidget(DeleteColor)

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
            self.toggle_editable(True)
            self.update_excel()
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
                self.toggle_editable(True)
                self.HandlerData.setText("Bật Tùy Chỉnh")
            else:
                self.toggle_editable(False)
                self.HandlerData.setText("Tắt Tùy Chỉnh")

        def saveChange():
            self.HandlerData.setText("Tắt Tùy Chỉnh")
            self.toggle_editable(False)
            self.saveRowNgang()

        def backupNgang():
            self.toggle_editable(False)
            self.HandlerData.setText("Tắt Tùy Chỉnh")
            self.backUpNgang()

        def deleteRows():
            self.delete_all_row()

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
                self.copyRowNgang(selected_rows)
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

        def move_cursor(position: str):
            """
            Di chuyển con trỏ đến vị trí được chỉ định trong cột: "first", "middle", "last"
            """
            data_range = self.sheet.range("A1").expand("right")  # Lấy phạm vi dữ liệu theo cột
            total_cols = data_range.columns.count  # Số cột trong bảng

            if total_cols == 0:
                return  # Không có dữ liệu thì không làm gì cả

            if position == "first":
                col_index = 2  # Cột đầu tiên (A)
            elif position == "middle":
                col_index = (int(total_cols) / 2) + 1  # Cột giữa
            elif position == "last":
                col_index = total_cols  # Cột cuối cùng
            else:
                SendMessage("Vị trí không hợp lệ!")
                return

            cell = self.sheet.cells(1, col_index)  # Chọn ô đầu tiên của cột tương ứng (hàng 1)
            cell.api.Activate()  # Di chuyển con trỏ đến ô đó



        self.Change_number.currentIndexChanged.connect(change_number_selected)
        SwapLine.clicked.connect(self.swapNgangRow)
        self.HandlerData.clicked.connect(changeTypeCount)
        Save.clicked.connect(saveChange)
        BackUp.clicked.connect(backupNgang)
        Delete.clicked.connect(deleteRows)
        DeleteRow.clicked.connect(self.delete_one_row)
        CopyRow.clicked.connect(copyRow_Click)
        # DeleteColor.clicked.connect(self.delete_color_click)
        SaveFile.clicked.connect(saveFile_click)
        backToFirst.clicked.connect(lambda _: move_cursor("first"))
        skipToMind.clicked.connect(lambda _: move_cursor("middle"))
        skipToEnd.clicked.connect(lambda _: move_cursor("last"))

        # Default value
        current_number = self.stay.get('ngang', 0)
        if current_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            current_number = current_ban_info_number
        self.Change_number.setCurrentIndex(current_number)

    def save_stay(self, value):
        self.ban_info["meta"]['number'] = int(value)
        self.stay['ngang'] = int(value)
        with open(os.path.join(self.current_dir, "db", 'stay.json'), "w") as file:
            json.dump(self.stay, file)
    
    # TODO Handler Events
    def toggle_editable(self, enable_edit: bool):
        """Bật/Tắt chế độ chỉnh sửa nhưng vẫn cho phép thay đổi định dạng"""
        self.sheet.api.Unprotect(Password=self.pwd)  # Bỏ bảo vệ sheet trước khi thay đổi

        if enable_edit:
            self.table_range.api.Locked = False  # Mở khóa để chỉnh sửa dữ liệu
        else:
            self.table_range.api.Locked = True  # Khóa dữ liệu nhưng không khóa định dạng

        # Bảo vệ sheet nhưng cho phép định dạng (AllowFormattingCells=True)
        self.sheet.api.Protect(Password=self.pwd, AllowFormattingCells=True, AllowFormattingColumns=True, AllowFormattingRows=True)

    def swapNgangRow(self):
        # / Check isEditor
        self.toggle_editable(True)
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
        

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.update_excel]))
        self.thread.task_completed.connect(lambda: SendMessage("Đã đổi dữ liệu dòng thành công, xin vui lòng lưu dữ liệu lại"))
        self.thread.start()
        return

    def changeDataNgangWithNumber(self, number):
        self.ngang_data = None
        with open(os.path.join(self.ngang_path, f"number_{number}.json"), "r") as file:
            data = json.load(file)
            self.ngang_data = data

    def backUpNgang(self):
        data = {}
        data["number"] = self.ban_info["meta"]['number']
        result = backUpNgang(data)

        self.ngang_info = result["stt"]

        self.stt_ngang = self.ngang_info["stt"]
        self.ngang_data = result["ngang_data"]
        self.toggle_editable(True)

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.update_excel]))
        self.thread.task_completed.connect(lambda: SendMessage("Đã khôi phục dữ liệu thành công!"))
        self.thread.start()

    def saveRowNgang(self):
        data_excel = self.get_change_history()
        data = {}
        data["update"] = data_excel
        data["number"] = self.Change_number.currentIndex()
        data["stt"] = self.stt_ngang
        data["change"] = self.ngang_info["change"]
        saveNgang(data)
        SendMessage("Đã lưu dữ liệu thành công!")

    def delete_all_row(self):
        self.toggle_editable(True)
        self.HandlerData.setText("Tắt Tùy Chỉnh")

        # self.table_main.setRowCount(0)
        # self.table_main.setRowCount(rowCount)
        
        last_row = self.sheet.range("B2").end("down").row
        last_col = self.sheet.range("B2").end("right").column
        table_range = self.sheet.range((2, 2), (last_row, last_col))
        table_range.clear_contents()

        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([]))
        self.thread.start()
        self.toggle_editable(False)

    def delete_one_row(self):
        """Xóa dòng hiện tại mà người dùng đã chọn"""
        self.toggle_editable(True)  # Cho phép chỉnh sửa trước khi xóa
        self.HandlerData.setText("Tắt Tùy Chỉnh")

        # Lấy đối tượng App từ Workbook
        app = self.sheet.book.app  

        try:
            # Lấy dòng được chọn
            data_select = app.selection.row  

            # Kiểm tra nếu không có dòng nào được chọn
            if not data_select:
                SendMessage("Xin vui lòng chọn 1 dòng để tiến hành xóa dữ liệu!")
                return

            # Xóa dòng
            self.ngang_data[data_select - 2] = [""] * 600

            # Cập nhật giao diện
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(lambda: self.updateWidget([self.update_excel]))
            self.thread.task_completed.connect(lambda: SendMessage(f"Đã xóa dòng {data_select} thành công, xin vui lòng lưu dữ liệu lại"))
            self.thread.start()

        except Exception as e:
            print(f"Lỗi khi xóa dòng: {e}")
            SendMessage("Không thể xóa dòng. Vui lòng thử lại!")

        return

    def copyRowNgang(self, selceted_rows):
        row1 = selceted_rows[0] - 2
        row2 = selceted_rows[1] - 2
        # row1_h = f"{row1:02}"  # Ensure proper formatting for display
        row2_h = f"{row2:02}"
        # / Check row2 selected, if it not null is return
        data_row2 = self.ngang_data[row2]
        for i, item in enumerate(data_row2):
            if len(str(item)) != 0:
                SendMessage(f"Dòng nhận chưa được xóa dữ liệu! (Dòng {row2_h})")
                return
        sender = self.ngang_data[row1][:]
        self.ngang_data[row2] = sender  # / Copy from sender to receiver
        self.toggle_editable(True)
        self.HandlerData.setText("Tắt Tùy Chỉnh")
        self.show_loading_screen()
        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.updateWidget([self.update_excel]))
        self.thread.task_completed.connect(lambda: SendMessage(f"Đã copy dữ liệu từ dòng {selceted_rows[0]} sang dòng {selceted_rows[1]} thành công!"))
        self.thread.start()
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

    # TODO Execl Function
    def get_change_history(self):
        # Đọc dữ liệu từ bảng
        data = pd.DataFrame(self.sheet.range("B2").expand().value)
        data = data.fillna("")
        number_change = []
        for j, row in enumerate(data.values.tolist()):
            row_v = []
            for k, cell in enumerate(row):
                if cell != "":
                    # Chuyển chuỗi thành số thực (float) trước
                    cell = float(cell)
                    # Sau đó áp dụng math.floor()
                    cell = math.floor(cell)
                    row_v.append(cell)
                else:
                    row_v.append(cell)
            number_change.append(row_v)
        return number_change  # Trả về danh sách lịch sử thay đổi

    def update_excel(self):
        # TODO Data configuration
        data = self.ngang_data
        stt = self.stt_ngang[self.ban_info["meta"]['number']]
        meta_number = self.stay.get('ngang', 0)
        if meta_number == 0:
            current_ban_info_number = self.ban_info["meta"]["number"]
            meta_number = current_ban_info_number
        rowCount = len(data)
        colCount = len(data[0])

        # TODO Render Header Table
        header_lables = [f"C.{i+1}" for i in range(colCount)]
        data_excel = []

        # TODO: Render Rows
        for i in range(rowCount):
            row_data = []
            row_data.append(f"{stt[i]:02}")
            # Thêm giá trị từng cột
            for j, value in enumerate(data[i]):
                row_data.append(value)
            data_excel.append(row_data)

        # Ghi dữ liệu vào Excel
        self.sheet.range("A1").value = [["STT"] + header_lables]  # Tiêu đề
        self.sheet.range("A2").value = data_excel  # Dữ liệu

        # Tự động căn chỉnh kích thước cột dựa trên nội dung
        self.sheet.autofit('c')  # 'c' để autofit các cột
        
        # Chọn ô B1 (Excel sẽ đóng băng tất cả cột bên trái ô này, tức là cột A)
        self.sheet.range("B2").select()

        # Đóng băng cột A
        self.wb.app.api.ActiveWindow.FreezePanes = True
        self.toggle_editable(False)

    # TODO Handler Question
    def showQuestion(self):
        icon = Path().path_logo()
        message = QMessageBox()
        message.setWindowTitle("Thông Báo")
        message.setText(f"Bạn có chắc chắn đồng bộ dữ liệu bảng ngang {self.name}")
        message.setWindowIcon(QIcon(icon))  # Thay bằng đường dẫn đến icon của bạn
        message.setFont(self.font)
        message.setIcon(QMessageBox.Icon.Question)
        message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message.setDefaultButton(QMessageBox.No)  # Đặt nút "No" làm mặc định

        # Hiển thị hộp thoại và lấy kết quả
        result = message.exec()

        if result == QMessageBox.Yes:
            data = {}
            data["update"] = self.ngang_data
            data["number"] = self.ban_info["meta"]['number']
            data["stt"] = self.ngang_info["stt"]
            data["change"] = self.ngang_info["change"]
            data['name'] = self.ban_info['thong']['name']
            data["pm"] = self.ban_info["thong"]["pm"]
            msg = sync_ngang(data)
            self.show_loading_screen()
            self.thread = Thread()
            self.thread.task_completed.connect(
                lambda: SendMessage(f'{msg} {self.name}')
            )
            self.thread.start()

    def closeEvent(self, event):
        """Xử lý khi cửa sổ PySide6 đóng"""
        if self.wb:
            self.wb.close()  # Đóng workbook mà không lưu
        if self.app:
            self.app.quit()  # Đóng Excel ngay lập tức
        event.accept()  # Chấp nhận sự kiện đóng