<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{ name: string; src?: string | null; size?: 'sm' | 'md' | 'lg' }>(), {
  src: null,
  size: 'md',
})

const initials = computed(() =>
  props.name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0]?.toUpperCase() ?? '')
    .join(''),
)

const dimensions: Record<string, string> = {
  sm: 'h-8 w-8 text-xs',
  md: 'h-10 w-10 text-sm',
  lg: 'h-16 w-16 text-xl',
}
</script>

<template>
  <span
    class="inline-flex shrink-0 items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-flamingo-300 to-clay-700 font-medium text-white ring-2 ring-white"
    :class="dimensions[size]"
  >
    <img v-if="src" :src="src" :alt="name" class="h-full w-full object-cover" />
    <span v-else>{{ initials }}</span>
  </span>
</template>
