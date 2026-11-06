import type { EventListItem } from '~/types'

export function useEventsSidebar() {
  const { getAll } = useApi()
  const { t } = useI18n()

  const events = ref<EventListItem[]>([])
  const isLoading = ref(false)
  // ponytail: track a flag, not the translated string, so `error` re-translates
  // on its own if the user switches locale after a failed fetch instead of
  // getting stuck in whatever language was active when the fetch failed.
  const hasError = ref(false)
  const error = computed(() => hasError.value ? t('eventsSidebar.loadError') : '')

  const fetchWeeklyEvents = async () => {
    isLoading.value = true
    hasError.value = false

    try {
      events.value = await getAll<EventListItem>('/events/?status=upcoming&week=current')
    }
    catch {
      hasError.value = true
    }
    finally {
      isLoading.value = false
    }
  }

  return { events, isLoading, error, fetchWeeklyEvents }
}
