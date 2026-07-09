from pathlib import Path

from chesscom_api import ChessComClient
from analyzer import analyze_pgn
from report_utils import save_json_report

STOCKFISH_PATH = r"D:\stockfish\stockfish-windows-x86-64-avx2.exe"


def main():
    stockfish_file = Path(STOCKFISH_PATH)
    if not stockfish_file.exists():
        print("[ERROR] Stockfish executable not found:")
        print(STOCKFISH_PATH)
        return

    username = input("Chess.com username: ").strip()
    client = ChessComClient(username)

    try:
        games = client.get_recent_games(max_games=3)
    except Exception as e:
        print("[ERROR] Could not fetch games:", e)
        return

    if not games:
        print("No games found.")
        return

    print(f"Found {len(games)} games")

    all_reports = []

    for i, game in enumerate(games, start=1):
        print("=" * 90)
        print(f"Game #{i}")
        print("URL:", game.get("url"))

        try:
            report = analyze_pgn(
                pgn_text=game["pgn"],
                stockfish_path=STOCKFISH_PATH,
                username=username,
                depth=12
            )
        except Exception as e:
            print(f"[ERROR] analyze failed for game #{i}: {e}")
            continue

        report["source"] = {
            "game_url": game.get("url"),
            "time_class": game.get("time_class"),
            "rated": game.get("rated"),
            "rules": game.get("rules"),
        }

        all_reports.append(report)

        game_info = report["game_info"]
        summary = report["summary"]

        print(f"White: {game_info['white']}")
        print(f"Black: {game_info['black']}")
        print(f"Your color: {game_info['player_color']}")
        print(f"Opponent: {game_info['opponent']}")
        print(f"Result: {game_info['result']} ({game_info['player_result']})")
        print(f"Opening: {game_info['opening']} ({game_info['eco']})")
        print(f"Your accuracy: {summary['player_accuracy']}")
        print(f"White accuracy: {summary['white_accuracy']}")
        print(f"Black accuracy: {summary['black_accuracy']}")
        print(
            f"Your counts -> "
            f"Blunders: {summary['player_blunders']}, "
            f"Mistakes: {summary['player_mistakes']}, "
            f"Inaccuracies: {summary['player_inaccuracies']}"
        )

        print("\nYour first 10 analyzed moves:")
        shown = 0
        for row in report["moves"]:
            if row["side"] != game_info["player_color"]:
                continue

            print(
                f"{row['move_number']}. {row['played_move_san']:<8} | "
                f"{row['classification']:<11} | "
                f"loss={row['cp_loss']:<4} | "
                f"best={row['best_move_san'] or row['best_move_uci']}"
            )
            shown += 1
            if shown >= 10:
                break

    if all_reports:
        save_json_report(all_reports, "outputs/analysis_report.json")
        print("\nSaved full report to outputs/analysis_report.json")


if __name__ == "__main__":
    main()