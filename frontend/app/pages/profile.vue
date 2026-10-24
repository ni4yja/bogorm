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

        <section class="danger-zone">
          <h2 class="danger-title">
            {{ t('profile.dangerZone.title') }}
          </h2>
          <p class="danger-text">
            {{ t('profile.dangerZone.text') }}
          </p>
          <button class="danger-btn" @click="isDeleteModalOpen = true">
            {{ t('profile.dangerZone.button') }}
          </button>
        </section>
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
  color: var(--color-black);
}

.danger-zone {
  border: 1px solid var(--color-error);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
}

.danger-title {
  color: var(--color-error);
  font-size: 1rem;
  margin: 0 0 0.5rem;
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
</style>
