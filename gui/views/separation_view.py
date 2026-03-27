from pathlib import Path

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from gui.components.file_drop_widget import FileDropWidget
from gui.components.waveform_widget import WaveformWidget
from gui.components.progress_panel import ProgressPanel
from gui.dialogs.project_name_dialog import ProjectNameDialog

from backend.projects import project_manager
from backend.separation import separate_stems


# -----------------------------
# Worker Thread for Separation
# -----------------------------
class SeparationWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)

    def __init__(self, audio_path: str, output_dir: str):
        super().__init__()
        self.audio_path = audio_path
        self.output_dir = output_dir

    def run(self):
        self.progress.emit(10)
        stems = separate_stems(self.audio_path, self.output_dir)
        self.progress.emit(100)
        self.finished.emit(stems)


# -----------------------------
# Separation View
# -----------------------------
class SeparationView(QWidget):
    def __init__(self):
        super().__init__()

        self.current_project_id: str | None = None
        self.worker: SeparationWorker | None = None

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)

        # UI Elements
        self.info_label = QLabel("Separation View")
        self.file_drop = FileDropWidget()
        self.waveform = WaveformWidget()
        self.progress = ProgressPanel()

        self.separate_btn = QPushButton("Separate Stems")
        self.separate_btn.setFixedHeight(40)
        self.separate_btn.setEnabled(False)

        # Add widgets
        layout.addWidget(self.info_label)
        layout.addWidget(self.file_drop)
        layout.addWidget(self.waveform)
        layout.addWidget(self.separate_btn)
        layout.addWidget(self.progress)

        self.setLayout(layout)

        # Connections
        self.file_drop.fileSelected.connect(self.on_file_selected)
        self.separate_btn.clicked.connect(self.on_separate_clicked)

    # -----------------------------
    # File Selected → Ask for Project Name
    # -----------------------------
    def on_file_selected(self, path: str):
        dialog = ProjectNameDialog()

        # PyQt6 FIX: use QDialog.DialogCode.Accepted
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.get_name()
            if not name:
                name = Path(path).stem  # fallback

            project = project_manager.create_project(path, name)
            self.current_project_id = project.id

            self.info_label.setText(f"Project: {project.name}")
            self.separate_btn.setEnabled(True)

            # TODO: Load waveform preview here later

    # -----------------------------
    # Run Separation
    # -----------------------------
    def on_separate_clicked(self):
        if not self.current_project_id:
            return

        project = project_manager.projects[self.current_project_id]

        # Folder structure:
        # projects/<project_name>/stems/
        project_dir = Path("projects") / project.name
        stems_dir = project_dir / "stems"
        stems_dir.mkdir(parents=True, exist_ok=True)

        self.progress.set_status("Separating stems...")
        self.progress.set_progress(0)
        self.separate_btn.setEnabled(False)

        # Start worker thread
        self.worker = SeparationWorker(project.audio_path, str(stems_dir))
        self.worker.progress.connect(self.progress.set_progress)
        self.worker.finished.connect(self.on_separation_finished)
        self.worker.start()

    # -----------------------------
    # Separation Finished
    # -----------------------------
    def on_separation_finished(self, stems: list[str]):
        if self.current_project_id:
            project_manager.add_stems(self.current_project_id, stems)

        self.progress.set_status("Separation complete")
        self.progress.set_progress(100)
        self.separate_btn.setEnabled(True)