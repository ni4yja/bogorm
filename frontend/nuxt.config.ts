export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@vueuse/nuxt',
    '@nuxtjs/i18n',
  ],

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api/v1',
      cartoApiKey: '',
    },
  },

  css: [
    'leaflet/dist/leaflet.css',
    '~/assets/css/global.css',
  ],

  app: {
    head: {
      script: [
        {
          'src': 'https://stats.bogorm.app/stats.js',
          'defer': true,
          'data-website-id': '388d495c-4e33-4dcb-9d93-34cfa4577fc1',
          'data-domains': 'bogorm.app',
        },
      ],
      meta: [
        { name: 'theme-color', content: '#390000' },
      ],
      link: [
        { rel: 'icon', href: '/favicon.ico', sizes: '48x48' },
        { rel: 'icon', href: '/favicon.svg', type: 'image/svg+xml' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
        { rel: 'manifest', href: '/site.webmanifest' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Merriweather:wght@300;700&display=swap',
        },
      ],
    },
  },

  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
        'leaflet',
      ],
    },
  },

  i18n: {
    locales: [
      { code: 'pl', language: 'pl-PL', name: 'Polski', file: 'pl.json' },
      { code: 'en', language: 'en-GB', name: 'English', file: 'en.json' },
    ],
    defaultLocale: 'pl',
    // Needed for canonical, hreflang and og:url links from useLocaleHead
    baseUrl: 'https://bogorm.app',
    strategy: 'prefix_except_default',
    langDir: 'locales/',
    vueI18n: 'i18n.config.ts',
  },
})
