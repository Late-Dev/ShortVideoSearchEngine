<template>
  <v-app style="height: 100vh; overflow: hidden">
    <v-main>
      <router-view />
    </v-main>
    <v-app-bar color="transparent" elevation="0" class="toolbar--mobile">
      <template v-slot:append>
        <v-btn icon="mdi-heart"></v-btn>

        <v-btn icon="mdi-magnify" @click="router.push('/search')"></v-btn>

        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>
    <v-toolbar class="toolbar--mobile">
      <v-row class="justify-center">
        <UploadVideo></UploadVideo>

      </v-row>
    </v-toolbar>
  </v-app>
</template>

<script lang="ts" setup>

import UploadVideo from '../components/UploadVideo.vue'

import { useRouter } from 'vue-router'

const router = useRouter()


</script>

<style scoped lang="scss">
.toolbar {
  @media screen and (max-width: 1020px) {
    display: none;
  }

  &--mobile {
    @media screen and (min-width: 1020px) {
      display: none;
    }
  }
}
</style>
