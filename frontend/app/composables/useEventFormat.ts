export function useEventFormat() {
  function formatEventTime(eventTime: string | null) {
    if (!eventTime)
      return ''
    return new Date(eventTime).toLocaleString('pl-PL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return { formatEventTime }
}
