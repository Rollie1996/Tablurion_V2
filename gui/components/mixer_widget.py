# gui/components/mixer_widget.py
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal


class MixerWidget(QWidget):
    volumeChanged = pyqtSignal(str, float)
    muteChanged = pyqtSignal(str, bool)
    soloChanged = pyqtSignal(str, bool)

    def __init__(self, stem_names: List[str]):
        super().__init__()

        self.stem_names = stem_names
        self.sliders = {}
        self.mute_buttons = {}
        self.solo_buttons = {}

        main_layout = QHBoxLayout()

        for name in stem_names:
            col = QVBoxLayout()

            # Name bar
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Slider
            slider = QSlider(Qt.Orientation.Vertical)
            slider.setRange(0, 100)
            slider.setValue(100)
            slider.valueChanged.connect(
                lambda v, n=name: self.volumeChanged.emit(n, v / 100.0)
            )
            self.sliders[name] = slider

            # Mute button
            mute_btn = QPushButton("Mute")
            mute_btn.setCheckable(True)
            mute_btn.toggled.connect(
                lambda state, n=name: self.muteChanged.emit(n, state)
            )
            self.mute_buttons[name] = mute_btn

            # Solo button
            solo_btn = QPushButton("Solo")
            solo_btn.setCheckable(True)
            solo_btn.toggled.connect(
                lambda state, n=name: self.soloChanged.emit(n, state)
            )
            self.solo_buttons[name] = solo_btn

            col.addWidget(name_label)
            col.addWidget(slider)
            col.addWidget(mute_btn)
            col.addWidget(solo_btn)

            main_layout.addLayout(col)

        self.setLayout(main_layout)