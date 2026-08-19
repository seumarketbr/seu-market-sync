import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, CalendarDays, Clock, Newspaper } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { SiteFooter } from "@/components/SiteFooter";
import { FloatingWhatsApp } from "@/components/FloatingWhatsApp";
import { sortedPosts, formatDate } from "@/lib/blog";
import { WEBSITE_URL } from "@/lib/constants";

const TITLE = "Blog — Seu Market Br | Minimercado autônomo em condomínios";
const DESCRIPTION =
  "Artigos sobre minimercado autônomo 24h, conveniência em condomínios, tecnologia de lojas sem funcionários e gestão condominial em Belém-PA.";

export const Route = createFileRoute("/blog/")({
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESCRIPTION },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "website" },
      { property: "og:url", content: "/blog" },
    ],
    links: [{ rel: "canonical", href: "/blog" }],
    scripts: [
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Blog",
          name: "Blog Seu Market Br",
          description: DESCRIPTION,
          url: `${WEBSITE_URL}blog`,
          publisher: { "@type": "Organization", name: "Seu Market Br", url: WEBSITE_URL },
          blogPost: sortedPosts().map((p) => ({
            "@type": "BlogPosting",
            headline: p.title,
            description: p.excerpt,
            datePublished: p.date,
            url: `${WEBSITE_URL}blog/${p.slug}`,
            author: { "@type": "Organization", name: p.author },
          })),
        }),
      },
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "BreadcrumbList",
          itemListElement: [
            { "@type": "ListItem", position: 1, name: "Início", item: WEBSITE_URL },
            { "@type": "ListItem", position: 2, name: "Blog", item: `${WEBSITE_URL}blog` },
          ],
        }),
      },
    ],
  }),
  component: BlogIndex,
});

function BlogIndex() {
  const posts = sortedPosts();
  const [featured, ...rest] = posts;

  return (
    <div className="min-h-screen bg-background font-sans">
      <Navbar />
      <FloatingWhatsApp />

      {/* HERO */}
      <header className="pt-32 pb-16 bg-[image:var(--gradient-hero)] text-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Trilha de navegação" className="text-xs text-white/60 mb-5">
            <a href="/" className="hover:text-primary transition-colors">Início</a>
            <span className="mx-2">/</span>
            <span className="text-white/90">Blog</span>
          </nav>
          <span className="inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary">
            <Newspaper className="size-3.5" /> Conteúdo Seu Market Br
          </span>
          <h1 className="mt-5 font-display text-4xl md:text-5xl font-bold max-w-3xl leading-tight">
            Blog: conveniência, tecnologia e condomínios
          </h1>
          <p className="mt-4 max-w-2xl text-white/70 leading-relaxed">
            Tudo sobre minimercados autônomos 24h: como funcionam, quanto espaço ocupam, segurança,
            tecnologia e o impacto na valorização do seu condomínio.
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        {featured && (
          <article className="grid lg:grid-cols-2 gap-8 items-center rounded-3xl overflow-hidden border border-border shadow-card bg-card">
            <img
              src={featured.cover}
              alt={featured.title}
              className="h-64 lg:h-full w-full object-cover"
              loading="eager"
            />
            <div className="p-8 lg:p-10">
              <span className="text-xs font-semibold uppercase tracking-wider text-primary-dark bg-lime-soft rounded-full px-3 py-1">
                {featured.category}
              </span>
              <h2 className="mt-4 font-display text-2xl md:text-3xl font-bold leading-snug">
                <Link to="/blog/$slug" params={{ slug: featured.slug }} className="hover:text-primary-dark transition-colors">
                  {featured.title}
                </Link>
              </h2>
              <p className="mt-3 text-muted-foreground leading-relaxed">{featured.excerpt}</p>
              <div className="mt-5 flex items-center gap-4 text-xs text-muted-foreground">
                <span className="inline-flex items-center gap-1.5"><CalendarDays className="size-3.5" /> {formatDate(featured.date)}</span>
                <span className="inline-flex items-center gap-1.5"><Clock className="size-3.5" /> {featured.readingMinutes} min de leitura</span>
              </div>
              <Link
                to="/blog/$slug"
                params={{ slug: featured.slug }}
                className="mt-7 inline-flex items-center gap-2 rounded-full bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-lime hover:-translate-y-0.5 transition-transform"
              >
                Ler artigo <ArrowRight className="size-4" />
              </Link>
            </div>
          </article>
        )}

        <h2 className="mt-16 mb-8 font-display text-2xl font-bold">Últimos artigos</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-7">
          {rest.map((post) => (
            <article
              key={post.slug}
              className="group rounded-2xl overflow-hidden border border-border bg-card shadow-card hover:shadow-elevated transition-shadow"
            >
              <Link to="/blog/$slug" params={{ slug: post.slug }} className="block">
                <img src={post.cover} alt={post.title} className="h-48 w-full object-cover" loading="lazy" />
              </Link>
              <div className="p-6">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-primary-dark bg-lime-soft rounded-full px-3 py-1">
                  {post.category}
                </span>
                <h3 className="mt-4 font-display text-lg font-bold leading-snug">
                  <Link to="/blog/$slug" params={{ slug: post.slug }} className="group-hover:text-primary-dark transition-colors">
                    {post.title}
                  </Link>
                </h3>
                <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{post.excerpt}</p>
                <div className="mt-4 flex items-center gap-4 text-xs text-muted-foreground">
                  <span className="inline-flex items-center gap-1.5"><CalendarDays className="size-3.5" /> {formatDate(post.date)}</span>
                  <span className="inline-flex items-center gap-1.5"><Clock className="size-3.5" /> {post.readingMinutes} min</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </main>

      <SiteFooter />
    </div>
  );
}