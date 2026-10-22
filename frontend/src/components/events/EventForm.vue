<script setup lang="ts">
import { reactive, watch } from 'vue'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseChip from '@/components/ui/BaseChip.vue'
import BaseField from '@/components/ui/BaseField.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseTextarea from '@/components/ui/BaseTextarea.vue'
import type { EventPayload } from '@/api'
import { toLocalInput } from '@/lib/date'
import { EVENT_KINDS, KIND_META } from '@/lib/kinds'
import type { EventItem, Person, StoredEventKind } from '@/types'

const props = defineProps<{
  open: boolean
  initial?: EventItem | null
  people: Person[]
  title: string
  submitLabel?: string
}>()

const emit = defineEmits<{ close: []; submit: [EventPayload] }>()

const kindOptions = [...EVENT_KINDS, 'appointment' as const].map((kind) => ({
  value: kind,
  label: KIND_META[kind].label,
}))

const form = reactive({
  title: '',
  kind: 'event' as StoredEventKind,
  description: '',
  location: '',
  start: '',
  stop: '',
  all_day: false,
  people_ids: [] as number[],
})

function reset() {
  const event = props.initial
  form.title = event?.title ?? ''
  form.kind =
    event?.kind === 'event' || event?.kind === 'appointment' || event?.kind === 'task'
      ? event.kind
      : 'event'
  form.description = event?.description ?? ''
  form.location = event?.location ?? ''
  form.start = toLocalInput(event?.start)
  form.stop = toLocalInput(event?.stop)
  form.all_day = event?.all_day ?? false
  form.people_ids = event?.people.map((person) => person.id) ?? []
}

watch(() => [props.open, props.initial], reset, { immediate: true })

function togglePerson(id: number) {
  form.people_ids = form.people_ids.includes(id)
    ? form.people_ids.filter((value) => value !== id)
    : [...form.people_ids, id]
}

function submit() {
  if (!form.title.trim()) return
  emit('submit', {
    title: form.title.trim(),
    kind: form.kind,
    description: form.description,
    location: form.location,
    start: form.start || null,
    stop: form.stop || null,
    all_day: form.all_day,
    people_ids: form.people_ids,
  })
}
</script>

<template>
  <BaseModal :open="open" :title="title" @close="emit('close')">
    <form class="space-y-4" @submit.prevent="submit">
      <BaseField label="Titel">
        <BaseInput v-model="form.title" placeholder="z. B. Ausflug in den Zoo" />
      </BaseField>

      <BaseField label="Art">
        <BaseSelect v-model="form.kind" :options="kindOptions" />
      </BaseField>

      <div class="grid grid-cols-2 gap-3">
        <BaseField label="Beginn">
          <BaseInput v-model="form.start" type="datetime-local" />
        </BaseField>
        <BaseField label="Ende">
          <BaseInput v-model="form.stop" type="datetime-local" />
        </BaseField>
      </div>

      <label class="flex items-center gap-2 text-sm text-stone-700">
        <input v-model="form.all_day" type="checkbox" class="h-4 w-4 rounded accent-flamingo-500" />
        Ganztägig
      </label>

      <BaseField label="Ort">
        <BaseInput v-model="form.location" placeholder="optional" />
      </BaseField>

      <BaseField label="Beschreibung">
        <BaseTextarea v-model="form.description" placeholder="optional" />
      </BaseField>

      <BaseField label="Beteiligte Personen">
        <div class="flex flex-wrap gap-2">
          <BaseChip
            v-for="person in people"
            :key="person.id"
            :active="form.people_ids.includes(person.id)"
            @toggle="togglePerson(person.id)"
          >
            {{ person.name }}
          </BaseChip>
          <span v-if="!people.length" class="text-sm text-stone-400">Noch keine Personen angelegt.</span>
        </div>
      </BaseField>

      <div class="flex justify-end gap-2 pt-2">
        <BaseButton variant="ghost" @click="emit('close')">Abbrechen</BaseButton>
        <BaseButton type="submit" :disabled="!form.title.trim()">
          {{ submitLabel ?? 'Speichern' }}
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>
