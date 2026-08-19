import { MessageCircle } from "lucide-react";
import { WHATSAPP_URL } from "@/lib/constants";

export function FloatingWhatsApp() {
  return (
    <a
      href={WHATSAPP_URL}
      target="_top"
      rel="noopener noreferrer"
      aria-label="Fale conosco no WhatsApp"
      className="fixed bottom-5 right-5 z-50 grid place-items-center size-14 rounded-full bg-whatsapp text-primary-foreground shadow-elevated animate-pulse-ring hover:scale-110 transition-transform"
    >
      <MessageCircle className="size-7" />
    </a>
  );
}
