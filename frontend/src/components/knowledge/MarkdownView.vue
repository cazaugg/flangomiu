<script setup lang="ts">
import { computed } from 'vue'
import DOMPurify from 'dompurify'
import { marked } from 'marked'

const props = defineProps<{ content: string }>()

const html = computed(() => {
  const raw = marked.parse(props.content || '', {
    async: false,
    gfm: true,
    breaks: true,
  }) as string
  return DOMPurify.sanitize(raw, { USE_PROFILES: { html: true } })
})
</script>

<template>
  <div class="markdown-body prose max-w-none" v-html="html" />
</template>
