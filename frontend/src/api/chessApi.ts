import axios from "axios";
import type { RecentGameItem, ReviewReport } from "../types/review";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function fetchRecentGames(username: string, limit = 5) {
  const res = await api.get<RecentGameItem[]>(`/games/${username}?limit=${limit}`);
  return res.data;
}

export async function analyzeGame(payload: {
  username: string;
  pgn: string;
  depth?: number;
}) {
  const res = await api.post<ReviewReport>("/analyze-game", payload);
  return res.data;
}

export default api;