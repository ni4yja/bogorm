import { defineCollection, defineContentConfig } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    // One collection per locale; prefix '' keeps paths free of the locale
    // folder, so content/pl/privacy.md is queried as /privacy
    content_pl: defineCollection({
      type: 'page',
      source: { include: 'pl/**', prefix: '' },
    }),
    content_en: defineCollection({
      type: 'page',
      source: { include: 'en/**', prefix: '' },
    }),
  },
})