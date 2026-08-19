import { createFileRoute } from "@tanstack/react-router";
import type {} from "@tanstack/react-start";
import { BLOG_POSTS } from "@/lib/blog";
import { WEBSITE_URL } from "@/lib/constants";

const BASE_URL = WEBSITE_URL.replace(/\/$/, "");

interface SitemapEntry {
  path: string;
  lastmod?: string;
  changefreq?: "always" | "hourly" | "daily" | "weekly" | "monthly" | "yearly" | "never";
  priority?: string;
}

export const Route = createFileRoute("/sitemap.xml")({
  server: {
    handlers: {
      GET: async () => {
        // Tenta carregar posts dinâmicos do manifest
        let dynamicEntries: SitemapEntry[] = [];
        try {
          const manifestRes = await fetch(`${BASE_URL}/blog-posts/manifest.json`);
          if (manifestRes.ok) {
            const slugs: string[] = await manifestRes.json();
            dynamicEntries = slugs.map((slug) => ({
              path: `/blog/${slug}`,
              changefreq: "monthly" as const,
              priority: "0.7",
            }));
          }
        } catch {
          // ignora se manifest não existir ainda
        }

        const entries: SitemapEntry[] = [
          { path: "/", changefreq: "weekly", priority: "1.0" },
          { path: "/blog", changefreq: "weekly", priority: "0.8" },
          ...dynamicEntries,
          ...BLOG_POSTS.map((p) => ({
            path: `/blog/${p.slug}`,
            lastmod: p.date,
            changefreq: "monthly" as const,
            priority: "0.7",
          })),
        ];

        const urls = entries.map((e) =>
          [
            `  <url>`,
            `    <loc>${BASE_URL}${e.path}</loc>`,
            e.lastmod ? `    <lastmod>${e.lastmod}</lastmod>` : null,
            e.changefreq ? `    <changefreq>${e.changefreq}</changefreq>` : null,
            e.priority ? `    <priority>${e.priority}</priority>` : null,
            `  </url>`,
          ]
            .filter(Boolean)
            .join("\n"),
        );

        const xml = [
          `<?xml version="1.0" encoding="UTF-8"?>`,
          `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`,
          ...urls,
          `</urlset>`,
        ].join("\n");

        return new Response(xml, {
          headers: { "Content-Type": "application/xml", "Cache-Control": "public, max-age=3600" },
        });
      },
    },
  },
});
