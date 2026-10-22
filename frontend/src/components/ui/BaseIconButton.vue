<script setup lang="ts">
withDefaults(defineProps<{ label?: string }>(), { label: '' })
const emit = defineEmits<{ click: [MouseEvent] }>()
</script>

<template>
  <button
    type="button"
    :aria-label="label || undefined"
    class="inline-flex h-9 w-9 items-center justify-center rounded-full text-stone-500 transition hover:bg-sand-100 hover:text-clay-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-flamingo-400/50"
    @click="emit('click', $event)"
  >
    <slot />
  </button>
</template>
