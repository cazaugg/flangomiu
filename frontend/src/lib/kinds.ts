import type { EventKind } from '@/types'

export interface KindMeta {
  label: string
  color: string
  soft: string
  icon: string
}

export const KIND_META: Record<EventKind, KindMeta> = {
  event: { label: 'Erlebnis', color: '#EE6C5A', soft: '#FFE1DA', icon: '✨' },
  event_excursion: { label: 'Ausflug', color: '#E28A4C', soft: '#FBE6D3', icon: '🥾' },
  event_vacation: { label: 'Ferien', color: '#6E9B6B', soft: '#E3EBDF', icon: '🏖️' },
  event_festival: { label: 'Fest', color: '#C0556A', soft: '#F6DCE2', icon: '🎉' },
  event_project: { label: 'Projekt', color: '#8A6A4F', soft: '#EDE3D9', icon: '🛠️' },
  event_birthday: { label: 'Geburtstag', color: '#B5643E', soft: '#F3DED3', icon: '🎂' },
  appointment: { label: 'Termin', color: '#C08A3E', soft: '#F6E7CB', icon: '📍' },
  task: { label: 'Aufgabe', color: '#A8432F', soft: '#F0DAD3', icon: '✓' },
}

export const EVENT_KINDS: EventKind[] = [
  'event',
  'event_excursion',
  'event_vacation',
  'event_festival',
  'event_project',
  'event_birthday',
]

export function isEventKind(kind: EventKind | string): boolean {
  return EVENT_KINDS.includes(kind as EventKind)
}

export function kindMeta(kind: EventKind | string): KindMeta {
  return KIND_META[kind as EventKind] ?? KIND_META.event
}
