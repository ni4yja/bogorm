export default defineNuxtRouteMiddleware(() => {
  // Tokens live in localStorage, which the server can't see —
  // checking here would bounce every logged-in user on a hard reload.
  // The check runs again on the client during hydration.
  if (import.meta.server)
    return

  // useAuth() / useLocalePath() rely on component setup context, which middleware
  // doesn't have — read the token directly and use the plugin helper (as useApi does)
  const { accessToken } = useAuthTokens()
  const { $localePath } = useNuxtApp()

  // An expired access token still counts: useApi refreshes it on the first request
  if (!accessToken.value)
    return navigateTo($localePath('/login'))
})
