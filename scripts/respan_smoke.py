#!/usr/bin/env python3
"""
scripts/respan_smoke.py
Smoke test da integração Respan (mesma fiação de gemini_generate.py), com um modelo
de texto barato para não gastar créditos de imagem.

Uso:
    python scripts/respan_smoke.py            # tracing: chama Google direto, exporta trace p/ Respan
    RESPAN_GATEWAY=1 python scripts/respan_smoke.py   # gateway: roteia via api.respan.ai
Verifique depois com:
    respan traces list --limit 5 --json
    respan logs list --limit 5 --all-envs true --json
"""
import os
import sys

from gemini_generate import load_env


def main() -> int:
    load_env()
    respan_api_key = os.environ.get("RESPAN_API_KEY")
    if not respan_api_key:
        print("ERRO: RESPAN_API_KEY ausente", file=sys.stderr)
        return 1
    use_gateway = os.environ.get("RESPAN_GATEWAY", "").strip() in ("1", "true", "yes")

    from google import genai
    from respan import Respan
    from respan_instrumentation_google_genai import GoogleGenAIInstrumentor

    import json as _json
    try: _meta = _json.loads(os.environ.get("RESPAN_METADATA", "") or "{}")
    except ValueError: _meta = {}
    Respan(instrumentations=[GoogleGenAIInstrumentor()],
           app_name=os.environ.get("RESPAN_WORKFLOW_NAME") or "respan_smoke",
           customer_identifier="movies-projects", metadata=_meta)

    if use_gateway:
        client = genai.Client(
            api_key=respan_api_key,
            http_options={"base_url": "https://api.respan.ai/api/google/gemini"},
        )
        mode = "gateway"
    else:
        google_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not google_key:
            print("ERRO: GEMINI_API_KEY ausente", file=sys.stderr)
            return 1
        client = genai.Client(api_key=google_key)
        mode = "tracing"

    model = os.environ.get("RESPAN_SMOKE_MODEL", "gemini-3.8-flash")
    from respan import workflow as _wf
    @_wf(name=os.environ.get("RESPAN_WORKFLOW_NAME") or "respan_smoke")
    def _generate():
        return client.models.generate_content(model=model, contents="Reply with exactly: respan smoke ok")
    response = _generate()
    print(f"[{mode}] model={model} response={response.text!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
