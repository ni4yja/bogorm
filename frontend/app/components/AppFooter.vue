<script setup lang="ts">
const { t } = useI18n()
const localePath = useLocalePath()

const year = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <nav class="footer-links">
      <NuxtLink :to="localePath('/about')">
        {{ t('footer.about') }}
      </NuxtLink>
      <NuxtLink :to="localePath('/privacy')">
        {{ t('footer.privacy') }}
      </NuxtLink>
      <NuxtLink :to="localePath('/terms')">
        {{ t('footer.terms') }}
      </NuxtLink>
    </nav>
    <p class="footer-copy">
      © {{ year }} Bogorm
    </p>
  </footer>
</template>

<style scoped>
.app-footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem 1.5rem;
  padding: 1rem var(--spacing-md);
  border-top: 1px solid rgb(0 0 0 / 0.1);
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1.5rem;
}

.footer-links a {
  color: inherit;
  text-decoration: none;
}

.footer-links a:hover {
  text-decoration: underline;
}

.footer-copy {
  margin: 0;
  opacity: 0.7;
}

@media (max-width: 640px) {
  .app-footer {
    flex-direction: column;
  }

  .footer-links {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
