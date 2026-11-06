import type { PaginatedResponse } from '~/types'

let refreshPromise: Promise<void> | null = null

export function useApi() {
  const config = useRuntimeConfig()
  const { accessToken, refreshToken } = useAuthTokens()
  const { $i18n, $localePath } = useNuxtApp()

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

  const clearTokens = () => {
    accessToken.value = null
    refreshToken.value = null
  }

  // Network errors and 5xx say nothing about the session, so they must not end it
  const isSessionRejected = (error: any) =>
    !refreshToken.value || [400, 401].includes(error?.response?.status)

  const ensureFreshToken = async (path: string) => {
    if (isAuthPath(path) || !accessToken.value)
      return

    if (isTokenExpired(accessToken.value)) {
      if (!refreshPromise) {
        refreshPromise = refreshAccessToken()
          .catch((error) => {
            if (isSessionRejected(error))
              clearTokens()
            throw error
          })
          .finally(() => {
            refreshPromise = null
          })
      }

      try {
        await refreshPromise
      }
      catch (error) {
        // session rejected: tokens are already cleared, the request below will 401 and redirect.
        // Otherwise fail here, sending the expired token would 401 and end the session
        if (!isSessionRejected(error))
          throw error
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
        clearTokens()
        await navigateTo($localePath('/login'))
      }
      throw error
    }
  }

  const get = <T>(path: string) => request<T>(path)

  const getAll = async <T>(path: string) => {
    const results: T[] = []
    const separator = path.includes('?') ? '&' : '?'

    for (let page = 1; ; page++) {
      const response = await get<PaginatedResponse<T>>(`${path}${separator}page=${page}`)
      results.push(...response.results)
      if (!response.next)
        return results
    }
  }

  const post = <T>(path: string, body: Record<string, unknown> | (() => Record<string, unknown>)) =>
    request<T>(path, { method: 'POST', body })

  const put = <T>(path: string) => request<T>(path, { method: 'PUT' })

  const del = <T>(path: string, body?: Record<string, unknown>) =>
    request<T>(path, { method: 'DELETE', body })

  return { get, getAll, post, put, del }
}
