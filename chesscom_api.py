import requests


class ChessComClient:
    BASE = "https://api.chess.com/pub/player"

    def __init__(self, username: str):
        self.username = username.lower().strip()

    def get_archives(self):
        url = f"{self.BASE}/{self.username}/games/archives"
        r = requests.get(url, headers={"User-Agent": "chess-review-app/1.0"})
        r.raise_for_status()
        return r.json()["archives"]

    def get_games_from_archive(self, archive_url: str):
        r = requests.get(archive_url, headers={"User-Agent": "chess-review-app/1.0"})
        r.raise_for_status()
        return r.json().get("games", [])

    def get_recent_games(self, max_games=20):
        archives = self.get_archives()
        archives = list(reversed(archives))  # newest first

        games = []
        for archive_url in archives:
            month_games = self.get_games_from_archive(archive_url)
            month_games = list(reversed(month_games))
            for g in month_games:
                if "pgn" in g:
                    games.append(g)
                if len(games) >= max_games:
                    return games
        return games