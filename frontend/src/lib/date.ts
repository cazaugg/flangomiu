import { differenceInYears, format, parseISO } from 'date-fns'
import { de } from 'date-fns/locale'

export function toDate(value: string | null | undefined): Date | null {
  if (!value) return null
  try {
    return parseISO(value)
  } catch {
    return null
  }
}

export function formatDateTime(value: string | null | undefined): string {
  const date = toDate(value)
  return date ? format(date, "EEE, d. MMM yyyy · HH:mm", { locale: de }) : ''
}

export function formatDate(value: string | null | undefined): string {
  const date = toDate(value)
  return date ? format(date, 'd. MMMM yyyy', { locale: de }) : ''
}

export function formatDay(value: string | null | undefined): string {
  const date = toDate(value)
  return date ? format(date, 'd. MMM', { locale: de }) : ''
}

export function formatRange(start: string | null, stop: string | null, allDay = false): string {
  const from = toDate(start)
  const to = toDate(stop)
  if (!from) return 'Ohne Datum'
  if (!to) return formatDateTime(start)
  const sameDay = from.toDateString() === to.toDateString()
  if (allDay || sameDay) {
    return `${format(from, 'd. MMM yyyy', { locale: de })}${allDay ? ' · ganztägig' : ` · ${format(from, 'HH:mm')}–${format(to, 'HH:mm')}`}`
  }
  return `${format(from, 'd. MMM', { locale: de })} – ${format(to, 'd. MMM yyyy', { locale: de })}`
}

export function birthdayLabel(birthday: string | null): string {
  const date = toDate(birthday)
  if (!date) return ''
  const age = differenceInYears(new Date(), date)
  return `${format(date, 'd. MMMM yyyy', { locale: de })} · ${age} Jahre`
}

/** Convert an ISO/datetime string to a value usable by <input type="datetime-local">. */
export function toLocalInput(value: string | null | undefined): string {
  const date = toDate(value)
  return date ? format(date, "yyyy-MM-dd'T'HH:mm") : ''
}

/** Convert a date-only string to <input type="date"> value. */
export function toDateInput(value: string | null | undefined): string {
  const date = toDate(value)
  return date ? format(date, 'yyyy-MM-dd') : ''
}

export function monthKey(date: Date): string {
  return format(date, 'yyyy-MM')
}
