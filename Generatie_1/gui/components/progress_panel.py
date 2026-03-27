from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt6.QtCore import Qt


class ProgressPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(120)
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
            QProgressBar {
                background-color: #2a2a2a;
                border: 1px solid #555;
                border-radius: 5px;
                height: 18px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00aa55;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    # -----------------------------
    # Public API for updating UI
    # -----------------------------
    def set_status(self, text: str):
        self.status_label.setText(text)

    def set_progress(self, value: int):
        self.progress_bar.setValue(value)