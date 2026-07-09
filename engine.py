import chess
import chess.engine


class EngineAnalyzer:
    def __init__(self, stockfish_path: str, depth: int = 12):
        self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def analyze_position(self, board: chess.Board):
        info = self.engine.analyse(
            board,
            chess.engine.Limit(depth=self.depth)
        )

        pv = info.get("pv", [])
        best_move = pv[0] if pv else None
        score = info["score"].white()

        return {
            "best_move": best_move,
            "score": score,
            "raw": info,
        }

    @staticmethod
    def score_to_cp(score) -> int:
        """
        Convert python-chess score to centipawns.
        Mate scores are mapped to large values.
        """
        if score.is_mate():
            mate = score.mate()
            if mate is None:
                return 0

            # Positive mate => huge positive score, negative mate => huge negative
            if mate > 0:
                return 100000 - (abs(mate) * 100)
            else:
                return -100000 + (abs(mate) * 100)

        cp = score.score()
        return cp if cp is not None else 0

    def close(self):
        if self.engine:
            self.engine.quit()