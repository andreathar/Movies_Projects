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
import math
import subprocess

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


def video_facts(path):
    """Probe a local file only. No provider, URL fetch, model or download."""
    result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                             '-show_streams', '-show_format', '-of', 'json', path],
                            capture_output=True, text=True, timeout=30, check=True)
    data = json.loads(result.stdout)
    stream = data['streams'][0]
    numerator, denominator = stream['avg_frame_rate'].split('/')
    return {'durationSeconds': float(data['format']['duration']),
            'width': stream['width'], 'height': stream['height'],
            'fps': float(numerator) / float(denominator), 'bytes': os.path.getsize(path)}


def check_media(rep, label, ref, root, req_dir, allow_ph, *, video=False, image_tool=False):
    if PLACEHOLDER_RE.match(ref.strip()):
        (rep.warn if allow_ph else rep.err)("PLACEHOLDER", f"{label}: placeholder não resolvido: {ref[:80]}")
        return
    if URL_RE.match(ref):
        rep.info("URL", f"{label}: URL externa (não verifiquei o conteúdo; URLs podem expirar; prazo não verificado).")
        return
    path = resolve_local(ref, root, req_dir)
    if not os.path.isfile(path):
        rep.err("FILE_MISSING", f"{label}: arquivo não encontrado: {ref}")
        return
    size = os.path.getsize(path)
    if video:
        if os.path.splitext(path)[1].lower() not in ('.mp4', '.mov'):
            rep.err('VIDEO_FORMAT', f'{label}: vídeo MP4/MOV obrigatório.')
        return
    if size > MAX_BYTES:
        rep.err("FILE_SIZE", f"{label}: {size/1e6:.1f} MB > 30 MB: {ref}")
    fmt, w, h = image_info(path)
    ext = os.path.splitext(path)[1].lower()
    if fmt is None:
        rep.err("FILE_FORMAT", f"{label}: slot de imagem requer PNG/JPG; arquivo não reconhecido: {ref}")
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
        if ratio < MIN_RATIO_ERR and image_tool:
            rep.warn("FILE_ASPECT", f"{label}: {w}x{h} (proporção {ratio:.2f}); em ferramenta de imagem 4:1 foi aceito [PROJETO] (R2-J02..J06 geraram 4128x1024), mas o limite escrito é 1:2: {ref}")
        elif ratio < MIN_RATIO_ERR:
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
        if not isinstance(e, dict) or any(not isinstance(e.get(k), str) or not e[k].strip() for k in ("id", "bindName")):
            rep.err("ELEMENTS_SHAPE", f"elemento inválido (precisa de id e bindName): {e}")
        else:
            ok.append(e)
    if len({e["id"] for e in ok}) != len(ok):
        rep.err("ELEMENT_DUPLICATE", "Cada Element deve aparecer uma vez na lista de vínculos.")
    return ok


def cli_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def media_mapping(job, spec, rep):
    """Mesmo mapeamento usado pelo runner; nunca descarta uma entrada."""
    names = [s["name"] for s in spec.get("inputs", [])]
    named, images = job.get("inputs") or {}, job.get("images") or []
    if not isinstance(named, dict) or not isinstance(images, list):
        rep.err("INPUT_SHAPE", "inputs deve ser objeto e images deve ser lista.")
        return {}
    if named and images:
        rep.err("INPUT_MIX", "Use somente inputs nomeados ou images; não misture os formatos.")
    if named and job.get("tool") not in {"image_to_video", "omni_ref_video", "motion_control"}:
        rep.err("NAMED_UNSUPPORTED", "Este comando do CLI não aceita inputs nomeados; use images.")
    mapping = dict(named)
    if job.get("tool") == "image_to_video":
        free = [n for n in names if n not in {"tail_image", "tailImage"}]
    elif job.get("tool") == "motion_control":
        free = [n for n in names if n == "image"]
    elif job.get("tool") == "omni_ref_video":
        free = [f"image_{i+1}" for i in range(len(images))]
    else:
        free = names
    if len(images) > len(free):
        rep.err("SLOT_COUNT", "Imagens excedem os slots não terminais; use inputs para vídeo/cauda.")
    for n, ref in zip(free, images):
        if n in mapping:
            rep.err("SLOT_DUPLICATE", f"slot repetido: {n}")
        mapping[n] = ref
    for n, ref in mapping.items():
        if n not in names:
            rep.err("SLOT_UNKNOWN", f"slot não declarado: {n}")
        if not isinstance(ref, str) or not ref.strip():
            rep.err("INPUT_VALUE", f"slot {n}: caminho ou URL não vazio obrigatório.")
    for slot in spec.get("inputs", []):
        if slot.get("required") and slot["name"] not in mapping:
            rep.err("SLOT_REQUIRED", f"slot obrigatório sem mídia: {slot['name']}")
    return mapping


def check_job(job, models, root, req_dir, allow_ph):
    rep = Report(job.get("job", "?") if isinstance(job, dict) else "?")
    if not isinstance(job, dict):
        rep.err("JOB_SHAPE", "job deve ser um objeto.")
        return rep
    if job.get("submissionBlocked"):
        rep.err("PLAN_BLOCKED", "Plano bloqueado: " + str(job["submissionBlocked"]))
    auth = job.get("auth")
    if auth and (not isinstance(auth, str) or re.search(r"REPLACE|PLACEHOLDER|<.*>|PENDING", auth, re.I)):
        rep.err("AUTH_PLACEHOLDER", "auth contém placeholder; exige referência real e escopo conferido pelo produtor.")
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
    if not isinstance(job.get("args", {}), dict):
        rep.err("ARGS_SHAPE", "args deve ser um objeto.")
        return rep
    args = dict(job.get("args") or {})
    for field in ("prompt", "elements"):
        if field in job and field in args and cli_value(job[field]) != cli_value(args[field]):
            rep.err("ARG_CONFLICT", f"{field}: valores diferentes no topo e em args.")
    if "prompt" in job and "prompt" not in args:
        args["prompt"] = job["prompt"]
    if "elements" in job and "elements" not in args:
        args["elements"] = job["elements"]
    given = {}
    for k, v in args.items():
        if not isinstance(k, str) or v is None or isinstance(v, dict):
            rep.err("ARG_TYPE", "Argumento inválido: nome string e valor não nulo obrigatórios.")
            continue
        canonical = k if k in declared else dnorm.get(norm(k))
        if canonical in given:
            rep.err("ARG_DUPLICATE", f"Argumento duplicado por alias: {k}")
        if k in declared:
            given[k] = v
        elif norm(k) in dnorm:
            real = dnorm[norm(k)]
            given[real] = v
            rep.warn("ARG_NAME", f"argumento '{k}' → o modelo declara '{real}' (o runner normaliza para o nome declarado; use esse nome no CLI direto).")
        else:
            rep.err("ARG_UNKNOWN", f"argumento '{k}' não é declarado por {model}. Declarados: {', '.join(declared)}")
    for n, a in declared.items():
        if a.get("required") and n not in given:
            rep.err("ARG_REQUIRED", f"argumento obrigatório ausente: {n}")
    for n, v in given.items():
        allowed = declared[n].get("allowedValues")
        if allowed and cli_value(v) not in [cli_value(x) for x in allowed]:
            rep.err("ARG_VALUE", f"{n}='{v}' fora dos valores permitidos {allowed}")
    prompt = str(given.get("prompt", ""))
    if not prompt.strip():
        rep.warn("PROMPT_EMPTY", "prompt vazio (permitido por alguns modelos; confirme que é intencional).")

    # ---- padrões perigosos
    for n in ("enable_audio", "prefer_multi_shots", "keepOriginalSound"):
        if n in declared and n not in given:
            rep.warn("DEFAULT", f"{n} não definido → vale o padrão do servidor '{declared[n].get('default')}'. Defina explicitamente.")
    for n in ("imageCount", "image_count"):
        if n in given and str(given[n]) not in ("1",):
            rep.warn("COST_MULT", f"{n}={given[n]} multiplica o custo.")
    if given.get("resolution") == "4k" or given.get("img_resolution") == "4k":
        rep.warn("COST_4K", "4K altera o custo. Exige estimativa identificada e escopo aprovado; não há cotação nesta checagem.")

    # ---- inputs
    mapping = media_mapping(job, spec, rep)
    for sn, ref in mapping.items():
        if isinstance(ref, str) and ref.strip():
            check_media(rep, f"slot {sn}", ref, root, req_dir, allow_ph, video=sn.startswith('video'),
                        image_tool=str(job.get('tool', '')).endswith('_image'))
    caps = ([spec['combinedItemCap']] if spec.get('combinedItemCap') else []) + spec.get('combinedItemCaps', [])
    for cap in caps:
        try:
            present = lambda prefixes: any(n.startswith(prefix) for n in mapping for prefix in prefixes)
            if cap.get('whenAnyInputPrefixes') and not present(cap['whenAnyInputPrefixes']):
                continue
            if cap.get('whenNoneInputPrefixes') and present(cap['whenNoneInputPrefixes']):
                continue
            count = sum(any(n.startswith(p) for p in cap["inputPrefixes"]) for n in mapping)
            for n in cap["arguments"]:
                val = given.get(n, [])
                val = json.loads(val) if isinstance(val, str) else val
                if not isinstance(val, list):
                    raise ValueError("esperada lista")
                count += len(val)
            if count > cap["maxItems"]:
                rep.err("COMBINED_CAP", f"{count} referências > limite combinado {cap['maxItems']}.")
        except (ValueError, KeyError, TypeError):
            rep.err("COMBINED_SCHEMA", "combinedItemCap ou argumento de lista inválido; não assumir compatibilidade.")

    # ---- elements
    elems = parse_elements(rep, given.get("elements"))
    if elems:
        if "elements" not in declared:
            rep.err("ELEMENTS_UNSUPPORTED", f"{model} não declara 'elements'.")
        for e in elems:
            marker = f"<<<{e['id']}>>>"
            if marker not in prompt:
                rep.err("ELEMENT_MARKER", f"prompt não contém {marker} (bind '{e['bindName']}').")
        cap = declared.get("elements", {}).get("maxItems") or (spec.get("elementSupport") or {}).get("maxTotalElements")
        if cap and len(elems) > cap:
            rep.err("ELEMENTS_CAP", f"{len(elems)} elements > máximo {cap}.")
        bound = {str(e["id"]) for e in elems}
        markers = set(re.findall(r"<<<([^<>]+)>>>", prompt))
        if markers - bound:
            rep.err("ELEMENT_UNBOUND", "Há marcadores no prompt sem vínculo em elements.")
    elif "<<<" in prompt:
        rep.err("ELEMENT_NOBIND", "prompt usa <<<id>>> mas 'elements' não foi enviado.")

    support = spec.get('elementSupport') or {}
    if elems and support:
        types = [e.get('type') for e in elems]
        if any(t not in {'image', 'video'} for t in types):
            rep.err('ELEMENT_TYPE_REQUIRED', 'Informe type=image|video conforme element_get; não inferir pelo nome.')
        for kind in ('image', 'video'):
            count = types.count(kind)
            if count and not support.get(kind + 'Elements'):
                rep.err('ELEMENT_TYPE_UNSUPPORTED', f'Element {kind} não suportado nesta rota.')
            cap = support.get('max' + kind.title() + 'Elements')
            if cap is not None and count > cap:
                rep.err('ELEMENT_TYPE_CAP', f'{count} Elements {kind} excedem {cap}.')
        if 'video_1' in mapping and types.count('video'):
            if any(n.startswith('image_') for n in mapping) or 'image' in types:
                rep.err('VIDEO_ELEMENT_MIX', 'Com video_1, Element de vídeo não combina com imagens/Elements de imagem.')
            if types.count('video') > support.get('maxVideoElementsWithVideoInput', 0):
                rep.err('VIDEO_ELEMENT_CAP', 'Quantidade de Elements de vídeo incompatível com video_1.')

    facts_by_slot = job.get('inputFacts') or {}
    for sn, ref in mapping.items():
        if not sn.startswith('video') or not isinstance(ref, str):
            continue
        facts = facts_by_slot.get(sn, {}) if isinstance(facts_by_slot, dict) else {}
        if not URL_RE.match(ref) and os.path.isfile(resolve_local(ref, root, req_dir)):
            try:
                facts = video_facts(resolve_local(ref, root, req_dir))
            except (OSError, ValueError, KeyError, IndexError, ZeroDivisionError, subprocess.SubprocessError):
                rep.err('VIDEO_PROBE', f'{sn}: ffprobe não confirmou vídeo válido.')
                continue
        numeric = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0
        if not isinstance(facts, dict) or not all(numeric(facts.get(k)) for k in ('durationSeconds', 'width', 'height', 'fps', 'bytes')):
            rep.err('VIDEO_FACTS_REQUIRED', f'{sn}: duração/dimensões/fps/tamanho precisam de evidência; não sondar pagando.')
            continue
        if tool == 'omni_ref_video':
            if not 3 <= facts['durationSeconds'] <= 10 or facts['bytes'] > 200 * 1024 * 1024 or not 24 <= facts['fps'] <= 60 or not (720 <= min(facts['width'], facts['height']) and max(facts['width'], facts['height']) <= 2160):
                rep.err('VIDEO_LIMIT', 'Contrato desta rota: vídeo 3–10 s, até 200 MiB, 720–2160 px, 24–60 fps.')
        if tool == 'motion_control' and job.get('referenceDurationSeconds') != facts['durationSeconds']:
            rep.err('MOTION_DURATION_MISMATCH', 'Duração orçada difere da referência medida; rever antes de enviar.')

    # ---- regras por ferramenta
    if tool == "motion_control":
        has_video = "video" in mapping
        has_motion = bool(given.get("motionId"))
        if has_video == has_motion:
            rep.err("MOTION_SOURCE", "motion_control exige exatamente UM de: input 'video' ou motionId.")
        seconds = job.get("referenceDurationSeconds")
        if not isinstance(seconds, (int, float)) or isinstance(seconds, bool) or not math.isfinite(seconds) or seconds <= 0:
            rep.warn("MOTION_DURATION_UNKNOWN", "Duração da referência desconhecida; não orçar como 5 s nem enviar.")
        elif given.get("motionDirection") == "image_direction" and not 3 <= seconds <= 10:
            rep.err("MOTION_DURATION", "image_direction exige referência de 3 a 10 s no contrato atual.")
        else:
            rep.info("MOTION_DURATION", f"Referência informada: {seconds} s; medir/verificar antes do orçamento.")
        if has_motion and not re.fullmatch(r'[1-9][0-9]*', str(given['motionId'])):
            rep.err('MOTION_ID', 'motionId precisa ser o ID decimal positivo real da biblioteca.')
        if elems and given.get('motionDirection') != 'motion_direction':
            rep.err('MOTION_ELEMENT_DIRECTION', 'Vínculo facial requer direção do vídeo; image_direction não foi qualificado.')
    if tool == "omni_ref_video":
        if cli_value(given.get("enable_audio")) == "true" and cli_value(given.get("keepOriginalSound")) == "true":
            rep.err("OMNI_AUDIO", "enable_audio e keepOriginalSound ambos 'true' — o guia do skill diz usar só um.")
        if "audio_1" not in slot_names:
            rep.info("OMNI_AUDIO_SLOT", "O snapshot não declara áudio independente; a presença de --audio no help não comprova suporte.")
        if 'video_1' in mapping:
            if cli_value(given.get('enable_audio')) == 'true':
                rep.err('OMNI_VIDEO_AUDIO', 'video_1 exige enable_audio=false nesta rota.')
            if str(given.get('duration', '5')).isdigit() and int(given.get('duration', '5')) > 10:
                rep.err('OMNI_VIDEO_DURATION', 'Saída acima de 10 s com vídeo não confirmada para esta rota; não usar API distinta como prova.')
    if tool == 'image_to_video' and model == 'kling-video-v2_6':
        tail = 'tail_image' in mapping
        if tail and given.get('resolution', '1080p') != '1080p':
            rep.err('V26_TAIL_RESOLUTION', 'Cauda no v2.6 exige 1080p.')
        if cli_value(given.get('enable_audio', 'true')) == 'true' and (tail or given.get('resolution', '1080p') != '1080p'):
            rep.err('V26_AUDIO', 'Áudio v2.6 exige 1080p e ausência de cauda.')
    if tool in ("image_to_video", "text_to_video") and model == "kling-video-v3_0_turbo":
        rep.info("TURBO", "Use somente os campos declarados neste snapshot; ausência de controle de áudio não garante silêncio.")
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
