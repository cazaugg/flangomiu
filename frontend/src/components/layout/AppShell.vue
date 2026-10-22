<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

import BaseAvatar from '@/components/ui/BaseAvatar.vue'
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import { useAuthStore } from '@/stores/auth'
import { useTasksStore } from '@/stores/tasks'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
const tasks = useTasksStore()

const nav = computed(() => [
  { name: 'dashboard', label: t('nav.dashboard'), icon: '🏡' },
  { name: 'diary', label: t('nav.diary'), icon: '📖' },
  { name: 'knowledge', label: t('nav.knowledge'), icon: '📚' },
  { name: 'pinboard', label: t('nav.pinboard'), icon: '📌' },
  { name: 'events', label: t('nav.events'), icon: '✨' },
  { name: 'people', label: t('nav.people'), icon: '👪' },
  { name: 'calendar', label: t('nav.calendar'), icon: '🗓️' },
  { name: 'tasks', label: t('nav.tasks'), icon: '✓', badge: tasks.openCount },
])

async function signOut() {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-dvh">
    <!-- Desktop sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-40 hidden w-72 flex-col border-r border-sand-200/70 bg-white/60 px-5 py-8 backdrop-blur md:flex"
    >
      <RouterLink :to="{ name: 'dashboard' }" class="mb-10 flex items-center gap-3 px-2">
        <span
          class="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-flamingo-400 to-brick-600 text-xl shadow-[0_10px_30px_-12px_var(--color-flamingo-600)]"
        >
          🦩
        </span>
        <span>
          <span class="block font-display text-xl font-semibold text-clay-700">Flagomiu</span>
          <span class="block text-xs text-stone-400">{{ t('app.tagline') }}</span>
        </span>
      </RouterLink>

      <nav class="flex flex-1 flex-col gap-1">
        <RouterLink
          v-for="item in nav"
          :key="item.name"
          :to="{ name: item.name }"
          class="group flex items-center gap-3 rounded-2xl px-3.5 py-3 text-sm font-medium text-stone-500 transition hover:bg-sand-100 hover:text-clay-700"
          active-class="!bg-flamingo-100 !text-flamingo-700"
        >
          <span class="text-lg">{{ item.icon }}</span>
          <span class="flex-1">{{ item.label }}</span>
          <span
            v-if="item.badge"
            class="rounded-full bg-flamingo-500 px-2 py-0.5 text-xs font-semibold text-white"
          >
            {{ item.badge }}
          </span>
        </RouterLink>
      </nav>

      <div class="mt-6 rounded-2xl bg-sand-100 p-3">
        <div class="flex items-center gap-3">
          <BaseAvatar :name="auth.displayName" :src="auth.user?.person?.picture?.url" size="sm" />
          <div class="min-w-0 flex-1">
            <p class="truncate text-sm font-medium text-clay-700">{{ auth.displayName }}</p>
            <p class="text-xs text-stone-400">
              {{ auth.isWriter ? 'Schreibzugriff' : 'Nur Lesen' }}
            </p>
          </div>
          <BaseIconButton label="Abmelden" @click="signOut">⎋</BaseIconButton>
        </div>
      </div>
    </aside>

    <!-- Mobile top bar -->
    <header
      class="sticky top-0 z-40 flex items-center justify-between border-b border-sand-200/70 bg-flamingo-50/85 px-4 py-3 backdrop-blur md:hidden"
    >
      <RouterLink :to="{ name: 'dashboard' }" class="flex items-center gap-2">
        <span
          class="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-flamingo-400 to-brick-600 text-lg"
        >
          🦩
        </span>
        <span class="font-display text-lg font-semibold text-clay-700">Flagomiu</span>
      </RouterLink>
      <BaseIconButton label="Abmelden" @click="signOut">⎋</BaseIconButton>
    </header>

    <div class="md:pl-72">
      <main class="mx-auto w-full max-w-4xl px-4 pb-28 pt-6 md:px-10 md:pb-16 md:pt-10">
        <slot />
      </main>
    </div>

    <!-- Mobile bottom nav -->
    <nav
      class="no-scrollbar fixed inset-x-0 bottom-0 z-40 flex items-stretch overflow-x-auto border-t border-sand-200 bg-white/90 pb-[env(safe-area-inset-bottom)] backdrop-blur md:hidden"
    >
      <RouterLink
        v-for="item in nav"
        :key="item.name"
        :to="{ name: item.name }"
        class="relative flex min-w-[68px] shrink-0 flex-1 flex-col items-center gap-0.5 py-2.5 text-[11px] font-medium text-stone-400 transition"
        active-class="text-flamingo-600"
      >
        <span class="text-lg">{{ item.icon }}</span>
        {{ item.label }}
        <span
          v-if="item.badge"
          class="absolute right-1/2 top-1.5 translate-x-4 rounded-full bg-flamingo-500 px-1.5 text-[10px] font-semibold text-white"
        >
          {{ item.badge }}
        </span>
      </RouterLink>
    </nav>
  </div>
</template>
