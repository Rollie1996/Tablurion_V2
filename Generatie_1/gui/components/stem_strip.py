from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QHBoxLayout
from PyQt6.QtCore import Qt


class StemStrip(QWidget):
    def __init__(self, stem_name: str):
        super().__init__()

        self.setFixedWidth(120)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 8px;
            }
            QLabel {
                color: #cccccc;
                font-size: 13px;
            }
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QSlider::groove:vertical {
                background: #333;
                width: 6px;
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                background: #00aa55;
                height: 14px;
                margin: -4px;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Stem name
        label = QLabel(stem_name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Volume slider (centered horizontally)
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(80)

        slider_container = QHBoxLayout()
        slider_container.addStretch()
        slider_container.addWidget(self.slider)
        slider_container.addStretch()

        # Mute + Solo buttons
        self.mute_btn = QPushButton("Mute")
        self.solo_btn = QPushButton("Solo")

        layout.addWidget(label)
        layout.addLayout(slider_container)
        layout.addWidget(self.mute_btn)
        layout.addWidget(self.solo_btn)

        self.setLayout(layout)