"""Gera public/blog-posts/manifest.json com todos os slugs disponíveis (por título, não por data)."""
import os, json, glob
from datetime import datetime

posts_dir = "public/blog-posts"
json_files = glob.glob(f"{posts_dir}/*.json")

# Exclui o próprio manifest.json
json_files = [f for f in json_files if os.path.basename(f) != "manifest.json"]

# Lê data de cada post para ordenar do mais recente
posts_meta = []
for filepath in json_files:
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        slug = data.get("slug") or os.path.splitext(os.path.basename(filepath))[0]
        date = data.get("date", "1970-01-01")
        posts_meta.append({"slug": slug, "date": date})
    except Exception as e:
        print(f"Aviso: erro ao ler {filepath}: {e}")

# Ordena do mais recente para o mais antigo
posts_meta.sort(key=lambda x: x["date"], reverse=True)
slugs = [p["slug"] for p in posts_meta]

with open(f"{posts_dir}/manifest.json", "w", encoding="utf-8") as f:
    json.dump(slugs, f, ensure_ascii=False, indent=2)

print(f"{len(slugs)} posts no manifest.")
for p in posts_meta[:5]:
    print(f"  - {p['slug']} ({p['date']})")
