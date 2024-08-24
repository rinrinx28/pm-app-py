from PySide6.QtCore import QThread, Signal
import time


class Thread(QThread):
    task_completed = Signal()

    def run(self):
        # Simulate a heavy task
        time.sleep(3)  # Replace with actual heavy task
        self.task_completed.emit()
