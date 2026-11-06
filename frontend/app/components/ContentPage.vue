<script setup lang="ts">
import type { Collections } from '@nuxt/content'

const props = defineProps<{ path: string }>()

const { locale } = useI18n()

// One collection per locale (see content.config.ts); the key includes the
// locale, so switching language fetches the matching file
const { data: page } = await useAsyncData(
  () => `content-${locale.value}-${props.path}`,
  () => queryCollection(`content_${locale.value}` as keyof Collections)
    .path(props.path)
    .first(),
)

if (!page.value) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found', fatal: true })
}

// useAsyncData's key includes the locale, so switching language re-runs the
// query above; re-check then too, since the initial throw only covers the
// first load.
watch(page, (value) => {
  if (!value) {
    showError(createError({ statusCode: 404, statusMessage: 'Page not found', fatal: true }))
  }
})

// Nuxt Content takes the title from the first # heading
useSeoMeta({
  title: () => page.value?.title,
})
</script>

<template>
  <article class="content-page">
    <ContentRenderer v-if="page" :value="page" />
  </article>
</template>

<style scoped>
.content-page {
  max-width: 720px;
  margin: 0 auto;
  /* The header is fixed, so push the text below it */
  padding: calc(var(--header-height) + var(--spacing-md)) var(--spacing-md) var(--spacing-lg);
  line-height: 1.6;
}

.content-page :deep(h1) {
  margin: 0 0 0.5rem;
  font-size: 2rem;
}

.content-page :deep(h2) {
  margin: 2rem 0 0.75rem;
  font-size: 1.25rem;
}

.content-page :deep(h3) {
  margin: 1.5rem 0 0.5rem;
  font-size: 1rem;
}

.content-page :deep(ul) {
  padding-left: 1.25rem;
}

.content-page :deep(a) {
  color: inherit;
}
</style>
