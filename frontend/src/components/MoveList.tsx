import type { MoveRow } from "../types/review";
import { getMoveBadge } from "../utils/moveStyles";

type Props = {
  moves: MoveRow[];
  currentIndex: number;
  onSelect: (index: number) => void;
};

export default function MoveList({ moves, currentIndex, onSelect }: Props) {
  return (
    <div className="panel move-list">
      <h2>Moves</h2>

      <div className="moves-scroll">
        {moves.map((move, idx) => {
          const badge = getMoveBadge(move.classification);

          return (
            <button
              key={idx}
              className={`move-item ${idx === currentIndex ? "active" : ""}`}
              onClick={() => onSelect(idx)}
            >
              <div className="move-item-main">
                <span className="move-left">
                  <span className="move-number">{move.move_number}.</span>
                  <span className="move-san">{move.played_move_san}</span>
                </span>

                <span
                  className="move-badge"
                  style={{
                    background: badge.bg,
                    color: badge.text,
                    borderColor: badge.border,
                  }}
                >
                  {badge.short} {badge.label}
                </span>
              </div>

              <div className="move-subline">
                <span>Loss: {move.cp_loss}</span>
                {move.best_move_san && (
                  <span>Best: {move.best_move_san}</span>
                )}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}