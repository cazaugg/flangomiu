import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { eventsApi, type EventPayload } from '@/api'
import type { EventItem } from '@/types'

export const useEventsStore = defineStore('events', () => {
  const items = ref<EventItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const upcoming = computed(() =>
    [...items.value]
      .filter((event) => !event.is_done)
      .sort((a, b) => (a.start ?? '').localeCompare(b.start ?? ''))
      .slice(0, 5),
  )

  async function fetchAll(kind?: string) {
    loading.value = true
    error.value = null
    try {
      items.value = (await eventsApi.list(kind ? { kind } : undefined)).items
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function create(payload: EventPayload) {
    const { event } = await eventsApi.create(payload)
    items.value.unshift(event)
    return event
  }

  async function fetchOne(id: number | string) {
    const { event } = await eventsApi.get(id)
    return event
  }

  async function update(id: number | string, payload: EventPayload) {
    const { event } = await eventsApi.update(id, payload)
    const index = items.value.findIndex((item) => item.id === id)
    if (index >= 0) items.value[index] = event
    return event
  }

  async function remove(id: number | string) {
    await eventsApi.remove(id)
    items.value = items.value.filter((item) => item.id !== id)
  }

  return { items, loading, error, upcoming, fetchAll, fetchOne, create, update, remove }
})
