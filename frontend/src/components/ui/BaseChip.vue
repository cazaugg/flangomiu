<script setup lang="ts">
withDefaults(defineProps<{ active?: boolean }>(), { active: false })
const emit = defineEmits<{ toggle: [] }>()
</script>

<template>
  <button
    type="button"
    class="inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition"
    :class="
      active
        ? 'border-flamingo-300 bg-flamingo-100 text-flamingo-700'
        : 'border-sand-200 bg-white text-stone-500 hover:border-flamingo-200 hover:text-clay-700'
    "
    @click="emit('toggle')"
  >
    <slot />
  </button>
</template>
