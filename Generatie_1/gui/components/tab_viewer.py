from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt6.QtCore import Qt


class TabViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(300)
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
            QTextEdit {
                background-color: #111;
                color: #00ff66;
                font-family: Consolas, monospace;
                font-size: 14px;
                border: none;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Generated Guitar Tab")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setPlaceholderText("Tab output will appear here...")

        layout.addWidget(label)
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    def update_tab(self, text: str):
        """Update the tab display."""
        self.text_area.setPlainText(text)