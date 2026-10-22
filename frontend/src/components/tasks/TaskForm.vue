<script setup lang="ts">
import { reactive, watch } from 'vue'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseChip from '@/components/ui/BaseChip.vue'
import BaseField from '@/components/ui/BaseField.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseTextarea from '@/components/ui/BaseTextarea.vue'
import type { EventPayload } from '@/api'
import { toLocalInput } from '@/lib/date'
import type { EventItem, Person } from '@/types'

const props = defineProps<{
  open: boolean
  initial?: EventItem | null
  people: Person[]
  title: string
  submitLabel?: string
}>()

const emit = defineEmits<{ close: []; submit: [EventPayload] }>()

const form = reactive({ title: '', description: '', start: '', stop: '', people_ids: [] as number[] })

watch(
  () => [props.open, props.initial],
  () => {
    form.title = props.initial?.title ?? ''
    form.description = props.initial?.description ?? ''
    form.start = toLocalInput(props.initial?.start)
    form.stop = toLocalInput(props.initial?.stop)
    form.people_ids = props.initial?.people.map((person) => person.id) ?? []
  },
  { immediate: true },
)

function togglePerson(id: number) {
  form.people_ids = form.people_ids.includes(id)
    ? form.people_ids.filter((value) => value !== id)
    : [...form.people_ids, id]
}

function submit() {
  if (!form.title.trim()) return
  emit('submit', {
    title: form.title.trim(),
    description: form.description,
    start: form.start || null,
    stop: form.stop || null,
    people_ids: form.people_ids,
  })
}
</script>

<template>
  <BaseModal :open="open" :title="title" @close="emit('close')">
    <form class="space-y-4" @submit.prevent="submit">
      <BaseField label="Aufgabe">
        <BaseInput v-model="form.title" placeholder="z. B. Reifen wechseln" />
      </BaseField>
      <div class="grid grid-cols-2 gap-3">
        <BaseField label="Von">
          <BaseInput v-model="form.start" type="datetime-local" />
        </BaseField>
        <BaseField label="Bis" hint="Danach gilt sie als erledigt.">
          <BaseInput v-model="form.stop" type="datetime-local" />
        </BaseField>
      </div>
      <BaseField label="Notiz">
        <BaseTextarea v-model="form.description" placeholder="optional" />
      </BaseField>
      <BaseField label="Zuständig">
        <div class="flex flex-wrap gap-2">
          <BaseChip
            v-for="person in people"
            :key="person.id"
            :active="form.people_ids.includes(person.id)"
            @toggle="togglePerson(person.id)"
          >
            {{ person.name }}
          </BaseChip>
        </div>
      </BaseField>
      <div class="flex justify-end gap-2 pt-2">
        <BaseButton variant="ghost" @click="emit('close')">Abbrechen</BaseButton>
        <BaseButton type="submit" :disabled="!form.title.trim()">{{ submitLabel ?? 'Speichern' }}</BaseButton>
      </div>
    </form>
  </BaseModal>
</template>
