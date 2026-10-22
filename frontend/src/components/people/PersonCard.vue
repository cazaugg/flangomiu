<script setup lang="ts">
import BaseAvatar from '@/components/ui/BaseAvatar.vue'
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import { birthdayLabel } from '@/lib/date'
import type { Person } from '@/types'

defineProps<{ person: Person; showActions?: boolean }>()
const emit = defineEmits<{ edit: [Person]; remove: [Person] }>()
</script>

<template>
  <article
    class="surface-card flex items-center gap-4 rounded-3xl p-4 shadow-[0_18px_50px_-34px_rgba(140,59,46,0.5)] transition hover:-translate-y-0.5"
  >
    <BaseAvatar :name="person.name" :src="person.picture?.url" size="lg" />
    <div class="min-w-0 flex-1">
      <h3 class="truncate font-display text-lg font-semibold text-clay-700">{{ person.name }}</h3>
      <p v-if="person.description" class="truncate text-sm text-stone-500">{{ person.description }}</p>
      <p v-if="person.birthday" class="mt-0.5 flex items-center gap-1 text-sm text-stone-400">
        <span>🎂</span>{{ birthdayLabel(person.birthday) }}
      </p>
    </div>
    <div v-if="showActions" class="flex shrink-0 items-center gap-1">
      <BaseIconButton label="Bearbeiten" @click="emit('edit', person)">✎</BaseIconButton>
      <BaseIconButton label="Löschen" @click="emit('remove', person)">🗑</BaseIconButton>
    </div>
  </article>
</template>
