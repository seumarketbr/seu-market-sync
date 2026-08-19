import os, json, urllib.request, urllib.error, urllib.parse, sys, random, re, unicodedata
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
today = now.strftime("%Y-%m-%d")
hour = now.hour
api_key = os.environ["OPENROUTER_API_KEY"]

SEU_MARKET_FACTS = """
Empresa brasileira: minimercados autônomos 24h em condomínios residenciais e comerciais.
Operação 100% self-checkout: totem com Pix, crédito, débito e aproximação.
Implantação gratuita para o condomínio: estrutura, equipamentos e estoque são da operação.
O condomínio cede o espaço ocioso e recebe o serviço pronto, sem custo nem rateio.
Modelos: Compact (2x2m), Wall (3x1m), Smart (3x2m, mais vendido), Prime (4x2m).
Tecnologia: acesso por app, câmeras em nuvem, alertas automáticos de estoque.
Reposição periódica com curadoria conforme o perfil do condomínio.
Suporte via WhatsApp para moradores e síndico.
Site oficial e único link permitido: https://seumarketbr.com.br
NÃO FAZER:
Não confirmar números de unidades instaladas desconhecidos.
Não dizer que produtos são mais baratos que supermercados.
Não dizer que o serviço é totalmente gratuito (cobra dos consumidores nos produtos).
NÃO usar traços ou hífens para separar ideias no meio de frases. Use vírgulas.
NÃO inserir links para sites externos. O único link permitido é https://seumarketbr.com.br
"""

IMAGE_PROMPTS = {
    "mercado_autonomo": "ultra realistic photo, modern self-service mini market inside a luxury apartment building lobby, bright LED lighting, clean shelves with food and drinks, self-checkout kiosk touchscreen, marble floor, no people, no text, professional interior photography, 4k",
    "sindico": "ultra realistic photo, modern condominium meeting room with glass walls overlooking a residential building, professional manager at desk reviewing documents, clean corporate interior, no text, 4k architectural photography",
    "tecnologia": "ultra realistic photo, futuristic digital access control panel on wall of modern building corridor, glowing blue interface, security camera visible, sleek dark surfaces, no text, 4k tech photography",
    "seguranca": "ultra realistic photo, modern security surveillance room with multiple monitor screens showing building corridors, clean dark ambient lighting, professional equipment, no text, 4k photography",
    "espaco": "ultra realistic photo, small modern convenience store fitting perfectly inside a residential building common area, organized shelves, warm lighting, clean floors, no people, no text, 4k interior photography",
    "conveniencia": "ultra realistic photo, close up of organized mini market shelves with packaged snacks drinks personal care items, bright clean lighting, no people, no text, 4k product photography",
    "implantacao": "ultra realistic photo, construction workers installing modern retail shelving system inside a building lobby, clean professional environment, tools and equipment visible, no text, 4k photography",
    "gestao": "ultra realistic photo, property manager using tablet showing analytics dashboard inside a modern condominium office, clean minimalist interior, no text, 4k photography",
    "valorizacao": "ultra realistic photo, luxury residential building exterior at golden hour with modern lobby visible, premium architecture, lush landscaping, no text, 4k real estate photography",
    "sustentabilidade": "ultra realistic photo, eco-friendly modern building with green wall and solar panels, sustainable architecture, clear blue sky, no text, 4k architectural photography",
}
DEFAULT_IMAGE_PROMPT = "ultra realistic photo, modern mini market inside residential building lobby, organized shelves, bright clean lighting, self-checkout kiosk, no people, no text, 4k interior photography"

TOPICOS_OPERACIONAL = [
    ("mercado_autonomo", "Como funciona um minimercado autônomo 24h instalado dentro de um condomínio residencial: como o morador acessa, faz o pagamento self-checkout, como funciona a reposição e qual a diferença para um mercado comum."),
    ("implantacao", "O processo de implantação de um minimercado autônomo em condomínio: análise do espaço, modelos disponíveis e o que o condomínio precisa providenciar."),
    ("espaco", "Comparação dos modelos Compact (2x2m), Wall (3x1m), Smart (3x2m) e Prime (4x2m) e qual atende melhor cada tipo de condomínio."),
    ("conveniencia", "O mix ideal de produtos para um minimercado autônomo em condomínio: bebidas, snacks, higiene, mercearia e limpeza."),
    ("mercado_autonomo", "O self-checkout em minimercados de condomínio: como funciona o totem, formas de pagamento e por que é diferente de um caixa humano."),
]
TOPICOS_SINDICO = [
    ("sindico", "Como propor e aprovar um minimercado autônomo em assembleia: argumentos, objeções comuns e como respondê-las."),
    ("valorizacao", "Como um minimercado autônomo 24h valoriza um condomínio residencial sem custo extra na taxa condominial."),
    ("gestao", "Os benefícios para síndicos: aproveitamento de áreas ociosas, redução de entregadores externos e diferencial no mercado imobiliário."),
    ("sindico", "As perguntas mais frequentes de síndicos antes de instalar um minimercado autônomo: custo, segurança, contrato e suporte."),
    ("valorizacao", "Como amenities internos como academia, coworking e minimercado autônomo estão se tornando decisivos na escolha de onde morar."),
]
TOPICOS_TECNOLOGIA = [
    ("tecnologia", "A tecnologia de um minimercado autônomo em condomínio: app de acesso, câmeras em nuvem e alertas de estoque sem funcionários presenciais."),
    ("seguranca", "Segurança em minimercados autônomos: como câmeras, identificação do morador e pagamento rastreável reduzem perdas."),
    ("tecnologia", "Como Pix e pagamento por aproximação transformaram o varejo de conveniência em condomínios residenciais."),
    ("gestao", "Como dados de consumo de um minimercado autônomo ajudam a melhorar o mix de produtos e beneficiam os moradores."),
    ("sustentabilidade", "Como minimercados autônomos em condomínios contribuem para hábitos mais sustentáveis: menos deslocamento e compras de proximidade."),
]

pool = TOPICOS_OPERACIONAL if hour < 12 else (TOPICOS_SINDICO if hour < 19 else TOPICOS_TECNOLOGIA)
image_key, topic = random.choice(pool)
image_prompt = IMAGE_PROMPTS.get(image_key, DEFAULT_IMAGE_PROMPT)

if pool == TOPICOS_OPERACIONAL:
    category = random.choice(["Como funciona", "Guias"])
elif pool == TOPICOS_SINDICO:
    category = random.choice(["Gestão condominial", "Para síndicos"])
else:
    category = random.choice(["Tecnologia", "Sustentabilidade"])

tags_map = {
    "mercado_autonomo": ["mercado autônomo", "self-checkout", "conveniência"],
    "sindico": ["síndico", "gestão condominial", "assembleia"],
    "tecnologia": ["tecnologia", "acesso digital", "pagamento"],
    "seguranca": ["segurança", "câmeras", "controle de acesso"],
    "espaco": ["modelos", "espaço", "compact", "smart", "prime"],
    "conveniencia": ["conveniência", "produtos", "24 horas"],
    "implantacao": ["implantação", "instalação", "sem custo"],
    "gestao": ["gestão", "síndico", "condomínio"],
    "valorizacao": ["valorização", "imóvel", "amenities"],
    "sustentabilidade": ["sustentabilidade", "consumo local", "proximidade"],
}
tags = tags_map.get(image_key, ["mercado autônomo", "condomínio"])


def title_to_slug(title: str) -> str:
    title = unicodedata.normalize("NFD", title)
    title = "".join(c for c in title if unicodedata.category(c) != "Mn")
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s-]", "", title)
    title = re.sub(r"[\s-]+", "-", title).strip("-")
    return title[:80]


def chamar_api(messages, max_tokens=4000):
    """Tenta cada modelo em ordem. Retorna (texto, model_id) ou lança sys.exit(1)."""
    MODELS = [
        "google/gemma-4-31b-it:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "nvidia/nemotron-3-nano-30b-a3b:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "openrouter/free",
    ]
    for model in MODELS:
        print(f"  [{model}] Tentando...")
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": max_tokens
        }).encode()
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://seumarketbr.com.br",
                "X-Title": "Seu Market Blog"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                choices = data.get("choices", [])
                if not choices:
                    print(f"  [{model}] Sem choices.")
                    continue
                finish = choices[0].get("finish_reason", "")
                msg = choices[0].get("message", {})
                print(f"  [{model}] finish_reason: {finish}")
                if finish == "length":
                    print(f"  [{model}] Truncado, tentando proximo.")
                    continue
                raw = (msg.get("content") or msg.get("reasoning") or "").strip()
                if len(raw) < 50:
                    print(f"  [{model}] Resposta curta demais, pulando.")
                    continue
                print(f"  [{model}] OK ({len(raw)} chars)")
                return raw, model
        except urllib.error.HTTPError as e:
            print(f"  [{model}] HTTPError {e.code}: {e.read().decode()[:200]}")
        except urllib.error.URLError as e:
            print(f"  [{model}] URLError: {e.reason}")
        except Exception as e:
            print(f"  [{model}] Erro: {type(e).__name__}: {e}")
    return None, None


# ── ETAPA 1: Gerar o corpo do artigo (só markdown, sem JSON) ──────────────
print("=" * 60)
print("ETAPA 1: Gerando corpo do artigo...")
print(f"Tema: {topic}")
print("=" * 60)

system_artigo = (
    "Você é o redator do blog do Seu Market, empresa de minimercados autônomos 24h em condomínios brasileiros. "
    "Escreve artigos informativos, úteis e com tom humano, sem soar como IA.\n"
    "REGRAS:\n"
    "1. NUNCA use bullet points, traços ou listas. Apenas parágrafos corridos.\n"
    "2. Use ## para títulos de seção (no mínimo 4 seções). Jamais ### ou ####.\n"
    "3. O único link permitido: https://seumarketbr.com.br. Ao citar a empresa use [Seu Market](https://seumarketbr.com.br).\n"
    "4. Tom natural e direto. Sem 'Além disso', 'Em conclusão', 'Outrossim'.\n"
    "5. NUNCA invente dados ou estatísticas.\n"
    "6. 100% em português do Brasil.\n"
    "Retorne SOMENTE o texto do artigo em markdown. Nenhum JSON, nenhuma explicação extra."
)

user_artigo = (
    f"Hoje é {today}. Escreva um artigo sobre: {topic}\n\n"
    f"Fatos obrigatórios (use apenas esses, nunca invente):\n{SEU_MARKET_FACTS}\n\n"
    "Escreva NO MÍNIMO 1200 palavras em português do Brasil. "
    "Use ## para títulos de seção e **negrito** para ênfase. "
    "Apenas parágrafos corridos, sem listas, sem traços para separar ideias.\n"
    "Retorne SOMENTE o texto markdown do artigo, sem nenhum JSON ou explicação."
)

content, model_usado = chamar_api([
    {"role": "system", "content": system_artigo},
    {"role": "user", "content": user_artigo}
], max_tokens=4000)

if not content:
    print("ETAPA 1 falhou: todos os modelos truncaram ou falharam.")
    sys.exit(1)

word_count = len(content.split())
print(f"\nEtapa 1 concluída: {word_count} palavras com [{model_usado}]")


# ── ETAPA 2: Gerar título e excerpt (resposta curta, ~100 tokens) ─────────
print("\n" + "=" * 60)
print("ETAPA 2: Gerando titulo e excerpt...")
print("=" * 60)

system_meta = "Você extrai metadados de artigos. Responda SOMENTE com JSON válido, sem nenhum texto fora."
user_meta = (
    f"Com base neste artigo, gere um título atraente e um excerpt de 1 frase.\n"
    f"Artigo (primeiros 800 chars):\n{content[:800]}\n\n"
    "Responda SOMENTE este JSON:\n"
    '{"title": "...", "excerpt": "..."}'
)

meta_raw, _ = chamar_api([
    {"role": "system", "content": system_meta},
    {"role": "user", "content": user_meta}
], max_tokens=200)

title = ""
excerpt = ""
if meta_raw:
    try:
        meta = json.loads(meta_raw)
        title = meta.get("title", "").strip()
        excerpt = meta.get("excerpt", "").strip()
    except Exception:
        # tenta extrair do JSON embutido
        m = re.search(r'"title"\s*:\s*"([^"]+)"', meta_raw)
        if m:
            title = m.group(1).strip()
        m = re.search(r'"excerpt"\s*:\s*"([^"]+)"', meta_raw)
        if m:
            excerpt = m.group(1).strip()

# Fallback: primeira linha não vazia como titulo
if not title:
    for line in content.splitlines():
        line = line.strip().lstrip("#").strip()
        if len(line) > 10:
            title = line[:100]
            break
if not title:
    title = f"Minimercado autônomo em condomínios: {today}"
if not excerpt:
    for line in content.splitlines():
        line = line.strip()
        if len(line) > 40 and not line.startswith("#"):
            excerpt = line[:200]
            break

print(f"Titulo: {title}")
print(f"Excerpt: {excerpt[:80]}...")


# ── ETAPA 3: Montar o post localmente ──────────────────────────────────
# Remove links externos do content
content = re.sub(
    r'\[([^\]]+)\]\((?!https://seumarketbr\.com\.br)[^)]+\)',
    r'\1',
    content
)

slug = title_to_slug(title)
base_slug = slug
counter = 1
while os.path.exists(f"public/blog-posts/{slug}.json"):
    slug = f"{base_slug}-{counter}"
    counter += 1

seed = abs(hash(slug)) % 999999
encoded_prompt = urllib.parse.quote(image_prompt)
cover_image = (
    f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    f"?width=1440&height=720&model=flux&nologo=true&seed={seed}"
)

reading_time = max(1, round(len(content.split()) / 200))

post = {
    "id": slug,
    "slug": slug,
    "title": title,
    "excerpt": excerpt,
    "content": content,
    "category": category,
    "author": "Seu Market",
    "date": today,
    "readingTime": reading_time,
    "featured": False,
    "coverImage": cover_image,
    "tags": tags,
}

os.makedirs("public/blog-posts", exist_ok=True)
filepath = f"public/blog-posts/{slug}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(post, f, ensure_ascii=False, indent=2)

print(f"\n[OK] Post salvo: {filepath}")
print(f"[OK] Titulo: {title}")
print(f"[OK] Slug: {slug}")
print(f"[OK] Palavras: {len(content.split())}")
print(f"[OK] Leitura: {reading_time} min")
print(f"[OK] Imagem: {cover_image}")
