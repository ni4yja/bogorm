import type { Event, MapResponse, PaginatedResponse, PlaceDetail } from '~/types'

export function useMapMarkers(L: typeof import('leaflet'), markersLayer: ReturnType<typeof L.layerGroup>, isAuthenticated: boolean, selectedPlace: Ref<PlaceDetail | null>, selectedEventCount: Ref<number>, selectedEvents: Ref<Event[]>, isBannerVisible: Ref<boolean>) {
  const { get } = useApi()
  const { createIcon } = useMapIcons(L)

  let latestClickId = ''

  const fetchPlaces = async (map: ReturnType<typeof L.map>) => {
    const bounds = map.getBounds()
    const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`
    const data = await get<MapResponse>(`/map?bbox=${bbox}`)

    markersLayer.clearLayers()

    for (const place of data.places) {
      const marker = L.marker([place.lat, place.lng], {
        icon: createIcon(place.category, place.event_count > 0),
      }).addTo(markersLayer)

      marker.on('click', async () => {
        const clickId = place.id
        latestClickId = clickId

        isBannerVisible.value = false
        const detail = await get<PlaceDetail>(`/places/${place.id}/`)
        if (latestClickId !== clickId)
          return

        selectedPlace.value = detail
        selectedEventCount.value = place.event_count

        if (isAuthenticated && place.event_count > 0) {
          const response = await get<PaginatedResponse<Event>>(`/places/${place.id}/events/`)
          if (latestClickId !== clickId)
            return
          selectedEvents.value = response.results
        }
        else {
          selectedEvents.value = []
        }
      })
    }
  }

  return { fetchPlaces }
}
