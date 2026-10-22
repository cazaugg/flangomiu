<script setup lang="ts">
import { useId } from 'vue'

export interface SelectOption {
  value: string
  label: string
}

const model = defineModel<string>()
defineProps<{ options: SelectOption[]; disabled?: boolean; name?: string }>()

const uid = useId()
</script>

<template>
  <div class="relative">
    <select
      v-model="model"
      :id="uid"
      :name="name || uid"
      :disabled="disabled"
      class="w-full appearance-none rounded-2xl border border-sand-200 bg-white px-4 py-2.5 pr-10 text-sm text-stone-900 shadow-sm transition focus:border-flamingo-400 focus:outline-none focus:ring-4 focus:ring-flamingo-400/15"
    >
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
    <span class="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-stone-400">▾</span>
  </div>
</template>
