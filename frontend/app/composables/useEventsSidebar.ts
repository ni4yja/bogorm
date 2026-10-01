import type { EventListItem, PaginatedResponse } from '~/types'

export function useEventsSidebar() {
  const { get } = useApi()
  const { t } = useI18n()

  const events = ref<EventListItem[]>([])
  const isLoading = ref(false)
  const error = ref('')

  const fetchWeeklyEvents = async () => {
    isLoading.value = true
    error.value = ''

    try {
      const response = await get<PaginatedResponse<EventListItem>>(
        '/events/?status=upcoming&week=current',
      )
      events.value = response.results
    }
    catch {
      error.value = t('eventsSidebar.loadError')
    }
    finally {
      isLoading.value = false
    }
  }

  return { events, isLoading, error, fetchWeeklyEvents }
}
