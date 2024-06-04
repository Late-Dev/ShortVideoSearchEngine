<template>
  <v-container>
    <div>
      <div class="caption">{{ videoArray[activeVideo] }} {{ activeVideoData.description }}</div>

      <video @wheel="onScrollWheel" v-touch="{
        up: up,
        down: down
      }" class="video" autoplay controls :src="activeVideoData.link"></video>
    </div>
  </v-container>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';
import data from '../assets/yappy_hackaton_2024_400k.json'



const videoSize = 400000

const videoArray = ref<number[]>([generateRandomInt(videoSize)])

const activeVideo = ref(0)

function up() {
  if (activeVideo.value > videoArray.value.length - 2) {

    videoArray.value.push(generateRandomInt(videoSize))
  }
  activeVideo.value++
}

function down() {
  if (activeVideo.value > 0) {

    // videoArray.value.pop()
    activeVideo.value--
  }
}

function onScrollWheel(e) {
  if (e.wheelDelta < 0) {
    up()

  }
  else {
    down()
  }
}




function generateRandomInt(max) {
  return Math.floor(Math.random() * (max)); // The maximum is exclusive and the minimum is inclusive
}

const activeVideoData = computed(() => {
  return data[videoArray.value[activeVideo.value]]
})

</script>

<style scoped lang="scss">
.video {
  position: absolute;
  z-index: 0;
  width: 100%;
  height: calc(100% - 64px);
  inset: 0px;
  object-fit: cover;
}

.caption {
  position: fixed;
  z-index: 100;
  bottom: 150px;
}
</style>
