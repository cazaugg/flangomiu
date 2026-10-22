import { defineStore } from 'pinia'
import { ref } from 'vue'

import { diaryApi } from '@/api'
import type { DiaryYear, EventItem } from '@/types'

export const useDiaryStore = defineStore('diary', () => {
  const years = ref<DiaryYear[]>([])
  const year = ref(new Date().getFullYear())
  const items = ref<EventItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchYears() {
    try {
      years.value = (await diaryApi.years()).items
    } catch (e) {
      error.value = (e as Error).message
    }
  }

  async function fetchYear(target: number) {
    loading.value = true
    error.value = null
    try {
      const response = await diaryApi.year(target)
      year.value = response.year
      items.value = response.items
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  return { years, year, items, loading, error, fetchYears, fetchYear }
})
