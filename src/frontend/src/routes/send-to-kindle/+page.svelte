<script>
  import LandingPage from "$lib/components/LandingPage.svelte";

  const seo = {
    title: "Send Wattpad Stories to Kindle - Free | WP Downloader",
    description:
      "Download WP Books as EPUB and send them to your Kindle. Works with any Kindle device or app. Free, no account required.",
    path: "/send-to-kindle/",
    jsonLd: {
      "@context": "https://schema.org",
      "@type": "HowTo",
      name: "How to send a Wattpad story to Kindle",
      description:
        "Download a WP story as EPUB using WP Downloader, then send it to your Kindle device.",
      step: [
        {
          "@type": "HowToStep",
          position: 1,
          name: "Download the story as EPUB",
          text: "Go to wpd.my, paste the WP story URL, and download it as an EPUB file."
        },
        {
          "@type": "HowToStep",
          position: 2,
          name: "Find your Kindle email address",
          text: "In Amazon's 'Manage Your Content and Devices', find the Send-to-Kindle email for your device."
        },
        {
          "@type": "HowToStep",
          position: 3,
          name: "Email the EPUB to your Kindle",
          text: "Send an email with the EPUB file attached to your Kindle email address. Amazon converts and delivers it automatically."
        },
        {
          "@type": "HowToStep",
          position: 4,
          name: "Read on your Kindle",
          text: "The story appears in your Kindle library within minutes."
        }
      ]
    }
  };
</script>

<LandingPage
  {seo}
  h1="Send WP Stories to Your Kindle"
  intro="Read your favourite WP Books on your Kindle. Download as EPUB using WP Downloader, then send to your Kindle in minutes using Amazon's free Send-to-Kindle service."
  steps={[
    {
      title: "Download the story as EPUB",
      description:
        "Paste the WP story URL into WP Downloader and download as EPUB. No account needed."
    },
    {
      title: "Find your Kindle email address",
      description:
        "Go to Amazon → Manage Your Content and Devices → Preferences → Personal Document Settings to find your device's email address."
    },
    {
      title: "Email the EPUB to your Kindle",
      description:
        "Attach the EPUB to an email and send it to your Kindle email address. Amazon converts it automatically."
    },
    {
      title: "Read on your Kindle",
      description:
        "Your story appears in your Kindle library within a few minutes, ready to read offline."
    }
  ]}
  features={[
    {
      title: "Works with all Kindle devices",
      description:
        "Kindle Paperwhite, Kindle Scribe, Kindle app on iOS and Android - all support Send-to-Kindle."
    },
    {
      title: "Amazon converts the file",
      description:
        "Amazon automatically converts EPUB to Kindle format. You don't need any extra software."
    },
    {
      title: "Free service",
      description: "Both WP Downloader and Amazon's Send-to-Kindle are free to use."
    },
    {
      title: "Also works via the Send-to-Kindle app",
      description:
        "The Amazon Send-to-Kindle desktop app lets you drag-and-drop EPUB files directly to your Kindle."
    }
  ]}
  faqs={[
    {
      q: "Does Kindle support EPUB files?",
      a: "Kindle now supports EPUB natively (since 2022). You can email EPUB files to your Kindle email address and Amazon delivers them to your device."
    },
    {
      q: "Where do I find my Kindle email address?",
      a: "Go to Amazon.com → Manage Your Content and Devices → Preferences → Personal Document Settings. Each Kindle device has its own @kindle.com address."
    },
    {
      q: "Is there a file size limit for Send-to-Kindle?",
      a: "Amazon accepts documents up to 50 MB via email. Most WP story EPUBs are well under this limit, even with images."
    },
    {
      q: "Can I use the Send-to-Kindle app instead of email?",
      a: "Yes. Amazon's Send-to-Kindle desktop app (Windows and Mac) lets you drag-and-drop an EPUB file to send it to your Kindle without using email."
    },
    {
      q: "Is downloading stories legal?",
      a: "WP Downloader is intended for personal offline reading of stories you already have access to. Please respect authors' wishes and Wattpad's terms of service."
    }
  ]}
  related={[
    { label: "WP to EPUB", href: "/wattpad-to-epub/" },
    { label: "WP to PDF", href: "/wattpad-to-pdf/" },
    {
      label: "How to Send to Kindle (guide)",
      href: "/help/how-to-send-wattpad-stories-to-kindle/"
    },
    { label: "Back to tool", href: "/" }
  ]}
/>
