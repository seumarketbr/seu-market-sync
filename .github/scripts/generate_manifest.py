"""Gera public/blog-posts/manifest.json com todos os slugs disponíveis."""
import os, json, glob

posts_dir = "public/blog-posts"
json_files = glob.glob(f"{posts_dir}/post-*.json")
slugs = [os.path.splitext(os.path.basename(f))[0] for f in sorted(json_files, reverse=True)]

with open(f"{posts_dir}/manifest.json", "w", encoding="utf-8") as f:
    json.dump(slugs, f, ensure_ascii=False, indent=2)

print(f"{len(slugs)} posts no manifest.")
