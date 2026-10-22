<script setup lang="ts">
import { computed } from 'vue'
import {
  addDays,
  endOfMonth,
  endOfWeek,
  format,
  isSameDay,
  isSameMonth,
  startOfMonth,
  startOfWeek,
} from 'date-fns'

import { toDate } from '@/lib/date'
import { kindMeta } from '@/lib/kinds'
import type { EventItem } from '@/types'

const props = defineProps<{ month: Date; items: EventItem[]; selectedDay?: string | null }>()
const emit = defineEmits<{ selectDay: [string]; selectItem: [EventItem] }>()

const weekdayLabels = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

const days = computed(() => {
  const gridStart = startOfWeek(startOfMonth(props.month), { weekStartsOn: 1 })
  const gridEnd = endOfWeek(endOfMonth(props.month), { weekStartsOn: 1 })
  const result: Date[] = []
  let cursor = gridStart
  while (cursor <= gridEnd) {
    result.push(cursor)
    cursor = addDays(cursor, 1)
  }
  return result
})

function itemsFor(day: Date): EventItem[] {
  return props.items.filter((item) => {
    const date = toDate(item.start)
    return date ? isSameDay(date, day) : false
  })
}

function dayKey(day: Date): string {
  return format(day, 'yyyy-MM-dd')
}
</script>

<template>
  <div>
    <div class="mb-2 grid grid-cols-7 gap-1.5 text-center text-xs font-medium text-stone-400">
      <div v-for="label in weekdayLabels" :key="label">{{ label }}</div>
    </div>
    <div class="grid grid-cols-7 gap-1.5">
      <button
        v-for="day in days"
        :key="dayKey(day)"
        type="button"
        class="flex min-h-[92px] flex-col gap-1 rounded-2xl border p-1.5 text-left transition"
        :class="[
          isSameMonth(day, month)
            ? 'border-sand-200 bg-white/80'
            : 'border-transparent bg-transparent text-stone-300',
          selectedDay === dayKey(day) ? 'ring-2 ring-flamingo-400' : 'hover:border-flamingo-200',
        ]"
        @click="emit('selectDay', dayKey(day))"
      >
        <span
          class="grid h-6 w-6 place-items-center rounded-full text-xs font-semibold"
          :class="
            isSameDay(day, new Date())
              ? 'bg-flamingo-500 text-white'
              : 'text-stone-500'
          "
        >
          {{ format(day, 'd') }}
        </span>
        <span
          v-for="item in itemsFor(day).slice(0, 3)"
          :key="item.id"
          class="flex items-center gap-1 truncate rounded-md px-1.5 py-0.5 text-[11px] font-medium"
          :style="{ backgroundColor: kindMeta(item.kind).soft, color: kindMeta(item.kind).color }"
          @click.stop="emit('selectItem', item)"
        >
          <span class="truncate">{{ item.title }}</span>
        </span>
        <span v-if="itemsFor(day).length > 3" class="px-1.5 text-[10px] text-stone-400">
          +{{ itemsFor(day).length - 3 }} mehr
        </span>
      </button>
    </div>
  </div>
</template>
