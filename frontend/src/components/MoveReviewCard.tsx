import type { MoveRow } from "../types/review";
import { getMoveBadge } from "../utils/moveStyles";

type Props = {
  move?: MoveRow;
};

export default function MoveReviewCard({ move }: Props) {
  if (!move) {
    return (
      <div className="panel">
        <h2>Move Review</h2>
        <p>Start position — select a move or press next.</p>
      </div>
    );
  }

  const badge = getMoveBadge(move.classification);

  return (
    <div className="panel">
      <div className="move-review-header">
        <h2>Move Review</h2>

        <span
          className="review-badge"
          style={{
            background: badge.bg,
            color: badge.text,
            borderColor: badge.border,
          }}
        >
          {badge.label}
        </span>
      </div>

      <div className="review-grid">
        <div className="review-row">
          <span className="review-key">Played move</span>
          <span className="review-value">{move.played_move_san}</span>
        </div>

        <div className="review-row">
          <span className="review-key">Best move</span>
          <span className="review-value">
            {move.best_move_san || move.best_move_uci || "-"}
          </span>
        </div>

        <div className="review-row">
          <span className="review-key">Side</span>
          <span className="review-value">{move.side}</span>
        </div>

        <div className="review-row">
          <span className="review-key">Move number</span>
          <span className="review-value">{move.move_number}</span>
        </div>

        <div className="review-row">
          <span className="review-key">Centipawn loss</span>
          <span className="review-value">{move.cp_loss}</span>
        </div>

        <div className="review-row">
          <span className="review-key">Eval before</span>
          <span className="review-value">{move.eval_before_cp}</span>
        </div>

        <div className="review-row">
          <span className="review-key">Eval after</span>
          <span className="review-value">{move.eval_after_cp}</span>
        </div>
      </div>
    </div>
  );
}