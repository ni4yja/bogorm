<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const { register } = useAuth()
const { t } = useI18n()

const email = ref('')
const username = ref('')
const password = ref('')
const accepted = ref(false)

// Inputs that can show their own error; anything else from the API goes to the general message
const FIELDS = ['email', 'username', 'password'] as const
type Field = typeof FIELDS[number]

const fieldErrors = ref<Partial<Record<Field, string>>>({})

function isField(key: string): key is Field {
  return (FIELDS as readonly string[]).includes(key)
}

function toMessage(value: unknown): string {
  return [value].flat().join(' ')
}

// The backend's field messages already follow Accept-Language
function mapError(err: any): string {
  if (err?.response?.status !== 400 || !err.data)
    return t('register.errorDefault')

  const perField: Partial<Record<Field, string>> = {}
  const general: string[] = []

  for (const [key, value] of Object.entries(err.data as Record<string, unknown>)) {
    if (isField(key))
      perField[key] = toMessage(value)
    else
      general.push(toMessage(value))
  }

  fieldErrors.value = perField
  return general.length > 0 ? general.join(' ') : t('register.checkFields')
}

const { error, isLoading, handleSubmit } = useAuthForm(
  () => {
    fieldErrors.value = {}
    return register(email.value, username.value, password.value, accepted.value)
  },
  mapError,
)
</script>

<template>
  <AuthLayout :title="t('register.title')" :subtitle="t('register.subtitle')">
    <form class="auth-form" @submit.prevent="handleSubmit">
      <label class="label" for="email">{{ t('register.emailLabel') }}</label>
      <input
        id="email"
        v-model="email"
        type="email"
        :placeholder="t('register.emailPlaceholder')"
        class="input"
        :class="{ 'input--invalid': fieldErrors.email }"
        :aria-invalid="!!fieldErrors.email"
        :aria-describedby="fieldErrors.email ? 'email-error' : undefined"
        required
        @input="fieldErrors.email = undefined"
      >
      <p v-if="fieldErrors.email" id="email-error" class="error">
        {{ fieldErrors.email }}
      </p>

      <label class="label" for="username">{{ t('register.usernameLabel') }}</label>
      <input
        id="username"
        v-model="username"
        type="text"
        :placeholder="t('register.usernamePlaceholder')"
        class="input"
        :class="{ 'input--invalid': fieldErrors.username }"
        :aria-invalid="!!fieldErrors.username"
        :aria-describedby="fieldErrors.username ? 'username-error' : undefined"
        required
        @input="fieldErrors.username = undefined"
      >
      <p v-if="fieldErrors.username" id="username-error" class="error">
        {{ fieldErrors.username }}
      </p>

      <label class="label" for="password">{{ t('register.passwordLabel') }}</label>
      <input
        id="password"
        v-model="password"
        type="password"
        :placeholder="t('register.passwordPlaceholder')"
        class="input"
        :class="{ 'input--invalid': fieldErrors.password }"
        :aria-invalid="!!fieldErrors.password"
        :aria-describedby="fieldErrors.password ? 'password-error' : undefined"
        minlength="8"
        required
        @input="fieldErrors.password = undefined"
      >
      <p v-if="fieldErrors.password" id="password-error" class="error">
        {{ fieldErrors.password }}
      </p>

      <label class="consent">
        <input v-model="accepted" type="checkbox" required>
        <i18n-t keypath="register.consent" tag="span" scope="global">
          <template #terms>
            <NuxtLinkLocale to="/terms" target="_blank">{{ t('register.consentTerms') }}</NuxtLinkLocale>
          </template>
          <template #privacy>
            <NuxtLinkLocale to="/privacy" target="_blank">{{ t('register.consentPrivacy') }}</NuxtLinkLocale>
          </template>
        </i18n-t>
      </label>

      <p v-if="error" class="error" role="alert">
        {{ error }}
      </p>

      <button type="submit" class="btn-submit" :disabled="isLoading">
        {{ isLoading ? t('register.submitting') : t('register.submit') }}
      </button>
    </form>

    <p class="switch-link">
      {{ t('register.hasAccount') }} <NuxtLinkLocale to="/login">
        {{ t('register.logInLink') }}
      </NuxtLinkLocale>
    </p>

    <i18n-t keypath="register.needHelp" tag="p" scope="global" class="switch-link help-link">
      <template #email>
        <a :href="SUPPORT_MAILTO">{{ SUPPORT_EMAIL }}</a>
      </template>
    </i18n-t>
  </AuthLayout>
</template>

<style scoped>
/* Two classes so it outranks the global `.auth-form .input` border */
.auth-form .input--invalid {
  border-color: var(--color-error);
}

.consent {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.875rem;
  line-height: 1.4;
  margin-bottom: var(--spacing-xs);
}

.consent input {
  flex-shrink: 0;
  margin-top: 0.2em;
}

.consent a {
  color: inherit;
}

/* Secondary to the login link: smaller and set apart, so it reads as a footnote */
.help-link {
  margin-top: 1.5rem;
  font-size: 12px;
}
</style>
