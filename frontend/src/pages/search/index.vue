<template>
  <v-container>
    <!-- <v-text-field v-model="search" label="Поиск" prepend-inner-icon="mdi-magnify" variant="outlined" hide-details
      single-line density="compact" color="primary" @input="debouncedGetSearch"></v-text-field> -->
    <v-autocomplete :items="words" variant="outlined" density="compact" item-props hide-no-data label="Поиск"
      prepend-inner-icon="mdi-magnify" @update:search="search = $event" theme="dark"
      @update:model-value="search = $event; getSearch()" @keydown.enter="getSearch"></v-autocomplete>
    <VideoContainer :videos="videos"></VideoContainer>
    <div v-if="!videos?.length">
      Введите запрос и нажмите Enter
    </div>
  </v-container>
</template>

<route lang="yaml">

</route>

<script setup lang="ts">
import { ref } from "vue";
import { getVideosSearch } from "../../api";
import { Videos } from "../../types";

import words from './all_words.json'
import VideoContainer from "../../components/VideoContainer.vue";

const search = ref();

const videos = ref<Videos[]>();

// Функция debounce
function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

// Создаем обертку для getSearch с debounce
const debouncedGetSearch = debounce(getSearch, 500);

function onScroll() {
  return
}

async function getSearch() {
  console.log(search.value);
  await getVideosSearch(search.value).then((resp) => {
    console.log(resp.data);
    videos.value = resp.data;
  });
}
</script>

