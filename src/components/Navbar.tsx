import { useEffect, useState } from "react";
import { Menu, X, MessageCircle } from "lucide-react";
import logo from "@/assets/logo-seu-market.png";
import { WHATSAPP_URL } from "@/lib/constants";

const links = [
  { href: "/#sobre", label: "Quem somos" },
  { href: "/#modelos", label: "Modelos" },
  { href: "/#beneficios", label: "Benefícios" },
  { href: "/#tecnologia", label: "Tecnologia" },
  { href: "/blog", label: "Blog" },
  { href: "/#faq", label: "FAQ" },
  { href: "/#contato", label: "Contato" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const textColor = scrolled ? "text-foreground/80 hover:text-primary-dark" : "text-white/80 hover:text-primary";

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        scrolled ? "bg-background/90 backdrop-blur-md shadow-card border-b border-border" : "bg-transparent"
      }`}
    >
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-18 py-3 flex items-center justify-between">
        <a href="/" className="flex items-center" aria-label="Seu Market Br - Início">
          <div className={`rounded-xl transition-all ${scrolled ? "" : "bg-white/95 px-3 py-1.5 shadow-card"}`}>
            <img src={logo} alt="Seu Market Br" className="h-10 md:h-11 w-auto" />
          </div>
        </a>

        <ul className="hidden lg:flex items-center gap-7">
          {links.map((l) => (
            <li key={l.href}>
              <a href={l.href} className={`text-sm font-medium transition-colors ${textColor}`}>
                {l.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="hidden lg:flex items-center gap-3">
          <a
            href={WHATSAPP_URL}
            target="_top"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-primary text-primary-foreground text-sm font-semibold shadow-lime hover:-translate-y-0.5 transition-transform"
          >
            <MessageCircle className="size-4" /> Fale conosco
          </a>
        </div>

        <button
          aria-label="Abrir menu"
          className={`lg:hidden p-2 rounded-lg ${scrolled ? "text-foreground hover:bg-muted" : "text-white hover:bg-white/10"}`}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X className="size-6" /> : <Menu className="size-6" />}
        </button>
      </nav>

      {open && (
        <div className="lg:hidden bg-background border-t border-border">
          <ul className="px-4 py-4 space-y-1">
            {links.map((l) => (
              <li key={l.href}>
                <a
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="block py-3 px-2 text-base font-medium hover:text-primary-dark"
                >
                  {l.label}
                </a>
              </li>
            ))}
            <li className="pt-2">
              <a
                href={WHATSAPP_URL}
                target="_top"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 px-5 py-3 rounded-full bg-primary text-primary-foreground font-semibold"
              >
                <MessageCircle className="size-4" /> Fale conosco
              </a>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}
