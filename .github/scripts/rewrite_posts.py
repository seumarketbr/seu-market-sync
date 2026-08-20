import os, json, urllib.request, urllib.error, urllib.parse, sys, re, glob
from datetime import datetime, timezone

api_key = os.environ["OPENROUTER_API_KEY"]

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
                "X-Title": "Seu Market Blog Rewrite"
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


system_artigo = (
    "Você é o redator editorial do blog do **Seu Market BR**, uma empresa brasileira que atua no segmento de minimercados autônomos em condomínios.\n\n"
    "Sua principal missão é produzir conteúdos informativos, educativos e relevantes sobre o mercado de minimercados autônomos, conveniência, varejo autônomo, comportamento do consumidor, novas formas de comprar, operação de pequenos pontos de venda, tecnologia aplicada ao varejo e transformação da experiência de compra em condomínios brasileiros.\n\n"
    "O artigo NÃO deve ser tratado como uma propaganda do Seu Market BR. A prioridade é construir autoridade sobre o mercado autônomo como categoria, explicando conceitos, tendências, comportamentos, desafios, oportunidades e mudanças que esse modelo representa para consumidores, condomínios e para o varejo.\n\n"
    "O Seu Market BR pode aparecer naturalmente quando houver relação direta com o assunto, mas nunca deve ser forçado dentro do texto. A prioridade é falar sobre o mercado autônomo, e não sobre o que o Seu Market BR possui.\n\n"
    "REGRAS ABSOLUTAS DE FORMATAÇÃO:\n"
    "NUNCA usar bullet points. NUNCA usar listas numeradas. NUNCA usar listas com traços. NUNCA criar tabelas.\n"
    "O conteúdo deve ser formado exclusivamente por parágrafos corridos.\n"
    "Use ## para todos os títulos de seção. Utilize no mínimo 4 seções. Jamais utilize ### ou ####.\n"
    "Utilize negrito somente quando realmente contribuir para destacar uma informação importante.\n"
    "O artigo deve ter no mínimo 1200 palavras. Escreva 100% em português do Brasil.\n\n"
    "TOM E ESTILO:\n"
    "Texto com tom humano, linguagem natural, direta e fácil. Sem 'Além disso', 'Em conclusão', 'Outrossim'. Varie ritmo e estrutura. Exemplos hipotéticos apresentados claramente como exemplos.\n\n"
    "REGRA DE VERACIDADE:\n"
    "NUNCA invente números, estatísticas, percentuais, quantidades de unidades, clientes, faturamento ou crescimento. NUNCA invente tecnologias, equipamentos ou funcionalidades do Seu Market BR. NUNCA atribua à empresa informações que não estejam no bloco SEU_MARKET_BR_FACTS.\n\n"
    "O QUE NÃO AFIRMAR SOBRE O SEU MARKET BR:\n"
    "Não afirmar número de unidades, condomínios, clientes, faturamento, crescimento. Não afirmar que produtos são mais baratos. Não afirmar aplicativo de compras, identificação por app, biometria ou reconhecimento facial. Não inventar equipamentos, sistemas de segurança ou tecnologias não autorizadas.\n\n"
    "LINKS: O único link permitido é https://seumarketbr.com.br. Nenhum outro link.\n\n"
    "ESTRUTURA: Começar com assunto de forma interessante, sem introduções genéricas. Pelo menos 4 seções ##. Encerramento natural sem CTA, sem pedir contato, sem propaganda.\n\n"
    "Retorne SOMENTE o texto do artigo em markdown. Nenhum JSON, nenhuma explicação extra."
)

system_meta = "Você extrai metadados de artigos. Responda SOMENTE com JSON válido, sem nenhum texto fora."


def reescrever_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        post = json.load(f)

    slug = post.get("slug", "")
    title_original = post.get("title", "")
    topic = post.get("title", "")  # usa o titulo original como tema
    today = post.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    category = post.get("category", "Como funciona")
    tags = post.get("tags", ["mercado autônomo", "condomínio"])
    cover_image = post.get("coverImage", "")

    print(f"\n{'=' * 60}")
    print(f"Reescrevendo: {slug}")
    print(f"Tema: {topic}")
    print("=" * 60)

    user_artigo = (
        f"Data atual: {today}\n"
        f"Tema: {topic}\n\n"
        f"Fatos autorizados sobre o Seu Market BR (use SOMENTE esses quando relevante, nunca invente outros):\n{SEU_MARKET_BR_FACTS}\n\n"
        "Escreva um artigo com NO MÍNIMO 1200 palavras em português do Brasil, seguindo rigorosamente todas as regras acima. "
        "Use ## para títulos de seção e **negrito** apenas para ênfase realmente necessária. "
        "Apenas parágrafos corridos, sem listas, sem traços, sem tabelas.\n\n"
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
        print(f"  FALHA ao reescrever {slug}, mantendo original.")
        return False

    content = re.sub(
        r'\[([^\]]+)\]\((?!https://seumarketbr\.com\.br)[^)]+\)',
        r'\1',
        content
    )

    user_meta = (
        f"Com base exclusivamente no artigo abaixo, gere um título atraente e um excerpt de exatamente 1 frase.\n"
        f"O título deve ser interessante, natural e relacionado diretamente ao assunto principal do artigo.\n"
        f"O excerpt deve resumir o conteúdo de forma clara e despertar interesse pela leitura.\n"
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

    new_title = title_original
    new_excerpt = post.get("excerpt", "")

    if meta_raw:
        try:
            meta = json.loads(meta_raw)
            new_title = meta.get("title", "").strip() or title_original
            new_excerpt = meta.get("excerpt", "").strip() or new_excerpt
        except Exception:
            m = re.search(r'"title"\s*:\s*"([^"]+)"', meta_raw)
            if m:
                new_title = m.group(1).strip()
            m = re.search(r'"excerpt"\s*:\s*"([^"]+)"', meta_raw)
            if m:
                new_excerpt = m.group(1).strip()

    reading_time = max(1, round(len(content.split()) / 200))

    post["title"] = new_title
    post["excerpt"] = new_excerpt
    post["content"] = content
    post["readingTime"] = reading_time

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)

    print(f"  [OK] {slug} reescrito com {len(content.split())} palavras via [{model_usado}]")
    return True


files = sorted(glob.glob("public/blog-posts/*.json"))
files = [f for f in files if not os.path.basename(f).startswith("manifest")]

if not files:
    print("Nenhum post encontrado em public/blog-posts/. Encerrando.")
    sys.exit(0)

print(f"Posts encontrados: {len(files)}")
success = 0
failed = 0

for filepath in files:
    ok = reescrever_post(filepath)
    if ok:
        success += 1
    else:
        failed += 1

print(f"\n{'=' * 60}")
print(f"Reescrita concluída: {success} OK, {failed} falhas.")
if failed > 0:
    print("Posts com falha mantiveram o conteúdo original.")
