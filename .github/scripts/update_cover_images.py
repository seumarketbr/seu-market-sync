"""Atualiza o coverImage dos posts existentes usando a API do Unsplash."""
import os, json, urllib.request, urllib.parse, random, sys

unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
if not unsplash_key:
    print("ERRO: UNSPLASH_ACCESS_KEY nao definida.")
    sys.exit(1)

# Mapa: slug -> query Unsplash
POSTS_TO_UPDATE = {
    "dados-de-consumo-e-mix-de-produtos-nos-minimercados-autonomos": "retail analytics dashboard data",
    "minimercados-24h-autonomos-revolucionam-o-consumo-nos-condominios": "sustainable modern building architecture",
    "post-2026-08-19-17": "condominium building manager professional",
    "minimercados-autonomos-24h-a-revolucao-do-pix-e-do-pagamento-por-aproximacao-nos": "digital payment touchscreen technology",
}
FALLBACK_QUERY = "convenience store interior modern"


def buscar_imagem_unsplash(query: str) -> str:
    for q in [query, FALLBACK_QUERY]:
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
                        print(f"  [OK] '{q[:50]}' -> {img_url[:70]}...")
                        return img_url
        except Exception as e:
            print(f"  [ERRO] query '{q}': {e}")
    return ""


updated = 0
for slug, query in POSTS_TO_UPDATE.items():
    filepath = f"public/blog-posts/{slug}.json"
    if not os.path.exists(filepath):
        print(f"[SKIP] {slug} - arquivo nao encontrado")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        post = json.load(f)

    print(f"\n[{slug[:55]}]")
    new_image = buscar_imagem_unsplash(query)
    if not new_image:
        print(f"  [SKIP] Nenhuma imagem encontrada, mantendo atual.")
        continue

    old_image = post.get("coverImage", "")
    post["coverImage"] = new_image

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)

    print(f"  [ATUALIZADO]")
    print(f"  Antes:  {old_image[:70]}...")
    print(f"  Depois: {new_image[:70]}...")
    updated += 1

print(f"\n{'='*50}")
print(f"Total atualizado: {updated}/{len(POSTS_TO_UPDATE)} posts")
