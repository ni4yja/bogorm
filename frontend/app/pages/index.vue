<script setup lang="ts">
import type { MapResponse } from '~/types'

const { get } = useApi()

onMounted(async () => {
  const L = await import('leaflet')

  const map = L.map('map').setView([52.23, 21.01], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map)

  const markersLayer = L.layerGroup().addTo(map)

  const fetchPlaces = async () => {
    const bounds = map.getBounds()
    const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`

    const data = await get<MapResponse>(`/map?bbox=${bbox}`)

    markersLayer.clearLayers()

    for (const place of data.places) {
      L.marker([place.lat, place.lng])
        .addTo(markersLayer)
        .bindPopup(place.title)
    }
  }

  await fetchPlaces()
  map.on('moveend', fetchPlaces)
})
</script>

<template>
  <div class="page">
    <section class="hero">
      <h1 class="hero-title">
        Reading doesn't have to be a lonely habit!
      </h1>
      <p class="hero-subtitle">
        Discover places, events, and people around books.<br>
        It's totally free. And absolutely fun!
      </p>
    </section>

    <section class="map-wrapper">
      <div id="map" />
    </section>
  </div>
</template>

<style scoped>
.page {
  padding-top: 60px;
}

.hero {
  text-align: center;
  padding: 3rem 2rem 2.5rem;
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  color: #2c1810;
  line-height: 1.15;
  margin-bottom: 1.25rem;
}

.hero-subtitle {
  font-size: 1rem;
  color: #555;
  line-height: 1.7;
}

.map-wrapper {
  margin: 0 2rem 2rem;
  border-radius: 16px;
  overflow: hidden;
}

#map {
  height: 620px;
  width: 100%;
}
</style>
