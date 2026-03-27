# gui/components/multi_track_player.py
from pathlib import Path
from typing import Dict

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class MultiTrackPlayer:
    def __init__(self):
        self.players: Dict[str, QMediaPlayer] = {}
        self.outputs: Dict[str, QAudioOutput] = {}
        self.stem_paths: Dict[str, Path] = {}

        self.volumes: Dict[str, float] = {}
        self.muted: Dict[str, bool] = {}
        self.soloed: Dict[str, bool] = {}

    def clear(self):
        for player in self.players.values():
            player.stop()
        self.players.clear()
        self.outputs.clear()
        self.stem_paths.clear()
        self.volumes.clear()
        self.muted.clear()
        self.soloed.clear()

    def load_stems(self, stem_paths: Dict[str, str]):
        self.clear()

        for name, path_str in stem_paths.items():
            path = Path(path_str).resolve()
            self.stem_paths[name] = path

            output = QAudioOutput()
            player = QMediaPlayer()
            player.setAudioOutput(output)
            player.setSource(QUrl.fromLocalFile(str(path)))

            self.players[name] = player
            self.outputs[name] = output

            self.volumes[name] = 1.0
            self.muted[name] = False
            self.soloed[name] = False

            output.setVolume(1.0)

    def play(self):
        for player in self.players.values():
            player.play()

    def pause(self):
        for player in self.players.values():
            player.pause()

    def stop(self):
        for player in self.players.values():
            player.stop()

    # -----------------------------
    # Volume / Mute / Solo
    # -----------------------------
    def set_volume(self, stem_name: str, volume_0_1: float):
        self.volumes[stem_name] = volume_0_1
        self._apply_mix()

    def set_mute(self, stem_name: str, muted: bool):
        self.muted[stem_name] = muted
        self._apply_mix()

    def set_solo(self, stem_name: str, solo: bool):
        self.soloed[stem_name] = solo
        self._apply_mix()

    def _apply_mix(self):
        any_solo = any(self.soloed.values())

        for name, output in self.outputs.items():
            if any_solo:
                # Only soloed tracks play
                if self.soloed[name]:
                    output.setVolume(self.volumes[name])
                else:
                    output.setVolume(0.0)
            else:
                # Normal mute/volume logic
                if self.muted[name]:
                    output.setVolume(0.0)
                else:
                    output.setVolume(self.volumes[name])