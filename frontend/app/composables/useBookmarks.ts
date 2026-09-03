import type { BookmarkItem, PaginatedResponse } from '~/types'

export function useBookmarks() {
  const { get, put, del } = useApi()

  const toggleBookmark = async (type: 'place' | 'event', id: string, isBookmarked: boolean) => {
    const path = `/${type}s/${id}/bookmark/`
    const response = isBookmarked
      ? await del<{ bookmarked: boolean }>(path)
      : await put<{ bookmarked: boolean }>(path)
    return response.bookmarked
  }

  const fetchBookmarks = async (type: 'place' | 'event', page = 1) => {
    return await get<PaginatedResponse<BookmarkItem>>(`/bookmarks/?type=${type}&page=${page}`)
  }

  return { toggleBookmark, fetchBookmarks }
}
