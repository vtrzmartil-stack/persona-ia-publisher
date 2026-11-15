#!/usr/bin/env python3
"""
Gera as legendas completas do Instagram (com hashtags) para os 35 reels novos
e monta queue/reels_backlog.json com os itens ainda não publicados, na ordem
em que devem ir saindo (1-2 por dia). Os 2 primeiros da lista escolhida para
"publicar hoje" NÃO entram no backlog — são adicionados direto ao
queue/manifest.json por outro passo.

Uso: python3 build_captions.py
"""
import json

BASE_URL = "https://raw.githubusercontent.com/vtrzmartil-stack/persona-ia-publisher/main/media/reels-novos"
LINK = "persona-ia.pages.dev/comprar"
TAGS_BASE = "#personaia #modelovirtual #iainfluencer #inteligenciaartificial #avatarvirtual"

EXPLICATIVO = {
    "explicativo-01": "Isso aqui não é uma mulher real — é uma modelo virtual gerada por IA, com rosto 100% consistente em toda foto e vídeo 🤖",
    "explicativo-02": "Essa consistência de rosto não é sorte, é treino certo de IA generativa. É exatamente isso que a gente entrega pronto pra você 💡",
    "explicativo-03": "Por trás de cada imagem tem um processo de edição que garante o mesmo rosto sempre — sem isso, a mágica não existe 🎬",
    "explicativo-04": "Esse é o erro mais comum de quem tenta criar modelo virtual sozinho: o rosto muda de foto pra foto. A gente já resolveu isso pra você 🙌",
    "explicativo-05": "Você escolhe o cenário, a gente gera a sua modelo virtual nele — do jeito que você precisar, no seu nicho 📸",
    "explicativo-06": "Apresentando a persona oficial: 100% gerada por IA e pronta pra vender. Quer a sua própria? ✨",
    "explicativo-07": "Por trás de cada vídeo tem um processo todo pensado pra parecer natural e consistente. Quer o seu? 🎥",
    "explicativo-08": "Cada imagem é escolhida a dedo pra manter a identidade visual da marca sempre igual 🖼️",
    "explicativo-09": "Conteúdo autêntico, engajador e vendável — mesmo sendo 100% gerado por IA. É mais simples do que parece 🚀",
    "explicativo-10": "Esse é o bastidor técnico de como a gente cria modelos virtuais com rosto consistente do início ao fim ⚙️",
}

DUVIDA = {
    "duvida-01": ("Isso é legal?", "Sim! 100% dentro da lei — persona virtual é só uma ferramenta de criação de conteúdo 😊"),
    "duvida-02": ("Preciso saber programar?", "Não! A gente cuida de toda a parte técnica pra você 💻"),
    "duvida-03": ("Quanto tempo leva pra ter a minha modelo virtual?", "Bem menos do que você imagina ⏱️"),
    "duvida-04": ("Dá pra monetizar rápido com isso?", "Muita gente já está lucrando com conteúdo gerado por IA 💰"),
    "duvida-05": ("Funciona pra qualquer nicho?", "Moda, fitness, comida, viagem, tech... funciona pra praticamente tudo ✅"),
    "duvida-06": ("Preciso mostrar meu rosto de verdade?", "Não! A modelo é 100% gerada por IA, você fica no anonimato 🕶️"),
    "duvida-07": ("Dá pra fazer vídeo falando, não só foto?", "Sim, com a nossa tecnologia dá pra ir além da imagem estática 🎙️"),
    "duvida-08": ("Quanto custa pra começar?", "Menos do que um cafézinho por dia ☕"),
    "duvida-09": ("Posso usar no TikTok e no Instagram ao mesmo tempo?", "Claro! O mesmo conteúdo funciona em simultâneo nas duas redes 📱"),
    "duvida-10": ("E se eu não tiver nada de design ou edição?", "Relaxa, a gente já deixa tudo pronto pra você publicar 🛋️"),
}

CAIXINHA = {
    "caixinha-01": ("Quanto tempo leva pra criar uma modelo virtual?", "Com os prompts certos, a primeira foto sai em minutos 😉"),
    "caixinha-02": ("Dá pra fazer part-time, com outro emprego?", "Dá sim! Muita gente começa assim mesmo ☕"),
    "caixinha-03": ("E se eu não tiver seguidores ainda?", "Todo mundo começa do zero — o conteúdo certo atrai o público 🌱"),
    "caixinha-04": ("Posso vender pra empresas também?", "Sim! O mercado B2B de modelos virtuais tá crescendo rápido 📈"),
    "caixinha-05": ("Tem suporte se eu tiver dúvidas?", "Sempre! Estamos aqui pra te ajudar em cada etapa 🎧"),
    "caixinha-06": ("Funciona em qualquer país?", "Sim, não só no Brasil — o alcance é global 🌍"),
    "caixinha-07": ("Preciso comprar equipamento caro?", "Não, só o celular já basta pra começar 📲"),
    "caixinha-08": ("Posso usar fotos antigas minhas como ponto de partida?", "Pode sim! A gente adapta a partir do que você já tem 📷"),
    "caixinha-09": ("Recebo atualizações depois de comprar?", "Sim, sempre melhorando a tecnologia pra você 🔄"),
    "caixinha-10": ("Preciso aparecer o tempo todo nas redes?", "Não! Você escolhe o nível de exposição que quiser 🙈"),
}

EXEMPLO = {
    "exemplo-01": ("Moda", "moda"),
    "exemplo-02": ("Fitness", "fitness"),
    "exemplo-03": ("Culinária", "culinaria"),
    "exemplo-04": ("Viagem e lifestyle", "viagem"),
    "exemplo-05": ("Beleza e skincare", "beleza"),
}

captions = {}

for name, hook in EXPLICATIVO.items():
    captions[name] = {
        "caption": f"{hook}\n\nCrie a sua também: {LINK}\n{TAGS_BASE}",
        "theme": "explicativo",
    }

for name, (q, a) in DUVIDA.items():
    captions[name] = {
        "caption": f"Tira-dúvidas 🙋 \"{q}\"\n{a}\n\nMais dúvidas? Link na bio: {LINK}\n{TAGS_BASE}",
        "theme": "duvida",
    }

for name, (q, a) in CAIXINHA.items():
    captions[name] = {
        "caption": f"Caixinha de perguntas 💬 \"{q}\"\n{a}\n\nLink na bio: {LINK}\n{TAGS_BASE}",
        "theme": "caixinha",
    }

for name, (nicho, tag) in EXEMPLO.items():
    captions[name] = {
        "caption": f"{nicho} também é um dos nichos que mais funcionam com modelo virtual de IA 🔥 Quer ver como fica no seu nicho?\n\nLink na bio: {LINK}\n{TAGS_BASE} #{tag}",
        "theme": "exemplo",
    }

# Ordem de publicação: alterna formatos para variar o feed, prioriza duvida/caixinha
# (mais "ganchos") no início, intercalando com explicativo e exemplo.
ORDER = []
pools = {
    "duvida": list(DUVIDA.keys()),
    "caixinha": list(CAIXINHA.keys()),
    "explicativo": list(EXPLICATIVO.keys()),
    "exemplo": list(EXEMPLO.keys()),
}
cycle = ["duvida", "caixinha", "explicativo", "exemplo", "duvida", "caixinha", "explicativo"]
i = 0
while any(pools.values()):
    key = cycle[i % len(cycle)]
    i += 1
    if pools[key]:
        ORDER.append(pools[key].pop(0))

# Os 2 primeiros desta ordem já viram "hoje" (tratados fora deste script).
TODAY = ORDER[:2]
BACKLOG = ORDER[2:]

print("Publicar HOJE:", TODAY)
print(f"Backlog restante: {len(BACKLOG)} itens")

backlog_items = []
for name in BACKLOG:
    c = captions[name]
    backlog_items.append({
        "id": f"novo-{name}",
        "type": "reels",
        "media_url": f"{BASE_URL}/{name}.mp4",
        "caption": c["caption"],
        "theme": c["theme"],
        "status": "scheduled",
    })

with open("queue/reels_backlog.json", "w", encoding="utf-8") as f:
    json.dump(backlog_items, f, ensure_ascii=False, indent=2)

# Salva também as legendas dos 2 de hoje num arquivo auxiliar p/ o próximo passo
today_items = []
for name in TODAY:
    c = captions[name]
    today_items.append({
        "name": name,
        "id": f"novo-{name}",
        "media_url": f"{BASE_URL}/{name}.mp4",
        "caption": c["caption"],
        "theme": c["theme"],
    })
with open("queue/today.json", "w", encoding="utf-8") as f:
    json.dump(today_items, f, ensure_ascii=False, indent=2)

print("queue/reels_backlog.json e queue/today.json gerados.")
