# gui/views/project_view.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget
from PyQt6.QtCore import Qt

from backend.projects import project_manager


class ProjectView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)

        self.title = QLabel("Projects")
        self.list_widget = QListWidget()

        layout.addWidget(self.title)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.reload_projects()

    def reload_projects(self):
        self.list_widget.clear()
        for p in project_manager.list_projects():
            status = "with stems" if p.stems else "no stems yet"
            self.list_widget.addItem(f"{p.name}  ({status})")