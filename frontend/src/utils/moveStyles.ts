export type MoveBadgeConfig = {
    label: string;
    short: string;
    bg: string;
    text: string;
    border: string;
  };
  
  export function getMoveBadge(classification?: string): MoveBadgeConfig {
    const c = (classification || "").toLowerCase();
  
    if (c.includes("blunder")) {
      return {
        label: "Blunder",
        short: "??",
        bg: "#5a1f24",
        text: "#ff8a93",
        border: "#b83c49",
      };
    }
  
    if (c.includes("mistake")) {
      return {
        label: "Mistake",
        short: "?",
        bg: "#5b3416",
        text: "#ffb36b",
        border: "#d57a24",
      };
    }
  
    if (c.includes("inaccuracy")) {
      return {
        label: "Inaccuracy",
        short: "?!",
        bg: "#5b5316",
        text: "#ffe06b",
        border: "#c7a81e",
      };
    }
  
    if (c.includes("best")) {
      return {
        label: "Best",
        short: "!!",
        bg: "#173f2d",
        text: "#74f0ad",
        border: "#2fa86a",
      };
    }
  
    if (c.includes("excellent")) {
      return {
        label: "Excellent",
        short: "!!",
        bg: "#173f2d",
        text: "#74f0ad",
        border: "#2fa86a",
      };
    }
  
    if (c.includes("good")) {
      return {
        label: "Good",
        short: "!",
        bg: "#16354f",
        text: "#7fc5ff",
        border: "#3a89d1",
      };
    }
  
    return {
      label: classification || "Move",
      short: "•",
      bg: "#333842",
      text: "#d7dbe3",
      border: "#555b66",
    };
  }
  export function isProblemMove(classification?: string): boolean {
    const c = (classification || "").toLowerCase();
    return (
      c.includes("inaccuracy") ||
      c.includes("mistake") ||
      c.includes("blunder")
    );
  }
  