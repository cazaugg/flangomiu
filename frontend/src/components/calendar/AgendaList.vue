<script setup lang="ts">
import { computed } from 'vue'
import { format } from 'date-fns'
import { de } from 'date-fns/locale'

import { formatRange, toDate } from '@/lib/date'
import { kindMeta } from '@/lib/kinds'
import type { EventItem } from '@/types'

const props = defineProps<{ items: EventItem[] }>()
const emit = defineEmits<{ selectItem: [EventItem] }>()

const groups = computed(() => {
  const map = new Map<string, { date: Date; items: EventItem[] }>()
  for (const item of props.items) {
    const date = toDate(item.start)
    const key = date ? format(date, 'yyyy-MM-dd') : 'none'
    if (!map.has(key)) map.set(key, { date: date ?? new Date(8640000000000), items: [] })
    map.get(key)!.items.push(item)
  }
  return [...map.values()].sort((a, b) => a.date.getTime() - b.date.getTime())
})
</script>

<template>
  <div class="space-y-6">
    <section v-for="group in groups" :key="group.date.toISOString()">
      <h3 class="mb-2 font-display text-sm font-semibold uppercase tracking-wide text-stone-400">
        {{ format(group.date, 'EEEE, d. MMMM', { locale: de }) }}
      </h3>
      <div class="space-y-2">
        <button
          v-for="item in group.items"
          :key="item.id"
          type="button"
          class="surface-card flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left transition hover:-translate-y-0.5"
          @click="emit('selectItem', item)"
        >
          <span
            class="h-8 w-1.5 shrink-0 rounded-full"
            :style="{ backgroundColor: kindMeta(item.kind).color }"
          />
          <div class="min-w-0 flex-1">
            <p class="truncate text-sm font-medium text-stone-900">{{ item.title }}</p>
            <p class="truncate text-xs text-stone-400">
              {{ formatRange(item.start, item.stop, item.all_day) }}
              <span v-if="item.location"> · {{ item.location }}</span>
            </p>
          </div>
          <span
            class="shrink-0 rounded-full px-2 py-0.5 text-[11px] font-medium"
            :style="{ backgroundColor: kindMeta(item.kind).soft, color: kindMeta(item.kind).color }"
          >
            {{ kindMeta(item.kind).label }}
          </span>
        </button>
      </div>
    </section>
  </div>
</template>
