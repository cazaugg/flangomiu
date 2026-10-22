<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import PersonCard from '@/components/people/PersonCard.vue'
import PersonForm from '@/components/people/PersonForm.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import type { PersonPayload } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { usePeopleStore } from '@/stores/people'
import { useUiStore } from '@/stores/ui'
import type { Person } from '@/types'

const { t } = useI18n()
const auth = useAuthStore()
const people = usePeopleStore()
const ui = useUiStore()

const formOpen = ref(false)
const editing = ref<Person | null>(null)

onMounted(() => people.fetchAll())

function openCreate() {
  editing.value = null
  formOpen.value = true
}

function openEdit(person: Person) {
  editing.value = person
  formOpen.value = true
}

async function submit(payload: PersonPayload) {
  try {
    if (editing.value) {
      await people.update(editing.value.id, payload)
      ui.success('Person aktualisiert.')
    } else {
      await people.create(payload)
      ui.success('Person hinzugefügt.')
    }
    formOpen.value = false
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function remove(person: Person) {
  if (!confirm(t('common.confirmDelete'))) return
  try {
    await people.remove(person.id)
    ui.success('Gelöscht.')
  } catch (error) {
    ui.error((error as Error).message)
  }
}
</script>

<template>
  <div class="space-y-6">
    <BasePageHeader :title="t('people.title')" :subtitle="t('people.subtitle')">
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('people.new') }}</BaseButton>
    </BasePageHeader>

    <div v-if="people.loading" class="flex justify-center py-12"><BaseSpinner /></div>

    <div v-else-if="people.sorted.length" class="grid gap-3 sm:grid-cols-2">
      <PersonCard
        v-for="person in people.sorted"
        :key="person.id"
        :person="person"
        :show-actions="auth.isWriter"
        @edit="openEdit"
        @remove="remove"
      />
    </div>

    <BaseEmptyState v-else :title="t('people.empty')" :message="t('people.emptyHint')">
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('people.new') }}</BaseButton>
    </BaseEmptyState>

    <PersonForm
      :open="formOpen"
      :initial="editing"
      :title="editing ? t('people.edit') : t('people.new')"
      @close="formOpen = false"
      @submit="submit"
    />
  </div>
</template>
