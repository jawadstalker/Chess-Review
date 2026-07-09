import json
from pathlib import Path

from chesscom_api import ChessComClient
from analyzer import analyze_pgn

STOCKFISH_PATH = r"D:\stockfish\stockfish-windows-x86-64-avx2.exe"


def main():
    stockfish_file = Path(STOCKFISH_PATH)
    if not stockfish_file.exists():
        print("[ERROR] Stockfish executable پیدا نشد:")
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
        print("هیچ بازی‌ای پیدا نشد.")
        return

    print(f"Found {len(games)} games")

    reports = []

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
            print(f"[ERROR] analyze failed: {e}")
            continue

        summary = report["summary"]
        reports.append(report)

        print(f"White: {summary['white']}")
        print(f"Black: {summary['black']}")
        print(f"Your color: {summary['player_color']}")
        print(f"Opponent: {summary['opponent']}")
        print(f"Result: {summary['result']}")
        print(f"Opening: {summary['opening']} ({summary['eco']})")
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
            if row["side"] != summary["player_color"]:
                continue

            print(
                f"{row['move_number']}. {row['played_move_san']:<8} | "
                f"{row['classification']:<11} | "
                f"loss={row['cp_loss']:<4} | "
                f"best={row['best_move_uci']}"
            )
            shown += 1
            if shown >= 10:
                break

    if reports:
        with open("analysis_report.json", "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)

        print("\nSaved full report to analysis_report.json")


if __name__ == "__main__":
    main()