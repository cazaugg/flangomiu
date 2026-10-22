<script setup lang="ts">
import BaseIconButton from './BaseIconButton.vue'

defineProps<{ open: boolean; title?: string }>()
const emit = defineEmits<{ close: [] }>()
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="open" class="fixed inset-0 z-50 flex items-end justify-center sm:items-center sm:p-6">
        <div class="absolute inset-0 bg-stone-900/40 backdrop-blur-sm" @click="emit('close')" />
        <div
          class="relative max-h-[92vh] w-full overflow-y-auto rounded-t-3xl bg-flamingo-50 p-6 shadow-2xl sm:max-w-lg sm:rounded-3xl"
        >
          <div class="mb-5 flex items-start justify-between gap-4">
            <h2 class="font-display text-2xl font-semibold text-clay-700">{{ title }}</h2>
            <BaseIconButton @click="emit('close')">✕</BaseIconButton>
          </div>
          <slot />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
