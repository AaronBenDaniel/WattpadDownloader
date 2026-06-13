<script>
  import LandingPage from "$lib/components/LandingPage.svelte";

  const seo = {
    title: "Wattpad to PDF Downloader - Free | WP Downloader",
    description:
      "Download Wattpad Books as PDF in seconds. Download stories for offline reading on any device. Free, supports images, no account required for EPUB.",
    path: "/wattpad-to-pdf/",
    jsonLd: {
      "@context": "https://schema.org",
      "@type": "HowTo",
      name: "How to download a Wattpad story as PDF",
      description: "Download a WP story as a PDF file using WP Downloader.",
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
          text: "Go to wpd.my, paste the URL into the input field, and select PDF as your format."
        },
        {
          "@type": "HowToStep",
          position: 3,
          name: "Sign in with Discord",
          text: "PDF downloads require a free Discord account. Sign in once and you're set."
        },
        {
          "@type": "HowToStep",
          position: 4,
          name: "Download your PDF",
          text: "Click Download and save the PDF file to your device."
        }
      ]
    }
  };
</script>

<LandingPage
  {seo}
  h1="Download WP Stories as PDF"
  intro="Save your favourite WP Books as PDF files for offline reading. Formatted beautifully with chapter headings, images, and full text, ready to read on any device."
  steps={[
    {
      title: "Copy the story URL",
      description: "Open the story on the Wattpad website or app and copy its URL."
    },
    {
      title: "Paste the URL and select PDF",
      description: "Go to WP Downloader, paste the URL, and choose PDF as your format."
    },
    {
      title: "Sign in with Discord (free)",
      description: "PDF generation requires a free Discord account to keep the service sustainable."
    },
    {
      title: "Download your PDF",
      description: "Click Download. Your PDF will be ready in seconds."
    }
  ]}
  features={[
    {
      title: "Formatted for reading",
      description:
        "Stories are formatted with clean chapter headings, proper typography, and consistent spacing."
    },
    {
      title: "Images included (optional)",
      description: "Enable the Include Images option to embed cover images and in-chapter photos."
    },
    {
      title: "Any device",
      description:
        "PDF files open on phones, tablets, laptops, and e-readers like Kindle via email."
    },
    {
      title: "Free to use",
      description: "WP Downloader is free. Free Discord members gain access to PDF downloads and faster speeds."
    }
  ]}
  faqs={[
    {
      q: "Is WP Downloader free?",
      a: "Yes, WP Downloader is free to use. Free Discord members gain access to PDF downloads and faster speeds."
    },
    {
      q: "Why do I need a Discord account for PDF downloads?",
      a: "PDF generation is compute-intensive. Requiring a Discord account helps us keep the service free by preventing abuse."
    },
    {
      q: "Is downloading stories legal?",
      a: "WP Downloader is intended for personal offline reading of stories you already have access to. Please respect authors' wishes and Wattpad's terms of service."
    },
    {
      q: "Does it work on mobile?",
      a: "Yes. The website works in any mobile browser. Your PDF downloads directly to your device."
    }
  ]}
  related={[
    { label: "WP to EPUB", href: "/wattpad-to-epub/" },
    { label: "Send to Kindle", href: "/send-to-kindle/" },
    { label: "Help & Guides", href: "/help/" }
  ]}
/>
