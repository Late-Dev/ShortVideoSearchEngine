<template>
  <v-app>
    <v-toolbar class="toolbar" title="Application"></v-toolbar>

    <v-main>
      <router-view />
    </v-main>
    <v-toolbar class="toolbar--mobile" title="Application"></v-toolbar>

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
