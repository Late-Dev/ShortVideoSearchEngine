import axios from "axios";
import { Videos } from "../types";
// @ts-ignore
export const API_URL = import.meta.env.VITE_API_URL;

axios.defaults.baseURL = API_URL;

export function getRandomVideos() {
  return axios.get("/get_random_video");
}

export function getVideosSearch(text: string) {
  return axios.get("/search", { params: { text } });
}

export function addNewVideo(payload: Videos) {
  return axios.post("index", payload);
}
