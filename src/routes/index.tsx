import { createFileRoute } from "@tanstack/react-router";
import {
  Clock, ShieldCheck, Sparkles, Home, Building2, Globe, Users, Briefcase,
  CheckCircle2, Star, Box, ShoppingBasket, Leaf, Heart, Gem,
  Maximize2, Settings, Lightbulb, Sofa, Puzzle, Smile,
  CreditCard, KeyRound, BarChart3, Smartphone, Boxes, Video,
  MapPin, Mail, Phone, ArrowRight, Zap, TrendingUp, Quote,
} from "lucide-react";
import {
  InstagramIcon, TikTokIcon, FacebookIcon, YouTubeIcon, PinterestIcon, LinkedInIcon,
} from "@/components/SocialIcons";
import { Navbar } from "@/components/Navbar";
import { WhatsAppButton } from "@/components/WhatsAppButton";
import { FloatingWhatsApp } from "@/components/FloatingWhatsApp";
import heroImg from "@/assets/hero-market.jpg";
import interiorImg from "@/assets/market-interior.jpg";
import compactImg from "@/assets/model-compact.jpg";
import wallImg from "@/assets/model-wall.jpg";
import smartImg from "@/assets/model-smart.jpg";
import primeImg from "@/assets/model-prime.jpg";
import logo from "@/assets/logo-seu-market.png";
import before1 from "@/assets/before-1.jpg";
import before2 from "@/assets/before-2.jpg";
import after1 from "@/assets/after-1.jpg";
import after2 from "@/assets/after-2.jpg";
import { WHATSAPP_DISPLAY, EMAIL, INSTAGRAM, LOCATION, INSTAGRAM_URL, TIKTOK_URL, PINTEREST_URL, WEBSITE_URL, FACEBOOK_URL, LINKEDIN_URL } from "@/lib/constants";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Seu Market Br — O seu mercado, no seu condomínio" },
      {
        name: "description",
        content:
          "Minimercados autônomos 24h para condomínios. Implantação sem custo, tecnologia, segurança e praticidade. Valorize seu condomínio em Belém-PA e região.",
      },
      { property: "og:title", content: "Seu Market Br — Minimercado autônomo para condomínios" },
      { property: "og:description", content: "Zero investimento. Zero preocupação. 100% vantagem para todos." },
      { property: "og:image", content: heroImg },
    ],
  }),
  component: Home_,
});

const models = [
  { n: "01", code: "COMPACT", size: "2 x 2 m", title: "Seu Market Compact", img: compactImg,
    tag: "Para espaços pequenos",
    desc: "Compacto por fora, completo por dentro. O essencial com design moderno.",
    attrs: ["Prático", "Moderno", "Compacto", "Completo"] },
  { n: "02", code: "WALL", size: "3 x 1 m", title: "Seu Market Wall", img: wallImg,
    tag: "Solução de parede",
    desc: "Perfeito para corredores, halls e áreas de passagem. O essencial com estilo.",
    attrs: ["Otimizado", "Funcional", "Inteligente", "Estilo"] },
  { n: "03", code: "SMART", size: "3 x 2 m", title: "Seu Market Smart", img: smartImg, featured: true,
    tag: "O mais escolhido",
    desc: "Mais variedade de produtos em um espaço inteligente, moderno e acolhedor.",
    attrs: ["Completo", "Confortável", "Versátil", "Moderno"] },
  { n: "04", code: "PRIME", size: "4 x 2 m", title: "Seu Market Prime", img: primeImg,
    tag: "Experiência premium",
    desc: "A experiência completa de um minimercado dentro do seu condomínio.",
    attrs: ["Premium", "Completo", "Conforto", "Sofisticado"] },
];

const pillars = [
  { icon: Clock, title: "Disponibilidade 24h", desc: "Acesso 24 horas por dia, todos os dias da semana." },
  { icon: Zap, title: "Autonomia total", desc: "Funcionamento 100% automatizado, sem funcionários no local." },
  { icon: ShieldCheck, title: "Segurança", desc: "Ambiente monitorado e controle de acesso para mais tranquilidade." },
  { icon: Heart, title: "Comunidade", desc: "Mais conveniência e qualidade de vida para todos os moradores." },
];

const audiences = [
  { icon: Users, t: "Para moradores", d: "Mais praticidade, segurança e economia de tempo no dia a dia." },
  { icon: Building2, t: "Para o condomínio", d: "Valorização do patrimônio e mais atratividade para o residencial." },
  { icon: Briefcase, t: "Para o síndico", d: "Gestão profissional, transparente e com zero dor de cabeça." },
  { icon: Sparkles, t: "Para todos", d: "Solução inteligente que transforma rotinas e fortalece a comunidade." },
];

const benefits = [
  { icon: Home, t: "Comodidade", d: "Tudo o que você precisa, a poucos passos de casa." },
  { icon: Clock, t: "Economia de tempo", d: "Menos deslocamentos e mais tempo para o que importa." },
  { icon: ShieldCheck, t: "Segurança", d: "Ambiente seguro, monitorado e com acesso controlado." },
  { icon: Users, t: "Convivência", d: "Mais interação entre moradores e valorização do espaço." },
  { icon: TrendingUp, t: "Valorização", d: "Um diferencial que aumenta o valor do seu imóvel." },
  { icon: Leaf, t: "Sustentabilidade", d: "Menos deslocamentos e incentivo ao consumo consciente." },
];

const tech = [
  { icon: Video, t: "Segurança 24h", d: "Câmeras com gravação contínua para total tranquilidade." },
  { icon: KeyRound, t: "Controle de acesso", d: "Acesso autorizado por moradores e liberado pela gestão." },
  { icon: CreditCard, t: "Pagamento digital", d: "Cartão de crédito, débito e PIX, de forma rápida e segura." },
  { icon: BarChart3, t: "Gestão inteligente", d: "Relatórios e indicadores em tempo real para decisões assertivas." },
  { icon: Smartphone, t: "App exclusivo", d: "Informações, promoções e comunicação na palma da mão." },
  { icon: Boxes, t: "Estoque otimizado", d: "Reposição inteligente para evitar faltas e desperdícios." },
];

const faqs = [
  { q: "Quem faz o abastecimento?", a: "Nossa equipe cuida de todo o abastecimento e gestão do minimercado." },
  { q: "Como é o pagamento?", a: "Aceitamos cartão de crédito, débito e PIX." },
  { q: "O condomínio precisa contratar funcionários?", a: "Não. Todo o funcionamento é 100% automatizado." },
  { q: "Funciona 24h mesmo?", a: "Sim! 24 horas por dia, 7 dias por semana." },
  { q: "E a segurança?", a: "O minimercado possui câmeras, monitoramento e controle de acesso." },
  { q: "O espaço precisa ser grande?", a: "Não. Temos modelos compactos que cabem em pequenos espaços." },
  { q: "Quais produtos são oferecidos?", a: "Bebidas, snacks, alimentos, higiene, limpeza e muito mais." },
  { q: "Há suporte se algo der errado?", a: "Sim. Temos suporte ágil para resolver qualquer situação." },
  { q: "Gera receita para o condomínio?", a: "Sim! Além da comodidade, pode gerar receita extra." },
  { q: "Os produtos têm qualidade?", a: "Trabalhamos com marcas confiáveis e produtos de alta qualidade." },
];

const requirements = [
  "Espaço disponível conforme modelo escolhido",
  "Ponto de energia elétrica",
  "Conexão com a internet (Wi-Fi ou cabeamento)",
  "Aprovação em assembleia e autorização da gestão",
];

function Home_() {
  return (
    <div id="top" className="min-h-screen bg-background overflow-x-hidden">
      <Navbar />
      <FloatingWhatsApp />

      {/* HERO */}
      <section className="relative min-h-screen pt-28 pb-20 lg:pt-32 bg-gradient-hero text-white overflow-hidden">
        <div className="absolute inset-0 grid-bg opacity-40" aria-hidden />
        <div className="absolute inset-0 bg-radial-lime" aria-hidden />
        <div className="absolute top-1/3 -left-20 size-96 rounded-full bg-primary/20 blur-3xl animate-float" aria-hidden />
        <div className="absolute bottom-10 -right-20 size-[28rem] rounded-full bg-primary/15 blur-3xl" aria-hidden />

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 grid lg:grid-cols-[1.05fr_1fr] gap-12 items-center">
          <div className="animate-fade-up">
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur ring-1 ring-white/20 text-xs font-semibold uppercase tracking-wider text-primary">
              <span className="size-1.5 rounded-full bg-primary animate-pulse" />
              Minimercado autônomo • 24h
            </span>
            <h1 className="mt-6 font-display font-bold text-4xl sm:text-5xl lg:text-6xl xl:text-7xl leading-[1.02] text-balance">
              O seu mercado, <br className="hidden sm:block" />
              no seu <span className="text-gradient-lime">condomínio</span>.
            </h1>
            <p className="mt-6 text-lg lg:text-xl text-white/75 max-w-xl leading-relaxed">
              Praticidade que transforma o dia a dia dos moradores. Tecnologia,
              segurança e produtos de qualidade — sem custo para o condomínio.
            </p>

            <div className="mt-9 flex flex-wrap gap-3">
              <WhatsAppButton size="lg">Solicitar proposta</WhatsAppButton>
              <a href="#modelos" className="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-full font-semibold text-white border border-white/25 hover:bg-white/10 transition-colors min-h-[44px]">
                Ver modelos <ArrowRight className="size-4" />
              </a>
            </div>

            <dl className="mt-12 grid grid-cols-3 gap-6 max-w-lg">
              {[
                { k: "24h", v: "Funcionamento todos os dias" },
                { k: "0", v: "Custo de implantação" },
                { k: "100%", v: "Gestão automatizada" },
              ].map((s) => (
                <div key={s.k}>
                  <dt className="font-display font-bold text-3xl lg:text-4xl text-gradient-lime">{s.k}</dt>
                  <dd className="mt-1 text-xs text-white/60 leading-snug">{s.v}</dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="relative animate-fade-up" style={{ animationDelay: "180ms" }}>
            <div className="absolute -inset-8 bg-gradient-lime rounded-[3rem] blur-3xl opacity-20" aria-hidden />
            <div className="relative rounded-3xl overflow-hidden ring-1 ring-white/10 shadow-elevated">
              <img
                src={heroImg}
                alt="Minimercado autônomo Seu Market Br instalado em condomínio"
                width={1240}
                height={1754}
                className="w-full h-auto object-cover"
              />
            </div>
            <div className="absolute -bottom-5 -left-5 hidden md:flex items-center gap-3 bg-white text-primary-dark rounded-2xl px-5 py-4 shadow-elevated">
              <span className="grid place-items-center size-10 rounded-xl bg-primary/15 text-primary-dark">
                <ShieldCheck className="size-5" />
              </span>
              <div>
                <p className="text-xs text-foreground/60">Implantação</p>
                <p className="font-display font-bold text-sm">100% por nossa conta</p>
              </div>
            </div>
          </div>
        </div>

        <div className="relative mt-20 lg:mt-24">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="rounded-full bg-gradient-lime px-6 py-4 shadow-lime flex flex-wrap items-center justify-center gap-x-10 gap-y-2">
              {["Conveniência", "Praticidade", "Confiança", "Tecnologia", "24 horas"].map((w, i) => (
                <span key={w} className="inline-flex items-center gap-3 font-display font-bold text-navy-deep uppercase tracking-wider text-sm sm:text-base">
                  {w}
                  {i < 4 && <span className="size-1.5 rounded-full bg-navy-deep/40" aria-hidden />}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* QUEM SOMOS */}
      <section id="sobre" className="py-24 lg:py-32">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="animate-fade-up">
              <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Quem somos</span>
              <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl text-primary-dark leading-tight text-balance">
                Minimercados autônomos para <span className="text-gradient-lime">condomínios modernos</span>.
              </h2>
              <p className="mt-5 text-foreground/70 text-lg leading-relaxed">
                O Seu Market Br é uma empresa especializada em minimercados autônomos
                dentro de condomínios, que leva praticidade, segurança e conveniência
                para o dia a dia dos moradores, com tecnologia, gestão eficiente e
                produtos de qualidade.
              </p>

              <div className="mt-10 grid sm:grid-cols-3 gap-4">
                {[
                  { t: "Missão", d: "Oferecer conveniência e praticidade com segurança e qualidade." },
                  { t: "Visão", d: "Ser referência em minimercados autônomos em condomínios." },
                  { t: "Valores", d: "Confiança, inovação, qualidade e respeito ao cliente." },
                ].map((m) => (
                  <div key={m.t} className="rounded-2xl border border-border p-5 bg-cream hover:border-primary/40 hover:shadow-card transition-all">
                    <p className="font-display font-bold text-primary-dark uppercase text-sm tracking-wider">{m.t}</p>
                    <p className="mt-2 text-sm text-foreground/70 leading-relaxed">{m.d}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative animate-fade-up" style={{ animationDelay: "120ms" }}>
              <div className="absolute -inset-6 bg-gradient-lime rounded-[2.5rem] blur-2xl opacity-25" aria-hidden />
              <img
                src={interiorImg}
                alt="Interior de minimercado Seu Market Br com prateleiras e refrigeradores"
                className="relative rounded-3xl shadow-elevated w-full h-auto object-cover aspect-[4/3]"
                loading="lazy"
              />
              <div className="absolute -bottom-6 -right-4 sm:right-6 bg-navy text-white rounded-2xl px-6 py-5 shadow-elevated max-w-[14rem]">
                <Quote className="size-5 text-primary mb-2" aria-hidden />
                <p className="text-sm leading-snug italic">
                  Modernizamos espaços. Transformamos rotinas.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* PILLARS / RAMO DE ATUAÇÃO */}
      <section className="py-20 lg:py-28 bg-gradient-navy text-white relative overflow-hidden">
        <div className="absolute inset-0 grid-bg opacity-30" aria-hidden />
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl animate-fade-up">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Nosso ramo de atuação</span>
            <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl text-balance">
              Modernizamos espaços. <br/>
              <span className="text-gradient-lime">Transformamos rotinas.</span>
            </h2>
            <p className="mt-5 text-white/70 text-lg leading-relaxed">
              Implantação e gestão de minimercados autônomos em condomínios residenciais e comerciais.
            </p>
          </div>

          <div className="mt-14 grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {pillars.map(({ icon: Icon, title, desc }, i) => (
              <div
                key={title}
                className="group p-7 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-primary/40 transition-all animate-fade-up"
                style={{ animationDelay: `${i * 90}ms` }}
              >
                <span className="grid place-items-center size-12 rounded-xl bg-gradient-lime text-navy-deep shadow-lime">
                  <Icon className="size-6" />
                </span>
                <h3 className="mt-5 font-display font-bold text-xl">{title}</h3>
                <p className="mt-2 text-sm text-white/70 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* MODELOS */}
      <section id="modelos" className="py-24 lg:py-32">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6 animate-fade-up">
            <div className="max-w-2xl">
              <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Nossos modelos</span>
              <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl text-primary-dark leading-tight text-balance">
                A solução certa para <span className="text-gradient-lime">cada espaço</span>.
              </h2>
            </div>
            <p className="text-foreground/70 max-w-md">
              Quatro formatos pensados para condomínios de todos os tamanhos — do compacto ao premium.
              Projetamos o modelo ideal para o espaço disponível.
            </p>
          </div>

          <div className="mt-14 grid sm:grid-cols-2 gap-6 lg:gap-8">
            {models.map((m, i) => (
              <article
                key={m.code}
                className={`group relative bg-card rounded-3xl overflow-hidden transition-all hover:-translate-y-1 animate-fade-up ${
                  m.featured
                    ? "ring-2 ring-primary shadow-elevated"
                    : "border border-border shadow-card hover:shadow-elevated"
                }`}
                style={{ animationDelay: `${i * 80}ms` }}
              >
                {m.featured && (
                  <div className="absolute top-4 right-4 z-10 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-gradient-lime text-navy-deep text-xs font-bold shadow-lime">
                    <Star className="size-3.5 fill-current" /> Mais escolhido
                  </div>
                )}
                <div className="relative aspect-[4/3] overflow-hidden bg-navy">
                  <img
                    src={m.img}
                    alt={`${m.title} — ${m.tag}`}
                    loading="lazy"
                    className="size-full object-contain group-hover:scale-105 transition-transform duration-700"
                  />
                  <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-navy-deep/70 via-transparent to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4 flex items-end justify-between">
                    <div>
                      <span className="text-xs font-bold text-primary tracking-widest">{m.code}</span>
                      <p className="text-white font-display font-bold text-lg leading-tight">{m.size}</p>
                    </div>
                    <span className="grid place-items-center size-10 rounded-full bg-gradient-lime text-navy-deep font-display font-bold text-sm shadow-lime">
                      {m.n}
                    </span>
                  </div>
                </div>
                <div className="p-7">
                  <h3 className="font-display font-bold text-2xl text-primary-dark">{m.title}</h3>
                  <p className="mt-1.5 text-primary-dark/60 font-semibold text-sm">{m.tag}</p>
                  <p className="mt-3 text-foreground/70 leading-relaxed">{m.desc}</p>
                  <ul className="mt-5 pt-5 border-t border-border flex flex-wrap gap-2">
                    {m.attrs.map((a) => (
                      <li key={a} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-cream text-primary-dark text-xs font-semibold">
                        <CheckCircle2 className="size-3.5 text-primary" /> {a}
                      </li>
                    ))}
                  </ul>
                </div>
              </article>
            ))}
          </div>

          <div className="mt-12 text-center">
            <p className="text-foreground/70 italic">
              Projetamos o modelo ideal para o espaço disponível no seu condomínio.
            </p>
          </div>
        </div>
      </section>

      {/* AUDIENCES / POR QUE LEVAR */}
      <section id="beneficios" className="py-24 lg:py-32 bg-cream">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center animate-fade-up">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Por que levar o Seu Market Br</span>
            <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl text-primary-dark leading-tight text-balance">
              Muito mais que um minimercado. <span className="text-gradient-lime">Uma parceria que faz a diferença.</span>
            </h2>
          </div>

          <div className="mt-14 grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {audiences.map(({ icon: Icon, t, d }, i) => (
              <div
                key={t}
                className="group bg-card rounded-2xl p-7 shadow-card hover:shadow-elevated hover:-translate-y-1 transition-all animate-fade-up"
                style={{ animationDelay: `${i * 80}ms` }}
              >
                <span className="grid place-items-center size-12 rounded-xl bg-primary/15 text-primary-dark group-hover:bg-gradient-lime group-hover:text-navy-deep transition-all">
                  <Icon className="size-6" />
                </span>
                <h3 className="mt-5 font-display font-bold text-lg text-primary-dark">{t}</h3>
                <p className="mt-2 text-sm text-foreground/70 leading-relaxed">{d}</p>
              </div>
            ))}
          </div>

          <div className="mt-16 grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {benefits.map(({ icon: Icon, t, d }, i) => (
              <div key={t} className="flex gap-4 p-5 rounded-2xl bg-white border border-border animate-fade-up" style={{ animationDelay: `${i * 60}ms` }}>
                <span className="shrink-0 grid place-items-center size-11 rounded-xl bg-cream text-primary-dark">
                  <Icon className="size-5" />
                </span>
                <div>
                  <p className="font-display font-bold text-primary-dark">{t}</p>
                  <p className="mt-1 text-sm text-foreground/70">{d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* TRANSFORMATION / ANTES E DEPOIS */}
      <section className="py-24 lg:py-32">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl animate-fade-up">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Transformamos espaços</span>
            <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl text-primary-dark leading-tight text-balance">
              Aproveitamos áreas ociosas e transformamos em <span className="text-gradient-lime">conveniência</span>.
            </h2>
          </div>

          <div className="mt-12 grid lg:grid-cols-2 gap-5">
            <div className="relative rounded-3xl bg-muted border border-border p-8 lg:p-10 animate-fade-up">
              <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-foreground/10 text-foreground/70 text-xs font-bold uppercase tracking-wider">Antes</span>
              <h3 className="mt-4 font-display font-bold text-2xl text-foreground/80">Espaço vazio</h3>
              <p className="mt-2 text-foreground/60 leading-relaxed">
                Sem utilização e sem retorno para o condomínio. Uma área subaproveitada
                que poderia entregar muito mais valor para os moradores.
              </p>
              <div className="mt-8 grid grid-cols-2 gap-3">
                <img src={before1} alt="Espaço vazio em condomínio" loading="lazy" width={800} height={600} className="aspect-[4/3] w-full rounded-xl object-cover grayscale opacity-80" />
                <img src={before2} alt="Corredor sem utilização em condomínio" loading="lazy" width={800} height={600} className="aspect-[4/3] w-full rounded-xl object-cover grayscale opacity-80" />
              </div>
            </div>

            <div className="relative rounded-3xl bg-gradient-navy text-white p-8 lg:p-10 overflow-hidden animate-fade-up" style={{ animationDelay: "120ms" }}>
              <div className="absolute inset-0 bg-radial-lime opacity-60" aria-hidden />
              <div className="relative">
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gradient-lime text-navy-deep text-xs font-bold uppercase tracking-wider">Depois</span>
                <div className="mt-4 bg-white/95 rounded-2xl px-4 py-3 inline-block shadow-card">
                  <img src={logo} alt="Seu Market Br" className="h-12 w-auto" />
                </div>
                <p className="mt-2 text-white/80 leading-relaxed">
                  Praticidade, conveniência e valorização para todos os moradores.
                  Um espaço moderno que entrega valor real ao condomínio.
                </p>
                <div className="mt-6 grid grid-cols-2 gap-3">
                  <img src={after1} alt="Minimercado Seu Market Br instalado em condomínio" loading="lazy" width={800} height={600} className="aspect-[4/3] w-full rounded-xl object-cover ring-1 ring-white/20" />
                  <img src={after2} alt="Espaço transformado com Seu Market Br" loading="lazy" width={800} height={600} className="aspect-[4/3] w-full rounded-xl object-cover ring-1 ring-white/20" />
                </div>
                <ul className="mt-8 space-y-3">
                  {[
                    "Mais comodidade no dia a dia",
                    "Facilidade para moradores e síndico",
                    "Ambiente seguro e organizado",
                    "Solução moderna e sem complicações",
                    "Retorno positivo para todos",
                  ].map((x) => (
                    <li key={x} className="flex items-start gap-3 text-white/90">
                      <CheckCircle2 className="size-5 text-primary shrink-0 mt-0.5" /> {x}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* PROCESSO */}
          <div className="mt-20 animate-fade-up">
            <div className="text-center max-w-2xl mx-auto">
              <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Como funciona</span>
              <h3 className="mt-3 font-display font-bold text-2xl md:text-4xl text-primary-dark text-balance">
                Do projeto à operação, do começo ao fim.
              </h3>
            </div>

            <ol className="mt-12 grid md:grid-cols-5 gap-4 relative">
              {[
                { t: "Analisamos", d: "O espaço disponível e o perfil do condomínio." },
                { t: "Projetamos", d: "A melhor solução para o local." },
                { t: "Implantamos", d: "Sem obras e com mínima interferência." },
                { t: "Operamos", d: "Abastecimento, gestão e suporte." },
                { t: "Você aproveita", d: "Mais comodidade, todos os dias." },
              ].map((s, i) => (
                <li key={s.t} className="relative bg-card rounded-2xl p-6 border border-border hover:border-primary/40 hover:shadow-card transition-all">
                  <span className="grid place-items-center size-11 rounded-xl bg-gradient-lime text-navy-deep font-display font-bold shadow-lime">
                    {i + 1}
                  </span>
                  <p className="mt-4 font-display font-bold text-primary-dark">{s.t}</p>
                  <p className="mt-1 text-sm text-foreground/70">{s.d}</p>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </section>

      {/* REQUIREMENTS / ZERO INVESTIMENTO */}
      <section className="py-20 lg:py-28 bg-gradient-navy text-white relative overflow-hidden">
        <div className="absolute inset-0 grid-bg opacity-30" aria-hidden />
        <div className="absolute -top-20 right-1/4 size-96 rounded-full bg-primary/15 blur-3xl" aria-hidden />
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 grid lg:grid-cols-2 gap-12 items-center">
          <div className="animate-fade-up">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">O que o condomínio precisa</span>
            <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl leading-tight text-balance">
              Apenas o essencial. <br/>
              <span className="text-gradient-lime">Cuidamos do resto.</span>
            </h2>
            <ul className="mt-8 space-y-3">
              {requirements.map((r) => (
                <li key={r} className="flex items-start gap-3 text-white/90">
                  <CheckCircle2 className="size-5 text-primary shrink-0 mt-0.5" /> {r}
                </li>
              ))}
            </ul>
          </div>

          <div className="relative animate-fade-up" style={{ animationDelay: "120ms" }}>
            <div className="rounded-3xl bg-gradient-lime p-10 lg:p-12 text-navy-deep shadow-lime relative overflow-hidden">
              <Sparkles className="absolute top-6 right-6 size-8 opacity-30" aria-hidden />
              <p className="text-xs font-bold tracking-[0.25em] uppercase">Implantação</p>
              <p className="mt-3 font-display font-bold text-4xl md:text-5xl leading-none">
                Sem custo.<br/>Sem dor de cabeça.
              </p>
              <p className="mt-5 text-navy-deep/80 text-lg leading-relaxed">
                A implantação é 100% por nossa conta.
                O condomínio não tem investimento inicial.
              </p>
              <div className="mt-8 grid grid-cols-3 gap-3 text-center">
                {[
                  { k: "Zero", v: "Investimento" },
                  { k: "Zero", v: "Preocupação" },
                  { k: "100%", v: "Vantagem" },
                ].map((s) => (
                  <div key={s.v} className="rounded-2xl bg-navy-deep text-white p-4">
                    <p className="font-display font-bold text-2xl text-primary">{s.k}</p>
                    <p className="text-xs text-white/70 mt-0.5">{s.v}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* TECHNOLOGY */}
      <section id="tecnologia" className="py-24 lg:py-32">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl animate-fade-up">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Tecnologia & Gestão</span>
            <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl text-primary-dark leading-tight text-balance">
              Tecnologia que <span className="text-gradient-lime">protege, organiza e simplifica</span>.
            </h2>
            <p className="mt-5 text-foreground/70 text-lg leading-relaxed">
              No Seu Market Br, a tecnologia trabalha a favor da segurança, da eficiência e
              da melhor experiência para os moradores e para a gestão.
            </p>
          </div>

          <div className="mt-14 grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {tech.map(({ icon: Icon, t, d }, i) => (
              <div
                key={t}
                className="group rounded-3xl p-7 bg-card border border-border hover:border-primary/40 hover:shadow-elevated hover:-translate-y-1 transition-all animate-fade-up"
                style={{ animationDelay: `${i * 70}ms` }}
              >
                <span className="grid place-items-center size-14 rounded-2xl bg-gradient-lime text-navy-deep shadow-lime">
                  <Icon className="size-7" />
                </span>
                <h3 className="mt-5 font-display font-bold text-xl text-primary-dark">{t}</h3>
                <p className="mt-2 text-foreground/70 leading-relaxed">{d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="py-24 lg:py-32 bg-cream">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl animate-fade-up">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Dúvidas frequentes</span>
            <h2 className="mt-3 font-display font-bold text-3xl md:text-5xl text-primary-dark leading-tight text-balance">
              Respostas claras para as <span className="text-gradient-lime">principais dúvidas</span>.
            </h2>
          </div>

          <div className="mt-12 grid md:grid-cols-2 gap-4">
            {faqs.map((f, i) => (
              <details
                key={f.q}
                className="group rounded-2xl bg-white border border-border p-5 sm:p-6 hover:border-primary/40 transition-colors animate-fade-up"
                style={{ animationDelay: `${i * 40}ms` }}
              >
                <summary className="flex items-start justify-between gap-4 cursor-pointer list-none">
                  <span className="font-display font-bold text-primary-dark text-base sm:text-lg">{f.q}</span>
                  <span className="shrink-0 grid place-items-center size-8 rounded-full bg-primary/15 text-primary-dark group-open:bg-gradient-lime group-open:rotate-45 transition-all">
                    <span className="text-lg leading-none">+</span>
                  </span>
                </summary>
                <p className="mt-3 text-foreground/70 leading-relaxed text-sm sm:text-base">{f.a}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* CTA / CONTATO */}
      <section id="contato" className="relative py-24 lg:py-32 bg-gradient-navy text-white overflow-hidden">
        <div className="absolute inset-0 grid-bg opacity-30" aria-hidden />
        <div className="absolute -bottom-32 -left-20 size-[28rem] rounded-full bg-primary/20 blur-3xl" aria-hidden />
        <div className="absolute -top-20 -right-20 size-96 rounded-full bg-primary/15 blur-3xl" aria-hidden />

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 grid lg:grid-cols-[1.1fr_1fr] gap-12 items-center">
          <div className="animate-fade-up">
            <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase">Fale com a gente</span>
            <h2 className="mt-3 font-display font-bold text-4xl md:text-6xl leading-[1.05] text-balance">
              Pronto para levar o <span className="text-gradient-lime">Seu Market</span> para o seu condomínio?
            </h2>
            <p className="mt-5 text-white/75 text-lg max-w-xl">
              Atendimento rápido pelo WhatsApp. Tire suas dúvidas e receba uma proposta
              sob medida para o seu condomínio.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <WhatsAppButton size="lg">Falar no WhatsApp</WhatsAppButton>
              <a href={`mailto:${EMAIL}`} className="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-full font-semibold text-white border border-white/25 hover:bg-white/10 transition-colors min-h-[44px]">
                <Mail className="size-4" /> Enviar e-mail
              </a>
            </div>
          </div>

          <div className="relative animate-fade-up" style={{ animationDelay: "150ms" }}>
            <div className="rounded-3xl bg-white/5 backdrop-blur border border-white/10 p-8 lg:p-10">
              <p className="font-display font-bold text-2xl">Informações de contato</p>
              <p className="mt-1 text-white/70 text-sm">Estamos prontos para ajudar.</p>

              <ul className="mt-8 space-y-5">
                <li className="flex items-start gap-4">
                  <span className="shrink-0 grid place-items-center size-11 rounded-xl bg-gradient-lime text-navy-deep shadow-lime">
                    <Phone className="size-5" />
                  </span>
                  <div>
                    <p className="text-xs uppercase tracking-wider text-white/60">Telefone</p>
                    <p className="font-display font-bold text-lg">{WHATSAPP_DISPLAY}</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <span className="shrink-0 grid place-items-center size-11 rounded-xl bg-gradient-lime text-navy-deep shadow-lime">
                    <Mail className="size-5" />
                  </span>
                  <div>
                    <p className="text-xs uppercase tracking-wider text-white/60">E-mail</p>
                    <a href={`mailto:${EMAIL}`} className="font-display font-bold text-lg hover:text-primary transition-colors">{EMAIL}</a>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <span className="shrink-0 grid place-items-center size-11 rounded-xl bg-gradient-lime text-navy-deep shadow-lime">
                    <InstagramIcon className="size-5" />
                  </span>
                  <div>
                    <p className="text-xs uppercase tracking-wider text-white/60">Instagram</p>
                    <p className="font-display font-bold text-lg">{INSTAGRAM}</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <span className="shrink-0 grid place-items-center size-11 rounded-xl bg-gradient-lime text-navy-deep shadow-lime">
                    <MapPin className="size-5" />
                  </span>
                  <div>
                    <p className="text-xs uppercase tracking-wider text-white/60">Localização</p>
                    <p className="font-display font-bold text-lg">{LOCATION}</p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-navy-deep text-white/70 pt-16 pb-10">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 grid md:grid-cols-4 gap-10 items-start">
          <div>
            <div className="bg-white/95 rounded-xl px-4 py-2 inline-block">
              <img src={logo} alt="Seu Market Br" className="h-10 w-auto" />
            </div>
            <p className="mt-5 text-sm leading-relaxed max-w-xs">
              O seu mercado, no seu condomínio. Mais conveniência, mais qualidade de vida, mais para todos.
            </p>
          </div>
          <div>
            <p className="text-white font-display font-bold mb-4">Mapa do Site</p>
            <ul className="space-y-2 text-sm">
              <li><a className="hover:text-primary transition-colors" href="#sobre">Quem somos</a></li>
              <li><a className="hover:text-primary transition-colors" href="#modelos">Modelos</a></li>
              <li><a className="hover:text-primary transition-colors" href="#beneficios">Benefícios</a></li>
              <li><a className="hover:text-primary transition-colors" href="#tecnologia">Tecnologia</a></li>
              <li><a className="hover:text-primary transition-colors" href="#faq">FAQ</a></li>
              <li><a className="hover:text-primary transition-colors" href="#contato">Contato</a></li>
            </ul>
          </div>
          <div>
            <p className="text-white font-display font-bold mb-4">Contato</p>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center gap-2"><Phone className="size-4 text-primary" /> {WHATSAPP_DISPLAY}</li>
              <li className="flex items-center gap-2"><Mail className="size-4 text-primary" /> {EMAIL}</li>
              <li className="flex items-center gap-2"><InstagramIcon className="size-4 text-primary" /> {INSTAGRAM}</li>
              <li className="flex items-center gap-2"><MapPin className="size-4 text-primary" /> {LOCATION}</li>
            </ul>
          </div>
                <div>
          <p className="text-white font-display font-bold mb-4">Redes Sociais</p>
          <ul className="space-y-2 text-sm">
            <li className="flex items-center gap-2"><Globe className="size-4 text-primary" /> <a href={WEBSITE_URL} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">seumarketbr.com.br</a></li>
            <li className="flex items-center gap-2"><InstagramIcon className="size-4 text-primary" /> <a href={INSTAGRAM_URL} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">@seumarket.br</a></li>
            <li className="flex items-center gap-2"><TikTokIcon className="size-4 text-primary" /> <a href={TIKTOK_URL} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">@seumarketbr</a></li>
            <li className="flex items-center gap-2"><FacebookIcon className="size-4 text-primary" /> <a href={FACEBOOK_URL} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">seumarketbr</a></li>
            <li className="flex items-center gap-2"><YouTubeIcon className="size-4 text-primary" /> <a href="https://www.youtube.com/@seumarketbr" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">seumarketbr</a></li>
            <li className="flex items-center gap-2"><LinkedInIcon className="size-4 text-primary" /> <a href={LINKEDIN_URL} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">seumarketbr</a></li>
            <li className="flex items-center gap-2"><PinterestIcon className="size-4 text-primary" /> <a href={PINTEREST_URL} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">seumarketbr</a></li>
                          <li className="flex items-center gap-2"><Users className="size-4 text-primary" /> <a href={LINKEDIN_URL} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">seumarketbr</a></li>
          </ul>
        </div>
                  </div>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-12 pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-white/50">
          <p>© {new Date().getFullYear()} Seu Market Br. Todos os direitos reservados.</p>
          <p className="inline-flex items-center gap-2">
            <ShoppingBasket className="size-3.5 text-primary" /> Mais conveniência. Mais qualidade de vida.
          </p>
        </div>
      </footer>
    </div>
  );
}
