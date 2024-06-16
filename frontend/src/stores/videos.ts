// Utilities
import { defineStore } from "pinia";
import { io } from "socket.io-client";
import { ref } from "vue";
import { VideoWithStatus } from "../types";

export const useVideosStore = defineStore("videos", () => {
  const connected = ref(false);

  // @ts-ignore
  const socket = io(import.meta.env.VITE_API_URL, {
    path: "/ws/socket.io/",
    transports: ["websocket"],
  });

  socket.on("connect", () => {
    connected.value = true;
  });

  socket.on("disconnect", () => {
    connected.value = false;
  });

  socket.on("connect_error", (error) => {
    if (socket.active) {
      // temporary failure, the socket will automatically try to reconnect2
      console.log("error, try to reconnect");
    } else {
      // the connection was denied by the server
      // in that case, `socket.connect()` must be manually called in order to reconnect
      console.log(error.message);
    }
  });

  const interval = ref();

  const processedVideo = ref<VideoWithStatus>({
    link: "",
    description: "",
    id: "",
    frames: "uploaded",
    speech: "uploaded",
    indexed: "uploaded",
    faces: "uploaded",
    indexed_faces: "uploaded",
    duration_frames: 0,
    duration_speech: 0,
    duration_indexed: 0,
  });

  function subscribeOnVideo(id: string) {
    socket.emit("status", id);
    interval.value = setInterval(() => {
      socket.emit("status", id);
    }, 3000);
  }

  function unsubscribe() {
    clearInterval(interval.value);
    processedVideo.value = {
      link: "",
      description: "",
      id: "",
      frames: "uploaded",
      speech: "uploaded",
      indexed: "uploaded",
      faces: "uploaded",
      indexed_faces: "uploaded",
      duration_frames: 0,
      duration_speech: 0,
      duration_indexed: 0,
    };
  }

  socket.on("status_response", (response) => {
    console.log(response);
    processedVideo.value = { ...processedVideo.value, ...response };

    if (
      [
        response.faces,
        response.speech,
        response.indexed,
        response.faces,
        response.indexed_faces,
      ].every((val) => val === "ready")
    ) {
      unsubscribe();
    }
  });

  return { socket, connected, subscribeOnVideo, unsubscribe, processedVideo };
});
