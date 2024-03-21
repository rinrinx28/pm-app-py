from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QMessageBox
from Pages.components.path import Path

css_button_submit = """
    QPushButton {
        padding: 10px;
        border-radius: 8px; 
        font-size: 24px;
        font-weight: bold; 
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
        border-width: 1px; 
        border-color: #E5E7EB; 
        font-size: 24px;
        font-weight: bold; 
        color: #111827; 
        background-color: #ffffff;
    }
    QPushButton:hover {
        color: #1D4ED8; 
        background-color: #F3F4F6; 
    }
"""

css_button_view = """
    QPushButton {
        border-radius: 8px; 
        border-width: 1px; 
        border-color: #E5E7EB; 
        font-size: 24px;
        font-weight: bold;
        background-color: #F0F8FF;
    }
"""

css_button_notice = """
    QPushButton {
        border-radius: 8px; 
        border-width: 1px; 
        border-color: #E5E7EB; 
        font-size: 24px;
        font-weight: bold;
        background-color: #FFD700;
    }
"""

css_button_normal = """
    QPushButton {
        border-radius: 8px; 
        border-width: 1px; 
        border-color: #E5E7EB; 
        font-size: 24px;
        font-weight: bold;
        background-color: #ffffff;
    }
"""

# TODO Css From

css_lable = """
    padding: 10px;
    font-size: 24px;
    font-weight: bold; 
    color: #111827;
"""

css_input = """
    padding: 10px;
    border-radius: 8px; 
    border-width: 1px; 
    border-color: #E5E7EB;
    font-size: 24px;
    color: #111827; 
    background-color: #F9FAFB; 
"""

# TODO Font configuration
def Font():
    font = QFont()
    font.setWeight(QFont.DemiBold)
    font.setPointSize(24)
    return font

# TODO Config Note
Note = [
    '0 1 2 3 4: Đứng yên >> chuyển: 5=0, 6=1, 7=2, 8=3, 9=4',
    '0 2 4 6 8: Đứng yên >> chuyển: 1=0, 3=2, 5=4, 7=6, 9=8',
    '1 3 5 7 9: Đứng yên >> chuyển: 2=1, 4=3, 6=5, 8=7, 0=9',
    '3 4 5 6 7: Đứng yên >> chuyển: 0=3, 1=4, 2=5, 8=6, 9=7',
    '1 2 3 4 6: Đứng yên >> chuyển: 0=1, 5=2, 7=3, 8=4, 9=6'
]

def SendMessage(msg):
    icon = Path().path_logo()
    message = QMessageBox()
    message.setWindowTitle('Thông Báo')
    message.setText(msg)
    message.setFont(Font())
    message.setWindowIcon(QIcon(icon))
    message.setIcon(QMessageBox.Icon.Information)
    message.exec()
