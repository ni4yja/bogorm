<script setup lang="ts">
const emit = defineEmits<{
  close: []
}>()

const { t } = useI18n()
const { deleteAccount } = useAuth()

const password = ref('')
const error = ref('')
const isSubmitting = ref(false)
const passwordRef = useTemplateRef('passwordRef')

onMounted(() => {
  passwordRef.value?.focus()
})

function handleClose() {
  // Don't let the user close the modal mid-request
  if (!isSubmitting.value)
    emit('close')
}

async function handleSubmit() {
  error.value = ''
  isSubmitting.value = true

  try {
    await deleteAccount(password.value)
    // deleteAccount redirects home on success; nothing left to do here
  }
  catch (err: any) {
    // The backend message already follows Accept-Language
    error.value = err?.response?.status === 400
      ? err.data?.password?.[0] ?? t('deleteAccount.genericError')
      : t('deleteAccount.genericError')
    isSubmitting.value = false
  }
}
</script>

<template>
  <BaseModal :title="t('deleteAccount.title')" @close="handleClose">
    <p class="warning">
      {{ t('deleteAccount.warning') }}
    </p>

    <form @submit.prevent="handleSubmit">
      <label for="delete-password" class="label">
        {{ t('deleteAccount.passwordLabel') }}
      </label>
      <input
        id="delete-password"
        ref="passwordRef"
        v-model="password"
        type="password"
        autocomplete="current-password"
        class="input"
        :class="{ 'input--error': error }"
        :aria-invalid="!!error"
        aria-describedby="delete-password-error"
      >
      <p v-if="error" id="delete-password-error" class="error">
        {{ error }}
      </p>

      <div class="actions">
        <button type="button" class="btn btn-outline" :disabled="isSubmitting" @click="handleClose">
          {{ t('deleteAccount.cancel') }}
        </button>
        <button type="submit" class="btn btn-danger" :disabled="isSubmitting || !password">
          {{ isSubmitting ? t('deleteAccount.deleting') : t('deleteAccount.confirm') }}
        </button>
      </div>
    </form>
  </BaseModal>
</template>

<style scoped>
.warning {
  color: var(--color-black);
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 1.25rem;
}

.label {
  display: block;
  font-size: 0.9rem;
  color: var(--color-grey);
  margin-bottom: 0.4rem;
}

.input {
  width: 100%;
  box-sizing: border-box;
  padding: 0.65rem 0.75rem;
  border: 1px solid var(--color-light-grey);
  border-radius: 8px;
  font-size: 1rem;
}

.input--error {
  border-color: var(--color-error);
}

.error {
  color: var(--color-error);
  font-size: 0.85rem;
  margin: 0.4rem 0 0;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.6rem 1.1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-outline {
  background: none;
  border: 1.5px solid var(--color-primary);
  color: var(--color-primary);
}

.btn-danger {
  background: var(--color-error);
  border: 1.5px solid var(--color-error);
  color: var(--color-white);
}
</style>
