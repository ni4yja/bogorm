<script setup lang="ts">
definePageMeta({ layout: 'default' })

const { t } = useI18n()
</script>

<template>
  <div class="placeholder">
    <p>{{ t('events.comingSoon') }}</p>
  </div>
</template>

<style scoped>
.placeholder {
  padding-top: calc(var(--header-height) + 4rem);
  text-align: center;
  color: var(--color-grey);
}
</style>
