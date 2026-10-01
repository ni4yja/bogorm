let refreshPromise: Promise<void> | null = null

export function useApi() {
  const config = useRuntimeConfig()
  const { accessToken, refreshToken } = useAuthTokens()
  const router = useRouter()
  // ponytail: useNuxtApp().$i18n instead of useI18n() — useI18n() needs Vue's
  // component instance (getCurrentInstance()), which is gone after an `await`
  // inside an async setup/lifecycle callback. useApi() gets called that way
  // (useMapMarkers() inside index.vue's async onMounted), so useI18n() would
  // throw "Must be called at the top of a setup function" there. $i18n reads
  // through Nuxt's app context instead, which survives post-await calls.
  const { $i18n } = useNuxtApp()

  const AUTH_PATHS = ['/auth/login/', '/auth/register/', '/auth/refresh/']
  const isAuthPath = (path: string) => AUTH_PATHS.some(p => path.startsWith(p))

  const isTokenExpired = (token: string): boolean => {
    try {
      const parts = token.split('.')
      if (parts.length !== 3)
        return true

      const payload = JSON.parse(atob(parts[1]!))
      return payload.exp * 1000 < Date.now()
    }
    catch {
      return true
    }
  }

  const refreshAccessToken = async () => {
    if (!refreshToken.value)
      throw new Error('No refresh token')

    const response = await $fetch<{ access: string, refresh: string }>(
      `${config.public.apiBase}/auth/refresh/`,
      { method: 'POST', body: { refresh: refreshToken.value } },
    )

    accessToken.value = response.access
    refreshToken.value = response.refresh
  }

  const ensureFreshToken = async (path: string) => {
    if (isAuthPath(path) || !accessToken.value)
      return

    if (isTokenExpired(accessToken.value)) {
      if (!refreshPromise) {
        refreshPromise = refreshAccessToken()
          .catch((error) => {
            accessToken.value = null
            refreshToken.value = null
            throw error
          })
          .finally(() => {
            refreshPromise = null
          })
      }

      try {
        await refreshPromise
      }
      catch {
      }
    }
  }

  const getHeaders = (path: string): Record<string, string> => {
    const headers: Record<string, string> = {
      'Accept-Language': $i18n.locale.value,
    }

    if (!isAuthPath(path) && accessToken.value) {
      headers.Authorization = `Bearer ${accessToken.value}`
    }

    return headers
  }

  const request = async <T>(
    path: string,
    options: {
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
      body?: Record<string, unknown> | (() => Record<string, unknown>)
    } = {},
  ) => {
    await ensureFreshToken(path)

    const resolvedBody = typeof options.body === 'function' ? options.body() : options.body

    try {
      return await $fetch<T>(`${config.public.apiBase}${path}`, {
        method: options.method,
        body: resolvedBody,
        headers: getHeaders(path),
      })
    }
    catch (error: any) {
      if (!isAuthPath(path) && error?.response?.status === 401) {
        await router.push('/login')
      }
      throw error
    }
  }

  const get = <T>(path: string) => request<T>(path)

  const post = <T>(path: string, body: Record<string, unknown> | (() => Record<string, unknown>)) =>
    request<T>(path, { method: 'POST', body })

  const put = <T>(path: string) => request<T>(path, { method: 'PUT' })

  const del = <T>(path: string) => request<T>(path, { method: 'DELETE' })

  return { get, post, put, del }
}
