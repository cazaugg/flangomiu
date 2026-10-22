<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

import EntryCard from '@/components/knowledge/EntryCard.vue'
import SubjectCard from '@/components/knowledge/SubjectCard.vue'
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
import type { KnowledgeEntry, Subject } from '@/types'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
const knowledge = useKnowledgeStore()
const ui = useUiStore()

const search = ref('')
const loaded = ref(false)
const subjectModal = ref(false)
const subjectForm = ref({ name: '', description: '' })

let timer: ReturnType<typeof setTimeout> | null = null

onMounted(async () => {
  await Promise.all([knowledge.fetchSubjects(), knowledge.fetchEntries()])
  loaded.value = true
})

const isSearching = computed(() => search.value.trim().length > 0)
const recent = computed(() => (isSearching.value ? [] : knowledge.entries.slice(0, 6)))

function onSearch() {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    const term = search.value.trim()
    knowledge.fetchEntries(term ? { q: term } : undefined)
  }, 300)
}

function openSubject(subject: Subject) {
  router.push({ name: 'knowledge-subject', params: { id: subject.id } })
}

function openEntry(entry: KnowledgeEntry) {
  router.push({ name: 'knowledge-entry', params: { id: entry.id } })
}

function openCreateSubject() {
  subjectForm.value = { name: '', description: '' }
  subjectModal.value = true
}

async function createSubject() {
  if (!subjectForm.value.name.trim()) return
  try {
    const subject = await knowledge.createSubject({
      name: subjectForm.value.name.trim(),
      description: subjectForm.value.description,
    })
    await knowledge.fetchSubjects()
    subjectModal.value = false
    ui.success('Bereich angelegt.')
    openSubject(subject)
  } catch (error) {
    ui.error((error as Error).message)
  }
}
</script>

<template>
  <div class="space-y-6">
    <BasePageHeader :title="t('knowledge.title')" :subtitle="t('knowledge.subtitle')">
      <BaseButton v-if="auth.isWriter" @click="openCreateSubject">
        ＋ {{ t('knowledge.newSubject') }}
      </BaseButton>
    </BasePageHeader>

    <BaseField>
      <BaseInput
        v-model="search"
        type="search"
        :placeholder="t('knowledge.searchPlaceholder')"
        @input="onSearch"
      />
    </BaseField>

    <div v-if="!loaded" class="flex justify-center py-12"><BaseSpinner /></div>

    <template v-else-if="isSearching">
      <div v-if="knowledge.entries.length" class="space-y-2">
        <EntryCard
          v-for="entry in knowledge.entries"
          :key="entry.id"
          :entry="entry"
          @open="openEntry"
        />
      </div>
      <BaseEmptyState
        v-else
        icon="🔍"
        :title="t('knowledge.noResults')"
        :message="t('knowledge.noResultsHint')"
      />
    </template>

    <template v-else>
      <section class="space-y-3">
        <h2 class="font-display text-xl font-semibold text-clay-700">{{ t('knowledge.subjects') }}</h2>
        <div v-if="knowledge.subjects.length" class="grid gap-3 sm:grid-cols-2">
          <SubjectCard
            v-for="subject in knowledge.subjects"
            :key="subject.id"
            :subject="subject"
            @open="openSubject"
          />
        </div>
        <BaseEmptyState
          v-else
          icon="📚"
          :title="t('knowledge.empty')"
          :message="t('knowledge.emptyHint')"
        >
          <BaseButton v-if="auth.isWriter" @click="openCreateSubject">
            ＋ {{ t('knowledge.newSubject') }}
          </BaseButton>
        </BaseEmptyState>
      </section>

      <section v-if="recent.length" class="space-y-3">
        <h2 class="font-display text-xl font-semibold text-clay-700">{{ t('knowledge.recent') }}</h2>
        <div class="space-y-2">
          <EntryCard v-for="entry in recent" :key="entry.id" :entry="entry" @open="openEntry" />
        </div>
      </section>
    </template>

    <BaseModal
      :open="subjectModal"
      :title="t('knowledge.newSubject')"
      @close="subjectModal = false"
    >
      <form class="space-y-4" @submit.prevent="createSubject">
        <BaseField :label="t('knowledge.subjectName')">
          <BaseInput
            v-model="subjectForm.name"
            :placeholder="t('knowledge.subjectNamePlaceholder')"
          />
        </BaseField>
        <BaseField :label="t('knowledge.subjectDescription')">
          <BaseTextarea
            v-model="subjectForm.description"
            :placeholder="t('knowledge.subjectDescriptionPlaceholder')"
          />
        </BaseField>
        <div class="flex justify-end gap-2 pt-2">
          <BaseButton variant="ghost" @click="subjectModal = false">
            {{ t('common.cancel') }}
          </BaseButton>
          <BaseButton type="submit" :disabled="!subjectForm.name.trim()">
            {{ t('common.create') }}
          </BaseButton>
        </div>
      </form>
    </BaseModal>
  </div>
</template>
