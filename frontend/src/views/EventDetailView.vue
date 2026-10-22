<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

import EventForm from '@/components/events/EventForm.vue'
import ImageUploader from '@/components/images/ImageUploader.vue'
import PictureGallery from '@/components/images/PictureGallery.vue'
import BaseAvatar from '@/components/ui/BaseAvatar.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import KindBadge from '@/components/ui/KindBadge.vue'
import { eventsApi, picturesApi, type EventPayload } from '@/api'
import { formatRange } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'
import { usePeopleStore } from '@/stores/people'
import { useUiStore } from '@/stores/ui'
import type { EventItem, Picture } from '@/types'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const people = usePeopleStore()
const ui = useUiStore()

const event = ref<EventItem | null>(null)
const loading = ref(true)
const uploading = ref(false)
const formOpen = ref(false)

const eventId = computed(() => route.params.id as string)
const when = computed(() =>
  event.value ? formatRange(event.value.start, event.value.stop, event.value.all_day) : '',
)

async function load() {
  loading.value = true
  try {
    event.value = (await eventsApi.get(eventId.value)).event
  } catch {
    event.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  load()
  if (!people.items.length) people.fetchAll()
})

watch(eventId, load)

async function upload(files: File[]) {
  if (!event.value) return
  uploading.value = true
  try {
    event.value = (await eventsApi.uploadPictures(event.value.id, files)).event
    ui.success('Bilder hinzugefügt.')
  } catch (error) {
    ui.error((error as Error).message)
  } finally {
    uploading.value = false
  }
}

async function updateCaption(picture: Picture, description: string) {
  if (!event.value || description === picture.description) return
  try {
    const updated = (await picturesApi.update(picture.id, { description })).picture
    event.value = {
      ...event.value,
      pictures: event.value.pictures.map((item) => (item.id === updated.id ? updated : item)),
    }
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function removePicture(picture: Picture) {
  if (!event.value || !confirm(t('common.confirmDelete'))) return
  try {
    event.value = (await eventsApi.removePicture(event.value.id, picture.id)).event
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function reorder(ids: number[]) {
  if (!event.value) return
  try {
    event.value = (await eventsApi.reorderPictures(event.value.id, ids)).event
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function setCover(picture: Picture) {
  if (!event.value) return
  try {
    event.value = (await eventsApi.update(event.value.id, { cover_picture_id: picture.id })).event
    ui.success('Titelbild gesetzt.')
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function submit(payload: EventPayload) {
  if (!event.value) return
  try {
    event.value = (await eventsApi.update(event.value.id, payload)).event
    formOpen.value = false
    ui.success('Gespeichert.')
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function removeEvent() {
  if (!event.value || !confirm(t('common.confirmDelete'))) return
  try {
    await eventsApi.remove(event.value.id)
    ui.success('Gelöscht.')
    router.push({ name: 'events' })
  } catch (error) {
    ui.error((error as Error).message)
  }
}
</script>

<template>
  <div class="space-y-6">
    <RouterLink
      :to="{ name: 'diary' }"
      class="inline-flex items-center gap-1 text-sm text-stone-500 transition hover:text-clay-700"
    >
      ‹ {{ t('detail.back') }}
    </RouterLink>

    <div v-if="loading" class="flex justify-center py-16"><BaseSpinner /></div>

    <BaseEmptyState v-else-if="!event" icon="🔍" :title="t('detail.notFound')" />

    <template v-else>
      <BaseCard padded>
        <div v-if="event.cover" class="-mx-5 -mt-5 mb-5 overflow-hidden rounded-t-3xl">
          <img :src="event.cover.url" :alt="event.title" class="max-h-80 w-full object-cover" />
        </div>

        <div class="flex flex-wrap items-start justify-between gap-4">
          <div class="min-w-0">
            <KindBadge :kind="event.kind" />
            <h1 class="mt-2 font-display text-3xl font-semibold text-clay-700">{{ event.title }}</h1>
            <p class="mt-1 text-sm text-stone-500">{{ when }}</p>
            <p v-if="event.location" class="mt-0.5 text-sm text-stone-400">📍 {{ event.location }}</p>
          </div>
          <div v-if="auth.isWriter" class="flex items-center gap-2">
            <BaseButton variant="secondary" size="sm" @click="formOpen = true">
              ✎ {{ t('common.edit') }}
            </BaseButton>
            <BaseButton variant="ghost" size="sm" @click="removeEvent">🗑</BaseButton>
          </div>
        </div>

        <p class="mt-4 whitespace-pre-line text-stone-700">
          {{ event.description || t('detail.noDescription') }}
        </p>

        <div v-if="event.people.length" class="mt-5">
          <p class="mb-2 text-xs font-medium uppercase tracking-wide text-stone-400">
            {{ t('detail.people') }}
          </p>
          <div class="flex flex-wrap gap-3">
            <div
              v-for="person in event.people"
              :key="person.id"
              class="flex items-center gap-2 rounded-full bg-sand-100 py-1 pl-1 pr-3"
            >
              <BaseAvatar :name="person.name" :src="person.picture?.url" size="sm" />
              <span class="text-sm text-stone-700">{{ person.name }}</span>
            </div>
          </div>
        </div>
      </BaseCard>

      <section class="space-y-3">
        <h2 class="font-display text-xl font-semibold text-clay-700">
          {{ t('images.title') }}
          <span v-if="event.picture_count" class="text-sm font-normal text-stone-400">
            · {{ event.picture_count }}
          </span>
        </h2>

        <ImageUploader v-if="auth.isWriter" :busy="uploading" @files="upload" />

        <PictureGallery
          v-if="event.pictures.length"
          :pictures="event.pictures"
          :editable="auth.isWriter"
          :cover-id="event.cover?.id ?? null"
          @caption="updateCaption"
          @remove="removePicture"
          @reorder="reorder"
          @cover="setCover"
        />
        <BaseEmptyState v-else icon="🖼️" :title="t('images.empty')" />
        <p v-if="event.pictures.length && auth.isWriter" class="text-xs text-stone-400">
          {{ t('images.hint') }}
        </p>
      </section>

      <EventForm
        :open="formOpen"
        :initial="event"
        :people="people.items"
        :title="t('events.edit')"
        @close="formOpen = false"
        @submit="submit"
      />
    </template>
  </div>
</template>
