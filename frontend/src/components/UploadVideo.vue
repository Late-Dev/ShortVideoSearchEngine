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
        <v-card-text v-if="added" class="preview">

          <video :src="videosWS.processedVideo.link" style="height: 200px;"></video>
          <div class="statuses">
            <UploadTag class="tag" label="Визуальный анализ" :duration="videosWS.processedVideo.duration_frames"
              :status="videosWS.processedVideo.frames" />
            <UploadTag class="tag" label="Анализ речи" :duration="videosWS.processedVideo.duration_speech"
              :status="videosWS.processedVideo.speech" />
            <UploadTag class="tag" label="Распознавание лиц" :status="videosWS.processedVideo.faces" />
            <UploadTag class="tag" label="Добавление в индекс лиц" :status="videosWS.processedVideo.indexed_faces" />
            <UploadTag class="tag" label="Индексация" :duration="videosWS.processedVideo.duration_indexed"
              :status="videosWS.processedVideo.indexed" />

          </div>
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
import UploadTag from './UploadTag.vue';

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

<style scoped lang="scss">
.preview {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.statuses {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}

.tag {
  margin: 5px 0;
}
</style>
