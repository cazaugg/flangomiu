<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

import ImageLightbox from './ImageLightbox.vue'
import type { Picture } from '@/types'

const props = withDefaults(
  defineProps<{ pictures: Picture[]; editable?: boolean; coverId?: number | null }>(),
  { editable: false, coverId: null },
)

const emit = defineEmits<{
  remove: [Picture]
  reorder: [number[]]
  cover: [Picture]
  caption: [Picture, string]
}>()

const { t } = useI18n()
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)
const dragIndex = ref<number | null>(null)

function openAt(index: number) {
  lightboxIndex.value = index
  lightboxOpen.value = true
}

function onCaption(picture: Picture, event: Event) {
  emit('caption', picture, (event.target as HTMLInputElement).value)
}

function onDragStart(index: number) {
  dragIndex.value = index
}

function onDrop(index: number) {
  if (dragIndex.value === null || dragIndex.value === index) return
  const order = [...props.pictures]
  const [moved] = order.splice(dragIndex.value, 1)
  order.splice(index, 0, moved)
  dragIndex.value = null
  emit('reorder', order.map((picture) => picture.id))
}
</script>

<template>
  <div>
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
      <figure
        v-for="(picture, index) in pictures"
        :key="picture.id"
        class="group relative overflow-hidden rounded-2xl border border-sand-200 bg-white"
        :draggable="editable"
        @dragstart="onDragStart(index)"
        @dragover.prevent
        @drop="onDrop(index)"
      >
        <img
          :src="picture.thumb"
          :alt="picture.description || picture.name"
          class="h-36 w-full cursor-zoom-in object-cover"
          @click="openAt(index)"
        />

        <span
          v-if="editable && coverId === picture.id"
          class="absolute left-2 top-2 rounded-full bg-clay-700/90 px-2 py-0.5 text-[10px] font-medium text-white"
        >
          {{ t('images.cover') }}
        </span>

        <div
          v-if="editable"
          class="absolute right-2 top-2 flex gap-1 opacity-0 transition group-hover:opacity-100"
        >
          <button
            type="button"
            class="grid h-7 w-7 place-items-center rounded-full bg-white/90 text-xs shadow"
            :title="t('images.setCover')"
            @click.stop="emit('cover', picture)"
          >
            ★
          </button>
          <button
            type="button"
            class="grid h-7 w-7 place-items-center rounded-full bg-white/90 text-xs shadow"
            :title="t('images.remove')"
            @click.stop="emit('remove', picture)"
          >
            🗑
          </button>
        </div>

        <figcaption class="p-2">
          <input
            v-if="editable"
            class="w-full rounded-xl border border-sand-200 bg-sand-50 px-2.5 py-1.5 text-xs text-stone-700 focus:border-flamingo-400 focus:outline-none focus:ring-2 focus:ring-flamingo-400/15"
            :name="`caption-${picture.id}`"
            :value="picture.description"
            :placeholder="t('images.captionPlaceholder')"
            :aria-label="t('images.caption')"
            @click.stop
            @change="onCaption(picture, $event)"
          />
          <p v-else class="px-1 text-xs text-stone-500">
            {{ picture.description || picture.name }}
          </p>
        </figcaption>
      </figure>
    </div>

    <ImageLightbox
      v-model:open="lightboxOpen"
      v-model:index="lightboxIndex"
      :pictures="pictures"
    />
  </div>
</template>
