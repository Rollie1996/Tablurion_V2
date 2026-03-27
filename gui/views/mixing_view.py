# gui/views/mixing_view.py
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

from gui.components.mixer_widget import MixerWidget
from gui.components.progress_panel import ProgressPanel
from gui.components.multi_track_player import MultiTrackPlayer

from backend.projects import project_manager


class MixingView(QWidget):
    def __init__(self):
        super().__init__()

        self.current_project_id = None
        self.player = MultiTrackPlayer()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)

        self.title = QLabel("Mixing View")
        self.project_select = QComboBox()
        self.project_select.addItem("Select Project")

        self.mixer = MixerWidget([])

        controls = QHBoxLayout()
        self.play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        controls.addWidget(self.play_btn)
        controls.addWidget(self.pause_btn)
        controls.addWidget(self.stop_btn)

        self.export_btn = QPushButton("Export Mixed Audio")
        self.progress = ProgressPanel()

        layout.addWidget(self.title)
        layout.addWidget(self.project_select)
        layout.addLayout(controls)
        layout.addWidget(self.mixer)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.progress)

        self.setLayout(layout)

        self.project_select.currentIndexChanged.connect(self.on_project_changed)
        self.play_btn.clicked.connect(self.player.play)
        self.pause_btn.clicked.connect(self.player.pause)
        self.stop_btn.clicked.connect(self.player.stop)

        self.mixer.volumeChanged.connect(self.player.set_volume)
        self.mixer.muteChanged.connect(self.player.set_mute)
        self.mixer.soloChanged.connect(self.player.set_solo)

    def showEvent(self, event):
        super().showEvent(event)
        self.reload_projects()

    def reload_projects(self):
        self.project_select.blockSignals(True)
        self.project_select.clear()
        self.project_select.addItem("Select Project")

        for project in project_manager.list_projects():
            self.project_select.addItem(project.name, project.id)

        self.project_select.blockSignals(False)

    def on_project_changed(self, index):
        if index <= 0:
            self.player.clear()
            self.replace_mixer([])
            return

        project_id = self.project_select.itemData(index)
        project = project_manager.projects.get(project_id)

        if not project:
            self.player.clear()
            self.replace_mixer([])
            return

        stems = project.stems
        stem_paths = {Path(s).stem: s for s in stems}

        self.player.load_stems(stem_paths)
        self.replace_mixer(list(stem_paths.keys()))

    def replace_mixer(self, stem_names):
        layout = self.layout()
        old = self.mixer
        old.setParent(None)

        self.mixer = MixerWidget(stem_names)
        self.mixer.volumeChanged.connect(self.player.set_volume)
        self.mixer.muteChanged.connect(self.player.set_mute)
        self.mixer.soloChanged.connect(self.player.set_solo)

        layout.insertWidget(3, self.mixer)