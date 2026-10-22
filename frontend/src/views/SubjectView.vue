<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import EntryCard from '@/components/knowledge/EntryCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BaseField from '@/components/ui/BaseField.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import BaseTextarea from '@/components/ui/BaseTextarea.vue'
import { useAuthStore } from '@/stores/auth'
import { useKnowledgeStore } from '@/stores/knowledge'
import { useUiStore } from '@/stores/ui'
import type { KnowledgeEntry } from '@/types'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const knowledge = useKnowledgeStore()
const ui = useUiStore()

const subjectId = computed(() => Number(route.params.id))
const loading = ref(true)
const editOpen = ref(false)
const form = ref({ name: '', description: '' })

async function load() {
  loading.value = true
  await knowledge.fetchSubject(subjectId.value)
  loading.value = false
}

onMounted(load)
watch(subjectId, load)

const subject = computed(() => knowledge.subject)
const entries = computed(() => subject.value?.entries ?? [])

function openEdit() {
  if (!subject.value) return
  form.value = { name: subject.value.name, description: subject.value.description }
  editOpen.value = true
}

async function saveSubject() {
  if (!subject.value || !form.value.name.trim()) return
  try {
    await knowledge.updateSubject(subject.value.id, {
      name: form.value.name.trim(),
      description: form.value.description,
    })
    await knowledge.fetchSubject(subject.value.id)
    await knowledge.fetchSubjects()
    editOpen.value = false
    ui.success('Bereich aktualisiert.')
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function deleteSubject() {
  if (!subject.value) return
  if (!confirm(t('knowledge.deleteSubject'))) return
  try {
    await knowledge.removeSubject(subject.value.id)
    await knowledge.fetchSubjects()
    ui.success('Bereich gelöscht.')
    router.push({ name: 'knowledge' })
  } catch (error) {
    ui.error((error as Error).message)
  }
}

function newEntry() {
  router.push({ name: 'knowledge-new', query: { subject: String(subjectId.value) } })
}

function openEntry(entry: KnowledgeEntry) {
  router.push({ name: 'knowledge-entry', params: { id: entry.id } })
}
</script>

<template>
  <div class="space-y-6">
    <RouterLink
      :to="{ name: 'knowledge' }"
      class="inline-flex items-center gap-1 text-sm text-stone-500 transition hover:text-clay-700"
    >
      ‹ {{ t('detail.back') }}
    </RouterLink>

    <div v-if="loading" class="flex justify-center py-16"><BaseSpinner /></div>

    <BaseEmptyState v-else-if="!subject" icon="🔍" :title="t('knowledge.noResults')" />

    <template v-else>
      <BasePageHeader :title="subject.name" :subtitle="subject.description">
        <template v-if="auth.isWriter">
          <BaseButton variant="secondary" size="sm" @click="openEdit">
            ✎ {{ t('knowledge.editSubject') }}
          </BaseButton>
          <BaseButton variant="ghost" size="sm" @click="deleteSubject">🗑</BaseButton>
          <BaseButton @click="newEntry">＋ {{ t('knowledge.newEntry') }}</BaseButton>
        </template>
      </BasePageHeader>

      <p class="text-sm text-stone-400">
        {{ subject.entry_count }} {{ subject.entry_count === 1 ? 'Beitrag' : 'Beiträge' }}
      </p>

      <div v-if="entries.length" class="space-y-2">
        <EntryCard v-for="entry in entries" :key="entry.id" :entry="entry" @open="openEntry" />
      </div>
      <BaseEmptyState
        v-else
        icon="📝"
        :title="t('knowledge.noEntries')"
        :message="t('knowledge.emptyHint')"
      >
        <BaseButton v-if="auth.isWriter" @click="newEntry">
          ＋ {{ t('knowledge.newEntry') }}
        </BaseButton>
      </BaseEmptyState>

      <BaseModal :open="editOpen" :title="t('knowledge.editSubject')" @close="editOpen = false">
        <form class="space-y-4" @submit.prevent="saveSubject">
          <BaseField :label="t('knowledge.subjectName')">
            <BaseInput v-model="form.name" :placeholder="t('knowledge.subjectNamePlaceholder')" />
          </BaseField>
          <BaseField :label="t('knowledge.subjectDescription')">
            <BaseTextarea
              v-model="form.description"
              :placeholder="t('knowledge.subjectDescriptionPlaceholder')"
            />
          </BaseField>
          <div class="flex justify-end gap-2 pt-2">
            <BaseButton variant="ghost" @click="editOpen = false">
              {{ t('common.cancel') }}
            </BaseButton>
            <BaseButton type="submit" :disabled="!form.name.trim()">
              {{ t('common.save') }}
            </BaseButton>
          </div>
        </form>
      </BaseModal>
    </template>
  </div>
</template>
