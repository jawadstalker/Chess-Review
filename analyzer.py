import io
import chess
import chess.pgn
from engine import EngineAnalyzer


def classify_move(cp_loss: int):
    if cp_loss < 20:
        return "best"
    elif cp_loss < 50:
        return "excellent"
    elif cp_loss < 90:
        return "good"
    elif cp_loss < 150:
        return "inaccuracy"
    elif cp_loss < 300:
        return "mistake"
    return "blunder"


def safe_lower(s):
    return (s or "").strip().lower()


def build_accuracy(move_rows):
    """
    accuracy تقریبی بر اساس average centipawn loss
    """
    if not move_rows:
        return 0.0

    losses = [row["cp_loss"] for row in move_rows]
    avg_loss = sum(losses) / len(losses)

    # نگاشت ساده و قابل‌تنظیم
    # هرچه loss کمتر، accuracy بیشتر
    accuracy = 100 - (avg_loss * 0.12)
    accuracy = max(0, min(100, accuracy))
    return round(accuracy, 1)


def analyze_pgn(pgn_text: str, stockfish_path: str, username: str, depth: int = 12):
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        raise ValueError("PGN could not be parsed.")

    headers = dict(game.headers)
    white_name = headers.get("White", "")
    black_name = headers.get("Black", "")
    result = headers.get("Result", "*")
    eco = headers.get("ECO", "")
    opening = headers.get("Opening", "")

    username_l = safe_lower(username)
    white_l = safe_lower(white_name)
    black_l = safe_lower(black_name)

    if username_l == white_l:
        player_color = chess.WHITE
        opponent = black_name
    elif username_l == black_l:
        player_color = chess.BLACK
        opponent = white_name
    else:
        # اگر یوزرنیم دقیقاً با PGN match نشد، همچنان بازی را تحلیل می‌کنیم
        player_color = None
        opponent = None

    board = game.board()
    engine = EngineAnalyzer(stockfish_path, depth=depth)

    all_moves = []
    player_moves = []
    white_moves = []
    black_moves = []

    try:
        ply_index = 0

        for move in game.mainline_moves():
            mover_color = board.turn  # کسی که الآن قرار است حرکت کند
            move_no = board.fullmove_number

            fen_before = board.fen()
            before_info = engine.analyze_position(board)
            before_score = EngineAnalyzer.score_to_cp(before_info["score"])
            best_move = before_info["best_move"]

            san = board.san(move)
            board.push(move)

            after_info = engine.analyze_position(board)
            after_score = -EngineAnalyzer.score_to_cp(after_info["score"])

            cp_loss = max(0, before_score - after_score)
            classification = classify_move(cp_loss)

            row = {
                "ply": ply_index + 1,
                "move_number": move_no,
                "side": "white" if mover_color == chess.WHITE else "black",
                "played_move_uci": move.uci(),
                "played_move_san": san,
                "best_move_uci": best_move.uci() if best_move else None,
                "eval_before_cp": before_score,
                "eval_after_cp": after_score,
                "cp_loss": cp_loss,
                "classification": classification,
                "fen_before": fen_before,
            }

            all_moves.append(row)

            if mover_color == chess.WHITE:
                white_moves.append(row)
            else:
                black_moves.append(row)

            if player_color is not None and mover_color == player_color:
                player_moves.append(row)

            ply_index += 1

        # اگر username پیدا نشد، summary مخصوص بازیکن را خالی می‌گذاریم
        target_moves = player_moves if player_color is not None else all_moves

        summary = {
            "player_username": username,
            "player_color": (
                "white" if player_color == chess.WHITE
                else "black" if player_color == chess.BLACK
                else "unknown"
            ),
            "white": white_name,
            "black": black_name,
            "opponent": opponent,
            "result": result,
            "eco": eco,
            "opening": opening,
            "player_accuracy": build_accuracy(target_moves),
            "white_accuracy": build_accuracy(white_moves),
            "black_accuracy": build_accuracy(black_moves),
            "player_blunders": sum(1 for x in target_moves if x["classification"] == "blunder"),
            "player_mistakes": sum(1 for x in target_moves if x["classification"] == "mistake"),
            "player_inaccuracies": sum(1 for x in target_moves if x["classification"] == "inaccuracy"),
            "total_player_moves": len(target_moves),
        }

        return {
            "headers": headers,
            "summary": summary,
            "moves": all_moves,
        }

    finally:
        engine.close()