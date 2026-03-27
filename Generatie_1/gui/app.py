import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow


def run_app():
    app = QApplication(sys.argv)

    window = MainWindow()

    # Load dark theme by default
    try:
        with open("gui/styles/dark.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: dark.qss not found. Running without stylesheet.")

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()