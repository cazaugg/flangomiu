<script setup lang="ts">
defineProps<{ title: string; subtitle?: string }>()
</script>

<template>
  <header class="flex flex-wrap items-end justify-between gap-4">
    <div>
      <h1 class="font-display text-3xl font-semibold text-clay-700 sm:text-4xl">{{ title }}</h1>
      <p v-if="subtitle" class="mt-1 text-sm text-stone-500">{{ subtitle }}</p>
    </div>
    <div class="flex items-center gap-2">
      <slot />
    </div>
  </header>
</template>
