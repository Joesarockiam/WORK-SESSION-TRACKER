import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "https://worktracker-backend.onrender.com";

console.log("🔥 Using API Base URL:", API_BASE_URL);

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

export default client;
