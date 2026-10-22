import type {
  DiaryYear,
  EventItem,
  EventKind,
  KnowledgeEntry,
  Person,
  Picture,
  PinItem,
  Subject,
  User,
} from '@/types'
import { api } from './client'

function qs(params?: Record<string, string | number | undefined>): string {
  if (!params) return ''
  const search = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== '') search.set(key, String(value))
  }
  const query = search.toString()
  return query ? `?${query}` : ''
}

export interface EventPayload {
  title?: string
  kind?: EventKind
  description?: string
  location?: string
  start?: string | null
  stop?: string | null
  all_day?: boolean
  cover_picture_id?: number | null
  people_ids?: number[]
  picture_ids?: number[]
}

export interface PersonPayload {
  name: string
  description?: string
  birthday?: string | null
  picture_id?: number | null
}

export interface PinPayload {
  author?: string
  text?: string
  tags?: string[]
  remove_image?: boolean
}

function pinForm(payload: PinPayload, file?: File | null): FormData {
  const form = new FormData()
  form.append('author', payload.author ?? '')
  form.append('text', payload.text ?? '')
  form.append('tags', (payload.tags ?? []).join(','))
  if (payload.remove_image) form.append('remove_image', '1')
  if (file) form.append('file', file)
  return form
}

export const authApi = {
  me: () => api.get<{ user: User | null }>('/auth/me'),
  login: (username: string, password: string) =>
    api.post<{ user: User }>('/auth/login', { username, password }),
  logout: () => api.post<{ ok: boolean }>('/auth/logout'),
}

export const eventsApi = {
  list: (params?: { kind?: string; from?: string; to?: string }) =>
    api.get<{ items: EventItem[] }>(`/events${qs(params)}`),
  get: (id: number | string) => api.get<{ event: EventItem }>(`/events/${id}`),
  create: (payload: EventPayload) => api.post<{ event: EventItem }>('/events', payload),
  update: (id: number | string, payload: EventPayload) =>
    api.put<{ event: EventItem }>(`/events/${id}`, payload),
  remove: (id: number | string) => api.del<{ ok: boolean }>(`/events/${id}`),
  uploadPictures: (id: number | string, files: File[]) => {
    const form = new FormData()
    files.forEach((file) => form.append('files', file))
    return api.post<{ event: EventItem }>(`/events/${id}/pictures`, form)
  },
  removePicture: (eventId: number | string, pictureId: number) =>
    api.del<{ event: EventItem }>(`/events/${eventId}/pictures/${pictureId}`),
  reorderPictures: (eventId: number | string, pictureIds: number[]) =>
    api.put<{ event: EventItem }>(`/events/${eventId}/pictures/order`, {
      picture_ids: pictureIds,
    }),
}

export const peopleApi = {
  list: () => api.get<{ items: Person[] }>('/people'),
  create: (payload: PersonPayload) => api.post<{ person: Person }>('/people', payload),
  update: (id: number, payload: PersonPayload) =>
    api.put<{ person: Person }>(`/people/${id}`, payload),
  remove: (id: number) => api.del<{ ok: boolean }>(`/people/${id}`),
}

export const tasksApi = {
  list: (status: 'all' | 'open' | 'done' = 'all') =>
    api.get<{ items: EventItem[] }>(`/tasks${qs({ status })}`),
  create: (payload: EventPayload) => api.post<{ task: EventItem }>('/tasks', payload),
  update: (id: number | string, payload: EventPayload) =>
    api.put<{ task: EventItem }>(`/tasks/${id}`, payload),
  remove: (id: number | string) => api.del<{ ok: boolean }>(`/tasks/${id}`),
}

export const calendarApi = {
  range: (start: string, end: string) =>
    api.get<{ items: EventItem[] }>(`/calendar${qs({ start, end })}`),
}

export const diaryApi = {
  year: (year: number) => api.get<{ year: number; items: EventItem[] }>(`/diary${qs({ year })}`),
  years: () => api.get<{ items: DiaryYear[] }>('/diary/years'),
}

export const pinsApi = {
  list: () => api.get<{ items: PinItem[] }>('/pins'),
  create: (payload: PinPayload, file?: File | null) =>
    api.post<{ pin: PinItem }>('/pins', pinForm(payload, file)),
  update: (id: number, payload: PinPayload, file?: File | null) =>
    api.put<{ pin: PinItem }>(`/pins/${id}`, pinForm(payload, file)),
  remove: (id: number) => api.del<{ ok: boolean }>(`/pins/${id}`),
}

export const picturesApi = {
  list: () => api.get<{ items: Picture[] }>('/pictures'),
  upload: (file: File, name?: string, description?: string) => {
    const form = new FormData()
    form.append('file', file)
    if (name) form.append('name', name)
    if (description) form.append('description', description)
    return api.post<{ picture: Picture }>('/pictures', form)
  },
  update: (id: number, payload: { name?: string; description?: string }) =>
    api.patch<{ picture: Picture }>(`/pictures/${id}`, payload),
  remove: (id: number) => api.del<{ ok: boolean }>(`/pictures/${id}`),
}

export interface SubjectPayload {
  name: string
  description?: string
  position?: number
}

export interface KnowledgeEntryPayload {
  title: string
  subject_id: number
  content?: string
}

export const knowledgeApi = {
  subjects: () => api.get<{ items: Subject[] }>('/knowledge/subjects'),
  subject: (id: number) => api.get<{ subject: Subject }>(`/knowledge/subjects/${id}`),
  createSubject: (payload: SubjectPayload) =>
    api.post<{ subject: Subject }>('/knowledge/subjects', payload),
  updateSubject: (id: number, payload: Partial<SubjectPayload>) =>
    api.put<{ subject: Subject }>(`/knowledge/subjects/${id}`, payload),
  removeSubject: (id: number) => api.del<{ ok: boolean }>(`/knowledge/subjects/${id}`),
  entries: (params?: { subject_id?: number; q?: string }) =>
    api.get<{ items: KnowledgeEntry[] }>(`/knowledge/entries${qs(params)}`),
  entry: (id: number) => api.get<{ entry: KnowledgeEntry }>(`/knowledge/entries/${id}`),
  createEntry: (payload: KnowledgeEntryPayload) =>
    api.post<{ entry: KnowledgeEntry }>('/knowledge/entries', payload),
  updateEntry: (id: number, payload: Partial<KnowledgeEntryPayload>) =>
    api.put<{ entry: KnowledgeEntry }>(`/knowledge/entries/${id}`, payload),
  removeEntry: (id: number) => api.del<{ ok: boolean }>(`/knowledge/entries/${id}`),
}
