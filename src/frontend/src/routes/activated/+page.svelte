<script>
  import { page } from "$app/stores";
  import { t } from "$lib/i18n/index.svelte.js";
  import { setUserId, loadFeatures } from "$lib/stores/features.svelte.js";
  import { browser } from "$app/environment";

  if (browser) {
    const id = $page.url.searchParams.get("id");
    if (id) {
      setUserId(id);
      loadFeatures();
    }
  }
</script>

<div class="flex min-h-screen items-center justify-center">
  <div class="card bg-base-200 max-w-md shadow-xl">
    <div class="card-body text-center">
      <h1 class="card-title justify-center text-2xl">
        {t("activated_title")}
      </h1>
      <p>{t("activated_body")}</p>
      <div class="card-actions mt-4 justify-center">
        <a href="/" class="btn btn-primary">{t("activated_home")}</a>
      </div>
    </div>
  </div>
</div>
