<template>
  <v-dialog max-width="500">
    <template v-slot:activator="{ props: activatorProps }">

      <v-btn v-bind="activatorProps" rounded="lg" color="primary" variant="flat" icon="mdi-plus">
      </v-btn>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card color="secondary" title="Новое видео">
        <v-card-subtitle>
          Добавьте ссылку на видео и описание
        </v-card-subtitle>
        <v-card-text>
          <v-text-field v-model="link" color="primary" label="Ссылка на видео"></v-text-field>
          <v-textarea color="primary" v-model="description" label="Описание и хэштеги"></v-textarea>
        </v-card-text>



        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="primary" text="Закрыть" @click="isActive.value = false"></v-btn>
          <v-btn color="primary" text="Добавить" @click="sendNewVideo"></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { addNewVideo } from '../api'



const link = ref('')
const description = ref('')


async function sendNewVideo() {
  await addNewVideo({ link: link.value, description: description.value })
}


</script>
