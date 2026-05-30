export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api/v1',
    },
  },

  css: ['leaflet/dist/leaflet.css'],

  vite: {
    optimizeDeps: {
      include: ['leaflet'],
    },
  },
})
