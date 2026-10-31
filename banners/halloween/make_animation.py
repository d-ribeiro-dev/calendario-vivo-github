from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BG_PATH = ROOT / "halloween-scene-title.png"
GIRL_PATH = ROOT / "ruivinha-surpresa.png"
WITCH_PATH = ROOT / "bruxa-voando.png"
OUT_PATH = ROOT / "halloween-animation.gif"
W, H = 720, 309
FRAMES = 80
DURATION = 120

bg = Image.open(BG_PATH).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)

def crop_alpha(path):
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A")
    bbox = a.point(lambda p: 255 if p > 16 else 0).getbbox()
    return im.crop(bbox)

girl_src = crop_alpha(GIRL_PATH)
girl_h = 146
girl_w = round(girl_src.width * girl_h / girl_src.height)
girl = girl_src.resize((girl_w, girl_h), Image.Resampling.LANCZOS)
witch_src = crop_alpha(WITCH_PATH)
witch_w = 78
witch_h = round(witch_src.height * witch_w / witch_src.width)
witch = witch_src.resize((witch_w, witch_h), Image.Resampling.LANCZOS)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
try:
    label_font = ImageFont.truetype(FONT, 8)
except OSError:
    label_font = ImageFont.load_default()

# Ghosts carry recognizable short coding/tool sigils while gently bobbing in the sky.
ghosts = [
    (165, 95, "VS", (28, 115, 207)),
    (252, 137, "GIT", (224, 93, 50)),
    (342, 102, "PIL", (45, 133, 188)),
    (432, 142, "PY", (190, 146, 28)),
    (520, 100, "JS", (180, 127, 26)),
    (606, 138, "CSS", (68, 91, 206)),
]

def draw_ghost(draw, cx, top, label, color):
    # Small floating sheet ghost with a crisp label on its chest.
    white = (247, 246, 255, 245)
    edge = (187, 205, 255, 240)
    x0, x1 = cx - 18, cx + 18
    y0 = top
    draw.ellipse((x0, y0, x1, y0 + 27), fill=white, outline=edge, width=1)
    draw.rectangle((x0, y0 + 14, x1, y0 + 30), fill=white)
    draw.polygon([
        (x0, y0 + 27), (x0 + 7, y0 + 35), (x0 + 13, y0 + 28),
        (cx, y0 + 36), (cx + 7, y0 + 28), (x1 - 7, y0 + 35),
        (x1, y0 + 27), (x1, y0 + 16), (x0, y0 + 16)
    ], fill=white, outline=edge)
    draw.ellipse((cx - 8, y0 + 11, cx - 4, y0 + 16), fill=(31, 28, 48, 255))
    draw.ellipse((cx + 4, y0 + 11, cx + 8, y0 + 16), fill=(31, 28, 48, 255))
    bbox = draw.textbbox((0, 0), label, font=label_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle((cx - tw / 2 - 3, y0 + 19, cx + tw / 2 + 3, y0 + 31), radius=2, fill=(255, 255, 255, 220))
    draw.text((cx - tw / 2, y0 + 20 - bbox[1]), label, font=label_font, fill=color, stroke_width=0)

frames = []
girl_x = 72
ground_y = 272
# Eye positions approximate the visible pupils in the cropped character sprite.
# They drift slightly between three glances; periodic short lines create a blink.
for f in range(FRAMES):
    frame = bg.convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Witch appears from the left of the moon, flies slowly across it, then fades away.
    if 8 <= f <= 70:
        progress = min(1.0, max(0.0, (f - 8) / 56))
        wx = int(540 + progress * 165)
        wy = int(31 + 3 * math.sin(f * math.pi / 18))
        fade_in = min(1.0, (f - 8) / 4)
        fade_out = min(1.0, (70 - f) / 5)
        opacity = max(0.0, min(fade_in, fade_out, 1.0))
        wimg = witch.copy()
        if opacity < 1:
            alpha = wimg.getchannel("A").point(lambda p: int(p * opacity))
            wimg.putalpha(alpha)
        frame.alpha_composite(wimg, (wx, wy))

    for i, (cx0, y0, label, color) in enumerate(ghosts):
        bob = int(5 * math.sin(f * 2 * math.pi / 42 + i * 1.05))
        drift = int(3 * math.sin(f * 2 * math.pi / 60 + i * 0.8))
        cx = cx0 + drift
        top = y0 + bob
        draw_ghost(d, cx, top, label, color)
        # A tiny twinkle accompanies each slow float.
        if (f + i * 7) % 20 in (0, 1):
            sx, sy = cx + 24, top + 12
            d.line((sx - 2, sy, sx + 2, sy), fill=(255, 242, 177, 230), width=1)
            d.line((sx, sy - 2, sx, sy + 2), fill=(255, 242, 177, 230), width=1)

    frame = Image.alpha_composite(frame, overlay)

    # Quiet idle pose: she stays planted, with a tiny breathing bob as she watches the sky.
    bob = int(1.5 * math.sin(f * 2 * math.pi / 32))
    gy = ground_y - girl_h - bob
    frame.alpha_composite(girl, (girl_x, gy))

    # Slight pupil/glint shifts make her gaze scan the floating ghosts.
    gaze = int(round(1.5 * math.sin(f * 2 * math.pi / 36)))
    eye_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(eye_layer)
    # Tiny dark pupils and moving catchlights sit within the already-wide orange eyes.
    for ex, ey, direction in [(girl_x + 47, gy + 43, 1), (girl_x + 67, gy + 39, -1)]:
        px = ex + gaze * direction
        py = ey - (1 if f % 36 < 18 else 0)
        ed.ellipse((px - 1, py - 2, px + 1, py + 2), fill=(52, 31, 48, 235))
        ed.point((px + 1, py - 2), fill=(255, 249, 225, 255))
    # Two brief blinks per cycle: the startled expression remains visible between them.
    if f % 40 in (18, 19):
        ed.line((girl_x + 38, gy + 44, girl_x + 55, gy + 44), fill=(54, 29, 48, 255), width=2)
        ed.line((girl_x + 58, gy + 40, girl_x + 72, gy + 40), fill=(54, 29, 48, 255), width=2)
    frame = Image.alpha_composite(frame, eye_layer)
    frames.append(frame.convert("RGB"))

# Build a shared palette from representative moments so the moon, sprites and labels stay stable.
sample = Image.new("RGB", (W * 4, H * 2))
for n, idx in enumerate([0, 10, 20, 30, 40, 50, 60, 70]):
    sample.paste(frames[idx], ((n % 4) * W, (n // 4) * H))
palette = sample.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
quantized = [fr.quantize(palette=palette, dither=Image.Dither.NONE) for fr in frames]
quantized[0].save(OUT_PATH, save_all=True, append_images=quantized[1:], duration=DURATION, loop=0, optimize=True, disposal=2)
print(f"GIF salvo em: {OUT_PATH}")
