import { Phone, Mail, MapPin, Globe, Users, ShoppingBasket } from "lucide-react";
import {
  InstagramIcon, TikTokIcon, FacebookIcon, YouTubeIcon, PinterestIcon, LinkedInIcon,
} from "@/components/SocialIcons";
import logo from "@/assets/logo-seu-market.png";
import {
  WHATSAPP_DISPLAY, EMAIL, INSTAGRAM, LOCATION, INSTAGRAM_URL, TIKTOK_URL,
  PINTEREST_URL, WEBSITE_URL, FACEBOOK_URL, LINKEDIN_URL,
} from "@/lib/constants";

export function SiteFooter() {
  return (
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
            <li><a className="hover:text-primary transition-colors" href="/#sobre">Quem somos</a></li>
            <li><a className="hover:text-primary transition-colors" href="/#modelos">Modelos</a></li>
            <li><a className="hover:text-primary transition-colors" href="/#beneficios">Benefícios</a></li>
            <li><a className="hover:text-primary transition-colors" href="/#tecnologia">Tecnologia</a></li>
            <li><a className="hover:text-primary transition-colors" href="/blog">Blog</a></li>
            <li><a className="hover:text-primary transition-colors" href="/#contato">Contato</a></li>
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
  );
}