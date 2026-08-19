import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { fetchPostBySlug, formatDate, type BlogPost } from "@/lib/blog";
import { Navbar } from "@/components/Navbar";
import { WhatsAppButton } from "@/components/WhatsAppButton";
import { ArrowLeft, Clock, Tag, Calendar } from "lucide-react";

export const Route = createFileRoute("/blog/$slug")({
  component: BlogPostPage,
});

function renderMarkdown(md: string): string {
  return md
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(
      /^## (.+)$/gm,
      '<h2 class="font-display font-bold text-2xl md:text-3xl text-primary-dark mt-10 mb-4">$1</h2>'
    )
    .replace(
      /\*\*(.+?)\*\*/g,
      '<strong class="font-bold text-primary-dark">$1</strong>'
    )
    .replace(
      /\\[([^\\]]+)\]\\(([^)]+)\\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-primary underline underline-offset-2 hover:text-primary/80 transition-colors">$1</a>'
    )
    .replace(
      /\n\n/g,
      '</p><p class="mt-5 text-foreground/80 leading-relaxed text-lg">'
    )
    .replace(/^/, '<p class="mt-5 text-foreground/80 leading-relaxed text-lg">')
    .replace(/$/, "</p>");
}

function BlogPostPage() {
  const { slug } = Route.useParams();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPostBySlug(slug).then((p) => {
      setPost(p);
      setLoading(false);
    });
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="pt-40 flex justify-center">
          <div className="size-10 rounded-full border-4 border-primary border-t-transparent animate-spin" />
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="pt-40 text-center px-4">
          <h1 className="font-display font-bold text-4xl text-primary-dark">
            Artigo não encontrado
          </h1>
          <p className="mt-4 text-foreground/60">
            Este artigo não existe ou foi removido.
          </p>
          <Link
            to="/blog"
            className="mt-8 inline-flex items-center gap-2 text-primary font-semibold hover:gap-3 transition-all"
          >
            <ArrowLeft className="size-4" /> Ver todos os artigos
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {post.coverImage && (
        <div className="relative h-[40vh] md:h-[50vh] overflow-hidden bg-navy pt-20">
          <img
            src={post.coverImage}
            alt={post.title}
            className="w-full h-full object-cover opacity-70"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-navy-deep/90 via-navy-deep/40 to-transparent" />
        </div>
      )}

      <div
        className={`mx-auto max-w-3xl px-4 sm:px-6 ${
          post.coverImage ? "-mt-20 relative z-10" : "pt-32"
        } pb-24`}
      >
        <Link
          to="/blog"
          className="inline-flex items-center gap-2 text-sm text-white/80 hover:text-primary transition-colors mb-6"
        >
          <ArrowLeft className="size-4" /> Blog
        </Link>

        <div className="bg-card rounded-3xl p-8 md:p-12 shadow-elevated border border-border">
          <div className="flex flex-wrap gap-3 mb-4">
            <span className="inline-flex items-center gap-1.5 text-xs font-bold tracking-widest text-primary uppercase">
              <Tag className="size-3.5" /> {post.category}
            </span>
            {post.tags.map((tag) => (
              <span
                key={tag}
                className="px-3 py-1 rounded-full bg-cream text-primary-dark text-xs font-semibold"
              >
                {tag}
              </span>
            ))}
          </div>

          <h1 className="font-display font-bold text-3xl md:text-4xl lg:text-5xl text-primary-dark leading-tight">
            {post.title}
          </h1>

          <div className="mt-5 flex flex-wrap gap-5 text-sm text-foreground/50">
            <span className="flex items-center gap-1.5">
              <Calendar className="size-4" /> {formatDate(post.date)}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="size-4" /> {post.readingTime} min de leitura
            </span>
            <span>Por {post.author}</span>
          </div>

          <article
            className="mt-10"
            dangerouslySetInnerHTML={{ __html: renderMarkdown(post.content) }}
          />

          <div className="mt-16 rounded-2xl bg-gradient-navy text-white p-8 text-center">
            <h3 className="font-display font-bold text-2xl">
              Quer levar o Seu Market para o seu condomínio?
            </h3>
            <p className="mt-3 text-white/70">
              Fale com a gente pelo WhatsApp e receba uma proposta sem
              compromisso.
            </p>
            <div className="mt-6">
              <WhatsAppButton size="lg">Solicitar proposta</WhatsAppButton>
            </div>
          </div>
        </div>

        <div className="mt-10 text-center">
          <Link
            to="/blog"
            className="inline-flex items-center gap-2 text-primary font-semibold hover:gap-3 transition-all"
          >
            <ArrowLeft className="size-4" /> Ver todos os artigos
          </Link>
        </div>
      </div>
    </div>
  );
}
