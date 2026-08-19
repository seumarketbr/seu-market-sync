import { MessageCircle } from "lucide-react";
import { WHATSAPP_URL } from "@/lib/constants";

type Props = {
  children: React.ReactNode;
  variant?: "primary" | "white" | "ghost";
  size?: "md" | "lg";
  className?: string;
};

export function WhatsAppButton({ children, variant = "primary", size = "md", className = "" }: Props) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-full font-semibold transition-all hover:-translate-y-0.5 active:translate-y-0 shadow-elevated min-h-[44px]";
  const variants = {
    primary: "bg-whatsapp text-primary-foreground hover:brightness-110",
    white: "bg-background text-primary-dark hover:bg-cream",
    ghost: "bg-primary text-primary-foreground hover:bg-primary-dark",
  };
  const sizes = {
    md: "px-6 py-3 text-sm",
    lg: "px-8 py-4 text-base",
  };
  return (
    <a
      href={WHATSAPP_URL}
      target="_top"
      rel="noopener noreferrer"
      aria-label="Falar no WhatsApp"
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
    >
      <MessageCircle className="size-5" aria-hidden />
      {children}
    </a>
  );
}
