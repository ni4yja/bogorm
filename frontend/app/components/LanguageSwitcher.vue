<script setup lang="ts">
const { locale, locales, setLocale } = useI18n()

const availableLocales = computed(() =>
  (locales.value as { code: string, name: string }[]),
)

function switchLocale(code: string) {
  setLocale(code)
}
</script>

<template>
  <div class="language-switcher">
    <button
      v-for="loc in availableLocales"
      :key="loc.code"
      class="lang-btn"
      :class="{ 'lang-btn--active': locale === loc.code }"
      @click="switchLocale(loc.code)"
    >
      {{ loc.code.toUpperCase() }}
    </button>
  </div>
</template>

<style scoped>
.language-switcher {
  display: flex;
  gap: 0.25rem;
  padding: 0.2rem;
  background: var(--color-light-grey-40);
  border-radius: 8px;
}

.lang-btn {
  padding: 0.35rem 0.6rem;
  border: none;
  background: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--color-grey);
  cursor: pointer;
}

.lang-btn--active {
  background: var(--color-white);
  color: var(--color-primary);
}
</style>
