export function useEventCategory() {
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
