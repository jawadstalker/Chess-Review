import { Chessboard } from "react-chessboard";
import type { MoveRow } from "../types/review";
import { getMoveBadge } from "../utils/moveStyles";
import { squareToCoords, uciToSquares } from "../utils/boardUtils";

type Props = {
  fen: string;
  currentMove?: MoveRow;
  orientation?: "white" | "black";
};

export default function ChessBoardPanel({
  fen,
  currentMove,
  orientation = "white",
}: Props) {
  const badge = currentMove ? getMoveBadge(currentMove.classification) : null;
  const playedSquares = currentMove
    ? uciToSquares(currentMove.played_move_uci)
    : { from: null, to: null };

  const targetCoords =
    playedSquares.to ? squareToCoords(playedSquares.to, orientation) : null;

  return (
    <div className="board-card">
      <div className="board-wrapper">
        <Chessboard
          key={fen}
          options={{
            position: fen,
          }}
        />

        <div className="board-overlay-grid">
          {targetCoords && badge && (
            <div
              className="board-badge-cell"
              style={{
                gridColumn: targetCoords.col + 1,
                gridRow: targetCoords.row + 1,
              }}
            >
              <div
                className="board-move-badge"
                style={{
                  background: badge.bg,
                  color: badge.text,
                  borderColor: badge.border,
                }}
                title={`${badge.label} — ${currentMove?.played_move_san ?? ""}`}
              >
                {badge.short}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}