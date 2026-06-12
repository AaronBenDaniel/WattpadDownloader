<script>
  import { t } from "$lib/i18n/index.svelte.js";
</script>

<svelte:head>
  <title>Error | Wattpad Downloader</title>
</svelte:head>

<div class="flex">
  <div class="hero min-h-screen">
    <div class="hero-content text-center">
      <div class="bg-base-200 max-w-lg rounded-md p-16">
        <h1 class="text-5xl font-bold">{t("error_title")}</h1>
        <div class="join py-6">
          <a class="btn btn-primary btn-lg" href="/">{t("error_home")}</a>
        </div>
      </div>
    </div>
  </div>

  <footer class="footer footer-center bg-base-300 text-base-content fixed bottom-0 p-4">
    <aside class="text-2xl">
      <p>WPDownloader © 2026</p>
    </aside>
  </footer>
</div>
