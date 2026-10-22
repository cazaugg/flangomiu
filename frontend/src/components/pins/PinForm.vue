<script setup lang="ts">
import { computed, onBeforeUnmount, reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'

import TagInput from './TagInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseField from '@/components/ui/BaseField.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseTextarea from '@/components/ui/BaseTextarea.vue'
import ImageUploader from '@/components/images/ImageUploader.vue'
import type { PinPayload } from '@/api'
import type { PinItem } from '@/types'

const props = defineProps<{
  open: boolean
  initial?: PinItem | null
  suggestions?: string[]
  title: string
  submitLabel?: string
}>()

const emit = defineEmits<{ close: []; submit: [PinPayload, File | null] }>()

const { t } = useI18n()

const form = reactive({
  author: '',
  text: '',
  tags: [] as string[],
  removeImage: false,
  file: null as File | null,
  preview: null as string | null,
})

let objectUrl: string | null = null

function clearPreview() {
  if (objectUrl) {
    URL.revokeObjectURL(objectUrl)
    objectUrl = null
  }
  form.preview = null
}

watch(
  () => [props.open, props.initial],
  () => {
    clearPreview()
    form.author = props.initial?.author ?? ''
    form.text = props.initial?.text ?? ''
    form.tags = props.initial?.tags.map((tag) => tag.name) ?? []
    form.removeImage = false
    form.file = null
  },
  { immediate: true },
)

onBeforeUnmount(clearPreview)

const currentImage = computed(() =>
  form.preview ?? (form.removeImage ? null : (props.initial?.image?.thumb ?? null)),
)
const hasImage = computed(() => Boolean(form.preview || (props.initial?.image && !form.removeImage)))
const canSubmit = computed(() => Boolean(form.text.trim() || hasImage.value))

function onFiles(files: File[]) {
  const file = files[0]
  if (!file) return
  clearPreview()
  objectUrl = URL.createObjectURL(file)
  form.preview = objectUrl
  form.file = file
  form.removeImage = false
}

function removeImage() {
  clearPreview()
  form.file = null
  form.removeImage = Boolean(props.initial?.image)
}

function submit() {
  if (!canSubmit.value) return
  emit(
    'submit',
    {
      author: form.author.trim(),
      text: form.text.trim(),
      tags: form.tags,
      remove_image: form.removeImage,
    },
    form.file,
  )
}
</script>

<template>
  <BaseModal :open="open" :title="title" @close="emit('close')">
    <form class="space-y-4" @submit.prevent="submit">
      <BaseField :label="t('pinboard.author')" :hint="t('pinboard.authorHint')">
        <BaseInput v-model="form.author" :placeholder="t('pinboard.authorPlaceholder')" />
      </BaseField>

      <BaseField :label="t('pinboard.text')" :hint="t('pinboard.textHint')">
        <BaseTextarea
          v-model="form.text"
          :rows="4"
          :placeholder="t('pinboard.textPlaceholder')"
        />
      </BaseField>

      <BaseField :label="t('pinboard.tags')" :hint="t('pinboard.tagsHint')">
        <TagInput v-model="form.tags" :suggestions="suggestions" />
      </BaseField>

      <BaseField :label="t('pinboard.image')" :hint="t('pinboard.imageHint')">
        <div v-if="currentImage" class="relative overflow-hidden rounded-2xl border border-sand-200">
          <img :src="currentImage" alt="" class="h-36 w-full object-cover" />
          <button
            type="button"
            class="absolute right-2 top-2 rounded-full bg-white/90 px-3 py-1 text-xs font-medium text-clay-700 shadow transition hover:bg-white"
            @click="removeImage"
          >
            {{ t('pinboard.removeImage') }}
          </button>
        </div>
        <ImageUploader v-else @files="onFiles" />
      </BaseField>

      <div class="flex justify-end gap-2 pt-2">
        <BaseButton variant="ghost" @click="emit('close')">{{ t('common.cancel') }}</BaseButton>
        <BaseButton type="submit" :disabled="!canSubmit">
          {{ submitLabel ?? t('common.save') }}
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>
