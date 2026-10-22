import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { pinsApi, type PinPayload } from '@/api'
import type { PinItem, PinUser } from '@/types'

export interface PinFilterUser extends PinUser {
  count: number
}

export interface PinFilterTag {
  name: string
  count: number
}

export const usePinsStore = defineStore('pins', () => {
  const items = ref<PinItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const users = computed<PinFilterUser[]>(() => {
    const counts = new Map<number, PinFilterUser>()
    for (const pin of items.value) {
      if (!pin.user) continue
      const entry = counts.get(pin.user.id)
      if (entry) entry.count += 1
      else counts.set(pin.user.id, { ...pin.user, count: 1 })
    }
    return [...counts.values()].sort(
      (a, b) => b.count - a.count || a.name.localeCompare(b.name, 'de'),
    )
  })

  const tags = computed<PinFilterTag[]>(() => {
    const counts = new Map<string, PinFilterTag>()
    for (const pin of items.value) {
      for (const tag of pin.tags) {
        const entry = counts.get(tag.name)
        if (entry) entry.count += 1
        else counts.set(tag.name, { name: tag.name, count: 1 })
      }
    }
    return [...counts.values()].sort(
      (a, b) => b.count - a.count || a.name.localeCompare(b.name, 'de'),
    )
  })

  const tagSuggestions = computed(() => tags.value.map((tag) => tag.name))

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      items.value = (await pinsApi.list()).items
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function create(payload: PinPayload, file?: File | null) {
    const { pin } = await pinsApi.create(payload, file)
    items.value = [pin, ...items.value]
    return pin
  }

  async function update(id: number, payload: PinPayload, file?: File | null) {
    const { pin } = await pinsApi.update(id, payload, file)
    const index = items.value.findIndex((item) => item.id === id)
    if (index >= 0) items.value[index] = pin
    return pin
  }

  async function remove(id: number) {
    await pinsApi.remove(id)
    items.value = items.value.filter((item) => item.id !== id)
  }

  return {
    items,
    users,
    tags,
    tagSuggestions,
    loading,
    error,
    fetchAll,
    create,
    update,
    remove,
  }
})
