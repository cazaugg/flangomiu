<script setup lang="ts">
import { formatDate } from '@/lib/date'
import type { KnowledgeEntry } from '@/types'

defineProps<{ entry: KnowledgeEntry }>()
const emit = defineEmits<{ open: [KnowledgeEntry] }>()
</script>

<template>
  <article
    class="surface-card cursor-pointer rounded-2xl p-4 transition hover:-translate-y-0.5"
    @click="emit('open', entry)"
  >
    <div class="flex items-start justify-between gap-3">
      <h3 class="font-display text-base font-semibold text-clay-700">{{ entry.title }}</h3>
      <span
        v-if="entry.subject_name"
        class="shrink-0 rounded-full bg-sand-100 px-2 py-0.5 text-[11px] text-stone-500"
      >
        {{ entry.subject_name }}
      </span>
    </div>
    <p v-if="entry.excerpt" class="mt-1 line-clamp-2 text-sm text-stone-500">{{ entry.excerpt }}</p>
    <p class="mt-2 text-xs text-stone-400">Aktualisiert {{ formatDate(entry.updated_at) }}</p>
  </article>
</template>
