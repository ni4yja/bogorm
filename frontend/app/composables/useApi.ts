let refreshPromise: Promise<void> | null = null

export function useApi() {
  const config = useRuntimeConfig()
  const { accessToken, refreshToken } = useAuthTokens()
  const router = useRouter()

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

  const getAuthHeaders = (path: string): Record<string, string> => {
    if (isAuthPath(path) || !accessToken.value)
      return {}
    return { Authorization: `Bearer ${accessToken.value}` }
  }

  const request = async <T>(path: string, options: Record<string, unknown> = {}) => {
    await ensureFreshToken(path)

    try {
      return await $fetch<T>(`${config.public.apiBase}${path}`, {
        ...options,
        headers: getAuthHeaders(path),
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

  const post = <T>(path: string, body: Record<string, unknown>) =>
    request<T>(path, { method: 'POST', body })

  return { get, post }
}
