<script setup lang="ts">
const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

const emit = defineEmits<{
  change: [page: number]
}>()

const { t } = useI18n()

function goTo(page: number) {
  if (page < 1 || page > props.totalPages || page === props.currentPage)
    return
  emit('change', page)
}
</script>

<template>
  <!-- A single page needs no navigation -->
  <nav v-if="totalPages > 1" class="pagination" :aria-label="t('pagination.label')">
    <button
      type="button"
      class="pagination-btn"
      :disabled="currentPage <= 1"
      :aria-label="t('pagination.previous')"
      @click="goTo(currentPage - 1)"
    >
      <IconsArrowLeft class="pagination-icon" />
    </button>
    <span class="pagination-label">
      {{ t('pagination.pageLabel', { current: currentPage, total: totalPages }) }}
    </span>
    <button
      type="button"
      class="pagination-btn"
      :disabled="currentPage >= totalPages"
      :aria-label="t('pagination.next')"
      @click="goTo(currentPage + 1)"
    >
      <IconsArrowLeft class="pagination-icon pagination-icon--next" />
    </button>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.pagination-label {
  font-size: 0.9rem;
  color: var(--color-grey);
}

.pagination-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-primary);
  padding: 0.25rem;
}

.pagination-btn:disabled {
  color: var(--color-light-grey);
  cursor: not-allowed;
}

.pagination-icon {
  width: 20px;
  height: 20px;
}

.pagination-icon--next {
  transform: rotate(180deg);
}
</style>
