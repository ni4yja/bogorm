<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const { login } = useAuth()
const { t } = useI18n()

const email = ref('')
const password = ref('')

const { error, isLoading, handleSubmit } = useAuthForm(
  () => login(email.value, password.value),
  () => t('login.errorDefault'),
)
</script>

<template>
  <AuthLayout :title="t('login.title')" :subtitle="t('login.subtitle')">
    <form class="auth-form" @submit.prevent="handleSubmit">
      <label class="label" for="email">{{ t('login.emailLabel') }}</label>
      <input
        id="email"
        v-model="email"
        type="email"
        :placeholder="t('login.emailPlaceholder')"
        class="input"
        required
      >

      <label class="label" for="password">{{ t('login.passwordLabel') }}</label>
      <input
        id="password"
        v-model="password"
        type="password"
        placeholder="••••••••"
        class="input"
        required
      >

      <p v-if="error" class="error">
        {{ error }}
      </p>

      <button type="submit" class="btn-submit" :disabled="isLoading">
        {{ isLoading ? t('login.submitting') : t('login.submit') }}
      </button>
    </form>

    <p class="switch-link">
      {{ t('login.noAccount') }} <NuxtLink to="/register">
        {{ t('login.signUpLink') }}
      </NuxtLink>
    </p>
  </AuthLayout>
</template>
