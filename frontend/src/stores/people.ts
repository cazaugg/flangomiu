import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { peopleApi, type PersonPayload } from '@/api'
import type { Person } from '@/types'

export const usePeopleStore = defineStore('people', () => {
  const items = ref<Person[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const sorted = computed(() => [...items.value].sort((a, b) => a.name.localeCompare(b.name, 'de')))

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      items.value = (await peopleApi.list()).items
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function create(payload: PersonPayload) {
    const { person } = await peopleApi.create(payload)
    items.value.push(person)
    return person
  }

  async function update(id: number, payload: PersonPayload) {
    const { person } = await peopleApi.update(id, payload)
    const index = items.value.findIndex((item) => item.id === id)
    if (index >= 0) items.value[index] = person
    return person
  }

  async function remove(id: number) {
    await peopleApi.remove(id)
    items.value = items.value.filter((item) => item.id !== id)
  }

  return { items, sorted, loading, error, fetchAll, create, update, remove }
})
