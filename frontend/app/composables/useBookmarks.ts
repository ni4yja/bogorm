import type { BookmarkItem, PaginatedResponse } from '~/types'

export function useBookmarks() {
  const { get, put, del } = useApi()

  const bookmarkedPlaces = useState<Record<string, boolean>>('bookmarkedPlaces', () => ({}))
  const bookmarkedEvents = useState<Record<string, boolean>>('bookmarkedEvents', () => ({}))

  const isBookmarked = (type: 'place' | 'event', id: string): boolean => {
    const store = type === 'place' ? bookmarkedPlaces : bookmarkedEvents
    return store.value[id] ?? false
  }

  const setBookmarked = (type: 'place' | 'event', id: string, value: boolean) => {
    const store = type === 'place' ? bookmarkedPlaces : bookmarkedEvents
    store.value[id] = value
  }

  const registerInitialState = (type: 'place' | 'event', id: string, value: boolean) => {
    const store = type === 'place' ? bookmarkedPlaces : bookmarkedEvents
    if (!(id in store.value)) {
      store.value[id] = value
    }
  }

  const toggleBookmark = async (type: 'place' | 'event', id: string, title?: string) => {
    const current = isBookmarked(type, id)
    const path = `/${type}s/${id}/bookmark/`

    try {
      const response = current
        ? await del<{ bookmarked: boolean }>(path)
        : await put<{ bookmarked: boolean }>(path)
      setBookmarked(type, id, response.bookmarked)

      if (response.bookmarked && title) {
        const { show } = useToast()
        show(`${title} saved to bookmarks`, { label: 'View bookmarks', to: `/bookmarks?type=${type}` })
      }

      return response.bookmarked
    }
    catch {
      const { show } = useToast()
      show('Could not update bookmark. Please try again.')
      return current
    }
  }

  const fetchBookmarks = async (type: 'place' | 'event', page = 1) => {
    return await get<PaginatedResponse<BookmarkItem>>(`/bookmarks/?type=${type}&page=${page}`)
  }

  return { isBookmarked, registerInitialState, toggleBookmark, fetchBookmarks }
}
