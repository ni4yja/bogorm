<script setup lang="ts">
import type { EventListItem, PaginatedResponse, TabItem } from '~/types'

definePageMeta({ layout: 'default', middleware: 'auth' })

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const { get } = useApi()

// Auto-imported components can't be referenced by string in :is — resolve once in setup
const CalendarIcon = resolveComponent('IconsCalendar')

type EventStatus = 'upcoming' | 'archived'

// URL is the source of truth: survives reload, back button and shared links
const activeStatus = computed<EventStatus>(() =>
  route.query.status === 'archived' ? 'archived' : 'upcoming',
)

const tabs = computed<TabItem<EventStatus>[]>(() => [
  { value: 'upcoming', label: t('events.upcoming'), icon: CalendarIcon },
  { value: 'archived', label: t('events.archived'), icon: CalendarIcon },
])

const events = ref<EventListItem[]>([])
const isLoading = ref(true)
const hasError = ref(false)

// Guards against a slow response for the old tab overwriting the new one
let latestRequestId = 0

async function loadEvents() {
  const requestId = ++latestRequestId
  isLoading.value = true
  hasError.value = false

  try {
    const response = await get<PaginatedResponse<EventListItem>>(
      `/events/?status=${activeStatus.value}`,
    )

    if (requestId !== latestRequestId)
      return

    events.value = response.results
  }
  catch {
    if (requestId !== latestRequestId)
      return

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

// Not immediate: page setup also runs on the server, where there's no token
watch(activeStatus, loadEvents)
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

      <!-- Temporary plain list — replaced by EventCard in the next step -->
      <ul v-else class="events-list">
        <li v-for="event in events" :key="event.id">
          {{ event.title }}
        </li>
      </ul>
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

@media (max-width: 640px) {
  .events-page {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
