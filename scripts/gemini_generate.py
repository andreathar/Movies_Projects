#!/usr/bin/env python3
"""
scripts/gemini_generate.py
Gera imagens cinematográficas e referências usando a API direta do Gemini (Google AI Studio)
sem gastar créditos do Kling.

Uso:
    python scripts/gemini_generate.py --prompt "..." --output "caminho.jpg"
    python scripts/gemini_generate.py --prompt "..." --references foto1.jpg foto2.jpg --output "caminho.jpg"
"""

import argparse
import os
import sys
from pathlib import Path

# Carrega .env se existir
def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip('"').strip("'")
                    os.environ.setdefault(key.strip(), val)

def main():
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERRO: GEMINI_API_KEY não encontrada no ambiente ou no arquivo .env", file=sys.stderr)
        print("Obtenha sua chave em: https://aistudio.google.com/apikey", file=sys.stderr)
        print("Adicione no arquivo .env: GEMINI_API_KEY=sua_chave_aqui", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Geração de imagens via Gemini API")
    parser.add_argument("--prompt", required=True, help="Descrição da imagem cinematográfica")
    parser.add_argument("--references", nargs="*", default=[], help="Fotos de referência (ex: suas fotos reais)")
    parser.add_argument("--model", default="gemini-3-pro-image", choices=["gemini-3-pro-image", "gemini-3.1-flash-image"], help="Modelo Gemini")
    parser.add_argument("--aspect-ratio", default="3:4", choices=["1:1", "3:4", "4:3", "16:9", "9:16"], help="Aspect ratio")
    parser.add_argument("--output", required=True, help="Arquivo de destino (JPG/PNG)")
    args = parser.parse_args()

    from google import genai
    from PIL import Image

    # --- Respan: tracing (observability) + optional gateway ---
    # Tracing: the instrumentor must be created BEFORE the Gemini client so every
    # generate_content call is exported as a trace/span to Respan.
    # Gateway: set RESPAN_GATEWAY=1 to route the call through api.respan.ai instead
    # of calling Google directly (uses RESPAN_API_KEY; Respan needs Gemini credits/key).
    respan_api_key = os.environ.get("RESPAN_API_KEY")
    use_gateway = os.environ.get("RESPAN_GATEWAY", "").strip() in ("1", "true", "yes")
    if respan_api_key:
        from respan import Respan
        from respan_instrumentation_google_genai import GoogleGenAIInstrumentor

        # Scene/lane tags come from the lane shell (scripts/lane_env.sh), same as the
        # agent hooks: RESPAN_WORKFLOW_NAME=<scene-id>, RESPAN_METADATA={lane,role,scene,episode}
        import json as _json
        try:
            _meta = _json.loads(os.environ.get("RESPAN_METADATA", "") or "{}")
        except ValueError:
            _meta = {}
        _meta.setdefault("project", "Movies_Projects")
        _meta.setdefault("script", "gemini_generate.py")
        Respan(
            instrumentations=[GoogleGenAIInstrumentor()],
            app_name=os.environ.get("RESPAN_WORKFLOW_NAME") or "gemini_generate",
            customer_identifier="movies-projects",
            metadata=_meta,
        )
    elif use_gateway:
        print("ERRO: RESPAN_GATEWAY=1 exige RESPAN_API_KEY no .env", file=sys.stderr)
        sys.exit(1)

    if use_gateway:
        client = genai.Client(
            api_key=respan_api_key,
            http_options={"base_url": "https://api.respan.ai/api/google/gemini"},
        )
    else:
        client = genai.Client(api_key=api_key)

    contents = []
    # Anexa fotos de referência para consistência de personagem
    for ref_path in args.references:
        p = Path(ref_path)
        if not p.exists():
            print(f"AVISO: Referência {ref_path} não encontrada, pulando.", file=sys.stderr)
            continue
        img = Image.open(p)
        contents.append(img)

    contents.append(args.prompt)

    print(f"Gerando via Gemini ({args.model}) com {len(args.references)} referências...")
    
    # Chama o modelo multimodal de geração de imagem
    def _generate():
        return client.models.generate_content(model=args.model, contents=contents)

    if respan_api_key:
        # Group this call under the scene (RESPAN_WORKFLOW_NAME) like the agent hooks do,
        # so Respan rolls image cost into the same per-scene total.
        from respan import workflow as _respan_workflow
        _generate = _respan_workflow(name=os.environ.get("RESPAN_WORKFLOW_NAME") or "gemini_generate")(_generate)

    response = _generate()

    # Procura a imagem gerada no output
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    saved = False
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            data = part.inline_data.data
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"✓ Imagem salva com sucesso em: {out_path}")
            saved = True
            break

    if not saved:
        print("Resposta do modelo (texto):", response.text)
        print("Nenhuma imagem gerada foi retornada na resposta.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
