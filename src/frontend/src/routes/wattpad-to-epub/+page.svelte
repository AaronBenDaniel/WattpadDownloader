<script>
  import LandingPage from "$lib/components/LandingPage.svelte";

  const seo = {
    title: "Wattpad to EPUB Downloader - Free | WP Downloader",
    description:
      "Download Wattpad Books as EPUB in seconds. Read offline on Kindle, Kobo, Apple Books, or any e-reader. Free, no account required.",
    path: "/wattpad-to-epub/",
    jsonLd: {
      "@context": "https://schema.org",
      "@type": "HowTo",
      name: "How to download a Wattpad story as EPUB",
      description: "Download a WP story as an EPUB file using WP Downloader.",
      step: [
        {
          "@type": "HowToStep",
          position: 1,
          name: "Copy the story URL",
          text: "Open the story on Wattpad and copy its URL from your browser address bar."
        },
        {
          "@type": "HowToStep",
          position: 2,
          name: "Paste the URL into WP Downloader",
          text: "Go to wpd.my, paste the URL, and make sure EPUB is selected as the format."
        },
        {
          "@type": "HowToStep",
          position: 3,
          name: "Click Download",
          text: "Click Download. No account needed for EPUB."
        },
        {
          "@type": "HowToStep",
          position: 4,
          name: "Open on your e-reader",
          text: "Transfer the EPUB to your Kindle, Kobo, Apple Books, or any compatible app."
        }
      ]
    }
  };
</script>

<LandingPage
  {seo}
  h1="Download WP Stories as EPUB"
  intro="Download WP Books as EPUB files - the standard format for e-readers. Open them on Kindle, Kobo, Apple Books, or any reading app. No account required."
  steps={[
    {
      title: "Copy the story URL",
      description: "Open the story on the Wattpad website or app and copy its URL."
    },
    {
      title: "Paste the URL into WP Downloader",
      description: "Go to WP Downloader, paste the URL. EPUB is selected by default."
    },
    {
      title: "Click Download",
      description: "No account needed. Your EPUB is ready in seconds."
    },
    {
      title: "Open on your e-reader or app",
      description: "Transfer to Kindle, Kobo, Apple Books, or open in any EPUB reader."
    }
  ]}
  features={[
    {
      title: "Reflowable text",
      description:
        "EPUB text reflows to fit any screen size, making it ideal for e-readers and reading apps."
    },
    {
      title: "No account required",
      description: "EPUB downloads are free with no sign-in. Just paste a URL and download."
    },
    {
      title: "Compatible with all e-readers",
      description: "EPUB works on Kobo, Apple Books, Google Play Books, Calibre, and more."
    },
    {
      title: "Kindle-compatible via conversion",
      description:
        "Send the EPUB to your Kindle using Amazon's Send-to-Kindle tool or email it to your Kindle address."
    }
  ]}
  faqs={[
    {
      q: "Do I need an account to download EPUB?",
      a: "No. EPUB downloads are free and require no account. Just paste a story URL and click Download."
    },
    {
      q: "Can I read an EPUB on Kindle?",
      a: "Yes. Amazon's Send-to-Kindle service converts EPUB files automatically. Email your EPUB to your Kindle email address or use the Send-to-Kindle app."
    },
    {
      q: "What e-readers support EPUB?",
      a: "Kobo, Apple Books, Google Play Books, PocketBook, and many reading apps like Moon+ Reader and Calibre all support EPUB natively."
    },
    {
      q: "Is downloading stories legal?",
      a: "WP Downloader is intended for personal offline reading of stories you already have access to. Please respect authors' wishes and Wattpad's terms of service."
    },
    {
      q: "Can I include images in my EPUB?",
      a: "Yes. Enable the Include Images option before downloading to embed chapter images in your EPUB file."
    }
  ]}
  related={[
    { label: "WP to PDF", href: "/wattpad-to-pdf/" },
    { label: "Send to Kindle", href: "/send-to-kindle/" },
    { label: "Best EPUB Readers", href: "/help/best-epub-readers-for-wattpad-books/" },
    { label: "Back to tool", href: "/" }
  ]}
/>
