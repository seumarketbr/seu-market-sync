#!/usr/bin/env python3
"""
RSS 2.0 generator para Pinterest.
LÃª todos os posts em public/blog-posts/*.json e gera public/rss.xml.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from xml.dom import minidom

DOMAIN = "https://seumarketbr.com.br"
BLOG_BASE = f"{DOMAIN}/blog"

def parse_post(file_path: Path) -> dict | None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    title = data.get("title") or data.get("titulo") or file_path.stem
    description = data.get("description") or data.get("resumo") or data.get("excerpt") or title
    
    slug = data.get("slug") or file_path.stem
    if slug.startswith("post-"):
        slug = slug[5:]
    
    link = f"{BLOG_BASE}/{slug}"
    
    image_url = (
        data.get("image")
        or data.get("imageUrl")
        or data.get("cover")
        or data.get("coverImage")
        or data.get("thumbnail")
        or ""
    )
    if not image_url and "images" in data and isinstance(data["images"], list) and len(data["images"]) > 0:
        image_url = data["images"][0]
    
    pub_date = None
    if "date" in data:
        try:
            pub_date = datetime.fromisoformat(data["date"].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            pass
    if pub_date is None:
        match = file_path.stem.replace("post-", "")
        try:
            parts = match.split("-")
            if len(parts) >= 4:
                dt_str = f"{parts[0]}-{parts[1]}-{parts[2]}T{parts[3]}:00:00+00:00"
                pub_date = datetime.fromisoformat(dt_str)
        except (ValueError, IndexError):
            pub_date = datetime.now(timezone.utc)

    if pub_date.tzinfo is None:
        pub_date = pub_date.replace(tzinfo=timezone.utc)

    return {
        "title": str(title),
        "description": str(description),
        "link": link,
        "image_url": str(image_url) if image_url else "",
        "pub_date": pub_date,
        "file_name": file_path.name,
    }

def format_rfc822(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

def generate_rss(posts: list[dict], output_path: Path) -> None:
    posts_sorted = sorted(posts, key=lambda p: p["pub_date"] or datetime.min.replace(tzinfo=timezone.utc))

    rss = ET.Element("rss")
    rss.set("version", "2.0")
    rss.set("xmlns:media", "http://search.yahoo.com/mrss/")

    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Seu Market BR - Blog"
    ET.SubElement(channel, "link").text = DOMAIN
    ET.SubElement(channel, "description").text = "Conteúdo sobre minimercado autônomo e tecnologia"
    ET.SubElement(channel, "language").text = "pt-br"
    ET.SubElement(channel, "lastBuildDate").text = format_rfc822(datetime.now(timezone.utc))

    for post in posts_sorted:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post["title"]
        ET.SubElement(item, "description").text = post["description"]
        ET.SubElement(item, "link").text = post["link"]
        ET.SubElement(item, "guid", isPermaLink="true").text = post["link"]
        ET.SubElement(item, "pubDate").text = format_rfc822(post["pub_date"])

        if post["image_url"]:
            image_url_parts = urlparse(post["image_url"])
            image_path = image_url_parts.path.lower()
            image_query = image_url_parts.query.lower()
            image_type = (
                "image/jpeg"
                if image_path.endswith((".jpg", ".jpeg")) or "fm=jpg" in image_query
                else "image/png"
            )

            enclosure = ET.SubElement(item, "enclosure")
            enclosure.set("url", post["image_url"])
            enclosure.set("type", image_type)

            media_content = ET.SubElement(item, "{http://search.yahoo.com/mrss/}content")
            media_content.set("url", post["image_url"])
            media_content.set("medium", "image")

    xml_str = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    dom = minidom.parseString(xml_str.decode("utf-8"))
    pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    posts_dir = repo_root / "public" / "blog-posts"
    output_file = repo_root / "public" / "rss.xml"

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
