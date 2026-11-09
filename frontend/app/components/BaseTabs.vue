<script setup lang="ts" generic="T extends string">
import type { TabItem } from '~/types'

const props = defineProps<{
  items: TabItem<T>[]
  modelValue: T
}>()

const emit = defineEmits<{
  'update:modelValue': [value: T]
}>()

function select(value: T) {
  // Clicking the active tab is a no-op — avoids pointless refetches in the parent
  if (value !== props.modelValue)
    emit('update:modelValue', value)
}
</script>

<template>
  <div class="tabs" role="tablist">
    <button
      v-for="item in items"
      :key="item.value"
      type="button"
      role="tab"
      class="tab"
      :class="{ 'tab--active': item.value === modelValue }"
      :aria-selected="item.value === modelValue"
      @click="select(item.value)"
    >
      <component :is="item.icon" v-if="item.icon" class="tab-icon" />
      {{ item.label }}
    </button>
  </div>
</template>

<style scoped>
.tabs {
  display: flex;
  border: 1px solid var(--color-light-grey-40);
  border-radius: 10px;
  overflow: hidden;
}

.tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
  color: var(--color-black);
}

.tab--active {
  background: var(--color-light-grey-40);
  font-weight: 500;
}

.tab-icon {
  width: 18px;
  height: 18px;
  color: var(--color-primary);
}

@media (max-width: 640px) {
  .tab {
    padding: 0.7rem 0.5rem;
    font-size: 0.85rem;
  }
}
</style>
