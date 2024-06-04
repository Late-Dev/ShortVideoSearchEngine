<template>
  <v-container>
    <div>

      <video class="video" autoplay controls
        src="https://cdn-st.rutubelist.ru/media/87/43/b11df3f344d0af773aac81e410ee/fhd.mp4"></video>
    </div>
  </v-container>
</template>

<script lang="ts" setup>
//
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
</style>
