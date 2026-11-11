<template>
  <div class="layout">
    <AppHeader />
    <Toast />
    <div class="layout-content">
      <slot />
    </div>
    <AppFooter />
  </div>
</template>

<style scoped>
/* Keep the footer at the bottom on short pages */
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
}

.layout-content {
  flex: 1;
  /* Lets a page stretch to the remaining height (the home map relies on this) */
  display: flex;
  flex-direction: column;
}
</style>
