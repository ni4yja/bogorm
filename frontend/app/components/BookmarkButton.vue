<script setup lang="ts">
const props = defineProps<{
  type: 'place' | 'event'
  id: string
  // Shown in the toast ("Saved: …"), so the user knows what was bookmarked
  title: string
}>()

const emit = defineEmits<{
  toggled: [bookmarked: boolean]
}>()

const { t } = useI18n()
const { isBookmarked, isPending, toggleBookmark } = useBookmarks()

const active = computed(() => isBookmarked(props.type, props.id))

async function handleClick() {
  const nowBookmarked = await toggleBookmark(props.type, props.id, props.title)
  // Pages react to the new state, e.g. /bookmarks drops the card on removal
  emit('toggled', nowBookmarked)
}
</script>

<template>
  <button
    type="button"
    class="bookmark-btn"
    :disabled="isPending(type, id)"
    :aria-pressed="active"
    :aria-label="active ? t('bookmark.remove') : t('bookmark.add')"
    @click.stop="handleClick"
  >
    <IconsBookmarkActive v-if="active" class="bookmark-icon" />
    <IconsBookmark v-else class="bookmark-icon" />
  </button>
</template>

<style scoped>
.bookmark-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.15rem;
  flex-shrink: 0;
  color: var(--color-primary);
}

.bookmark-btn:disabled {
  cursor: wait;
}

.bookmark-icon {
  width: 18px;
  height: 18px;
}
</style>
