<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

import DiaryEntry from '@/components/diary/DiaryEntry.vue'
import BaseChip from '@/components/ui/BaseChip.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import { useDiaryStore } from '@/stores/diary'
import type { EventItem } from '@/types'

const { t } = useI18n()
const router = useRouter()
const diary = useDiaryStore()

onMounted(async () => {
  await diary.fetchYears()
  await diary.fetchYear(diary.year)
})

function selectYear(year: number) {
  diary.fetchYear(year)
}

function open(event: EventItem) {
  router.push({ name: 'event-detail', params: { id: event.id } })
}

const years = computed(() => (diary.years.length ? diary.years.map((entry) => entry.year) : [diary.year]))
const current = computed(() => diary.years.find((entry) => entry.year === diary.year))
</script>

<template>
  <div class="space-y-6">
    <BasePageHeader :title="t('diary.title')" :subtitle="t('diary.subtitle')" />

    <div class="-mx-1 flex gap-2 overflow-x-auto px-1 pb-1">
      <BaseChip
        v-for="year in years"
        :key="year"
        :active="year === diary.year"
        @toggle="selectYear(year)"
      >
        {{ year }}
      </BaseChip>
    </div>

    <div v-if="diary.loading" class="flex justify-center py-12"><BaseSpinner /></div>

    <template v-else>
      <p class="text-sm text-stone-400">
        {{ current?.count ?? diary.items.length }} {{ t('diary.entries') }}
      </p>
      <div v-if="diary.items.length" class="space-y-3">
        <DiaryEntry v-for="event in diary.items" :key="event.id" :event="event" @open="open" />
      </div>
      <BaseEmptyState v-else icon="📖" :title="t('diary.empty')" :message="t('diary.emptyHint')" />
    </template>
  </div>
</template>
