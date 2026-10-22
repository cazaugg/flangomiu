import { defineStore } from 'pinia'
import { ref } from 'vue'

import { knowledgeApi, type KnowledgeEntryPayload, type SubjectPayload } from '@/api'
import type { KnowledgeEntry, Subject } from '@/types'

export const useKnowledgeStore = defineStore('knowledge', () => {
  const subjects = ref<Subject[]>([])
  const entries = ref<KnowledgeEntry[]>([])
  const subject = ref<Subject | null>(null)
  const entry = ref<KnowledgeEntry | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function run<T>(fn: () => Promise<T>): Promise<T | null> {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (e) {
      error.value = (e as Error).message
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchSubjects() {
    const response = await run(() => knowledgeApi.subjects())
    if (response) subjects.value = response.items
  }

  async function fetchSubject(id: number) {
    const response = await run(() => knowledgeApi.subject(id))
    subject.value = response?.subject ?? null
  }

  async function fetchEntries(params?: { subject_id?: number; q?: string }) {
    const response = await run(() => knowledgeApi.entries(params))
    if (response) entries.value = response.items
  }

  async function fetchEntry(id: number) {
    const response = await run(() => knowledgeApi.entry(id))
    entry.value = response?.entry ?? null
  }

  const createSubject = async (payload: SubjectPayload) =>
    (await knowledgeApi.createSubject(payload)).subject
  const updateSubject = async (id: number, payload: Partial<SubjectPayload>) =>
    (await knowledgeApi.updateSubject(id, payload)).subject
  const removeSubject = (id: number) => knowledgeApi.removeSubject(id)

  const createEntry = async (payload: KnowledgeEntryPayload) =>
    (await knowledgeApi.createEntry(payload)).entry
  const updateEntry = async (id: number, payload: Partial<KnowledgeEntryPayload>) =>
    (await knowledgeApi.updateEntry(id, payload)).entry
  const removeEntry = (id: number) => knowledgeApi.removeEntry(id)

  return {
    subjects,
    entries,
    subject,
    entry,
    loading,
    error,
    fetchSubjects,
    fetchSubject,
    fetchEntries,
    fetchEntry,
    createSubject,
    updateSubject,
    removeSubject,
    createEntry,
    updateEntry,
    removeEntry,
  }
})
