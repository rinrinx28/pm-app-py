from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt


class LoadingScreen(QWidget):
    def __init__(self, movie_path):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2  # Canh giữa theo chiều ngang
        y = (screen_geometry.height() - self.height()) // 2  # Canh giữa theo chiều dọc
        self.move(x, y)

        self.movie = QMovie(movie_path)
        self.movie_label = QLabel(self)
        self.movie_label.setMovie(self.movie)

        self.layout.addWidget(self.movie_label)

    def start(self):
        self.movie.start()

    def stop(self):
        self.movie.stop()
