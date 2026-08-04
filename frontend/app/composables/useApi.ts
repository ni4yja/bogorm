export function useApi() {
  const config = useRuntimeConfig()
  const accessToken = useLocalStorage<string | null>('access_token', null)
  const refreshToken = useLocalStorage<string | null>('refresh_token', null)

  const getAuthHeaders = (): Record<string, string> => {
    if (!accessToken.value)
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

  const request = async <T>(path: string, options: Record<string, unknown> = {}) => {
    try {
      return await $fetch<T>(`${config.public.apiBase}${path}`, {
        ...options,
        headers: getAuthHeaders(),
      })
    }
    catch (error: any) {
      if (error?.response?.status === 401 && refreshToken.value) {
        await refreshAccessToken()
        return await $fetch<T>(`${config.public.apiBase}${path}`, {
          ...options,
          headers: getAuthHeaders(),
        })
      }
      throw error
    }
  }

  const get = <T>(path: string) => request<T>(path)

  const post = <T>(path: string, body: Record<string, unknown>) =>
    request<T>(path, { method: 'POST', body })

  return { get, post }
}
