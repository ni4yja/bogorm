<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <div class="empty-state">
    <!-- Icon is passed by the page, so each context can show its own -->
    <div v-if="$slots.icon" class="empty-icon">
      <slot name="icon" />
    </div>
    <p class="empty-title">
      {{ title }}
    </p>
    <p v-if="subtitle" class="empty-subtitle">
      {{ subtitle }}
    </p>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4rem 1rem;
}

.empty-icon {
  display: flex;
  margin-bottom: 1rem;
  color: var(--color-light-grey);
}

/* Size the slotted icon from here — the page doesn't need its own class */
.empty-icon :deep(svg) {
  width: 48px;
  height: 48px;
}

.empty-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-primary);
  margin: 0 0 0.5rem;
}

.empty-subtitle {
  color: var(--color-grey);
  font-size: 0.9rem;
  margin: 0;
}
</style>
