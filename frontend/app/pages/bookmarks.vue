<script setup lang="ts">
import type { BookmarkEventTarget, BookmarkItem, BookmarkPlaceTarget } from '~/types'

definePageMeta({ layout: 'default' })

const { fetchBookmarks, toggleBookmark, isBookmarked, registerInitialState } = useBookmarks()
const { getCategoryLabel } = useEventCategory()

type Tab = 'place' | 'event'

const activeTab = ref<Tab>('place')
const currentPage = ref(1)
const totalCount = ref(0)
const placesCount = ref(0)
const eventsCount = ref(0)
const items = ref<BookmarkItem[]>([])
const isLoading = ref(false)
const error = ref('')

const totalPages = computed(() => Math.max(1, Math.ceil(totalCount.value / 20)))

let latestRequestId = 0

async function loadBookmarks() {
  const requestId = ++latestRequestId
  isLoading.value = true
  error.value = ''

  try {
    const response = await fetchBookmarks(activeTab.value, currentPage.value)

    if (requestId !== latestRequestId)
      return

    if (response.results.length === 0 && currentPage.value > 1) {
      currentPage.value -= 1
      return loadBookmarks()
    }

    items.value = response.results
    totalCount.value = response.count

    for (const item of response.results) {
      registerInitialState(item.type, item.target.id, true)
    }

    if (activeTab.value === 'place')
      placesCount.value = response.count
    else
      eventsCount.value = response.count
  }
  catch {
    if (requestId === latestRequestId)
      error.value = 'Could not load bookmarks'
  }
  finally {
    if (requestId === latestRequestId)
      isLoading.value = false
  }
}

async function loadCounts() {
  try {
    const [placesResponse, eventsResponse] = await Promise.all([
      fetchBookmarks('place', 1),
      fetchBookmarks('event', 1),
    ])
    placesCount.value = placesResponse.count
    eventsCount.value = eventsResponse.count
  }
  catch {
  }
}

function switchTab(tab: Tab) {
  activeTab.value = tab
  currentPage.value = 1
  loadBookmarks()
}

function goToPage(page: number) {
  if (page < 1 || page > totalPages.value)
    return
  currentPage.value = page
  loadBookmarks()
}

async function handleToggleBookmark(type: Tab, id: string) {
  await toggleBookmark(type, id)
  await loadBookmarks()
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

function isPlaceTarget(target: BookmarkItem['target']): target is BookmarkPlaceTarget {
  return target.type === 'place'
}

function isEventTarget(target: BookmarkItem['target']): target is BookmarkEventTarget {
  return target.type === 'event'
}

onMounted(async () => {
  await loadCounts()
  await loadBookmarks()
})
</script>

<template>
  <AccountLayout>
    <div class="bookmarks-page">
      <h1 class="page-title">
        Bookmarks
      </h1>
      <p class="page-subtitle">
        This is the place for your saved places and events
      </p>

      <div class="tabs">
        <button
          class="tab"
          :class="{ 'tab--active': activeTab === 'place' }"
          @click="switchTab('place')"
        >
          <IconsPin class="tab-icon" />
          Places ({{ placesCount }})
        </button>
        <button
          class="tab"
          :class="{ 'tab--active': activeTab === 'event' }"
          @click="switchTab('event')"
        >
          <IconsCalendar class="tab-icon" />
          Events ({{ eventsCount }})
        </button>
      </div>

      <div v-if="isLoading" class="state-message">
        Loading…
      </div>
      <div v-else-if="error" class="state-message">
        {{ error }}
      </div>

      <div v-else-if="items.length === 0" class="empty-state">
        <IconsPin v-if="activeTab === 'place'" class="empty-icon" />
        <IconsCalendar v-else class="empty-icon" />
        <p class="empty-title">
          Looks like you saved no {{ activeTab === 'place' ? 'places' : 'events' }} yet!
        </p>
        <p class="empty-subtitle">
          Explore {{ activeTab === 'place' ? 'places' : 'events' }} on map and save them to your bookmarks!
        </p>
      </div>

      <div v-else class="cards-grid">
        <div v-for="item in items" :key="item.id" class="card">
          <div class="card-image">
            <IconsImage class="image-icon" />
          </div>

          <div class="card-content">
            <div class="card-title-row">
              <h3 class="card-title">
                {{ item.target.title }}
              </h3>
              <button
                class="bookmark-btn"
                aria-label="Remove bookmark"
                @click="handleToggleBookmark(item.type, item.target.id)"
              >
                <IconsBookmarkActive v-if="isBookmarked(item.type, item.target.id)" class="bookmark-icon" />
                <IconsBookmark v-else class="bookmark-icon" />
              </button>
            </div>

            <div v-if="isEventTarget(item.target) && item.target.event_time" class="card-meta">
              <IconsTime class="meta-icon" />
              {{ formatEventTime(item.target.event_time) }}
            </div>

            <div v-if="isEventTarget(item.target)" class="card-badges">
              <span class="badge">{{ getCategoryLabel(item.target.category) }}</span>
            </div>

            <div v-if="isPlaceTarget(item.target)" class="card-badges">
              <span class="badge">Place</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="items.length > 0 && totalPages > 1" class="pagination">
        <span class="pagination-label">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          class="pagination-btn"
          :disabled="currentPage >= totalPages"
          aria-label="Next page"
          @click="goToPage(currentPage + 1)"
        >
          <IconsArrowLeft class="pagination-icon pagination-icon--next" />
        </button>
      </div>
    </div>
  </AccountLayout>
</template>

<style scoped>
.bookmarks-page {
  max-width: 900px;
}

.page-title {
  color: var(--color-primary);
  margin: 0 0 0.35rem;
}

.page-subtitle {
  color: var(--color-grey);
  font-size: 0.95rem;
  margin: 0 0 1.5rem;
}

.tabs {
  display: flex;
  border: 1px solid var(--color-light-grey-40);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 1.5rem;
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

.state-message {
  color: var(--color-grey);
  font-size: 0.9rem;
  padding: 2rem 0;
  text-align: center;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4rem 1rem;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: var(--color-light-grey);
  margin-bottom: 1rem;
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

.cards-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.card {
  border: 1px solid var(--color-light-grey-40);
  border-radius: 12px;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 140px;
  background: var(--color-light-grey-40);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-icon {
  width: 48px;
  height: 38px;
  color: var(--color-grey);
}

.card-content {
  padding: 1rem;
}

.card-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-primary);
  margin: 0;
}

.bookmark-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.15rem;
  flex-shrink: 0;
  color: var(--color-primary);
}

.bookmark-icon {
  width: 18px;
  height: 18px;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: var(--color-grey);
  margin-bottom: 0.5rem;
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: var(--color-primary);
}

.card-badges {
  display: flex;
  gap: 0.4rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 0.75rem;
  padding: 0.25rem 0.65rem;
  border-radius: 20px;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
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
