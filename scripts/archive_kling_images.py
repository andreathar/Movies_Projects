#!/usr/bin/env python3
"""Archive existing project image results. Never submits a generation.

Remote task queries use only the installed Kling CLI. Missing image bytes are
retrieved from the exact HTTPS asset URL returned by that CLI, without credentials.
Requires the documented renderer Python environment (Pillow).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import io
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from kling_batch import run as run_kling
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FILM = ROOT / "projects/andre-time-travel"
GENERATIONS = FILM / "07_generations"
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
TELEMETRY = ["--skill-name", "kling-cli", "--skill-version", "0.2.1"]


def relative(path):
    return path.relative_to(ROOT).as_posix()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover():
    tasks = {}
    for path in sorted((GENERATIONS / "responses").glob("*.response.json")):
        data = json.loads(path.read_text())
        body = data.get("body") or {}
        generations = body.get("generations") or [body]
        for generation in generations:
            gid = generation.get("generationId") or generation.get("generation_id")
            if gid:
                tasks[gid] = {"generationId": gid, "job": path.name.removesuffix(".response.json"),
                              "sourceResponse": relative(path), "sourceResponseSHA256": digest(path)}
    return tasks


def existing_candidates(job, index, generation_id):
    candidates = []
    for path in GENERATIONS.rglob(f"{job}_{index}.*"):
        if path.suffix.lower() not in EXTENSIONS:
            continue
        meta_path = path.with_suffix(".json")
        if not meta_path.exists():
            continue
        metadata = json.loads(meta_path.read_text())
        if metadata.get("generationId", metadata.get("generation_id")) != generation_id:
            continue
        actual_hash = digest(path)
        if metadata.get("sha256") and metadata["sha256"] != actual_hash:
            raise ValueError(f"Existing image changed since its metadata: {relative(path)}")
        candidates.append(path)
    return sorted(candidates, key=lambda p: ("originals" not in p.parts, len(p.parts), str(p)))


def inspect(path):
    with Image.open(path) as image:
        image.load()
        return {"path": relative(path), "sha256": digest(path), "bytes": path.stat().st_size,
                "width": image.width, "height": image.height, "format": image.format}


def archive_work(task, index, work, snapshot):
    candidates = existing_candidates(task["job"], index, task["generationId"])
    if candidates:
        target = candidates[0]
        result = inspect(target)
        result["retrieval"] = "already_local"
        result["otherExistingCopies"] = [relative(p) for p in candidates[1:]]
    else:
        url = work.get("url")
        parsed = urllib.parse.urlsplit(url or "")
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("No primary HTTPS image URL returned for this work")
        with urllib.request.urlopen(url, timeout=60) as response:
            payload = response.read(100 * 1024 * 1024 + 1)
        if len(payload) > 100 * 1024 * 1024:
            raise ValueError("Image exceeds the 100 MiB transfer limit")
        with Image.open(io.BytesIO(payload)) as image:
            image.load()
            extension = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}.get(image.format)
        if extension is None:
            raise ValueError("Unsupported returned image format")
        directory = GENERATIONS / "originals" / f"download-{snapshot.name}"
        directory.mkdir(exist_ok=True)
        target = directory / f"{task['job']}_{index}{extension}"
        # Exclusive creation prevents overwriting a concurrent producer's output.
        with target.open("xb") as stream:
            stream.write(payload)
        result = inspect(target)
        result["retrieval"] = "downloaded"
        metadata = {**task, **result, "workIndex": index, "provenance": "synthetic",
                    "approved": False, "urlField": "url", "downloadedAt": dt.datetime.now(dt.timezone.utc).isoformat()}
        with target.with_suffix(".json").open("x") as stream:
            json.dump(metadata, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    result.update(job=task["job"], generationId=task["generationId"], workIndex=index,
                  synthetic=True, approvalGrantedByArchive=False,
                  archivalOnly=("_quarantine-full-face" in target.parts or "rejected" in target.parts))
    return result


def build_gallery(snapshot, report):
    images = report["images"]
    cards = []
    for record in sorted(images, key=lambda r: (r["job"], r["workIndex"]), reverse=True):
        href = html.escape(os.path.relpath(ROOT / record["path"], snapshot), quote=True)
        name = html.escape(f"{record['job']} · {record['workIndex']}")
        archive = "true" if record["archivalOnly"] else "false"
        flag = "ARQUIVO / USO RESTRITO" if record["archivalOnly"] else "CANDIDATO SINTÉTICO"
        cards.append(f'<article data-search="{name.lower()}" data-archive="{archive}"><a href="{href}"><img loading="lazy" src="{href}" alt="{name}"></a><div><small>{flag}</small><h2>{name}</h2><p>{record["width"]} × {record["height"]} · {record["format"]}</p><a href="{href}" download>Baixar arquivo local</a></div></article>')
    summary = report["summary"]
    page = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Imagens Kling — Andre viajando no tempo</title><style>body{margin:0;background:#10161e;color:#edf2f7;font:16px system-ui}header,main,footer{max-width:1500px;margin:auto;padding:28px}h1{font-size:38px;margin:10px 0}p{line-height:1.6;color:#bdcbd8}a{color:#8dccff}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:20px}article{border:1px solid #384658;border-radius:10px;overflow:hidden;background:#1a2532}article img{width:100%;height:230px;object-fit:contain;background:#080d14}article div{padding:16px}h2{font-size:16px;overflow-wrap:anywhere}small{color:#e4be76}input[type=search]{background:#1a2532;border:1px solid #72849a;border-radius:7px;padding:13px;color:white;font:inherit;width:min(500px,100%)}label{display:block;margin-top:16px}article[hidden]{display:none}</style><header><small>THE TABLE BETWEEN CENTURIES · ACERVO LOCAL</small><h1>Imagens do Kling</h1>'''
    task_count = summary.get("cataloguedTasks", summary["queriedTasks"])
    page += f'<p>{summary["localImages"]} imagens de {task_count} trabalhos catalogados. {summary["downloadedImages"]} arquivos baixados neste passe; {summary["alreadyLocalImages"]} já estavam no projeto. Todos os arquivos listados foram decodificados e receberam SHA-256.</p>'
    if report["issues"]:
        page += '<p>Há ressalvas de consulta registradas no manifesto. Resultados preservados localmente continuam acessíveis; uma cópia local não comprova que a consulta atual ao provedor funcionou.</p>'
    page += '<p>Esta galeria reúne os resultados associados aos IDs registrados neste filme. Itens rejeitados ou em quarentena ficam ocultos por padrão. Arquivar uma imagem não concede aprovação de semelhança, continuidade ou uso no filme.</p><input id="search" type="search" placeholder="Filtrar: R3, galileo, session, caesar…" aria-label="Filtrar imagens"><label><input id="archive" type="checkbox"> Mostrar também rejeitados e quarentena</label><p id="count" aria-live="polite"></p></header><main class="grid">'
    page += "".join(cards)
    page += '''</main><footer><p><a href="manifest.json">Manifesto e cobertura</a> · <a href="images.csv">Catálogo CSV</a> · <a href="SHA256SUMS.txt">Integridade dos arquivos</a></p></footer><script>const search=document.querySelector('#search'),archive=document.querySelector('#archive'),cards=[...document.querySelectorAll('article')],count=document.querySelector('#count');function filter(){let shown=0;const q=search.value.trim().toLowerCase();for(const c of cards){c.hidden=!c.dataset.search.includes(q)||(!archive.checked&&c.dataset.archive==='true');if(!c.hidden)shown++;}count.textContent=shown+' imagens visíveis';}search.addEventListener('input',filter);archive.addEventListener('change',filter);filter();</script></html>'''
    (snapshot / "index.html").write_text(page)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True, help="New directory name within 07_generations/downloads")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", args.snapshot):
        parser.error("Snapshot name must contain only letters, digits, underscores and hyphens")
    snapshot = GENERATIONS / "downloads" / args.snapshot
    snapshot.mkdir(parents=True, exist_ok=False)
    tasks = discover()
    report = {"schemaVersion": "1.0", "startedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
              "scope": "All generation IDs recorded in this film's response files at scan time; not an account-wide history export",
              "accountHistoryListingAvailable": False, "paidJobsSubmitted": 0, "tasks": [], "images": [], "issues": []}
    baseline = {relative(p): digest(p) for p in GENERATIONS.rglob("*") if p.suffix.lower() in EXTENSIONS}
    (snapshot / "media-before.json").write_text(json.dumps(baseline, indent=2) + "\n")
    for number, task in enumerate(tasks.values(), 1):
        try:
            data = run_kling(["kling", "query_tasks", task["generationId"], "--quiet", *TELEMETRY], timeout=60)
            if not data.get("ok"):
                failure_body = data.get("body") or {}
                detail = failure_body.get("message") or failure_body.get("error")
                raise ValueError(str(detail or f"CLI task query failed (status {data.get('status')})"))
            body = data.get("body") or {}
            if body.get("generationId", body.get("generation_id")) != task["generationId"]:
                raise ValueError("Returned generation ID differs from the requested ID")
            works = body.get("works") or []
            current = {**task, "status": body.get("status"), "workCount": len(works), "liveQueryConfirmed": True,
                       "createTime": body.get("createTime"), "finishTime": body.get("finishTime")}
            report["tasks"].append(current)
            for index, work in enumerate(works, 1):
                if work.get("contentType", work.get("content_type")) != "image":
                    continue
                report["images"].append(archive_work(task, index, work, snapshot))
            print(json.dumps({"progress": f"{number}/{len(tasks)}", "job": task["job"], "status": current["status"], "works": len(works)}), flush=True)
        except Exception as error:
            # Avoid persisting expiring signed URLs from network exception strings.
            message = f"HTTP {error.code}" if isinstance(error, urllib.error.HTTPError) else str(error)
            message = re.sub(r"https?://\S+", "[asset URL omitted]", message)
            report["issues"].append({"job": task["job"], "error": message, "type": type(error).__name__})
            print(json.dumps({"stopped": task["job"], "error": message}), flush=True)
            break
    new_ids = set(discover()) - set(tasks)
    changed = [path for path, before in baseline.items() if not (ROOT / path).is_file() or digest(ROOT / path) != before]
    summary = {"knownTasksAtStart": len(tasks), "queriedTasks": len(report["tasks"]),
               "localImages": len(report["images"]),
               "downloadedImages": sum(r["retrieval"] == "downloaded" for r in report["images"]),
               "alreadyLocalImages": sum(r["retrieval"] == "already_local" for r in report["images"]),
               "nonCompletedTasks": [t["job"] for t in report["tasks"] if t["status"] != "COMPLETED"],
               "issues": len(report["issues"]), "newTasksDiscoveredDuringRun": sorted(new_ids),
               "preexistingMediaFiles": len(baseline), "preexistingMediaChanged": changed}
    summary["completeForKnownImageTasks"] = not (report["issues"] or summary["nonCompletedTasks"] or new_ids) and len(report["tasks"]) == len(tasks)
    report.update(summary=summary, finishedAt=dt.datetime.now(dt.timezone.utc).isoformat())
    (snapshot / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    with (snapshot / "images.csv").open("w", newline="") as stream:
        fields = ["job", "generationId", "workIndex", "path", "width", "height", "format", "bytes", "sha256", "retrieval", "archivalOnly"]
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(report["images"])
    (snapshot / "SHA256SUMS.txt").write_text("".join(f"{r['sha256']}  {r['path']}\n" for r in report["images"]))
    build_gallery(snapshot, report)
    print(json.dumps(summary, indent=2), flush=True)
    return 0 if summary["completeForKnownImageTasks"] and not changed else 2


if __name__ == "__main__":
    raise SystemExit(main())
