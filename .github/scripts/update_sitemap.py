import os, json, re, unicodedata
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

BASE_URL = "https://seumarketbr.com.br"
BLOG_DIR = "public/blog-posts"
SITEMAP_PATH = "public/sitemap.xml"
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Páginas estáticas do site
STATIC_PAGES = [
    {"loc": "/",           "priority": "1.0", "changefreq": "weekly"},
    {"loc": "/blog",       "priority": "0.9", "changefreq": "daily"},
    {"loc": "/sobre",      "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/contato",    "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/modelos",    "priority": "0.8", "changefreq": "monthly"},
]

urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# Páginas estáticas
for page in STATIC_PAGES:
    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = BASE_URL + page["loc"]
    SubElement(url, "lastmod").text = today
    SubElement(url, "changefreq").text = page["changefreq"]
    SubElement(url, "priority").text = page["priority"]

# Posts do blog
posts = []
for fname in os.listdir(BLOG_DIR):
    if not fname.endswith(".json") or fname.startswith(".") or fname == "manifest.json":
        continue
    try:
        with open(os.path.join(BLOG_DIR, fname), encoding="utf-8") as f:
            data = json.load(f)
        slug = data.get("slug") or fname.replace(".json", "")
        date = data.get("date", today)
        posts.append((date, slug))
    except Exception as e:
        print(f"Aviso: não foi possível ler {fname}: {e}")

# Ordena do mais recente para o mais antigo
posts.sort(key=lambda x: x[0], reverse=True)

for date, slug in posts:
    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = f"{BASE_URL}/blog/{slug}"
    SubElement(url, "lastmod").text = date
    SubElement(url, "changefreq").text = "monthly"
    SubElement(url, "priority").text = "0.8"

# Gera XML formatado
xml_str = minidom.parseString(tostring(urlset, encoding="unicode")).toprettyxml(indent="  ")
# Remove a linha <?xml ... ?> do toprettyxml e substitui pela versão correta
lines = xml_str.split("\n")
lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
xml_final = "\n".join(lines)

os.makedirs("public", exist_ok=True)
with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
    f.write(xml_final)

print(f"sitemap.xml gerado com {len(STATIC_PAGES)} páginas estáticas + {len(posts)} posts")
print(f"Salvo em: {SITEMAP_PATH}")
