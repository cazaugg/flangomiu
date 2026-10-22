<script setup lang="ts">
import { reactive, watch } from 'vue'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseField from '@/components/ui/BaseField.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseTextarea from '@/components/ui/BaseTextarea.vue'
import type { PersonPayload } from '@/api'
import { toDateInput } from '@/lib/date'
import type { Person } from '@/types'

const props = defineProps<{
  open: boolean
  initial?: Person | null
  title: string
  submitLabel?: string
}>()

const emit = defineEmits<{ close: []; submit: [PersonPayload] }>()

const form = reactive({ name: '', description: '', birthday: '' })

watch(
  () => [props.open, props.initial],
  () => {
    form.name = props.initial?.name ?? ''
    form.description = props.initial?.description ?? ''
    form.birthday = toDateInput(props.initial?.birthday)
  },
  { immediate: true },
)

function submit() {
  if (!form.name.trim()) return
  emit('submit', {
    name: form.name.trim(),
    description: form.description,
    birthday: form.birthday || null,
  })
}
</script>

<template>
  <BaseModal :open="open" :title="title" @close="emit('close')">
    <form class="space-y-4" @submit.prevent="submit">
      <BaseField label="Name">
        <BaseInput v-model="form.name" placeholder="z. B. Oma Rosa" />
      </BaseField>
      <BaseField label="Geburtstag" hint="Wird im Kalender als wiederkehrender Eintrag angezeigt.">
        <BaseInput v-model="form.birthday" type="date" />
      </BaseField>
      <BaseField label="Beschreibung">
        <BaseTextarea v-model="form.description" placeholder="optional" />
      </BaseField>
      <div class="flex justify-end gap-2 pt-2">
        <BaseButton variant="ghost" @click="emit('close')">Abbrechen</BaseButton>
        <BaseButton type="submit" :disabled="!form.name.trim()">{{ submitLabel ?? 'Speichern' }}</BaseButton>
      </div>
    </form>
  </BaseModal>
</template>
