<script setup lang="ts">
import { useId } from 'vue'

const model = defineModel<string | number | null>()
withDefaults(defineProps<{ name?: string; type?: string; placeholder?: string; disabled?: boolean }>(), {
  name: '',
  type: 'text',
  placeholder: '',
  disabled: false,
})

const uid = useId()
</script>

<template>
  <input
    v-model="model"
    :id="uid"
    :name="name || uid"
    :type="type"
    :placeholder="placeholder"
    :disabled="disabled"
    class="w-full rounded-2xl border border-sand-200 bg-white px-4 py-2.5 text-sm text-stone-900 shadow-sm transition placeholder:text-stone-400 focus:border-flamingo-400 focus:outline-none focus:ring-4 focus:ring-flamingo-400/15 disabled:opacity-60"
  />
</template>
