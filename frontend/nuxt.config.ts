export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api/v1',
    },
  },

  css: [
    'leaflet/dist/leaflet.css',
    '~/assets/css/global.css',
  ],

  app: {
    head: {
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Merriweather:wght@700&display=swap',
        },
      ],
    },
  },

  vite: {
    optimizeDeps: {
      include: ['leaflet'],
    },
  },
})
