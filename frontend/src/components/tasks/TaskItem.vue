<script setup lang="ts">
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import { formatDateTime } from '@/lib/date'
import type { EventItem } from '@/types'

const props = defineProps<{ task: EventItem; showActions?: boolean }>()
const emit = defineEmits<{ edit: [EventItem]; remove: [EventItem] }>()

const accent = '#A8432F'
</script>

<template>
  <div
    class="surface-card flex items-center gap-4 rounded-2xl px-4 py-3 shadow-[0_14px_40px_-34px_rgba(140,59,46,0.6)] transition hover:-translate-y-0.5"
    :class="{ 'opacity-60': task.is_done }"
  >
    <span
      class="grid h-7 w-7 shrink-0 place-items-center rounded-full border-2 text-sm"
      :style="{
        borderColor: task.is_done ? '#cbd5c0' : accent,
        color: task.is_done ? '#8d7a72' : accent,
        backgroundColor: task.is_done ? '#eef0ea' : '#F0DAD3',
      }"
    >
      {{ task.is_done ? '✓' : '•' }}
    </span>
    <div class="min-w-0 flex-1">
      <p class="truncate text-sm font-medium" :class="task.is_done ? 'text-stone-400 line-through' : 'text-stone-900'">
        {{ task.title }}
      </p>
      <p v-if="task.stop" class="text-xs text-stone-400">
        {{ task.is_done ? 'Erledigt' : 'Fällig' }} · {{ formatDateTime(task.stop) }}
      </p>
    </div>
    <div v-if="task.people.length" class="hidden shrink-0 text-xs text-stone-400 sm:block">
      {{ task.people.map((person) => person.name).join(', ') }}
    </div>
    <div v-if="showActions" class="flex shrink-0 items-center gap-1">
      <BaseIconButton label="Bearbeiten" @click="emit('edit', task)">✎</BaseIconButton>
      <BaseIconButton label="Löschen" @click="emit('remove', task)">🗑</BaseIconButton>
    </div>
  </div>
</template>
