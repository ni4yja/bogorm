import type { BookmarkItem, PaginatedResponse } from '~/types'

export function useBookmarks() {
  const { get, put, del } = useApi()

  const bookmarkedPlaces = useState<Record<string, boolean>>('bookmarkedPlaces', () => ({}))
  const bookmarkedEvents = useState<Record<string, boolean>>('bookmarkedEvents', () => ({}))
  const pendingIds = useState<Record<string, boolean>>('bookmarkPendingIds', () => ({}))

  const getStore = (type: 'place' | 'event') => type === 'place' ? bookmarkedPlaces : bookmarkedEvents

  const isBookmarked = (type: 'place' | 'event', id: string): boolean => {
    return getStore(type).value[id] ?? false
  }

  const setBookmarked = (type: 'place' | 'event', id: string, value: boolean) => {
    getStore(type).value[id] = value
  }

  const registerInitialState = (type: 'place' | 'event', id: string, value: boolean) => {
    const store = getStore(type)
    if (!(id in store.value)) {
      store.value[id] = value
    }
  }

  const isPending = (type: 'place' | 'event', id: string): boolean => {
    return pendingIds.value[`${type}:${id}`] ?? false
  }

  const toggleBookmark = async (type: 'place' | 'event', id: string, title?: string) => {
    const current = isBookmarked(type, id)
    const key = `${type}:${id}`
    if (pendingIds.value[key]) {
      return current
    }

    pendingIds.value[key] = true
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
    finally {
      delete pendingIds.value[key]
    }
  }

  const fetchBookmarks = async (type: 'place' | 'event', page = 1) => {
    return await get<PaginatedResponse<BookmarkItem>>(`/bookmarks/?type=${type}&page=${page}`)
  }

  return { isBookmarked, isPending, registerInitialState, toggleBookmark, fetchBookmarks }
}
