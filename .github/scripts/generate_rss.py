#!/usr/bin/env python3
"""
RSS 2.0 generator para Pinterest.
Le todos os posts em public/blog-posts/*.json e gera public/rss.xml.
Corrigido conforme especificacoes do Pinterest:
- RSS 2.0 (nao Atom)
- Tags <image>, <enclosure>, <media:content> por item
- <title>, <description>, <link> por item
- Links sempre sob o dominio reivindicado
- Conteudo em XML valido
- enclosure com atributo length
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Dominio oficial do site
DOMAIN = "https://seumarketbr.com.br"
BLOG_BASE = f"{DOMAIN}/blog"

def parse_post(file_path: Path) -> dict | None:
    """Carrega um JSON de post e extrai campos essenciais."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    # Extrair campos com fallbacks seguros
    title = data.get("title") or data.get("titulo") or ""
    if not title:
        return None
    
    description = data.get("description") or data.get("resumo") or data.get("excerpt") or title
    
    # Slug para URL
    slug = data.get("slug") or file_path.stem
    if slug.startswith("post-"):
        slug = slug[5:]
    
    link = f"{BLOG_BASE}/{slug}"
    
    # Validar que o link esta sob o dominio reivindicado
    if not link.startswith(DOMAIN):
        return None
    
    # Imagem de capa
    image_url = data.get("image") or data.get("imageUrl") or data.get("cover") or data.get("thumbnail") or ""
    if not image_url and "images" in data and isinstance(data["images"], list) and len(data["images"]) > 0:
        image_url = data["images"][0]
    
    # Garantir que a imagem seja HTTPS
    if image_url and not image_url.startswith("https://"):
        image_url = image_url.replace("http://", "https://")
    
    # Data de publicacao
    pub_date = None
    if "date" in data:
        try:
            pub_date = datetime.fromisoformat(data["date"].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            pass
    if pub_date is None:
        # Tentar extrair do nome do arquivo: post-2026-08-19-17.json
        match = file_path.stem.replace("post-", "")
        try:
            parts = match.split("-")
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
        "file_name": file_path.name,
    }


def format_rfc822(dt: datetime) -> str:
    """Formata data para RFC 822 (ex: Mon, 01 Jan 2024 12:00:00 +0000)."""
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


def generate_rss(posts: list[dict], output_path: Path) -> None:
    """Gera o arquivo RSS 2.0 com todos os posts."""
    # Ordenar do mais antigo para o mais recente (Pinterest publica mais antigo primeiro)
    posts_sorted = sorted(posts, key=lambda p: p["pub_date"] or datetime.min.replace(tzinfo=timezone.utc))

    # Elemento raiz rss
    rss = ET.Element("rss")
    rss.set("version", "2.0")
    rss.set("xmlns:media", "http://search.yahoo.com/mrss/")

    # Canal
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Seu Market BR - Blog"
    ET.SubElement(channel, "link").text = DOMAIN
    ET.SubElement(channel, "description").text = "Conteudo sobre minimercado autonomo e tecnologia"
    ET.SubElement(channel, "language").text = "pt-br"
    ET.SubElement(channel, "lastBuildDate").text = format_rfc822(datetime.now(timezone.utc))

    # Itens
    for post in posts_sorted:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post["title"]
        ET.SubElement(item, "description").text = post["description"]
        link_elem = ET.SubElement(item, "link")
        link_elem.text = post["link"]
        ET.SubElement(item, "guid", isPermaLink="true").text = post["link"]
        ET.SubElement(item, "pubDate").text = format_rfc822(post["pub_date"])

        # Imagem via <image> (dentro do item)
        if post["image_url"]:
            image_elem = ET.SubElement(item, "image")
            image_elem.text = post["image_url"]
            
            # enclosure com length (obrigatorio RSS 2.0)
            enclosure = ET.SubElement(item, "enclosure")
            enclosure.set("url", post["image_url"])
            enclosure.set("type", "image/jpeg" if post["image_url"].lower().endswith((".jpg", ".jpeg")) else "image/png")
            enclosure.set("length", "0")  # Pinterest nao usa length, mas RSS exige

            # media:content
            media_content = ET.SubElement(item, "{http://search.yahoo.com/mrss/}content")
            media_content.set("url", post["image_url"])
            media_content.set("medium", "image")

    # Serializar XML
    xml_str = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    # Pretty print
    dom = minidom.parseString(xml_str.decode("utf-8"))
    pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    # Escrever arquivo
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)


def main():
    # Diretorios relativos a raiz do repositorio
    repo_root = Path(__file__).resolve().parent.parent.parent
    posts_dir = repo_root / "public" / "blog-posts"
    output_file = repo_root / "public" / "rss.xml"

    # Coletar todos os posts
    posts = []
    for file_path in sorted(posts_dir.glob("*.json")):
        if file_path.name == "manifest.json":
            continue
        post = parse_post(file_path)
        if post:
            posts.append(post)

    if not posts:
        print("Nenhum post encontrado.")
        return

    generate_rss(posts, output_file)
    print(f"RSS gerado com {len(posts)} posts: {output_file}")


if __name__ == "__main__":
    main()
