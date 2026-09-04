interface ToastState {
  message: string
  actionLabel?: string
  actionTo?: string
}

export function useToast() {
  const toast = useState<ToastState | null>('toast', () => null)
  const timeoutId = useState<ReturnType<typeof setTimeout> | null>('toastTimeout', () => null)

  function show(message: string, action?: { label: string, to: string }) {
    if (timeoutId.value)
      clearTimeout(timeoutId.value)

    toast.value = { message, actionLabel: action?.label, actionTo: action?.to }
    timeoutId.value = setTimeout(() => {
      toast.value = null
    }, 4000)
  }

  function hide() {
    if (timeoutId.value)
      clearTimeout(timeoutId.value)
    toast.value = null
  }

  return { toast, show, hide }
}
