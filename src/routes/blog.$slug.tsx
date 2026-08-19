import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { ArrowLeft, CalendarDays, Clock, MessageCircle } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { SiteFooter } from "@/components/SiteFooter";
import { FloatingWhatsApp } from "@/components/FloatingWhatsApp";
import { getPost, sortedPosts, formatDate } from "@/lib/blog";
import { WEBSITE_URL, WHATSAPP_URL } from "@/lib/constants";

export const Route = createFileRoute("/blog/$slug")({
  loader: ({ params }) => {
    const post = getPost(params.slug);
    if (!post) throw notFound();
    return post;
  },
  head: ({ params, loaderData }) => {
    if (!loaderData) {
      return {
        meta: [{ title: "Artigo não encontrado — Blog Seu Market Br" }, { name: "robots", content: "noindex" }],
      };
    }
    const url = `${WEBSITE_URL}blog/${params.slug}`;
    return {
      meta: [
        { title: `${loaderData.title} — Blog Seu Market Br` },
        { name: "description", content: loaderData.excerpt },
        { property: "og:title", content: loaderData.title },
        { property: "og:description", content: loaderData.excerpt },
        { property: "og:type", content: "article" },
        { property: "og:url", content: `/blog/${params.slug}` },
        { property: "article:published_time", content: loaderData.date },
        { property: "article:section", content: loaderData.category },
      ],
      links: [{ rel: "canonical", href: `/blog/${params.slug}` }],
      scripts: [
        {
          type: "application/ld+json",
          children: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            headline: loaderData.title,
            description: loaderData.excerpt,
            datePublished: loaderData.date,
            dateModified: loaderData.date,
            articleSection: loaderData.category,
            inLanguage: "pt-BR",
            mainEntityOfPage: { "@type": "WebPage", "@id": url },
            author: { "@type": "Organization", name: loaderData.author, url: WEBSITE_URL },
            publisher: { "@type": "Organization", name: "Seu Market Br", url: WEBSITE_URL },
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
              { "@type": "ListItem", position: 3, name: loaderData.title, item: url },
            ],
          }),
        },
      ],
    };
  },
  notFoundComponent: PostNotFound,
  component: BlogPostPage,
});

function PostNotFound() {
  return (
    <div className="min-h-screen bg-background font-sans">
      <Navbar />
      <div className="pt-40 pb-24 text-center px-4">
        <h1 className="font-display text-3xl font-bold">Artigo não encontrado</h1>
        <p className="mt-3 text-muted-foreground">Esse conteúdo pode ter sido movido ou removido.</p>
        <Link
          to="/blog"
          className="mt-8 inline-flex items-center gap-2 rounded-full bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-lime"
        >
          Voltar para o blog
        </Link>
      </div>
      <SiteFooter />
    </div>
  );
}

function BlogPostPage() {
  const post = Route.useLoaderData();
  const related = sortedPosts().filter((p) => p.slug !== post.slug).slice(0, 3);

  return (
    <div className="min-h-screen bg-background font-sans">
      <Navbar />
      <FloatingWhatsApp />

      <header className="pt-32 pb-14 bg-[image:var(--gradient-hero)] text-white">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Trilha de navegação" className="text-xs text-white/60 mb-5">
            <a href="/" className="hover:text-primary transition-colors">Início</a>
            <span className="mx-2">/</span>
            <Link to="/blog" className="hover:text-primary transition-colors">Blog</Link>
          </nav>
          <span className="text-xs font-semibold uppercase tracking-wider text-primary">{post.category}</span>
          <h1 className="mt-4 font-display text-3xl md:text-4xl font-bold leading-tight">{post.title}</h1>
          <div className="mt-5 flex flex-wrap items-center gap-4 text-xs text-white/60">
            <span className="inline-flex items-center gap-1.5"><CalendarDays className="size-3.5" /> {formatDate(post.date)}</span>
            <span className="inline-flex items-center gap-1.5"><Clock className="size-3.5" /> {post.readingMinutes} min de leitura</span>
            <span>Por {post.author}</span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-14">
        <img src={post.cover} alt={post.title} className="rounded-3xl w-full h-72 object-cover shadow-card" />

        <div className="mt-10 space-y-7">
          {post.content.map((block, i) => (
            <section key={i}>
              {block.h && <h2 className="font-display text-xl md:text-2xl font-bold mb-3">{block.h}</h2>}
              {block.p && <p className="text-base leading-relaxed text-muted-foreground">{block.p}</p>}
              {block.list && (
                <ul className="mt-2 space-y-2">
                  {block.list.map((item) => (
                    <li key={item} className="flex gap-3 text-base text-muted-foreground leading-relaxed">
                      <span className="mt-2 size-1.5 rounded-full bg-primary shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              )}
            </section>
          ))}
        </div>

        <div className="mt-14 rounded-3xl bg-[image:var(--gradient-navy)] text-white p-8 md:p-10 text-center">
          <h2 className="font-display text-2xl font-bold">Quer um minimercado no seu condomínio?</h2>
          <p className="mt-3 text-white/70">Implantação sem custo, tecnologia e conveniência 24h para os moradores.</p>
          <a
            href={WHATSAPP_URL}
            target="_top"
            rel="noopener noreferrer"
            className="mt-6 inline-flex items-center gap-2 rounded-full bg-primary px-7 py-3.5 text-sm font-semibold text-primary-foreground shadow-lime hover:-translate-y-0.5 transition-transform"
          >
            <MessageCircle className="size-4" /> Falar com um especialista
          </a>
        </div>

        <Link to="/blog" className="mt-10 inline-flex items-center gap-2 text-sm font-semibold text-primary-dark hover:gap-3 transition-all">
          <ArrowLeft className="size-4" /> Voltar para o blog
        </Link>
      </main>

      <section className="bg-muted py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="font-display text-2xl font-bold mb-8">Leia também</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-7">
            {related.map((p) => (
              <article key={p.slug} className="rounded-2xl overflow-hidden border border-border bg-card shadow-card">
                <Link to="/blog/$slug" params={{ slug: p.slug }}>
                  <img src={p.cover} alt={p.title} className="h-40 w-full object-cover" loading="lazy" />
                </Link>
                <div className="p-6">
                  <h3 className="font-display text-base font-bold leading-snug">
                    <Link to="/blog/$slug" params={{ slug: p.slug }} className="hover:text-primary-dark transition-colors">
                      {p.title}
                    </Link>
                  </h3>
                  <p className="mt-2 text-sm text-muted-foreground line-clamp-3">{p.excerpt}</p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <SiteFooter />
    </div>
  );
}