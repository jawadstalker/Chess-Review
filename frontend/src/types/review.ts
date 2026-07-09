export type MoveRow = {
    ply: number;
    move_number: number;
    side: "white" | "black";
    played_move_uci: string;
    played_move_san: string;
    best_move_uci?: string | null;
    best_move_san?: string | null;
    eval_before_cp: number;
    eval_after_cp: number;
    cp_loss: number;
    classification: string;
    fen_before: string;
    fen_after: string;
  };
  
  export type GameInfo = {
    white: string;
    black: string;
    result: string;
    opening: string;
    eco: string;
    date?: string;
    time_control?: string;
    termination?: string;
    player_username: string;
    player_color: "white" | "black" | "unknown";
    opponent?: string | null;
    player_result?: string;
  };
  
  export type Summary = {
    player_accuracy: number;
    white_accuracy: number;
    black_accuracy: number;
    player_blunders: number;
    player_mistakes: number;
    player_inaccuracies: number;
    total_player_moves: number;
    total_moves: number;
  };
  
  export type ReviewReport = {
    game_info: GameInfo;
    summary: Summary;
    moves: MoveRow[];
    headers: Record<string, string>;
    source?: {
      game_url?: string;
      time_class?: string;
      rated?: boolean;
      rules?: string;
    };
  };
  
  export type RecentGameItem = {
    url?: string;
    pgn: string;
    time_class?: string;
    rated?: boolean;
    rules?: string;
  };