import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { tasksApi, type EventPayload } from '@/api'
import type { EventItem } from '@/types'

export const useTasksStore = defineStore('tasks', () => {
  const items = ref<EventItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const openTasks = computed(() => items.value.filter((task) => !task.is_done))
  const openCount = computed(() => openTasks.value.length)

  async function fetchAll(status: 'all' | 'open' | 'done' = 'all') {
    loading.value = true
    error.value = null
    try {
      items.value = (await tasksApi.list(status)).items
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function create(payload: EventPayload) {
    const { task } = await tasksApi.create(payload)
    items.value.unshift(task)
    return task
  }

  async function update(id: number | string, payload: EventPayload) {
    const { task } = await tasksApi.update(id, payload)
    const index = items.value.findIndex((item) => item.id === id)
    if (index >= 0) items.value[index] = task
    return task
  }

  async function remove(id: number | string) {
    await tasksApi.remove(id)
    items.value = items.value.filter((item) => item.id !== id)
  }

  return { items, openTasks, openCount, loading, error, fetchAll, create, update, remove }
})
