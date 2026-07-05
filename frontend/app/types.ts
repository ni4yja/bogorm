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
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
