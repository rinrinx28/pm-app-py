from PySide6.QtWidgets import (
    QDialog,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QCheckBox,
    QScrollArea,
)
from Pages.components.path import Path
from PySide6.QtGui import QIcon
from PySide6.QtGui import Qt, QCursor
from Controller.handler import updateColorInsert, enableTables, save_setting_tables
from Pages.components.stylesheet import css_button_submit, css_input, SendMessage

from functools import partial


class SettingTable(QDialog):
    def __init__(self, ban_info):
        super().__init__()
        # / Config Icon Windows
        self.path = Path()
        self.ban_info = ban_info
        self.change_data = self.ban_info["meta"]["number"]
        self.old_data = self.ban_info["meta"]["notice"]
        self.col_e = self.ban_info["meta"]["setting"]
        self.col_ngang = self.ban_info
        self.col_thong = self.ban_info["thong"]
        self.maxRow = self.ban_info["meta"]
        self.buttons = self.ban_info["meta"]["buttons"]
        icon = self.path.path_logo()
        self.current_widget = None

        # / Create Dialog Windows
        self.setWindowTitle("Cài đặt bảng")
        self.setWindowIcon(QIcon(icon))
        self.showFullScreen()

        # Create main layout
        dialog_main_layout = QVBoxLayout()

        # Create a QTabWidget
        tab_widget = QTabWidget()
        # Add tabs
        tab_widget.addTab(self.create_tab_main_setting(), "Cài Đặt Chung")
        tab_widget.addTab(self.create_tab_2_setting_bm(), "Tùy Chọn Bảng Màu")
        tab_widget.addTab(self.create_tab_3_setting_col_d_bm(), "Cài Đặt Bảng Màu")

        # Add the QTabWidget to the main layout
        dialog_main_layout.addWidget(tab_widget)
        # Set the main layout as the dialog's layout
        self.setLayout(dialog_main_layout)
    
    def showButton(self):
        button_widget = QWidget()
        # Create custom buttons
        button_layout = QHBoxLayout(button_widget)  # Layout for the buttons

        ok_button = QPushButton("Lưu")  # Custom OK button
        ok_button.setFixedWidth(150)
        ok_button.setStyleSheet(
            """
            QPushButton {
                border-radius: 8px;
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                background-color: #1D4ED8;
            }
            QPushButton:hover {
                background-color: #1E40AF;
            }

        """
        )
        ok_button.setCursor(QCursor(Qt.PointingHandCursor))
        ok_button.clicked.connect(
            lambda: self.submit_click(self)
        )  # Connect the custom action

        cancel_button = QPushButton("Hủy bỏ")  # Custom Cancel button
        cancel_button.setStyleSheet(
            """
            QPushButton {
                border-radius: 8px;
                font-size: 24px;
                font-weight: 600;
                color: #111827;
                background-color: #ffffff;
            }
            QPushButton:hover {
                color: #1D4ED8;
                background-color: #F3F4F6;
            }

        """
        )
        cancel_button.setFixedWidth(150)
        cancel_button.setCursor(QCursor(Qt.PointingHandCursor))
        cancel_button.clicked.connect(self.reject)  # Connect to reject action

        save_button = QPushButton("Đồng Bộ Cài Đặt")  # Custom save button
        save_button.setStyleSheet(
            """
            QPushButton {
                border-radius: 8px;
                font-size: 24px;
                font-weight: 600;
                color: #111827;
                background-color: #ffffff;
            }
            QPushButton:hover {
                color: #1D4ED8;
                background-color: #F3F4F6;
            }

        """
        )
        save_button.setCursor(QCursor(Qt.PointingHandCursor))
        save_button.clicked.connect(
            lambda _: self.save_setting_all_app(
                {
                    "col": self.ban_info["col"],
                    "meta": self.ban_info["meta"],
                    "thong": {
                        "value": self.ban_info["thong"]["value"],
                        "name": self.ban_info["thong"]["name"],
                    },
                }
            )
        )  # Connect to reject action
        # Add buttons to the button layout
        horizontalSpacer = QSpacerItem(
            40, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        button_layout.addItem(horizontalSpacer)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        return button_widget

    def save_setting_all_app(self, data):
        msg = save_setting_tables(data)
        return SendMessage(msg)

    def create_tab_main_setting(self):
        tab = QWidget()
        layout_tab = QVBoxLayout(tab)

        # / Setting Color Table Count
        s_table_count_color_w = QWidget()
        s_table_count_color_w.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_table_count_color_w)
        s_table_count_color_l = QGridLayout(s_table_count_color_w)

        # / Setting Color table count > Lable | SpinBox
        s_table_count_color_lable = QLabel("Báo Màu Bảng Tính")
        s_table_count_color_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_table_count_color_l.addWidget(s_table_count_color_lable, 0, 0)

        s_table_count_color_spinbox_1 = QSpinBox()
        s_table_count_color_l.addWidget(s_table_count_color_spinbox_1, 1, 0)
        s_table_count_color_spinbox_1.setMinimum(0)
        s_table_count_color_spinbox_1.setMaximum(120)
        s_table_count_color_spinbox_1.setStyleSheet(css_input)
        s_table_count_color_spinbox_1.setValue(self.old_data["count"][0])

        s_table_count_color_spinbox_2 = QSpinBox()
        s_table_count_color_l.addWidget(s_table_count_color_spinbox_2, 1, 1)
        s_table_count_color_spinbox_2.setMinimum(0)
        s_table_count_color_spinbox_2.setMaximum(120)
        s_table_count_color_spinbox_2.setStyleSheet(css_input)
        s_table_count_color_spinbox_2.setValue(self.old_data["count"][1])

        # / Setting Values Thong Config
        s_values_thong_w = QWidget()
        s_values_thong_w.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_values_thong_w)
        s_values_thong_l = QGridLayout(s_values_thong_w)

        # / Setting Values Thong Config > Lable | SpinBox
        s_values_thong_lable = QLabel("Số Thông")
        s_values_thong_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_values_thong_l.addWidget(s_values_thong_lable, 0, 0)

        s_values_thong_spinbox_1 = QSpinBox()
        s_values_thong_l.addWidget(s_values_thong_spinbox_1, 1, 0)
        s_values_thong_spinbox_1.setMinimum(0)
        s_values_thong_spinbox_1.setMaximum(120)
        s_values_thong_spinbox_1.setStyleSheet(css_input)
        s_values_thong_spinbox_1.setValue(self.col_thong["value"][0])

        s_values_thong_spinbox_2 = QSpinBox()
        s_values_thong_l.addWidget(s_values_thong_spinbox_2, 1, 1)
        s_values_thong_spinbox_2.setMinimum(0)
        s_values_thong_spinbox_2.setMaximum(120)
        s_values_thong_spinbox_2.setStyleSheet(css_input)
        s_values_thong_spinbox_2.setValue(self.col_thong["value"][1])

        # / Setting Value Ngang
        s_values_ngang_w = QWidget()
        s_values_ngang_w.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_values_ngang_w)
        s_values_ngang_l = QGridLayout(s_values_ngang_w)

        # / Setting Value Ngang > Lable | SpinBox
        s_values_ngang_lable = QLabel("Số Cột Ngang")
        s_values_ngang_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_values_ngang_l.addWidget(s_values_ngang_lable, 0, 0)

        s_values_ngang_spinbox_1 = QSpinBox()
        s_values_ngang_l.addWidget(s_values_ngang_spinbox_1, 1, 0)
        s_values_ngang_spinbox_1.setMinimum(0)
        s_values_ngang_spinbox_1.setMaximum(120)
        s_values_ngang_spinbox_1.setStyleSheet(css_input)
        s_values_ngang_spinbox_1.setValue(self.col_ngang["col"][0])

        s_values_ngang_spinbox_2 = QSpinBox()
        s_values_ngang_l.addWidget(s_values_ngang_spinbox_2, 1, 1)
        s_values_ngang_spinbox_2.setMinimum(0)
        s_values_ngang_spinbox_2.setMaximum(120)
        s_values_ngang_spinbox_2.setStyleSheet(css_input)
        s_values_ngang_spinbox_2.setValue(self.col_ngang["col"][1])

        # / Setting Max row
        s_max_row_w = QWidget()
        s_max_row_w.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_max_row_w)
        s_max_row_l = QGridLayout(s_max_row_w)
        # / Setting Max row > Lable | SpinBox
        s_max_row_lable = QLabel("Tối Đa Dòng Tồn Tại")
        s_max_row_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_max_row_l.addWidget(s_max_row_lable, 0, 0)

        s_max_row_spinbox_1 = QSpinBox()
        s_max_row_l.addWidget(s_max_row_spinbox_1, 1, 0)
        s_max_row_spinbox_1.setMinimum(1)
        s_max_row_spinbox_1.setMaximum(999)
        s_max_row_spinbox_1.setStyleSheet(css_input)
        s_max_row_spinbox_1.setValue(self.maxRow["maxRow"])

        # / Setting Value Change
        s_value_change_w = QWidget()
        s_value_change_w.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_value_change_w)
        s_value_change_l = QGridLayout(s_value_change_w)

        # / Setting Max row > Lable | SpinBox
        s_value_change_lable = QLabel("Bộ Chuyển Đổi")
        s_value_change_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_value_change_l.addWidget(s_value_change_lable, 0, 0)

        s_value_change_spinbox_1 = QSpinBox()
        s_value_change_l.addWidget(s_value_change_spinbox_1, 1, 0)
        s_value_change_spinbox_1.setMinimum(0)
        s_value_change_spinbox_1.setMaximum(10)
        s_value_change_spinbox_1.setStyleSheet(css_input)
        s_value_change_spinbox_1.setValue(self.ban_info["meta"]["number"])

        # TODO Handler Func
        def value_table_count_color(value):
            value1 = s_table_count_color_spinbox_1.value()
            value2 = s_table_count_color_spinbox_2.value()
            self.old_data["count"] = [value1, value2]

        def value_thong(value):
            value1 = s_values_thong_spinbox_1.value()
            value2 = s_values_thong_spinbox_2.value()
            self.col_thong["value"] = [value1, value2]

        def value_ngang(value):
            value1 = s_values_ngang_spinbox_1.value()
            value2 = s_values_ngang_spinbox_2.value()
            self.col_ngang["col"] = [value1, value2]

        def value_max_row(value):
            self.maxRow["maxRow"] = value

        def value_change(value):
            self.ban_info["meta"]["number"] = value

        # / Table Count Color Event Change
        s_table_count_color_spinbox_1.valueChanged.connect(value_table_count_color)
        s_table_count_color_spinbox_2.valueChanged.connect(value_table_count_color)

        # / Value thong Event Change
        s_values_thong_spinbox_1.valueChanged.connect(value_thong)
        s_values_thong_spinbox_2.valueChanged.connect(value_thong)

        # / Value ngang Event Change
        s_values_ngang_spinbox_1.valueChanged.connect(value_ngang)
        s_values_ngang_spinbox_2.valueChanged.connect(value_ngang)

        # / Value Max Row Event Change
        s_max_row_spinbox_1.valueChanged.connect(value_max_row)

        # / Value Change Event Change
        s_value_change_spinbox_1.valueChanged.connect(value_change)

        button = self.showButton()
        layout_tab.addWidget(button)


        verticalSpacer2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout_tab.addItem(verticalSpacer2)

        return tab

    def create_tab_2_setting_bm(self):
        # / Config Data
        data = self.ban_info["meta"]["tables"]
        tab = QWidget()
        layout = QGridLayout(tab)

        lable = QLabel("Chọn Bảng Màu Toán")
        lable.setStyleSheet(
            """
            QLabel{
                font-size: 24px;
                color: red;
            }

            """
        )

        # / BM1
        lable_m1 = QCheckBox("Bảng Màu M1")
        lable_m1.setChecked(data[0]["enable"])
        lable_m1.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(0, checked)
        )
        lable_m1.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        lable_m1.setDisabled(True)
        # / BM2
        lable_m2 = QCheckBox("Bảng Màu M2")
        lable_m2.setChecked(data[1]["enable"])
        lable_m2.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(1, checked)
        )
        lable_m2.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM3
        lable_m3 = QCheckBox("Bảng Màu M3")
        lable_m3.setChecked(data[2]["enable"])
        lable_m3.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(2, checked)
        )
        lable_m3.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM4
        lable_m4 = QCheckBox("Bảng Màu M4")
        lable_m4.setChecked(data[3]["enable"])
        lable_m4.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(3, checked)
        )
        lable_m4.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM5
        lable_m5 = QCheckBox("Bảng Màu M5")
        lable_m5.setChecked(data[4]["enable"])
        lable_m5.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(4, checked)
        )
        lable_m5.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM6
        lable_m6 = QCheckBox("Bảng Màu M6")
        lable_m6.setChecked(data[5]["enable"])
        lable_m6.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(5, checked)
        )
        lable_m6.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM7
        lable_m7 = QCheckBox("Bảng Màu M7")
        lable_m7.setChecked(data[6]["enable"])
        lable_m7.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(6, checked)
        )
        lable_m7.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM8
        lable_m8 = QCheckBox("Bảng Màu M8")
        lable_m8.setChecked(data[7]["enable"])
        lable_m8.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(7, checked)
        )
        lable_m8.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM9
        lable_m9 = QCheckBox("Bảng Màu M9")
        lable_m9.setChecked(data[8]["enable"])
        lable_m9.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(8, checked)
        )
        lable_m9.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        # / BM10
        lable_m10 = QCheckBox("Bảng Màu M10")
        lable_m10.setChecked(data[9]["enable"])
        lable_m10.checkStateChanged.connect(
            lambda checked: self.handle_save_enable_tables(9, checked)
        )
        lable_m10.setStyleSheet(
            """
            QCheckBox{
                padding: 4px;
                font-size: 24px;
                spacing: 5px;
            }
            """
        )
        layout.addWidget(lable, 0, 0)

        # / Column 1
        layout.addWidget(lable_m1, 1, 0)
        layout.addWidget(lable_m2, 2, 0)
        layout.addWidget(lable_m3, 3, 0)
        layout.addWidget(lable_m4, 4, 0)
        layout.addWidget(lable_m5, 5, 0)

        # / Column 2
        layout.addWidget(lable_m6, 1, 1)
        layout.addWidget(lable_m7, 2, 1)
        layout.addWidget(lable_m8, 3, 1)
        layout.addWidget(lable_m9, 4, 1)
        layout.addWidget(lable_m10, 5, 1)

        button = self.showButton()
        layout.addWidget(button)

        horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        # Add a vertical spacer to the layout
        verticalSpacer1 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        layout.addItem(verticalSpacer1, 6, 0, 1, 1)
        layout.addItem(horizontalSpacer, 6, 2, 1, 1)
        return tab

    def create_tab_3_setting_col_d_bm(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # / Main Widget
        main = QWidget()
        self.main_layout = QVBoxLayout(main)
        self.handle_change_setting_col_d_bm()

        # / Button Widget
        button_w = QWidget()
        button_l = QHBoxLayout(button_w)
        i = 0
        while i < 10:
            button = QPushButton(f"BM{i + 1}")
            button.setStyleSheet(css_button_submit)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.clicked.connect(partial(self.handle_change_setting_col_d_bm, i))
            button_l.addWidget(button)
            i = i + 1

        layout.addWidget(main)
        layout.addWidget(button_w)
        button = self.showButton()
        layout.addWidget(button)
        # Add a vertical spacer to the layout
        verticalSpacer1 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout.addItem(verticalSpacer1)
        return tab

    def clear_layout_main(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def submit_click(self, dialog):
        data = {
            "id": self.ban_info["id"],
            "notice": self.old_data,
            "col_e": self.col_e["col_e"],
            "col_e2": self.col_e["col_e2"],
            "col_e3": self.col_e["col_e3"],
            "col_e4": self.col_e["col_e4"],
            "col_e5": self.col_e["col_e5"],
            "col_e6": self.col_e["col_e6"],
            "col_e7": self.col_e["col_e7"],
            "col_e8": self.col_e["col_e8"],
            "col_e9": self.col_e["col_e9"],
            "col_e10": self.col_e["col_e10"],
            "number": self.ban_info["meta"]["number"],
            "col": self.col_ngang["col"],
            "thong": self.col_thong,
            "maxRow": self.maxRow["maxRow"],
            "buttons": self.ban_info["meta"]["buttons"],
            "tables": self.ban_info["meta"]["tables"],
        }
        msg = updateColorInsert(data)
        SendMessage(msg["msg"])
        if msg["status"]:
            dialog.reject()
            SendMessage("Xin vui lòng thoát và vào lại bảng tính để cập nhật cài đặt")
        return

    def handle_save_enable_tables(self, index, status):
        data = self.ban_info["meta"]["tables"]
        data[index] = {
            "enable": (True if status == Qt.CheckState.Checked else False),
            "col_d": data[index]["col_d"],
        }
        enableTables(data)

    def handle_change_setting_col_d_bm(self, type=0):
        info_table = self.ban_info["meta"]["tables"][type]
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel(f"Bộ tùy chỉnh số cột của D bảng màu M{type + 1}")
        title.setStyleSheet("font-size:24px;\ncolor:red;")
        layout.addWidget(title)

        # Tạo scroll area
        scroll_area = QScrollArea(widget)
        scroll_area.setMaximumHeight(500)
        scroll_area.setWidgetResizable(True)

        # Tạo widget chứa các nội dung để thêm vào scroll area
        content_widget = QWidget()
        content_layout = QGridLayout(content_widget)
        content_layout.setSpacing(20)

        # Danh sách để lưu trữ tất cả các QSpinBox
        spin_boxes = []

        # Hàm để tắt hoặc bật tất cả SpinBox
        def toggle_all_spinboxes():
            all_enabled = any(spinbox.isEnabled() for spinbox in spin_boxes)
            for spinbox in spin_boxes:
                spinbox.setEnabled(not all_enabled)

        # Thêm các widget vào lưới 4 cột
        for i in range(120):
            widget_label = QWidget()
            widget_label.setStyleSheet("border: 1px solid #999;")
            label_layout = QVBoxLayout(widget_label)

            label = QLabel(f"D {i + 1}/M{type + 1}")
            label.setStyleSheet("font-size: 24px;border: 0px;")

            spin_label = QSpinBox()
            spin_label.setDisabled(True)
            spin_label.setMinimum(1)
            spin_label.setStyleSheet("font-size: 24px;border: 0px;")
            spin_label.setValue(info_table["col_d"][i])
            spin_label.valueChanged.connect(partial(self.change_table_col_d, type, i))

            spin_boxes.append(spin_label)

            label_layout.addWidget(label)
            label_layout.addWidget(spin_label)

            # Thêm widget vào lưới 4 cột
            row = i // 4
            col = i % 4
            content_layout.addWidget(widget_label, row, col)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # / Add Notice Color
        notice = QWidget()
        notice.setStyleSheet("border: 1px solid #999;")
        notice_l = QVBoxLayout(notice)
        layout.addWidget(notice)

        # / Lable > SpinBox
        notice_lable = QLabel(f"Báo Màu M{type + 1}")
        notice_lable.setStyleSheet("border: 0px;font-size:24px;")
        notice_l.addWidget(notice_lable)

        notice_spinBox_w = QWidget()
        notice_spinBox_w.setStyleSheet("border: 0px;")
        notice_spinBox_l = QHBoxLayout(notice_spinBox_w)
        notice_l.addWidget(notice_spinBox_w)
        notice_spinBox_1 = QSpinBox()
        notice_spinBox_1.setMinimum(0)
        notice_spinBox_1.setMaximum(999)
        notice_spinBox_1.setStyleSheet("font-size: 24px;border: 0px;")
        notice_spinBox_1.setValue(
            self.old_data[f'color{"M" + str(type + 1) if type != 0 else ""}'][0]
        )
        notice_spinBox_2 = QSpinBox()
        notice_spinBox_2.setMinimum(0)
        notice_spinBox_2.setMaximum(999)
        notice_spinBox_2.setStyleSheet("font-size: 24px;border: 0px;")
        notice_spinBox_2.setValue(
            self.old_data[f'color{"M" + str(type + 1) if type != 0 else ""}'][1]
        )

        notice_spinBox_l.addWidget(notice_spinBox_1)
        notice_spinBox_l.addWidget(notice_spinBox_2)

        notice_spinBox_1.setDisabled(True)
        notice_spinBox_2.setDisabled(True)
        spin_boxes.append(notice_spinBox_1)
        spin_boxes.append(notice_spinBox_2)

        # / Add Config Col D
        config_col = QWidget()
        config_col.setStyleSheet("border: 1px solid #999;")
        config_col_l = QVBoxLayout(config_col)
        layout.addWidget(config_col)

        # / Lable > SpinBox
        config_col_lable = QLabel(f"Thông Kê D M{type + 1}")
        config_col_lable.setStyleSheet("border: 0px;font-size:24px;")
        config_col_l.addWidget(config_col_lable)

        config_col_spinBox_w = QWidget()
        config_col_spinBox_w.setStyleSheet("border: 0px;")
        config_col_spinBox_l = QHBoxLayout(config_col_spinBox_w)
        config_col_l.addWidget(config_col_spinBox_w)

        config_col_spinBox_1 = QSpinBox()
        config_col_spinBox_1.setMinimum(1)
        config_col_spinBox_1.setMaximum(120)
        config_col_spinBox_1.setStyleSheet("font-size: 24px;border: 0px;")
        config_col_spinBox_1.setValue(
            self.col_e[f"col_e{type + 1 if type != 0 else ''}"][0]
        )
        config_col_spinBox_2 = QSpinBox()
        config_col_spinBox_2.setMinimum(1)
        config_col_spinBox_2.setMaximum(120)
        config_col_spinBox_2.setStyleSheet("font-size: 24px;border: 0px;")
        config_col_spinBox_2.setValue(
            self.col_e[f"col_e{type + 1 if type != 0 else ''}"][1]
        )

        config_col_spinBox_l.addWidget(config_col_spinBox_1)
        config_col_spinBox_l.addWidget(config_col_spinBox_2)

        config_col_spinBox_1.setDisabled(True)
        config_col_spinBox_2.setDisabled(True)
        spin_boxes.append(config_col_spinBox_1)
        spin_boxes.append(config_col_spinBox_2)

        # verticalSpacer2 = QSpacerItem(
        #     20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        # )
        # layout.addItem(verticalSpacer2)

        # Tạo nút để bật/tắt tất cả SpinBox
        toggle_button = QPushButton("Bật Tắt Tùy Chỉnh D")
        toggle_button.setStyleSheet(css_button_submit)
        toggle_button.clicked.connect(toggle_all_spinboxes)
        layout.addWidget(toggle_button)

        # TODO Handler Func
        # / Notice Color
        notice_spinBox_1.valueChanged.connect(
            partial(
                self.value_change_col_table_color_notice,
                f'color{"M" + str(type + 1) if type != 0 else ""}',
                0,
            )
        )
        notice_spinBox_2.valueChanged.connect(
            partial(
                self.value_change_col_table_color_notice,
                f'color{"M" + str(type + 1) if type != 0 else ""}',
                1,
            )
        )

        # / Config Col
        config_col_spinBox_1.valueChanged.connect(
            partial(
                self.value_change_col_table_color_config_col,
                f"col_e{type + 1 if type != 0 else ''}",
                0,
            )
        )
        config_col_spinBox_2.valueChanged.connect(
            partial(
                self.value_change_col_table_color_config_col,
                f"col_e{type + 1 if type != 0 else ''}",
                1,
            )
        )

        if self.current_widget:
            self.clear_layout_main(self.main_layout)

        self.current_widget = widget
        self.main_layout.addWidget(self.current_widget)

    def change_table_col_d(self, type, index, value):
        self.ban_info["meta"]["tables"][type]["col_d"][index] = value

    def value_change_col_table_color_notice(self, type, index, value):
        self.old_data[type][index] = value

    def value_change_col_table_color_config_col(self, type, index, value):
        self.col_e[type][index] = value
