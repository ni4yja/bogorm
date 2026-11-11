<script setup lang="ts">
import type { CurrentUser } from '~/types'

definePageMeta({ layout: 'default' })

const { t } = useI18n()
const { fetchCurrentUser } = useAuth()

const user = ref<CurrentUser | null>(null)
const isLoading = ref(true)
const hasError = ref(false)
const isDeleteModalOpen = ref(false)

onMounted(async () => {
  try {
    user.value = await fetchCurrentUser()
  }
  catch {
    hasError.value = true
  }
  finally {
    isLoading.value = false
  }
})
</script>

<template>
  <AccountLayout>
    <div class="profile-page">
      <h1 class="page-title">
        {{ t('profile.title') }}
      </h1>

      <div v-if="isLoading" class="state-message">
        {{ t('profile.loading') }}
      </div>
      <div v-else-if="hasError || !user" class="state-message">
        {{ t('profile.loadError') }}
      </div>

      <template v-else>
        <dl class="details">
          <div class="detail-row">
            <dt>{{ t('profile.email') }}</dt>
            <dd>{{ user.email }}</dd>
          </div>
          <div class="detail-row">
            <dt>{{ t('profile.username') }}</dt>
            <dd>{{ user.username }}</dd>
          </div>
        </dl>

        <!-- Collapsed by default: an always-open red block read like an invitation to delete -->
        <details class="danger-toggle">
          <summary>{{ t('profile.dangerZone.toggle') }}</summary>
          <section class="danger-zone">
            <p class="danger-text">
              {{ t('profile.dangerZone.text') }}
            </p>
            <button class="danger-btn" @click="isDeleteModalOpen = true">
              {{ t('profile.dangerZone.button') }}
            </button>
          </section>
        </details>
      </template>
    </div>
    <DeleteAccountModal v-if="isDeleteModalOpen" @close="isDeleteModalOpen = false" />
  </AccountLayout>
</template>

<style scoped>
.profile-page {
  max-width: 640px;
}

.page-title {
  color: var(--color-primary);
  margin: 0 0 1.5rem;
}

.state-message {
  color: var(--color-grey);
  font-size: 0.9rem;
  padding: 2rem 0;
}

.details {
  margin: 0 0 3rem;
}

.detail-row {
  display: flex;
  gap: 1rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--color-light-grey-40);
}

.detail-row dt {
  width: 140px;
  flex-shrink: 0;
  color: var(--color-grey);
  font-size: 0.9rem;
}

.detail-row dd {
  margin: 0;
  min-width: 0;
  color: var(--color-black);
  /* Long emails have no natural break points and would push the page sideways on mobile */
  overflow-wrap: anywhere;
}

.danger-toggle summary {
  display: inline-block;
  list-style: none;
  color: var(--color-grey);
  font-size: 0.85rem;
  text-decoration: underline;
  text-underline-offset: 2px;
  cursor: pointer;
}

/* Safari still draws its own disclosure triangle */
.danger-toggle summary::-webkit-details-marker {
  display: none;
}

.danger-toggle[open] summary {
  margin-bottom: 1rem;
}

.danger-zone {
  border: 1px solid var(--color-error);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
}

.danger-text {
  color: var(--color-grey);
  font-size: 0.9rem;
  margin: 0 0 1rem;
}

.danger-btn {
  padding: 0.6rem 1.1rem;
  border: 1.5px solid var(--color-error);
  border-radius: 8px;
  background: none;
  color: var(--color-error);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
}

.danger-btn:hover {
  background: var(--color-error);
  color: var(--color-white);
}

@media (max-width: 640px) {
  .detail-row {
    flex-direction: column;
    gap: 0.25rem;
  }

  .detail-row dt {
    width: auto;
  }
}
</style>
