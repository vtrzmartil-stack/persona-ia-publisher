#!/usr/bin/env python3
"""
Converte uma imagem estática em um reel curto (9:16, ~10s) com efeito de
zoom (Ken Burns) e legenda sobreposta, para publicação no TikTok/Instagram.

Uso:
    python3 make_reel.py <imagem_entrada> <saida.mp4> "<linha 1 da legenda>" ["<linha 2>"]
"""
import subprocess
import sys
import os
import re
import unicodedata

W, H = 1080, 1920
DURATION = 10
FPS = 30


def strip_emoji(text):
    """Remove emoji e outros símbolos que a fonte DejaVu não consegue
    renderizar (aparecem como caixas/"tofu"). Mantém letras, números,
    pontuação e acentos comuns do português."""
    out = []
    for ch in text:
        if ch in "\n\t":
            out.append(ch)
            continue
        cat = unicodedata.category(ch)
        # So (Symbol, other) cobre a maioria dos emojis; filtra pelo range
        # também para pegar emojis categorizados como Sk/Cs (variation selectors).
        cp = ord(ch)
        is_emoji_range = (
            0x1F300 <= cp <= 0x1FAFF
            or 0x2600 <= cp <= 0x27BF
            or 0x2190 <= cp <= 0x21FF  # setas (ex.: 👆 usa outro range, mas setas simples também somem)
            or 0xFE00 <= cp <= 0xFE0F  # variation selectors
            or cp == 0x200D  # zero-width joiner
        )
        if is_emoji_range or cat == "So":
            continue
        out.append(ch)
    cleaned = "".join(out)
    # colapsa espaços duplos deixados pela remoção
    cleaned = re.sub(r" {2,}", " ", cleaned).strip()
    return cleaned


def build_drawtext(lines):
    filters = []
    n = len(lines)
    # posição vertical: empilha as linhas perto do terço inferior
    base_y = H - 420
    line_h = 70
    for i, line in enumerate(lines):
        line = strip_emoji(line)
        text = line.replace("'", "’").replace(":", "\\:").replace("%", "\\%")
        y = base_y + i * line_h
        filters.append(
            f"drawtext=text='{text}':fontcolor=white:fontsize=54:"
            f"font='DejaVu Sans Bold':x=(w-text_w)/2:y={y}:"
            f"box=1:boxcolor=black@0.45:boxborderw=18:line_spacing=10"
        )
    return filters


def main():
    if len(sys.argv) < 4:
        print("Uso: make_reel.py <entrada> <saida.mp4> <linha1> [linha2] [linha3]")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    lines = sys.argv[3:]

    zoom_frames = DURATION * FPS
    # zoompan precisa de uma imagem de entrada escalada bem maior para evitar artefatos
    vf_parts = [
        f"scale=3240:5760",
        f"zoompan=z='min(zoom+0.0007,1.15)':d={zoom_frames}:s={W}x{H}:fps={FPS}",
    ]
    vf_parts.extend(build_drawtext(lines))
    vf = ",".join(vf_parts)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", src,
        "-vf", vf,
        "-t", str(DURATION),
        "-r", str(FPS),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        dst,
    ]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"OK: {dst}")


if __name__ == "__main__":
    main()
