import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { fetchAllPosts, formatDate, type BlogPost } from "@/lib/blog";
import { Navbar } from "@/components/Navbar";
import { SiteFooter } from "@/components/SiteFooter";
import { ArrowRight, Clock, Tag, BookOpen } from "lucide-react";

export const Route = createFileRoute("/blog/")({
  head: () => ({
    meta: [
      { title: "Blog — Seu Market Br" },
      {
        name: "description",
        content:
          "Artigos sobre minimercados autônomos em condomínios, gestão condominial, tecnologia e muito mais.",
      },
    ],
  }),
  component: BlogIndex,
});

function BlogIndex() {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllPosts().then((p) => {
      setPosts(p);
      setLoading(false);
    });
  }, []);

  const featured = posts[0];
  const rest = posts.slice(1);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="pt-20">
        {/* HEADER */}
        <section className="relative py-16 lg:py-20 bg-gradient-navy text-white overflow-hidden">
          <div className="absolute inset-0 grid-bg opacity-30" aria-hidden />
          <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">
              Conteúdo exclusivo
            </span>
            <h1 className="mt-3 font-display font-bold text-4xl md:text-6xl text-balance">
              Blog <span className="text-gradient-lime">Seu Market</span>
            </h1>
            <p className="mt-5 text-white/70 text-lg max-w-2xl mx-auto leading-relaxed">
              Dicas, novidades e conteúdo sobre minimercados autônomos,
              gestão condominial e tecnologia.
            </p>
          </div>
        </section>

        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-16 pb-24">
          {loading && (
            <div className="flex justify-center py-24">
              <div className="size-10 rounded-full border-4 border-primary border-t-transparent animate-spin" />
            </div>
          )}

          {!loading && posts.length === 0 && (
            <div className="text-center py-24">
              <BookOpen className="size-12 text-primary/40 mx-auto mb-4" />
              <p className="text-foreground/60 text-lg">
                Os artigos estão sendo preparados. Volte em breve!
              </p>
            </div>
          )}

          {!loading && featured && (
            <Link
              to="/blog/$slug"
              params={{ slug: featured.slug }}
              className="group block mb-12 rounded-3xl overflow-hidden border border-border bg-card hover:shadow-elevated hover:-translate-y-1 transition-all lg:grid lg:grid-cols-2"
            >
              {featured.coverImage && (
                <div className="aspect-video lg:aspect-auto overflow-hidden bg-navy">
                  <img
                    src={featured.coverImage}
                    alt={featured.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                </div>
              )}
              <div className="p-8 lg:p-12 flex flex-col justify-center">
                <span className="inline-flex items-center gap-2 text-xs font-bold tracking-widest text-primary uppercase">
                  <Tag className="size-3.5" /> {featured.category}
                </span>
                <h2 className="mt-3 font-display font-bold text-2xl md:text-3xl text-primary-dark leading-tight">
                  {featured.title}
                </h2>
                <p className="mt-3 text-foreground/70 leading-relaxed line-clamp-3">
                  {featured.excerpt}
                </p>
                <div className="mt-6 flex items-center gap-4 text-sm text-foreground/50">
                  <span className="flex items-center gap-1.5">
                    <Clock className="size-4" /> {featured.readingTime} min
                  </span>
                  <span>{formatDate(featured.date)}</span>
                </div>
                <span className="mt-6 inline-flex items-center gap-2 text-primary font-semibold group-hover:gap-3 transition-all">
                  Ler artigo <ArrowRight className="size-4" />
                </span>
              </div>
            </Link>
          )}

          {!loading && rest.length > 0 && (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {rest.map((post) => (
                <Link
                  key={post.slug}
                  to="/blog/$slug"
                  params={{ slug: post.slug }}
                  className="group flex flex-col rounded-2xl overflow-hidden border border-border bg-card hover:shadow-elevated hover:-translate-y-1 transition-all"
                >
                  {post.coverImage && (
                    <div className="aspect-video overflow-hidden bg-navy">
                      <img
                        src={post.coverImage}
                        alt={post.title}
                        loading="lazy"
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                      />
                    </div>
                  )}
                  <div className="p-6 flex flex-col flex-1">
                    <span className="text-xs font-bold tracking-widest text-primary uppercase">
                      {post.category}
                    </span>
                    <h3 className="mt-2 font-display font-bold text-lg text-primary-dark leading-snug flex-1">
                      {post.title}
                    </h3>
                    <p className="mt-2 text-sm text-foreground/60 line-clamp-2">
                      {post.excerpt}
                    </p>
                    <div className="mt-4 flex items-center justify-between text-xs text-foreground/40">
                      <span className="flex items-center gap-1">
                        <Clock className="size-3.5" /> {post.readingTime} min
                      </span>
                      <span>{formatDate(post.date)}</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
      <SiteFooter />
    </div>
  );
}
