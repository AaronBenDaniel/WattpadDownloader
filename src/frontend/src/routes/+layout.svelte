<script>
  import "../app.css";
  import { init, i18n, t } from "$lib/i18n/index.svelte.js";
  import { loadFeatures } from "$lib/stores/features.svelte.js";
  import ThemeToggle from "$lib/components/ThemeToggle.svelte";
  /**
   * @typedef {Object} Props
   * @property {import('svelte').Snippet} [children]
   */

  /** @type {Props} */
  let { children } = $props();

  $effect(() => {
    init();
    loadFeatures();
  });

  $effect(() => {
    document.documentElement.lang = i18n.locale;
  });
</script>

<svelte:head>
  <style>
    body {
      background-image: url("/background-pattern.svg");
    }
  </style>
</svelte:head>

<div class="fixed top-4 right-4 z-50">
  <ThemeToggle />
</div>

{@render children()}

<footer class="footer footer-center bg-base-300 text-base-content fixed bottom-0 p-4">
  <aside>
    <a
      href="https://discord.gg/P9RHC4KCwd"
      target="_blank"
      class="link"
      data-umami-event="Footer Discord">{t("footer_discord")}</a
    >
    <p>{t("footer_copyright")}</p>
  </aside>
</footer>
