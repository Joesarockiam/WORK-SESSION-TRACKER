import axios from "axios";

/**
 * API Base URL
 *
 * In production (Render):
 *   process.env.REACT_APP_API_URL = "https://worktracker-backend.onrender.com"
 *
 * In development (local):
 *   falls back to "http://localhost:8000"
 */
const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  withCredentials: false,
});

export default client;
