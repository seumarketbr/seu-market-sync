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
- Site oficial e Único link permitido: https://seumarketbr.com.br
NÃO FAZER:
- Não confirmar números de unidades instaladas desconhecidos.
- Não dizer que produtos são mais baratos que supermercados.
- Não dizer que o serviço é totalmente gratuito (cobra dos consumidores nos produtos).
- NÃO usar traços ou hífens para separar ideias no meio de frases. Use vírgulas.
- NÃO inserir links para sites externos. O Único link permitido é https://seumarketbr.com.br
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
    title = unicodedata.normalize("NFD", title)
    title = "".join(c for c in title if unicodedata.category(c) != "Mn")
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s-]", "", title)
    title = re.sub(r"[\s-]+", "-", title).strip("-")
    return title[:80]


system_msg = (
    "Você é o redator do blog do Seu Market, empresa de minimercados autônomos 24h em condomínios brasileiros. "
    "Escreve artigos informativos, úteis e com tom humano, sem soar como IA. "
    "REGRAS OBRIGATÓRIAS:\n"
    "1. NUNCA use bullet points, traços ou listas. Tudo em parágrafos corridos.\n"
    "2. NUNCA use traço ou hífen para separar ideias no meio de uma frase. Use vírgula no lugar.\n"
    "3. Use ## apenas para títulos de seção. Jamais ### ou ####.\n"
    "4. O Único link permitido em todo o artigo é https://seumarketbr.com.br. NUNCA insira outros URLs.\n"
    "5. Tom natural, direto. Sem 'Além disso', 'Outrossim', 'Em conclusão'.\n"
    "6. NUNCA invente estatísticas ou fatos não fornecidos.\n"
    "7. Escreva 100% em português do Brasil.\n"
    "CRÍTICO: Retorne APENAS o objeto JSON válido, sem nenhum texto antes ou depois, "
    "sem blocos de código Markdown, sem ``` de nenhum tipo. "
    "A resposta deve começar EXATAMENTE com { e terminar EXATAMENTE com }."
)

user_msg = (
    f"Hoje é {today}. {topic}\n\n"
    f"FATOS OBRIGATÓRIOS, use SOMENTE esses dados, nunca invente:\n{SEU_MARKET_FACTS}\n\n"
    "Escreva um artigo com NO MÍNIMO 1200 palavras em português do Brasil. "
    "Use ## para títulos de seção e **negrito** para ênfase. "
    "Apenas parágrafos corridos, sem listas, sem traços para separar ideias, use vírgulas. "
    "O Único link permitido é https://seumarketbr.com.br. Ao citar o Seu Market, use: [Seu Market](https://seumarketbr.com.br).\n\n"
    "O campo slug deve ser gerado a partir do título: letras minúsculas, sem acentos, palavras separadas por hífen, máx 80 chars.\n"
    "Exemplo: título 'Como funciona o self-checkout' vira slug 'como-funciona-o-self-checkout'\n\n"
    "Retorne APENAS este JSON válido (sem nenhum texto fora do JSON):\n"
    "{\n"
    '  "title": "Título do artigo aqui",\n'
    '  "slug": "slug-do-artigo-aqui",\n'
    '  "excerpt": "Resumo de 1 a 2 frases aqui",\n'
    '  "content": "Conteúdo completo do artigo aqui em markdown",\n'
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
    "mistralai/mistral-small-3.2-24b-instruct:free",
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-r1-0528-qwen3-8b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
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
        raise ValueError("Nenhum { encontrado")
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
        raise ValueError("JSON incompleto")
    candidate = text[start:end]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido: {e}\nTrecho:\n{candidate[:400]}")


# ── Chamada à API com log detalhado ──────────────────────────────
response_data = None
content = ""

for model in MODELS:
    print(f"\n[{model}] Tentando...")
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
            "HTTP-Referer": "https://seumarketbr.com.br",
            "X-Title": "Seu Market Blog"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
            print(f"[{model}] Resposta recebida. Chaves: {list(data.keys())}")
            choices = data.get("choices", [])
            if not choices:
                print(f"[{model}] Sem choices. Resposta: {json.dumps(data)[:500]}")
                continue
            msg = choices[0].get("message", {})
            print(f"[{model}] finish_reason: {choices[0].get('finish_reason')} | message keys: {list(msg.keys())}")
            raw = msg.get("content") or ""
            if not raw.strip():
                raw = msg.get("reasoning") or ""
            print(f"[{model}] Tamanho do conteúdo: {len(raw)} chars")
            if len(raw.strip()) < 50:
                print(f"[{model}] Conteúdo muito curto, pulando. Raw: {repr(raw[:200])}")
                continue
            content = raw.strip()
            response_data = data
            print(f"[{model}] Sucesso! {len(content)} chars")
            break
    except urllib.error.HTTPError as e:
        print(f"[{model}] HTTPError {e.code}: {e.read().decode()[:300]}")
    except urllib.error.URLError as e:
        print(f"[{model}] URLError: {e.reason}")
    except Exception as e:
        print(f"[{model}] Erro inesperado: {type(e).__name__}: {e}")

if not response_data or not content:
    print("\nTodos os modelos falharam. Abortando.")
    sys.exit(1)

print(f"\nConteudo bruto (primeiros 300 chars):\n{content[:300]}")
try:
    post = extrair_json(content)
except ValueError as e:
    print(f"Erro ao extrair JSON: {e}")
    print(f"Conteúdo bruto completo:\n{content[:2000]}")
    sys.exit(1)

if not post.get("title") or not post.get("content"):
    print(f"ERRO: Post sem título ou conteúdo!")
    sys.exit(1)

# Garante que nenhum link externo passou pelo modelo
post["content"] = re.sub(
    r'\[([^\]]+)\]\((?!https://seumarketbr\.com\.br)[^)]+\)',
    r'\1',
    post.get("content", "")
)

# Slug baseado no título
raw_title = post.get("title", "")
slug = title_to_slug(raw_title) if raw_title else f"post-{now.strftime('%Y-%m-%d-%H%M')}"
base_slug = slug
counter = 1
while os.path.exists(f"public/blog-posts/{slug}.json"):
    slug = f"{base_slug}-{counter}"
    counter += 1

post["slug"] = slug
post["id"] = slug

# Imagem Pollinations
seed = abs(hash(slug)) % 999999
encoded_prompt = urllib.parse.quote(image_prompt)
post["coverImage"] = (
    f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    f"?width=1440&height=720&model=flux&nologo=true&seed={seed}"
)

# Pós-processamento
post["readingTime"] = max(1, round(len(post.get("content", "").split()) / 200))
post["author"] = "Seu Market"
post["category"] = category
post.setdefault("tags", tags)
post.setdefault("featured", False)
post.setdefault("date", today)

os.makedirs("public/blog-posts", exist_ok=True)
filepath = f"public/blog-posts/{slug}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(post, f, ensure_ascii=False, indent=2)

print(f"\n✔ Post salvo: {filepath}")
print(f"✔ Título: {post['title']}")
print(f"✔ Slug: {slug}")
print(f"✔ Palavras: {len(post['content'].split())}")
print(f"✔ Imagem: {post['coverImage']}")
