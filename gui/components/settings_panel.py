from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QFrame
from PyQt6.QtCore import Qt


class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(150)
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
            QComboBox {
                background-color: #2a2a2a;
                color: white;
                padding: 4px;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Model selection dropdown
        self.model_select = QComboBox()
        self.model_select.addItems([
            "Basic Pitch Model",
            "CREPE",
            "Tablurion Model (future)"
        ])

        # Tuning selection dropdown
        self.tuning_select = QComboBox()
        self.tuning_select.addItems([
            "Standard (EADGBE)",
            "Drop D",
            "Half Step Down",
            "Open D",
            "Open G"
        ])

        layout.addWidget(title)
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model_select)
        layout.addWidget(QLabel("Tuning:"))
        layout.addWidget(self.tuning_select)

        self.setLayout(layout)