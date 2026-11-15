#!/usr/bin/env python3
"""
Gera reels (9:16, ~10s) para todos os criativos já prontos em media/novos/,
usando make_reel.py, com legendas específicas por tema e CTA sempre
apontando para o link na bio (persona-ia.pages.dev/comprar).

Saída: media/reels-novos/<nome-do-criativo>.mp4
"""
import subprocess
import sys
import os

NOVOS_DIR = "media/novos"
OUT_DIR = "media/reels-novos"

# formato: nome_do_arquivo (sem extensao) -> lista de linhas da legenda
CAPTIONS = {
    # Explicativo — tom explicativo, soft-sell
    "explicativo-01": ["Isso aqui não é uma mulher real", "É uma modelo virtual gerada por IA", "Link na bio"],
    "explicativo-02": ["Essa consistência de rosto", "é treinada com IA generativa", "Link na bio"],
    "explicativo-03": ["Esse é o processo de edição", "que mantém o mesmo rosto sempre", "Link na bio"],
    "explicativo-04": ["Esse é o erro mais comum", "ao tentar criar modelo virtual sozinho", "A gente resolve isso. Link na bio"],
    "explicativo-05": ["Você escolhe o cenário", "a gente gera a modelo nele", "Simples assim. Link na bio"],
    "explicativo-06": ["Apresentando a persona oficial", "100% gerada por IA, pronta pra vender", "Link na bio"],
    "explicativo-07": ["Por trás de cada vídeo", "tem um processo todo pensado", "Quer o seu? Link na bio"],
    "explicativo-08": ["Cada imagem é escolhida a dedo", "pra manter a consistência da marca", "Link na bio"],
    "explicativo-09": ["Conteúdo autêntico,", "mesmo sendo 100% IA", "Saiba como. Link na bio"],
    "explicativo-10": ["Esse é o bastidor técnico", "de como criamos modelos virtuais", "Link na bio"],

    # Dúvida / FAQ — pergunta + resposta curta + CTA
    "duvida-01": ["Isso é legal?", "Sim! 100% dentro da lei", "Dúvidas? Link na bio"],
    "duvida-02": ["Preciso saber programar?", "Não! A gente cuida de tudo", "Link na bio"],
    "duvida-03": ["Quanto tempo leva?", "Bem menos do que você imagina", "Link na bio"],
    "duvida-04": ["Dá pra monetizar rápido?", "Muita gente já está lucrando", "Link na bio"],
    "duvida-05": ["Funciona pra qualquer nicho?", "Moda, fitness, comida, tech...", "Funciona! Link na bio"],
    "duvida-06": ["Preciso mostrar meu rosto de verdade?", "Não, a modelo é 100% gerada", "Link na bio"],
    "duvida-07": ["Dá pra fazer vídeo falando?", "Sim, com a nossa tecnologia", "Link na bio"],
    "duvida-08": ["Quanto custa pra começar?", "Menos do que um cafézinho por dia", "Link na bio"],
    "duvida-09": ["Posso usar no TikTok e Instagram juntos?", "Claro, em simultâneo!", "Link na bio"],
    "duvida-10": ["E se eu não tiver nada de design?", "A gente já deixa tudo pronto", "Link na bio"],

    # Caixinha de pergunta — estilo pergunta recebida + CTA pro produto
    "caixinha-01": ["Quanto tempo leva pra", "criar uma modelo virtual?", "Link na bio"],
    "caixinha-02": ["Dá pra fazer part-time,", "com outro emprego? Dá sim!", "Link na bio"],
    "caixinha-03": ["E se eu não tiver seguidores ainda?", "Todo mundo começa do zero", "Link na bio"],
    "caixinha-04": ["Posso vender pra empresas também?", "Sim, o mercado B2B tá crescendo", "Link na bio"],
    "caixinha-05": ["Tem suporte se eu tiver dúvidas?", "Sempre! Estamos aqui", "Link na bio"],
    "caixinha-06": ["Funciona em qualquer país?", "Sim, não só no Brasil", "Link na bio"],
    "caixinha-07": ["Preciso comprar equipamento caro?", "Não, só o celular já basta", "Link na bio"],
    "caixinha-08": ["Posso usar fotos antigas minhas?", "Pode ser o ponto de partida", "Link na bio"],
    "caixinha-09": ["Recebo atualizações depois de comprar?", "Sim, sempre melhorando", "Link na bio"],
    "caixinha-10": ["Preciso aparecer o tempo todo?", "Não, você escolhe sua exposição", "Link na bio"],

    # Exemplos — mostrar nichos possíveis, soft CTA
    "exemplo-01": ["Moda", "é um dos nichos que mais funcionam", "Veja mais exemplos. Link na bio"],
    "exemplo-02": ["Fitness", "também é um nicho em alta", "Link na bio"],
    "exemplo-03": ["Até culinária", "dá pra fazer com modelo virtual", "Link na bio"],
    "exemplo-04": ["Viagem e lifestyle", "outro nicho que converte muito", "Link na bio"],
    "exemplo-05": ["Beleza e skincare", "um dos nichos mais procurados", "Link na bio"],
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    only = sys.argv[1:] if len(sys.argv) > 1 else None

    done, skipped, failed = [], [], []
    for name, lines in CAPTIONS.items():
        if only and name not in only:
            continue
        src = os.path.join(NOVOS_DIR, f"{name}.jpg")
        dst = os.path.join(OUT_DIR, f"{name}.mp4")
        if not os.path.exists(src):
            skipped.append(name)
            continue
        if os.path.exists(dst):
            print(f"[skip] {name} (já existe)")
            done.append(name)
            continue
        print(f"[gerando] {name} ...")
        try:
            subprocess.run(
                ["python3", "make_reel.py", src, dst] + lines,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            done.append(name)
            print(f"[ok] {name}")
        except subprocess.CalledProcessError as e:
            failed.append(name)
            print(f"[ERRO] {name}: {e.stderr.decode()[-500:]}")

    print(f"\nFeitos: {len(done)} | Pulados (sem imagem): {len(skipped)} | Falharam: {len(failed)}")
    if skipped:
        print("Pulados:", skipped)
    if failed:
        print("Falharam:", failed)


if __name__ == "__main__":
    main()
