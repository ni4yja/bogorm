<script setup lang="ts">
const { toast, hide } = useToast()
</script>

<template>
  <Transition name="toast">
    <div v-if="toast" class="toast">
      <span class="toast-message">{{ toast.message }}</span>
      <NuxtLink v-if="toast.actionTo" :to="toast.actionTo" class="toast-action" @click="hide">
        {{ toast.actionLabel }}
      </NuxtLink>
      <button class="toast-close" aria-label="Dismiss" @click="hide">
        <IconsClose />
      </button>
    </div>
  </Transition>
</template>

<style scoped>
.toast {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: var(--color-white);
  padding: 0.85rem 1rem 0.85rem 1.25rem;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 2000;
  font-size: 0.9rem;
  white-space: nowrap;
}

.toast-action {
  color: var(--color-white);
  text-decoration: underline;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  color: var(--color-white);
  cursor: pointer;
  display: flex;
  padding: 0.15rem;
}

.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}
</style>
