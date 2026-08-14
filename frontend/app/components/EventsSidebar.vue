<script setup lang="ts">
import type { EventListItem } from '~/types'

type SidebarState = 'list' | 'detail' | 'collapsed'

const emit = defineEmits<{
  selectEvent: [place: { id: string, lat: number, lng: number }]
}>()

const { events, isLoading, error, fetchWeeklyEvents } = useEventsSidebar()
const { getCategoryLabel } = useEventCategory()

const state = ref<SidebarState>('list')
const selectedEvent = ref<EventListItem | null>(null)

onMounted(() => {
  fetchWeeklyEvents()
})

function openDetail(event: EventListItem) {
  selectedEvent.value = event
  state.value = 'detail'
  emit('selectEvent', {
    id: event.place.id,
    lat: event.place.lat,
    lng: event.place.lng,
  })
}

function closeDetail() {
  selectedEvent.value = null
  state.value = 'list'
}

defineExpose({ closeDetail })

function toggleCollapse() {
  state.value = state.value === 'collapsed' ? 'list' : 'collapsed'
}

function formatEventTime(eventTime: string | null) {
  if (!eventTime)
    return ''
  return new Date(eventTime).toLocaleString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <div class="sidebar">
    <template v-if="state === 'detail' && selectedEvent">
      <button class="back-row" @click="closeDetail">
        <IconsArrowLeft class="back-icon" />
        To All Events This Week
      </button>

      <div class="detail-scroll">
        <div class="image-placeholder">
          <IconsImage class="image-icon" />
        </div>

        <div class="badges">
          <div class="badge">
            {{ getCategoryLabel(selectedEvent.category) }}
          </div>
        </div>

        <div class="detail-content">
          <h3 class="event-title-lg">
            {{ selectedEvent.title }}
          </h3>

          <p v-if="selectedEvent.description" class="description">
            {{ selectedEvent.description }}
          </p>

          <div class="meta">
            <div class="meta-item">
              <IconsPin class="meta-icon" />
              <span>{{ selectedEvent.place.title }}</span>
            </div>
            <div v-if="selectedEvent.event_time" class="meta-item">
              <IconsTime class="meta-icon" />
              <span>{{ formatEventTime(selectedEvent.event_time) }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template v-else>
      <button class="header-row" @click="toggleCollapse">
        <h3 class="header-title">
          <IconsCalendar class="header-icon" />
          Events This Week
        </h3>
        <IconsChevronDown class="chevron" :class="{ open: state === 'list' }" />
      </button>

      <div v-if="state === 'list'" class="events-list">
        <div v-if="isLoading" class="state-message">
          Loading…
        </div>
        <div v-else-if="error" class="state-message">
          {{ error }}
        </div>
        <div v-else-if="events.length === 0" class="empty-state">
          <p class="empty-title">
            No events this week
          </p>
          <p class="empty-subtitle">
            Check back later or browse all upcoming events below.
          </p>
        </div>
        <button
          v-for="event in events"
          :key="event.id"
          class="event-item"
          @click="openDetail(event)"
        >
          <h4 class="event-title">
            {{ event.title }}
          </h4>
          <div v-if="event.event_time" class="event-meta">
            <IconsTime class="meta-icon" />
            {{ formatEventTime(event.event_time) }}
          </div>
          <div class="event-meta">
            <IconsPin class="meta-icon" />
            <p class="place-title">
              {{ event.place.title }}
            </p>
          </div>
        </button>
      </div>

      <NuxtLink to="/events" class="see-all-btn">
        <IconsCalendar class="see-all-icon" />
        See All Upcoming Events
      </NuxtLink>
    </template>
  </div>
</template>

<style scoped>
.sidebar {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  width: 400px;
  max-height: calc(100% - 3rem);
  background: var(--color-white);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
  z-index: 900;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 1.25rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-primary);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0;
}

.header-icon {
  width: 20px;
  height: 20px;
  color: var(--color-primary);
}

.chevron {
  width: 18px;
  height: 18px;
  color: var(--color-primary);
  transition: transform 0.15s ease;
}

.chevron.open {
  transform: rotate(180deg);
}

.events-list {
  overflow-y: auto;
  padding: 0 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.state-message {
  color: var(--color-grey);
  font-size: 0.9rem;
  padding: 1rem 0 1.5rem;
}

.empty-state {
  padding: 0.5rem 0 1.5rem;
}

.empty-title {
  font-weight: 500;
  color: var(--color-primary);
  margin: 0 0 0.35rem;
}

.empty-subtitle {
  font-size: 0.85rem;
  color: var(--color-grey);
  margin: 0;
}

.event-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  text-align: left;
  background: none;
  border: none;
  padding: 0 0 1.25rem;
  border-bottom: 1px solid var(--color-light-grey-40);
  cursor: pointer;
}

.event-item:last-child {
  border-bottom: none;
  padding-bottom: 0.5rem;
}

.event-title {
  margin: 0;
}

.event-meta {
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: var(--color-primary);
  flex-shrink: 0;
}

.place-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.see-all-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 1.25rem 1.5rem 1.5rem;
  padding: 0.75rem;
  border: 1.5px solid var(--color-primary);
  border-radius: 8px;
  color: var(--color-primary);
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
}

.see-all-icon {
  width: 18px;
  height: 18px;
}

/* --- detail state --- */

.back-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  width: 100%;
  padding: 1.25rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: var(--color-primary);
}

.back-icon {
  width: 20px;
  height: 20px;
}

.detail-scroll {
  overflow-y: auto;
}

.image-placeholder {
  width: 100%;
  height: 200px;
  background: var(--color-light-grey-40);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-icon {
  width: 64px;
  height: 50px;
  color: var(--color-grey);
}

.badges {
  padding: 0 1.5rem;
  margin-top: -0.9rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 0.75rem;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
}

.detail-content {
  padding: 1rem 1.5rem 1.5rem;
}

.event-title-lg {
  color: var(--color-primary);
  margin: 0 0 0.75rem;
}

.description {
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.4;
  color: var(--color-black);
  margin-bottom: 1.25rem;
}

.meta {
  border-top: 1px solid var(--color-light-grey-40);
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-black);
}
</style>
