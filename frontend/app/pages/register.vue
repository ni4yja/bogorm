<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const { register } = useAuth()
const { t } = useI18n()

const email = ref('')
const username = ref('')
const password = ref('')

const { error, isLoading, handleSubmit } = useAuthForm(
  () => register(email.value, username.value, password.value),
  () => t('register.errorDefault'),
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

      <p v-if="error" class="error">
        {{ error }}
      </p>

      <button type="submit" class="btn-submit" :disabled="isLoading">
        {{ isLoading ? t('register.submitting') : t('register.submit') }}
      </button>
    </form>

    <p class="switch-link">
      {{ t('register.hasAccount') }} <NuxtLink to="/login">
        {{ t('register.logInLink') }}
      </NuxtLink>
    </p>
  </AuthLayout>
</template>
