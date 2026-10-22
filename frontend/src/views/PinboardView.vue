<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import PinCard from '@/components/pins/PinCard.vue'
import PinForm from '@/components/pins/PinForm.vue'
import ImageLightbox from '@/components/images/ImageLightbox.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseChip from '@/components/ui/BaseChip.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BasePageHeader from '@/components/ui/BasePageHeader.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import SegmentedControl from '@/components/ui/SegmentedControl.vue'
import type { PinPayload } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { usePinsStore } from '@/stores/pins'
import { useUiStore } from '@/stores/ui'
import type { PinItem } from '@/types'

const { t } = useI18n()
const auth = useAuthStore()
const pins = usePinsStore()
const ui = useUiStore()

const kind = ref('all')
const search = ref('')
const userId = ref('')
const tag = ref('')

const formOpen = ref(false)
const editing = ref<PinItem | null>(null)

const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

onMounted(() => pins.fetchAll())

const kindOptions = computed(() => [
  { value: 'all', label: t('common.all') },
  { value: 'text', label: t('pinboard.textOnly') },
  { value: 'images', label: t('pinboard.withImages') },
])

const userOptions = computed(() => [
  { value: '', label: t('pinboard.allUsers') },
  ...pins.users.map((user) => ({
    value: String(user.id),
    label: `${user.name} (${user.count})`,
  })),
])

const hasFilters = computed(
  () => Boolean(search.value.trim() || userId.value || tag.value || kind.value !== 'all'),
)

const visible = computed(() => {
  const query = search.value.trim().toLocaleLowerCase('de')
  return pins.items.filter((pin) => {
    if (userId.value && pin.user?.id !== Number(userId.value)) return false
    if (tag.value && !pin.tags.some((item) => item.name === tag.value)) return false
    if (kind.value === 'text' && pin.image) return false
    if (kind.value === 'images' && !pin.image) return false
    if (query) {
      const haystack = `${pin.text} ${pin.author}`.toLocaleLowerCase('de')
      if (!haystack.includes(query)) return false
    }
    return true
  })
})

const imagePins = computed(() => visible.value.filter((pin) => pin.image))
const lightboxPictures = computed(() =>
  imagePins.value.map((pin) => pin.image).filter((image) => image !== null),
)

function resetFilters() {
  search.value = ''
  userId.value = ''
  tag.value = ''
  kind.value = 'all'
}

function toggleTag(name: string) {
  tag.value = tag.value === name ? '' : name
}

function canEdit(pin: PinItem) {
  return auth.isWriter && pin.user?.id === auth.user?.id
}

function openCreate() {
  editing.value = null
  formOpen.value = true
}

function openEdit(pin: PinItem) {
  editing.value = pin
  formOpen.value = true
}

async function submit(payload: PinPayload, file: File | null) {
  try {
    if (editing.value) {
      await pins.update(editing.value.id, payload, file)
      ui.success('Pin aktualisiert.')
    } else {
      await pins.create(payload, file)
      ui.success('Pin angeheftet.')
    }
    formOpen.value = false
  } catch (error) {
    ui.error((error as Error).message)
  }
}

async function remove(pin: PinItem) {
  if (!confirm(t('common.confirmDelete'))) return
  try {
    await pins.remove(pin.id)
    ui.success('Pin gelöscht.')
  } catch (error) {
    ui.error((error as Error).message)
  }
}

function openImage(pin: PinItem) {
  const index = imagePins.value.findIndex((item) => item.id === pin.id)
  if (index < 0) return
  lightboxIndex.value = index
  lightboxOpen.value = true
}
</script>

<template>
  <div class="space-y-6">
    <BasePageHeader :title="t('pinboard.title')" :subtitle="t('pinboard.subtitle')">
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('pinboard.new') }}</BaseButton>
    </BasePageHeader>

    <BaseCard class="space-y-3">
      <div class="grid gap-3 sm:grid-cols-[minmax(0,1fr)_15rem]">
        <BaseInput
          v-model="search"
          type="search"
          :placeholder="t('pinboard.searchPlaceholder')"
        />
        <BaseSelect v-model="userId" :options="userOptions" />
      </div>

      <div class="flex flex-wrap items-center justify-between gap-3">
        <SegmentedControl v-model="kind" :options="kindOptions" />
        <button
          v-if="hasFilters"
          type="button"
          class="text-sm text-flamingo-600 transition hover:underline"
          @click="resetFilters"
        >
          {{ t('pinboard.filterReset') }}
        </button>
      </div>

      <div v-if="pins.tags.length" class="flex flex-wrap items-center gap-1.5">
        <BaseChip :active="!tag" @toggle="tag = ''">{{ t('pinboard.allTags') }}</BaseChip>
        <BaseChip
          v-for="item in pins.tags"
          :key="item.name"
          :active="tag === item.name"
          @toggle="toggleTag(item.name)"
        >
          #{{ item.name }}
          <span class="text-xs opacity-60">{{ item.count }}</span>
        </BaseChip>
      </div>
    </BaseCard>

    <div v-if="pins.loading" class="flex justify-center py-12"><BaseSpinner /></div>

    <div v-else-if="visible.length" class="columns-1 gap-4 sm:columns-2 lg:columns-3">
      <PinCard
        v-for="pin in visible"
        :key="pin.id"
        :pin="pin"
        :can-edit="canEdit(pin)"
        @edit="openEdit"
        @remove="remove"
        @tag="toggleTag"
        @image="openImage"
      />
    </div>

    <BaseEmptyState
      v-else-if="hasFilters"
      icon="🔍"
      :title="t('pinboard.noResults')"
      :message="t('pinboard.noResultsHint')"
    >
      <BaseButton variant="secondary" @click="resetFilters">{{ t('pinboard.filterReset') }}</BaseButton>
    </BaseEmptyState>

    <BaseEmptyState
      v-else
      icon="📌"
      :title="t('pinboard.empty')"
      :message="t('pinboard.emptyHint')"
    >
      <BaseButton v-if="auth.isWriter" @click="openCreate">＋ {{ t('pinboard.new') }}</BaseButton>
    </BaseEmptyState>

    <PinForm
      :open="formOpen"
      :initial="editing"
      :suggestions="pins.tagSuggestions"
      :title="editing ? t('pinboard.edit') : t('pinboard.new')"
      @close="formOpen = false"
      @submit="submit"
    />

    <ImageLightbox
      v-model:open="lightboxOpen"
      v-model:index="lightboxIndex"
      :pictures="lightboxPictures"
    />
  </div>
</template>
