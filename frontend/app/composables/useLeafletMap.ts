export async function useLeafletMap(elementId: string) {
  const L = await import('leaflet')
  const config = useRuntimeConfig()

  const map = L.map(elementId, { zoomControl: false }).setView([52.23, 21.01], 13)

  L.control.zoom({ position: 'topright' }).addTo(map)

  L.tileLayer(
    `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png?key=${config.public.cartoApiKey}`,
    {
      attribution: '© OpenStreetMap contributors © CARTO',
    },
  ).addTo(map)

  const markersLayer = L.layerGroup().addTo(map)

  return { L, map, markersLayer }
}
