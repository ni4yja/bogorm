<script setup lang="ts">
import type { Event, PlaceDetail } from '~/types'

definePageMeta({ layout: 'default' })

const { isAuthenticated } = useAuth()
const isBannerVisible = ref(true)

const selectedPlace = ref<PlaceDetail | null>(null)
const selectedEventCount = ref(0)
const selectedEvents = ref<Event[]>([])
const isModalOpen = computed(() => selectedPlace.value !== null)
const sidebarRef = ref<{ closeDetail: () => void } | null>(null)

let mapInstance: Awaited<ReturnType<typeof useLeafletMap>>['map'] | null = null
let highlightMarkerFn: ((placeId: string) => void) | null = null
let clearHighlightFn: (() => void) | null = null

watch(selectedPlace, (place) => {
  if (place)
    sidebarRef.value?.closeDetail()
})

watch(isAuthenticated, (authenticated) => {
  if (!authenticated)
    clearHighlightFn?.()
})

onMounted(async () => {
  const { L, map, markersLayer } = await useLeafletMap('map')
  mapInstance = map

  const { fetchPlaces, highlightMarker, clearHighlight } = useMapMarkers(
    L,
    markersLayer,
    isAuthenticated,
    selectedPlace,
    selectedEventCount,
    selectedEvents,
    isBannerVisible,
  )
  highlightMarkerFn = highlightMarker
  clearHighlightFn = clearHighlight

  await fetchPlaces(map)
  map.on('moveend', () => fetchPlaces(map))
})

function handleSelectEvent(place: { id: string, lat: number, lng: number }) {
  if (!mapInstance)
    return

  selectedPlace.value = null

  mapInstance.flyTo([place.lat, place.lng], 16, { duration: 0.8 })

  mapInstance.once('moveend', () => {
    highlightMarkerFn?.(place.id)
  })
}
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
        <div id="map" />
        <div v-if="isModalOpen" class="map-overlay" />
        <PlaceModal
          v-if="selectedPlace"
          :place="selectedPlace"
          :event-count="selectedEventCount"
          :events="selectedEvents"
          :is-authenticated="isAuthenticated"
          @close="selectedPlace = null; selectedEvents = []; isBannerVisible = true"
        />
        <EventsSidebar v-if="isAuthenticated" ref="sidebarRef" @select-event="handleSelectEvent" />
        <div v-if="isBannerVisible && !isAuthenticated" class="unauth-banner">
          <p>
            Without an account, <strong>you can only view the map with places</strong>.
            To check events' details, note your impressions, and stay up-to-date with literary
            life of Warsaw, you need to <strong>sign up to our platform</strong>.
          </p>
          <NuxtLink to="/register" class="btn-full">
            Get The Full Experience
          </NuxtLink>
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
}

.map-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 950;
}

:deep(.leaflet-top.leaflet-right) {
  top: 50%;
  transform: translateY(-50%);
  right: 1rem;
}

:deep(.leaflet-control-zoom) {
  border-radius: 8px;
  overflow: hidden;
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
  display: inline-block;
  text-decoration: none;
  text-align: center;
}
</style>
