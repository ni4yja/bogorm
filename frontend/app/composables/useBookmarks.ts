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

  const toggleBookmark = async (type: 'place' | 'event', id: string) => {
    const current = isBookmarked(type, id)
    const path = `/${type}s/${id}/bookmark/`
    const response = current
      ? await del<{ bookmarked: boolean }>(path)
      : await put<{ bookmarked: boolean }>(path)
    setBookmarked(type, id, response.bookmarked)
    return response.bookmarked
  }

  const fetchBookmarks = async (type: 'place' | 'event', page = 1) => {
    return await get<PaginatedResponse<BookmarkItem>>(`/bookmarks/?type=${type}&page=${page}`)
  }

  return { isBookmarked, registerInitialState, toggleBookmark, fetchBookmarks }
}
