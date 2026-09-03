<script setup lang="ts">
const route = useRoute()
const { logout } = useAuth()
const router = useRouter()

const navItems = [
  { label: 'Bookmarks', to: '/bookmarks', icon: 'IconsBookmark' },
]

async function handleLogout() {
  await logout()
  await router.push('/')
}
</script>

<template>
  <div class="layout">
    <aside class="sidebar">
      <nav class="nav">
        <NuxtLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          :class="{ 'nav-item--active': route.path === item.to }"
        >
          <component :is="item.icon" class="nav-icon" />
          {{ item.label }}
        </NuxtLink>
      </nav>

      <button class="logout-btn" @click="handleLogout">
        <IconsLogOut class="logout-icon" />
        Log Out
      </button>
    </aside>

    <main class="content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: calc(100vh - var(--header-height));
  padding-top: var(--header-height);
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
  border-right: 1px solid var(--color-light-grey-40);
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: calc(100vh - var(--header-height));
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.75rem;
  border-radius: 8px;
  color: var(--color-black);
  text-decoration: none;
  font-size: 0.95rem;
}

.nav-item:hover {
  background: var(--color-light-grey-40);
}

.nav-item--active {
  background: var(--color-light-grey-40);
  color: var(--color-primary);
  font-weight: 500;
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.65rem;
  border: 1.5px solid var(--color-primary);
  border-radius: 8px;
  color: var(--color-primary);
  background: none;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
}

.content {
  flex: 1;
  padding: 2rem 2.5rem;
  min-width: 0;
}
</style>
