<script setup lang="ts">
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

const tones: Record<string, string> = {
  success: 'bg-emerald-600',
  error: 'bg-brick-600',
  info: 'bg-clay-700',
}
</script>

<template>
  <div
    class="pointer-events-none fixed inset-x-0 bottom-24 z-[60] flex flex-col items-center gap-2 px-4 sm:bottom-6"
  >
    <TransitionGroup name="fade">
      <button
        v-for="toast in ui.toasts"
        :key="toast.id"
        class="pointer-events-auto rounded-full px-4 py-2 text-sm font-medium text-white shadow-lg"
        :class="tones[toast.tone]"
        @click="ui.dismiss(toast.id)"
      >
        {{ toast.message }}
      </button>
    </TransitionGroup>
  </div>
</template>
