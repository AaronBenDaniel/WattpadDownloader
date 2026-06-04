<script>
  import "../app.css";
  import { init, i18n, t } from "$lib/i18n/index.svelte.js";
  import ThemeToggle from "$lib/components/ThemeToggle.svelte";
  /**
   * @typedef {Object} Props
   * @property {import('svelte').Snippet} [children]
   */

  /** @type {Props} */
  let { children } = $props();

  $effect(() => {
    init();
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

<footer
  class="footer bg-base-300 text-base-content fixed bottom-0 flex items-center justify-center gap-4 px-4 py-2 text-sm"
>
  <a
    href="https://discord.gg/P9RHC4KCwd"
    target="_blank"
    class="link"
    data-umami-event="Footer Discord">{t("footer_discord")}</a
  >
  <span class="text-base-content/30">·</span>
  <p>{t("footer_copyright")}</p>
</footer>
