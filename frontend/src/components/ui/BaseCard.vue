<script setup lang="ts">
withDefaults(defineProps<{ hoverable?: boolean; padded?: boolean }>(), {
  hoverable: false,
  padded: true,
})
</script>

<template>
  <div
    class="surface-card rounded-3xl shadow-[0_18px_50px_-30px_rgba(140,59,46,0.45)] transition"
    :class="[
      padded ? 'p-5' : '',
      hoverable ? 'hover:-translate-y-0.5 hover:shadow-[0_24px_60px_-30px_rgba(140,59,46,0.55)]' : '',
    ]"
  >
    <slot />
  </div>
</template>
