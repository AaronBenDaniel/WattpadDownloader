<script>
  import Seo from "$lib/components/Seo.svelte";

  const articles = [
    {
      slug: "how-to-download-wattpad-story-as-pdf",
      title: "How to Download a Wattpad Story as PDF",
      description:
        "A step-by-step guide to downloading WP stories as PDF files using WP Downloader."
    },
    {
      slug: "how-to-read-wattpad-offline",
      title: "How to Read Wattpad Stories Offline",
      description: "Download WP stories as EPUB or PDF and read them offline on any device."
    },
    {
      slug: "how-to-send-wattpad-stories-to-kindle",
      title: "How to Send Wattpad Stories to Kindle",
      description:
        "Download WP stories as EPUB and send them to your Kindle using Amazon's Send-to-Kindle."
    },
    {
      slug: "how-to-convert-wattpad-to-epub",
      title: "How to Convert Wattpad Stories to EPUB",
      description: "Download WP Books as EPUB files in seconds. No account needed."
    },
    {
      slug: "best-epub-readers-for-wattpad-books",
      title: "Best EPUB Readers for WP Books",
      description: "The best apps and devices to read WP stories you've downloaded as EPUB files."
    }
  ];
</script>

<Seo
  title="Help & Guides - WP Downloader"
  description="Step-by-step guides for downloading WP stories as PDF or EPUB, reading offline, sending to Kindle, and more."
  path="/help/"
/>

<div class="min-h-screen pb-24">
  <div class="bg-base-200/60 px-4 py-12 text-center">
    <div class="mx-auto max-w-2xl">
      <h1 class="mb-3 text-3xl font-extrabold">Help & Guides</h1>
      <p class="text-base-content/70">Everything you need to download and read WP Books offline.</p>
    </div>
  </div>

  <div class="mx-auto max-w-3xl px-4 py-10">
    <div class="grid gap-4 sm:grid-cols-2">
      {#each articles as article}
        <a
          href="/help/{article.slug}/"
          class="bg-base-100 border-base-300 hover:border-primary/50 block rounded-xl border p-5 shadow-sm transition-colors"
        >
          <h2 class="mb-1 font-semibold">{article.title}</h2>
          <p class="text-base-content/70 text-sm">{article.description}</p>
        </a>
      {/each}
    </div>

    <div class="border-base-300 mt-12 border-t pt-8 text-center">
      <p class="text-base-content/60 mb-4 text-sm">Looking for the download tool?</p>
      <a href="/" class="btn btn-primary">Go to WP Downloader</a>
    </div>
  </div>
</div>
