export function useAuthForm(action: () => Promise<unknown>, errorMessage: string) {
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
      error.value = errorMessage
    }
    finally {
      isLoading.value = false
    }
  }

  return { error, isLoading, handleSubmit }
}
