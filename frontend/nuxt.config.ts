export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api/v1',
    },
  },

  css: ['leaflet/dist/leaflet.css'],

  vite: {
    optimizeDeps: {
      include: ['leaflet'],
    },
  },
})