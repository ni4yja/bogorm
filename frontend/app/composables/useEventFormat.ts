// Bogorm is a Warsaw map: events happen in Warsaw, so their time is always shown
// in Warsaw time, regardless of the viewer's device timezone
const EVENT_TIME_ZONE = 'Europe/Warsaw'

export function useEventFormat() {
  const { localeProperties } = useI18n()

  function formatEventTime(eventTime: string | null) {
    if (!eventTime)
      return ''
    return new Date(eventTime).toLocaleString(localeProperties.value.language, {
      timeZone: EVENT_TIME_ZONE,
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return { formatEventTime }
}
