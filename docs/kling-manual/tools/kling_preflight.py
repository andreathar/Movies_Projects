#!/usr/bin/env python3
"""Pré-checagem OFFLINE de um request.json do projeto contra o snapshot de `kling who_am_i`.

Não chama o Kling, não faz upload, não gasta crédito. Só stdlib.
Valida o que dá para validar antes de pedir autorização de gasto ao produtor.

Uso:
  python3 -I tools/kling_preflight.py REQUEST.json [--snapshot snapshots/who_am_i.sanitized.json]
                                      [--root PROJECT_ROOT] [--allow-placeholders] [--json]

REQUEST.json = lista de jobs (ou um job):
  {job, tool, model, auth, args{...}, images[...], inputs{slot: path|url}, elements, prompt}

Saída: linhas ERROR / WARN / INFO. Código de saída: 0 sem ERROR, 1 com ERROR, 2 uso incorreto.
"""
import argparse
import json
import os
import re
import struct
import sys

MAX_BYTES = 30 * 1024 * 1024
MIN_RATIO_WARN = 0.5    # texto das ferramentas: "não mais largo que 1:2"
MIN_RATIO_ERR = 0.39    # empírico [PROJETO]: 5:2 (0,40) foi aceito como entrada de vídeo; 4:1 (0,25) foi rejeitado
MAX_SIDE = 4096          # "abaixo de 4K"
URL_RE = re.compile(r"^https?://", re.I)
PLACEHOLDER_RE = re.compile(r"^<.*>$")


def norm(name):
    return re.sub(r"[_\-\s]", "", name).lower()


def image_info(path):
    """Retorna (formato, largura, altura) lendo cabeçalho; None se não reconhecer."""
    with open(path, "rb") as f:
        head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return "PNG", w, h
        if head[:3] == b"\xff\xd8\xff":
            f.seek(2)
            while True:
                b = f.read(1)
                if not b:
                    return "JPEG", None, None
                if b != b"\xff":
                    continue
                m = f.read(1)
                while m == b"\xff":
                    m = f.read(1)
                if not m:
                    return "JPEG", None, None
                mv = m[0]
                if mv in (0xD8, 0x01) or 0xD0 <= mv <= 0xD7:
                    continue
                ln = f.read(2)
                if len(ln) < 2:
                    return "JPEG", None, None
                seglen = struct.unpack(">H", ln)[0]
                if mv in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    data = f.read(5)
                    h, w = struct.unpack(">HH", data[1:5])
                    return "JPEG", w, h
                f.seek(seglen - 2, 1)
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            return "WEBP", None, None
    return None, None, None


class Report:
    def __init__(self, job):
        self.job = job
        self.items = []

    def add(self, level, code, msg):
        self.items.append({"job": self.job, "level": level, "code": code, "msg": msg})

    def err(self, code, msg):
        self.add("ERROR", code, msg)

    def warn(self, code, msg):
        self.add("WARN", code, msg)

    def info(self, code, msg):
        self.add("INFO", code, msg)


def find_root(req_path, given):
    if given:
        return os.path.abspath(given)
    d = os.path.dirname(os.path.abspath(req_path))
    while True:
        if os.path.isdir(os.path.join(d, "02_references")):
            return d
        p = os.path.dirname(d)
        if p == d:
            return os.path.dirname(os.path.abspath(req_path))
        d = p


def resolve_local(p, root, req_dir):
    if os.path.isabs(p):
        return p
    for base in (root, req_dir, os.getcwd()):
        c = os.path.join(base, p)
        if os.path.exists(c):
            return c
    return os.path.join(root, p)


def check_media(rep, label, ref, root, req_dir, allow_ph):
    if PLACEHOLDER_RE.match(ref.strip()):
        (rep.warn if allow_ph else rep.err)("PLACEHOLDER", f"{label}: placeholder não resolvido: {ref[:80]}")
        return
    if URL_RE.match(ref):
        rep.info("URL", f"{label}: URL externa (não verifiquei o conteúdo; URLs do Kling expiram em 24 h).")
        return
    path = resolve_local(ref, root, req_dir)
    if not os.path.isfile(path):
        rep.err("FILE_MISSING", f"{label}: arquivo não encontrado: {ref}")
        return
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        rep.err("FILE_SIZE", f"{label}: {size/1e6:.1f} MB > 30 MB: {ref}")
    fmt, w, h = image_info(path)
    ext = os.path.splitext(path)[1].lower()
    if fmt is None:
        rep.warn("FILE_FORMAT", f"{label}: não reconheci como PNG/JPG (pode ser vídeo/áudio — não validado): {ref}")
        return
    if fmt not in ("PNG", "JPEG"):
        rep.err("FILE_FORMAT", f"{label}: formato {fmt} não aceito (só PNG/JPG): {ref}")
        return
    if (fmt == "PNG" and ext != ".png") or (fmt == "JPEG" and ext not in (".jpg", ".jpeg")):
        rep.warn("EXT_MISMATCH", f"{label}: extensão {ext} não bate com conteúdo {fmt}: {ref}")
    if w and h:
        if max(w, h) >= MAX_SIDE:
            rep.err("FILE_DIMS", f"{label}: {w}x{h} não está abaixo de 4K: {ref}")
        ratio = min(w, h) / max(w, h)
        if ratio < MIN_RATIO_ERR:
            rep.err("FILE_ASPECT", f"{label}: {w}x{h} (proporção {ratio:.2f}) é mais extrema que 2,5:1; entrada 4:1 já foi rejeitada: {ref}")
        elif ratio < MIN_RATIO_WARN:
            rep.warn("FILE_ASPECT", f"{label}: {w}x{h} (proporção {ratio:.2f}) passa de 1:2, limite escrito nas ferramentas; 5:2 foi aceito em vídeo no projeto, mas confirme: {ref}")
    rep.info("FILE_OK", f"{label}: {fmt} {w}x{h} {size/1e6:.2f} MB")


def parse_elements(rep, val):
    if val is None:
        return []
    if isinstance(val, str):
        try:
            val = json.loads(val)
        except ValueError:
            rep.err("ELEMENTS_JSON", "elements não é JSON válido")
            return []
    if not isinstance(val, list):
        rep.err("ELEMENTS_JSON", "elements deve ser uma lista [{id, bindName}]")
        return []
    ok = []
    for e in val:
        if not isinstance(e, dict) or "id" not in e or "bindName" not in e:
            rep.err("ELEMENTS_SHAPE", f"elemento inválido (precisa de id e bindName): {e}")
        else:
            ok.append(e)
    return ok


def check_job(job, models, root, req_dir, allow_ph):
    rep = Report(job.get("job", "?"))
    tool, model = job.get("tool"), job.get("model")
    if tool not in models:
        rep.err("TOOL", f"ferramenta '{tool}' não existe no snapshot (existentes: {', '.join(models)})")
        return rep
    cat = {m["model"]: m for m in models[tool]["models"]}
    if not model:
        rep.err("MODEL_MISSING", "model ausente — sempre explícito (nunca confie no padrão).")
        return rep
    if model not in cat:
        near = [m for m in cat if norm(m) == norm(model)]
        hint = f" (parecido: {near[0]})" if near else ""
        rep.err("MODEL", f"modelo '{model}' não existe em {tool}{hint}. Existentes: {', '.join(cat)}")
        return rep
    spec = cat[model]
    declared = {a["name"]: a for a in spec.get("arguments", [])}
    dnorm = {norm(n): n for n in declared}
    slots = spec.get("inputs", [])
    slot_names = [s["name"] for s in slots]

    if not job.get("auth"):
        rep.warn("AUTH", "sem campo 'auth' (regra do projeto: gasto exige autorização registrada, ex. D16-...).")

    # ---- argumentos
    args = dict(job.get("args") or {})
    if "prompt" in job and "prompt" not in args:
        args["prompt"] = job["prompt"]
    if "elements" in job and "elements" not in args:
        args["elements"] = job["elements"]
    given = {}
    for k, v in args.items():
        if k in declared:
            given[k] = v
        elif norm(k) in dnorm:
            real = dnorm[norm(k)]
            given[real] = v
            rep.warn("ARG_NAME", f"argumento '{k}' → o modelo declara '{real}' (CLI aceita snake/camel; o JSON bruto da API exige o nome declarado).")
        else:
            rep.err("ARG_UNKNOWN", f"argumento '{k}' não é declarado por {model}. Declarados: {', '.join(declared)}")
    for n, a in declared.items():
        if a.get("required") and n not in given:
            rep.err("ARG_REQUIRED", f"argumento obrigatório ausente: {n}")
    for n, v in given.items():
        allowed = declared[n].get("allowedValues")
        if allowed and str(v) not in allowed:
            rep.err("ARG_VALUE", f"{n}='{v}' fora dos valores permitidos {allowed}")
    prompt = str(given.get("prompt", ""))
    if not prompt.strip():
        rep.warn("PROMPT_EMPTY", "prompt vazio (permitido por alguns modelos; confirme que é intencional).")

    # ---- padrões perigosos
    for n in ("enable_audio", "prefer_multi_shots"):
        if n in declared and n not in given:
            rep.warn("DEFAULT", f"{n} não definido → vale o padrão do servidor '{declared[n].get('default')}'. Defina explicitamente.")
    for n in ("imageCount", "image_count"):
        if n in given and str(given[n]) not in ("1",):
            rep.warn("COST_MULT", f"{n}={given[n]} multiplica o custo.")
    if given.get("resolution") == "4k" or given.get("img_resolution") == "4k":
        rep.warn("COST_4K", "4K custa muito mais (~30 cr/s em vídeo). Trave o prompt em 1080p/2K antes.")

    # ---- inputs
    images = list(job.get("images") or [])
    named = dict(job.get("inputs") or {})
    mapping = {}
    for sn, ref in named.items():
        if sn not in slot_names:
            rep.err("SLOT_UNKNOWN", f"slot '{sn}' não declarado por {model}. Slots: {slot_names or 'nenhum'}")
        else:
            mapping[sn] = ref
    free = [s for s in slot_names if s not in mapping]
    if len(images) > len(free):
        rep.err("SLOT_COUNT", f"{len(images)} imagens para {len(free)} slot(s) livres ({', '.join(free) or 'nenhum'}) em {model}. "
                              "Excedentes são descartados ou rejeitados — escolha outro modelo ou reduza as referências.")
    for sn, ref in zip(free, images):
        mapping[sn] = ref
    for s in slots:
        if s.get("required") and s["name"] not in mapping:
            rep.err("SLOT_REQUIRED", f"slot obrigatório sem mídia: {s['name']}")
    for sn, ref in mapping.items():
        check_media(rep, f"slot {sn}", str(ref), root, req_dir, allow_ph)
    if not slots and (images or named):
        rep.err("SLOT_NONE", f"{model} não declara slots de input, mas o request traz mídia.")

    # ---- elements
    elems = parse_elements(rep, given.get("elements"))
    if elems:
        if "elements" not in declared:
            rep.err("ELEMENTS_UNSUPPORTED", f"{model} não declara 'elements'.")
        for e in elems:
            marker = f"<<<{e['id']}>>>"
            if marker not in prompt:
                rep.err("ELEMENT_MARKER", f"prompt não contém {marker} (bind '{e['bindName']}').")
        cap = (spec.get("elementSupport") or {}).get("maxTotalElements")
        if cap and len(elems) > cap:
            rep.err("ELEMENTS_CAP", f"{len(elems)} elements > máximo {cap}.")
    elif "<<<" in prompt:
        rep.err("ELEMENT_NOBIND", "prompt usa <<<id>>> mas 'elements' não foi enviado.")

    # ---- regras por ferramenta
    if tool == "motion_control":
        has_video = "video" in mapping
        has_motion = bool(given.get("motionId"))
        if has_video == has_motion:
            rep.err("MOTION_SOURCE", "motion_control exige exatamente UM de: input 'video' ou motionId.")
        if given.get("motionDirection") == "image_direction":
            rep.info("MOTION_DUR", "image_direction só aceita movimentos de 3 a 10 s.")
    if tool == "omni_ref_video":
        if str(given.get("enable_audio")) == "true" and str(given.get("keepOriginalSound")) == "true":
            rep.warn("OMNI_AUDIO", "enable_audio e keepOriginalSound ambos 'true' — o guia do skill diz usar só um.")
        if "audio_1" not in slot_names:
            rep.info("OMNI_AUDIO_SLOT", "o modelo não declara audio_N no who_am_i, embora o CLI aceite --audio (divergência conhecida).")
    if tool in ("image_to_video", "text_to_video") and model == "kling-video-v3_0_turbo":
        rep.info("TURBO", "Turbo: sem elements, sem áudio nativo configurável, sem multi-shot, sem tail_image.")
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("request")
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--snapshot", default=os.path.join(here, "..", "snapshots", "who_am_i.sanitized.json"))
    ap.add_argument("--root")
    ap.add_argument("--allow-placeholders", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        snap = json.load(open(a.snapshot, encoding="utf-8"))["body"]["availableModels"]
        data = json.load(open(a.request, encoding="utf-8"))
    except (OSError, ValueError, KeyError) as e:
        print(f"erro de leitura: {e}", file=sys.stderr)
        return 2
    jobs = data if isinstance(data, list) else [data]
    root = find_root(a.request, a.root)
    req_dir = os.path.dirname(os.path.abspath(a.request))
    results = []
    for j in jobs:
        results.extend(check_job(j, snap, root, req_dir, a.allow_placeholders).items)
    nerr = sum(1 for r in results if r["level"] == "ERROR")
    nwarn = sum(1 for r in results if r["level"] == "WARN")
    if a.json:
        print(json.dumps({"errors": nerr, "warnings": nwarn, "items": results}, ensure_ascii=False, indent=1))
    else:
        print(f"# preflight de {a.request}  (raiz de mídia: {root})")
        for r in results:
            print(f"{r['level']:5} [{r['job']}] {r['code']}: {r['msg']}")
        print(f"\nresultado: {nerr} ERROR, {nwarn} WARN em {len(jobs)} job(s) — "
              + ("NÃO enviar." if nerr else "ok para pedir autorização (custo NÃO estimado aqui)."))
    return 1 if nerr else 0


if __name__ == "__main__":
    sys.exit(main())
