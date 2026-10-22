<script setup lang="ts">
withDefaults(
  defineProps<{ tone?: 'neutral' | 'brand' | 'success' | 'warn' | 'danger' }>(),
  { tone: 'neutral' },
)

const tones: Record<string, string> = {
  neutral: 'bg-sand-100 text-stone-700',
  brand: 'bg-flamingo-100 text-flamingo-700',
  success: 'bg-emerald-100 text-emerald-700',
  warn: 'bg-amber-100 text-amber-700',
  danger: 'bg-red-100 text-red-700',
}
</script>

<template>
  <span
    class="inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium"
    :class="tones[tone]"
  >
    <slot />
  </span>
</template>
