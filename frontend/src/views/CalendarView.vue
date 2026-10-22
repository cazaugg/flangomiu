<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { addMonths, endOfMonth, format, startOfMonth } from 'date-fns'
import { de } from 'date-fns/locale'
import { useI18n } from 'vue-i18n'

import AgendaList from '@/components/calendar/AgendaList.vue'
import CalendarMonth from '@/components/calendar/CalendarMonth.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import SegmentedControl from '@/components/ui/SegmentedControl.vue'
import { calendarApi } from '@/api'
import { kindMeta } from '@/lib/kinds'
import { useUiStore } from '@/stores/ui'
import type { EventItem } from '@/types'

const { t } = useI18n()
const ui = useUiStore()

const cursor = ref(startOfMonth(new Date()))
const mode = ref<'month' | 'agenda'>('month')
const items = ref<EventItem[]>([])
const loading = ref(false)
const selectedDay = ref<string | null>(null)

const modeOptions = [
  { value: 'month', label: t('calendar.month') },
  { value: 'agenda', label: t('calendar.agenda') },
]

const monthLabel = computed(() => format(cursor.value, 'MMMM yyyy', { locale: de }))

const agendaItems = computed(() => {
  if (!selectedDay.value) return items.value
  return items.value.filter((item) => (item.start ?? '').slice(0, 10) === selectedDay.value)
})

async function load() {
  loading.value = true
  try {
    const start = format(startOfMonth(cursor.value), 'yyyy-MM-dd')
    const end = format(endOfMonth(cursor.value), 'yyyy-MM-dd')
    items.value = (await calendarApi.range(start, end)).items
  } catch (error) {
    ui.error((error as Error).message)
  } finally {
    loading.value = false
  }
}

watch(cursor, load)

onMounted(() => {
  if (window.innerWidth < 768) mode.value = 'agenda'
  load()
})

function shift(delta: number) {
  cursor.value = addMonths(cursor.value, delta)
  selectedDay.value = null
}

function goToday() {
  cursor.value = startOfMonth(new Date())
  selectedDay.value = null
}

function selectItem(item: EventItem) {
  ui.notify(`${kindMeta(item.kind).label}: ${item.title}`)
}
</script>

<template>
  <div class="space-y-6">
    <BasePageHeader :title="t('calendar.title')" :subtitle="t('calendar.subtitle')">
      <SegmentedControl v-model="mode" :options="modeOptions" />
    </BasePageHeader>

    <BaseCard>
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center gap-1">
          <BaseIconButton label="Vorheriger Monat" @click="shift(-1)">‹</BaseIconButton>
          <BaseIconButton label="Nächster Monat" @click="shift(1)">›</BaseIconButton>
        </div>
        <h2 class="font-display text-lg font-semibold capitalize text-clay-700">{{ monthLabel }}</h2>
        <BaseButton variant="ghost" size="sm" @click="goToday">{{ t('calendar.today') }}</BaseButton>
      </div>

      <div v-if="loading" class="flex justify-center py-12"><BaseSpinner /></div>
      <template v-else>
        <CalendarMonth
          v-if="mode === 'month'"
          :month="cursor"
          :items="items"
          :selected-day="selectedDay"
          @select-day="(day) => (selectedDay = day)"
          @select-item="selectItem"
        />

        <div v-else>
          <p v-if="selectedDay" class="mb-3 text-sm text-stone-400">
            Ausgewählt: {{ format(new Date(selectedDay), 'd. MMMM yyyy', { locale: de }) }}
          </p>
          <AgendaList v-if="agendaItems.length" :items="agendaItems" @select-item="selectItem" />
          <BaseEmptyState v-else icon="🗓️" :title="t('calendar.empty')" />
        </div>
      </template>
    </BaseCard>

    <BaseCard v-if="mode === 'month' && selectedDay">
      <h2 class="mb-3 font-display text-lg font-semibold text-clay-700">
        {{ format(new Date(selectedDay), 'EEEE, d. MMMM', { locale: de }) }}
      </h2>
      <AgendaList v-if="agendaItems.length" :items="agendaItems" @select-item="selectItem" />
      <p v-else class="text-sm text-stone-400">{{ t('calendar.empty') }}</p>
    </BaseCard>
  </div>
</template>
