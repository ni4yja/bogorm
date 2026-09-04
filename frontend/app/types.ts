export interface Place {
  id: string
  title: string
  lat: number
  lng: number
  category: number
  event_count: number
}

export interface PlaceDetail {
  id: string
  title: string
  description: string
  lat: number
  lng: number
  category: number
  address: string
  website: string
  is_bookmarked: boolean
}

export interface PlaceMinimal {
  id: string
  title: string
  lat: number
  lng: number
}

export interface MapResponse {
  places: Place[]
}

export interface Event {
  id: string
  title: string
  description: string
  event_time: string | null
  category: number
  is_bookmarked: boolean
}

export interface EventListItem extends Event {
  place: PlaceMinimal
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface BookmarkPlaceTarget {
  type: 'place'
  id: string
  title: string
  lat: number
  lng: number
}

export interface BookmarkEventTarget {
  type: 'event'
  id: string
  title: string
  event_time: string | null
  category: number
}

export type BookmarkTarget = BookmarkPlaceTarget | BookmarkEventTarget

export interface BookmarkItem {
  id: string
  type: 'place' | 'event'
  target: BookmarkTarget
  created_at: string
}
