<script setup lang="ts">
</script>

<template>
  <header class="header">
    <span class="logo">Bogorm</span>
    <nav class="nav">
      <button class="btn btn-primary">
        Sign Up
      </button>
      <button class="btn btn-outline">
        <span>→</span> Log In
      </button>
    </nav>
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
  background: #fff;
}

.logo {
  font-family: 'Merriweather', serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--color-primary);
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
}

.btn-primary {
  background: var(--color-primary);
  color: #fff;
}

.btn-outline {
  background: transparent;
  border: 1.5px solid var(--color-primary);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
</style>
