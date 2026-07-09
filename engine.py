import chess
import chess.engine


class EngineAnalyzer:
    def __init__(self, stockfish_path: str, depth: int = 15):
        self.stockfish_path = stockfish_path
        self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def close(self):
        self.engine.quit()

    def analyze_position(self, board: chess.Board):
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))
        score = info["score"].pov(board.turn)
        pv = info.get("pv", [])
        best_move = pv[0] if pv else None
        return {
            "score": score,
            "best_move": best_move,
        }

    @staticmethod
    def score_to_cp(score):
        if score.is_mate():
            mate = score.mate()
            if mate is None:
                return 0
            return 100000 if mate > 0 else -100000
        return score.score(mate_score=100000)