#!/usr/bin/env python3
"""
RSS 2.0 generator para Pinterest / Google.
Le todos os posts em public/blog-posts/*.json e gera public/rss.xml.
- Suporta manifest.json como lista OU dicionario
- Gera XML por string para evitar atributos xmlns duplicados do ElementTree
"""

import json
from datetime import datetime, timezone
from pathlib import Path
import html as html_lib

DOMAIN = "https://seumarketbr.com.br"
BLOG_BASE = f"{DOMAIN}/blog"


def load_manifest(posts_dir: Path) -> dict:
    """Carrega manifest.json. Suporta lista de slugs OU dicionario."""
    manifest_path = posts_dir / "manifest.json"
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

    if isinstance(raw, list):
        return {item: {"slug": item} for item in raw if isinstance(item, str)}

    if isinstance(raw, dict):
        return raw

    return {}


def parse_post(file_path: Path, manifest: dict) -> dict | None:
    """Carrega um JSON de post e extrai campos essenciais."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    title = data.get("title") or data.get("titulo") or ""
    if not title:
        return None

    description = (
        data.get("description")
        or data.get("resumo")
        or data.get("excerpt")
        or title
    )

    file_name = file_path.stem
    slug = (
        manifest.get(file_name, {}).get("slug")
        or data.get("slug")
        or file_name
    )
    if slug.startswith("post-"):
        slug = slug[5:]

    link = f"{BLOG_BASE}/{slug}"
    if not link.startswith(DOMAIN):
        return None

    image_url = (
        data.get("image")
        or data.get("imageUrl")
        or data.get("cover")
        or data.get("thumbnail")
        or ""
    )
    if not image_url:
        images = data.get("images")
        if isinstance(images, list) and images:
            image_url = images[0]

    if image_url and not image_url.startswith("https://"):
        image_url = image_url.replace("http://", "https://")

    pub_date = None
    if "date" in data:
        try:
            pub_date = datetime.fromisoformat(data["date"].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            pass
    if pub_date is None:
        stem = file_path.stem.replace("post-", "")
        try:
            parts = stem.split("-")
            if len(parts) >= 4:
                dt_str = f"{parts[0]}-{parts[1]}-{parts[2]}T{parts[3]}:00:00+00:00"
                pub_date = datetime.fromisoformat(dt_str)
        except (ValueError, IndexError):
            pub_date = datetime.now(timezone.utc)

    return {
        "title": str(title),
        "description": str(description),
        "link": link,
        "image_url": str(image_url) if image_url else "",
        "pub_date": pub_date,
    }


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def esc(text: str) -> str:
    """Escapa caracteres especiais para XML."""
    return html_lib.escape(str(text), quote=False)


def build_rss(posts: list) -> str:
    """Constroi RSS 2.0 como string para evitar atributos xmlns duplicados."""
    now = fmt_date(datetime.now(timezone.utc))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0"',
        '  xmlns:media="http://search.yahoo.com/mrss/"',
        '  xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        f"    <title>Seu Market BR - Blog</title>",
        f"    <link>{DOMAIN}</link>",
        "    <description>Dicas, tendencias e novidades sobre minimercados autonomos em condominios.</description>",
        "    <language>pt-BR</language>",
        f"    <lastBuildDate>{now}</lastBuildDate>",
        "    <generator>SeuMarketBR RSS Generator</generator>",
        "    <image>",
        f"      <url>{DOMAIN}/logo.png</url>",
        "      <title>Seu Market BR</title>",
        f"      <link>{DOMAIN}</link>",
        "    </image>",
        f'    <atom:link href="{DOMAIN}/rss.xml" rel="self" type="application/rss+xml"/>',
    ]

    for post in posts:
        pub = fmt_date(post["pub_date"]) if post.get("pub_date") else now
        lines += [
            "    <item>",
            f"      <title>{esc(post['title'])}</title>",
            f"      <link>{esc(post['link'])}</link>",
            f"      <description>{esc(post['description'])}</description>",
            f"      <guid isPermaLink=\"true\">{esc(post['link'])}</guid>",
            f"      <pubDate>{pub}</pubDate>",
        ]
        if post.get("image_url"):
            img = esc(post["image_url"])
            lines += [
                f'      <enclosure url="{img}" type="image/jpeg" length="0"/>',
                f'      <media:content url="{img}" medium="image"/>',
            ]
        lines.append("    </item>")

    lines += ["  </channel>", "</rss>", ""]
    return "\n".join(lines)


def main():
    base_dir = Path(__file__).parent.parent.parent
    posts_dir = base_dir / "public" / "blog-posts"

    if not posts_dir.exists():
        print(f"[ERRO] Diretorio nao encontrado: {posts_dir}")
        return

    manifest = load_manifest(posts_dir)

    json_files = sorted(posts_dir.glob("*.json"))
    json_files = [f for f in json_files if f.name != "manifest.json"]

    posts = []
    for file_path in json_files:
        post = parse_post(file_path, manifest)
        if post:
            posts.append(post)

    posts.sort(
        key=lambda p: p["pub_date"] or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    posts = posts[:50]

    rss_content = build_rss(posts)

    output_path = base_dir / "public" / "rss.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rss_content)

    print(f"[OK] RSS gerado com {len(posts)} posts em {output_path}")


if __name__ == "__main__":
    main()
