from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from desktop.board_widget import BoardWidget
from desktop.controls import ControlsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chess Review")
        self.resize(1400, 900)

        self.username = ""
        self.current_game = None
        self.current_move_index = 0

        self._create_actions()
        self._create_menu()
        self._build_ui()

        status = QStatusBar()
        status.showMessage("Ready")
        self.setStatusBar(status)

    # --------------------------------------------------
    # Menu
    # --------------------------------------------------

    def _create_actions(self):
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)

    def _create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addAction(self.exit_action)

        help_menu = menu.addMenu("Help")
        help_menu.addAction(self.about_action)

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        # ===========================
        # Header
        # ===========================

        header = QHBoxLayout()

        title = QLabel("Chess Review")

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        header.addWidget(title)
        header.addStretch()

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Chess.com Username")

        self.fetch_button = QPushButton("Load Games")
        self.fetch_button.setMinimumHeight(36)

        header.addWidget(self.username_edit)
        header.addWidget(self.fetch_button)

        root_layout.addLayout(header)

        # ===========================
        # Main Splitter
        # ===========================

        splitter = QSplitter(Qt.Horizontal)

        root_layout.addWidget(splitter)

        # ---------------------------
        # Left Side (Board)
        # ---------------------------

        left = QWidget()
        left_layout = QVBoxLayout(left)

        self.board = BoardWidget()

        self.board.setMinimumSize(640, 640)

        left_layout.addWidget(self.board)

        splitter.addWidget(left)

        # ---------------------------
        # Right Side
        # ---------------------------

        right = QWidget()
        right_layout = QVBoxLayout(right)

        self.controls = ControlsWidget()

        right_layout.addWidget(self.controls)

        info_title = QLabel("Analysis")

        info_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        right_layout.addWidget(info_title)

        self.analysis_box = QTextEdit()

        self.analysis_box.setReadOnly(True)

        self.analysis_box.setPlaceholderText(
            "Game analysis will appear here..."
        )

        right_layout.addWidget(self.analysis_box)

        splitter.addWidget(right)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        right.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )
                # ===========================
        # Status Labels
        # ===========================

        self.game_info = QLabel("No game loaded")
        self.game_info.setAlignment(Qt.AlignCenter)
        self.game_info.setStyleSheet("""
            font-size:15px;
            font-weight:bold;
            color:#555;
        """)

        right_layout.addWidget(self.game_info)

        self.eval_label = QLabel("Evaluation: --")
        self.eval_label.setStyleSheet("""
            font-size:16px;
        """)

        right_layout.addWidget(self.eval_label)

        self.best_move_label = QLabel("Best Move: --")
        self.best_move_label.setStyleSheet("""
            font-size:16px;
        """)

        right_layout.addWidget(self.best_move_label)

        self.classification_label = QLabel("Classification: --")
        self.classification_label.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        right_layout.addWidget(self.classification_label)

        right_layout.addStretch()

        # ===========================
        # Signals
        # ===========================

        self.fetch_button.clicked.connect(self.load_games)

        self.controls.next_button.clicked.connect(
            self.next_move
        )

        self.controls.prev_button.clicked.connect(
            self.previous_move
        )

        self.controls.analyze_button.clicked.connect(
            self.analyze_current_game
        )

    # ==================================================
    # Slots
    # ==================================================

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            "Chess Review Desktop\nVersion 1.0"
        )

    def load_games(self):

        username = self.username_edit.text().strip()

        if not username:

            QMessageBox.warning(
                self,
                "Username",
                "Please enter a Chess.com username."
            )
            return

        self.username = username

        self.statusBar().showMessage(
            f"Loading games for {username}..."
        )

        self.analysis_box.clear()

        self.analysis_box.append(
            f"Username: {username}"
        )

        self.analysis_box.append(
            "\nWaiting for Chess.com API..."
        )

    def analyze_current_game(self):

        self.statusBar().showMessage(
            "Analyzing..."
        )

        self.analysis_box.append(
            "\nStockfish analysis started..."
        )

    def next_move(self):

        self.current_move_index += 1

        self.statusBar().showMessage(
            f"Move {self.current_move_index}"
        )

    def previous_move(self):

        if self.current_move_index > 0:
            self.current_move_index -= 1

        self.statusBar().showMessage(
            f"Move {self.current_move_index}"
        )

    # ==================================================
    # Update Methods
    # ==================================================

    def update_analysis(
        self,
        evaluation: str,
        best_move: str,
        classification: str,
        explanation: str,
    ):

        self.eval_label.setText(
            f"Evaluation: {evaluation}"
        )

        self.best_move_label.setText(
            f"Best Move: {best_move}"
        )

        self.classification_label.setText(
            f"Classification: {classification}"
        )

        self.analysis_box.setPlainText(
            explanation
        )

    def update_game_info(
        self,
        white,
        black,
        result,
        opening,
    ):

        self.game_info.setText(
            f"{white} vs {black}    {result}\n{opening}"
        )