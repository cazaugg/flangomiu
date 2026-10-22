<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps<{ suggestions?: string[]; placeholder?: string }>()
const tags = defineModel<string[]>({ required: true })

const { t } = useI18n()
const draft = ref('')

const available = computed(() =>
  (props.suggestions ?? [])
    .filter((name) => !tags.value.some((tag) => tag.toLowerCase() === name.toLowerCase()))
    .slice(0, 12),
)

function add(value: string) {
  const name = value.replace(/\s+/g, ' ').trim().slice(0, 60).trim()
  if (!name) return
  if (tags.value.some((tag) => tag.toLowerCase() === name.toLowerCase())) return
  tags.value = [...tags.value, name]
}

function commit() {
  add(draft.value)
  draft.value = ''
}

function remove(index: number) {
  tags.value = tags.value.filter((_, position) => position !== index)
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter' || event.key === ',') {
    event.preventDefault()
    commit()
  } else if (event.key === 'Backspace' && !draft.value && tags.value.length) {
    tags.value = tags.value.slice(0, -1)
  }
}
</script>

<template>
  <div class="space-y-2">
    <div
      class="flex flex-wrap items-center gap-1.5 rounded-2xl border border-sand-200 bg-white px-2.5 py-2 shadow-sm transition focus-within:border-flamingo-400 focus-within:ring-4 focus-within:ring-flamingo-400/15"
    >
      <span
        v-for="(tag, index) in tags"
        :key="tag"
        class="inline-flex items-center gap-1 rounded-full bg-flamingo-100 px-2.5 py-1 text-xs font-medium text-flamingo-700"
      >
        {{ tag }}
        <button
          type="button"
          class="grid h-4 w-4 place-items-center rounded-full text-flamingo-600 transition hover:bg-flamingo-200"
          :aria-label="`${tag} entfernen`"
          @click="remove(index)"
        >
          ✕
        </button>
      </span>
      <input
        v-model="draft"
        type="text"
        class="min-w-32 flex-1 border-0 bg-transparent px-1 py-1 text-sm text-stone-900 placeholder:text-stone-400 focus:outline-none"
        :placeholder="tags.length ? '' : (placeholder ?? t('pinboard.tagPlaceholder'))"
        @keydown="onKeydown"
        @blur="commit"
      />
    </div>
    <div v-if="available.length" class="flex flex-wrap gap-1.5">
      <button
        v-for="name in available"
        :key="name"
        type="button"
        class="rounded-full border border-dashed border-sand-300 px-2.5 py-1 text-xs text-stone-500 transition hover:border-flamingo-300 hover:text-flamingo-700"
        @click="add(name)"
      >
        ＋ {{ name }}
      </button>
    </div>
  </div>
</template>
