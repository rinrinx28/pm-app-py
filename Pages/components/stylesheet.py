from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QMessageBox
from Pages.components.path import Path

css_button_submit = """
    QPushButton {
        padding: 10px;
        border-radius: 8px; 
        font-size: 24px;
        line-height: 32px;
        font-weight: 600; 
        color: #ffffff; 
        background-color: #1D4ED8;
    } 
    QPushButton:hover {
        background-color: #1E40AF; 
    }
"""


css_button_cancel = """
    QPushButton {
        padding: 10px;
        border-radius: 8px; 
        font-size: 24px;
        line-height: 32px;
        font-weight: 600; 
        color: #ffffff; 
        background-color: #1D4ED8;
    } 
    QPushButton:hover {
        background-color: #1E40AF; 
    }
"""

css_button_view = """
    QPushButton {
        border-radius: 8px;
        font-size: 24px;
        line-height: 32px;
        font-weight: 600;
        background-color: rgb(178, 255, 255);
        padding: 8px;
        color: #000;
    }
"""

css_button_notice = """
    QPushButton {
        border-radius: 8px;
        font-size: 24px;
        line-height: 32px;
        font-weight: 600;
        background-color: #FFD700;
        padding: 8px;
        color: #000;
    }
"""

css_button_normal = """
    QPushButton {
        border-radius: 8px;
        font-size: 24px;
        line-height: 32px;
        font-weight: 600;
        background-color: #D3D3D3;
        padding: 8px;
        color: #000;
    }
"""

# TODO Css From

css_lable = """
    padding: 10px;
    font-size: 24px;
    line-height: 32px;
    font-weight: 600; 
"""

css_input = """
    width: 100%;
    border-radius: 4px; 
    border-width: 1px; 
    border-color: #E5E7EB;
    font-size: 24px;
    line-height: 32px;
    font-weight: 600; 
    color: #000;
    background-color: #F9FAFB; 
    padding: 10px;
"""

# TODO CSS Analysis Color D
css_analysis_color = """
    background-color: red;
    border-radius: 8px;
    padding: 10px;
    font-size: 24px;
    line-height: 32px;
    font-weight: 600; 
    color: white;
"""

# TODO Css Color Thong
css_title = """
    color: rgb(239, 1, 7);
    font-size: 24px;
    line-height: 32px;
    font-weight: 600; 
"""

css_customs_table = """
    QLabel {
        border: 2px solid black;
        background-color: #FFFFFF;
        color: #000;
        font-size: 24px;
        line-height: 32px;
        font-weight: 600;
    }
"""

css_button_checkbox = """
    QCheckBox {
        font-size: 24px;
        line-height: 32px;
        font-weight: 600; 
        spacing: 5px;
    }
"""

css_table_header = """
    QTableView {
        gridline-color: black;
    }
    QTableView::item:selected {
        background-color: #FEBE10;
        color: black;
    }
"""


# TODO Font configuration
def Font():
    font = QFont()
    font.setWeight(QFont.DemiBold)
    font.setPointSize(24)
    return font


# TODO Config Note
Note = [
    "SĐY: 0 1 2 3 4; SCĐ: 5=0; 6=1; 7=2; 8=3; 9=4",
    "SĐY: 0 2 4 6 8; SCĐ: 1=0, 3=2, 5=4, 7=6, 9=8",
    "SĐY: 1 3 5 7 9; SCĐ: 2=1, 4=3, 6=5, 8=7, 0=9",
    "SĐY: 5 6 7 8 9; SCĐ: 0=5, 1=7, 2=8, 3=9, 4=6",
    "SĐY: 1 2 3 4 0; SCĐ: 5=1, 6=2, 7=3, 8=4, 9=0",
    "SĐY: 4 3 2 1 0; SCĐ: 5=3, 6=4, 7=0, 8=1, 9=2",
    "SĐY: 9 8 7 6 5; SCĐ: 0=7; 1=8; 2=6; 3=5, 4=9",
    "SĐY: 9 3 2 1 0; SCĐ: 4=2; 5=3; 6=9; 7=0; 8=1",
    "SĐY: 7 8 9 0 1; SCĐ: 2=0; 3=1; 4=7; 5=8; 6=9",
    "SĐY: 2 3 4 6 7; SCĐ: 0=2; 1=3; 5=4; 8=7; 9=6",
    "SĐY: 0 1 2 3 4 5 6 7 8 9",
]


def SendMessage(msg):
    icon = Path().path_logo()
    message = QMessageBox()
    message.setWindowTitle("Thông Báo")
    message.setText(msg)
    message.setFont(Font())
    message.setWindowIcon(QIcon(icon))
    message.setIcon(QMessageBox.Icon.Information)
    message.exec()
