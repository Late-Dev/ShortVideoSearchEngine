// Utilities
import { defineStore } from "pinia";
import { Manager } from "socket.io-client";
import { ref } from "vue";

export const useAppStore = defineStore("videos", () => {
  // @ts-ignore
  const manager = new Manager(import.meta.env.VITE_API_URL);

  const connected = ref(false);

  const socket = manager.socket("/"); // main namespace

  socket.on("connect", () => {
    console.log("connected");
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

  return { socket };
});
