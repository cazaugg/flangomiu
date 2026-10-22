<script setup lang="ts">
export interface SegmentOption {
  value: string
  label: string
}

defineProps<{ modelValue: string; options: SegmentOption[] }>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()
</script>

<template>
  <div class="inline-flex rounded-full border border-sand-200 bg-white p-1">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      class="rounded-full px-3.5 py-1.5 text-sm font-medium transition"
      :class="
        modelValue === option.value
          ? 'bg-flamingo-500 text-white shadow-sm'
          : 'text-stone-500 hover:text-clay-700'
      "
      @click="emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>
