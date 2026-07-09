from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from chesscom_api import ChessComClient
from analyzer import analyze_pgn
from schemas import AnalyzeGameRequest, AnalyzeGameResponse, RecentGameItem

# مسیر Stockfish را با مسیر واقعی خودت تنظیم کن
STOCKFISH_PATH = r"C:\Users\203-236\Desktop\chess preview\stockfish\stockfish-windows-x86-64-avx2.exe"

app = FastAPI(
    title="Chess Review API",
    version="0.1.0",
    description="Backend API for Chess.com-style game review"
)

# برای اینکه بعداً React frontend بتواند راحت به API وصل شود
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # بعداً می‌توانیم محدودش کنیم
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_stockfish():
    stockfish_file = Path(STOCKFISH_PATH)
    if not stockfish_file.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Stockfish executable not found at: {STOCKFISH_PATH}"
        )


@app.get("/")
def root():
    return {
        "message": "Chess Review API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    validate_stockfish()
    return {
        "status": "ok",
        "stockfish_path": STOCKFISH_PATH
    }


@app.get("/games/{username}", response_model=List[RecentGameItem])
def get_recent_games(
    username: str,
    limit: int = Query(5, ge=1, le=20)
):
    """
    Fetch recent Chess.com games for a username.
    """
    try:
        client = ChessComClient(username)
        games = client.get_recent_games(max_games=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not games:
        return []

    results = []
    for game in games:
        if not game.get("pgn"):
            continue

        results.append(
            RecentGameItem(
                url=game.get("url"),
                pgn=game["pgn"],
                time_class=game.get("time_class"),
                rated=game.get("rated"),
                rules=game.get("rules"),
            )
        )

    return results


@app.post("/analyze-game", response_model=AnalyzeGameResponse)
def analyze_game(payload: AnalyzeGameRequest):
    """
    Analyze a single PGN game for a given Chess.com username.
    """
    validate_stockfish()

    try:
        report = analyze_pgn(
            pgn_text=payload.pgn,
            stockfish_path=STOCKFISH_PATH,
            username=payload.username,
            depth=payload.depth
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {e}")

    return report


@app.get("/analyze-recent/{username}")
def analyze_recent_games(
    username: str,
    limit: int = Query(3, ge=1, le=10),
    depth: int = Query(12, ge=1, le=30),
):
    """
    Convenience endpoint:
    fetch recent games from Chess.com and analyze them directly.
    """
    validate_stockfish()

    try:
        client = ChessComClient(username)
        games = client.get_recent_games(max_games=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    reports = []

    for game in games:
        pgn = game.get("pgn")
        if not pgn:
            continue

        try:
            report = analyze_pgn(
                pgn_text=pgn,
                stockfish_path=STOCKFISH_PATH,
                username=username,
                depth=depth
            )
        except Exception as e:
            reports.append({
                "source": {
                    "game_url": game.get("url"),
                    "time_class": game.get("time_class"),
                    "rated": game.get("rated"),
                    "rules": game.get("rules"),
                },
                "error": str(e)
            })
            continue

        report["source"] = {
            "game_url": game.get("url"),
            "time_class": game.get("time_class"),
            "rated": game.get("rated"),
            "rules": game.get("rules"),
        }

        reports.append(report)

    return {
        "username": username,
        "count": len(reports),
        "reports": reports
    }