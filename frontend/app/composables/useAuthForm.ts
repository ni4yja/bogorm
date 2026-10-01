// ponytail: errorMessage is resolved lazily (string | () => string) instead of
// a pre-resolved string, so a t('...') passed in stays reactive to locale
// switches — it's read at the moment the error actually fires, not captured
// once when the page mounts.
export function useAuthForm(action: () => Promise<unknown>, errorMessage: string | (() => string)) {
  const router = useRouter()

  const error = ref('')
  const isLoading = ref(false)

  async function handleSubmit() {
    error.value = ''
    isLoading.value = true

    try {
      await action()
      await router.push('/')
    }
    catch {
      error.value = typeof errorMessage === 'function' ? errorMessage() : errorMessage
    }
    finally {
      isLoading.value = false
    }
  }

  return { error, isLoading, handleSubmit }
}
