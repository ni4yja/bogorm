export interface Place {
  id: string
  title: string
  lat: number
  lng: number
  category: number
  event_count: number
}

export interface MapResponse {
  places: Place[]
}
