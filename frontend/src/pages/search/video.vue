<template>

  <VideoContainer :videos="videos"></VideoContainer>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { getSimilar } from '../../api';


const route = useRoute()
const videos = ref()

onMounted(async () => {
  await getSimilar(route.query.url as string).then((response) => { videos.value = response.data })
})
</script>
