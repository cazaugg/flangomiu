<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
    size?: 'sm' | 'md' | 'lg'
    type?: 'button' | 'submit' | 'reset'
    disabled?: boolean
    block?: boolean
  }>(),
  { variant: 'primary', size: 'md', type: 'button', disabled: false, block: false },
)

const base =
  'inline-flex items-center justify-center gap-2 rounded-full font-medium transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-flamingo-400/60 focus-visible:ring-offset-2 focus-visible:ring-offset-flamingo-50 disabled:cursor-not-allowed disabled:opacity-50'

const variants: Record<string, string> = {
  primary:
    'bg-flamingo-500 text-white shadow-[0_10px_30px_-12px_var(--color-flamingo-600)] hover:bg-flamingo-600 active:scale-[0.98]',
  secondary:
    'border border-sand-200 bg-white text-clay-700 hover:border-flamingo-300 hover:text-flamingo-700',
  ghost: 'text-stone-500 hover:bg-sand-100 hover:text-clay-700',
  danger: 'bg-brick-600 text-white hover:bg-clay-700 active:scale-[0.98]',
}

const sizes: Record<string, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2.5 text-sm',
  lg: 'px-6 py-3 text-base',
}

const classes = computed(() => [
  base,
  variants[props.variant],
  sizes[props.size],
  props.block ? 'w-full' : '',
])
</script>

<template>
  <button :type="type" :disabled="disabled" :class="classes">
    <slot />
  </button>
</template>
