import os, json, urllib.request, urllib.error, urllib.parse, sys, random, re, unicodedata
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
today = now.strftime("%Y-%m-%d")
hour = now.hour
api_key = os.environ["OPENROUTER_API_KEY"]
unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")

SEU_MARKET_BR_FACTS = """
O Seu Market BR é uma empresa brasileira que atua com minimercados autônomos 24 horas em condomínios.
A operação utiliza modelo de self-checkout.
Os meios de pagamento autorizados são Pix, crédito, débito e aproximação.
A implantação para o condomínio é gratuita.
Existem os seguintes modelos de estrutura: Compact (2x2m), Wall (3x1m), Smart (3x2m), Prime (4x2m).
O Seu Market BR possui câmeras em nuvem.
O Seu Market BR possui recursos de alertas de estoque.
O suporte é realizado via WhatsApp.
Site oficial e único link permitido: https://seumarketbr.com.br
"""

UNSPLASH_QUERIES = {
    "mercado_autonomo": "self service mini market convenience store interior",
    "sindico": "condominium building manager professional",
    "tecnologia": "digital payment kiosk touchscreen technology",
    "seguranca": "security camera surveillance building modern",
    "espaco": "convenience store shelves interior organized",
    "conveniencia": "grocery store shelves food drinks products",
    "implantacao": "retail store installation shelving modern",
    "gestao": "property management building modern office",
    "valorizacao": "luxury residential building exterior architecture",
    "sustentabilidade": "sustainable modern building green architecture",
}
DEFAULT_UNSPLASH_QUERY = "modern convenience store interior clean"

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
    ("tecnologia", "A tecnologia de um minimercado autônomo em condomínio: câmeras em nuvem, alertas de estoque e pagamento digital sem funcionários presenciais."),
    ("seguranca", "Segurança em minimercados autônomos: como câmeras, pagamento rastreável e ambiente de comunidade fechada reduzem perdas."),
    ("tecnologia", "Como Pix e pagamento por aproximação transformaram o varejo de conveniência em condomínios residenciais."),
    ("gestao", "Como dados de consumo de um minimercado autônomo ajudam a melhorar o mix de produtos e beneficiam os moradores."),
    ("sustentabilidade", "Como minimercados autônomos em condomínios contribuem para hábitos mais sustentáveis: menos deslocamento e compras de proximidade."),
]

pool = TOPICOS_OPERACIONAL if hour < 12 else (TOPICOS_SINDICO if hour < 19 else TOPICOS_TECNOLOGIA)
image_key, topic = random.choice(pool)

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


def buscar_imagem_unsplash(query: str, fallback: str = DEFAULT_UNSPLASH_QUERY) -> str:
    if not unsplash_key:
        print("  [Unsplash] UNSPLASH_ACCESS_KEY nao definida, pulando.")
        return ""
    for q in [query, fallback]:
        try:
            encoded = urllib.parse.quote(q)
            url = f"https://api.unsplash.com/search/photos?query={encoded}&per_page=15&orientation=landscape&content_filter=high"
            req = urllib.request.Request(url, headers={
                "Authorization": f"Client-ID {unsplash_key}",
                "Accept-Version": "v1"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                results = data.get("results", [])
                if results:
                    photo = random.choice(results)
                    img_url = (
                        photo.get("urls", {}).get("full")
                        or photo.get("urls", {}).get("regular")
                        or ""
                    )
                    if img_url:
                        print(f"  [Unsplash] Imagem encontrada para '{q}': {img_url[:80]}...")
                        return img_url
        except Exception as e:
            print(f"  [Unsplash] Erro na query '{q}': {e}")
    return ""


def chamar_api(messages, max_tokens=4000):
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


print("=" * 60)
print("ETAPA 1: Buscando imagem no Unsplash...")
unsplash_query = UNSPLASH_QUERIES.get(image_key, DEFAULT_UNSPLASH_QUERY)
cover_image = buscar_imagem_unsplash(unsplash_query)
if cover_image:
    print(f"Imagem Unsplash OK")
else:
    print("Unsplash nao retornou imagem, post ficara sem capa.")


print("\n" + "=" * 60)
print("ETAPA 2: Gerando corpo do artigo...")
print(f"Tema: {topic}")
print("=" * 60)

system_artigo = (
    "Você é o redator editorial do blog do **Seu Market BR**, uma empresa brasileira que atua no segmento de minimercados autônomos em condomínios.\n\n"
    "Sua principal missão é produzir conteúdos informativos, educativos e relevantes sobre o mercado de minimercados autônomos, conveniência, varejo autônomo, comportamento do consumidor, novas formas de comprar, operação de pequenos pontos de venda, tecnologia aplicada ao varejo e transformação da experiência de compra em condomínios brasileiros.\n\n"
    "O artigo NÃO deve ser tratado como uma propaganda do Seu Market BR. A prioridade é construir autoridade sobre o mercado autônomo como categoria, explicando conceitos, tendências, comportamentos, desafios, oportunidades e mudanças que esse modelo representa para consumidores, condomínios e para o varejo.\n\n"
    "O Seu Market BR pode aparecer naturalmente quando houver relação direta com o assunto, mas nunca deve ser forçado dentro do texto. A prioridade é falar sobre o mercado autônomo, e não sobre o que o Seu Market BR possui.\n\n"
    "## OBJETIVO EDITORIAL\n"
    "Escreva como um especialista que conhece o mercado de minimercados autônomos e consegue explicar o assunto de maneira simples, clara e interessante para uma pessoa comum. O leitor deve terminar o artigo entendendo melhor o tema abordado. O conteúdo deve funcionar mesmo que o nome Seu Market BR seja removido do artigo. Evite transformar o texto em apresentação comercial da empresa. Não fique repetindo o nome Seu Market BR ao longo do artigo. Quando o tema permitir uma conexão natural com a empresa, uma breve menção institucional pode ser feita, desde que baseada exclusivamente nos fatos autorizados no bloco SEU_MARKET_BR_FACTS.\n\n"
    "## REGRAS ABSOLUTAS DE FORMATAÇÃO\n"
    "NUNCA usar bullet points.\n"
    "NUNCA usar listas numeradas.\n"
    "NUNCA usar listas com traços.\n"
    "NUNCA criar tabelas.\n"
    "O conteúdo deve ser formado exclusivamente por parágrafos corridos.\n"
    "Use ## para todos os títulos de seção.\n"
    "Utilize no mínimo 4 seções.\n"
    "Jamais utilize ### ou ####.\n"
    "Utilize negrito somente quando realmente contribuir para destacar uma informação importante.\n"
    "NUNCA use asterisco simples para envolver palavras ou expressões (ex: *palavra* ou *expressão*). "
    "Asterisco simples é itálico e não deve ser usado em nenhuma hipótese. "
    "Se quiser dar ênfase, use **negrito** apenas quando estritamente necessário.\n"
    "NUNCA use travessão (—), meia-risca (–) ou hífen (-) para separar ideias dentro de uma frase no lugar de vírgulas. "
    "Quando precisar intercalar uma explicação ou complemento dentro de uma frase, use vírgulas. "
    "O hífen (-) só é permitido em palavras compostas (ex: self-checkout, 24h, guarda-chuva).\n"
    "O artigo deve ter no mínimo 1200 palavras.\n"
    "Escreva 100% em português do Brasil.\n\n"
    "## TOM E ESTILO\n"
    "O texto deve parecer escrito por um redator humano especializado em varejo e comportamento do consumidor. Use linguagem natural, direta e fácil de compreender. Evite linguagem corporativa excessiva. Evite frases genéricas e artificiais. Não utilize expressões como 'Além disso', 'Em conclusão', 'Outrossim', 'Nesse contexto, é importante destacar' ou outras construções excessivamente previsíveis e artificiais. Não comece todos os artigos com a mesma estrutura. Não termine todos os artigos com a mesma estrutura. Varie o ritmo dos parágrafos. Use exemplos hipotéticos apenas quando forem claramente apresentados como exemplos, nunca como fatos. Não faça afirmações absolutas sem base.\n\n"
    "## REGRA DE VERACIDADE\n"
    "NUNCA invente números, estatísticas, pesquisas, percentuais, quantidade de clientes, quantidade de lojas, quantidade de condomínios, faturamento, crescimento, número de usuários ou qualquer outro dado quantitativo. NUNCA transforme uma possibilidade em fato. NUNCA atribua ao Seu Market BR uma informação que não esteja no bloco SEU_MARKET_BR_FACTS. NUNCA invente funcionalidades, equipamentos, tecnologias ou processos utilizados pela empresa. Quando não houver informação suficiente para afirmar algo sobre a empresa, simplesmente não faça a afirmação.\n\n"
    "## O QUE NÃO AFIRMAR SOBRE O SEU MARKET BR\n"
    "Não afirmar número de unidades instaladas. Não afirmar quantidade de condomínios atendidos. Não afirmar quantidade de clientes ou usuários. Não afirmar faturamento. Não afirmar crescimento percentual. Não afirmar que os produtos são mais baratos que supermercados. Não afirmar que o Seu Market BR possui aplicativo de compras. Não afirmar que o consumidor precisa de aplicativo para comprar. Não afirmar identificação por app, biometria ou reconhecimento facial. Não inventar equipamentos, sistemas de segurança, tecnologias de pagamento ou integrações tecnológicas não autorizadas.\n\n"
    "## COMO TRATAR TECNOLOGIA E AUTOMAÇÃO\n"
    "Ao falar sobre tecnologia no mercado autônomo, diferencie claramente o que é uma característica geral do setor daquilo que é uma característica específica do Seu Market BR. É permitido explicar como tecnologias podem ser utilizadas no mercado autônomo de maneira geral. Uma tecnologia só pode ser atribuída ao Seu Market BR se estiver explicitamente no bloco SEU_MARKET_BR_FACTS.\n\n"
    "## MENÇÕES AO SEU MARKET BR\n"
    "A empresa não precisa aparecer em todos os artigos. Se o assunto não exigir uma conexão direta com a empresa, produza o artigo exclusivamente sobre o mercado e o tema proposto. Se houver uma conexão natural, faça uma menção breve e contextualizada. Nunca repita o nome Seu Market BR artificialmente. Nunca transforme um artigo educativo em uma página de vendas. Nunca utilize frases como 'por isso, escolha o Seu Market BR' ou outras chamadas comerciais.\n\n"
    "## LINKS\n"
    "O único link permitido é https://seumarketbr.com.br. Não inserir nenhum outro link. Não inserir links para pesquisas, notícias, concorrentes, redes sociais ou sites externos. Não criar URLs fictícias.\n\n"
    "## ESTRUTURA DO ARTIGO\n"
    "O artigo deve começar apresentando o assunto de forma interessante, sem introduções genéricas. Depois, desenvolva o tema progressivamente. Utilize pelo menos 4 seções com títulos em ##. Cada seção deve acrescentar uma ideia relevante. Inclua explicações, contexto, exemplos e consequências práticas quando pertinentes. Evite repetir a mesma ideia com palavras diferentes apenas para aumentar palavras. O encerramento deve sintetizar a ideia central de maneira natural, sem 'Em conclusão' e sem transformar o final em propaganda. Não adicionar CTA. Não pedir para o leitor entrar em contato, conhecer o site, comprar, contratar ou visitar uma loja.\n\n"
    "Retorne SOMENTE o texto do artigo em markdown. Nenhum JSON, nenhuma explicação extra."
)

user_artigo = (
    f"Data atual: {today}\n"
    f"Tema: {topic}\n\n"
    f"Fatos autorizados sobre o Seu Market BR (use SOMENTE esses quando relevante, nunca invente outros):\n{SEU_MARKET_BR_FACTS}\n\n"
    "Escreva um artigo com NO MÍNIMO 1200 palavras em português do Brasil, seguindo rigorosamente todas as regras acima. "
    "Use ## para títulos de seção e **negrito** apenas para ênfase realmente necessária. "
    "Apenas parágrafos corridos, sem listas, sem traços, sem tabelas.\n\n"
    "ATENÇÃO ESPECIAL À PONTUAÇÃO: não use travessão, meia-risca nem hífen para intercalar ideias — use vírgulas. "
    "Não use *asterisco simples* em nenhuma palavra ou expressão.\n\n"
    "Antes de finalizar, verifique internamente se o texto contém alguma informação inventada sobre o Seu Market BR, "
    "alguma tecnologia não autorizada, algum número não fornecido, alguma afirmação de preço ou algum link externo. "
    "Se encontrar qualquer informação não autorizada, remova-a antes de entregar o artigo.\n\n"
    "Retorne SOMENTE o texto markdown do artigo, sem nenhum JSON ou explicação."
)

content, model_usado = chamar_api([
    {"role": "system", "content": system_artigo},
    {"role": "user", "content": user_artigo}
], max_tokens=4000)

if not content:
    print("ETAPA 2 falhou: todos os modelos truncaram ou falharam.")
    sys.exit(1)

word_count = len(content.split())
print(f"\nEtapa 2 concluída: {word_count} palavras com [{model_usado}]")


print("\n" + "=" * 60)
print("ETAPA 3: Gerando titulo e excerpt...")
print("=" * 60)

system_meta = "Você extrai metadados de artigos. Responda SOMENTE com JSON válido, sem nenhum texto fora."
user_meta = (
    f"Com base exclusivamente no artigo abaixo, gere um título atraente e um excerpt de exatamente 1 frase.\n"
    f"O título deve ser interessante, natural e relacionado diretamente ao assunto principal do artigo.\n"
    f"O excerpt deve resumir o conteúdo de forma clara e despertar interesse pela leitura, sem criar informações que não estejam presentes no artigo.\n"
    f"Não faça propaganda do Seu Market BR.\n"
    f"Artigo (primeiros 800 chars):\n{content[:800]}\n\n"
    "Responda SOMENTE com JSON válido, exatamente neste formato:\n"
    '{"title": "...", "excerpt": "..."}'
    "\nNunca inclua comentários, explicações, markdown ou qualquer outro texto fora do JSON."
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
        m = re.search(r'"title"\s*:\s*"([^"]+)"', meta_raw)
        if m:
            title = m.group(1).strip()
        m = re.search(r'"excerpt"\s*:\s*"([^"]+)"', meta_raw)
        if m:
            excerpt = m.group(1).strip()

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

reading_time = max(1, round(len(content.split()) / 200))

post = {
    "id": slug,
    "slug": slug,
    "title": title,
    "excerpt": excerpt,
    "content": content,
    "category": category,
    "author": "Seu Market BR",
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
print(f"[OK] Imagem: {cover_image[:80] if cover_image else 'sem imagem'}")
