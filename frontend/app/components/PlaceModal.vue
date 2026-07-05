<script setup lang="ts">
import type { Event, PlaceDetail } from '~/types'

defineProps<{
  place: PlaceDetail
  eventCount: number
  events: Event[]
  isAuthenticated?: boolean
}>()

defineEmits<{
  close: []
}>()
</script>

<template>
  <div class="modal">
    <button class="close" aria-label="Close" @click="$emit('close')">
      <IconsClose />
    </button>

    <div class="image-placeholder">
      <IconsImage class="image-icon" />
    </div>

    <div class="badges">
      <div v-if="eventCount > 0 && !isAuthenticated" class="badge badge--events">
        <IconsCalendar class="badge-icon" />
        {{ eventCount }} Upcoming Event{{ eventCount > 1 ? 's' : '' }}
      </div>
      <div v-if="isAuthenticated" class="badge badge--visited">
        <IconsPinMarked class="badge-icon" />
        You've been here
      </div>
    </div>

    <div class="content">
      <div class="title-row">
        <h2 class="title">
          {{ place.title }}
        </h2>
        <button v-if="isAuthenticated" class="bookmark-btn" aria-label="Save place">
          <IconsBookmark class="bookmark-icon" />
        </button>
      </div>

      <p v-if="place.description" class="description">
        {{ place.description }}
      </p>

      <div v-if="place.address || place.website" class="meta">
        <div v-if="place.address" class="meta-item">
          <IconsPin class="meta-icon" />
          <span>{{ place.address }}</span>
        </div>
        <div v-if="place.website" class="meta-item">
          <IconsLink class="meta-icon" />
          <a :href="place.website" target="_blank" rel="noopener">
            {{ place.website.replace(/^https?:\/\/(www\.)?/, '') }}
          </a>
        </div>
      </div>

      <div v-if="isAuthenticated && events.length > 0" class="events-section">
        <div class="events-header">
          <IconsCalendar class="events-header-icon" />
          Upcoming Events:
        </div>
        <div v-for="event in events" :key="event.id" class="event-item">
          <div class="event-title">
            {{ event.title }}
            <button class="bookmark-btn" aria-label="Save event">
              <IconsBookmark class="bookmark-icon" />
            </button>
          </div>
          <div v-if="event.event_time" class="event-time">
            <IconsTime class="meta-icon" />
            {{ new Date(event.event_time).toLocaleString('uk-UA') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 640px;
  max-height: calc(100% - 3rem);
  overflow-y: auto;
  background: var(--color-white);
  border-radius: var(--badge-radius);
  z-index: 900;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
}

.close {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-primary);
  z-index: 1;
  padding: 0.25rem;
}

.image-placeholder {
  width: 100%;
  height: 354px;
  background: var(--color-light-grey-40);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px 20px 0 0;
}

.image-icon {
  width: 80px;
  height: 63px;
  color: var(--color-grey);
}

.badges {
  padding: 0 1.5rem;
  margin-top: calc(-1 * (var(--badge-height) + var(--spacing-xs)));
  margin-bottom: 0;
  display: flex;
  gap: 0.5rem;
}

.badge {
  height: var(--badge-height);
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 12px;
  font-weight: 400;
  padding: 0 8px;
  border-radius: 20px;
  background: var(--color-primary);
  color: var(--color-white);
}

.badge-icon {
  width: 14px;
  height: 14px;
  color: var(--color-white);
  flex-shrink: 0;
}

.content {
  padding: 1.25rem 1.5rem 2rem;
}

.title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
  margin-top: 1rem;
}

.title {
  color: var(--color-primary);
  margin: 0;
}

.bookmark-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  flex-shrink: 0;
  color: var(--color-primary);
  margin-top: 0.2rem;
}

.bookmark-icon {
  width: 22px;
  height: 22px;
}

.description {
  font-size: 1rem;
  color: var(--color-black);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.meta {
  border-top: 1px solid var(--color-light-grey-40);
  padding-top: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1rem;
  color: var(--color-black);
}

.meta-item a {
  color: var(--color-black);
  text-decoration: none;
}

.meta-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--color-primary);
}

.events-section {
  margin-top: 1.5rem;
  border-top: 1px solid var(--color-light-grey-40);
  padding-top: 1.25rem;
}

.events-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-black);
  margin-bottom: 1rem;
}

.events-header-icon {
  width: 20px;
  height: 20px;
  color: var(--color-primary);
}

.event-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.event-item:last-child {
  margin-bottom: 0;
}

.event-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-black);
}

.event-time {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.9rem;
  color: var(--color-grey);
}
</style>
