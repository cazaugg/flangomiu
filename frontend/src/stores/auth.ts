import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { authApi } from '@/api'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const ready = ref(false)

  const isAuthenticated = computed(() => user.value !== null)
  const isWriter = computed(() => user.value?.write_access === true)
  const displayName = computed(() => user.value?.person?.name || user.value?.username || '')

  async function fetchMe() {
    try {
      const { user: current } = await authApi.me()
      user.value = current
    } catch {
      user.value = null
    } finally {
      ready.value = true
    }
  }

  async function login(username: string, password: string) {
    const { user: current } = await authApi.login(username, password)
    user.value = current
  }

  async function logout() {
    try {
      await authApi.logout()
    } finally {
      user.value = null
    }
  }

  return { user, ready, isAuthenticated, isWriter, displayName, fetchMe, login, logout }
})
