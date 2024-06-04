<template>
  <v-app>

    <v-main>
      <router-view />
    </v-main>
    <v-app-bar color="transparent" elevation="0" class="toolbar--mobile">
      <template v-slot:append>
        <v-btn icon="mdi-heart"></v-btn>

        <v-btn icon="mdi-magnify"></v-btn>

        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>
    <v-toolbar class="toolbar--mobile"> <v-row class="justify-center ">
        <v-btn rounded="lg" color="primary" variant="flat" icon="mdi-plus">
        </v-btn>
      </v-row></v-toolbar>

  </v-app>
</template>

<script lang="ts" setup>
//
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
