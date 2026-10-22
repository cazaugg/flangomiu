<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import TaskForm from '@/components/tasks/TaskForm.vue'
import TaskItem from '@/components/tasks/TaskItem.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import SegmentedControl from '@/components/ui/SegmentedControl.vue'
import type { EventPayload } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { usePeopleStore } from '@/stores/people'
import { useTasksStore } from '@/stores/tasks'
import { useUiStore } from '@/stores/ui'
import type { EventItem } from '@/types'

const { t } = useI18n()
const auth = useAuthStore()
const tasks = useTasksStore()
const people = usePeopleStore()
const ui = useUiStore()

const status = ref('all')
const formOpen = ref(false)
const editing = ref<EventItem | null>(null)

const statusOptions = [
  { value: 'open', label: t('common.open') },
  { value: 'done', label: t('common.done') },
  { value: 'all', label: t('common.all') },
]

onMounted(() => tasks.fetchAll('all'))

const visible = computed(() => {
  if (status.value === 'open') return tasks.items.filter((task) => !task.is_done)
  if (status.value === 'done') return tasks.items.filter((task) => task.is_done)
  return tasks.items
})

function openCreate() {
  editing.value = null
  formOpen.value = true
}

function openEdit(task: EventItem) {
  editing.value = task
  formOpen.value = true
}

async function submit(payload: EventPayload) {
  try {
    if (editing.value) {
      await tasks.update(editing.value.id, payload)
      ui.success('Aufgabe aktualisiert.')
    } else {
      await tasks.create(payload)
      ui.success('Aufgabe hinzugefügt.')
    }
    formOpen.value = false
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function remove(task: EventItem) {
  if (!confirm(t('common.confirmDelete'))) return
  try {
    await tasks.remove(task.id)
    ui.success('Gelöscht.')
  } catch (error) {
    ui.error((error as Error).message)
  }
}
</script>

<template>
  <div class="space-y-6">
    <BasePageHeader :title="t('tasks.title')" :subtitle="t('tasks.subtitle')">
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('tasks.new') }}</BaseButton>
    </BasePageHeader>

    <SegmentedControl v-model="status" :options="statusOptions" />

    <div v-if="tasks.loading" class="flex justify-center py-12"><BaseSpinner /></div>

    <div v-else-if="visible.length" class="space-y-2">
      <TaskItem
        v-for="task in visible"
        :key="task.id"
        :task="task"
        :show-actions="auth.isWriter"
        @edit="openEdit"
        @remove="remove"
      />
    </div>

    <BaseEmptyState v-else icon="✅" :title="t('tasks.empty')" :message="t('tasks.emptyHint')">
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('tasks.new') }}</BaseButton>
    </BaseEmptyState>

    <TaskForm
      :open="formOpen"
      :initial="editing"
      :people="people.items"
      :title="editing ? t('tasks.edit') : t('tasks.new')"
      @close="formOpen = false"
      @submit="submit"
    />
  </div>
</template>
