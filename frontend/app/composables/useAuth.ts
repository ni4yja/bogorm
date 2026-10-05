export function useAuth() {
  const { accessToken, refreshToken } = useAuthTokens()
  const { post } = useApi()
  const localePath = useLocalePath()

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
        // logout is best-effort: clear local tokens even if the request fails
      }
    }
    accessToken.value = null
    refreshToken.value = null
  }

  const logoutAndRedirect = async () => {
    await logout()
    await navigateTo(localePath('/'))
  }

  return { isAuthenticated, login, register, logout, logoutAndRedirect }
}
