<script setup lang="ts">
import type { PlaceDetail } from '~/types'

defineProps<{
  place: PlaceDetail
  eventCount: number
}>()

defineEmits<{
  close: []
}>()
</script>

<template>
  <div class="modal">
    <button class="close" @click="$emit('close')">
      ×
    </button>

    <div class="image-placeholder">
      <span class="image-icon">🖼</span>
    </div>

    <div class="content">
      <div v-if="eventCount > 0" class="events-badge">
        📅 {{ eventCount }} Upcoming Event{{ eventCount > 1 ? 's' : '' }}
      </div>

      <h2 class="title">
        {{ place.title }}
      </h2>

      <p v-if="place.description" class="description">
        {{ place.description }}
      </p>

      <div class="meta">
        <div v-if="place.address" class="meta-item">
          <span class="meta-icon">📍</span>
          {{ place.address }}
        </div>
        <div v-if="place.website" class="meta-item">
          <span class="meta-icon">🔗</span>
          <a :href="place.website" target="_blank">{{ place.website }}</a>
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
  width: 340px;
  max-height: calc(100% - 3rem);
  overflow-y: auto;
  background: #fff;
  border-radius: 16px;
  z-index: 1000;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
}

.close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #555;
  z-index: 1;
}

.image-placeholder {
  width: 100%;
  height: 200px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px 16px 0 0;
}

.image-icon {
  font-size: 2.5rem;
  opacity: 0.4;
}

.content {
  padding: 1.25rem 1.5rem 1.5rem;
}

.events-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--Primary);
  color: #fff;
  font-size: 0.8rem;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  margin-bottom: 1rem;
}

.title {
  color: var(--Primary);
  margin-bottom: 0.75rem;
  line-height: 1.35;
}

.description {
  font-size: 0.9rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.meta {
  border-top: 1px solid #eee;
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #444;
}

.meta-item a {
  color: #444;
  text-decoration: none;
}

.meta-icon {
  font-size: 1rem;
}
</style>
