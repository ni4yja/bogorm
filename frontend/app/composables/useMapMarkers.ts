import type { Event, MapResponse, PaginatedResponse, PlaceDetail } from '~/types'

export function useMapMarkers(
  L: typeof import('leaflet'),
  markersLayer: ReturnType<typeof L.layerGroup>,
  isAuthenticated: Ref<boolean>,
  selectedPlace: Ref<PlaceDetail | null>,
  selectedEventCount: Ref<number>,
  selectedEvents: Ref<Event[]>,
  isBannerVisible: Ref<boolean>,
) {
  const { get } = useApi()
  const { createIcon } = useMapIcons(L)

  let latestClickId = ''
  const markersById = new Map<string, InstanceType<typeof L.Marker>>()
  let highlightedMarkerId: string | null = null

  const fetchPlaces = async (map: ReturnType<typeof L.map>) => {
    const bounds = map.getBounds()
    const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`
    const data = await get<MapResponse>(`/map?bbox=${bbox}`)

    markersLayer.clearLayers()
    markersById.clear()

    for (const place of data.places) {
      const marker = L.marker([place.lat, place.lng], {
        icon: createIcon(place.category, place.event_count > 0),
      }).addTo(markersLayer)

      markersById.set(place.id, marker)

      if (place.id === highlightedMarkerId)
        marker.getElement()?.classList.add('marker-highlighted')

      marker.on('click', async () => {
        const clickId = place.id
        latestClickId = clickId

        isBannerVisible.value = false
        const detail = await get<PlaceDetail>(`/places/${place.id}/`)
        if (latestClickId !== clickId)
          return

        selectedPlace.value = detail
        selectedEventCount.value = place.event_count

        if (isAuthenticated.value && place.event_count > 0) {
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

  const clearHighlight = () => {
    if (highlightedMarkerId) {
      const previous = markersById.get(highlightedMarkerId)
      previous?.getElement()?.classList.remove('marker-highlighted')
      highlightedMarkerId = null
    }
  }

  const highlightMarker = (placeId: string) => {
    clearHighlight()
    const marker = markersById.get(placeId)
    marker?.getElement()?.classList.add('marker-highlighted')
    highlightedMarkerId = placeId
  }

  return { fetchPlaces, highlightMarker, clearHighlight }
}
