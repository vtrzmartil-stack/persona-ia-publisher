#!/usr/bin/env python3
"""
Persona IA — publicador automático para Instagram via Graph API.

Lê queue/manifest.json, pega os próximos itens "pending" (por padrão 2 por
execução) e publica no Instagram (@personadeia) via Graph API oficial da Meta.
Suporta feed (imagem), reels (vídeo) e stories (imagem ou vídeo).

Variáveis de ambiente obrigatórias:
  IG_ACCESS_TOKEN  — token de usuário de sistema do app "Persona IA Publisher"
  IG_USER_ID       — ID da conta profissional do Instagram (@personadeia)

Variáveis opcionais:
  POSTS_PER_RUN    — quantos itens pending publicar nesta execução (default 2)
"""
import json
import os
import sys
import time
from pathlib import Path
from urllib import request, parse, error

GRAPH_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"
MANIFEST_PATH = Path(__file__).parent / "queue" / "manifest.json"
LOG_PATH = Path(__file__).parent / "queue" / "log.jsonl"

MEDIA_TYPE_MAP = {
    "feed_image": {"params": {}, "field": "image_url"},
    "feed_video": {"params": {"media_type": "VIDEO"}, "field": "video_url"},
    "reels": {"params": {"media_type": "REELS"}, "field": "video_url"},
    "stories_image": {"params": {"media_type": "STORIES"}, "field": "image_url"},
    "stories_video": {"params": {"media_type": "STORIES"}, "field": "video_url"},
}


def http(method, url, data=None):
    body = parse.urlencode(data).encode() if data else None
    req = request.Request(url, data=body if method == "POST" else None, method=method)
    if method == "GET" and data:
        req.full_url = url + "?" + parse.urlencode(data)
    try:
        with request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} on {url}: {e.read().decode()}") from e


def log_event(event: dict):
    event["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def create_container(ig_user_id, token, item):
    spec = MEDIA_TYPE_MAP[item["type"]]
    params = {spec["field"]: item["media_url"], "access_token": token}
    if item.get("caption"):
        params["caption"] = item["caption"]
    params.update(spec["params"])
    resp = http("POST", f"{GRAPH_BASE}/{ig_user_id}/media", params)
    return resp["id"]


def wait_until_ready(creation_id, token, timeout_s=300, interval_s=10):
    waited = 0
    while waited < timeout_s:
        resp = http("GET", f"{GRAPH_BASE}/{creation_id}",
                     {"fields": "status_code", "access_token": token})
        status = resp.get("status_code")
        if status == "FINISHED":
            return True
        if status == "ERROR":
            raise RuntimeError(f"Container {creation_id} entrou em ERROR")
        time.sleep(interval_s)
        waited += interval_s
    raise RuntimeError(f"Timeout esperando container {creation_id} ficar pronto")


def publish_container(ig_user_id, token, creation_id):
    resp = http("POST", f"{GRAPH_BASE}/{ig_user_id}/media_publish",
                {"creation_id": creation_id, "access_token": token})
    return resp["id"]


def main():
    token = os.environ.get("IG_ACCESS_TOKEN")
    ig_user_id = os.environ.get("IG_USER_ID")
    posts_per_run = int(os.environ.get("POSTS_PER_RUN", "2"))

    if not token or not ig_user_id:
        print("Faltam IG_ACCESS_TOKEN / IG_USER_ID no ambiente.", file=sys.stderr)
        sys.exit(1)

    if not MANIFEST_PATH.exists():
        print("queue/manifest.json não existe. Nada a publicar.")
        return

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    pending = [item for item in manifest if item.get("status") == "pending"]

    if not pending:
        print("Fila vazia (nenhum item pending). Nada a publicar nesta execução.")
        return

    todo = pending[:posts_per_run]
    print(f"{len(todo)} item(ns) para publicar nesta execução (de {len(pending)} pendentes).")

    for item in todo:
        try:
            if item["type"] not in MEDIA_TYPE_MAP:
                raise ValueError(f"Tipo desconhecido: {item['type']}")

            creation_id = create_container(ig_user_id, token, item)

            if item["type"] in ("reels", "feed_video", "stories_video"):
                wait_until_ready(creation_id, token)

            media_id = publish_container(ig_user_id, token, creation_id)

            item["status"] = "published"
            item["published_media_id"] = media_id
            item["published_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            log_event({"id": item["id"], "result": "success", "media_id": media_id})
            print(f"  OK: {item['id']} -> media_id={media_id}")

        except Exception as exc:  # noqa: BLE001
            item["status"] = "failed"
            item["error"] = str(exc)
            log_event({"id": item["id"], "result": "failed", "error": str(exc)})
            print(f"  FALHOU: {item['id']} -> {exc}", file=sys.stderr)

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
