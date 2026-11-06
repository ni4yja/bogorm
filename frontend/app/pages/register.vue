<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const { register } = useAuth()
const { t } = useI18n()

const email = ref('')
const username = ref('')
const password = ref('')
const accepted = ref(false)

const { error, isLoading, handleSubmit } = useAuthForm(
  () => register(email.value, username.value, password.value, accepted.value),
  // The backend's field messages already follow Accept-Language
  (err: any) => (err?.response?.status === 400 && Object.values(err.data ?? {}).flat().join(' ')) || t('register.errorDefault'),
)
</script>

<template>
  <AuthLayout :title="t('register.title')" :subtitle="t('register.subtitle')">
    <form class="auth-form" @submit.prevent="handleSubmit">
      <label class="label" for="email">{{ t('register.emailLabel') }}</label>
      <input
        id="email"
        v-model="email"
        type="email"
        :placeholder="t('register.emailPlaceholder')"
        class="input"
        required
      >

      <label class="label" for="username">{{ t('register.usernameLabel') }}</label>
      <input
        id="username"
        v-model="username"
        type="text"
        :placeholder="t('register.usernamePlaceholder')"
        class="input"
        required
      >

      <label class="label" for="password">{{ t('register.passwordLabel') }}</label>
      <input
        id="password"
        v-model="password"
        type="password"
        :placeholder="t('register.passwordPlaceholder')"
        class="input"
        minlength="8"
        required
      >

      <label class="consent">
        <input v-model="accepted" type="checkbox" required>
        <i18n-t keypath="register.consent" tag="span" scope="global">
          <template #terms>
            <NuxtLinkLocale to="/terms" target="_blank">{{ t('register.consentTerms') }}</NuxtLinkLocale>
          </template>
          <template #privacy>
            <NuxtLinkLocale to="/privacy" target="_blank">{{ t('register.consentPrivacy') }}</NuxtLinkLocale>
          </template>
        </i18n-t>
      </label>

      <p v-if="error" class="error">
        {{ error }}
      </p>

      <button type="submit" class="btn-submit" :disabled="isLoading">
        {{ isLoading ? t('register.submitting') : t('register.submit') }}
      </button>
    </form>

    <p class="switch-link">
      {{ t('register.hasAccount') }} <NuxtLinkLocale to="/login">
        {{ t('register.logInLink') }}
      </NuxtLinkLocale>
    </p>
  </AuthLayout>
</template>

<style scoped>
.consent {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.875rem;
  line-height: 1.4;
  margin-bottom: var(--spacing-xs);
}

.consent input {
  flex-shrink: 0;
  margin-top: 0.2em;
}

.consent a {
  color: inherit;
}
</style>
