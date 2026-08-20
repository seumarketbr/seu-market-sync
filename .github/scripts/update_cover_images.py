"""Atualiza o coverImage dos posts existentes usando a API do Pexels."""
import os, json, urllib.request, urllib.parse, random, sys

pexels_key = os.environ.get("PEXELS_API_KEY", "")
if not pexels_key:
    print("ERRO: PEXELS_API_KEY nao definida.")
    sys.exit(1)

# Mapa: slug -> query Pexels
POSTS_TO_UPDATE = {
    "dados-de-consumo-e-mix-de-produtos-nos-minimercados-autonomos": "analytics dashboard retail store management",
    "minimercados-24h-autonomos-revolucionam-o-consumo-nos-condominios": "sustainable modern building green architecture",
    "post-2026-08-19-17": "condominium building manager professional meeting",
    "minimercados-autonomos-24h-a-revolucao-do-pix-e-do-pagamento-por-aproximacao-nos": "digital payment kiosk touchscreen technology",
}
FALLBACK_QUERY = "modern convenience store interior clean"


def buscar_imagem_pexels(query: str) -> str:
    for q in [query, FALLBACK_QUERY]:
        try:
            encoded = urllib.parse.quote(q)
            url = f"https://api.pexels.com/v1/search?query={encoded}&per_page=15&orientation=landscape"
            req = urllib.request.Request(url, headers={"Authorization": pexels_key})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                photos = data.get("photos", [])
                if photos:
                    photo = random.choice(photos)
                    img_url = (
                        photo.get("src", {}).get("large2x")
                        or photo.get("src", {}).get("large")
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

    print(f"\n[{slug[:50]}]")
    new_image = buscar_imagem_pexels(query)
    if not new_image:
        print(f"  [SKIP] Nenhuma imagem encontrada, mantendo atual.")
        continue

    old_image = post.get("coverImage", "")
    post["coverImage"] = new_image

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)

    print(f"  [OK] Atualizado!")
    print(f"  Antes: {old_image[:70]}...")
    print(f"  Depois: {new_image[:70]}...")
    updated += 1

print(f"\n{'='*50}")
print(f"Total atualizado: {updated}/{len(POSTS_TO_UPDATE)} posts")
