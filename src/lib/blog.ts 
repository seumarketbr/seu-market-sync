export interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  category: string;
  author: string;
  date: string;
  readingTime: number;
  featured: boolean;
  coverImage: string;
  tags: string[];
}

export async function fetchPostSlugs(): Promise<string[]> {
  try {
    const res = await fetch("/blog-posts/manifest.json");
    if (!res.ok) return [];
    return await res.json();
  } catch {
    return [];
  }
}

export async function fetchAllPosts(): Promise<BlogPost[]> {
  const slugs = await fetchPostSlugs();
  if (!slugs.length) return [];
  const posts = await Promise.all(
    slugs.map(async (slug) => {
      try {
        const res = await fetch(`/blog-posts/${slug}.json`);
        if (!res.ok) return null;
        return (await res.json()) as BlogPost;
      } catch {
        return null;
      }
    })
  );
  return posts
    .filter((p): p is BlogPost => p !== null)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

export async function fetchPostBySlug(slug: string): Promise<BlogPost | null> {
  try {
    const res = await fetch(`/blog-posts/${slug}.json`);
    if (!res.ok) return null;
    return (await res.json()) as BlogPost;
  } catch {
    return null;
  }
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
}
