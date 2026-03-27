from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 8px;
            }
            QLabel {
                color: #bbbbbb;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        placeholder = QLabel("Waveform Preview\n(coming soon)")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(placeholder)
        self.setLayout(layout)