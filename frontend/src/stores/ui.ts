import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ToastTone = 'success' | 'error' | 'info'

export interface Toast {
  id: number
  message: string
  tone: ToastTone
}

let counter = 0

export const useUiStore = defineStore('ui', () => {
  const toasts = ref<Toast[]>([])

  function notify(message: string, tone: ToastTone = 'info') {
    const id = ++counter
    toasts.value.push({ id, message, tone })
    setTimeout(() => dismiss(id), 4000)
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((toast) => toast.id !== id)
  }

  const success = (message: string) => notify(message, 'success')
  const error = (message: string) => notify(message, 'error')

  return { toasts, notify, dismiss, success, error }
})
