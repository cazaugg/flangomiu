<script setup lang="ts">
withDefaults(defineProps<{ icon?: string; title: string; message?: string }>(), {
  icon: '🦩',
  message: '',
})
</script>

<template>
  <div
    class="flex flex-col items-center justify-center gap-2 rounded-3xl border border-dashed border-sand-300 bg-white/50 px-6 py-12 text-center"
  >
    <div class="text-3xl">{{ icon }}</div>
    <p class="font-display text-lg text-clay-700">{{ title }}</p>
    <p v-if="message" class="max-w-sm text-sm text-stone-500">{{ message }}</p>
    <div v-if="$slots.default" class="mt-2">
      <slot />
    </div>
  </div>
</template>
