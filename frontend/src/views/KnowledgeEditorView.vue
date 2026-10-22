<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import MarkdownEditor from '@/components/knowledge/MarkdownEditor.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseField from '@/components/ui/BaseField.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import { useKnowledgeStore } from '@/stores/knowledge'
import { useUiStore } from '@/stores/ui'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const knowledge = useKnowledgeStore()
const ui = useUiStore()

const isEdit = computed(() => route.name === 'knowledge-edit')
const entryId = computed(() => Number(route.params.id))
const loading = ref(true)
const saving = ref(false)

const form = ref({ title: '', subject_id: '', content: '' })

const subjectOptions = computed(() =>
  knowledge.subjects.map((subject) => ({ value: String(subject.id), label: subject.name })),
)

onMounted(async () => {
  await knowledge.fetchSubjects()

  if (isEdit.value) {
    await knowledge.fetchEntry(entryId.value)
    if (knowledge.entry) {
      form.value = {
        title: knowledge.entry.title,
        subject_id: String(knowledge.entry.subject_id),
        content: knowledge.entry.content ?? '',
      }
    }
  } else {
    const requested = String(route.query.subject ?? '')
    form.value.subject_id = requested || String(knowledge.subjects[0]?.id ?? '')
  }

  loading.value = false
})

async function save() {
  if (!form.value.title.trim()) {
    ui.error(t('knowledge.titleRequired'))
    return
  }
  const subjectId = Number(form.value.subject_id)
  if (!subjectId) return

  saving.value = true
  try {
    const payload = {
      title: form.value.title.trim(),
      subject_id: subjectId,
      content: form.value.content,
    }
    const entry = isEdit.value
      ? await knowledge.updateEntry(entryId.value, payload)
      : await knowledge.createEntry(payload)
    ui.success('Gespeichert.')
    router.push({ name: 'knowledge-entry', params: { id: entry.id } })
  } catch (error) {
    ui.error((error as Error).message)
  } finally {
    saving.value = false
  }
}

function cancel() {
  router.back()
}
</script>

<template>
  <div class="space-y-6">
    <button
      type="button"
      class="inline-flex items-center gap-1 text-sm text-stone-500 transition hover:text-clay-700"
      @click="cancel"
    >
      ‹ {{ t('common.cancel') }}
    </button>

    <div v-if="loading" class="flex justify-center py-16"><BaseSpinner /></div>

    <BaseCard v-else>
      <h1 class="mb-5 font-display text-2xl font-semibold text-clay-700">
        {{ isEdit ? t('knowledge.editEntry') : t('knowledge.newEntry') }}
      </h1>

      <form class="space-y-4" @submit.prevent="save">
        <BaseField :label="t('knowledge.entryTitle')">
          <BaseInput v-model="form.title" :placeholder="t('knowledge.entryTitlePlaceholder')" />
        </BaseField>

        <BaseField :label="t('knowledge.subject')">
          <BaseSelect v-model="form.subject_id" :options="subjectOptions" />
        </BaseField>

        <BaseField :label="t('knowledge.content')">
          <MarkdownEditor v-model="form.content" />
        </BaseField>

        <div class="flex justify-end gap-2">
          <BaseButton variant="ghost" @click="cancel">{{ t('common.cancel') }}</BaseButton>
          <BaseButton type="submit" :disabled="saving || !form.title.trim() || !form.subject_id">
            {{ t('common.save') }}
          </BaseButton>
        </div>
      </form>
    </BaseCard>
  </div>
</template>
