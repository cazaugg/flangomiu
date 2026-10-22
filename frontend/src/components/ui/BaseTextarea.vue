<script setup lang="ts">
import { useId } from 'vue'

const model = defineModel<string>()
withDefaults(defineProps<{ name?: string; rows?: number; placeholder?: string }>(), {
  name: '',
  rows: 3,
  placeholder: '',
})

const uid = useId()
</script>

<template>
  <textarea
    v-model="model"
    :id="uid"
    :name="name || uid"
    :rows="rows"
    :placeholder="placeholder"
    class="w-full resize-none rounded-2xl border border-sand-200 bg-white px-4 py-2.5 text-sm text-stone-900 shadow-sm transition placeholder:text-stone-400 focus:border-flamingo-400 focus:outline-none focus:ring-4 focus:ring-flamingo-400/15"
  />
</template>
