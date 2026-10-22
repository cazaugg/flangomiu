<script setup lang="ts">
import { computed } from 'vue'
import { format, parseISO } from 'date-fns'
import { de } from 'date-fns/locale'
import { useI18n } from 'vue-i18n'

import type { PinItem } from '@/types'

const props = defineProps<{ pin: PinItem; canEdit?: boolean }>()
const emit = defineEmits<{
  edit: [PinItem]
  remove: [PinItem]
  tag: [string]
  image: [PinItem]
}>()

const { t } = useI18n()

const accents = ['bg-flamingo-50', 'bg-sand-100', 'bg-white', 'bg-[#fdf2e5]']
const tilts = ['-rotate-[0.4deg]', 'rotate-[0.35deg]', 'rotate-0', 'rotate-[0.2deg]']

const accent = computed(() => accents[props.pin.id % accents.length])
const tilt = computed(() => tilts[props.pin.id % tilts.length])
const longText = computed(() => props.pin.text.length > 180)

const created = computed(() => {
  if (!props.pin.created_at) return ''
  try {
    return format(parseISO(props.pin.created_at), 'd. MMM yyyy', { locale: de })
  } catch {
    return ''
  }
})
</script>

<template>
  <article
    class="group relative mb-4 break-inside-avoid rounded-3xl border border-sand-200 p-5 shadow-[0_16px_40px_-28px_rgba(140,59,46,0.55)] transition duration-300 hover:rotate-0 hover:shadow-[0_22px_50px_-26px_rgba(140,59,46,0.6)]"
    :class="[accent, tilt]"
  >
    <p
      v-if="pin.text"
      class="whitespace-pre-line font-display text-clay-700"
      :class="longText ? 'text-base leading-relaxed' : 'text-lg leading-snug'"
    >
      {{ pin.text }}
    </p>
    <p v-if="pin.author" class="mt-2 text-sm italic text-stone-500">— {{ pin.author }}</p>

    <button
      v-if="pin.image"
      type="button"
      class="mt-3 block w-full cursor-zoom-in overflow-hidden rounded-2xl border border-sand-200/80"
      @click="emit('image', pin)"
    >
      <img
        :src="pin.image.thumb"
        :alt="pin.text || pin.image.name"
        class="max-h-80 w-full object-cover transition duration-500 hover:scale-[1.02]"
      />
    </button>

    <div v-if="pin.tags.length" class="mt-4 flex flex-wrap gap-1.5">
      <button
        v-for="tag in pin.tags"
        :key="tag.id"
        type="button"
        class="rounded-full bg-white/70 px-2.5 py-1 text-xs font-medium text-clay-700 transition hover:bg-flamingo-100 hover:text-flamingo-700"
        @click="emit('tag', tag.name)"
      >
        #{{ tag.name }}
      </button>
    </div>

    <footer class="mt-4 flex items-center justify-between gap-2 border-t border-sand-200/70 pt-3">
      <p class="min-w-0 truncate text-[11px] text-stone-400">
        {{ t('pinboard.pinnedBy', { name: pin.user?.name ?? '?' }) }}
        <span v-if="created"> · {{ created }}</span>
      </p>
      <div v-if="canEdit" class="flex shrink-0 gap-1">
        <button
          type="button"
          class="grid h-7 w-7 place-items-center rounded-full text-xs text-stone-400 transition hover:bg-white/80 hover:text-clay-700"
          :title="t('common.edit')"
          @click="emit('edit', pin)"
        >
          ✎
        </button>
        <button
          type="button"
          class="grid h-7 w-7 place-items-center rounded-full text-xs text-stone-400 transition hover:bg-white/80 hover:text-flamingo-700"
          :title="t('common.delete')"
          @click="emit('remove', pin)"
        >
          🗑
        </button>
      </div>
    </footer>
  </article>
</template>
