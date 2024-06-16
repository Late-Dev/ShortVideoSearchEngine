<template>
  <div>
    <v-progress-circular model-value="100" :indeterminate="status === 'uploaded' || status === 'processing'"
      :color="statusColor">
      <v-icon color="green-darken-2" v-if="status === 'ready'" icon="mdi-check" size="large"></v-icon>
      <v-icon color="error" v-if="status === 'error'" icon="mdi-alert-circle" size="large"></v-icon>

    </v-progress-circular> {{ label }} {{ status }} {{ durationRound(duration) }} {{ duration ? 'сек' : '' }}
  </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { Status } from '../types'

type Props = {
  label: string
  status: Status,
  duration?: number
}

const statusColor = computed(() => {
  if (props.status === 'uploaded') {
    return 'purple'
  }
  if (props.status === 'processing') {
    return 'blue'
  }
  if (props.status === 'error') {
    return 'warning'
  }
  return 'green'
})

const props = defineProps<Props>()

function durationRound(num) {
  if (!num) return
  return Math.round(num*1000)/1000
}

</script>
