export function useAuth() {
  const accessToken = useLocalStorage<string | null>('access_token', null)
  const refreshToken = useLocalStorage<string | null>('refresh_token', null)
  const { post } = useApi()

  const isAuthenticated = computed(() => !!accessToken.value)

  const login = async (email: string, password: string) => {
    const response = await post<{ access: string, refresh: string }>('/auth/login/', {
      email,
      password,
    })
    accessToken.value = response.access
    refreshToken.value = response.refresh
  }

  const register = async (email: string, username: string, password: string) => {
    await post('/auth/register/', { email, username, password })
    await login(email, password)
  }

  const logout = async () => {
    if (refreshToken.value) {
      try {
        await post('/auth/logout/', { refresh: refreshToken.value })
      }
      catch {
      }
    }
    accessToken.value = null
    refreshToken.value = null
  }

  return { isAuthenticated, login, register, logout }
}
