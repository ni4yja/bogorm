<script setup lang="ts">
import type { EventListItem, PaginatedResponse, TabItem } from '~/types'

definePageMeta({ layout: 'default', middleware: 'auth' })

// Matches PAGE_SIZE in DRF's PageNumberPagination settings
const PAGE_SIZE = 20

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const { get } = useApi()
const { registerInitialState } = useBookmarks()

// Auto-imported components can't be referenced by string in :is — resolve once in setup
const CalendarIcon = resolveComponent('IconsCalendar')

type EventStatus = 'upcoming' | 'archived'

// URL is the source of truth: survives reload, back button and shared links
const activeStatus = computed<EventStatus>(() =>
  route.query.status === 'archived' ? 'archived' : 'upcoming',
)

// Anything that isn't a positive integer (?page=abc, ?page=0) falls back to the first page
const currentPage = computed(() => {
  const page = Number(route.query.page)
  return Number.isInteger(page) && page > 0 ? page : 1
})

const tabs = computed<TabItem<EventStatus>[]>(() => [
  { value: 'upcoming', label: t('events.upcoming'), icon: CalendarIcon },
  { value: 'archived', label: t('events.archived'), icon: CalendarIcon },
])

const events = ref<EventListItem[]>([])
const totalCount = ref(0)
const isLoading = ref(true)
const hasError = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(totalCount.value / PAGE_SIZE)))

// Guards against a slow response for the old tab or page overwriting the new one
let latestRequestId = 0

async function loadEvents() {
  const requestId = ++latestRequestId
  isLoading.value = true
  hasError.value = false

  try {
    const response = await get<PaginatedResponse<EventListItem>>(
      `/events/?status=${activeStatus.value}&page=${currentPage.value}`,
    )

    if (requestId !== latestRequestId)
      return

    // Seed shared bookmark state so icons render right away and stay in sync with the map and /bookmarks
    for (const event of response.results)
      registerInitialState('event', event.id, event.is_bookmarked)

    events.value = response.results
    totalCount.value = response.count
  }
  catch (error: any) {
    if (requestId !== latestRequestId)
      return

    // DRF answers 404 past the last page (stale link, or the list shrank) — step back one page,
    // same recovery as /bookmarks, instead of losing the user's place entirely
    if (error?.response?.status === 404 && currentPage.value > 1) {
      const previousPage = currentPage.value - 1
      router.replace({ query: { ...route.query, page: previousPage === 1 ? undefined : String(previousPage) } })
      return
    }

    hasError.value = true
  }
  finally {
    if (requestId === latestRequestId)
      isLoading.value = false
  }
}

function switchStatus(status: EventStatus) {
  router.replace({
    query: {
      ...route.query,
      // Default status stays out of the URL to keep it clean
      status: status === 'upcoming' ? undefined : status,
      // A new tab always starts from the first page
      page: undefined,
    },
  })
}

// push, not replace: the back button should return to the previous page of results
function goToPage(page: number) {
  router.push({
    query: {
      ...route.query,
      page: page === 1 ? undefined : String(page),
    },
  })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Not immediate: page setup also runs on the server, where there's no token
watch([activeStatus, currentPage], loadEvents)
onMounted(loadEvents)
</script>

<template>
  <!-- Private page: tokens are client-only, so skip SSR to avoid flashing content before the auth redirect -->
  <ClientOnly>
    <div class="events-page">
      <h1 class="page-title">
        {{ t('events.title') }}
      </h1>
      <p class="page-subtitle">
        {{ t('events.subtitle') }}
      </p>

      <BaseTabs
        class="tabs-nav"
        :items="tabs"
        :model-value="activeStatus"
        @update:model-value="switchStatus"
      />

      <div v-if="isLoading" class="state-message">
        {{ t('events.loading') }}
      </div>
      <div v-else-if="hasError" class="state-message">
        {{ t('events.loadError') }}
      </div>
      <BaseEmptyState
        v-else-if="events.length === 0"
        :title="activeStatus === 'upcoming' ? t('events.emptyTitleUpcoming') : t('events.emptyTitleArchived')"
        :subtitle="activeStatus === 'upcoming' ? t('events.emptySubtitleUpcoming') : t('events.emptySubtitleArchived')"
      >
        <template #icon>
          <IconsCalendar />
        </template>
      </BaseEmptyState>

      <template v-else>
        <div class="cards-grid">
          <EventCard
            v-for="event in events"
            :key="event.id"
            :title="event.title"
            :event-time="event.event_time"
            :category="event.category"
            :place-title="event.place.title"
          >
            <template #actions>
              <BookmarkButton :id="event.id" type="event" :title="event.title" />
            </template>
          </EventCard>
        </div>

        <BasePagination
          class="pagination-nav"
          :current-page="currentPage"
          :total-pages="totalPages"
          @change="goToPage"
        />
      </template>
    </div>
  </ClientOnly>
</template>

<style scoped>
.events-page {
  max-width: 1360px;
  margin: 0 auto;
  padding: calc(var(--header-height) + 2rem) 2.5rem 3rem;
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}

.pagination-nav {
  margin-top: 2rem;
}

@media (max-width: 640px) {
  .events-page {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
