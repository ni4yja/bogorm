export const useApi = () => {
  const config = useRuntimeConfig()

  const get = <T>(path: string) =>
    $fetch<T>(`${config.public.apiBase}${path}`)

  return { get }
}