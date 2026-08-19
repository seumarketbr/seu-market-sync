import interiorImg from "@/assets/market-interior.jpg";
import smartImg from "@/assets/model-smart.jpg";
import primeImg from "@/assets/model-prime.jpg";
import compactImg from "@/assets/model-compact.jpg";

export interface BlogPost {
  slug: string;
  title: string;
  excerpt: string;
  category: string;
  date: string; // ISO
  readingTime: number;
  coverImage: string;
  author: string;
  content: string; // Markdown string
  tags: string[];
  featured?: boolean;
}

// Posts estáticos hardcoded
const STATIC_POSTS: BlogPost[] = [
  {
    slug: "minimercado-autonomo-em-condominio-como-funciona",
    title: "Minimercado autônomo em condomínio: como funciona na prática",
    excerpt:
      "Entenda passo a passo como um minimercado autônomo 24h opera dentro do condomínio, da implantação ao dia a dia dos moradores.",
    category: "Como funciona",
    date: "2026-08-12",
    readingTime: 6,
    coverImage: interiorImg,
    author: "Seu Market Br",
    tags: ["mercado autônomo", "self-checkout", "conveniência"],
    content: `O minimercado autônomo é um espaço de conveniência instalado dentro do próprio condomínio, aberto 24 horas por dia, sem funcionários e com pagamento self-checkout. O morador entra, escolhe os produtos, passa no totem e paga por aproximação, Pix ou cartão.

## Implantação sem custo para o condomínio

A estrutura, os equipamentos, o estoque e a manutenção ficam por conta da operação. O condomínio cede um espaço ocioso — hall, salão, área de passagem — e recebe uma solução pronta, com identidade visual moderna e iluminação própria.

## O dia a dia da loja

A reposição é periódica com curadoria conforme o perfil do prédio. O monitoramento é feito por câmeras e controle de acesso por aplicativo. Os preços são de mercado, sem taxa de conveniência abusiva. O suporte é rápido pelo WhatsApp para moradores e síndico.

## Por que os moradores adotam tão rápido

A conveniência resolve o esquecimento do dia a dia: café, leite, higiene, bebidas e snacks a poucos metros do apartamento, sem pegar o carro. O resultado é uma valorização real da experiência de morar no condomínio.`,
  },
  {
    slug: "quanto-espaco-preciso-para-instalar-um-minimercado",
    title: "Quanto espaço é preciso para instalar um minimercado no seu prédio",
    excerpt:
      "De 2x2 m a 4x2 m: comparamos os modelos Compact, Wall, Smart e Prime e mostramos qual cabe melhor em cada tipo de condomínio.",
    category: "Modelos",
    date: "2026-07-29",
    readingTime: 5,
    coverImage: smartImg,
    author: "Seu Market Br",
    tags: ["modelos", "espaço", "compact", "smart", "prime"],
    content: `Não é preciso reformar nem sacrificar áreas nobres. A maioria dos condomínios instala o minimercado em espaços que hoje estão ociosos, com metragens a partir de 4 m².

## Compact — 2 x 2 m

Ideal para prédios menores ou halls compactos. Traz o essencial: bebidas, snacks, higiene e itens de emergência.

## Wall — 3 x 1 m

Solução de parede para corredores e áreas de passagem. Ocupa pouca profundidade e mantém a circulação livre.

## Smart — 3 x 2 m

O modelo mais escolhido. Equilibra variedade de produtos e conforto de circulação, com espaço para refrigeração e mercearia.

## Prime — 4 x 2 m

A experiência completa, com maior mix de produtos, mais refrigeração e ambiente pensado como uma pequena loja de conveniência premium.`,
  },
  {
    slug: "seguranca-e-tecnologia-do-mercado-autonomo",
    title: "Segurança e tecnologia: o que protege um mercado autônomo 24h",
    excerpt:
      "Controle de acesso, câmeras, antifurto e pagamento digital: as camadas de tecnologia que tornam a loja sem funcionários confiável.",
    category: "Tecnologia",
    date: "2026-07-15",
    readingTime: 4,
    coverImage: primeImg,
    author: "Seu Market Br",
    tags: ["segurança", "câmeras", "controle de acesso"],
    content: `A confiança é o principal ativo de uma loja autônoma. Por isso o sistema combina identificação do usuário, monitoramento contínuo e pagamento rastreável.

## Camadas de proteção

O acesso é liberado por aplicativo, vinculado ao morador. Câmeras com gravação em nuvem garantem visão total do ambiente. O totem de autoatendimento aceita Pix, crédito, débito e aproximação. Alertas automáticos de estoque e de ocorrências completam a proteção.

## Índices de perda menores do que se imagina

Em ambientes fechados como condomínios, a comunidade é conhecida e identificada. Isso reduz drasticamente perdas e transforma o espaço em um ponto de convivência.`,
  },
  {
    slug: "como-o-sindico-valoriza-o-condominio-com-conveniencia",
    title: "Como o síndico valoriza o condomínio oferecendo conveniência",
    excerpt:
      "Serviços internos pesam na decisão de compra e locação. Veja o impacto de um minimercado 24h na percepção de valor do seu empreendimento.",
    category: "Gestão condominial",
    date: "2026-06-30",
    readingTime: 5,
    coverImage: compactImg,
    author: "Seu Market Br",
    tags: ["síndico", "gestão condominial", "valorização"],
    content: `Academia, coworking, pet place e, cada vez mais, minimercado autônomo: a lista de comodidades que um morador espera encontrar cresceu. Condomínios que oferecem conveniência interna se destacam no anúncio e na visita.

## Benefícios para a gestão

Não há investimento ou custo operacional para o condomínio. Áreas ociosas são aproveitadas com espaço requalificado. O minimercado se torna um diferencial competitivo em vendas e locações, além de reduzir a circulação de entregadores externos.

## Aprovação em assembleia

A proposta costuma ser bem recebida porque não há rateio nem aumento de taxa. O material de apresentação, com plantas e simulação do espaço, pode ser enviado ao conselho antes da assembleia.`,
  },
];

// Busca posts dinâmicos gerados pela GitHub Action
async function fetchDynamicPosts(): Promise<BlogPost[]> {
  try {
    const manifestRes = await fetch("/blog-posts/manifest.json");
    if (!manifestRes.ok) return [];
    const slugs: string[] = await manifestRes.json();

    const posts = await Promise.all(
      slugs.map(async (slug) => {
        try {
          const res = await fetch(`/blog-posts/${slug}.json`);
          if (!res.ok) return null;
          const post = await res.json();
          return post as BlogPost;
        } catch {
          return null;
        }
      })
    );

    return posts.filter((p): p is BlogPost => p !== null);
  } catch {
    return [];
  }
}

// Busca todos os posts (dinâmicos + estáticos), ordenados por data
export async function fetchAllPosts(): Promise<BlogPost[]> {
  const dynamic = await fetchDynamicPosts();
  const all = [...dynamic, ...STATIC_POSTS];
  return all.sort((a, b) => (a.date < b.date ? 1 : -1));
}

// Busca post por slug (dinâmico primeiro, depois estático)
export async function fetchPostBySlug(slug: string): Promise<BlogPost | null> {
  // Tenta buscar direto o JSON dinâmico
  try {
    const res = await fetch(`/blog-posts/${slug}.json`);
    if (res.ok) {
      const post = await res.json();
      return post as BlogPost;
    }
  } catch {
    // ignora e cai no estático
  }

  // Fallback: posts estáticos
  return STATIC_POSTS.find((p) => p.slug === slug) ?? null;
}

export const formatDate = (iso: string) =>
  new Date(`${iso}T12:00:00Z`).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
