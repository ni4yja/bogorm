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

/* In a flex column, `margin: 0 auto` makes a page shrink to its content instead of stretching.
   Full width restores the old block behaviour; max-width + auto margins still centre it. */
.layout-content > :deep(*) {
  width: 100%;
}
</style>
