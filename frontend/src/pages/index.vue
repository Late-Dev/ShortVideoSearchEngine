<template>
  <v-container>
    <div>
      <div class="caption">
        {{ activeVideoData?.description }}
      </div>
      <video v-if="prevVideoData" @wheel="onScrollWheel" v-touch="{
        up: up,
        down: down,
      }" class="video video--prev" :class="{ 'scroll-up': scrollUp, 'scroll-down': scrollDown }"
        :src="prevVideoData?.link"></video>
      <video @wheel="onScrollWheel" v-touch="{
        up: up,
        down: down,
      }" class="video" :class="{ 'scroll-up': scrollUp, 'scroll-down': scrollDown }" autoplay controls
        :src="activeVideoData?.link"></video>
      <video @wheel="onScrollWheel" v-touch="{
        up: up,
        down: down,
      }" class="video video--next" :class="{ 'scroll-up': scrollUp, 'scroll-down': scrollDown }"
        :src="nextVideoData?.link"></video>
    </div>
    <v-fab icon="mdi-movie-search-outline" @click="$router.push('/search/video?url=' + activeVideoData.link)"
      location="bottom end" style="bottom: 200px;" absolute app appear></v-fab>

  </v-container>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";

import { getRandomVideos } from "../api";

import { Videos } from "../types";


const data = ref<Videos[]>([]);

const scrollUp = ref(false);
const scrollDown = ref(false);

const activeVideo = ref(0);

const disabled = ref(false);

async function up() {
  if (disabled.value) return;
  disabled.value = true;
  if (activeVideo.value > data.value.length - 3) {
    await addNewRandomVideos();
  }

  scrollUp.value = true;
  setTimeout(() => {
    scrollUp.value = false;
    activeVideo.value++;
    disabled.value = false;
  }, 800);
}

async function down() {
  if (disabled.value) return;
  disabled.value = true;
  if (activeVideo.value > 0) {
    // videoArray.value.pop()
    scrollDown.value = true;
    setTimeout(() => {
      scrollDown.value = false;
      if (activeVideo.value > 0) {
        activeVideo.value--;
      }
      disabled.value = false;
    }, 800);
  }
}

function onScrollWheel(e) {
  if (e.wheelDelta < 0) {
    up();
  } else {
    down();
  }
}

async function addNewRandomVideos() {
  await getRandomVideos().then((response) => {
    data.value = [...data.value, ...response.data];
  });
}

onMounted(async () => {
  await addNewRandomVideos();
});

const activeVideoData = computed(() => {
  return data.value[activeVideo.value];
});

const nextVideoData = computed(() => {
  return data.value[activeVideo.value + 1];
});

const prevVideoData = computed(() => {
  return data.value[activeVideo.value - 1];
});
</script>

<style scoped lang="scss">
@keyframes scrollDown {
  from {
    transform: translateY(0%);
  }

  to {
    transform: translateY(100%);
  }
}

@keyframes scrollUp {
  from {
    transform: translateY(0%);
  }

  to {
    transform: translateY(-100%);
  }
}

.scroll-up {
  animation: scrollUp 0.82s ease forwards;
}

.scroll-down {
  animation: scrollDown 0.82s ease forwards;
}

.video {
  position: absolute;
  z-index: 0;
  width: 100%;
  height: calc(100% - 64px);
  inset: 0px;
  object-fit: cover;
  transition: transform 0.8s ease;

  &--next {
    top: 100%;
  }

  &--prev {
    top: -100%;
  }
}

.caption {
  position: fixed;
  z-index: 100;
  bottom: 150px;
}
</style>
