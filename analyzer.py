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
    A simple approximate accuracy based on average centipawn loss.
    """
    if not move_rows:
        return 0.0

    losses = [row["cp_loss"] for row in move_rows]
    avg_loss = sum(losses) / len(losses)

    accuracy = 100 - (avg_loss * 0.12)
    accuracy = max(0, min(100, accuracy))
    return round(accuracy, 1)


def result_for_color(result: str, color: str):
    """
    color: 'white' or 'black'
    returns: 'win' / 'loss' / 'draw' / 'unknown'
    """
    if result == "1-0":
        return "win" if color == "white" else "loss"
    elif result == "0-1":
        return "loss" if color == "white" else "win"
    elif result == "1/2-1/2":
        return "draw"
    return "unknown"


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
    date = headers.get("Date", "")
    time_control = headers.get("TimeControl", "")
    termination = headers.get("Termination", "")

    username_l = safe_lower(username)
    white_l = safe_lower(white_name)
    black_l = safe_lower(black_name)

    player_color = None
    opponent = None

    if username_l == white_l:
        player_color = chess.WHITE
        opponent = black_name
    elif username_l == black_l:
        player_color = chess.BLACK
        opponent = white_name

    board = game.board()
    engine = EngineAnalyzer(stockfish_path, depth=depth)

    all_moves = []
    white_moves = []
    black_moves = []
    player_moves = []

    try:
        ply_index = 0

        for move in game.mainline_moves():
            mover_color = board.turn
            move_no = board.fullmove_number

            fen_before = board.fen()

            before_info = engine.analyze_position(board)
            before_score = EngineAnalyzer.score_to_cp(before_info["score"])
            best_move = before_info["best_move"]

            # SAN of played move must be computed before push
            played_move_san = board.san(move)

            best_move_san = None
            if best_move is not None:
                try:
                    best_move_san = board.san(best_move)
                except Exception:
                    best_move_san = None

            board.push(move)
            fen_after = board.fen()

            after_info = engine.analyze_position(board)
            # Negate because side to move changed after push
            after_score = -EngineAnalyzer.score_to_cp(after_info["score"])

            cp_loss = max(0, before_score - after_score)
            classification = classify_move(cp_loss)

            row = {
                "ply": ply_index + 1,
                "move_number": move_no,
                "side": "white" if mover_color == chess.WHITE else "black",
                "played_move_uci": move.uci(),
                "played_move_san": played_move_san,
                "best_move_uci": best_move.uci() if best_move else None,
                "best_move_san": best_move_san,
                "eval_before_cp": before_score,
                "eval_after_cp": after_score,
                "cp_loss": cp_loss,
                "classification": classification,
                "fen_before": fen_before,
                "fen_after": fen_after,
            }

            all_moves.append(row)

            if mover_color == chess.WHITE:
                white_moves.append(row)
            else:
                black_moves.append(row)

            if player_color is not None and mover_color == player_color:
                player_moves.append(row)

            ply_index += 1

        if player_color == chess.WHITE:
            player_color_name = "white"
        elif player_color == chess.BLACK:
            player_color_name = "black"
        else:
            player_color_name = "unknown"

        target_moves = player_moves if player_color is not None else all_moves

        game_info = {
            "white": white_name,
            "black": black_name,
            "result": result,
            "opening": opening,
            "eco": eco,
            "date": date,
            "time_control": time_control,
            "termination": termination,
            "player_username": username,
            "player_color": player_color_name,
            "opponent": opponent,
            "player_result": (
                result_for_color(result, player_color_name)
                if player_color_name in ("white", "black")
                else "unknown"
            ),
        }

        summary = {
            "player_accuracy": build_accuracy(target_moves),
            "white_accuracy": build_accuracy(white_moves),
            "black_accuracy": build_accuracy(black_moves),
            "player_blunders": sum(1 for x in target_moves if x["classification"] == "blunder"),
            "player_mistakes": sum(1 for x in target_moves if x["classification"] == "mistake"),
            "player_inaccuracies": sum(1 for x in target_moves if x["classification"] == "inaccuracy"),
            "total_player_moves": len(target_moves),
            "total_moves": len(all_moves),
        }

        return {
            "game_info": game_info,
            "summary": summary,
            "moves": all_moves,
            "headers": headers,
        }

    finally:
        engine.close()