<script>
  import { i18n, LOCALES, setLocale } from "$lib/i18n/index.svelte.js";
</script>

<div class="grid grid-cols-3 gap-2">
  {#each LOCALES as loc}
    <button
      class="btn btn-sm h-auto min-h-[2rem] flex-wrap py-1 text-center leading-tight whitespace-normal {loc.code ===
      i18n.locale
        ? 'btn-primary'
        : 'btn-outline'}"
      style="height:auto"
      onclick={() => setLocale(loc.code)}
      ><div style="margin: 3px">
        <span class="whitespace-nowrap">{loc.flag} {loc.englishName || loc.name}</span>
        {#if loc.englishName}
          <span class="whitespace-nowrap">({loc.name})</span>
        {/if}
      </div>
    </button>
  {/each}
</div>
