<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import MarkdownView from './MarkdownView.vue'
import SegmentedControl from '@/components/ui/SegmentedControl.vue'
import { picturesApi } from '@/api'
import { useUiStore } from '@/stores/ui'

const model = defineModel<string>({ default: '' })

const { t } = useI18n()
const ui = useUiStore()

const textarea = ref<HTMLTextAreaElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const mode = ref('write')
const uploading = ref(false)

const modeOptions = computed(() => [
  { value: 'write', label: t('knowledge.write') },
  { value: 'preview', label: t('knowledge.preview') },
])

const toolbarClass =
  'grid h-8 min-w-8 place-items-center rounded-lg px-2 text-sm text-stone-600 transition hover:bg-sand-200 disabled:opacity-50'

let savedRange = { start: 0, end: 0 }

function currentRange() {
  const element = textarea.value
  if (!element) return { start: model.value.length, end: model.value.length }
  return { start: element.selectionStart, end: element.selectionEnd }
}

function insertAt(start: number, end: number, text: string) {
  model.value = model.value.slice(0, start) + text + model.value.slice(end)
  requestAnimationFrame(() => {
    const element = textarea.value
    if (!element) return
    element.focus()
    const position = start + text.length
    element.setSelectionRange(position, position)
  })
}

function insert(before: string, after = '', placeholder = '') {
  const { start, end } = currentRange()
  const selected = model.value.slice(start, end) || placeholder
  insertAt(start, end, before + selected + after)
}

function openImagePicker() {
  savedRange = currentRange()
  fileInput.value?.click()
}

async function onFile(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  uploading.value = true
  try {
    const { picture } = await picturesApi.upload(file)
    insertAt(savedRange.start, savedRange.end, `![${picture.name}](${picture.url})\n`)
  } catch (error) {
    ui.error((error as Error).message)
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="overflow-hidden rounded-2xl border border-sand-200 bg-white">
    <div
      class="flex flex-wrap items-center justify-between gap-2 border-b border-sand-200 bg-sand-50 px-2 py-1.5"
    >
      <div class="flex flex-wrap items-center gap-0.5">
        <button type="button" :class="toolbarClass" :title="t('knowledge.editor.heading')" @click="insert('## ', '', 'Überschrift')">
          H
        </button>
        <button type="button" :class="toolbarClass" :title="t('knowledge.editor.bold')" @click="insert('**', '**', 'fett')">
          <strong>B</strong>
        </button>
        <button type="button" :class="toolbarClass" :title="t('knowledge.editor.italic')" @click="insert('*', '*', 'kursiv')">
          <em>I</em>
        </button>
        <button type="button" :class="toolbarClass" :title="t('knowledge.editor.list')" @click="insert('- ', '', 'Punkt')">
          •
        </button>
        <button type="button" :class="toolbarClass" :title="t('knowledge.editor.code')" @click="insert('```\n', '\n```', 'code')">
          &lt;/&gt;
        </button>
        <button type="button" :class="toolbarClass" :title="t('knowledge.editor.link')" @click="insert('[', '](https://)', 'Linktext')">
          🔗
        </button>
        <button
          type="button"
          :class="toolbarClass"
          :title="t('knowledge.editor.image')"
          :disabled="uploading"
          @click="openImagePicker"
        >
          {{ uploading ? '…' : '🖼️' }}
        </button>
      </div>

      <div class="md:hidden">
        <SegmentedControl v-model="mode" :options="modeOptions" />
      </div>
    </div>

    <div class="grid md:grid-cols-2">
      <div :class="mode === 'preview' ? 'hidden md:block' : 'block'">
        <textarea
          ref="textarea"
          v-model="model"
          rows="22"
          spellcheck="true"
          placeholder="Markdown …"
          class="h-full min-h-[22rem] w-full resize-none border-0 bg-white p-4 font-mono text-sm leading-relaxed text-stone-800 focus:outline-none"
        />
      </div>
      <div
        :class="mode === 'write' ? 'hidden md:block' : 'block'"
        class="min-h-[22rem] border-t border-sand-200 bg-sand-50/50 p-4 md:border-l md:border-t-0"
      >
        <MarkdownView :content="model" />
      </div>
    </div>

    <input
      ref="fileInput"
      name="knowledge-image"
      class="hidden"
      type="file"
      accept="image/*"
      @change="onFile"
    />
  </div>
</template>
