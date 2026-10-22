<script setup lang="ts">
import { computed } from 'vue'
import { format } from 'date-fns'
import { de } from 'date-fns/locale'

import KindBadge from '@/components/ui/KindBadge.vue'
import { formatRange, toDate } from '@/lib/date'
import { kindMeta } from '@/lib/kinds'
import type { EventItem } from '@/types'

const props = defineProps<{ event: EventItem }>()
const emit = defineEmits<{ open: [EventItem] }>()

const date = computed(() => toDate(props.event.start))
const meta = computed(() => kindMeta(props.event.kind))
const strip = computed(() => props.event.pictures.slice(0, 4))
</script>

<template>
  <article
    class="surface-card flex cursor-pointer gap-4 rounded-3xl p-4 shadow-[0_18px_50px_-34px_rgba(140,59,46,0.5)] transition hover:-translate-y-0.5"
    @click="emit('open', event)"
  >
    <div
      class="flex w-14 shrink-0 flex-col items-center justify-start rounded-2xl py-2"
      :style="{ backgroundColor: meta.soft }"
    >
      <span class="font-display text-2xl font-semibold leading-none" :style="{ color: meta.color }">
        {{ date ? format(date, 'd') : '–' }}
      </span>
      <span class="mt-0.5 text-xs" :style="{ color: meta.color }">
        {{ date ? format(date, 'MMM', { locale: de }) : '' }}
      </span>
    </div>

    <div class="min-w-0 flex-1">
      <div class="mb-1.5 flex flex-wrap items-center gap-2">
        <KindBadge :kind="event.kind" />
        <span class="text-xs text-stone-400">
          {{ formatRange(event.start, event.stop, event.all_day) }}
        </span>
      </div>
      <h3 class="truncate font-display text-lg font-semibold text-clay-700">{{ event.title }}</h3>
      <p v-if="event.location" class="text-sm text-stone-400">📍 {{ event.location }}</p>
      <p v-if="event.description" class="mt-1 line-clamp-2 text-sm text-stone-500">
        {{ event.description }}
      </p>

      <div v-if="strip.length" class="mt-3 flex items-center gap-2">
        <img
          v-for="picture in strip"
          :key="picture.id"
          :src="picture.thumb"
          :alt="picture.description || picture.name"
          class="h-12 w-12 rounded-xl object-cover"
        />
        <span v-if="event.picture_count > strip.length" class="text-xs text-stone-400">
          +{{ event.picture_count - strip.length }}
        </span>
      </div>
    </div>
  </article>
</template>
