# Persona IA — Publicador automático de Instagram

Publica automaticamente no Instagram (@personadeia) via Graph API oficial da
Meta, usando um GitHub Actions agendado (cron) — não depende de nenhuma
sessão do Claude estar ativa no horário do post.

## Como funciona

- `queue/manifest.json` é a fila de conteúdo: uma lista de posts com
  `status: "pending"`.
- O workflow `.github/workflows/publish.yml` roda 3x por dia (09h, 15h e 18h
  BRT) e publica até `POSTS_PER_RUN` (padrão 2) itens pendentes por execução
  → 6 posts/dia no total.
- `publish.py` cria o container de mídia na Graph API, espera processar
  (vídeos/reels) e publica.
- Depois de publicar, o item vira `status: "published"` e isso é commitado
  de volta no repositório automaticamente pela Action.

## Formato de cada item em `queue/manifest.json`

```json
{
  "id": "2026-11-20-reel-caixinha-01",
  "type": "feed_image" | "feed_video" | "reels" | "stories_image" | "stories_video",
  "media_url": "https://URL-PÚBLICA-DA-MÍDIA",
  "caption": "Legenda com call-to-action pra persona-ia.pages.dev/comprar",
  "theme": "conteudo" | "explicativo" | "venda",
  "status": "pending"
}
```

**Importante:** `media_url` precisa ser uma URL **pública** (a Graph API
busca a mídia diretamente de lá — não pode ser um link privado do GitHub).
O plano é hospedar as mídias em `persona-ia.pages.dev` (mesmo domínio já
usado pro checkout) e referenciar a URL pública aqui.

## Secrets necessários (Settings → Secrets and variables → Actions)

- `IG_ACCESS_TOKEN` — token de usuário de sistema do app "Persona IA
  Publisher" (Meta for Developers, App ID 1842076933595622)
- `IG_USER_ID` — `17841409783476331` (conta @personadeia)

## Rodar manualmente (teste)

Aba "Actions" → workflow "Publicar no Instagram" → "Run workflow".
