<script setup lang="ts">
import type { TabItem } from '~/types'

definePageMeta({ layout: 'default', middleware: 'auth' })

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

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

@media (max-width: 640px) {
  .events-page {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
