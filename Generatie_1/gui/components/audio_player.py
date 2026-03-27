from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl


class AudioPlayer:
    def __init__(self):
        self.output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.output)

    def load(self, file_path: str):
        url = QUrl.fromLocalFile(file_path)
        self.player.setSource(url)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()