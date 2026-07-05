<script setup lang="ts">
import type { Event, MapResponse, PaginatedResponse, PlaceDetail } from '~/types'

definePageMeta({ layout: 'default' })
const { get } = useApi()

const isAuthenticated = true
const isBannerVisible = ref(true)

const selectedPlace = ref<PlaceDetail | null>(null)
const selectedEventCount = ref(0)
const selectedEvents = ref<Event[]>([])
const isModalOpen = computed(() => selectedPlace.value !== null)

onMounted(async () => {
  const L = await import('leaflet')

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
      const marker = L.marker([place.lat, place.lng], {
        icon: createIcon(place.category, place.event_count > 0),
      }).addTo(markersLayer)
      marker.on('click', async () => {
        isBannerVisible.value = false
        const detail = await get<PlaceDetail>(`/places/${place.id}/`)
        selectedPlace.value = detail
        selectedEventCount.value = place.event_count

        if (isAuthenticated && place.event_count > 0) {
          const response = await get<PaginatedResponse<Event>>(`/places/${place.id}/events/`)
          selectedEvents.value = response.results
        }
        else {
          selectedEvents.value = []
        }
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
          :events="selectedEvents"
          :is-authenticated="isAuthenticated"
          @close="selectedPlace = null; selectedEvents = []; isBannerVisible = true"
        />
        <div v-if="isBannerVisible" class="unauth-banner">
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
