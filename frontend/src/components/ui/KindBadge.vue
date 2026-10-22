<script setup lang="ts">
import { computed } from 'vue'

import { kindMeta } from '@/lib/kinds'
import type { EventKind } from '@/types'

const props = defineProps<{ kind: EventKind | string }>()
const meta = computed(() => kindMeta(props.kind))
</script>

<template>
  <span
    class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium"
    :style="{ color: meta.color, backgroundColor: meta.soft }"
  >
    <span class="h-1.5 w-1.5 rounded-full" :style="{ backgroundColor: meta.color }" />
    {{ meta.label }}
  </span>
</template>
