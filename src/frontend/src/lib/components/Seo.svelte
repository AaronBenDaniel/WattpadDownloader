<script>
  import { SITE } from "$lib/seo/pages.js";

  let {
    title,
    description,
    path,
    ogImage = "/embed.png",
    jsonLd = null,
    noindex = false
  } = $props();

  const canonical = SITE + path;
  const imageUrl = ogImage.startsWith("http") ? ogImage : SITE + ogImage;
</script>

<svelte:head>
  <title>{title}</title>
  <meta name="description" content={description} />
  {#if noindex}
    <meta name="robots" content="noindex" />
  {/if}
  <link rel="canonical" href={canonical} />

  <meta property="og:type" content="website" />
  <meta property="og:url" content={canonical} />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={imageUrl} />

  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content={canonical} />
  <meta property="twitter:title" content={title} />
  <meta property="twitter:description" content={description} />
  <meta property="twitter:image" content={imageUrl} />

  {#if jsonLd}
    {@html `<script type="application/ld+json">${JSON.stringify(Array.isArray(jsonLd) ? jsonLd : [jsonLd])}</${"script"}>`}
  {/if}
</svelte:head>
