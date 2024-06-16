<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>

import { onMounted } from 'vue';
import { useVideosStore } from './stores/videos'

const videoStore = useVideosStore()

onMounted(() => {
  videoStore.socket.connect()
})

</script>
