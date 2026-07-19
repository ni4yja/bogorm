export function useMapIcons(L: typeof import('leaflet')) {
  const categoryToIcon: Record<number, string> = {
    10: 'library',
    20: 'bookshop',
    30: 'cultural-centre',
    40: 'cafe',
    50: 'museum',
    60: 'other',
  }

  const createIcon = (category: number, hasEvents: boolean) => {
    if (hasEvents) {
      return L.divIcon({
        html: `
          <div style="position: relative; width: 48px; height: 64px;">
            <img src="/icons/marker-${categoryToIcon[category] ?? 'other'}.svg" width="48" height="64" />
            <img src="/icons/upcoming-events.svg" width="24" height="24" style="position: absolute; top: -2px; right: -4px;" />
          </div>
        `,
        className: '',
        iconSize: [48, 64],
        iconAnchor: [24, 64],
        popupAnchor: [0, -64],
      })
    }

    return L.icon({
      iconUrl: `/icons/marker-${categoryToIcon[category] ?? 'other'}.svg`,
      iconSize: [48, 64],
      iconAnchor: [24, 64],
      popupAnchor: [0, -64],
    })
  }

  return { createIcon }
}
