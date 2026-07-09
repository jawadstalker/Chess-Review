from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AnalyzeGameRequest(BaseModel):
    username: str = Field(..., description="Chess.com username")
    pgn: str = Field(..., description="Full PGN text of the game")
    depth: int = Field(12, ge=1, le=30, description="Stockfish analysis depth")


class GameSourceInfo(BaseModel):
    game_url: Optional[str] = None
    time_class: Optional[str] = None
    rated: Optional[bool] = None
    rules: Optional[str] = None


class RecentGameItem(BaseModel):
    url: Optional[str] = None
    pgn: str
    time_class: Optional[str] = None
    rated: Optional[bool] = None
    rules: Optional[str] = None


class AnalyzeGameResponse(BaseModel):
    game_info: Dict[str, Any]
    summary: Dict[str, Any]
    moves: List[Dict[str, Any]]
    headers: Dict[str, Any]
    source: Optional[Dict[str, Any]] = None