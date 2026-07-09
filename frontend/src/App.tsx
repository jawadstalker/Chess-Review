import { useMemo, useState } from "react";
import "./index.css";

import { analyzeGame, fetchRecentGames } from "./api/chessApi";
import ChessBoardPanel from "./components/ChessBoardPanel";
import ControlBar from "./components/ControlBar";
import GameSummary from "./components/GameSummary";
import MoveList from "./components/MoveList";
import MoveReviewCard from "./components/MoveReviewCard";
import type { ReviewReport } from "./types/review";

function App() {
  const [username, setUsername] = useState("Godseeker_Sandman");
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<ReviewReport | null>(null);

  // -1 یعنی قبل از حرکت اول (starting position)
  const [currentMoveIndex, setCurrentMoveIndex] = useState(-1);

  const [error, setError] = useState("");

  const currentMove = useMemo(() => {
    if (!report?.moves?.length) return undefined;
    if (currentMoveIndex < 0) return undefined;
    return report.moves[currentMoveIndex];
  }, [report, currentMoveIndex]);

  const currentFen = useMemo(() => {
    if (!report?.moves?.length) return "start";

    // اگر هنوز هیچ حرکتی انتخاب نشده، بورد روی شروع بازی باشد
    if (currentMoveIndex < 0) {
      return report.moves[0].fen_before;
    }

    return report.moves[currentMoveIndex]?.fen_after || report.moves[0].fen_before;
  }, [report, currentMoveIndex]);

  async function handleAnalyzeLatestGame() {
    setLoading(true);
    setError("");
    setReport(null);

    try {
      const games = await fetchRecentGames(username, 1);

      if (!games.length) {
        throw new Error("No recent games found for this username.");
      }

      const analyzed = await analyzeGame({
        username,
        pgn: games[0].pgn,
        depth: 12,
      });

      setReport({
        ...analyzed,
        source: {
          game_url: games[0].url,
          time_class: games[0].time_class,
          rated: games[0].rated,
          rules: games[0].rules,
        },
      });

      // شروع از position اولیه
      setCurrentMoveIndex(-1);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function goFirst() {
    setCurrentMoveIndex(-1);
  }

  function goPrev() {
    setCurrentMoveIndex((prev) => Math.max(-1, prev - 1));
  }

  function goNext() {
    if (!report) return;
    setCurrentMoveIndex((prev) => Math.min(report.moves.length - 1, prev + 1));
  }

  function goLast() {
    if (!report) return;
    setCurrentMoveIndex(report.moves.length - 1);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>Chess Review</h1>
        <div className="search-box">
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Chess.com username"
          />
          <button onClick={handleAnalyzeLatestGame} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze latest game"}
          </button>
        </div>
      </header>

      {error && <div className="error-box">{error}</div>}

      {!report ? (
        <div className="empty-state">
          <p>Enter a Chess.com username and analyze the latest game.</p>
        </div>
      ) : (
        <div className="review-layout">
          <div className="left-column">
          <ChessBoardPanel
  fen={currentFen}
  currentMove={currentMove}
  orientation={report.game_info.player_color === "black" ? "black" : "white"}
/>
            <ControlBar
              currentIndex={currentMoveIndex}
              maxIndex={report.moves.length - 1}
              onFirst={goFirst}
              onPrev={goPrev}
              onNext={goNext}
              onLast={goLast}
            />
          </div>

          <div className="right-column">
            <GameSummary report={report} />
            <MoveReviewCard move={currentMove} />
            <MoveList
              moves={report.moves}
              currentIndex={currentMoveIndex}
              onSelect={setCurrentMoveIndex}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;