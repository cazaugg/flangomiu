<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'

import type { Picture } from '@/types'

const props = defineProps<{ pictures: Picture[] }>()
const open = defineModel<boolean>('open', { required: true })
const index = defineModel<number>('index', { required: true })

const current = computed(() => props.pictures[Math.min(index.value, props.pictures.length - 1)])

function close() {
  open.value = false
}

function step(delta: number) {
  const count = props.pictures.length
  if (!count) return
  index.value = (index.value + delta + count) % count
}

function onKey(event: KeyboardEvent) {
  if (!open.value) return
  if (event.key === 'Escape') close()
  else if (event.key === 'ArrowRight') step(1)
  else if (event.key === 'ArrowLeft') step(-1)
}

onMounted(() => window.addEventListener('keydown', onKey))
onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="open && current"
        class="fixed inset-0 z-[70] flex flex-col bg-stone-900/92 backdrop-blur"
      >
        <div class="flex items-center justify-between px-5 py-4 text-white/80">
          <span class="text-sm">{{ index + 1 }} / {{ pictures.length }}</span>
          <button
            class="grid h-9 w-9 place-items-center rounded-full transition hover:bg-white/10"
            aria-label="Schliessen"
            @click="close"
          >
            ✕
          </button>
        </div>
        <div class="relative flex flex-1 items-center justify-center px-4" @click.self="close">
          <button
            class="absolute left-3 grid h-11 w-11 place-items-center rounded-full bg-white/10 text-2xl text-white transition hover:bg-white/20 sm:left-6"
            aria-label="Zurück"
            @click="step(-1)"
          >
            ‹
          </button>
          <img
            :src="current.url"
            :alt="current.description || current.name"
            class="max-h-[74vh] max-w-full rounded-2xl object-contain shadow-2xl"
          />
          <button
            class="absolute right-3 grid h-11 w-11 place-items-center rounded-full bg-white/10 text-2xl text-white transition hover:bg-white/20 sm:right-6"
            aria-label="Weiter"
            @click="step(1)"
          >
            ›
          </button>
        </div>
        <p v-if="current.description" class="px-8 pb-8 text-center text-sm text-white/85">
          {{ current.description }}
        </p>
      </div>
    </Transition>
  </Teleport>
</template>
