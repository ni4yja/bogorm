export async function useLeafletMap() {
  const L = await import('leaflet')

  const map = L.map('map', { zoomControl: false }).setView([52.23, 21.01], 13)

  L.control.zoom({ position: 'topright' }).addTo(map)

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors © CARTO',
  }).addTo(map)

  const markersLayer = L.layerGroup().addTo(map)

  return { L, map, markersLayer }
}
