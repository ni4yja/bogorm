<script setup lang="ts">
defineProps<{
  title: string
  eventTime: string | null
  category: number
  // Optional: omitted where the place is already clear from context (place page)
  placeTitle?: string
}>()

const { getCategoryLabel } = useEventCategory()
const { formatEventTime } = useEventFormat()
</script>

<template>
  <article class="event-card">
    <div class="card-header">
      <h3 class="card-title">
        {{ title }}
      </h3>
      <!-- Header actions (bookmark) go here -->
      <slot name="actions" />
    </div>

    <div v-if="eventTime" class="card-meta">
      <IconsTime class="meta-icon" />
      <time :datetime="eventTime">{{ formatEventTime(eventTime) }}</time>
    </div>

    <div v-if="placeTitle" class="card-meta">
      <IconsPin class="meta-icon" />
      <span class="meta-text--truncate">{{ placeTitle }}</span>
    </div>

    <div class="card-badges">
      <span class="badge">{{ getCategoryLabel(category) }}</span>
    </div>
  </article>
</template>

<style scoped>
.event-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  border: 1px solid var(--color-light-grey-40);
  border-radius: 12px;
  background: var(--color-white);
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.card-title {
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.35;
  color: var(--color-black);
  margin: 0;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  min-width: 0;
  font-size: 0.9rem;
  color: var(--color-black);
}

.meta-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: var(--color-primary);
}

/* Long library names would otherwise push the card height around */
.meta-text--truncate {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.card-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.25rem;
}
</style>
