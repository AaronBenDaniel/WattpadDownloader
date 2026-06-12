import { SITE, PAGES } from "$lib/seo/pages.js";

export const prerender = true;

export function GET() {
  const urls = PAGES.map(
    (p) => `
  <url>
    <loc>${SITE}${p.path}</loc>
    <lastmod>${p.lastmod}</lastmod>
    <priority>${p.priority}</priority>
  </url>`
  ).join("");

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}
</urlset>`;

  return new Response(body, {
    headers: { "Content-Type": "application/xml" }
  });
}
