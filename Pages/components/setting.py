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
from PySide6.QtGui import QGuiApplication
from Controller.handler import (
    updateColorInsert,
    enableTables,
    save_setting_tables,
    convert_string_format,
    convert_string_format_type,async_setting_number_pm,async_setting_range_thong
)
from Pages.components.stylesheet import (
    css_button_submit,
    css_input,
    SendMessage,
    css_title,
)

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

        self.name = convert_string_format(self.col_thong["name"])
        self.name_type = convert_string_format_type(self.col_thong["name"])
        icon = self.path.path_logo()
        self.current_widget = None

        # / Create Dialog Windows
        self.setWindowTitle("Cài đặt bảng")
        self.setWindowIcon(QIcon(icon))
        self.showFullScreen()

        # Create main layout
        dialog_main_layout = QVBoxLayout()

        label = QLabel(f"Cài đặt - {self.name}")
        label.setStyleSheet(css_title)
        dialog_main_layout.addWidget(label)

        # Create a QTabWidget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                font-size: 24px;  /* Set font size */
            }
        """)
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
                padding: 2px 12px 2px 12px;
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

        cancel_button = QPushButton("Thoát")  # Custom Cancel button
        cancel_button.setStyleSheet(
            """
            QPushButton {
                border-radius: 8px;
                font-size: 24px;
                font-weight: 600;
                color: #fff;
                background-color: #EE4B2B;
                padding: 2px 12px 2px 12px;
            }
            QPushButton:hover {
                color: #EE4B2B;
                background-color: #fff;
            }

        """
        )
        cancel_button.setFixedWidth(150)
        cancel_button.setCursor(QCursor(Qt.PointingHandCursor))
        cancel_button.clicked.connect(self.reject)  # Connect to reject action

        async_setting_number = QPushButton("Đặt bộ chuyển đổi của Bộ")  # Đồng bộ dữ liệu cài đặt Bộ chuyển đổi cho tập
        async_setting_number.setStyleSheet(
            """
            QPushButton {
                border-radius: 8px;
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                background-color: #1D4ED8;
                padding: 2px 12px 2px 12px;
            }
            QPushButton:hover {
                color: #1D4ED8;
                background-color: #F3F4F6;
            }

        """
        )
        # async_setting_number.setFixedWidth(150)
        async_setting_number.setCursor(QCursor(Qt.PointingHandCursor))
        async_setting_number.clicked.connect(self.async_setting_number_all)

        async_setting_thong = QPushButton("Đồng bộ Số Thông của Tập")  # Đồng bộ dữ liệu cài đặt Bộ chuyển đổi cho tập
        async_setting_thong.setStyleSheet(
            """
            QPushButton {
                border-radius: 8px;
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                background-color: #1D4ED8;
                padding: 2px 12px 2px 12px;
            }
            QPushButton:hover {
                color: #1D4ED8;
                background-color: #F3F4F6;
            }

        """
        )
        # async_setting_thong.setFixedWidth(150)
        async_setting_thong.setCursor(QCursor(Qt.PointingHandCursor))
        async_setting_thong.clicked.connect(self.async_setting_thong_all)

        save_button = QPushButton("Đồng bộ cài đặt của Tập")  # Custom save button
        save_button.setStyleSheet(
            """
            QPushButton {
                border-radius: 8px;
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                background-color: #1D4ED8;
                padding: 2px 12px 2px 12px;
            }
            QPushButton:hover {
                background-color: #1E40AF;
            }
        """
        )
        # save_button.setFixedWidth(200)
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
        button_layout.addWidget(save_button)
        button_layout.addWidget(async_setting_thong)
        button_layout.addWidget(async_setting_number)
        button_layout.addWidget(cancel_button)
        return button_widget

    def async_setting_number_all(self):
        msg = async_setting_number_pm({
            "name": self.col_thong["name"]
        })
        return SendMessage(msg)

    def async_setting_thong_all(self):
        msg = async_setting_range_thong({
            "name": self.col_thong["name"],
            "thong": {
                        "value": self.ban_info["thong"]["value"],
                    },
        })
        return SendMessage(msg)

    def save_setting_all_app(self, data):
        msg = save_setting_tables(data)
        return SendMessage(f"{msg} {self.name_type}")

    def create_tab_main_setting(self):
        tab = QWidget()
        layout_tab = QVBoxLayout(tab)

        group_spin_box = []

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
        s_table_count_color_spinbox_1.setStyleSheet("font-size: 24px;border: 0px;")
        s_table_count_color_spinbox_1.setValue(self.old_data["count"][0])
        s_table_count_color_spinbox_1.setDisabled(True)
        group_spin_box.append(s_table_count_color_spinbox_1)

        s_table_count_color_spinbox_2 = QSpinBox()
        s_table_count_color_l.addWidget(s_table_count_color_spinbox_2, 1, 1)
        s_table_count_color_spinbox_2.setMinimum(0)
        s_table_count_color_spinbox_2.setMaximum(120)
        s_table_count_color_spinbox_2.setStyleSheet("font-size: 24px;border: 0px;")
        s_table_count_color_spinbox_2.setValue(self.old_data["count"][1])
        s_table_count_color_spinbox_2.setDisabled(True)
        group_spin_box.append(s_table_count_color_spinbox_2)

        # / Setting Values Thong Config
        s_values_thong_w = QWidget()
        s_values_thong_w.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_values_thong_w)
        s_values_thong_l = QGridLayout(s_values_thong_w)

        # / Setting Values Thong Config > Lable | SpinBox
        s_values_thong_lable = QLabel("Khoảng Thông")
        s_values_thong_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_values_thong_l.addWidget(s_values_thong_lable, 0, 0)

        s_values_thong_spinbox_1 = QSpinBox()
        s_values_thong_l.addWidget(s_values_thong_spinbox_1, 1, 0)
        s_values_thong_spinbox_1.setMinimum(1)
        s_values_thong_spinbox_1.setMaximum(600)
        s_values_thong_spinbox_1.setStyleSheet("font-size: 24px;border: 0px;")
        s_values_thong_spinbox_1.setValue(self.col_thong["value"][0])
        s_values_thong_spinbox_1.setDisabled(True)
        group_spin_box.append(s_values_thong_spinbox_1)

        s_values_thong_spinbox_2 = QSpinBox()
        s_values_thong_l.addWidget(s_values_thong_spinbox_2, 1, 1)
        s_values_thong_spinbox_2.setMinimum(1)
        s_values_thong_spinbox_2.setMaximum(600)
        s_values_thong_spinbox_2.setStyleSheet("font-size: 24px;border: 0px;")
        s_values_thong_spinbox_2.setValue(self.col_thong["value"][1])
        s_values_thong_spinbox_2.setDisabled(True)
        group_spin_box.append(s_values_thong_spinbox_2)

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
        s_values_ngang_spinbox_1.setStyleSheet("font-size: 24px;border: 0px;")
        s_values_ngang_spinbox_1.setValue(self.col_ngang["col"][0])
        s_values_ngang_spinbox_1.setDisabled(True)
        group_spin_box.append(s_values_ngang_spinbox_1)

        s_values_ngang_spinbox_2 = QSpinBox()
        s_values_ngang_l.addWidget(s_values_ngang_spinbox_2, 1, 1)
        s_values_ngang_spinbox_2.setMinimum(0)
        s_values_ngang_spinbox_2.setMaximum(120)
        s_values_ngang_spinbox_2.setStyleSheet("font-size: 24px;border: 0px;")
        s_values_ngang_spinbox_2.setValue(self.col_ngang["col"][1])
        s_values_ngang_spinbox_2.setDisabled(True)
        group_spin_box.append(s_values_ngang_spinbox_2)

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
        s_max_row_spinbox_1.setStyleSheet("font-size: 24px;border: 0px;")
        s_max_row_spinbox_1.setValue(self.maxRow["maxRow"])
        s_max_row_spinbox_1.setDisabled(True)
        group_spin_box.append(s_max_row_spinbox_1)

        # / Setting Value Change
        s_value_change_w = QWidget()
        s_value_change_w.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_value_change_w)
        s_value_change_l = QGridLayout(s_value_change_w)

        # / Setting Max row > Lable | SpinBox
        s_value_change_lable = QLabel("Cơ")
        s_value_change_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_value_change_l.addWidget(s_value_change_lable, 0, 0)

        s_value_change_spinbox_1 = QSpinBox()
        s_value_change_l.addWidget(s_value_change_spinbox_1, 1, 0)
        s_value_change_spinbox_1.setMinimum(0)
        s_value_change_spinbox_1.setMaximum(10)
        s_value_change_spinbox_1.setStyleSheet("font-size: 24px;border: 0px;")
        s_value_change_spinbox_1.setValue(self.ban_info["meta"]["number"])
        s_value_change_spinbox_1.setDisabled(True)
        group_spin_box.append(s_value_change_spinbox_1)

        # / Setting Size table
        s_size_table = QWidget()
        s_size_table.setStyleSheet("border: 1px solid #999;")
        layout_tab.addWidget(s_size_table)
        s_size_table_l = QGridLayout(s_size_table)

        # / Setting Max row > Lable | SpinBox
        s_size_table_lable = QLabel("Kích Thước Chữ")
        s_size_table_lable.setStyleSheet("border: 0px;font-size: 24px;")
        s_size_table_l.addWidget(s_size_table_lable, 0, 0)

        s_size_table_spinbox_1 = QSpinBox()
        s_size_table_l.addWidget(s_size_table_spinbox_1, 1, 0)
        s_size_table_spinbox_1.setMinimum(12)
        s_size_table_spinbox_1.setStyleSheet("font-size: 24px;border: 0px;")
        s_size_table_spinbox_1.setValue(self.ban_info.get('size', 28))
        s_size_table_spinbox_1.setDisabled(True)
        group_spin_box.append(s_size_table_spinbox_1)

        # / Setting Turn Off / On
        turn_setting = QCheckBox("Tắt Tùy Chỉnh")
        turn_setting.setStyleSheet("border: 0px; font-size: 24px;")
        layout_tab.addWidget(turn_setting)

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

        def size_change(value):
            self.ban_info['size'] = value

        def turn_setting_e():
            ischecked = turn_setting.isChecked()
            if ischecked:
                turn_setting.setText('Bật Tùy Chỉnh')
                for spin_box in group_spin_box:
                    spin_box.setDisabled(False)
            else:
                turn_setting.setText('Tắt Tùy Chỉnh')
                for spin_box in group_spin_box:
                    spin_box.setDisabled(True)

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

        # / Size change Event Change
        s_size_table_spinbox_1.valueChanged.connect(size_change)

        # / Turn off / on setting
        turn_setting.checkStateChanged.connect(turn_setting_e)

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

        # button = self.showButton()
        # layout.addWidget(button, 6,1)

        # horizontalSpacer = QSpacerItem(
        #     40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        # )

        # Add a vertical spacer to the layout
        verticalSpacer1 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        # layout.addItem(horizontalSpacer, 6, 0, 1, 1)
        layout.addItem(verticalSpacer1, 7, 0, 1, 1)
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
            button = QPushButton(f"m{i + 1}")
            button.setStyleSheet(css_button_submit)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.clicked.connect(partial(self.handle_change_setting_col_d_bm, i))
            button_l.addWidget(button)
            i = i + 1

        layout.addWidget(main)
        layout.addWidget(button_w)
        # button = self.showButton()
        # layout.addWidget(button)
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
            "size": self.ban_info['size']
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
        info_table['btn_notice'] = info_table['btn_notice'] if "btn_notice" in info_table else [[8, 36] for _ in range(120)]
        info_table['number_btn_notice'] = info_table['number_btn_notice'] if "number_btn_notice" in info_table else 10
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

        # Thêm các widget vào lưới 4 cột
        for i in range(120):
            widget_label = QWidget()
            widget_label.setStyleSheet("border: 1px solid #999;")
            label_layout = QVBoxLayout(widget_label)

            label = QLabel(f"d {i + 1}/m{type + 1}")
            label.setStyleSheet("font-size: 24px;border: 0px;")

            spin_label = QSpinBox()
            spin_label.setDisabled(True)
            spin_label.setMinimum(1)
            spin_label.setStyleSheet("font-size: 24px;border: 0px;")
            spin_label.setValue(info_table["col_d"][i])
            spin_label.valueChanged.connect(partial(self.change_table_col_d, type, i))
            
            # Widget btn_notice of number "d"
            # Label btn_notice
            btn_notice_label = QLabel(f'Báo màu: d {i + 1}/m{type + 1}')
            btn_notice_label.setStyleSheet("font-size: 24px;border: 0px;")
            widget_btn_notice = QWidget()
            widget_btn_notice.setStyleSheet(
                """
                    border: 0px;
                """
            )
            btn_notice_layout = QHBoxLayout(widget_btn_notice)
            spin_label_btn_notice_first = QSpinBox()
            spin_label_btn_notice_first.setDisabled(True)
            spin_label_btn_notice_first.setMinimum(1)
            spin_label_btn_notice_first.setStyleSheet("font-size: 24px;border: 0px;")
            spin_label_btn_notice_first.setValue(info_table['btn_notice'][i][0])
            spin_label_btn_notice_first.valueChanged.connect(partial(self.save_btn_notice, type, i, 0))

            spin_label_btn_notice_second = QSpinBox()
            spin_label_btn_notice_second.setDisabled(True)
            spin_label_btn_notice_second.setMinimum(1)
            spin_label_btn_notice_second.setStyleSheet("font-size: 24px;border: 0px;")
            spin_label_btn_notice_second.setValue(info_table['btn_notice'][i][1])
            spin_label_btn_notice_second.valueChanged.connect(partial(self.save_btn_notice, type, i, 1))

            btn_notice_layout.addWidget(spin_label_btn_notice_first)
            btn_notice_layout.addWidget(spin_label_btn_notice_second)

            label_layout.addWidget(label)
            label_layout.addWidget(spin_label)
            label_layout.addWidget(btn_notice_label)
            label_layout.addWidget(widget_btn_notice)

            spin_boxes.append(spin_label)
            spin_boxes.append(spin_label_btn_notice_first)
            spin_boxes.append(spin_label_btn_notice_second)

            # Thêm widget vào lưới 4 cột
            row = i // 4
            col = i % 4
            content_layout.addWidget(widget_label, row, col)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # # / Add Notice Color
        # notice = QWidget()
        # notice.setStyleSheet("border: 1px solid #999;")
        # notice_l = QVBoxLayout(notice)
        # layout.addWidget(notice) // Disable Notice Color

        # # / Lable > SpinBox
        # notice_lable = QLabel(f"Báo Màu M{type + 1}")
        # notice_lable.setStyleSheet("border: 0px;font-size:24px;")
        # notice_l.addWidget(notice_lable)

        # notice_spinBox_w = QWidget()
        # notice_spinBox_w.setStyleSheet("border: 0px;")
        # notice_spinBox_l = QHBoxLayout(notice_spinBox_w)
        # notice_l.addWidget(notice_spinBox_w)
        # notice_spinBox_1 = QSpinBox()
        # notice_spinBox_1.setMinimum(0)
        # notice_spinBox_1.setMaximum(999)
        # notice_spinBox_1.setStyleSheet("font-size: 24px;border: 0px;")
        # notice_spinBox_1.setValue(
        #     self.old_data[f'color{"M" + str(type + 1) if type != 0 else ""}'][0]
        # )
        # notice_spinBox_2 = QSpinBox()
        # notice_spinBox_2.setMinimum(0)
        # notice_spinBox_2.setMaximum(999)
        # notice_spinBox_2.setStyleSheet("font-size: 24px;border: 0px;")
        # notice_spinBox_2.setValue(
        #     self.old_data[f'color{"M" + str(type + 1) if type != 0 else ""}'][1]
        # )

        # notice_spinBox_l.addWidget(notice_spinBox_1)
        # notice_spinBox_l.addWidget(notice_spinBox_2)

        # notice_spinBox_1.setDisabled(True)
        # notice_spinBox_2.setDisabled(True)
        # spin_boxes.append(notice_spinBox_1)
        # spin_boxes.append(notice_spinBox_2)

        # / Add Config Col D
        config_col = QWidget()
        config_col.setStyleSheet("border: 1px solid #999;")
        config_col_l = QVBoxLayout(config_col)
        layout.addWidget(config_col)

        # / Lable > SpinBox
        config_col_lable = QLabel(f"Thông Kê D m{type + 1}")
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

        config_col_spinBox_1.setEnabled(False)
        config_col_spinBox_2.setEnabled(False)
        spin_boxes.append(config_col_spinBox_1)
        spin_boxes.append(config_col_spinBox_2)

        # Label number btn_notice
        number_btn_notice_col = QWidget()
        number_btn_notice_col.setStyleSheet("border: 1px solid #999;")
        number_btn_notice_col_l = QVBoxLayout(number_btn_notice_col)
        layout.addWidget(number_btn_notice_col)

        number_btn_notice_label = QLabel('Số nút màu')
        number_btn_notice_label.setStyleSheet("font-size: 24px;border: 0px;")

        spin_label_number_btn_notice = QSpinBox()
        spin_label_number_btn_notice.setEnabled(False)
        spin_label_number_btn_notice.setMinimum(1)
        spin_label_number_btn_notice.setStyleSheet("font-size: 24px;border: 0px;")
        spin_label_number_btn_notice.setValue(info_table['number_btn_notice'])
        spin_label_number_btn_notice.valueChanged.connect(partial(self.save_number_btn_notice, type))
        

        number_btn_notice_col_l.addWidget(number_btn_notice_label)
        number_btn_notice_col_l.addWidget(spin_label_number_btn_notice)

        spin_boxes.append(spin_label_number_btn_notice)
        # verticalSpacer2 = QSpacerItem(
        #     20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        # )
        # layout.addItem(verticalSpacer2)

        # Tạo nút để bật/tắt tất cả SpinBox
        turn_setting = QCheckBox("Tắt Tùy Chỉnh")
        turn_setting.setStyleSheet("border: 0px; font-size: 24px;")
        layout.addWidget(turn_setting)

        # TODO Handler Func
        # / Hàm để tắt hoặc bật tất cả SpinBox
        def toggle_all_spinboxes(checked):
            ischecked = turn_setting.isChecked()
            if ischecked:
                turn_setting.setText('Bật Tùy Chỉnh')
                for spin in spin_boxes:
                    spin.setDisabled(False)
            else:
                turn_setting.setText('Tắt Tùy Chỉnh')
                for spin in spin_boxes:
                    spin.setDisabled(True)

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

        # / Config turn_setting
        turn_setting.checkStateChanged.connect(toggle_all_spinboxes)

        if self.current_widget:
            self.clear_layout_main(self.main_layout)

        self.current_widget = widget
        self.main_layout.addWidget(self.current_widget)

    # Handler func notice
    def save_btn_notice(self, type, index,n, value):
        self.ban_info["meta"]["tables"][type]['btn_notice'][index][n] = value
    
    def save_number_btn_notice(self, type, value):
        self.ban_info["meta"]["tables"][type]['number_btn_notice'] =  value

    def change_table_col_d(self, type, index, value):
        self.ban_info["meta"]["tables"][type]["col_d"][index] = value

    def value_change_col_table_color_notice(self, type, index, value):
        self.old_data[type][index] = value

    def value_change_col_table_color_config_col(self, type, index, value):
        self.col_e[type][index] = value
