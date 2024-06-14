import axios, { AxiosResponse } from "axios";
import { Videos } from "../types";

export const API_URL = import.meta.env.VITE_API_URL;

axios.defaults.baseURL = API_URL;

export function getRandomVideos() {
  return axios.get("/get_random_video");
}

export function getVideosSearch(query: string) {
  return axios.get("/get_video_by_query", { params: { query } });
}

export function addNewVideo(payload: Videos) {
  return axios.post("add_video", payload);
}
