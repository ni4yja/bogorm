<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const { login } = useAuth()

const email = ref('')
const password = ref('')

const { error, isLoading, handleSubmit } = useAuthForm(
  () => login(email.value, password.value),
  'Invalid email or password',
)
</script>

<template>
  <AuthLayout title="Log in" subtitle="Welcome back to Bogorm">
    <form class="auth-form" @submit.prevent="handleSubmit">
      <label class="label" for="email">Email</label>
      <input
        id="email"
        v-model="email"
        type="email"
        placeholder="name@example.com"
        class="input"
        required
      >

      <label class="label" for="password">Password</label>
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
        {{ isLoading ? 'Logging in…' : 'Log in' }}
      </button>
    </form>

    <p class="switch-link">
      No account? <NuxtLink to="/register">
        Sign up
      </NuxtLink>
    </p>
  </AuthLayout>
</template>
