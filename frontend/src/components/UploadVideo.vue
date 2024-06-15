<template>
  <v-dialog max-width="500">
    <template v-slot:activator="{ props: activatorProps }">

      <v-btn v-bind="activatorProps" @click="resetForms" rounded="lg" color="primary" variant="flat" icon="mdi-plus">
      </v-btn>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card color="secondary" title="Новое видео">
        <v-card-subtitle v-if="!added">
          Добавьте ссылку на видео и описание
        </v-card-subtitle>
        <v-card-text v-if="!added">
          <v-text-field v-model="link" color="primary" label="Ссылка на видео"></v-text-field>
          <v-textarea color="primary" v-model="description" label="Описание и хэштеги"></v-textarea>
        </v-card-text>
        <v-card-subtitle v-if="added">
          Статус обработки видео:
        </v-card-subtitle>
        <v-card-text v-if="added">
          <video :src="videosWS.processedVideo.link" style="height: 100px;"></video>
          {{ videosWS.processedVideo }}
        </v-card-text>




        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="primary" text="Закрыть" @click="isActive.value = false"></v-btn>
          <v-btn color="primary" text="Добавить" v-if="!added" @click="sendNewVideo"></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue';
import { addNewVideo } from '../api'

import { useVideosStore } from '../stores/videos'

const videosWS = useVideosStore()

const link = ref('')
const description = ref('')
const added = ref(false)

const videoId = ref()

async function sendNewVideo() {
  const response = await addNewVideo({ link: link.value, description: description.value })
  videoId.value = response.data.video_id
  added.value = true
  videosWS.processedVideo["link"] = link.value
  videosWS.processedVideo["description"] = description.value

  videosWS.subscribeOnVideo(videoId.value)
}

function resetForms() {
  videosWS.unsubscribe()
  link.value = ''
  description.value = ''
  added.value = false
  videoId.value = undefined
}



onBeforeUnmount(() => {
  resetForms()
})


</script>
