export function useEventCategory() {
  // Keep in sync with the backend EventCategory enum (backend/events/models.py).
  // Unknown/future values fall back to 'Other' below.
  const categoryLabels: Record<number, string> = {
    10: 'Book Presentation',
    20: 'Author Meeting',
    30: 'Discussion',
    40: 'Lecture',
    50: 'Book Club',
    60: 'Other',
  }

  const getCategoryLabel = (category: number) => categoryLabels[category] ?? 'Other'

  return { getCategoryLabel }
}
