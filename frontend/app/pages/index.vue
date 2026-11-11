<script setup lang="ts">
import type { Event, PlaceDetail } from '~/types'

definePageMeta({ layout: 'default' })
const { t } = useI18n()
const { show } = useToast()

const { isAuthenticated } = useAuth()

// Kept out of the locale files: vue-i18n parses "@" as a linked-message reference
const CONTACT_MAILTO = 'mailto:liubuntu@proton.me'

const selectedPlace = ref<PlaceDetail | null>(null)
const selectedEventCount = ref(0)
const selectedEvents = ref<Event[]>([])
const isModalOpen = computed(() => selectedPlace.value !== null)
const sidebarRef = ref<{ closeDetail: () => void } | null>(null)
const mapWrapperRef = ref<HTMLElement | null>(null)

let mapInstance: Awaited<ReturnType<typeof useLeafletMap>>['map'] | null = null
let highlightMarkerFn: ((placeId: string) => void) | null = null
let clearHighlightFn: (() => void) | null = null

// Leaflet only tracks window resizes, not its container: the map height now depends on
// the notice and footer, so redraw tiles whenever the wrapper itself changes size
useResizeObserver(mapWrapperRef, () => {
  mapInstance?.invalidateSize()
})

watch(selectedPlace, (place: PlaceDetail | null) => {
  if (place)
    sidebarRef.value?.closeDetail()
})

watch(isAuthenticated, (authenticated: boolean) => {
  if (!authenticated)
    clearHighlightFn?.()
})

// useMapMarkers runs after an await, where useI18n is no longer available
function handleLoadError() {
  show(t('home.loadError'))
}

onBeforeUnmount(() => {
  mapInstance?.remove()
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
    handleLoadError,
  )
  highlightMarkerFn = highlightMarker
  clearHighlightFn = clearHighlight

  const refreshPlaces = () => fetchPlaces(map).catch(handleLoadError)

  // Before the first fetch, so a failed load can still recover on the next pan
  map.on('moveend', refreshPlaces)
  await refreshPlaces()
})

function handleSelectEvent(place: { id: string, lat: number, lng: number }) {
  if (!mapInstance)
    return

  selectedPlace.value = null

  mapInstance.flyTo([place.lat, place.lng], 16, { duration: 0.8 })

  // fetchPlaces re-applies this to the marker it creates once the map stops
  highlightMarkerFn?.(place.id)
}
</script>

<template>
  <div class="page">
    <section ref="mapWrapperRef" class="map-wrapper">
      <ClientOnly>
        <div id="map" />
        <div v-if="isModalOpen" class="map-overlay" />
        <PlaceModal
          v-if="selectedPlace"
          :place="selectedPlace"
          :event-count="selectedEventCount"
          :events="selectedEvents"
          :is-authenticated="isAuthenticated"
          @close="selectedPlace = null; selectedEvents = []"
        />
        <EventsSidebar
          v-if="isAuthenticated"
          ref="sidebarRef"
          @select-event="handleSelectEvent"
          @deselect-event="clearHighlightFn?.()"
        />
      </ClientOnly>
    </section>

    <!-- Static and shown to everyone, so it renders on the server with no hydration flash -->
    <aside class="beta-notice">
      <span class="badge">{{ t('home.betaNotice.badge') }}</span>
      <div class="beta-notice-text">
        <p class="beta-notice-lead">
          {{ t('home.betaNotice.lead') }}
        </p>
        <i18n-t keypath="home.betaNotice.invite" tag="p" scope="global">
          <template #email>
            <a :href="CONTACT_MAILTO" class="beta-notice-link">{{ t('home.betaNotice.email') }}</a>
          </template>
        </i18n-t>
      </div>
    </aside>
  </div>
</template>

<style scoped>
/* Fills the space between header and footer; the map takes whatever the notice leaves */
.page {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-top: var(--header-height);
}

.map-wrapper {
  position: relative;
  flex: 1;
  /* Below this the page scrolls instead of squashing the map into a strip */
  min-height: 360px;
  margin: var(--spacing-xs) var(--spacing-md);
  border-radius: 16px;
  overflow: hidden;
}

/* Absolute so Leaflet gets exact pixel dimensions; percentage heights in a flex column often resolve to 0 */
#map {
  position: absolute;
  inset: 0;
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

/* Yellow card below the map: the only copy on the first screen, so it should stand out */
.beta-notice {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin: 0 var(--spacing-md) var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-md);
  background: var(--color-yellow);
  color: var(--color-primary);
  border-radius: 12px;
}

.beta-notice .badge {
  flex-shrink: 0;
  margin-top: 0.15rem;
}

.beta-notice-text p {
  font-size: 0.9rem;
  color: inherit;
  line-height: 1.5;
  margin: 0;
}

.beta-notice-lead {
  font-weight: 500;
}

.beta-notice-link {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 2px;
  overflow-wrap: anywhere;
}

@media (max-width: 640px) {
  .map-wrapper {
    min-height: 280px;
  }

  .beta-notice {
    flex-direction: column;
    gap: 0.5rem;
    padding: var(--spacing-xs);
  }
}
</style>
