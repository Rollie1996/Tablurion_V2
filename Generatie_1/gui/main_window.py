from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
)
from PyQt6.QtCore import Qt

# Import views
from gui.views.separation_view import SeparationView
from gui.views.guitar_tab_view import GuitarTabView
from gui.views.project_view import ProjectView
from gui.views.audio_view import AudioView
from gui.views.mixing_view import MixingView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tablurion")
        self.setMinimumSize(1400, 900)

        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout()
        container.setLayout(main_layout)

        # -------------------------
        # Sidebar Navigation
        # -------------------------
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)

        btn_sep = QPushButton("Separation")
        btn_tab = QPushButton("Guitar Tab")
        btn_proj = QPushButton("Projects")
        btn_audio = QPushButton("Audio Player")
        btn_mix = QPushButton("Mixer")

        for btn in (btn_sep, btn_tab, btn_proj, btn_audio, btn_mix):
            btn.setFixedHeight(40)
            sidebar.addWidget(btn)

        # -------------------------
        # Stacked Views
        # -------------------------
        self.stack = QStackedWidget()

        self.sep_view = SeparationView()
        self.tab_view = GuitarTabView()
        self.project_view = ProjectView()
        self.audio_view = AudioView()
        self.mixing_view = MixingView()

        self.stack.addWidget(self.sep_view)      # index 0
        self.stack.addWidget(self.tab_view)      # index 1
        self.stack.addWidget(self.project_view)  # index 2
        self.stack.addWidget(self.audio_view)    # index 3
        self.stack.addWidget(self.mixing_view)   # index 4

        # Connect buttons
        btn_sep.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_tab.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_proj.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_audio.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_mix.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        # Add sidebar + stack to layout
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.stack, 5)