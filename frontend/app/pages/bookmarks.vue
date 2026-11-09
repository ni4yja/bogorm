<script setup lang="ts">
import type { BookmarkEventTarget, BookmarkItem, BookmarkPlaceTarget, PaginatedResponse, TabItem } from '~/types'

definePageMeta({ layout: 'default' })

const { t } = useI18n()
const route = useRoute()
const { fetchBookmarks, registerInitialState } = useBookmarks()
const { getCategoryLabel } = useEventCategory()
const { formatEventTime } = useEventFormat()

// Auto-imported components can't be referenced by string in :is — resolve once in setup
const PinIcon = resolveComponent('IconsPin')
const CalendarIcon = resolveComponent('IconsCalendar')

type Tab = 'place' | 'event'

const activeTab = ref<Tab>(
  route.query.type === 'event' ? 'event' : 'place',
)

const currentPage = ref(1)
const pageSize = ref(20)
const placesCount = ref(0)
const eventsCount = ref(0)
const items = ref<BookmarkItem[]>([])
const isLoading = ref(true)
const hasError = ref(false)

const currentCount = computed(() => activeTab.value === 'place' ? placesCount.value : eventsCount.value)
const totalPages = computed(() => Math.max(1, Math.ceil(currentCount.value / pageSize.value)))

const tabs = computed<TabItem<Tab>[]>(() => [
  { value: 'place', label: t('bookmarks.placesTab', { count: placesCount.value }), icon: PinIcon },
  { value: 'event', label: t('bookmarks.eventsTab', { count: eventsCount.value }), icon: CalendarIcon },
])

let latestRequestId = 0

function applyPage(type: Tab, response: PaginatedResponse<BookmarkItem>) {
  for (const item of response.results) {
    registerInitialState(item.type, item.target.id, true)
  }

  if (type === 'place')
    placesCount.value = response.count
  else
    eventsCount.value = response.count

  if (type === activeTab.value) {
    items.value = response.results
    if (currentPage.value === 1 && response.results.length > 0)
      pageSize.value = response.results.length
  }
}

async function loadBookmarks() {
  const requestId = ++latestRequestId
  isLoading.value = true
  hasError.value = false

  try {
    const response = await fetchBookmarks(activeTab.value, currentPage.value)

    if (requestId !== latestRequestId)
      return

    applyPage(activeTab.value, response)
  }
  catch (error: any) {
    if (requestId !== latestRequestId)
      return

    // DRF answers 404 past the last page, e.g. after removals on another device
    if (error?.response?.status === 404 && currentPage.value > 1) {
      currentPage.value -= 1
      return loadBookmarks()
    }

    hasError.value = true
  }
  finally {
    if (requestId === latestRequestId)
      isLoading.value = false
  }
}

// Runs once on mount and doesn't touch latestRequestId, so a tab switch can't discard the counts
async function loadCounts() {
  try {
    const [placesResponse, eventsResponse] = await Promise.all([
      fetchBookmarks('place', 1),
      fetchBookmarks('event', 1),
    ])

    applyPage('place', placesResponse)
    applyPage('event', eventsResponse)
  }
  catch {
    hasError.value = true
  }
}

function switchTab(tab: Tab) {
  activeTab.value = tab
  currentPage.value = 1
  loadBookmarks()
}

// BasePagination only emits valid, in-range pages
function goToPage(page: number) {
  currentPage.value = page
  loadBookmarks()
}

// BookmarkButton already called the API — here we only sync the list
async function handleBookmarkToggled(type: Tab, id: string, nowBookmarked: boolean) {
  if (nowBookmarked || type !== activeTab.value)
    return

  const wasFullPage = items.value.length === pageSize.value
  const isLastPage = currentPage.value >= totalPages.value

  items.value = items.value.filter((item: BookmarkItem) => item.target.id !== id)
  if (type === 'place')
    placesCount.value = Math.max(0, placesCount.value - 1)
  else
    eventsCount.value = Math.max(0, eventsCount.value - 1)

  if (items.value.length === 0 && currentPage.value > 1) {
    currentPage.value -= 1
    await loadBookmarks()
  }
  else if (wasFullPage && !isLastPage) {
    // removing an item from a full, non-last page needs a refetch to pull the next item forward
    await loadBookmarks()
  }
}

function isPlaceTarget(target: BookmarkItem['target']): target is BookmarkPlaceTarget {
  return target.type === 'place'
}

function isEventTarget(target: BookmarkItem['target']): target is BookmarkEventTarget {
  return target.type === 'event'
}

onMounted(async () => {
  await loadCounts()
  isLoading.value = false
})
</script>

<template>
  <AccountLayout>
    <div class="bookmarks-page">
      <h1 class="page-title">
        {{ t('bookmarks.title') }}
      </h1>
      <p class="page-subtitle">
        {{ t('bookmarks.subtitle') }}
      </p>

      <!-- Not v-model: switchTab also resets the page and refetches -->
      <BaseTabs
        class="tabs-nav"
        :items="tabs"
        :model-value="activeTab"
        @update:model-value="switchTab"
      />

      <div v-if="isLoading" class="state-message">
        {{ t('bookmarks.loading') }}
      </div>
      <div v-else-if="hasError" class="state-message">
        {{ t('bookmarks.loadError') }}
      </div>
      <BaseEmptyState
        v-else-if="items.length === 0"
        :title="activeTab === 'place' ? t('bookmarks.emptyTitlePlaces') : t('bookmarks.emptyTitleEvents')"
        :subtitle="activeTab === 'place' ? t('bookmarks.emptySubtitlePlaces') : t('bookmarks.emptySubtitleEvents')"
      >
        <template #icon>
          <IconsPin v-if="activeTab === 'place'" />
          <IconsCalendar v-else />
        </template>
      </BaseEmptyState>

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
              <BookmarkButton
                :id="item.target.id"
                :type="item.type"
                @toggled="handleBookmarkToggled(item.type, item.target.id, $event)"
              />
            </div>

            <div v-if="isEventTarget(item.target) && item.target.event_time" class="card-meta">
              <IconsTime class="meta-icon" />
              {{ formatEventTime(item.target.event_time) }}
            </div>

            <div v-if="isEventTarget(item.target)" class="card-badges">
              <span class="badge">{{ getCategoryLabel(item.target.category) }}</span>
            </div>

            <div v-if="isPlaceTarget(item.target)" class="card-badges">
              <span class="badge">{{ t('bookmarks.placeBadge') }}</span>
            </div>
          </div>
        </div>
      </div>

      <BasePagination
        v-if="items.length > 0"
        class="pagination-nav"
        :current-page="currentPage"
        :total-pages="totalPages"
        @change="goToPage"
      />
    </div>
  </AccountLayout>
</template>

<style scoped>
.bookmarks-page {
  max-width: 900px;
}

.tabs-nav {
  margin-bottom: 1.5rem;
}

.state-message {
  color: var(--color-grey);
  font-size: 0.9rem;
  padding: 2rem 0;
  text-align: center;
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

.pagination-nav {
  margin-top: 1.5rem;
}

@media (max-width: 640px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
