<template>


  <v-container class="overflow-y-auto" style="max-height: calc(100vh - 50px)">
    <v-row>
      <v-col v-for="item in videos" :key="item.link">
        <div style="display: flex; position: relative; justify-content: center;">
          <video controls :src="item.link" :key="item.link" style=" height: 50vh; "></video>
          <div class="description">
            {{ item.description }}</div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup lang="ts">

defineProps(['videos'])

</script>
<style lang="scss" scoped>
.description {
  max-width: calc(100% - 80px);
  padding: 5px;
  font-size: 12px;
  position: absolute;
  bottom: 80px;
  text-align: center;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px
}
</style>
