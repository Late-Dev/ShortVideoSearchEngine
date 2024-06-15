// Utilities
import { defineStore } from "pinia";
import { io } from "socket.io-client";
import { ref } from "vue";

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

  return { socket, connected };
});