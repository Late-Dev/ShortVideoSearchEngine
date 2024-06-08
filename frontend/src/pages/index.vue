<template>
  <v-container>
    <div>
      <div class="caption">{{ activeVideoData?.description }}</div>

      <video @wheel="onScrollWheel" v-touch="{
        up: up,
        down: down
      }" class="video" autoplay controls :src="activeVideoData?.link"></video>
    </div>
  </v-container>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';

import { getRandomVideos } from '../api'

type Videos = {
  link: string,
  description: string
}

const data = ref<Videos[]>([])



const activeVideo = ref(0)

function up() {
  if (activeVideo.value > data.value.length - 2) {
    addNewRandomVideos()
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

async function addNewRandomVideos() {
  await getRandomVideos().then((response)=>{
    data.value = [...data.value, ...response.data]
  })
}

onMounted(async ()=>{
  await addNewRandomVideos()
})



const activeVideoData = computed(() => {
  return data.value[activeVideo.value]
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
