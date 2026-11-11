export function usePlaceCategory() {
  const { t } = useI18n()

  // Keep in sync with the backend PlaceCategory enum (backend/places/models.py).
  // Unknown/future values fall back to 'Other' below.
  const knownCategories = [10, 20, 30, 40, 50, 60]

  const getCategoryLabel = (category: number) => {
    const key = knownCategories.includes(category) ? category : 60
    return t(`placeCategory.${key}`)
  }

  return { getCategoryLabel }
}
