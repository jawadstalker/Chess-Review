from __future__ import annotations
import io
import chess.pgn
import chess

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QBrush, QPen
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QVBoxLayout,
)


BOARD_SIZE = 8
SQUARE_SIZE = 80


LIGHT_COLOR = QColor("#f0d9b5")
DARK_COLOR = QColor("#b58863")

LAST_MOVE_COLOR = QColor("#f6f669")


class BoardWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.board = chess.Board()

        self.last_move = None

        self.scene = QGraphicsScene(self)

        self.view = QGraphicsView(self.scene)

        self.view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.view.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.view.setFrameShape(
            QGraphicsView.NoFrame
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.view)

        self.draw_board()
            # -----------------------------------

    def draw_board(self):

        self.scene.clear()

        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                color = LIGHT_COLOR

                if (row + col) % 2:
                    color = DARK_COLOR

                self.scene.addRect(

                    QRectF(

                        col * SQUARE_SIZE,

                        row * SQUARE_SIZE,

                        SQUARE_SIZE,

                        SQUARE_SIZE

                    ),

                    QPen(Qt.NoPen),

                    QBrush(color)

                )

        self.scene.setSceneRect(

            0,

            0,

            BOARD_SIZE * SQUARE_SIZE,

            BOARD_SIZE * SQUARE_SIZE

        )

        self.draw_coordinates()
            # -----------------------------------

    def draw_coordinates(self):

        files = "abcdefgh"

        for i in range(8):

            self.scene.addText(

                files[i]

            ).setPos(

                i * SQUARE_SIZE + 4,

                8 * SQUARE_SIZE - 22

            )

        for i in range(8):

            self.scene.addText(

                str(8 - i)

            ).setPos(

                2,

                i * SQUARE_SIZE + 2

            )
                # -----------------------------------

    def reset_board(self):

        self.board.reset()

        self.draw_board()
            # -----------------------------------

    def load_fen(self, fen: str):

        self.board.set_fen(fen)

        self.draw_board()
            # -----------------------------------

    def load_pgn(self, pgn):

        game = chess.pgn.read_game(
            io.StringIO(pgn)
        )

        self.board = game.board()

        self.draw_board()
            # -----------------------------------

    def next_move(self):

        pass

    def previous_move(self):

        pass