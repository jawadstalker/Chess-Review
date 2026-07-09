import type { ReviewReport } from "../types/review";

type Props = {
  report: ReviewReport;
};

export default function GameSummary({ report }: Props) {
  const { game_info, summary, source } = report;

  return (
    <div className="panel">
      <h2>Game Summary</h2>
      <p><strong>{game_info.white}</strong> vs <strong>{game_info.black}</strong></p>
      <p>Result: {game_info.result} ({game_info.player_result})</p>
      <p>Opening: {game_info.opening || "Unknown"} {game_info.eco ? `(${game_info.eco})` : ""}</p>
      <p>Your color: {game_info.player_color}</p>
      <p>Your accuracy: {summary.player_accuracy}</p>
      <p>White accuracy: {summary.white_accuracy}</p>
      <p>Black accuracy: {summary.black_accuracy}</p>
      <p>Blunders: {summary.player_blunders}</p>
      <p>Mistakes: {summary.player_mistakes}</p>
      <p>Inaccuracies: {summary.player_inaccuracies}</p>

      {source?.game_url && (
        <p>
          Game URL:{" "}
          <a href={source.game_url} target="_blank" rel="noreferrer">
            Open on Chess.com
          </a>
        </p>
      )}
    </div>
  );
}