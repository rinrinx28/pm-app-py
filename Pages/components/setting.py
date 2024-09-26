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
from Controller.handler import updateColorInsert, enableTables
from Pages.components.stylesheet import (
    css_button_cancel,
    css_button_submit,
    css_input,
    css_lable,
    SendMessage,
    Note,
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
        tab_widget.addTab(self.create_tab_main_setting(), "Cài Đặt")
        tab_widget.addTab(self.create_tab_2_setting_bm(), "Tùy Chọn Bảng Màu")
        tab_widget.addTab(self.create_tab_3_setting_col_d_bm(), "Tùy Chọn Thống Kê")

        # Add the QTabWidget to the main layout
        dialog_main_layout.addWidget(tab_widget)

        # Create custom buttons
        button_layout = QHBoxLayout()  # Layout for the buttons

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

        # Add buttons to the button layout
        horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        button_layout.addItem(horizontalSpacer)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        dialog_main_layout.addLayout(button_layout)

        # Set the main layout as the dialog's layout
        self.setLayout(dialog_main_layout)

    def create_tab_main_setting(self):
        tab = QWidget()
        layout_tab = QVBoxLayout(tab)

        main = QWidget()
        dialog_main_layout = QHBoxLayout(main)

        # / Create Layout
        layout_w = QWidget()
        layout = QGridLayout(layout_w)
        layout.setSpacing(2)
        dialog_main_layout.addWidget(layout_w)
        layout_w.setStyleSheet(
            """
            QWidget {
                border: 1px solid #999;
            }
            """
        )

        # / Create Second Layout
        layout_w_2 = QWidget()
        layout_2 = QGridLayout(layout_w_2)
        layout_2.setSpacing(2)
        dialog_main_layout.addWidget(layout_w_2)
        layout_w_2.setStyleSheet(
            """
            QWidget {
                border: 1px solid #999;
            }
            """
        )

        # / Setting Color Table Count
        setting_color_count_w = QWidget()
        setting_color_count_l = QGridLayout(setting_color_count_w)

        setting_color_count_label = QLabel("Báo Màu Bảng Tính")
        setting_color_count_label.setStyleSheet(css_lable)

        setting_color_count_edit_fisrt = QSpinBox()
        setting_color_count_edit_fisrt.setMinimum(0)
        setting_color_count_edit_fisrt.setMaximum(120)
        setting_color_count_edit_fisrt.setStyleSheet(css_input)
        setting_color_count_edit_fisrt.setValue(self.old_data["count"][0])

        setting_color_count_edit_second = QSpinBox()
        setting_color_count_edit_second.setMinimum(0)
        setting_color_count_edit_second.setMaximum(120)
        setting_color_count_edit_second.setStyleSheet(css_input)
        setting_color_count_edit_second.setValue(self.old_data["count"][1])

        setting_color_count_l.addWidget(setting_color_count_edit_fisrt, 0, 0)
        setting_color_count_l.addWidget(setting_color_count_edit_second, 0, 1)

        layout.addWidget(setting_color_count_label, 0, 0)
        layout.addWidget(setting_color_count_w, 1, 0)

        # / Setting Color Table Color
        setting_color_color_w = QWidget()
        setting_color_color_l = QGridLayout(setting_color_color_w)

        setting_color_color_label = QLabel("Báo Màu BM1")
        setting_color_color_label.setStyleSheet(css_lable)

        setting_color_color_edit_fisrt = QSpinBox()
        setting_color_color_edit_fisrt.setDisabled(not self.buttons[0])
        setting_color_color_edit_fisrt.setMinimum(0)
        setting_color_color_edit_fisrt.setMaximum(120)
        setting_color_color_edit_fisrt.setStyleSheet(css_input)
        setting_color_color_edit_fisrt.setValue(self.old_data["color"][0])

        setting_color_color_edit_second = QSpinBox()
        setting_color_color_edit_second.setDisabled(not self.buttons[0])
        setting_color_color_edit_second.setMinimum(0)
        setting_color_color_edit_second.setMaximum(120)
        setting_color_color_edit_second.setStyleSheet(css_input)
        setting_color_color_edit_second.setValue(self.old_data["color"][1])

        setting_color_color_l.addWidget(setting_color_color_edit_fisrt, 0, 0)
        setting_color_color_l.addWidget(setting_color_color_edit_second, 0, 1)

        layout.addWidget(setting_color_color_label, 2, 0)
        layout.addWidget(setting_color_color_w, 3, 0)

        # / Setting Thong Ke D B Tinh
        setting_count_d_label = QLabel("Thông Kê D M1")
        setting_count_d_label.setStyleSheet(css_lable)

        setting_count_d_w = QWidget()
        setting_count_d_l = QGridLayout(setting_count_d_w)

        setting_count_d_edit_fisrt = QSpinBox()
        setting_count_d_edit_fisrt.setMinimum(2)
        setting_count_d_edit_fisrt.setMaximum(120)
        setting_count_d_edit_fisrt.setStyleSheet(css_input)
        setting_count_d_edit_fisrt.setValue(self.col_e["col_e"][0])

        setting_count_d_edit_second = QSpinBox()
        setting_count_d_edit_second.setMinimum(2)
        setting_count_d_edit_second.setMaximum(120)
        setting_count_d_edit_second.setStyleSheet(css_input)
        setting_count_d_edit_second.setValue(self.col_e["col_e"][1])

        setting_count_d_l.addWidget(setting_count_d_edit_fisrt, 0, 0)
        setting_count_d_l.addWidget(setting_count_d_edit_second, 0, 1)

        layout.addWidget(setting_count_d_label, 2, 1)
        layout.addWidget(setting_count_d_w, 3, 1)

        # / Setting Buttons Notice M2
        setting_color_color_w_m2 = QWidget()
        setting_color_color_l_m2 = QGridLayout(setting_color_color_w_m2)

        setting_color_color_label_m2 = QLabel("Báo Màu BM2")
        setting_color_color_label_m2.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m2 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m2.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m2.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m2.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m2.setValue(self.old_data["colorM2"][0])

        setting_buttons_notice_edit_second_m2 = QSpinBox()
        setting_buttons_notice_edit_second_m2.setMinimum(0)
        setting_buttons_notice_edit_second_m2.setMaximum(120)
        setting_buttons_notice_edit_second_m2.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m2.setValue(self.old_data["colorM2"][1])

        setting_color_color_l_m2.addWidget(setting_buttons_notice_edit_fisrt_m2, 0, 0)
        setting_color_color_l_m2.addWidget(setting_buttons_notice_edit_second_m2, 0, 1)

        layout.addWidget(setting_color_color_label_m2, 4, 0)
        layout.addWidget(setting_color_color_w_m2, 5, 0)

        # / Setting Thong Ke D M1
        setting_count_d_label_m2 = QLabel("Thông Kê D M2")
        setting_count_d_label_m2.setStyleSheet(css_lable)

        setting_count_d_w_m2 = QWidget()
        setting_count_d_l_m2 = QGridLayout(setting_count_d_w_m2)

        setting_count_d_edit_fisrt_m2 = QSpinBox()
        setting_count_d_edit_fisrt_m2.setMinimum(2)
        setting_count_d_edit_fisrt_m2.setMaximum(120)
        setting_count_d_edit_fisrt_m2.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m2.setValue(self.col_e["col_e2"][0])

        setting_count_d_edit_second_m2 = QSpinBox()
        setting_count_d_edit_second_m2.setMinimum(2)
        setting_count_d_edit_second_m2.setMaximum(120)
        setting_count_d_edit_second_m2.setStyleSheet(css_input)
        setting_count_d_edit_second_m2.setValue(self.col_e["col_e2"][1])

        setting_count_d_l_m2.addWidget(setting_count_d_edit_fisrt_m2, 0, 0)
        setting_count_d_l_m2.addWidget(setting_count_d_edit_second_m2, 0, 1)

        layout.addWidget(setting_count_d_label_m2, 4, 1)
        layout.addWidget(setting_count_d_w_m2, 5, 1)

        # / Setting Color Table Color M3
        setting_color_color_w_m3 = QWidget()
        setting_color_color_l_m3 = QGridLayout(setting_color_color_w_m3)

        setting_color_color_label_m3 = QLabel("Báo Màu BM3")
        setting_color_color_label_m3.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m3 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m3.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m3.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m3.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m3.setValue(self.old_data["colorM3"][0])

        setting_buttons_notice_edit_second_m3 = QSpinBox()
        setting_buttons_notice_edit_second_m3.setMinimum(0)
        setting_buttons_notice_edit_second_m3.setMaximum(120)
        setting_buttons_notice_edit_second_m3.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m3.setValue(self.old_data["colorM3"][1])

        setting_color_color_l_m3.addWidget(setting_buttons_notice_edit_fisrt_m3, 0, 0)
        setting_color_color_l_m3.addWidget(setting_buttons_notice_edit_second_m3, 0, 1)

        layout.addWidget(setting_color_color_label_m3, 6, 0)
        layout.addWidget(setting_color_color_w_m3, 7, 0)

        # / Setting Thong Ke D M2=
        setting_count_d_label_m3 = QLabel("Thông Kê D M3")
        setting_count_d_label_m3.setStyleSheet(css_lable)

        setting_count_d_w_m3 = QWidget()
        setting_count_d_l_m3 = QGridLayout(setting_count_d_w_m3)

        setting_count_d_edit_fisrt_m3 = QSpinBox()
        setting_count_d_edit_fisrt_m3.setMinimum(2)
        setting_count_d_edit_fisrt_m3.setMaximum(120)
        setting_count_d_edit_fisrt_m3.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m3.setValue(self.col_e["col_e3"][0])

        setting_count_d_edit_second_m3 = QSpinBox()
        setting_count_d_edit_second_m3.setMinimum(2)
        setting_count_d_edit_second_m3.setMaximum(120)
        setting_count_d_edit_second_m3.setStyleSheet(css_input)
        setting_count_d_edit_second_m3.setValue(self.col_e["col_e3"][1])

        setting_count_d_l_m3.addWidget(setting_count_d_edit_fisrt_m3, 0, 0)
        setting_count_d_l_m3.addWidget(setting_count_d_edit_second_m3, 0, 1)

        layout.addWidget(setting_count_d_label_m3, 6, 1)
        layout.addWidget(setting_count_d_w_m3, 7, 1)

        # / Setting Color Table Color M4
        setting_color_color_w_m4 = QWidget()
        setting_color_color_l_m4 = QGridLayout(setting_color_color_w_m4)

        setting_color_color_label_m4 = QLabel("Báo Màu BM4")
        setting_color_color_label_m4.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m4 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m4.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m4.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m4.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m4.setValue(self.old_data["colorM4"][0])

        setting_buttons_notice_edit_second_m4 = QSpinBox()
        setting_buttons_notice_edit_second_m4.setMinimum(0)
        setting_buttons_notice_edit_second_m4.setMaximum(120)
        setting_buttons_notice_edit_second_m4.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m4.setValue(self.old_data["colorM4"][1])

        setting_color_color_l_m4.addWidget(setting_buttons_notice_edit_fisrt_m4, 0, 0)
        setting_color_color_l_m4.addWidget(setting_buttons_notice_edit_second_m4, 0, 1)

        layout.addWidget(setting_color_color_label_m4, 8, 0)
        layout.addWidget(setting_color_color_w_m4, 9, 0)

        # / Setting Thong Ke D M4
        setting_count_d_label_m4 = QLabel("Thông Kê D M4")
        setting_count_d_label_m4.setStyleSheet(css_lable)

        setting_count_d_w_m4 = QWidget()
        setting_count_d_l_m4 = QGridLayout(setting_count_d_w_m4)

        setting_count_d_edit_fisrt_m4 = QSpinBox()
        setting_count_d_edit_fisrt_m4.setMinimum(1)
        setting_count_d_edit_fisrt_m4.setMaximum(120)
        setting_count_d_edit_fisrt_m4.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m4.setValue(self.col_e["col_e4"][0])

        setting_count_d_edit_second_m4 = QSpinBox()
        setting_count_d_edit_second_m4.setMinimum(1)
        setting_count_d_edit_second_m4.setMaximum(120)
        setting_count_d_edit_second_m4.setStyleSheet(css_input)
        setting_count_d_edit_second_m4.setValue(self.col_e["col_e4"][1])

        setting_count_d_l_m4.addWidget(setting_count_d_edit_fisrt_m4, 0, 0)
        setting_count_d_l_m4.addWidget(setting_count_d_edit_second_m4, 0, 1)

        layout.addWidget(setting_count_d_label_m4, 8, 1)
        layout.addWidget(setting_count_d_w_m4, 9, 1)

        # / Setting Color Table Color M5
        setting_color_color_w_m5 = QWidget()
        setting_color_color_l_m5 = QGridLayout(setting_color_color_w_m5)

        setting_color_color_label_m5 = QLabel("Báo Màu BM5")
        setting_color_color_label_m5.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m5 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m5.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m5.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m5.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m5.setValue(self.old_data["colorM5"][0])

        setting_buttons_notice_edit_second_m5 = QSpinBox()
        setting_buttons_notice_edit_second_m5.setMinimum(0)
        setting_buttons_notice_edit_second_m5.setMaximum(120)
        setting_buttons_notice_edit_second_m5.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m5.setValue(self.old_data["colorM5"][1])

        setting_color_color_l_m5.addWidget(setting_buttons_notice_edit_fisrt_m5, 0, 0)
        setting_color_color_l_m5.addWidget(setting_buttons_notice_edit_second_m5, 0, 1)

        layout.addWidget(setting_color_color_label_m5, 10, 0)
        layout.addWidget(setting_color_color_w_m5, 11, 0)

        # / Setting Thong Ke D M5
        setting_count_d_label_m5 = QLabel("Thông Kê D M5")
        setting_count_d_label_m5.setStyleSheet(css_lable)

        setting_count_d_w_m5 = QWidget()
        setting_count_d_l_m5 = QGridLayout(setting_count_d_w_m5)

        setting_count_d_edit_fisrt_m5 = QSpinBox()
        setting_count_d_edit_fisrt_m5.setMinimum(1)
        setting_count_d_edit_fisrt_m5.setMaximum(120)
        setting_count_d_edit_fisrt_m5.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m5.setValue(self.col_e["col_e5"][0])

        setting_count_d_edit_second_m5 = QSpinBox()
        setting_count_d_edit_second_m5.setMinimum(1)
        setting_count_d_edit_second_m5.setMaximum(120)
        setting_count_d_edit_second_m5.setStyleSheet(css_input)
        setting_count_d_edit_second_m5.setValue(self.col_e["col_e5"][1])

        setting_count_d_l_m5.addWidget(setting_count_d_edit_fisrt_m5, 0, 0)
        setting_count_d_l_m5.addWidget(setting_count_d_edit_second_m5, 0, 1)

        layout.addWidget(setting_count_d_label_m5, 10, 1)
        layout.addWidget(setting_count_d_w_m5, 11, 1)

        # / Setting Color Table Color M6
        setting_color_color_w_m6 = QWidget()
        setting_color_color_l_m6 = QGridLayout(setting_color_color_w_m6)

        setting_color_color_label_m6 = QLabel("Báo Màu BM6")
        setting_color_color_label_m6.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m6 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m6.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m6.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m6.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m6.setValue(self.old_data["colorM6"][0])

        setting_buttons_notice_edit_second_m6 = QSpinBox()
        setting_buttons_notice_edit_second_m6.setMinimum(0)
        setting_buttons_notice_edit_second_m6.setMaximum(120)
        setting_buttons_notice_edit_second_m6.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m6.setValue(self.old_data["colorM6"][1])

        setting_color_color_l_m6.addWidget(setting_buttons_notice_edit_fisrt_m6, 0, 0)
        setting_color_color_l_m6.addWidget(setting_buttons_notice_edit_second_m6, 0, 1)

        layout.addWidget(setting_color_color_label_m6, 12, 0)
        layout.addWidget(setting_color_color_w_m6, 13, 0)

        # / Setting Thong Ke D M6
        setting_count_d_label_m6 = QLabel("Thông Kê D M6")
        setting_count_d_label_m6.setStyleSheet(css_lable)

        setting_count_d_w_m6 = QWidget()
        setting_count_d_l_m6 = QGridLayout(setting_count_d_w_m6)

        setting_count_d_edit_fisrt_m6 = QSpinBox()
        setting_count_d_edit_fisrt_m6.setMinimum(1)
        setting_count_d_edit_fisrt_m6.setMaximum(120)
        setting_count_d_edit_fisrt_m6.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m6.setValue(self.col_e["col_e6"][0])

        setting_count_d_edit_second_m6 = QSpinBox()
        setting_count_d_edit_second_m6.setMinimum(1)
        setting_count_d_edit_second_m6.setMaximum(120)
        setting_count_d_edit_second_m6.setStyleSheet(css_input)
        setting_count_d_edit_second_m6.setValue(self.col_e["col_e6"][1])

        setting_count_d_l_m6.addWidget(setting_count_d_edit_fisrt_m6, 0, 0)
        setting_count_d_l_m6.addWidget(setting_count_d_edit_second_m6, 0, 1)

        layout.addWidget(setting_count_d_label_m6, 12, 1)
        layout.addWidget(setting_count_d_w_m6, 13, 1)

        verticalSpacer1 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout.addItem(verticalSpacer1, 14, 0, 1, 1)

        # / Setting Thong Value
        setting_thong_value_label = QLabel("Số Thông")
        setting_thong_value_label.setStyleSheet(css_lable)

        setting_thong_value_w = QWidget()
        setting_thong_value_l = QGridLayout(setting_thong_value_w)

        setting_thong_value_edit_fisrt = QSpinBox()
        setting_thong_value_edit_fisrt.setMinimum(1)
        setting_thong_value_edit_fisrt.setMaximum(420)
        setting_thong_value_edit_fisrt.setStyleSheet(css_input)
        setting_thong_value_edit_fisrt.setValue(self.col_thong["value"][0])

        setting_thong_value_edit_second = QSpinBox()
        setting_thong_value_edit_second.setMinimum(1)
        setting_thong_value_edit_second.setMaximum(420)
        setting_thong_value_edit_second.setStyleSheet(css_input)
        setting_thong_value_edit_second.setValue(self.col_thong["value"][1])

        setting_thong_value_l.addWidget(setting_thong_value_edit_fisrt, 0, 0)
        setting_thong_value_l.addWidget(setting_thong_value_edit_second, 0, 1)

        layout_2.addWidget(setting_thong_value_label, 1, 0)
        layout_2.addWidget(setting_thong_value_w, 2, 0)

        # / Setting Ngang Value
        setting_ngang_value_label = QLabel("Số Cột Ngang")
        setting_ngang_value_label.setStyleSheet(css_lable)

        setting_ngang_value_w = QWidget()
        setting_ngang_value_l = QGridLayout(setting_ngang_value_w)

        setting_ngang_value_edit_fisrt = QSpinBox()
        setting_ngang_value_edit_fisrt.setMinimum(1)
        setting_ngang_value_edit_fisrt.setMaximum(600)
        setting_ngang_value_edit_fisrt.setStyleSheet(css_input)
        setting_ngang_value_edit_fisrt.setValue(self.col_ngang["col"][0])

        setting_ngang_value_edit_second = QSpinBox()
        setting_ngang_value_edit_second.setMinimum(1)
        setting_ngang_value_edit_second.setMaximum(600)
        setting_ngang_value_edit_second.setStyleSheet(css_input)
        setting_ngang_value_edit_second.setValue(self.col_ngang["col"][1])

        setting_ngang_value_l.addWidget(setting_ngang_value_edit_fisrt, 0, 0)
        setting_ngang_value_l.addWidget(setting_ngang_value_edit_second, 0, 1)

        layout_2.addWidget(setting_ngang_value_label, 1, 1)
        layout_2.addWidget(setting_ngang_value_w, 2, 1)

        # / Setting Thong Value
        setting_max_row_label = QLabel("Tối Đa Dòng Tồn Tại")
        setting_max_row_label.setStyleSheet(css_lable)

        setting_max_row_edit_fisrt = QSpinBox()
        setting_max_row_edit_fisrt.setMinimum(1)
        setting_max_row_edit_fisrt.setMaximum(1000)
        setting_max_row_edit_fisrt.setStyleSheet(css_input)
        setting_max_row_edit_fisrt.setValue(self.maxRow["maxRow"])

        layout_2.addWidget(setting_max_row_label, 3, 0)
        layout_2.addWidget(setting_max_row_edit_fisrt, 4, 0)

        # / Setting Thong Change
        setting_thong_change_label = QLabel("Bộ Chuyển Đổi")
        setting_thong_change_label.setStyleSheet(css_lable)

        setting_thong_change_edit_fisrt = QSpinBox()
        setting_thong_change_edit_fisrt.setMinimum(0)
        setting_thong_change_edit_fisrt.setMaximum(5)
        setting_thong_change_edit_fisrt.setStyleSheet(css_input)
        setting_thong_change_edit_fisrt.setValue(self.change_data)

        layout_2.addWidget(setting_thong_change_label, 3, 1)
        layout_2.addWidget(setting_thong_change_edit_fisrt, 4, 1)

        # / Setting Color Table Color M7
        setting_color_color_w_m7 = QWidget()
        setting_color_color_l_m7 = QGridLayout(setting_color_color_w_m7)

        setting_color_color_label_m7 = QLabel("Báo Màu BM7")
        setting_color_color_label_m7.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m7 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m7.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m7.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m7.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m7.setValue(self.old_data["colorM7"][0])

        setting_buttons_notice_edit_second_m7 = QSpinBox()
        setting_buttons_notice_edit_second_m7.setMinimum(0)
        setting_buttons_notice_edit_second_m7.setMaximum(120)
        setting_buttons_notice_edit_second_m7.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m7.setValue(self.old_data["colorM7"][1])

        setting_color_color_l_m7.addWidget(setting_buttons_notice_edit_fisrt_m7, 0, 0)
        setting_color_color_l_m7.addWidget(setting_buttons_notice_edit_second_m7, 0, 1)

        layout_2.addWidget(setting_color_color_label_m7, 5, 0)
        layout_2.addWidget(setting_color_color_w_m7, 6, 0)

        # / Setting Thong Ke D M7
        setting_count_d_label_m7 = QLabel("Thông Kê D M7")
        setting_count_d_label_m7.setStyleSheet(css_lable)

        setting_count_d_w_m7 = QWidget()
        setting_count_d_l_m7 = QGridLayout(setting_count_d_w_m7)

        setting_count_d_edit_fisrt_m7 = QSpinBox()
        setting_count_d_edit_fisrt_m7.setMinimum(1)
        setting_count_d_edit_fisrt_m7.setMaximum(120)
        setting_count_d_edit_fisrt_m7.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m7.setValue(self.col_e["col_e7"][0])

        setting_count_d_edit_second_m7 = QSpinBox()
        setting_count_d_edit_second_m7.setMinimum(1)
        setting_count_d_edit_second_m7.setMaximum(120)
        setting_count_d_edit_second_m7.setStyleSheet(css_input)
        setting_count_d_edit_second_m7.setValue(self.col_e["col_e7"][1])

        setting_count_d_l_m7.addWidget(setting_count_d_edit_fisrt_m7, 0, 0)
        setting_count_d_l_m7.addWidget(setting_count_d_edit_second_m7, 0, 1)

        layout_2.addWidget(setting_count_d_label_m7, 5, 1)
        layout_2.addWidget(setting_count_d_w_m7, 6, 1)

        # / Setting Color Table Color M8
        setting_color_color_w_m8 = QWidget()
        setting_color_color_l_m8 = QGridLayout(setting_color_color_w_m8)

        setting_color_color_label_m8 = QLabel("Báo Màu BM8")
        setting_color_color_label_m8.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m8 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m8.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m8.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m8.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m8.setValue(self.old_data["colorM8"][0])

        setting_buttons_notice_edit_second_m8 = QSpinBox()
        setting_buttons_notice_edit_second_m8.setMinimum(0)
        setting_buttons_notice_edit_second_m8.setMaximum(120)
        setting_buttons_notice_edit_second_m8.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m8.setValue(self.old_data["colorM8"][1])

        setting_color_color_l_m8.addWidget(setting_buttons_notice_edit_fisrt_m8, 0, 0)
        setting_color_color_l_m8.addWidget(setting_buttons_notice_edit_second_m8, 0, 1)

        layout_2.addWidget(setting_color_color_label_m8, 7, 0)
        layout_2.addWidget(setting_color_color_w_m8, 8, 0)

        # / Setting Thong Ke D M8
        setting_count_d_label_m8 = QLabel("Thông Kê D M8")
        setting_count_d_label_m8.setStyleSheet(css_lable)

        setting_count_d_w_m8 = QWidget()
        setting_count_d_l_m8 = QGridLayout(setting_count_d_w_m8)

        setting_count_d_edit_fisrt_m8 = QSpinBox()
        setting_count_d_edit_fisrt_m8.setMinimum(1)
        setting_count_d_edit_fisrt_m8.setMaximum(120)
        setting_count_d_edit_fisrt_m8.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m8.setValue(self.col_e["col_e8"][0])

        setting_count_d_edit_second_m8 = QSpinBox()
        setting_count_d_edit_second_m8.setMinimum(1)
        setting_count_d_edit_second_m8.setMaximum(120)
        setting_count_d_edit_second_m8.setStyleSheet(css_input)
        setting_count_d_edit_second_m8.setValue(self.col_e["col_e8"][1])

        setting_count_d_l_m8.addWidget(setting_count_d_edit_fisrt_m8, 0, 0)
        setting_count_d_l_m8.addWidget(setting_count_d_edit_second_m8, 0, 1)

        layout_2.addWidget(setting_count_d_label_m8, 7, 1)
        layout_2.addWidget(setting_count_d_w_m8, 8, 1)

        # / Setting Color Table Color M9
        setting_color_color_w_m9 = QWidget()
        setting_color_color_l_m9 = QGridLayout(setting_color_color_w_m9)

        setting_color_color_label_m9 = QLabel("Báo Màu BM9")
        setting_color_color_label_m9.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m9 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m9.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m9.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m9.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m9.setValue(self.old_data["colorM9"][0])

        setting_buttons_notice_edit_second_m9 = QSpinBox()
        setting_buttons_notice_edit_second_m9.setMinimum(0)
        setting_buttons_notice_edit_second_m9.setMaximum(120)
        setting_buttons_notice_edit_second_m9.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m9.setValue(self.old_data["colorM9"][1])

        setting_color_color_l_m9.addWidget(setting_buttons_notice_edit_fisrt_m9, 0, 0)
        setting_color_color_l_m9.addWidget(setting_buttons_notice_edit_second_m9, 0, 1)

        layout_2.addWidget(setting_color_color_label_m9, 9, 0)
        layout_2.addWidget(setting_color_color_w_m9, 10, 0)

        # / Setting Thong Ke D M9
        setting_count_d_label_m9 = QLabel("Thông Kê D M9")
        setting_count_d_label_m9.setStyleSheet(css_lable)

        setting_count_d_w_m9 = QWidget()
        setting_count_d_l_m9 = QGridLayout(setting_count_d_w_m9)

        setting_count_d_edit_fisrt_m9 = QSpinBox()
        setting_count_d_edit_fisrt_m9.setMinimum(1)
        setting_count_d_edit_fisrt_m9.setMaximum(120)
        setting_count_d_edit_fisrt_m9.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m9.setValue(self.col_e["col_e9"][0])

        setting_count_d_edit_second_m9 = QSpinBox()
        setting_count_d_edit_second_m9.setMinimum(1)
        setting_count_d_edit_second_m9.setMaximum(120)
        setting_count_d_edit_second_m9.setStyleSheet(css_input)
        setting_count_d_edit_second_m9.setValue(self.col_e["col_e9"][1])

        setting_count_d_l_m9.addWidget(setting_count_d_edit_fisrt_m9, 0, 0)
        setting_count_d_l_m9.addWidget(setting_count_d_edit_second_m9, 0, 1)

        layout_2.addWidget(setting_count_d_label_m9, 9, 1)
        layout_2.addWidget(setting_count_d_w_m9, 10, 1)

        # / Setting Color Table Color M10
        setting_color_color_w_m10 = QWidget()
        setting_color_color_l_m10 = QGridLayout(setting_color_color_w_m10)

        setting_color_color_label_m10 = QLabel("Báo Màu BM10")
        setting_color_color_label_m10.setStyleSheet(css_lable)

        setting_buttons_notice_edit_fisrt_m10 = QSpinBox()
        setting_buttons_notice_edit_fisrt_m10.setMinimum(0)
        setting_buttons_notice_edit_fisrt_m10.setMaximum(120)
        setting_buttons_notice_edit_fisrt_m10.setStyleSheet(css_input)
        setting_buttons_notice_edit_fisrt_m10.setValue(self.old_data["colorM10"][0])

        setting_buttons_notice_edit_second_m10 = QSpinBox()
        setting_buttons_notice_edit_second_m10.setMinimum(0)
        setting_buttons_notice_edit_second_m10.setMaximum(120)
        setting_buttons_notice_edit_second_m10.setStyleSheet(css_input)
        setting_buttons_notice_edit_second_m10.setValue(self.old_data["colorM10"][1])

        setting_color_color_l_m10.addWidget(setting_buttons_notice_edit_fisrt_m10, 0, 0)
        setting_color_color_l_m10.addWidget(
            setting_buttons_notice_edit_second_m10, 0, 1
        )

        layout_2.addWidget(setting_color_color_label_m10, 11, 0)
        layout_2.addWidget(setting_color_color_w_m10, 12, 0)

        # / Setting Thong Ke D M10
        setting_count_d_label_m10 = QLabel("Thông Kê D M10")
        setting_count_d_label_m10.setStyleSheet(css_lable)

        setting_count_d_w_m10 = QWidget()
        setting_count_d_l_m10 = QGridLayout(setting_count_d_w_m10)

        setting_count_d_edit_fisrt_m10 = QSpinBox()
        setting_count_d_edit_fisrt_m10.setMinimum(1)
        setting_count_d_edit_fisrt_m10.setMaximum(120)
        setting_count_d_edit_fisrt_m10.setStyleSheet(css_input)
        setting_count_d_edit_fisrt_m10.setValue(self.col_e["col_e10"][0])

        setting_count_d_edit_second_m10 = QSpinBox()
        setting_count_d_edit_second_m10.setMinimum(1)
        setting_count_d_edit_second_m10.setMaximum(120)
        setting_count_d_edit_second_m10.setStyleSheet(css_input)
        setting_count_d_edit_second_m10.setValue(self.col_e["col_e10"][1])

        setting_count_d_l_m10.addWidget(setting_count_d_edit_fisrt_m10, 0, 0)
        setting_count_d_l_m10.addWidget(setting_count_d_edit_second_m10, 0, 1)

        layout_2.addWidget(setting_count_d_label_m10, 11, 1)
        layout_2.addWidget(setting_count_d_w_m10, 12, 1)

        verticalSpacer2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout_2.addItem(verticalSpacer2, 13, 0, 1, 1)

        # TODO Handler Button
        def changeColorCount():
            value1 = setting_color_count_edit_fisrt.value()
            value2 = setting_color_count_edit_second.value()
            self.old_data["count"] = [value1, value2]

        def changeColorColor():
            value1 = setting_color_color_edit_fisrt.value()
            value2 = setting_color_color_edit_second.value()
            self.old_data["color"] = [value1, value2]

        def changeThong():
            value = setting_thong_change_edit_fisrt.value()
            self.ban_info["meta"]["number"] = value
            if value != 0:
                note = Note[value - 1]
                self.note.setText(note)
            else:
                self.note.setText("")

        def changeThongValue():
            value_1 = setting_thong_value_edit_fisrt.value()
            value_2 = setting_thong_value_edit_second.value()
            self.col_thong["value"] = [value_1, value_2]

        def changeNgangValue():
            value_1 = setting_ngang_value_edit_fisrt.value()
            value_2 = setting_ngang_value_edit_second.value()
            self.col_ngang["col"] = [value_1, value_2]

        def changeColunmE():
            value1 = setting_count_d_edit_fisrt.value()
            value2 = setting_count_d_edit_second.value()
            self.col_e["col_e"] = [value1, value2]

        def changeColunmEM2():
            value1 = setting_count_d_edit_fisrt_m2.value()
            value2 = setting_count_d_edit_second_m2.value()
            self.col_e["col_e2"] = [value1, value2]

        def changeColunmEM3():
            value1 = setting_count_d_edit_fisrt_m3.value()
            value2 = setting_count_d_edit_second_m3.value()
            self.col_e["col_e3"] = [value1, value2]

        def changeColunmEM4():
            value1 = setting_count_d_edit_fisrt_m4.value()
            value2 = setting_count_d_edit_second_m4.value()
            self.col_e["col_e4"] = [value1, value2]

        def changeColunmEM5():
            value1 = setting_count_d_edit_fisrt_m5.value()
            value2 = setting_count_d_edit_second_m5.value()
            self.col_e["col_e5"] = [value1, value2]

        def changeColunmEM6():
            value1 = setting_count_d_edit_fisrt_m6.value()
            value2 = setting_count_d_edit_second_m6.value()
            self.col_e["col_e6"] = [value1, value2]

        def changeColunmEM7():
            value1 = setting_count_d_edit_fisrt_m7.value()
            value2 = setting_count_d_edit_second_m7.value()
            self.col_e["col_e7"] = [value1, value2]

        def changeColunmEM8():
            value1 = setting_count_d_edit_fisrt_m8.value()
            value2 = setting_count_d_edit_second_m8.value()
            self.col_e["col_e8"] = [value1, value2]

        def changeColunmEM9():
            value1 = setting_count_d_edit_fisrt_m9.value()
            value2 = setting_count_d_edit_second_m9.value()
            self.col_e["col_e9"] = [value1, value2]

        def changeColunmEM10():
            value1 = setting_count_d_edit_fisrt_m10.value()
            value2 = setting_count_d_edit_second_m10.value()
            self.col_e["col_e10"] = [value1, value2]

        def changeMaxRow():
            value = setting_max_row_edit_fisrt.value()
            self.maxRow["maxRow"] = value

        def changeButtonNoticeM2():
            value1 = setting_buttons_notice_edit_fisrt_m2.value()
            value2 = setting_buttons_notice_edit_second_m2.value()
            self.old_data["colorM2"] = [value1, value2]

        def changeButtonNoticeM3():
            value1 = setting_buttons_notice_edit_fisrt_m3.value()
            value2 = setting_buttons_notice_edit_second_m3.value()
            self.old_data["colorM3"] = [value1, value2]

        def changeButtonNoticeM4():
            value1 = setting_buttons_notice_edit_fisrt_m4.value()
            value2 = setting_buttons_notice_edit_second_m4.value()
            self.old_data["colorM4"] = [value1, value2]

        def changeButtonNoticeM5():
            value1 = setting_buttons_notice_edit_fisrt_m5.value()
            value2 = setting_buttons_notice_edit_second_m5.value()
            self.old_data["colorM5"] = [value1, value2]

        def changeButtonNoticeM6():
            value1 = setting_buttons_notice_edit_fisrt_m6.value()
            value2 = setting_buttons_notice_edit_second_m6.value()
            self.old_data["colorM6"] = [value1, value2]

        def changeButtonNoticeM7():
            value1 = setting_buttons_notice_edit_fisrt_m7.value()
            value2 = setting_buttons_notice_edit_second_m7.value()
            self.old_data["colorM7"] = [value1, value2]

        def changeButtonNoticeM8():
            value1 = setting_buttons_notice_edit_fisrt_m8.value()
            value2 = setting_buttons_notice_edit_second_m8.value()
            self.old_data["colorM8"] = [value1, value2]

        def changeButtonNoticeM9():
            value1 = setting_buttons_notice_edit_fisrt_m9.value()
            value2 = setting_buttons_notice_edit_second_m9.value()
            self.old_data["colorM9"] = [value1, value2]

        def changeButtonNoticeM10():
            value1 = setting_buttons_notice_edit_fisrt_m10.value()
            value2 = setting_buttons_notice_edit_second_m10.value()
            self.old_data["colorM10"] = [value1, value2]

        # / Buttons tpye 1 change (Color)
        setting_color_color_edit_fisrt.valueChanged.connect(changeColorColor)
        setting_color_color_edit_second.valueChanged.connect(changeColorColor)

        # / Buttons Color Count Change
        setting_color_count_edit_fisrt.valueChanged.connect(changeColorCount)
        setting_color_count_edit_second.valueChanged.connect(changeColorCount)

        # / Change Number
        setting_thong_change_edit_fisrt.valueChanged.connect(changeThong)

        # / Change Value of Thong and Ngang (Column)
        setting_ngang_value_edit_fisrt.valueChanged.connect(changeNgangValue)
        setting_ngang_value_edit_second.valueChanged.connect(changeNgangValue)

        setting_thong_value_edit_fisrt.valueChanged.connect(changeThongValue)
        setting_thong_value_edit_second.valueChanged.connect(changeThongValue)

        # / Change value of Column Table Color
        setting_count_d_edit_fisrt.valueChanged.connect(changeColunmE)
        setting_count_d_edit_second.valueChanged.connect(changeColunmE)

        # / Change value of Column Table M2 Color
        setting_count_d_edit_fisrt_m2.valueChanged.connect(changeColunmEM2)
        setting_count_d_edit_second_m2.valueChanged.connect(changeColunmEM2)

        # / Change value of Column Table M3 Color
        setting_count_d_edit_fisrt_m3.valueChanged.connect(changeColunmEM3)
        setting_count_d_edit_second_m3.valueChanged.connect(changeColunmEM3)

        # / Change value of Column Table M4 Color
        setting_count_d_edit_fisrt_m4.valueChanged.connect(changeColunmEM4)
        setting_count_d_edit_second_m4.valueChanged.connect(changeColunmEM4)

        # / Change value of Column Table M5 Color
        setting_count_d_edit_fisrt_m5.valueChanged.connect(changeColunmEM5)
        setting_count_d_edit_second_m5.valueChanged.connect(changeColunmEM5)

        # / Change value of Column Table M6 Color
        setting_count_d_edit_fisrt_m6.valueChanged.connect(changeColunmEM6)
        setting_count_d_edit_second_m6.valueChanged.connect(changeColunmEM6)

        # / Change value of Column Table M7 Color
        setting_count_d_edit_fisrt_m7.valueChanged.connect(changeColunmEM7)
        setting_count_d_edit_second_m7.valueChanged.connect(changeColunmEM7)

        # / Change value of Column Table M8 Color
        setting_count_d_edit_fisrt_m8.valueChanged.connect(changeColunmEM8)
        setting_count_d_edit_second_m8.valueChanged.connect(changeColunmEM8)

        # / Change value of Column Table M9 Color
        setting_count_d_edit_fisrt_m9.valueChanged.connect(changeColunmEM9)
        setting_count_d_edit_second_m9.valueChanged.connect(changeColunmEM9)

        # / Change value of Column Table M10 Color
        setting_count_d_edit_fisrt_m10.valueChanged.connect(changeColunmEM10)
        setting_count_d_edit_second_m10.valueChanged.connect(changeColunmEM10)

        # / Change MaxRow for All Table
        setting_max_row_edit_fisrt.valueChanged.connect(changeMaxRow)

        # / Buttons Type 2 change (ColorM2)
        setting_buttons_notice_edit_fisrt_m2.valueChanged.connect(changeButtonNoticeM2)
        setting_buttons_notice_edit_second_m2.valueChanged.connect(changeButtonNoticeM2)

        # / Buttons Type 2 change (ColorM3)
        setting_buttons_notice_edit_fisrt_m3.valueChanged.connect(changeButtonNoticeM3)
        setting_buttons_notice_edit_second_m3.valueChanged.connect(changeButtonNoticeM3)

        # / Buttons Type 2 change (ColorM4)
        setting_buttons_notice_edit_fisrt_m4.valueChanged.connect(changeButtonNoticeM4)
        setting_buttons_notice_edit_second_m4.valueChanged.connect(changeButtonNoticeM4)

        # / Buttons Type 2 change (ColorM5)
        setting_buttons_notice_edit_fisrt_m5.valueChanged.connect(changeButtonNoticeM5)
        setting_buttons_notice_edit_second_m5.valueChanged.connect(changeButtonNoticeM5)

        # / Buttons Type 2 change (ColorM6)
        setting_buttons_notice_edit_fisrt_m6.valueChanged.connect(changeButtonNoticeM6)
        setting_buttons_notice_edit_second_m6.valueChanged.connect(changeButtonNoticeM6)

        # / Buttons Type 2 change (ColorM7)
        setting_buttons_notice_edit_fisrt_m7.valueChanged.connect(changeButtonNoticeM7)
        setting_buttons_notice_edit_second_m7.valueChanged.connect(changeButtonNoticeM7)

        # / Buttons Type 2 change (ColorM8)
        setting_buttons_notice_edit_fisrt_m8.valueChanged.connect(changeButtonNoticeM8)
        setting_buttons_notice_edit_second_m8.valueChanged.connect(changeButtonNoticeM8)

        # / Buttons Type 2 change (ColorM9)
        setting_buttons_notice_edit_fisrt_m9.valueChanged.connect(changeButtonNoticeM9)
        setting_buttons_notice_edit_second_m9.valueChanged.connect(changeButtonNoticeM9)

        # / Buttons Type 2 change (ColorM10)
        setting_buttons_notice_edit_fisrt_m10.valueChanged.connect(
            changeButtonNoticeM10
        )
        setting_buttons_notice_edit_second_m10.valueChanged.connect(
            changeButtonNoticeM10
        )
        # Add the button layout to the main layout
        layout_tab.addWidget(main)
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
            button = QPushButton(f"BM{i+1}")
            button.setStyleSheet(css_button_submit)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.clicked.connect(partial(self.handle_change_setting_col_d_bm, i))
            button_l.addWidget(button)
            i = i + 1

        # Add a vertical spacer to the layout
        verticalSpacer1 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(main)
        layout.addItem(verticalSpacer1)
        layout.addWidget(button_w)
        return tab

    def clearLayoutMain(self, layout):
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

        # Create the scrollarea
        scroll_area = QScrollArea(widget)
        scroll_area.setFixedHeight(600)
        scroll_area.setWidgetResizable(
            True
        )  # Ensure the widget inside scrolls as needed

        # Create the content widget to put inside the scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        for i in range(120):
            widget_label = QWidget()
            label_layout = QVBoxLayout(widget_label)

            label = QLabel(f"D {i + 1}/M{type + 1}")
            label.setStyleSheet("font-size: 24px;")

            spin_label = QSpinBox()
            spin_label.setMinimum(1)
            spin_label.setStyleSheet("font-size: 24px;")
            spin_label.setValue(info_table["col_d"][i])
            spin_label.valueChanged.connect(partial(self.change_table_col_d, type, i))

            label_layout.addWidget(label)
            label_layout.addWidget(spin_label)

            content_layout.addWidget(widget_label)

        scroll_area.setWidget(content_widget)

        layout.addWidget(scroll_area)

        if self.current_widget:
            self.clearLayoutMain(self.main_layout)

        self.current_widget = widget
        self.main_layout.addWidget(self.current_widget)

    def change_table_col_d(self, type, index, value):
        self.ban_info["meta"]["tables"][type]["col_d"][index] = value
