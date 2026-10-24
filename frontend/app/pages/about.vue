<script setup lang="ts">
definePageMeta({ layout: 'default' })

const { t } = useI18n()

useSeoMeta({
  title: () => t('about.metaTitle'),
  description: () => t('about.metaDescription'),
  ogTitle: () => t('about.metaTitle'),
  ogDescription: () => t('about.metaDescription'),
})

const ARTICLE_URL = 'https://anywhere.pl/polecane/po-cichu-na-glos-razem-o-czytaniu-ktore-laczy-ludzi/'
const AUTHOR_URL = 'https://liubuntu.tech'
const DESIGNER_URL = 'https://www.linkedin.com/in/anastasiia-kirman-4b35b72a4/'

const benefits = computed(() => [
  { title: t('about.partners.visibilityTitle'), text: t('about.partners.visibilityText') },
  { title: t('about.partners.readersTitle'), text: t('about.partners.readersText') },
  { title: t('about.partners.networkTitle'), text: t('about.partners.networkText') },
])

const invitees = computed(() => [
  t('about.partners.inviteBookshops'),
  t('about.partners.inviteLibraries'),
  t('about.partners.inviteClubs'),
  t('about.partners.inviteOrganisers'),
])
</script>

<template>
  <main class="about">
    <div class="grid">
      <!-- Hero -->
      <div class="cell span-9 hero">
        <h1 class="hero-title">
          {{ t('about.heroTitle') }}
        </h1>
      </div>
      <NuxtLinkLocale to="/" class="cell span-3 cell--primary map-link">
        <span class="label label--light">bogorm.app</span>
        <span class="map-link-text">{{ t('about.mapLink') }} →</span>
      </NuxtLinkLocale>

      <!-- What / why / quote -->
      <section class="cell span-4 stack">
        <span class="label label--index">01</span>
        <h2>{{ t('about.what.title') }}</h2>
        <p>{{ t('about.what.text') }}</p>
        <p>{{ t('about.what.free') }}</p>
      </section>
      <section class="cell span-5 stack">
        <span class="label label--index">02</span>
        <h2>{{ t('about.why.title') }}</h2>
        <p>{{ t('about.why.text1') }}</p>
        <p>{{ t('about.why.text2') }}</p>
      </section>
      <div class="cell span-3 cell--yellow quote">
        <p>{{ t('about.quote') }}</p>
      </div>

      <!-- Who -->
      <div class="cell span-4 row-2 photo">
        <img src="/images/liuba.jpg" :alt="t('about.who.photoAlt')" width="720" height="960" loading="lazy">
      </div>
      <section class="cell span-8 stack">
        <span class="label label--index">03</span>
        <h2>{{ t('about.who.title') }}</h2>
        <p>{{ t('about.who.text1') }}</p>
        <i18n-t keypath="about.who.text2" tag="p" scope="global">
          <template #link>
            <a :href="ARTICLE_URL" target="_blank" rel="noopener" class="inline-link">{{ t('about.who.text2Link') }}</a>
          </template>
        </i18n-t>
        <p>{{ t('about.who.text3') }}</p>
      </section>
      <div class="cell span-3 credit">
        <span class="label">{{ t('about.who.authorSite') }}</span>
        <a :href="AUTHOR_URL" target="_blank" rel="noopener" class="credit-link">liubuntu.tech ↗</a>
      </div>
      <div class="cell span-5 credit">
        <span class="label">{{ t('about.who.designer') }}</span>
        <a :href="DESIGNER_URL" target="_blank" rel="noopener" class="credit-link">Anastasiia Kirman ↗</a>
      </div>

      <!-- Partners -->
      <div class="cell span-12 partners-head">
        <div class="stack">
          <span class="label label--index">04</span>
          <h2 class="partners-title">
            {{ t('about.partners.title') }}
          </h2>
        </div>
        <p class="partners-lead">
          {{ t('about.partners.lead') }}
        </p>
      </div>
      <section class="cell span-6 cell--yellow stack">
        <h3>{{ t('about.partners.nonCommercialTitle') }}</h3>
        <p>{{ t('about.partners.nonCommercialText') }}</p>
      </section>
      <section class="cell span-6 stack">
        <h3>{{ t('about.partners.inviteTitle') }}</h3>
        <ul class="invite-list">
          <li v-for="item in invitees" :key="item">
            {{ item }}
          </li>
        </ul>
      </section>
      <section v-for="benefit in benefits" :key="benefit.title" class="cell span-4 stack stack--tight">
        <h4>{{ benefit.title }}</h4>
        <p class="muted">
          {{ benefit.text }}
        </p>
      </section>

      <!-- Contact -->
      <section class="cell span-12 cell--primary contact">
        <div class="stack contact-text">
          <h2>{{ t('about.contact.title') }}</h2>
          <p>{{ t('about.contact.text') }}</p>
        </div>
        <a :href="`mailto:${t('about.contact.email')}`" class="contact-email">
          {{ t('about.contact.email') }}
        </a>
      </section>
    </div>
  </main>
</template>

<style scoped>
.about {
  max-width: 1280px;
  margin: 0 auto;
  padding: calc(var(--header-height) + var(--spacing-xs)) var(--spacing-md) var(--spacing-lg);
}

/* Hairline grid: 1px gap over a grey background draws the lines */
.grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 1px;
  background: var(--color-light-grey-40);
  border: 1px solid var(--color-light-grey-40);
  border-radius: 0;
  overflow: hidden;
}

.cell {
  background: var(--color-white);
  padding: var(--spacing-md);
}

.span-3 { grid-column: span 3; }
.span-4 { grid-column: span 4; }
.span-5 { grid-column: span 5; }
.span-6 { grid-column: span 6; }
.span-8 { grid-column: span 8; }
.span-9 { grid-column: span 9; }
.span-12 { grid-column: span 12; }
.row-2 { grid-row: span 2; }

.cell--primary {
  background: var(--color-primary);
  color: var(--color-white);
}

.cell--yellow {
  background: var(--color-yellow);
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stack--tight {
  gap: 8px;
}

.label {
  font-size: 14px;
  color: var(--color-black);
}

.label--light {
  color: var(--color-light-grey-40);
}

.label--index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: var(--color-yellow);
  color: var(--color-primary);
  font-weight: 700;
}

.muted {
  font-size: 16px;
  color: var(--color-black);
}

/* Hero */
.hero {
  padding-block: var(--spacing-lg);
}

.hero-title {
  font-weight: 300;
  letter-spacing: 0.01em;
}

.map-link {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 8px;
  min-height: 240px;
  text-decoration: none;
}

.map-link-text {
  font-size: 27px;
  font-weight: 500;
  line-height: 1.3;
}

.map-link:hover .map-link-text {
  text-decoration: underline;
}

/* Quote */
.quote {
  display: flex;
  align-items: flex-end;
}

.quote p {
  font-family: 'Merriweather', serif;
  font-weight: 700;
  font-size: 27px;
  line-height: 1.3;
}

/* Who */
.photo {
  position: relative;
  min-height: 560px;
  padding: 0;
}

.photo img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;
  display: block;
}

.inline-link {
  color: inherit;
  text-decoration: underline;
}

.credit {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 6px;
}

.credit-link {
  font-size: 23px;
  font-weight: 500;
  color: var(--color-primary);
  text-decoration: none;
}

.credit-link:hover {
  text-decoration: underline;
}

/* Partners */
.partners-head {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--spacing-xs);
  padding-top: var(--spacing-lg);
}

.partners-title {
  font-family: 'Merriweather', serif;
  font-weight: 700;
  font-size: 40px;
  line-height: 1.2;
  letter-spacing: 0.02em;
}

.partners-lead {
  max-width: 440px;
}

.invite-list {
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Contact */
.contact {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--spacing-md);
  padding-block: var(--spacing-lg);
}

.contact-text {
  flex: 999 1 420px;
  min-width: 0;
}

.contact-text p {
  max-width: 620px;
  color: var(--color-light-grey-40);
}

.contact-email {
  flex: 1 1 260px;
  font-size: 32px;
  font-weight: 500;
  color: var(--color-yellow);
  text-decoration: none;
  overflow-wrap: anywhere;
}

.contact-email:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .grid > .cell {
    grid-column: 1 / -1;
    grid-row: auto;
  }

  .photo {
    min-height: 0;
    aspect-ratio: 4 / 5;
  }

  .map-link {
    min-height: 0;
  }

  .partners-title {
    font-size: 28px;
  }

  .quote p,
  .map-link-text {
    font-size: 22px;
  }
}
</style>
