<script>
  import { t } from "$lib/i18n/index.svelte.js";
  import {
    hasFeature,
    getUserId,
    getExternalIdentifier,
    clearUser
  } from "$lib/stores/features.svelte.js";
  import LanguageSelector from "$lib/components/LanguageSelector.svelte";
  import { browser } from "$app/environment";

  import LinkIcon from "$lib/icons/LinkIcon.svelte";
  import LibraryIcon from "$lib/icons/LibraryIcon.svelte";
  import ArchiveIcon from "$lib/icons/ArchiveIcon.svelte";
  import UserIcon from "$lib/icons/UserIcon.svelte";
  import LockIcon from "$lib/icons/LockIcon.svelte";
  import EyeIcon from "$lib/icons/EyeIcon.svelte";
  import EyeOffIcon from "$lib/icons/EyeOffIcon.svelte";
  import DownloadIcon from "$lib/icons/DownloadIcon.svelte";
  import GlobeIcon from "$lib/icons/GlobeIcon.svelte";
  import InfoIcon from "$lib/icons/InfoIcon.svelte";
  import DiscordIcon from "$lib/icons/DiscordIcon.svelte";
  import BookIcon from "$lib/icons/BookIcon.svelte";
  import FileTextIcon from "$lib/icons/FileTextIcon.svelte";

  let inputUrl = $state("");
  let storyURLTutorialModal = $state();
  let signOutModal = $state();
  let showPassword = $state(false);
  let includeImages = $state(false);
  let downloadAsPdf = $state(false); // 0 = epub, 1 = pdf
  let isPaidStory = $state(false);
  let downloadImages = $state(false);
  let source = $state("url");
  let urlNeeded = $derived(source == "url");
  let loginRequired = $derived(source != "url" || isPaidStory);
  let invalidUrl = $derived(false);
  let afterDownloadPage = $derived(false);
  let downloadId = $state("");
  let rememberedMode = $state("");
  let mode = $derived(source == "url" ? rememberedMode : source);
  let credentials = $state({
    username: "",
    password: ""
  });

  let isBulkDownload = $derived(source !== "url" || mode === "list");
  let pdfAllowed = $derived(
    hasFeature("pdf_download") && (!isBulkDownload || hasFeature("unrestricted_pdf"))
  );

  $effect(() => {
    if (downloadAsPdf && !pdfAllowed) {
      downloadAsPdf = false;
    }
  });

  let downloadButtonDisabled = $derived(
    (!inputUrl && urlNeeded) || (loginRequired && !(credentials.username && credentials.password))
  );

  let url = $derived.by(() => {
    let base =
      `/download/` +
      (urlNeeded ? downloadId : "0") +
      `?om=1` +
      `&download_images=${downloadImages}` +
      (loginRequired
        ? `&username=${encodeURIComponent(credentials.username)}&password=${encodeURIComponent(credentials.password)}`
        : "") +
      `&mode=${mode}` +
      `&format=${downloadAsPdf ? "pdf" : "epub"}`;
    const uid = getUserId();
    if (uid) {
      base += `&user_id=${encodeURIComponent(uid)}`;
    }
    return base;
  });

  /** @param {string} input */
  const setInputAsValid = (input) => {
    invalidUrl = false;
    inputUrl = input;
    downloadId = input;
  };

  /** @param {string} input */
  const setInputAsInvalid = (input) => {
    invalidUrl = true;
    inputUrl = input;
    downloadId = input;
  };

  /** @param {string} input */
  const setInputUrl = (input) => {
    input = input.toLowerCase();

    if (!input) {
      rememberedMode = "";
      setInputAsValid("");
      return;
    }

    if (/^\d+$/.test(input)) {
      // All numbers
      mode = "story";
      rememberedMode = mode;
      setInputAsValid(input);
      return;
    }

    if (!input.includes("wattpad.com/")) {
      setInputAsInvalid(input.match(/\d+/g)?.join("") ?? "");
      return;
    }

    // Is a string and contains wattpad.com/

    if (input.includes("/story/")) {
      // https://wattpad.com/story/237369078-wattpad-books-presents
      mode = "story";
      rememberedMode = mode;
      setInputAsValid(
        input.split("-", 1)[0].split("?", 1)[0].split("/story/")[1] // removes tracking fields and title
      );
    } else if (input.includes("/stories/")) {
      // https://www.wattpad.com/api/v3/stories/237369078?fields=...
      mode = "story";
      rememberedMode = mode;
      setInputAsValid(
        input.split("?", 1)[0].split("/stories/")[1] // removes params
      );
    } else if (input.includes("/list/")) {
      // https://www.wattpad.com/list/1582628905
      mode = "list";
      rememberedMode = mode;
      setInputAsValid(
        input.split("?", 1)[0].split("/list/")[1] // removes tracking fields
      );
    } else {
      // https://www.wattpad.com/939051741-wattpad-books-presents-the-qb-bad-boy-and-me
      input = input.split("-", 1)[0].split("?", 1)[0].split("wattpad.com/")[1]; // removes tracking fields and title
      if (/^\d+$/.test(input)) {
        // If "wattpad.com/{downloadId}" contains only numbers
        mode = "part";
        rememberedMode = mode;
        setInputAsValid(input);
      } else {
        setInputAsInvalid("");
      }
    }
  };
</script>

<div>
  <div class="hero min-h-screen">
    <div
      class="hero-content bg-base-100/50 flex-col rounded py-32 shadow-sm lg:flex-row-reverse lg:items-start lg:p-16"
    >
      {#if !afterDownloadPage}
        <div class="max-w-lg text-center lg:p-10 lg:text-left">
          <h1
            class="bg-gradient-to-r from-red-700 via-yellow-600 to-pink-600 bg-clip-text text-5xl font-extrabold text-transparent"
          >
            {t("title")}
          </h1>
          <div
            role="alert"
            class="alert discord-alert mt-10 max-w-md bg-indigo-100 break-words text-black"
          >
            <InfoIcon />
            <div>
              <p>
                {t("discord_cta")}
                <span class="font-semibold">{t("discord_cta_highlight")}</span>
              </p>
              <a href="https://discord.gg/P9RHC4KCwd" class="link" target="_blank"
                >{t("discord_join_now")}</a
              >
            </div>
          </div>
          <p class="max-w-md pt-6 text-lg">
            {t("hero_description")}
          </p>
          <div class="pt-4">
            <div class="mb-2 flex items-center justify-center lg:justify-start">
              <GlobeIcon />
              <span class="ml-1 text-lg font-bold">Site Language</span>
            </div>
            <LanguageSelector />
          </div>
        </div>

        <form
          class="bg-base-100 border-base-300 rounded-2xl border px-5 pt-4 pb-4 shadow-xl"
          id="wpd-download-form"
        >
          <input type="hidden" name="path" />

          <!-- 1 · SOURCE -->
          <div class="grid grid-cols-[28px_1fr] gap-x-3.5 gap-y-1.5 pt-0.5" data-section="source">
            <span
              class="step-badge-active border-primary/30 mt-0.5 inline-flex size-[22px] items-center justify-center rounded-md border text-xs font-bold"
              >1</span
            >
            <div class="flex min-h-6 items-center gap-2.5">
              <h3 class="m-0 text-xs font-bold tracking-[0.14em] uppercase">{t("source")}</h3>
            </div>
            <div class="col-start-2">
              <div class="flex flex-wrap gap-2.5" role="radiogroup" aria-label="Download source">
                {#each [{ key: "url", icon: LinkIcon, labelKey: "url", descKey: "url_desc" }, { key: "library", icon: LibraryIcon, labelKey: "library", descKey: "library_desc" }, { key: "archive", icon: ArchiveIcon, labelKey: "archive", descKey: "archive_desc" }] as tile}
                  {@const Icon = tile.icon}
                  <button
                    type="button"
                    class="focus-visible:outline-primary grid min-w-0 flex-1 basis-28 cursor-pointer grid-cols-[auto_1fr] items-center
                      gap-x-2.5 gap-y-px rounded-lg border p-2.5 text-left transition-all
                      duration-150 focus-visible:outline-2 focus-visible:outline-offset-2
                      {source === tile.key
                      ? 'border-primary bg-primary/5 ring-primary ring-1 ring-inset'
                      : 'bg-base-200/30 border-base-300 hover:border-base-content/20 hover:bg-base-100'}"
                    role="radio"
                    aria-checked={source === tile.key}
                    data-tile
                    onclick={() => (source = tile.key)}
                  >
                    <span
                      class="col-start-1 row-start-1 inline-flex size-5 items-center justify-center
                        {source === tile.key ? 'text-primary' : 'text-base-content/60'}"
                      ><Icon /></span
                    >
                    <span class="col-start-2 row-start-1 text-sm font-semibold"
                      >{t(tile.labelKey)}</span
                    >
                    <span
                      class="text-base-content/50 col-span-full row-start-2 text-xs leading-snug"
                      >{t(tile.descKey)}</span
                    >
                  </button>
                {/each}
              </div>
            </div>
          </div>

          <!-- 2 · STORY URL -->
          <div
            class="border-base-200 grid grid-cols-[28px_1fr] gap-x-3.5 gap-y-1.5 border-t py-2
              transition-opacity duration-200 {!urlNeeded ? 'opacity-50' : ''}"
            data-section="url"
            aria-disabled={!urlNeeded}
          >
            <span
              class="mt-0.5 inline-flex size-[22px] items-center justify-center rounded-md border
                text-xs font-bold {urlNeeded
                ? 'step-badge-active border-primary/30'
                : 'bg-base-200 text-base-content/50 border-base-300'}">2</span
            >
            <div class="flex min-h-6 items-center gap-2.5">
              <h3 class="m-0 text-xs font-bold tracking-[0.14em] uppercase">
                {t("story_url_placeholder")}
              </h3>
              <span
                class="badge badge-xs font-semibold tracking-wider uppercase
                  {urlNeeded ? 'badge-primary' : 'badge-outline'}"
              >
                {urlNeeded ? t("required") : t("not_needed")}
              </span>
            </div>
            <div class="col-start-2 {!urlNeeded ? 'pointer-events-none' : ''}">
              <div class="flex flex-col gap-1">
                <label class="mb-1 block text-xs font-semibold" for="wpd-url"
                  >{t("wattpad_url")}</label
                >
                <div
                  class="bg-base-100 focus-within:border-primary focus-within:ring-primary/20 flex h-9 w-full items-center gap-2 rounded-lg
                    border px-3 transition-all
                    focus-within:ring-2 {invalidUrl ? 'border-error' : 'border-base-300'}"
                >
                  <span class="text-base-content/40 inline-flex shrink-0"
                    ><LinkIcon size={16} /></span
                  >
                  <input
                    id="wpd-url"
                    name="story_url"
                    type="text"
                    autocomplete="off"
                    placeholder={t("story_url_placeholder")}
                    disabled={!urlNeeded}
                    class="placeholder:text-base-content/30 h-full min-w-0 grow border-0 bg-transparent p-0 text-sm
                      outline-none disabled:cursor-not-allowed"
                    bind:value={() => inputUrl, setInputUrl}
                  />
                </div>
              </div>
              <div class="mt-1.5 flex items-center justify-between gap-4">
                {#if invalidUrl}
                  <p class="text-error text-sm">
                    {t("invalid_url_refer")}<button
                      class="hover:text-primary cursor-pointer border-0 bg-transparent p-0
                        text-sm font-bold underline transition-colors"
                      onclick={() => storyURLTutorialModal.showModal()}
                      data-umami-event="Part StoryURLTutorialModal Open"
                      type="button">{t("how_to_get_url")}</button
                    >{t("invalid_url_refer_end")}
                  </p>
                {:else}
                  <button
                    class="hover:text-primary cursor-pointer border-0 bg-transparent p-0
                      text-sm font-bold underline transition-colors"
                    onclick={() => storyURLTutorialModal.showModal()}
                    data-umami-event="StoryURLTutorialModal Open"
                    type="button">{t("how_to_get_url")}</button
                  >
                {/if}
                <label
                  class="inline-flex cursor-pointer items-center gap-2 text-sm select-none
                    {!urlNeeded ? 'cursor-not-allowed opacity-50' : ''}"
                >
                  <input
                    type="checkbox"
                    class="checkbox checkbox-xs checkbox-primary"
                    name="paid_story"
                    data-paid
                    disabled={!urlNeeded}
                    bind:checked={isPaidStory}
                  />
                  <span
                    ><strong>{t("paid_story_label")}</strong>
                    <span class="text-base-content/50">{t("paid_story_label_end")}</span></span
                  >
                </label>
              </div>
            </div>
          </div>

          <!-- 3 · ACCOUNT -->
          <div
            class="border-base-200 grid grid-cols-[28px_1fr] gap-x-3.5 gap-y-1.5 border-t py-2
              transition-opacity duration-200 {!loginRequired ? 'opacity-50' : ''}"
            data-section="account"
            aria-disabled={!loginRequired}
          >
            <span
              class="mt-0.5 inline-flex size-[22px] items-center justify-center rounded-md border
                text-xs font-bold {loginRequired
                ? 'step-badge-active border-primary/30'
                : 'bg-base-200 text-base-content/50 border-base-300'}">3</span
            >
            <div class="flex min-h-6 items-center gap-2.5">
              <h3 class="m-0 text-xs font-bold tracking-[0.14em] uppercase">
                {t("wattpad_account")}
              </h3>
              <span
                class="badge badge-xs font-semibold tracking-wider uppercase
                  {loginRequired ? 'badge-primary' : 'badge-outline'}"
              >
                {loginRequired ? t("required") : t("not_needed")}
              </span>
            </div>
            <div class="col-start-2 {!loginRequired ? 'pointer-events-none' : ''}">
              <div class="flex w-full min-w-0 flex-col gap-2">
                <div class="flex flex-col gap-1">
                  <label class="mb-1 block text-xs font-semibold" for="wpd-username"
                    >{t("username")}</label
                  >
                  <div
                    class="border-base-300 bg-base-100 focus-within:border-primary focus-within:ring-primary/20 flex h-9 w-full items-center
                      gap-2 rounded-lg border px-3 transition-all
                      focus-within:ring-2"
                  >
                    <span class="text-base-content/40 inline-flex shrink-0"><UserIcon /></span>
                    <input
                      id="wpd-username"
                      name="username"
                      type="text"
                      autocomplete="username"
                      placeholder="your.handle"
                      disabled={!loginRequired}
                      class="placeholder:text-base-content/30 h-full min-w-0 grow border-0 bg-transparent p-0 text-sm
                        outline-none disabled:cursor-not-allowed"
                      bind:value={credentials.username}
                    />
                  </div>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="mb-1 block text-xs font-semibold" for="wpd-password"
                    >{t("password")}</label
                  >
                  <div
                    class="border-base-300 bg-base-100 focus-within:border-primary focus-within:ring-primary/20 flex h-9 w-full items-center
                      gap-2 rounded-lg border px-3 transition-all
                      focus-within:ring-2"
                  >
                    <span class="text-base-content/40 inline-flex shrink-0"><LockIcon /></span>
                    <input
                      id="wpd-password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      autocomplete="current-password"
                      placeholder={showPassword ? t("password") : "••••••••"}
                      disabled={!loginRequired}
                      class="placeholder:text-base-content/30 h-full min-w-0 grow border-0 bg-transparent p-0
                        text-sm lowercase outline-none disabled:cursor-not-allowed"
                      bind:value={credentials.password}
                    />
                    <button
                      type="button"
                      class="text-base-content/40 hover:text-base-content hover:bg-base-200 inline-flex cursor-pointer
                        rounded border-0 bg-transparent p-1"
                      data-toggle-pw
                      aria-label={showPassword ? "Hide password" : "Show password"}
                      tabindex={loginRequired ? undefined : "-1"}
                      onclick={() => {
                        showPassword = !showPassword;
                      }}
                    >
                      {#if showPassword}<EyeOffIcon />{:else}<EyeIcon />{/if}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 4 · FORMAT -->
          <div
            class="border-base-200 grid grid-cols-[28px_1fr] gap-x-3.5 gap-y-1.5 border-t py-2
              transition-opacity duration-200 {!pdfAllowed ? 'opacity-50' : ''}"
            data-section="format"
            aria-disabled={!pdfAllowed}
          >
            <span
              class="mt-0.5 inline-flex size-[22px] items-center justify-center rounded-md border
                text-xs font-bold {pdfAllowed
                ? 'step-badge-active border-primary/30'
                : 'bg-base-200 text-base-content/50 border-base-300'}">4</span
            >
            <div class="flex min-h-6 items-center gap-2.5">
              <h3 class="m-0 text-xs font-bold tracking-[0.14em] uppercase">
                {t("format_label")}
              </h3>
              {#if !pdfAllowed}
                <span class="badge badge-outline badge-xs font-semibold tracking-wider uppercase">
                  {#if !hasFeature("pdf_download")}
                    {t(getUserId() ? "format_pdf_no_access" : "format_pdf_locked")}
                  {:else}
                    {t("format_pdf_bulk_locked")}
                  {/if}
                </span>
              {/if}
            </div>
            <div class="col-start-2 {!pdfAllowed ? 'pointer-events-none' : ''}">
              <div class="flex flex-wrap gap-2.5" role="radiogroup" aria-label="Format">
                {#each [{ key: "epub", labelKey: "format_epub", icon: BookIcon }, { key: "pdf", labelKey: "format_pdf", icon: FileTextIcon }] as fmt}
                  {@const Icon = fmt.icon}
                  {@const isActive = fmt.key === "pdf" ? downloadAsPdf : !downloadAsPdf}
                  <button
                    type="button"
                    class="focus-visible:outline-primary grid min-w-0 flex-1 basis-28 grid-cols-[auto_1fr] items-center
                      gap-x-2.5 rounded-lg border p-2.5 text-left transition-all
                      duration-150 focus-visible:outline-2 focus-visible:outline-offset-2
                      {isActive
                      ? 'border-primary bg-primary/5 ring-primary ring-1 ring-inset'
                      : 'bg-base-200/30 border-base-300 hover:border-base-content/20 hover:bg-base-100 cursor-pointer'}"
                    role="radio"
                    aria-checked={isActive}
                    disabled={!pdfAllowed}
                    onclick={() => (downloadAsPdf = fmt.key === "pdf")}
                  >
                    <span
                      class="col-start-1 row-start-1 inline-flex size-5 items-center justify-center
                        {isActive ? 'text-primary' : 'text-base-content/60'}"><Icon /></span
                    >
                    <span class="col-start-2 row-start-1 text-sm font-semibold"
                      >{t(fmt.labelKey)}</span
                    >
                  </button>
                {/each}
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="border-base-200 mt-1 flex flex-col gap-3 border-t pt-3.5">
            <div class="flex items-center justify-between gap-4">
              <div class="flex flex-col gap-1.5">
                <label class="inline-flex cursor-pointer items-center gap-2 text-sm select-none">
                  <input
                    type="checkbox"
                    class="checkbox checkbox-xs checkbox-primary"
                    name="include_images"
                    data-include-images
                    bind:checked={downloadImages}
                  />
                  <span
                    ><strong>{t("include_images_bold")}</strong>
                    <span class="text-base-content/50">{t("include_images")}</span></span
                  >
                </label>
              </div>
            </div>

            <div class="flex items-center justify-between gap-4">
              {#if getExternalIdentifier()}
                <div class="flex items-center gap-2 text-xs">
                  <span class="text-base-content/60"
                    >{t("signed_in_as")}
                    <span class="font-semibold">{getExternalIdentifier()}</span></span
                  >
                  <button
                    type="button"
                    class="badge badge-outline badge-sm hover:bg-base-300 cursor-pointer whitespace-nowrap"
                    onclick={() => signOutModal.showModal()}>{t("sign_out")}</button
                  >
                </div>
              {:else}
                <span class="text-base-content/50 text-xs"
                  >{t("sign_in_cta")}
                  <a href="https://discord.gg/P9RHC4KCwd" target="_blank" class="link"
                    >{t("discord_link")}</a
                  ></span
                >
              {/if}
              <button
                type="submit"
                class="btn btn-primary"
                id="wpd-submit"
                name="submit"
                disabled={downloadButtonDisabled}
                ><a href={url} onclick={() => (afterDownloadPage = true)}>
                  <DownloadIcon /><span data-cta>{t("download")}</span></a
                >
              </button>
            </div>
          </div>
        </form>
      {:else}
        <div class="max-w-4xl text-center">
          <h1 class="text-3xl font-bold">
            {t("download_started")}
            <span
              class="bg-gradient-to-r from-red-700 via-yellow-600 to-pink-600 bg-clip-text text-transparent"
              >{t("download_started_highlight")}</span
            >
          </h1>
          <div class="space-y-2 py-4">
            <p class="pt-2 text-lg">
              {t("discord_before")}<a
                href="https://discord.gg/P9RHC4KCwd"
                target="_blank"
                class="link"
                data-umami-event="Discord">{t("discord_link")}</a
              >{t("discord_after")}
            </p>
          </div>
          <div class="grid grid-rows-2 justify-center gap-y-10">
            <a
              href="https://discord.gg/P9RHC4KCwd"
              target="_blank"
              class="btn btn-lg discord-btn mt-10 bg-indigo-500 text-white hover:bg-indigo-600"
              ><DiscordIcon />{t("join_discord")}</a
            >
            <button
              onclick={() => {
                afterDownloadPage = false;
                inputUrl = "";
              }}
              class="btn btn-outline btn-lg">{t("download_more")}</button
            >
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>

<dialog class="modal" bind:this={storyURLTutorialModal}>
  <div class="modal-box">
    <form method="dialog">
      <button class="btn btn-circle btn-ghost btn-sm absolute top-2 right-2">✕</button>
    </form>
    <h3 class="text-lg font-bold">{t("modal_title")}</h3>
    <ol class="list list-inside list-disc space-y-4 py-4">
      <li>{t("modal_step1")}</li>
      <li>
        {t("modal_step2_before")}
        <span class="bg-base-200 p-1 font-mono"
          >wattpad.com/<span class="bg-warning/30 rounded-sm">story</span
          >/9341306-news-updates</span
        >{t("modal_step2_after")}
      </li>
      <li>
        <span class="bg-base-200 p-1 font-mono"
          >https://www.wattpad.com/1623482034-news-updates</span
        >{t("modal_step3_after")}
      </li>
      <li>
        {t("modal_step4")}<span class="bg-base-200 p-1 font-mono"
          >https://www.wattpad.com/list/1582628905</span
        >
      </li>
      <li>{t("modal_step5")}</li>
    </ol>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>

<dialog class="modal" bind:this={signOutModal}>
  <div class="modal-box max-w-sm">
    <h3 class="text-lg font-bold">{t("sign_out_confirm_title")}</h3>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn btn-ghost">{t("cancel")}</button>
      </form>
      <button
        class="btn btn-error"
        onclick={() => {
          signOutModal.close();
          clearUser();
          window.location.reload();
        }}>{t("sign_out")}</button
      >
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
