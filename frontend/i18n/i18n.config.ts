// vue-i18n's built-in default pluralization rule only distinguishes
// 0 / 1 / "everything else" — it has no notion of Polish's one/few/many
// categories, so a 3-form message like "{count} nadchodzące wydarzenie |
// {count} nadchodzące wydarzenia | {count} nadchodzących wydarzeń" picks the
// wrong form for counts 0, 1 and 2-4. This registers the real CLDR rule for
// Polish so vue-i18n selects the correct index.
export default defineI18nConfig(() => ({
  pluralRules: {
    pl: (choice: number, choicesLength: number) => {
      if (choicesLength < 3)
        return choice === 1 ? 0 : 1

      const n = Math.abs(choice)
      if (n === 1)
        return 0

      const mod10 = n % 10
      const mod100 = n % 100
      if (mod10 >= 2 && mod10 <= 4 && !(mod100 >= 12 && mod100 <= 14))
        return 1

      return 2
    },
  },
}))
