export function useApi() {
  const config = useRuntimeConfig()
  const { accessToken, refreshToken } = useAuthTokens()

  const AUTH_PATHS = ['/auth/login/', '/auth/register/', '/auth/refresh/']
  const isAuthPath = (path: string) => AUTH_PATHS.some(p => path.startsWith(p))

  const getAuthHeaders = (path: string): Record<string, string> => {
    if (isAuthPath(path) || !accessToken.value)
      return {}
    return { Authorization: `Bearer ${accessToken.value}` }
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

  const fetchWithAuth = <T>(path: string, options: Record<string, unknown>) =>
    $fetch<T>(`${config.public.apiBase}${path}`, {
      ...options,
      headers: getAuthHeaders(path),
    })

  const request = async <T>(path: string, options: Record<string, unknown> = {}) => {
    try {
      return await fetchWithAuth<T>(path, options)
    }
    catch (error: any) {
      if (!isAuthPath(path) && error?.response?.status === 401 && refreshToken.value) {
        await refreshAccessToken()
        return await fetchWithAuth<T>(path, options)
      }
      throw error
    }
  }

  const get = <T>(path: string) => request<T>(path)

  const post = <T>(path: string, body: Record<string, unknown>) =>
    request<T>(path, { method: 'POST', body })

  return { get, post }
}
