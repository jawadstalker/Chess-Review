export function squareToCoords(square: string, orientation: "white" | "black" = "white") {
    if (!square || square.length < 2) return null;
  
    const file = square[0].toLowerCase();
    const rank = Number(square[1]);
  
    const fileIndex = "abcdefgh".indexOf(file);
    if (fileIndex === -1 || Number.isNaN(rank) || rank < 1 || rank > 8) return null;
  
    let col: number;
    let row: number;
  
    if (orientation === "white") {
      col = fileIndex;        // a=0 ... h=7
      row = 8 - rank;         // rank 8 بالا => row 0
    } else {
      col = 7 - fileIndex;
      row = rank - 1;
    }
  
    return { row, col };
  }
  
  export function uciToSquares(uci?: string | null) {
    if (!uci || uci.length < 4) {
      return { from: null, to: null };
    }
  
    return {
      from: uci.slice(0, 2),
      to: uci.slice(2, 4),
    };
  }