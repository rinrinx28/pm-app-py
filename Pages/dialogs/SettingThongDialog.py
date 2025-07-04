# Pages/dialogs/setting-thong-dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QIcon
import os
import json

from Pages.components.stylesheet import css_button_submit, css_button_cancel, css_input, css_lable, SendMessage

class SettingThongDialog(QDialog):
    def __init__(self, parent, icon_path: str, config_dir: str, update_excel: callable, toggle_editer: callable):
        super().__init__(parent)
        self.setWindowTitle("Cài Đặt E & H")
        self.setWindowIcon(QIcon(icon_path))

        self.config_dir = config_dir
        self.steps_path = os.path.join(config_dir, "steps.json")
        self.mods_path = os.path.join(config_dir, "modifications.json")

        self.steps_data = self.load_json(self.steps_path)
        self.mods_data = self.load_json(self.mods_path)

        self.update_excel = update_excel
        self.toggle_editer = toggle_editer
        self.initUi()

    def load_json(self, path: str) -> list[list[int]]:
        try:
            with open(path, "r") as file:
                return json.load(file)
        except Exception:
            return [[0, 0, 0]]

    def initUi(self):
        layout = QVBoxLayout(self)
        self.resize(600, 400)  # 👈 Dialog size

        self.stepsTable = self.createTable("H", self.steps_data)
        self.modsTable = self.createTable("E", self.mods_data)

        layout.addWidget(self.stepsTable["label"])
        layout.addWidget(self.stepsTable["table"])
        layout.addWidget(self.modsTable["label"])
        layout.addWidget(self.modsTable["table"])

        self.stepsTable["table"].horizontalHeader().setDefaultSectionSize(100)
        self.modsTable["table"].horizontalHeader().setDefaultSectionSize(100)
        self.stepsTable["table"].verticalHeader().setDefaultSectionSize(40)
        self.modsTable["table"].verticalHeader().setDefaultSectionSize(40)

        # Buttons
        button_layout = QHBoxLayout()
        saveBtn = QPushButton("Lưu")
        saveBtn.setStyleSheet(css_button_submit)
        saveBtn.clicked.connect(self.saveChanges)

        cancelBtn = QPushButton("Thoát")
        cancelBtn.setStyleSheet(css_button_cancel)
        cancelBtn.clicked.connect(self.reject)

        button_layout.addWidget(saveBtn)
        button_layout.addWidget(cancelBtn)
        layout.addLayout(button_layout)

    def createTable(self, title: str, data: list[list[int]]):
        label = QLabel(title)
        label.setStyleSheet(css_lable)
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(data[0]) if data else 0)

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(0x0004 | 0x0080)  # center both ways
                table.setItem(i, j, item)
        return {"label": label, "table": table}

    def extractData(self, table: QTableWidget) -> list[list[int]]:
        data = []
        for i in range(table.rowCount()):
            row = []
            for j in range(table.columnCount()):
                item = table.item(i, j)
                try:
                    row.append(int(item.text()) if item else 0)
                except ValueError:
                    row.append(0)
            data.append(row)
        return data

    def saveChanges(self):
        steps = self.extractData(self.stepsTable["table"])
        mods = self.extractData(self.modsTable["table"])

        try:
            with open(self.steps_path, "w") as f:
                json.dump(steps, f, indent=2)
            with open(self.mods_path, "w") as f:
                json.dump(mods, f, indent=2)
            SendMessage("Đã lưu cập nhật E & H.")
            self.toggle_editer(True)
            self.update_excel()
            self.accept()
        except Exception as e:
            SendMessage(f"Lỗi khi lưu: {e}")
