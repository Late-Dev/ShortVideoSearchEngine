<template>
  <v-app style="height: 100vh; overflow: hidden">
    <v-main>
      <router-view />
    </v-main>
    <v-app-bar color="transparent" elevation="0" class="toolbar--mobile">
      <template v-slot:append>
        <v-btn icon="mdi-heart"></v-btn>

        <v-btn icon="mdi-magnify" @click="router.push('/search')"></v-btn>

        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>
    <v-toolbar class="toolbar--mobile">
      <v-row class="justify-center">

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
      </v-row>
    </v-toolbar>
  </v-app>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import { addNewVideo } from '../api'

const router = useRouter()

const link = ref('')
const description = ref('')

async function sendNewVideo() {
  await addNewVideo({ link: link.value, description: description.value })
}

</script>

<style scoped lang="scss">
.toolbar {
  @media screen and (max-width: 1020px) {
    display: none;
  }

  &--mobile {
    @media screen and (min-width: 1020px) {
      display: none;
    }
  }
}
</style>
