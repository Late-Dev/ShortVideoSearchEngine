<template>
  <v-app style="height: 100vh; overflow: hidden">
    <v-main>
      <router-view />
    </v-main>
    <v-toolbar class="toolbar--mobile">
      <v-row class="justify-space-around">
        <v-btn icon="mdi-magnify" v-if="$route.path === '/'" @click="router.push('/search')"></v-btn>
        <v-btn icon="mdi-home" v-if="$route.path !== '/'" @click="router.push('/')"></v-btn>
        <UploadVideo></UploadVideo>
        <div></div>
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
