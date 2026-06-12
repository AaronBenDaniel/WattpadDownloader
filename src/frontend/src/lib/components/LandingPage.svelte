<script>
  import Seo from "$lib/components/Seo.svelte";

  let { seo, h1, intro, steps, features, faqs, related } = $props();

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a }
    }))
  };

  const allJsonLd = [
    ...(seo.jsonLd ? (Array.isArray(seo.jsonLd) ? seo.jsonLd : [seo.jsonLd]) : []),
    faqSchema
  ];
</script>

<Seo title={seo.title} description={seo.description} path={seo.path} jsonLd={allJsonLd} />

<div class="min-h-screen pb-24">
  <div class="bg-base-200/60 px-4 py-16 text-center">
    <div class="mx-auto max-w-2xl">
      <h1 class="mb-4 text-4xl font-extrabold">{h1}</h1>
      <p class="text-base-content/70 mb-8 text-lg">{intro}</p>
      <a href="/" class="btn btn-primary btn-lg" data-umami-event="Landing CTA Top">
        Download your story - free
      </a>
    </div>
  </div>

  <div class="mx-auto max-w-3xl px-4 py-12">
    <h2 class="mb-8 text-center text-2xl font-bold">How it works</h2>
    <ol class="space-y-6">
      {#each steps as step, i}
        <li class="bg-base-100 border-base-300 flex gap-4 rounded-xl border p-5 shadow-sm">
          <span
            class="border-primary/30 bg-primary/10 flex size-8 shrink-0 items-center justify-center rounded-md border text-sm font-bold"
          >
            {i + 1}
          </span>
          <div>
            <p class="font-semibold">{step.title}</p>
            {#if step.description}
              <p class="text-base-content/70 mt-1 text-sm">{step.description}</p>
            {/if}
          </div>
        </li>
      {/each}
    </ol>
    <div class="mt-10 text-center">
      <a href="/" class="btn btn-primary btn-lg" data-umami-event="Landing CTA Steps">
        Try it now - free
      </a>
    </div>
  </div>

  {#if features.length}
    <div class="bg-base-200/40 px-4 py-12">
      <div class="mx-auto max-w-3xl">
        <h2 class="mb-8 text-center text-2xl font-bold">Why use WP Downloader?</h2>
        <div class="grid gap-4 sm:grid-cols-2">
          {#each features as feature}
            <div class="bg-base-100 border-base-300 rounded-xl border p-5 shadow-sm">
              <p class="font-semibold">{feature.title}</p>
              <p class="text-base-content/70 mt-1 text-sm">{feature.description}</p>
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}

  <div class="mx-auto max-w-3xl px-4 py-12">
    <h2 class="mb-8 text-center text-2xl font-bold">Frequently asked questions</h2>
    <div class="space-y-3">
      {#each faqs as faq}
        <details class="collapse-arrow bg-base-100 border-base-300 collapse border shadow-sm">
          <summary class="collapse-title font-medium">{faq.q}</summary>
          <div class="collapse-content">
            <p class="text-base-content/80 text-sm">{faq.a}</p>
          </div>
        </details>
      {/each}
    </div>
  </div>

  <div class="px-4 pb-4 text-center">
    <a href="/" class="btn btn-primary btn-lg" data-umami-event="Landing CTA Bottom">
      Download your story - free
    </a>
  </div>

  <div class="border-base-300 mx-auto mt-12 max-w-3xl border-t px-4 pt-8">
    <h2 class="mb-4 text-center text-base font-semibold">More from WP Downloader</h2>
    <nav class="flex flex-wrap justify-center gap-3 text-sm">
      {#each related as link}
        <a href={link.href} class="btn btn-outline btn-sm">{link.label}</a>
      {/each}
    </nav>
  </div>
</div>
