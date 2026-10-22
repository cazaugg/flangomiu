<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import EventCard from '@/components/events/EventCard.vue'
import EventForm from '@/components/events/EventForm.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseChip from '@/components/ui/BaseChip.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import type { EventPayload } from '@/api'
import { EVENT_KINDS, KIND_META } from '@/lib/kinds'
import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'
import { usePeopleStore } from '@/stores/people'
import { useUiStore } from '@/stores/ui'
import type { EventItem, EventKind } from '@/types'

const { t } = useI18n()
const auth = useAuthStore()
const events = useEventsStore()
const people = usePeopleStore()
const ui = useUiStore()

const LIST_KINDS: EventKind[] = [...EVENT_KINDS, 'appointment']
const filter = ref<'all' | EventKind>('all')
const formOpen = ref(false)
const editing = ref<EventItem | null>(null)

const filterOptions = computed(() => [
  { value: 'all' as const, label: 'Alle' },
  ...LIST_KINDS.map((kind) => ({ value: kind, label: KIND_META[kind].label })),
])

onMounted(() => events.fetchAll(LIST_KINDS.join(',')))

const visible = computed(() =>
  filter.value === 'all' ? events.items : events.items.filter((item) => item.kind === filter.value),
)

function openCreate() {
  editing.value = null
  formOpen.value = true
}

function openEdit(event: EventItem) {
  editing.value = event
  formOpen.value = true
}

async function submit(payload: EventPayload) {
  try {
    if (editing.value) {
      await events.update(editing.value.id, payload)
      ui.success('Erlebnis aktualisiert.')
    } else {
      await events.create(payload)
      ui.success('Erlebnis hinzugefügt.')
    }
    formOpen.value = false
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function remove(event: EventItem) {
  if (!confirm(t('common.confirmDelete'))) return
  try {
    await events.remove(event.id)
    ui.success('Gelöscht.')
  } catch (error) {
    ui.error((error as Error).message)
  }
}
</script>

<template>
  <div class="space-y-6">
    <BasePageHeader :title="t('events.title')" :subtitle="t('events.subtitle')">
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('events.new') }}</BaseButton>
    </BasePageHeader>

    <div class="flex flex-wrap gap-2">
      <BaseChip
        v-for="option in filterOptions"
        :key="option.value"
        :active="filter === option.value"
        @toggle="filter = option.value"
      >
        {{ option.label }}
      </BaseChip>
    </div>

    <div v-if="events.loading" class="flex justify-center py-12"><BaseSpinner /></div>

    <div v-else-if="visible.length" class="grid gap-3 sm:grid-cols-2">
      <EventCard
        v-for="event in visible"
        :key="event.id"
        :event="event"
        :show-actions="auth.isWriter"
        @edit="openEdit"
        @remove="remove"
      />
    </div>

    <BaseEmptyState v-else :title="t('events.empty')" :message="t('events.emptyHint')">
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('events.new') }}</BaseButton>
    </BaseEmptyState>

    <EventForm
      :open="formOpen"
      :initial="editing"
      :people="people.items"
      :title="editing ? t('events.edit') : t('events.new')"
      @close="formOpen = false"
      @submit="submit"
    />
  </div>
</template>
