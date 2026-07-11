from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSlider,
    QFrame,
)


class ControlsWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.build_ui()

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setSpacing(12)

        # ===========================
        
        # ===========================

        title = QLabel("Game Controls")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        root.addWidget(title)

        # ===========================
        #
        # ===========================

        self.analyze_button = QPushButton("Analyze Game")

        self.analyze_button.setMinimumHeight(40)

        root.addWidget(self.analyze_button)

        # ===========================
        # ===========================

        move_layout = QHBoxLayout()

        self.prev_button = QPushButton("◀ Previous")

        self.next_button = QPushButton("Next ▶")

        move_layout.addWidget(self.prev_button)
        move_layout.addWidget(self.next_button)

        root.addLayout(move_layout)

        # ===========================
        
        # ===========================

        self.move_slider = QSlider(Qt.Horizontal)

        self.move_slider.setMinimum(0)
        self.move_slider.setMaximum(0)
        self.move_slider.setValue(0)

        root.addWidget(self.move_slider)

        # ===========================
        # ===========================

        self.move_label = QLabel("Move: 0 / 0")

        self.move_label.setAlignment(Qt.AlignCenter)

        root.addWidget(self.move_label)

        # ===========================
        # ===========================

        line = QFrame()

        line.setFrameShape(QFrame.HLine)

        root.addWidget(line)

        # ===========================
        # ===========================

        self.eval_label = QLabel("Eval : --")

        self.best_move_label = QLabel("Best Move : --")

        self.classification_label = QLabel("Classification : --")

        root.addWidget(self.eval_label)

        root.addWidget(self.best_move_label)

        root.addWidget(self.classification_label)

        root.addStretch()

    # ---------------------------------------

    def set_move_count(self, current, total):

        self.move_slider.setMaximum(max(total, 0))
        self.move_slider.setValue(current)

        self.move_label.setText(
            f"Move: {current} / {total}"
        )

    # ---------------------------------------

    def update_analysis(
        self,
        evaluation,
        best_move,
        classification,
    ):

        self.eval_label.setText(
            f"Eval : {evaluation}"
        )

        self.best_move_label.setText(
            f"Best Move : {best_move}"
        )

        self.classification_label.setText(
            f"Classification : {classification}"
        )