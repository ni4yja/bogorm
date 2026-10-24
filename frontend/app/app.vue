<script setup lang="ts">
const { t } = useI18n()
const { public: { i18n: { baseUrl: SITE_URL } } } = useRuntimeConfig()

// lang/dir on <html>, plus canonical, hreflang alternates and og:locale
const localeHead = useLocaleHead({ dir: true, lang: true, seo: true })

useHead(() => ({
  htmlAttrs: localeHead.value.htmlAttrs,
  link: localeHead.value.link,
  meta: localeHead.value.meta,
}))

// Site-wide defaults; pages override title/description where they need to
useSeoMeta({
  title: () => t('site.title'),
  description: () => t('site.description'),
  ogTitle: () => t('site.title'),
  ogDescription: () => t('site.description'),
  ogSiteName: 'Bogorm',
  ogType: 'website',
  ogImage: `${SITE_URL}/og-image.png`,
  ogImageWidth: 1200,
  ogImageHeight: 630,
  ogImageAlt: () => t('site.ogImageAlt'),
  twitterCard: 'summary_large_image',
  twitterImage: `${SITE_URL}/og-image.png`,
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
