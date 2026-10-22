<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps<{ busy?: boolean }>()
const emit = defineEmits<{ files: [File[]] }>()

const { t } = useI18n()
const input = ref<HTMLInputElement | null>(null)
const dragging = ref(false)

function pick() {
  input.value?.click()
}

function handle(list: FileList | null) {
  const files = Array.from(list ?? []).filter((file) => file.type.startsWith('image/'))
  if (files.length) emit('files', files)
}

function onChange(event: Event) {
  const element = event.target as HTMLInputElement
  handle(element.files)
  element.value = ''
}

function onDrop(event: DragEvent) {
  dragging.value = false
  handle(event.dataTransfer?.files ?? null)
}
</script>

<template>
  <div
    class="rounded-2xl border border-dashed p-4 text-center transition"
    :class="dragging ? 'border-flamingo-400 bg-flamingo-50' : 'border-sand-300 bg-white/60'"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="onDrop"
  >
    <input
      ref="input"
      name="images"
      class="hidden"
      type="file"
      accept="image/*"
      multiple
      @change="onChange"
    />
    <p class="text-sm text-stone-500">
      {{ props.busy ? t('images.uploading') : t('images.drop') }}
      <button
        type="button"
        class="font-medium text-flamingo-600 hover:underline disabled:opacity-50"
        :disabled="props.busy"
        @click="pick"
      >
        {{ t('images.choose') }}
      </button>
    </p>
  </div>
</template>
