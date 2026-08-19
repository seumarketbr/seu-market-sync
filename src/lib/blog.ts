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
  readingMinutes: number;
  cover: string;
  author: string;
  /** Simple content blocks so novos artigos são fáceis de publicar. */
  content: Array<{ h?: string; p?: string; list?: string[] }>;
}

export const BLOG_POSTS: BlogPost[] = [
  {
    slug: "minimercado-autonomo-em-condominio-como-funciona",
    title: "Minimercado autônomo em condomínio: como funciona na prática",
    excerpt:
      "Entenda passo a passo como um minimercado autônomo 24h opera dentro do condomínio, da implantação ao dia a dia dos moradores.",
    category: "Como funciona",
    date: "2026-08-12",
    readingMinutes: 6,
    cover: interiorImg,
    author: "Seu Market Br",
    content: [
      {
        p: "O minimercado autônomo é um espaço de conveniência instalado dentro do próprio condomínio, aberto 24 horas por dia, sem funcionários e com pagamento self-checkout. O morador entra, escolhe os produtos, passa no totem e paga por aproximação, Pix ou cartão.",
      },
      {
        h: "Implantação sem custo para o condomínio",
        p: "A estrutura, os equipamentos, o estoque e a manutenção ficam por conta da operação. O condomínio cede um espaço ocioso — hall, salão, área de passagem — e recebe uma solução pronta, com identidade visual moderna e iluminação própria.",
      },
      {
        h: "O dia a dia da loja",
        list: [
          "Reposição periódica de produtos com curadoria conforme o perfil do prédio",
          "Monitoramento por câmeras e controle de acesso por aplicativo",
          "Preços de mercado, sem taxa de conveniência abusiva",
          "Suporte rápido pelo WhatsApp para moradores e síndico",
        ],
      },
      {
        h: "Por que os moradores adotam tão rápido",
        p: "A conveniência resolve o esquecimento do dia a dia: café, leite, higiene, bebidas e snacks a poucos metros do apartamento, sem pegar o carro. O resultado é uma valorização real da experiência de morar no condomínio.",
      },
    ],
  },
  {
    slug: "quanto-espaco-preciso-para-instalar-um-minimercado",
    title: "Quanto espaço é preciso para instalar um minimercado no seu prédio",
    excerpt:
      "De 2x2 m a 4x2 m: comparamos os modelos Compact, Wall, Smart e Prime e mostramos qual cabe melhor em cada tipo de condomínio.",
    category: "Modelos",
    date: "2026-07-29",
    readingMinutes: 5,
    cover: smartImg,
    author: "Seu Market Br",
    content: [
      {
        p: "Não é preciso reformar nem sacrificar áreas nobres. A maioria dos condomínios instala o minimercado em espaços que hoje estão ociosos, com metragens a partir de 4 m².",
      },
      {
        h: "Compact — 2 x 2 m",
        p: "Ideal para prédios menores ou halls compactos. Traz o essencial: bebidas, snacks, higiene e itens de emergência.",
      },
      {
        h: "Wall — 3 x 1 m",
        p: "Solução de parede para corredores e áreas de passagem. Ocupa pouca profundidade e mantém a circulação livre.",
      },
      {
        h: "Smart — 3 x 2 m",
        p: "O modelo mais escolhido. Equilibra variedade de produtos e conforto de circulação, com espaço para refrigeração e mercearia.",
      },
      {
        h: "Prime — 4 x 2 m",
        p: "A experiência completa, com maior mix de produtos, mais refrigeração e ambiente pensado como uma pequena loja de conveniência premium.",
      },
    ],
  },
  {
    slug: "seguranca-e-tecnologia-do-mercado-autonomo",
    title: "Segurança e tecnologia: o que protege um mercado autônomo 24h",
    excerpt:
      "Controle de acesso, câmeras, antifurto e pagamento digital: as camadas de tecnologia que tornam a loja sem funcionários confiável.",
    category: "Tecnologia",
    date: "2026-07-15",
    readingMinutes: 4,
    cover: primeImg,
    author: "Seu Market Br",
    content: [
      {
        p: "A confiança é o principal ativo de uma loja autônoma. Por isso o sistema combina identificação do usuário, monitoramento contínuo e pagamento rastreável.",
      },
      {
        h: "Camadas de proteção",
        list: [
          "Acesso liberado por aplicativo, vinculado ao morador",
          "Câmeras com gravação em nuvem e visão total do ambiente",
          "Totem de autoatendimento com Pix, crédito, débito e aproximação",
          "Alertas automáticos de estoque e de ocorrências",
        ],
      },
      {
        h: "Índices de perda menores do que se imagina",
        p: "Em ambientes fechados como condomínios, a comunidade é conhecida e identificada. Isso reduz drasticamente perdas e transforma o espaço em um ponto de convivência.",
      },
    ],
  },
  {
    slug: "como-o-sindico-valoriza-o-condominio-com-conveniencia",
    title: "Como o síndico valoriza o condomínio oferecendo conveniência",
    excerpt:
      "Serviços internos pesam na decisão de compra e locação. Veja o impacto de um minimercado 24h na percepção de valor do seu empreendimento.",
    category: "Gestão condominial",
    date: "2026-06-30",
    readingMinutes: 5,
    cover: compactImg,
    author: "Seu Market Br",
    content: [
      {
        p: "Academia, coworking, pet place e, cada vez mais, minimercado autônomo: a lista de comodidades que um morador espera encontrar cresceu. Condomínios que oferecem conveniência interna se destacam no anúncio e na visita.",
      },
      {
        h: "Benefícios para a gestão",
        list: [
          "Nenhum investimento ou custo operacional para o condomínio",
          "Aproveitamento de áreas ociosas com espaço requalificado",
          "Diferencial competitivo em vendas e locações",
          "Menos circulação de entregadores externos",
        ],
      },
      {
        h: "Aprovação em assembleia",
        p: "A proposta costuma ser bem recebida porque não há rateio nem aumento de taxa. O material de apresentação, com plantas e simulação do espaço, pode ser enviado ao conselho antes da assembleia.",
      },
    ],
  },
];

export const getPost = (slug: string) => BLOG_POSTS.find((p) => p.slug === slug);

export const sortedPosts = () =>
  [...BLOG_POSTS].sort((a, b) => (a.date < b.date ? 1 : -1));

export const formatDate = (iso: string) =>
  new Date(`${iso}T12:00:00Z`).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });