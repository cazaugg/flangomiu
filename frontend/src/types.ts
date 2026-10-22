export type EventKind =
  | 'event'
  | 'event_excursion'
  | 'event_vacation'
  | 'event_festival'
  | 'event_project'
  | 'event_birthday'
  | 'appointment'
  | 'task'

export type StoredEventKind = EventKind

export interface Picture {
  id: number
  name: string
  description: string
  url: string
  thumb: string
}

export interface Person {
  id: number
  name: string
  description: string
  birthday: string | null
  picture: Picture | null
}

export interface EventItem {
  id: number
  title: string
  kind: EventKind
  description: string
  location: string
  start: string | null
  stop: string | null
  all_day: boolean
  is_done: boolean
  cover: Picture | null
  picture_count: number
  people: Person[]
  pictures: Picture[]
}

export interface Tag {
  id: number
  name: string
}

export interface PinUser {
  id: number
  username: string
  name: string
}

export interface PinItem {
  id: number
  author: string
  text: string
  image: Picture | null
  tags: Tag[]
  user: PinUser | null
  created_at: string | null
  updated_at: string | null
}

export interface DiaryYear {
  year: number
  count: number
  cover: Picture | null
}

export interface Subject {
  id: number
  name: string
  description: string
  position: number
  entry_count: number
  created_at: string | null
  updated_at: string | null
  entries?: KnowledgeEntry[]
}

export interface KnowledgeEntry {
  id: number
  subject_id: number
  title: string
  content?: string
  excerpt: string
  subject?: Subject | null
  subject_name?: string
  created_at: string | null
  updated_at: string | null
}

export interface User {
  id: number
  username: string
  write_access: boolean
  person: Person | null
}
