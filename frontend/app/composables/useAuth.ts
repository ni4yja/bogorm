import type { CurrentUser } from '~/types'

export function useAuth() {
  const { accessToken, refreshToken } = useAuthTokens()
  const { get, post, del } = useApi()
  const { resetBookmarks } = useBookmarks()
  const localePath = useLocalePath()

  const isAuthenticated = computed(() => !!accessToken.value)

  // Everything that belongs to the signed-in user, cleared in one place
  const clearSession = () => {
    accessToken.value = null
    refreshToken.value = null
    resetBookmarks()
  }

  const login = async (email: string, password: string) => {
    const response = await post<{ access: string, refresh: string }>('/auth/login/', {
      email,
      password,
    })
    // Logging in as a different user without logging out first shouldn't
    // leak the previous account's cached bookmark state
    resetBookmarks()
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
        // logout is best-effort: clear local state even if the request fails
      }
    }
    clearSession()
  }

  const logoutAndRedirect = async () => {
    await logout()
    await navigateTo(localePath('/'))
  }

  const fetchCurrentUser = () => get<CurrentUser>('/auth/me/')

  // Throws on 400 (wrong password) so the modal can show the error inline
  const deleteAccount = async (password: string) => {
    await del('/auth/me/', { password })
    clearSession()
    await navigateTo(localePath('/'))
  }

  return {
    isAuthenticated,
    login,
    register,
    logout,
    logoutAndRedirect,
    fetchCurrentUser,
    deleteAccount,
  }
}
