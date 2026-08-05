<script setup lang="ts">
const { isAuthenticated, logout } = useAuth()
const router = useRouter()

const isDropdownOpen = ref(false)

async function handleLogout() {
  isDropdownOpen.value = false
  await logout()
  await router.push('/')
}
</script>

<template>
  <header class="header">
    <NuxtLink to="/" class="logo">
      Bogorm
    </NuxtLink>

    <nav v-if="!isAuthenticated" class="nav">
      <NuxtLink to="/register" class="btn btn-primary">
        Sign Up
      </NuxtLink>
      <NuxtLink to="/login" class="btn btn-outline">
        <IconsLogIn class="btn-icon" /> Log In
      </NuxtLink>
    </nav>

    <div v-else class="account">
      <button class="account-trigger" @click="isDropdownOpen = !isDropdownOpen">
        <IconsProfile class="avatar-icon" />
        <IconsChevronDown class="chevron" :class="{ open: isDropdownOpen }" />
      </button>

      <div v-if="isDropdownOpen" class="dropdown">
        <button class="dropdown-item" @click="handleLogout">
          <IconsLogIn class="dropdown-icon dropdown-icon--logout" />
          Log Out
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-xs) var(--spacing-md);
  height: var(--header-height);
  background: var(--color-white);
}

.logo {
  font-family: 'Merriweather', serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--color-primary);
  text-decoration: none;
}

.nav {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.btn {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-white);
}

.btn-outline {
  background: transparent;
  border: 1.5px solid var(--color-primary);
  color: var(--color-primary);
}

.account {
  position: relative;
}

.account-trigger {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  color: var(--color-primary);
}

.avatar-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
}

.chevron {
  width: 18px;
  height: 18px;
  transition: transform 0.15s ease;
}

.chevron.open {
  transform: rotate(180deg);
}

.dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: var(--color-white);
  border: 1px solid var(--color-light-grey-40);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  min-width: 160px;
  overflow: hidden;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-align: left;
  padding: 0.65rem 1rem;
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  color: var(--color-primary);
}

.dropdown-item:hover {
  background: var(--color-light-grey-40);
}

.dropdown-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.dropdown-icon--logout {
  transform: scaleX(-1);
}
</style>
