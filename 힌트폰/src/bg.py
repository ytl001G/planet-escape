# 힌트폰 배경 생성 (사진 없이 직접 그림 → 저작권 걱정 없음). 갤럭시 A13: 1080x2408 (20:9)
import sys, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(exist_ok=True)
PREV = pathlib.Path(sys.argv[2])
W, H = 1080, 2408

def hexc(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float) / 255

def fbm(seed, scales=(6, 12, 24, 48, 96, 192, 384), gain=0.85):
    rng = np.random.default_rng(seed); acc = np.zeros((H, W)); tot = 0
    for s in scales:
        a = rng.random((H // s + 3, W // s + 3))
        im = Image.fromarray((a * 255).astype(np.uint8)).resize((W + 2 * s, H + 2 * s), Image.BICUBIC)
        a = np.asarray(im, float)[s:s + H, s:s + W] / 255
        w = s ** gain; acc += a * w; tot += w
    acc /= tot
    return (acc - acc.min()) / (acc.max() - acc.min())

def grad(cx, cy, r):
    y, x = np.mgrid[0:H, 0:W]
    return np.clip(1 - np.hypot((x - cx) / r, (y - cy) / r), 0, 1)

def stars(seed, n, tint=(1, 1, 1), maxb=1.0):
    rng = np.random.default_rng(seed)
    lay = Image.new('RGB', (W, H)); d = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y = rng.random() * W, rng.random() * H
        b = min(1.0, (rng.pareto(3.0) + 0.15) * 0.35) * maxb
        r = 0.6 + 2.2 * b ** 2
        c = tuple(int(255 * b * (0.75 + 0.25 * t)) for t in tint)
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    glow = lay.filter(ImageFilter.GaussianBlur(5))
    return np.asarray(lay, float) / 255 + np.asarray(glow, float) / 255 * 1.6

def finish(img, name, vignette=0.55, center_dim=0.25):
    # UI가 놓이는 가운데를 살짝 어둡게, 가장자리 비네트 → 흰 글씨가 잘 읽히게
    v = grad(W / 2, H / 2, np.hypot(W, H) * 0.62)
    img = img * (1 - vignette + vignette * v[..., None] ** 0.6)
    band = np.exp(-((np.mgrid[0:H, 0:W][0] - H * 0.47) / (H * 0.28)) ** 2)
    img = img * (1 - center_dim * band[..., None])
    rng = np.random.default_rng(7)
    img = img + (rng.random((H, W, 1)) - 0.5) / 255 * 3  # 밴딩 방지 디더
    out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    out.save(OUT / f'{name}.png', optimize=True)
    return out

made = {}
# 1) 안전 모드 이전: 무채색, 잠긴 시스템 느낌 (흐린 성운 + 아주 옅은 주사선)
n = fbm(11)
img = hexc('#101014') + (n[..., None] ** 2.2) * hexc('#2a2a33') * 0.9
img += stars(12, 500, (0.9, 0.95, 1), 0.55) * 0.55
scan = (np.arange(H) % 6 < 1).astype(float)[:, None, None] * 0.018
img = img - scan
made['bg_pre'] = finish(img, 'bg_pre')

# 2) 1부: 릴리 보라 성운
n = fbm(21); m = fbm(22, gain=1.1)
neb = np.clip((n - 0.38) * 2.2, 0, 1) ** 1.6 * (0.55 + 0.9 * grad(W * 0.85, H * 0.2, H * 0.75))[..., None] if False else None
mask = np.clip((n - 0.38) * 2.2, 0, 1) ** 1.6 * (0.35 + 0.95 * grad(W * 0.85, H * 0.18, H * 0.8))
fil = np.clip((m - 0.55) * 3, 0, 1) ** 2 * mask
img = (hexc('#0d0812') + mask[..., None] * hexc('#5a1a74') * 0.85 + fil[..., None] * hexc('#cf86e6') * 0.45
       + grad(W * 0.15, H * 0.92, H * 0.5)[..., None] ** 2 * hexc('#2b1a5c') * 0.6)
img += stars(23, 1100, (1, 0.9, 1), 0.9) * 0.8
made['bg_part1'] = finish(img, 'bg_part1')

# 3) 2부: 비아 주황 — 따뜻한 빛 + 디지털 흔적(주사선, 몇 줄 밀림)
n = fbm(31); m = fbm(32, gain=1.1)
mask = np.clip((n - 0.4) * 2.2, 0, 1) ** 1.5 * (0.3 + 1.0 * grad(W * 0.2, H * 0.25, H * 0.8))
fil = np.clip((m - 0.55) * 3, 0, 1) ** 2 * mask
img = (hexc('#120a05') + mask[..., None] * hexc('#7a3a00') * 0.85 + fil[..., None] * hexc('#ffae4d') * 0.4
       + grad(W * 0.9, H * 0.9, H * 0.45)[..., None] ** 2 * hexc('#5c2a00') * 0.5)
img += stars(33, 900, (1, 0.85, 0.65), 0.85) * 0.75
img = img - (np.arange(H) % 5 < 1).astype(float)[:, None, None] * 0.025
rng = np.random.default_rng(34)
for _ in range(7):  # 몇 줄만 옆으로 밀린 글리치 띠
    y0 = int(rng.random() * H); h = int(6 + rng.random() * 22); dx = int((rng.random() - 0.5) * 90)
    img[y0:y0 + h] = np.roll(img[y0:y0 + h], dx, axis=1) * 1.08
made['bg_part2'] = finish(img, 'bg_part2')

# 4) 행성 엔딩: 아래쪽 행성 지평선 + 대기 빛, 위로 별
img = hexc('#05070d') + stars(41, 1300, (0.85, 0.92, 1), 1.0) * 0.85
y, x = np.mgrid[0:H, 0:W]
cx, cy, R = W * 0.5, H + 1650, 2150
d = np.hypot(x - cx, y - cy) - R
planet = (d < 0)
surf = fbm(42, scales=(12, 24, 48, 96, 192))
lit = np.clip(1 - (y - (cy - R)) / 900, 0, 1)
img[planet] = (hexc('#0b1426') * 0.6 + surf[planet][:, None] * hexc('#1c3358') * 0.5) * (0.35 + 0.65 * lit[planet][:, None])
rim = np.exp(-np.abs(d) / 26) * (d > -60)
halo = np.exp(-np.clip(d, 0, None) / 220) * (d >= 0)
img += rim[..., None] * hexc('#ffb36b') * 0.9 + halo[..., None] * hexc('#3a6db0') * 0.55
made['bg_end_planet'] = finish(img, 'bg_end_planet', vignette=0.4, center_dim=0.15)

# 5) 탈출 엔딩: 완전한 검정
Image.new('RGB', (W, H), 'black').save(OUT / 'bg_end_escape.png'); made['bg_end_escape'] = Image.new('RGB', (W, H), 'black')

# 미리보기: 메인 화면 UI를 얹어 글자가 읽히는지 확인용
font = lambda s, b=True: ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf' if b else 'C:/Windows/Fonts/malgun.ttf', s)
order = [('bg_pre', '#ffffff', None), ('bg_part1', '#cf86e6', '알렉스의 승인 확보'), ('bg_part2', '#ffae4d', None),
         ('bg_end_planet', '#ffae4d', None), ('bg_end_escape', '#ffffff', None)]
tw, th = 300, 669
sheet = Image.new('RGB', (tw * len(order) + 20 * (len(order) + 1), th + 40), '#17151b')
for i, (k, acc, goal) in enumerate(order):
    im = made[k].resize((tw, th), Image.LANCZOS).convert('RGBA')
    ov = Image.new('RGBA', im.size); d = ImageDraw.Draw(ov)
    if k.startswith('bg_end'):
        if k == 'bg_end_planet':
            d.text((tw / 2, th * 0.42), '공개 구조 신호 송출 중.', font=font(16), fill='#ffffff', anchor='mm')
            d.text((tw / 2, th * 0.42 + 30), '여기는 알파. 여기는 알파…', font=font(15), fill=acc, anchor='mm')
    else:
        d.rounded_rectangle((24, 40, tw - 24, 100), 12, fill=(30, 28, 36, 170))
        d.text((tw / 2, 70), '47:12', font=font(26), fill='#ffffff', anchor='mm')
        d.rounded_rectangle((24, 116, tw - 24, 400), 14, fill=(30, 28, 36, 120), outline=acc if k != 'bg_pre' else (120, 118, 128), width=2)
        if goal:
            d.text((40, 150), '현재 목표', font=font(12, False), fill=acc)
            d.text((40, 176), goal, font=font(16), fill='#ffffff')
        d.rounded_rectangle((24, th - 110, tw - 24, th - 56), 12, fill=(30, 28, 36, 170), outline=(90, 86, 100), width=1)
        d.text((tw / 2, th - 83), '힌트', font=font(15), fill='#ffffff', anchor='mm')
    im = Image.alpha_composite(im, ov)
    mask = Image.new('L', (tw, th), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw, th), 34, fill=255)
    sheet.paste(im.convert('RGB'), (20 + i * (tw + 20), 20), mask)
sheet.save(PREV)
for k, v in made.items():
    v.resize((270, 602), Image.LANCZOS).save(PREV.parent / f'thumb_{k}.jpg', quality=82)
print('ok', sorted(p.name for p in OUT.iterdir()))
