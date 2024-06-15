<template>
  <v-app style="height: 100vh; overflow: hidden">
    <v-main>
      <router-view />
    </v-main>
    <v-toolbar class="toolbar--mobile">
      <v-row class="justify-center">
        <v-btn rounded="lg" color="primary" variant="flat" icon="mdi-plus">
        </v-btn>
      </v-row>
    </v-toolbar>
  </v-app>
</template>

<style scoped lang="scss">
.toolbar--mobile{
  position: fixed;
  bottom: 0;
}
</style>
