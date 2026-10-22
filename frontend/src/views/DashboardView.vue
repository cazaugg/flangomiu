<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { differenceInCalendarDays, format, parseISO } from 'date-fns'
import { de } from 'date-fns/locale'
import { useI18n } from 'vue-i18n'

import EventCard from '@/components/events/EventCard.vue'
import TaskItem from '@/components/tasks/TaskItem.vue'
import BaseAvatar from '@/components/ui/BaseAvatar.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'
import { usePeopleStore } from '@/stores/people'
import { useTasksStore } from '@/stores/tasks'

const { t } = useI18n()
const auth = useAuthStore()
const events = useEventsStore()
const people = usePeopleStore()
const tasks = useTasksStore()

onMounted(() => events.fetchAll('event,appointment'))

const upcoming = computed(() => events.upcoming)
const openTasks = computed(() => tasks.openTasks.slice(0, 4))

function nextBirthday(birthday: string): Date {
  const date = parseISO(birthday)
  const today = new Date()
  const next = new Date(today.getFullYear(), date.getMonth(), date.getDate())
  const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate())
  if (next < startOfToday) next.setFullYear(today.getFullYear() + 1)
  return next
}

const birthdays = computed(() =>
  people.items
    .filter((person) => person.birthday)
    .map((person) => ({ person, date: nextBirthday(person.birthday as string) }))
    .sort((a, b) => a.date.getTime() - b.date.getTime())
    .slice(0, 4),
)

const stats = computed(() => [
  { label: 'Erlebnisse', value: events.items.length, icon: '✨' },
  { label: 'Personen', value: people.items.length, icon: '👪' },
  { label: 'Offene Aufgaben', value: tasks.openCount, icon: '✓' },
])
</script>

<template>
  <div class="space-y-8">
    <BasePageHeader :title="`${t('dashboard.greeting')}, ${auth.displayName}`" subtitle="Schön, dass du da bist." />

    <div class="grid grid-cols-3 gap-3">
      <BaseCard v-for="stat in stats" :key="stat.label" class="text-center">
        <div class="text-2xl">{{ stat.icon }}</div>
        <div class="mt-1 font-display text-2xl font-semibold text-clay-700">{{ stat.value }}</div>
        <div class="text-xs text-stone-400">{{ stat.label }}</div>
      </BaseCard>
    </div>

    <section class="space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="font-display text-xl font-semibold text-clay-700">{{ t('dashboard.upcoming') }}</h2>
        <RouterLink :to="{ name: 'events' }" class="text-sm text-flamingo-600 hover:underline">
          {{ t('dashboard.seeAll') }}
        </RouterLink>
      </div>
      <div v-if="upcoming.length" class="grid gap-3 sm:grid-cols-2">
        <EventCard v-for="event in upcoming" :key="event.id" :event="event" />
      </div>
      <BaseEmptyState
        v-else
        title="Noch nichts geplant"
        message="Erlebnisse und Termine erscheinen hier, sobald du sie anlegst."
      />
    </section>

    <div class="grid gap-8 lg:grid-cols-2">
      <section class="space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="font-display text-xl font-semibold text-clay-700">{{ t('dashboard.openTasks') }}</h2>
          <RouterLink :to="{ name: 'tasks' }" class="text-sm text-flamingo-600 hover:underline">
            {{ t('dashboard.seeAll') }}
          </RouterLink>
        </div>
        <div v-if="openTasks.length" class="space-y-2">
          <TaskItem v-for="task in openTasks" :key="task.id" :task="task" />
        </div>
        <BaseEmptyState v-else icon="🎉" title="Keine offenen Aufgaben" />
      </section>

      <section class="space-y-3">
        <h2 class="font-display text-xl font-semibold text-clay-700">{{ t('dashboard.nextBirthdays') }}</h2>
        <div v-if="birthdays.length" class="space-y-2">
          <BaseCard
            v-for="entry in birthdays"
            :key="entry.person.id"
            class="flex items-center gap-3"
          >
            <BaseAvatar :name="entry.person.name" :src="entry.person.picture?.url" size="sm" />
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-medium text-clay-700">{{ entry.person.name }}</p>
              <p class="text-xs text-stone-400">
                {{ format(entry.date, 'd. MMMM', { locale: de }) }}
              </p>
            </div>
            <span class="shrink-0 text-xs text-stone-400">
              {{
                differenceInCalendarDays(entry.date, new Date()) === 0
                  ? 'heute'
                  : `in ${differenceInCalendarDays(entry.date, new Date())} T.`
              }}
            </span>
          </BaseCard>
        </div>
        <BaseEmptyState v-else icon="🎂" title="Keine Geburtstage erfasst" />
      </section>
    </div>
  </div>
</template>
