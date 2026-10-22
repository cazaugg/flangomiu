<script setup lang="ts">
import { watch } from 'vue'
import { RouterView } from 'vue-router'

import AppShell from '@/components/layout/AppShell.vue'
import ToastHost from '@/components/ui/ToastHost.vue'
import { useAuthStore } from '@/stores/auth'
import { usePeopleStore } from '@/stores/people'
import { useTasksStore } from '@/stores/tasks'

const auth = useAuthStore()
const tasks = useTasksStore()
const people = usePeopleStore()

watch(
  () => auth.isAuthenticated,
  (authenticated) => {
    if (!authenticated) return
    tasks.fetchAll()
    people.fetchAll()
  },
  { immediate: true },
)
</script>

<template>
  <AppShell v-if="auth.isAuthenticated">
    <RouterView />
  </AppShell>
  <RouterView v-else />
  <ToastHost />
</template>
