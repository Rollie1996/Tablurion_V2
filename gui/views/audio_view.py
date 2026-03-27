from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class AudioView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Audio Player View"))
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)