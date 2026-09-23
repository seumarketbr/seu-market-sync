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
- Usa slugs do manifest.json para URLs corretas
- Suporta manifest.json como lista OU dicionario
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

def load_manifest(posts_dir: Path) -> dict:
    """Carrega o manifest.json para obter slugs corretos.
    Suporta manifest como lista de slugs OU dicionario {filename: {slug:...}}.
    Retorna sempre um dicionario {filename_sem_ext: {"slug": slug}}.
    """
    manifest_path = posts_dir / "manifest.json"
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

    # Se for lista, converte para dicionario usando o slug como chave e valor
    if isinstance(raw, list):
        result = {}
        for item in raw:
            if isinstance(item, str):
                # item é o proprio slug; usa como nome de arquivo tambem
                result[item] = {"slug": item}
        return result

    # Se ja for dicionario, retorna direto
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

    # Extrair campos com fallbacks seguros
    title = data.get("title") or data.get("titulo") or ""
    if not title:
        return None
    
    description = data.get("description") or data.get("resumo") or data.get("excerpt") or title
    
    # Slug: tenta manifest primeiro, depois data.slug, depois nome do arquivo
    file_name = file_path.stem
    slug = manifest.get(file_name, {}).get("slug") or data.get("slug") or file_name
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
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def build_rss(posts: list) -> str:
    """Constroi o XML RSS 2.0 com suporte a media:content."""
    # Namespace media
    ET.register_namespace("media", "http://search.yahoo.com/mrss/")
    ET.register_namespace("atom", "http://www.w3.org/2005/Atom")

    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:media": "http://search.yahoo.com/mrss/",
        "xmlns:atom": "http://www.w3.org/2005/Atom",
    })

    channel = ET.SubElement(rss, "channel")

    # Metadados do canal
    ET.SubElement(channel, "title").text = "Seu Market BR - Blog"
    ET.SubElement(channel, "link").text = DOMAIN
    ET.SubElement(channel, "description").text = (
        "Dicas, tendencias e novidades sobre minimercados autonomos em condominios."
    )
    ET.SubElement(channel, "language").text = "pt-BR"
    ET.SubElement(channel, "lastBuildDate").text = format_rfc822(datetime.now(timezone.utc))
    ET.SubElement(channel, "generator").text = "SeuMarketBR RSS Generator"

    # Logo do canal
    image_el = ET.SubElement(channel, "image")
    ET.SubElement(image_el, "url").text = f"{DOMAIN}/logo.png"
    ET.SubElement(image_el, "title").text = "Seu Market BR"
    ET.SubElement(image_el, "link").text = DOMAIN

    # Self-referencing atom:link
    atom_link = ET.SubElement(channel, "{http://www.w3.org/2005/Atom}link")
    atom_link.set("href", f"{DOMAIN}/rss.xml")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")

    # Itens
    for post in posts:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post["title"]
        ET.SubElement(item, "link").text = post["link"]
        ET.SubElement(item, "description").text = post["description"]
        ET.SubElement(item, "guid", isPermaLink="true").text = post["link"]

        if post.get("pub_date"):
            ET.SubElement(item, "pubDate").text = format_rfc822(post["pub_date"])

        if post.get("image_url"):
            img = post["image_url"]
            # enclosure
            enc = ET.SubElement(item, "enclosure")
            enc.set("url", img)
            enc.set("type", "image/jpeg")
            enc.set("length", "0")
            # media:content
            mc = ET.SubElement(item, "{http://search.yahoo.com/mrss/}content")
            mc.set("url", img)
            mc.set("medium", "image")

    # Serializar com pretty-print
    raw = ET.tostring(rss, encoding="unicode", xml_declaration=False)
    reparsed = minidom.parseString(f'<?xml version="1.0" encoding="UTF-8"?>{raw}')
    return reparsed.toprettyxml(indent="  ", encoding=None).replace(
        '<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>'
    )


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

    # Ordenar por data (mais recentes primeiro)
    posts.sort(key=lambda p: p["pub_date"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    # Limitar a 50 itens no RSS
    posts = posts[:50]

    rss_content = build_rss(posts)

    output_path = base_dir / "public" / "rss.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rss_content)

    print(f"[OK] RSS gerado com {len(posts)} posts em {output_path}")


if __name__ == "__main__":
    main()
