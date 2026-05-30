<script setup lang="ts">
import type { MapResponse } from '~/types'

const { get } = useApi()

onMounted(async () => {
  const L = await import('leaflet')

  const map = L.map('map').setView([52.23, 21.01], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map)

  const bounds = map.getBounds()
  const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`

  const data = await get<MapResponse>(`/map?bbox=${bbox}`)

  for (const place of data.places) {
    L.marker([place.lat, place.lng])
      .addTo(map)
      .bindPopup(place.title)
  }
})
</script>

<template>
  <div id="map" />
</template>

<style>
#map {
  height: 100vh;
  width: 100%;
}
</style>
