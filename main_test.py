import sys
import time
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QMovie
from Pages.tinh_mau import TinhAndMauPage


class LoadingScreen(QWidget):
    def __init__(self, movie_path):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.movie = QMovie(movie_path)
        self.movie_label = QLabel(self)
        self.movie_label.setMovie(self.movie)
        layout = QVBoxLayout()
        layout.addWidget(self.movie_label)
        self.setLayout(layout)
        self.setFixedSize(300, 200)
        self.center()

    def start(self):
        self.movie.start()

    def stop(self):
        self.movie.stop()

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class HeavyTaskThread(QThread):
    task_completed = Signal()

    def run(self):
        # Simulate a heavy task
        time.sleep(5)  # Replace with actual heavy task
        self.task_completed.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Button to start a heavy task
        self.button = QPushButton("Start Heavy Task", self)
        self.button.clicked.connect(self.start_heavy_task)
        self.layout.addWidget(self.button)

        # Placeholder for results
        self.result_label = QLabel("Result will be shown here", self)
        self.layout.addWidget(self.result_label)

        # Loading screen
        self.loading_screen = LoadingScreen("C:/data/1/image/loading.gif")

    def start_heavy_task(self):
        self.show_loading_screen()

        # Create and start a thread to perform the heavy task
        self.thread = HeavyTaskThread()
        self.thread.task_completed.connect(self.on_task_completed)
        self.thread.start()

    def show_loading_screen(self):
        self.loading_screen.show()
        self.loading_screen.start()

    def hide_loading_screen(self):
        self.loading_screen.stop()
        self.loading_screen.hide()

    def on_task_completed(self):
        self.hide_loading_screen()
        page = TinhAndMauPage()
        page.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
