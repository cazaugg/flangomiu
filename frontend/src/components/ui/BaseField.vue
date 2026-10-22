<script setup lang="ts">
defineProps<{ label?: string; hint?: string; error?: string }>()
</script>

<template>
  <label class="block space-y-1.5">
    <span v-if="label" class="block text-sm font-medium text-stone-700">{{ label }}</span>
    <slot />
    <span v-if="error" class="block text-xs text-flamingo-700">{{ error }}</span>
    <span v-else-if="hint" class="block text-xs text-stone-400">{{ hint }}</span>
  </label>
</template>
