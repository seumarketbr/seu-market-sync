import os, json, urllib.request, urllib.error, urllib.parse, sys, random, re, unicodedata
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
today = now.strftime("%Y-%m-%d")
hour = now.hour
api_key = os.environ["OPENROUTER_API_KEY"]

SEU_MARKET_FACTS = """
- Empresa brasileira: minimercados autônomos 24h em condomínios residenciais e comerciais.
- Operação 100% self-checkout: totem com Pix, crédito, débito e aproximação.
- Implantação gratuita para o condomínio: estrutura, equipamentos e estoque são da operação.
- O condomínio cede o espaço ocioso e recebe o serviço pronto, sem custo nem rateio.
- Modelos: Compact (2x2m), Wall (3x1m), Smart (3x2m — mais vendido), Prime (4x2m).
- Tecnologia: acesso por app, câmeras em nuvem, alertas automáticos de estoque.
- Reposição periódica com curadoria conforme o perfil do condomínio.
- Suporte via WhatsApp para moradores e síndico.
- Site oficial: seumarket.com.br
NÃO DIZER:
- Que tem centenas de unidades instaladas (não confirme números desconhecidos)
- Que produtos são mais baratos que supermercados (são preços de mercado)
- Que o serviço é totalmente gratuito (cobra dos consumidores nos produtos)
"""

IMAGE_PROMPTS = {
    "mercado_autonomo": "minimalist modern blog banner, sleek autonomous convenience store interior with self-checkout kiosk, soft warm lighting, no text, professional retail aesthetic, photorealistic",
    "sindico": "minimalist modern blog banner, modern building management concept, neutral tones, professional corporate aesthetic, no text, photorealistic",
    "tecnologia": "minimalist modern blog banner, digital access control and surveillance camera concept, clean dark blue palette, professional tech aesthetic, no text, photorealistic",
    "seguranca": "minimalist modern blog banner, security shield and camera silhouette, dark background with blue accents, professional aesthetic, no text, photorealistic",
    "espaco": "minimalist modern blog banner, architectural floor plan of small store inside a building corridor, clean lines, neutral tones, professional aesthetic, no text, photorealistic",
    "conveniencia": "minimalist modern blog banner, grocery items and smartphone with QR code payment, soft green tones, professional lifestyle aesthetic, no text, photorealistic",
    "implantacao": "minimalist modern blog banner, installation and setup concept with tools and building blueprint, neutral professional tones, no text, photorealistic",
    "gestao": "minimalist modern blog banner, modern property management dashboard concept, clean blue and white tones, professional aesthetic, no text, photorealistic",
    "valorizacao": "minimalist modern blog banner, upward growth arrow above residential building silhouette, clean green palette, professional real estate aesthetic, no text, photorealistic",
    "sustentabilidade": "minimalist modern blog banner, green leaf icon integrated with building silhouette, eco-friendly tones, professional aesthetic, no text, photorealistic",
}
DEFAULT_IMAGE_PROMPT = "minimalist modern blog banner, convenience store shelf inside a residential building, clean neutral tones, professional retail aesthetic, no text, photorealistic"

TOPICOS_OPERACIONAL = [
    ("mercado_autonomo", "Escreva um artigo explicando como funciona um minimercado autônomo 24h instalado dentro de um condomínio residencial: como o morador acessa, faz o pagamento self-checkout, como funciona a reposição e qual a diferença para um mercado comum."),
    ("implantacao", "Escreva um artigo detalhando o processo de implantação de um minimercado autônomo em condomínio: análise do espaço, modelos disponíveis e o que o condomínio precisa providenciar."),
    ("espaco", "Escreva um artigo comparando os modelos Compact (2x2m), Wall (3x1m), Smart (3x2m) e Prime (4x2m) e qual atende melhor cada tipo de condomínio."),
    ("conveniencia", "Escreva um artigo sobre o mix ideal de produtos para um minimercado autônomo em condomínio: bebidas, snacks, higiene, mercearia e limpeza."),
    ("mercado_autonomo", "Escreva um artigo sobre o self-checkout em minimercados de condomínio: como funciona o totem, formas de pagamento e por que é diferente de um caixa humano."),
]
TOPICOS_SINDICO = [
    ("sindico", "Escreva um artigo para síndicos sobre como propor e aprovar um minimercado autônomo em assembleia: argumentos, objeções comuns e como respondê-las."),
    ("valorizacao", "Escreva um artigo sobre como um minimercado autônomo 24h valoriza um condomínio residencial sem custo extra na taxa condominial."),
    ("gestao", "Escreva um artigo sobre os benefícios para síndicos: aproveitamento de áreas ociosas, redução de entregadores externos e diferencial no mercado imobiliário."),
    ("sindico", "Escreva um artigo com as perguntas mais frequentes de síndicos antes de instalar um minimercado autônomo: custo, segurança, contrato e suporte."),
    ("valorizacao", "Escreva um artigo sobre como amenities internos como academia, coworking e minimercado autônomo estão se tornando decisivos na escolha de onde morar."),
]
TOPICOS_TECNOLOGIA = [
    ("tecnologia", "Escreva um artigo sobre a tecnologia de um minimercado autônomo em condomínio: app de acesso, câmeras em nuvem e alertas de estoque sem funcionários presenciais."),
    ("seguranca", "Escreva um artigo sobre segurança em minimercados autônomos: como câmeras, identificação do morador e pagamento rastreável reduzem perdas."),
    ("tecnologia", "Escreva um artigo sobre como Pix e pagamento por aproximação transformaram o varejo de conveniência em condomínios residenciais."),
    ("gestao", "Escreva um artigo sobre como dados de consumo de um minimercado autônomo ajudam a melhorar o mix de produtos e beneficiam os moradores."),
    ("sustentabilidade", "Escreva um artigo sobre como minimercados autônomos em condomínios contribuem para hábitos mais sustentáveis: menos deslocamento e compras de proximidade."),
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
    """Converte título em slug URL-friendly."""
    title = unicodedata.normalize("NFD", title)
    title = "".join(c for c in title if unicodedata.category(c) != "Mn")
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s-]", "", title)
    title = re.sub(r"[\s-]+", "-", title).strip("-")
    return title[:80]  # máx 80 chars


system_msg = (
    "Você é o redator do blog do Seu Market, empresa de minimercados autônomos 24h em condomínios brasileiros. "
    "Escreve artigos informativos, úteis e com tom humano — sem soar como IA. "
    "REGRAS OBRIGATÓRIAS:\n"
    "1. NUNCA use bullet points, traços ou listas. Tudo em parágrafos corridos.\n"
    "2. Use ## apenas para títulos de seção. Jamais ### ou ####.\n"
    "3. Links sempre no formato [texto visível](url). Nunca URL crua.\n"
    "4. Tom natural, direto. Sem 'Além disso', 'Outrossim', 'Em conclusão'.\n"
    "5. NUNCA invente estatísticas ou fatos não fornecidos.\n"
    "6. Escreva 100% em português do Brasil.\n"
    "CRÍTICO: Retorne APENAS o objeto JSON puro, sem nenhum texto antes ou depois, "
    "sem blocos de código Markdown, sem ``` de nenhum tipo. "
    "A resposta deve começar EXATAMENTE com { e terminar EXATAMENTE com }. Nada mais."
)

user_msg = (
    f"Hoje é {today}. {topic}\n\n"
    f"FATOS OBRIGATÓRIOS — use SOMENTE esses dados, nunca invente:\n{SEU_MARKET_FACTS}\n\n"
    "Escreva um artigo com NO MÍNIMO 1200 palavras em português do Brasil. "
    "Use ## para títulos de seção e **negrito** para ênfase. "
    "Sem bullet points, sem traços, sem ###. Apenas parágrafos corridos. "
    "Links no formato [texto](url). Ao citar o Seu Market, linke para [seumarket.com.br](https://seumarket.com.br).\n\n"
    "IMPORTANTE: o campo \"slug\" deve ser gerado a partir do título do artigo em formato URL-friendly "
    "(letras minúsculas, sem acentos, palavras separadas por hífen, máx 80 chars). Exemplo: "
    "título 'Como funciona o self-checkout' → slug 'como-funciona-o-self-checkout'.\n\n"
    "Retorne APENAS este JSON (comece com { e termine com }, sem nenhum texto adicional):\n"
    "{\n"
    '  "title": "",\n'
    '  "slug": "",\n'
    '  "excerpt": "",\n'
    '  "content": "",\n'
    f'  "category": "{category}",\n'
    '  "author": "Seu Market",\n'
    f'  "date": "{today}",\n'
    '  "readingTime": 6,\n'
    '  "featured": false,\n'
    '  "coverImage": "",\n'
    f'  "tags": {json.dumps(tags, ensure_ascii=False)}\n'
    "}"
)

MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "mistralai/mistral-small-3.2-24b-instruct:free",
]


def extrair_json(text):
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    cleaned = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except Exception:
        pass
    start = text.find("{")
    if start == -1:
        raise ValueError("Nenhum { encontrado na resposta do modelo.")
    depth, in_string, escape_next, end = 0, False, False, -1
    for i, ch in enumerate(text[start:], start):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end == -1:
        raise ValueError("JSON incompleto.")
    candidate = text[start:end]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON extraído mas inválido: {e}\nTrecho:\n{candidate[:400]}")


# ── Chamada à API ─────────────────────────────────────────────────────────────
response_data = None
content = ""

for model in MODELS:
    print(f"Tentando modelo: {model}")
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7,
        "max_tokens": 4500
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://seumarket.com.br",
            "X-Title": "Seu Market Blog"
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            msg = data.get("choices", [{}])[0].get("message", {})
            content = msg.get("content") or msg.get("reasoning") or ""
            if not content.strip():
                print(f"Modelo {model} retornou vazio, próximo...")
                continue
            content = content.strip()
            response_data = data
            print(f"Sucesso com {model} ({len(content)} chars)")
            break
    except urllib.error.HTTPError as e:
        print(f"Modelo {model} falhou: {e.code} - {e.read().decode()[:200]}")
        continue

if not response_data or not content:
    print("Todos os modelos falharam.")
    sys.exit(1)

# ── Extração robusta do JSON ──────────────────────────────────────────────────
try:
    post = extrair_json(content)
except ValueError as e:
    print(f"Erro ao extrair JSON: {e}")
    print(f"Conteúdo bruto (primeiros 800 chars):\n{content[:800]}")
    sys.exit(1)

# ── Slug baseado no título ────────────────────────────────────────────────────
raw_title = post.get("title", "")
if raw_title:
    slug = title_to_slug(raw_title)
    # Garante unicidade com sufixo de data se necessário
    base_slug = slug
    counter = 1
    while os.path.exists(f"public/blog-posts/{slug}.json"):
        slug = f"{base_slug}-{counter}"
        counter += 1
else:
    slug = f"post-{now.strftime('%Y-%m-%d-%H%M')}"

post["slug"] = slug
post["id"] = slug

# ── Imagem Pollinations alta qualidade ───────────────────────────────────────
encoded_prompt = urllib.parse.quote(image_prompt)
# width=1280, height=640 (aspect ratio 2:1, banner ideal), enhance=true para qualidade
post["coverImage"] = (
    f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    f"?width=1280&height=640&model=flux&enhance=true&nologo=true"
    f"&seed={abs(hash(slug)) % 99999}"
)

# ── Pós-processamento ─────────────────────────────────────────────────────────
post["readingTime"] = max(1, round(len(post.get("content", "").split()) / 200))
post["author"] = "Seu Market"
post["category"] = category
post.setdefault("tags", tags)
post.setdefault("featured", False)
post.setdefault("date", today)

# ── Salvar JSON ───────────────────────────────────────────────────────────────
os.makedirs("public/blog-posts", exist_ok=True)
filepath = f"public/blog-posts/{slug}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(post, f, ensure_ascii=False, indent=2)

print(f"Post salvo: {filepath}")
print(f"Título: {post.get('title', 'sem título')}")
print(f"Slug: {slug}")
print(f"Imagem: {post['coverImage']}")
