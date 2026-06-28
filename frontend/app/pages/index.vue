<script setup lang="ts">
import type { MapResponse, PlaceDetail } from '~/types'

definePageMeta({ layout: 'default' })
const { get } = useApi()

const selectedPlace = ref<PlaceDetail | null>(null)
const selectedEventCount = ref(0)
const isModalOpen = computed(() => selectedPlace.value !== null)

onMounted(async () => {
  const L = await import('leaflet')

  const markerIcon = await import('leaflet/dist/images/marker-icon.png')
  const markerIcon2x = await import('leaflet/dist/images/marker-icon-2x.png')
  const markerShadow = await import('leaflet/dist/images/marker-shadow.png')

  delete (L.Icon.Default.prototype as any)._getIconUrl
  L.Icon.Default.mergeOptions({
    iconUrl: markerIcon.default,
    iconRetinaUrl: markerIcon2x.default,
    shadowUrl: markerShadow.default,
  })

  const map = L.map('map').setView([52.23, 21.01], 13)

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors © CARTO',
  }).addTo(map)

  const markersLayer = L.layerGroup().addTo(map)

  const fetchPlaces = async () => {
    const bounds = map.getBounds()
    const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`
    const data = await get<MapResponse>(`/map?bbox=${bbox}`)

    markersLayer.clearLayers()

    for (const place of data.places) {
      const marker = L.marker([place.lat, place.lng]).addTo(markersLayer)
      marker.on('click', async () => {
        const detail = await get<PlaceDetail>(`/places/${place.id}/`)
        selectedPlace.value = detail
        selectedEventCount.value = place.event_count
      })
    }
  }

  await fetchPlaces()
  map.on('moveend', fetchPlaces)
})
</script>

<template>
  <div class="page">
    <section class="hero">
      <h1>
        Reading doesn't have to be a lonely habit!
      </h1>
      <p class="hero-subtitle">
        Discover places, events, and people around books.<br>
        It's totally free. And absolutely fun!
      </p>
    </section>

    <section class="map-wrapper">
      <ClientOnly>
        <div id="map" :class="{ dimmed: isModalOpen }" />
        <PlaceModal
          v-if="selectedPlace"
          :place="selectedPlace"
          :event-count="selectedEventCount"
          @close="selectedPlace = null"
        />
        <div class="unauth-banner">
          <p>
            Without an account, <strong>you can only view the map with places</strong>.
            To check events' details, note your impressions, and stay up-to-date with literary
            life of Warsaw, you need to <strong>sign up to our platform</strong>.
          </p>
          <button class="btn-full">
            Get The Full Experience
          </button>
        </div>
      </ClientOnly>
    </section>
  </div>
</template>

<style scoped>
.page {
  padding-top: var(--header-height);
}

.hero {
  text-align: center;
  padding: var(--spacing-lg) var(--spacing-md) var(--spacing-xl);
}

.hero h1 {
  margin-bottom: var(--spacing-xs);
}

.hero-subtitle {
  color: #313131;
}

.map-wrapper {
  position: relative;
  margin: 0 var(--spacing-md) var(--spacing-md);
  border-radius: 16px;
  overflow: hidden;
}

#map {
  height: 620px;
  width: 100%;
  transition: filter 0.2s ease;
}

#map.dimmed {
  filter: brightness(0.85);
}

.unauth-banner {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  right: 1.5rem;
  background: #fff;
  border-radius: 12px;
  padding: var(--spacing-xs) var(--spacing-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.unauth-banner p {
  font-size: 0.9rem;
  color: #444;
  line-height: 1.5;
  margin: 0;
}

.btn-full {
  white-space: nowrap;
  background: var(--color-primary);
  color: #fff;
  border: none;
  padding: 0.85rem 1.75rem;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
}
</style>
