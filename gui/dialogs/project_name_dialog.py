from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton


class ProjectNameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Project")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        self.label = QLabel("Enter a name for this project:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("My Song Name")

        self.ok_btn = QPushButton("Create")
        self.ok_btn.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def get_name(self) -> str:
        return self.input.text().strip()