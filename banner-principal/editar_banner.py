from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).resolve().parent
ORIGINAL = PASTA / "banner_github_animated.gif"
SAIDA = PASTA / "banner-d-ribeiro.gif"
LARGURA, ALTURA = 1000, 429  # Mantém o formato e a resolução do GIF original.

# Área onde ficam as duas linhas de texto do GIF de referência.
# A máscara é localizada por brilho dentro dessa região para preservar o resto da arte.
REGIAO_TEXTO = (24, 190, 690, 260)

CAMINHOS_FONTE = [
    "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
]


def carregar_fonte(tamanho):
    for caminho in CAMINHOS_FONTE:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    raise FileNotFoundError("Instale uma fonte serifada, por exemplo Noto Serif Display.")


def limpar_texto_antigo(quadro):
    """Apaga letras e ornamentos do texto antigo com inpainting quadro a quadro."""
    rgb = np.asarray(quadro.convert("RGB"))
    x1, y1, x2, y2 = REGIAO_TEXTO
    recorte = rgb[y1:y2, x1:x2]
    cinza = cv2.cvtColor(recorte, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(recorte, cv2.COLOR_RGB2HSV)

    # Letras claras e pequenos separadores coloridos. O limite espacial evita
    # capturar o fio, a flor e a faixa iluminada do chão.
    # A tipografia é clara e pouco saturada. Assim, o fio cobre mais saturado
    # não é confundido com letras, mesmo quando passa perto do texto.
    claro = ((cinza > 65) & (hsv[:, :, 1] < 105)).astype(np.uint8) * 255
    saturados = ((hsv[:, :, 1] > 65) & (hsv[:, :, 2] > 90)).astype(np.uint8) * 255
    # Os separadores coloridos do texto são pequenos pontos; o fio, ao contrário,
    # é uma linha comprida. Abrir e filtrar componentes preserva o fio.
    saturados = cv2.morphologyEx(saturados, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(saturados, connectivity=8)
    colorido = np.zeros_like(saturados)
    for k in range(1, n):
        x, y, w, h, area = stats[k]
        if 3 <= area <= 160 and w <= 12 and h <= 12:
            colorido[labels == k] = 255
    mascara_local = cv2.bitwise_or(claro, colorido)
    mascara_local = cv2.dilate(mascara_local, np.ones((3, 3), np.uint8), iterations=1)

    mascara = np.zeros(rgb.shape[:2], dtype=np.uint8)
    mascara[y1:y2, x1:x2] = mascara_local
    limpo = cv2.inpaint(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), mascara, 4, cv2.INPAINT_TELEA)
    limpo = cv2.cvtColor(limpo, cv2.COLOR_BGR2RGB)
    return Image.fromarray(limpo)


def desenhar_texto(quadro):
    quadro = quadro.convert("RGB")
    camada = Image.new("RGBA", quadro.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    cor = (229, 220, 205, 255)  # marfim quente, próximo ao texto original
    sombra = (16, 11, 13, 150)

    linhas = [
        ("Em constante compilação", 27, 188),
        ("Estudos, desafios e aprendizados em programação, IA e automações.", 15, 220),
        ("Aberto a pequenos projetos.", 15, 244),
    ]
    for texto, tamanho, y in linhas:
        fonte = carregar_fonte(tamanho)
        # Sombra mínima para manter a leitura sem criar uma placa atrás do texto.
        d.text((40, y + 1), texto, font=fonte, fill=sombra, anchor="lt")
        d.text((40, y), texto, font=fonte, fill=cor, anchor="lt")

    # Assinatura discreta no canto inferior direito, conforme pedido anterior.
    assinatura = carregar_fonte(13)
    d.text((977, 397), "d-ribeiro", font=assinatura, fill=(225, 183, 174, 220), anchor="rs")
    return Image.alpha_composite(quadro.convert("RGBA"), camada).convert("RGB")


def main():
    if not ORIGINAL.exists():
        raise FileNotFoundError(f"Arquivo original não encontrado: {ORIGINAL}")

    gif = Image.open(ORIGINAL)
    if gif.size != (LARGURA, ALTURA):
        raise ValueError(f"O GIF esperado deve ter {LARGURA}x{ALTURA}; recebido: {gif.size}")

    quadros = []
    duracoes = []
    for indice in range(gif.n_frames):
        gif.seek(indice)
        quadro = gif.convert("RGB").copy()
        quadro = limpar_texto_antigo(quadro)
        quadro = desenhar_texto(quadro)
        quadros.append(quadro)
        duracoes.append(gif.info.get("duration", 120))

    quadros[0].save(
        SAIDA,
        format="GIF",
        save_all=True,
        append_images=quadros[1:],
        duration=duracoes,
        loop=gif.info.get("loop", 0),
        optimize=True,
        disposal=2,
    )
    print(f"GIF pronto: {SAIDA}")
    print(f"Tamanho: {LARGURA}x{ALTURA}; quadros: {len(quadros)}; duração: {sum(duracoes)/1000:.2f}s")


if __name__ == "__main__":
    main()
