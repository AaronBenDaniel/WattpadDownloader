<script>
  import Seo from "$lib/components/Seo.svelte";

  let { data } = $props();

  const { content: ArticleContent, meta } = data;
</script>

<Seo
  title="{meta.title} | Wattpad Downloader"
  description={meta.description}
  path="/help/{meta.slug}/"
  jsonLd={{
    "@context": "https://schema.org",
    "@type": "Article",
    headline: meta.title,
    description: meta.description,
    datePublished: meta.datePublished,
    dateModified: meta.dateModified,
    publisher: {
      "@type": "Organization",
      name: "Wattpad Downloader",
      url: "https://wpd.my"
    }
  }}
/>

<div class="min-h-screen pb-24">
  <div class="mx-auto max-w-2xl px-4 py-12">
    <div class="bg-base-100/85 backdrop-blur-sm rounded-2xl p-6 sm:p-10 shadow-sm">
      <a href="/help/" class="text-base-content/50 hover:text-base-content mb-6 inline-block text-sm">
        ← All guides
      </a>

      <article class="prose prose-sm sm:prose max-w-none">
        <h1>{meta.title}</h1>
        <ArticleContent />
      </article>

      <div class="bg-base-200 my-10 rounded-xl p-6 text-center">
        <p class="mb-3 font-semibold">Ready to download your story?</p>
        <a href="/" class="btn btn-primary" data-umami-event="Article CTA">
          Open WP Downloader - free
        </a>
      </div>

      {#if meta.related?.length}
        <div class="border-base-300 border-t pt-8">
          <p class="mb-3 text-sm font-semibold">Related guides</p>
          <nav class="flex flex-wrap gap-2">
            {#each meta.related as link}
              <a href={link.href} class="btn btn-outline btn-sm">{link.label}</a>
            {/each}
          </nav>
        </div>
      {/if}
    </div>
  </div>
</div>
