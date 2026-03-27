from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFileDialog, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class FileDropWidget(QWidget):
    fileSelected = pyqtSignal(str)   # Signal emitted when a file is chosen

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.setMinimumHeight(150)
        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #555;
                border-radius: 10px;
                background-color: #2b2b2b;
            }
            QLabel {
                color: #cccccc;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Drag & Drop Audio File Here\nor Click to Browse")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Browse")
        self.button.clicked.connect(self.open_file_dialog)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.selected_file = None

    # -----------------------------
    # Drag & Drop Events
    # -----------------------------
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.set_file(file_path)

    # -----------------------------
    # File Dialog
    # -----------------------------
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.wav *.mp3 *.flac *.ogg)"
        )
        if file_path:
            self.set_file(file_path)

    # -----------------------------
    # Helper
    # -----------------------------
    def set_file(self, path: str):
        self.selected_file = path
        self.label.setText(f"Selected:\n{path}")
        self.fileSelected.emit(path)

    def get_path(self):
        return self.selected_file