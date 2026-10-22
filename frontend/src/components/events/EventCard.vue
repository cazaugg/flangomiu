<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import KindBadge from '@/components/ui/KindBadge.vue'
import BaseAvatar from '@/components/ui/BaseAvatar.vue'
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import { formatRange } from '@/lib/date'
import { kindMeta } from '@/lib/kinds'
import type { EventItem } from '@/types'

const props = withDefaults(defineProps<{ event: EventItem; showActions?: boolean }>(), {
  showActions: false,
})
const emit = defineEmits<{ edit: [EventItem]; remove: [EventItem] }>()

const router = useRouter()
const meta = computed(() => kindMeta(props.event.kind))
const when = computed(() => formatRange(props.event.start, props.event.stop, props.event.all_day))

function open() {
  router.push({ name: 'event-detail', params: { id: props.event.id } })
}
</script>

<template>
  <article
    class="surface-card group relative cursor-pointer overflow-hidden rounded-3xl shadow-[0_18px_50px_-32px_rgba(140,59,46,0.5)] transition hover:-translate-y-0.5"
    @click="open"
  >
    <span class="absolute inset-y-0 left-0 z-10 w-1.5" :style="{ backgroundColor: meta.color }" />

    <div v-if="event.cover" class="relative">
      <img :src="event.cover.thumb" :alt="event.title" class="h-40 w-full object-cover" />
      <span
        v-if="event.picture_count > 1"
        class="absolute bottom-2 right-2 rounded-full bg-stone-900/60 px-2 py-0.5 text-[11px] font-medium text-white"
      >
        📷 {{ event.picture_count }}
      </span>
    </div>

    <div class="p-5">
      <div class="flex items-start justify-between gap-4">
        <div class="min-w-0">
          <div class="mb-2 flex flex-wrap items-center gap-2">
            <KindBadge :kind="event.kind" />
            <span v-if="event.is_done" class="text-xs font-medium text-stone-400">
              abgeschlossen
            </span>
          </div>
          <h3 class="truncate font-display text-lg font-semibold text-clay-700">{{ event.title }}</h3>
          <p class="mt-1 text-sm text-stone-500">{{ when }}</p>
          <p v-if="event.location" class="mt-0.5 flex items-center gap-1 text-sm text-stone-400">
            <span>📍</span>{{ event.location }}
          </p>
          <p v-if="event.description" class="mt-2 line-clamp-2 text-sm text-stone-500">
            {{ event.description }}
          </p>
        </div>
        <div v-if="showActions" class="flex shrink-0 items-center gap-1">
          <BaseIconButton label="Bearbeiten" @click.stop="emit('edit', event)">✎</BaseIconButton>
          <BaseIconButton label="Löschen" @click.stop="emit('remove', event)">🗑</BaseIconButton>
        </div>
      </div>

      <div v-if="event.people.length" class="mt-4 flex items-center gap-2">
        <div class="flex -space-x-2">
          <BaseAvatar
            v-for="person in event.people.slice(0, 5)"
            :key="person.id"
            :name="person.name"
            :src="person.picture?.url"
            size="sm"
          />
        </div>
        <span class="text-xs text-stone-400">
          {{ event.people.map((person) => person.name).join(', ') }}
        </span>
      </div>
    </div>
  </article>
</template>
