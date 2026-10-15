#!/usr/bin/env python3
"""Verify the local Andre Instagram import and build a photo gallery.

Read-only for imported media. Does not contact Instagram, handle authentication,
generate images, or grant creative approval. Run from the workspace root.
"""

import csv
import hashlib
import html
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "inbox/andre-reference-photos/instagram-andreathar"
OUTPUT = ROOT / "inbox/instagram-andreathar/2026-10-09-chrome"


def relative(path):
    return path.relative_to(ROOT).as_posix()


def main():
    evidence = json.loads((OUTPUT / "browser-verification.json").read_text())
    carousel_ids = {row["id"] for row in evidence["carousels"]}
    catalog = SOURCE / "CATALOG.md"
    rows = []
    for line in catalog.read_text().splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) < 5 or not re.fullmatch(r"[A-Za-z0-9_-]{10,11}", cells[0]):
            continue
        rows.append({"id": cells[0], "dateAsCatalogued": cells[1],
                     "filename": cells[2], "mediaType": "photo" if cells[-1] == "yes" else "video"})

    posts = {}
    for row in rows:
        code, kind = row["id"], row["mediaType"]
        post = posts.setdefault(code, {
            "id": code, "mediaType": kind, "carousel": code in carousel_ids,
            "sourceUrl": f"https://www.instagram.com/andreathar/{'p' if kind == 'photo' else 'reel'}/{code}/",
            "dateAsCatalogued": row["dateAsCatalogued"], "files": [],
        })
        if row["filename"]:
            post["files"].append(relative(SOURCE / row["filename"]))

    text = "\n".join(sorted(f"{p['id']}|{p['mediaType']}|{str(p['carousel']).lower()}" for p in posts.values()))
    fingerprint = 2166136261
    for character in text:
        fingerprint = ((fingerprint ^ ord(character)) * 16777619) & 0xFFFFFFFF
    if len(text) != evidence["setComparison"]["textLength"] or f"{fingerprint:x}" != evidence["setComparison"]["fingerprint"]:
        raise ValueError("Local catalog differs from the observed browser inventory; review before rebuilding")
    if len(posts) != evidence["uniqueObservedPostLinks"]:
        raise ValueError("Post count mismatch")

    expected = {row["filename"] for row in rows if row["filename"]}
    actual = {p.name for p in SOURCE.iterdir() if p.suffix.lower() in {".jpg", ".mp4"} and p.name != "profile-picture.jpg"}
    if expected != actual:
        raise ValueError(f"Media/catalog mismatch: missing={expected-actual}, unlisted={actual-expected}")

    media = []
    row_by_name = {row["filename"]: row for row in rows if row["filename"]}
    for path in sorted(SOURCE.iterdir()):
        if path.suffix.lower() not in {".jpg", ".mp4"}:
            continue
        row = row_by_name.get(path.name)
        item = {"path": relative(path), "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "kind": "profile_picture" if row is None else row["mediaType"],
                "postId": row["id"] if row else None,
                "dateAsCatalogued": row["dateAsCatalogued"] if row else None,
                "sourceUrl": posts[row["id"]]["sourceUrl"] if row else evidence["profile"],
                "creativeApproval": "unapproved", "authenticityReview": "not_performed"}
        if path.suffix.lower() == ".jpg":
            with Image.open(path) as image:
                image.load()
                item.update(width=image.width, height=image.height, format=image.format, decoded=True)
        else:
            item["playbackVerified"] = False
        media.append(item)

    photo_files = [m for m in media if m["kind"] == "photo"]
    missing_photos = [p["id"] for p in posts.values() if p["mediaType"] == "photo" and not p["files"]]
    for carousel in evidence["carousels"]:
        if len(posts[carousel["id"]]["files"]) != carousel["slidesViewed"]:
            raise ValueError("Carousel file count differs from browser review")
    summary = {"observedPosts": len(posts), "photoPosts": sum(p["mediaType"] == "photo" for p in posts.values()),
               "postPhotoFiles": len(photo_files), "profilePictureFiles": sum(m["kind"] == "profile_picture" for m in media),
               "existingVideoFiles": sum(m["kind"] == "video" for m in media),
               "missingPhotoPosts": missing_photos,
               "videoPostsWithoutFile": [p["id"] for p in posts.values() if p["mediaType"] == "video" and not p["files"]],
               "photoGridDownloadComplete": not missing_photos,
               "uniqueImageHashes": len({m["sha256"] for m in media if m["kind"] != "video"}),
               "mediaBytes": sum(m["bytes"] for m in media)}
    result = {"schemaVersion": "1.0", "verifiedAt": datetime.now(timezone.utc).isoformat(),
              "scope": evidence["scope"], "accountExportComplete": False,
              "sourceCatalog": relative(catalog), "sourceCatalogSHA256": hashlib.sha256(catalog.read_bytes()).hexdigest(),
              "browserEvidence": relative(OUTPUT / "browser-verification.json"),
              "provenanceNote": "Existing concurrent import, independently reconciled with the authenticated profile grid. Files are Instagram-served copies, not certified camera originals.",
              "summary": summary, "posts": list(posts.values()), "media": media}
    (OUTPUT / "manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    with (OUTPUT / "photos.csv").open("w", newline="") as stream:
        fields = ["postId", "dateAsCatalogued", "kind", "path", "sourceUrl", "width", "height", "bytes", "sha256", "creativeApproval"]
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(m for m in media if m["kind"] != "video")
    (OUTPUT / "SHA256SUMS.txt").write_text("".join(f"{m['sha256']}  {m['path']}\n" for m in media))

    cards = []
    for m in sorted(photo_files, key=lambda m: (m["dateAsCatalogued"], m["path"]), reverse=True):
        src = html.escape(os.path.relpath(ROOT / m["path"], OUTPUT), quote=True)
        date = html.escape(m["dateAsCatalogued"])
        code = html.escape(m["postId"])
        cards.append(f'<article data-search="{date} {code}"><a href="{src}"><img loading="lazy" src="{src}" alt="Foto do post {code}"></a><div><b>{date}</b><p>{code} · {m["width"]} × {m["height"]}</p><a href="{html.escape(m["sourceUrl"], quote=True)}" target="_blank" rel="noopener">Abrir publicação</a></div></article>')
    page = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fotos de Andre — acervo do Instagram</title>
<style>body{margin:0;background:#10151b;color:#eef2f6;font:16px system-ui,sans-serif}header,main,footer{max-width:1400px;margin:auto;padding:28px}h1{font-size:38px;margin:8px 0}p{line-height:1.6;color:#c5ced8}a{color:#85c7ff}.label{color:#f1c477;font-size:13px;letter-spacing:2px}input{box-sizing:border-box;width:min(100%,560px);padding:14px;border:1px solid #607083;border-radius:8px;background:#19222c;color:white;font:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}article{background:#1b2530;border-radius:10px;overflow:hidden}article img{width:100%;height:240px;object-fit:contain;background:#080c11}article div{padding:15px}article p{font-size:13px;margin:7px 0}article[hidden]{display:none}</style>
<header><div class="label">ANDRE VIAJANDO NO TEMPO · ACERVO LOCAL</div><h1>Fotografias do Instagram</h1><p><strong>289 imagens de 286 publicações</strong>, incluindo todos os slides dos dois carrosséis. Perfil verificado: 353 publicações, sendo 67 de vídeo. A foto de perfil está catalogada separadamente. Nenhuma referência foi aprovada automaticamente.</p><p>Arquivos preservados como recebidos do Instagram. As datas são as registradas pelo catálogo da importação e podem diferir do dia mostrado em outro fuso horário. Este acervo cobre as fotos publicadas no perfil; não inclui stories, destaques ou conteúdo arquivado.</p><input id="search" type="search" placeholder="Filtrar por ano, data ou código do post" aria-label="Filtrar fotografias"><p id="count" aria-live="polite">289 imagens</p></header><main class="grid">'''
    page += "".join(cards)
    page += '''</main><footer><p>Fontes e integridade: <a href="manifest.json">manifesto completo</a> · <a href="photos.csv">planilha CSV</a> · <a href="SHA256SUMS.txt">verificação de arquivos</a> · <a href="browser-verification.json">conferência no navegador</a></p></footer><script>const input=document.querySelector('#search'),cards=[...document.querySelectorAll('article')],count=document.querySelector('#count');input.addEventListener('input',()=>{const query=input.value.trim().toLowerCase();let shown=0;for(const card of cards){card.hidden=!card.dataset.search.toLowerCase().includes(query);if(!card.hidden)shown++;}count.textContent=shown+' imagens';});</script></html>'''
    (OUTPUT / "index.html").write_text(page)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
