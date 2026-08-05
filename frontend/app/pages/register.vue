<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const { register } = useAuth()
const router = useRouter()

const email = ref('')
const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

async function handleSubmit() {
  error.value = ''
  isLoading.value = true

  try {
    await register(email.value, username.value, password.value)
    await router.push('/')
  }
  catch {
    error.value = 'Could not create account. Please check your details.'
  }
  finally {
    isLoading.value = false
  }
}
</script>

<template>
  <AuthLayout title="Sign up" subtitle="Create your Bogorm account">
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

      <label class="label" for="username">Username</label>
      <input
        id="username"
        v-model="username"
        type="text"
        placeholder="your_username"
        class="input"
        required
      >

      <label class="label" for="password">Password</label>
      <input
        id="password"
        v-model="password"
        type="password"
        placeholder="min 8 characters"
        class="input"
        minlength="8"
        required
      >

      <p v-if="error" class="error">
        {{ error }}
      </p>

      <button type="submit" class="btn-submit" :disabled="isLoading">
        {{ isLoading ? 'Signing up…' : 'Sign up' }}
      </button>
    </form>

    <p class="switch-link">
      Already have an account? <NuxtLink to="/login">
        Log in
      </NuxtLink>
    </p>
  </AuthLayout>
</template>
