import axios, { AxiosResponse } from 'axios';


export const API_URL = "https://api.omegasoft.keenetic.name"

axios.defaults.baseURL = API_URL;


export function getRandomVideos() {
    return axios.get('/get_random_video');
  }
