<script setup lang="ts">
withDefaults(defineProps<{
  title: string
  width?: string
}>(), {
  width: '480px',
})

const emit = defineEmits<{
  close: []
}>()

const { t } = useI18n()

onKeyStroke('Escape', () => emit('close'))
</script>

<template>
  <Teleport to="body">
    <div class="backdrop" @click.self="emit('close')">
      <div
        class="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="base-modal-title"
        :style="{ maxWidth: width }"
      >
        <div class="header">
          <h2 id="base-modal-title" class="title">
            {{ title }}
          </h2>
          <button class="close" :aria-label="t('a11y.close')" @click="emit('close')">
            <IconsClose />
          </button>
        </div>

        <slot />
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  z-index: 2000; /* above the fixed header (1000) */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.4);
}

.modal {
  width: 100%;
  max-height: calc(100vh - 2rem);
  overflow-y: auto;
  background: var(--color-white);
  border-radius: var(--badge-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
  padding: 1.5rem;
}

.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.title {
  color: var(--color-primary);
  font-size: 1.25rem;
  margin: 0;
}

.close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-primary);
  padding: 0.25rem;
  flex-shrink: 0;
}
</style>
