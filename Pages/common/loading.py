from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt


class LoadingScreen(QWidget):
    def __init__(self, movie_path):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.movie = QMovie(movie_path)
        self.movie_label = QLabel(self)
        self.movie_label.setMovie(self.movie)

        self.layout.addWidget(self.movie_label)

    def start(self):
        self.movie.start()

    def stop(self):
        self.movie.stop()
