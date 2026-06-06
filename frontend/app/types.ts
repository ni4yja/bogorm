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
