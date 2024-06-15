<template>
  <v-container>
    <!-- <v-text-field v-model="search" label="Поиск" prepend-inner-icon="mdi-magnify" variant="outlined" hide-details
      single-line density="compact" color="primary" @input="debouncedGetSearch"></v-text-field> -->
    <v-autocomplete :items="words" variant="outlined" density="compact" item-props hide-no-data label="Поиск"
      prepend-inner-icon="mdi-magnify" @update:search="search = $event" theme="dark" @update:model-value="getSearch"
      @keydown.enter="getSearch"></v-autocomplete>
    <v-virtual-scroll item-height="'calc(50vh)'" :height="'calc(100vh - 45px)'" :items="videos">
      <template v-slot:default="{ item }">
        <div style="display: flex; position: relative; justify-content: center;">
          <video controls :src="item.link" :key="item.link" style="height: 50vh"></video>
          <div
            style=" position: absolute; bottom: 80px; text-align: center; background: rgba(0, 0, 0, 0.5); border-radius: 10px">
            {{ item.description }}</div>

        </div>
      </template>
    </v-virtual-scroll>
  </v-container>
</template>

<route lang="yaml">
meta:
  layout: search
</route>

<script setup lang="ts">
import { ref } from "vue";
import { getVideosSearch } from "../../api";
import { Videos } from "../../types";

import words from './all_words.json'

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


async function getSearch() {
  console.log(search.value);
  await getVideosSearch(search.value).then((resp) => {
    console.log(resp.data);
    videos.value = resp.data;
  });
}
</script>
