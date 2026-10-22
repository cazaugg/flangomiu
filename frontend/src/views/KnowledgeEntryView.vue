<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import MarkdownView from '@/components/knowledge/MarkdownView.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import { formatDateTime } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'
import { useKnowledgeStore } from '@/stores/knowledge'
import { useUiStore } from '@/stores/ui'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const knowledge = useKnowledgeStore()
const ui = useUiStore()

const entryId = computed(() => Number(route.params.id))
const loading = ref(true)

async function load() {
  loading.value = true
  await knowledge.fetchEntry(entryId.value)
  loading.value = false
}

onMounted(load)
watch(entryId, load)

const entry = computed(() => knowledge.entry)

function back() {
  if (entry.value?.subject_id) {
    router.push({ name: 'knowledge-subject', params: { id: entry.value.subject_id } })
  } else {
    router.push({ name: 'knowledge' })
  }
}

function edit() {
  router.push({ name: 'knowledge-edit', params: { id: entryId.value } })
}

async function remove() {
  if (!entry.value) return
  if (!confirm(t('common.confirmDelete'))) return
  try {
    const subjectId = entry.value.subject_id
    await knowledge.removeEntry(entry.value.id)
    ui.success('Beitrag gelöscht.')
    router.push({ name: 'knowledge-subject', params: { id: subjectId } })
  } catch (error) {
    ui.error((error as Error).message)
  }
}
</script>

<template>
  <div class="space-y-6">
    <button
      type="button"
      class="inline-flex items-center gap-1 text-sm text-stone-500 transition hover:text-clay-700"
      @click="back"
    >
      ‹ {{ t('detail.back') }}
    </button>

    <div v-if="loading" class="flex justify-center py-16"><BaseSpinner /></div>

    <BaseEmptyState v-else-if="!entry" icon="🔍" :title="t('detail.notFound')" />

    <template v-else>
      <BaseCard>
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div class="min-w-0">
            <RouterLink
              v-if="entry.subject"
              :to="{ name: 'knowledge-subject', params: { id: entry.subject.id } }"
              class="text-xs font-medium uppercase tracking-wide text-flamingo-600 hover:underline"
            >
              📚 {{ entry.subject.name }}
            </RouterLink>
            <h1 class="mt-1 font-display text-3xl font-semibold text-clay-700">{{ entry.title }}</h1>
            <p class="mt-1 text-xs text-stone-400">
              {{ t('knowledge.updated', { date: formatDateTime(entry.updated_at) }) }}
            </p>
          </div>
          <div v-if="auth.isWriter" class="flex items-center gap-2">
            <BaseButton variant="secondary" size="sm" @click="edit">
              ✎ {{ t('common.edit') }}
            </BaseButton>
            <BaseButton variant="ghost" size="sm" @click="remove">🗑</BaseButton>
          </div>
        </div>

        <hr class="my-5 border-sand-200" />

        <MarkdownView :content="entry.content ?? ''" />
      </BaseCard>
    </template>
  </div>
</template>
