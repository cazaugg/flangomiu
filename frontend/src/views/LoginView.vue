<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseField from '@/components/ui/BaseField.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const ui = useUiStore()

const username = ref('admin')
const password = ref('flamingo')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    ui.success('Willkommen zurück!')
    const redirect = route.query.redirect as string | undefined
    router.push(redirect || { name: 'dashboard' })
  } catch {
    error.value = t('auth.invalid')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="grid min-h-dvh lg:grid-cols-2">
    <div
      class="relative hidden overflow-hidden bg-gradient-to-br from-flamingo-400 via-flamingo-500 to-brick-600 p-12 text-white lg:flex lg:flex-col lg:justify-between"
    >
      <div class="text-4xl">🦩</div>
      <div>
        <h1 class="font-display text-5xl font-semibold leading-tight">Flagomiu</h1>
        <p class="mt-3 max-w-sm text-lg text-white/85">
          Das Familientagebuch für gemeinsame Erlebnisse, Geburtstage und alles, was noch ansteht.
        </p>
      </div>
      <p class="text-sm text-white/70">Erlebnisse · Personen · Kalender · Aufgaben</p>
    </div>

    <div class="flex items-center justify-center p-6 sm:p-12">
      <form class="w-full max-w-sm space-y-5" @submit.prevent="submit">
        <div class="mb-2 flex items-center gap-3 lg:hidden">
          <span
            class="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-flamingo-400 to-brick-600 text-xl"
          >
            🦩
          </span>
          <span class="font-display text-2xl font-semibold text-clay-700">Flagomiu</span>
        </div>

        <div>
          <h2 class="font-display text-3xl font-semibold text-clay-700">{{ t('auth.welcome') }}</h2>
          <p class="mt-1 text-sm text-stone-500">{{ t('auth.subtitle') }}</p>
        </div>

        <BaseField :label="t('auth.username')">
          <BaseInput v-model="username" name="username" autocomplete="username" />
        </BaseField>
        <BaseField :label="t('auth.password')">
          <BaseInput
            v-model="password"
            name="password"
            type="password"
            autocomplete="current-password"
          />
        </BaseField>

        <p v-if="error" class="text-sm text-flamingo-700">{{ error }}</p>

        <BaseButton type="submit" block :disabled="loading || !username || !password">
          {{ loading ? t('common.loading') : t('auth.login') }}
        </BaseButton>

        <p class="rounded-2xl bg-sand-100 px-4 py-3 text-xs text-stone-500">
          Demo: <strong>admin</strong> / <strong>flamingo</strong> (Schreibzugriff) oder
          <strong>gast</strong> / <strong>flamingo</strong> (nur Lesen).
        </p>
      </form>
    </div>
  </div>
</template>
