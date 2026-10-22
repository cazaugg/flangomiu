<script setup lang="ts">
import type { Subject } from '@/types'

defineProps<{ subject: Subject }>()
const emit = defineEmits<{ open: [Subject] }>()
</script>

<template>
  <article
    class="surface-card cursor-pointer rounded-3xl p-5 transition hover:-translate-y-0.5"
    @click="emit('open', subject)"
  >
    <div class="flex items-start gap-3">
      <span class="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-flamingo-100 text-xl">
        📚
      </span>
      <div class="min-w-0 flex-1">
        <h3 class="truncate font-display text-lg font-semibold text-clay-700">{{ subject.name }}</h3>
        <p class="text-xs text-stone-400">
          {{ subject.entry_count }} {{ subject.entry_count === 1 ? 'Beitrag' : 'Beiträge' }}
        </p>
      </div>
      <span class="text-stone-300">›</span>
    </div>
    <p v-if="subject.description" class="mt-3 line-clamp-2 text-sm text-stone-500">
      {{ subject.description }}
    </p>
  </article>
</template>
