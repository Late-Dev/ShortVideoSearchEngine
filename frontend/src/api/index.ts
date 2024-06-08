import axios, { AxiosResponse } from 'axios';


export const API_URL = "http://localhost:8000"

axios.defaults.baseURL = API_URL;


export function getRandomVideos() {
    return axios.get('/get_random_video');
  }
