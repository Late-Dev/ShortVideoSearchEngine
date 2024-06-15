<template>
  <v-app style="height: 100vh; overflow: hidden">
    <v-main>
      <router-view />
    </v-main>
    <v-toolbar class="toolbar--mobile">
      <v-row class="justify-center">
        <UploadVideo></UploadVideo>

      </v-row>
    </v-toolbar>
  </v-app>
</template>

<script setup>
import UploadVideo from '../components/UploadVideo.vue'

</script>

<style scoped lang="scss">
.toolbar--mobile {
  position: fixed;
  bottom: 0;
}
</style>
