<script setup lang="ts">
defineProps<{
  title: string
  subtitle: string
}>()
</script>

<template>
  <div class="auth-page">
    <NuxtLink to="/" class="back-link">
      ← Back to map
    </NuxtLink>

    <div class="auth-card">
      <span class="logo">Bogorm</span>
      <h2 class="title">
        {{ title }}
      </h2>
      <p class="subtitle">
        {{ subtitle }}
      </p>

      <slot />
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  background: var(--color-white);
}

.back-link {
  position: absolute;
  top: var(--spacing-md);
  left: var(--spacing-md);
  font-size: 0.9rem;
  color: var(--color-grey);
  text-decoration: none;
}

.back-link:hover {
  color: var(--color-primary);
}

.auth-card {
  width: 380px;
  background: var(--color-white);
  border: 1px solid var(--color-light-grey-40);
  border-radius: 16px;
  padding: 2.5rem 2rem;
}

.logo {
  font-family: 'Merriweather', serif;
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--color-primary);
  display: block;
  margin-bottom: 2rem;
}

.title {
  color: var(--color-primary);
  margin: 0 0 0.4rem;
}

.subtitle {
  font-size: 0.9rem;
  color: var(--color-grey);
  margin: 0 0 1.75rem;
}
</style>
