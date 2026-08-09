export function useAuthTokens() {
  const accessToken = useLocalStorage<string | null>('access_token', null)
  const refreshToken = useLocalStorage<string | null>('refresh_token', null)

  return { accessToken, refreshToken }
}
