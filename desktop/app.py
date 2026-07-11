import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("Chess Review")
    app.setOrganizationName("Jawad")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()