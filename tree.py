#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
터미널 3D 크리스마스트리  (tree.py)

  실행:   python3 tree.py          끝내기: Ctrl+C
  필요:   파이썬 3 + numpy         (없으면: python3 -m pip install numpy
                                    / 홈브루 파이썬이면: brew install numpy)

  * 화면 모양은 아래 SCREEN 으로 골라요.
      "shorts" → 세로 쇼츠(9:16) 72칸 x 64줄
      "wide"   → 가로 96칸 x 54줄   (지금 설정)
    터미널 창이 그보다 작으면 안내 문구가 나와요. 줄이 모자라면 글자를 줄여 주세요(Cmd -).
  * 트루컬러(24비트 색)를 써요. iTerm2 나 VS Code 터미널에서 보는 걸 권해요.
    맥 기본 '터미널' 앱은 색이 다르게 나올 수 있어요.

  색·개수·시간은 아래 맨 위쪽 설정에 이름을 붙여 모아 뒀어요.
  예) 「하트 더 많이」 → N_HEARTS, SNOW_HEART_RATIO 를 키우면 돼요.
"""
import math
import os
import signal
import sys
import time

import numpy as np

# ════════════════════════════════════════════════════════════════════
#  색 팔레트  (R, G, B — 0~255)
# ════════════════════════════════════════════════════════════════════
# ── 트리 ──
TREE_DARK     = (16, 78, 38)      # 트리 진한 초록
TREE_LIGHT    = (92, 196, 84)     # 트리 밝은 초록
TREE_SNOW     = (230, 242, 255)   # 가지 끝에 살짝 묻은 눈
TRUNK         = (118, 72, 38)     # 트리 아래 갈색 기둥
FRESH_WHITE   = (255, 255, 255)   # 트리가 방금 생긴 부분이 잠깐 빛나는 흰빛
# ── 땅 ──
GROUND_SNOW   = (214, 228, 246)   # 눈 쌓인 둥근 땅
# ── 빛 효과 ──
SWIRL         = (228, 240, 255)   # 트리를 감아 올라가는 흰 빛 회오리
FLASH         = (255, 252, 236)   # 꼭대기에서 8방향으로 번쩍 퍼지는 빛
# ── 장식 볼 (빨강·금색·은색 번갈아) ──
RED           = (216, 30, 42)     # 빨간 볼
GOLD          = (240, 178, 38)    # 금색 볼
SILVER        = (196, 204, 220)   # 은색 볼
# ── 전구 ──
BULB_WARM     = (255, 222, 160)   # 따뜻한 흰색 전구
BULB_RED      = (255, 58, 48)     # 빨간 전구
BULB_GOLD     = (255, 186, 40)    # 금색 전구
BULB_GREEN    = (70, 255, 112)    # 초록 전구
# ── 꼭대기 별 ──
STAR_GOLD     = (255, 204, 58)    # 금색 별 몸통
STAR_RAY      = (255, 232, 150)   # 별 빛살
# ── 하트 ──
PINK          = (255, 104, 182)   # 분홍 하트 (트리에 달린 것, 눈 사이 작은 것)
# ── 선물 상자 (6개, 색이 다 달라요) ──
GIFT_WHITE    = (236, 236, 242)   # 흰 상자
GIFT_RED      = (204, 34, 46)     # 빨간 상자
GIFT_GREEN    = (36, 150, 72)     # 초록 상자
GIFT_GOLD     = (226, 170, 44)    # 금색 상자
GIFT_BLUE     = (52, 102, 222)    # 파란 상자
GIFT_PINK     = (238, 120, 176)   # 분홍 상자 (여섯 번째)
RIBBON_GOLD   = (255, 208, 70)    # 금색 리본
RIBBON_RED    = (226, 36, 52)     # 빨간 리본
RIBBON_SILVER = (226, 232, 244)   # 은색 리본
# ── 눈 ──
SNOW          = (238, 244, 255)   # 하늘에서 내리는 눈
# ── 우주 배경 ──
SKY_STAR_COLORS = [               # 배경 별 색 (골고루 섞여요)
    (210, 222, 255),              #   푸른빛 흰색
    (255, 246, 228),              #   하얀색
    (255, 228, 180),              #   노르스름한 색
    (186, 204, 255),              #   파르스름한 색
]
MILKY_WAY     = (112, 122, 214)   # 은하수 (푸른 보라)
MILKY_WAY_2   = (176, 112, 196)   # 은하수 반대쪽 끝 (분홍 보라)
PLANET_SILVER = (204, 208, 220)   # 왼쪽 위 고리 달린 은빛 행성
PLANET_RING   = (222, 206, 172)   # 그 행성의 고리
PLANET_BLUE   = (66, 140, 255)    # 오른쪽 위 푸른 행성
PLANET_PURPLE = (164, 92, 226)    # 왼쪽 중간 작은 보랏빛 행성

# ════════════════════════════════════════════════════════════════════
#  개수 · 속도
# ════════════════════════════════════════════════════════════════════
N_SKY_STARS      = 500    # 배경 별 개수
N_ORNAMENTS      = 34     # 장식 볼 개수
N_LIGHTS         = 280    # 전구 개수
LIGHT_TURNS      = 5.5    # 전구 줄이 트리를 감는 바퀴 수
N_HEARTS         = 10     # 트리에 달리는 하트 개수
N_SNOW           = 180    # 내리는 눈송이 개수
SNOW_HEART_RATIO = 0.15   # 눈송이 중 분홍 하트 비율 (0~1)
ROT_PERIOD       = 17.0   # 트리가 한 바퀴 도는 시간(초)
FPS              = 30     # 1초에 다시 그리는 횟수
HOLD_TIME        = 6.0    # 다 생긴 뒤 보여 주는 시간(초)

# ════════════════════════════════════════════════════════════════════
#  생기는 순서 (초) — 처음부터 다시 그릴 때마다 이 순서로
# ════════════════════════════════════════════════════════════════════
T_GROUND, D_GROUND = 0.0, 1.1    # 1. 눈 쌓인 땅이 퍼짐
T_SWIRL,  D_SWIRL  = 0.8, 3.1    # 2. 회오리가 감아 올라가며 트리가 생김
T_BURST,  D_BURST  = T_SWIRL + D_SWIRL, 0.8   # 3. 꼭대기에서 8방향 번쩍
T_ORN,    D_ORN    = 4.5, 1.8    # 4. 장식 볼이 하나씩
ORN_POP            = 0.25        #    볼 하나가 톡 커지는 시간
T_LIGHTS, D_LIGHTS = 6.1, 1.8    # 5. 전구가 아래부터 켜짐
T_STAR,   D_STAR   = 7.8, 0.7    # 6. 꼭대기 별
T_HEARTS, D_HEARTS = 8.4, 1.1    # 7. 하트가 하나씩
T_GIFTS,  D_GIFTS  = 9.3, 1.6    # 8. 선물 상자가 하나씩 올라옴
GIFT_RISE          = 0.5         #    상자 하나가 쑥 올라오는 시간
T_SNOW             = 10.4        # 9. 눈이 내리기 시작
T_DONE             = T_GIFTS + D_GIFTS * 5 / 6 + GIFT_RISE   # 10. 다 생김 → 전구 달리기
LOOP               = T_DONE + HOLD_TIME                      # 한 바퀴 전체 길이

# ════════════════════════════════════════════════════════════════════
#  화면 · 카메라 (보통은 안 바꿔도 돼요)
# ════════════════════════════════════════════════════════════════════
SCREEN = "wide"                     # "shorts" = 세로 쇼츠(9:16), "wide" = 가로 화면
if SCREEN == "shorts":
    W, H = 72, 64                       # 화면 가로 칸, 세로 줄 (글자 1칸 ≈ 가로1:세로2 → 9:16)
    SX, SY = 24.0, 20.0                 # 1 단위 길이가 몇 칸/몇 줄인지 → 늘씬하고 키 큰 트리
    CX, CY = W / 2, 30.0                # 화면 중심
    PIVOT_Y = 1.05                      # 화면 중심에 오는 높이
else:
    W, H = 96, 54
    SX, SY = 32.0, 16.0                 # (글자는 세로로 길쭉해서 SY 는 SX 의 반)
    CX, CY = W / 2, 26.5
    PIVOT_Y = 0.95
RAMP = " .,:;-=+*#%@"               # 밝기 → 글자
CHARS = list(RAMP) + ["♥"]     # 마지막은 ♥
HEART_CODE = len(RAMP)
PITCH = 0.24                        # 살짝 내려다보는 각도
CAM_D = 7.0                         # 원근 정도


def _unit(v):
    v = np.asarray(v, dtype=np.float64)
    return v / np.linalg.norm(v)


LIGHT = _unit([-0.55, 0.62, -0.56])   # 빛: 왼쪽 위 앞에서
HALF = _unit(LIGHT + np.array([0.0, 0.0, -1.0]))
CP, SP = math.cos(PITCH), math.sin(PITCH)

RNG = np.random.default_rng(1225)


def rgbf(c):
    return np.asarray(c, dtype=np.float64) / 255.0


# ════════════════════════════════════════════════════════════════════
#  작은 도우미
# ════════════════════════════════════════════════════════════════════
def clamp01(x):
    return np.clip(x, 0.0, 1.0)


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def back_out(x):          # 톡! 하고 살짝 넘쳤다가 자리 잡는 움직임
    x = clamp01(x)
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2


def normalize_rows(v):
    return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-9)


def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.cos(phi), np.sin(th) * np.sin(phi)], 1)


def rot_angle(T):
    return 2 * math.pi * T / ROT_PERIOD


def view_xform(P, ang, pivot=PIVOT_Y):
    """물체 좌표 → 카메라 좌표 (가운데 축 회전 + 살짝 내려다보기)."""
    c, s = math.cos(ang), math.sin(ang)
    x = P[:, 0] * c + P[:, 2] * s
    z = -P[:, 0] * s + P[:, 2] * c
    y = P[:, 1] - pivot
    return np.stack([x, y * CP + z * SP, -y * SP + z * CP], 1)


def view_normals(N, ang):
    return view_xform(N, ang, pivot=0.0)


def project(V):
    k = CAM_D / (CAM_D + V[:, 2])
    return CX + V[:, 0] * SX * k, CY - V[:, 1] * SY * k


def shade(Nv, base, amb=0.22, dif=0.92, spec=0.0, shin=18.0):
    lam = np.clip(Nv @ LIGHT, 0.0, None)
    out = base * (amb + dif * lam)[:, None]
    if np.any(spec):
        hs = np.clip(Nv @ HALF, 0.0, None) ** shin
        out = out + (np.asarray(spec) * hs)[:, None]
    return out


# ════════════════════════════════════════════════════════════════════
#  모양 만들기 (처음 한 번)
# ════════════════════════════════════════════════════════════════════
TIERS = [  # (아래 높이, 꼭대기 높이, 아래 반지름) — 원뿔 4층
    (0.16, 1.04, 0.95),
    (0.74, 1.38, 0.70),
    (1.05, 1.68, 0.52),
    (1.38, 1.98, 0.33),
]
TREE_TOP = 1.98
SWIRL_H = TREE_TOP + 0.06
STAR_Y = TREE_TOP + 0.10
STAR_R = 0.21
GROUND_R = 1.35
ORN_R = 0.075


def tier_radius(y):
    y = np.asarray(y, dtype=np.float64)
    r = np.zeros_like(y)
    for yb, yt, rb in TIERS:
        t = (yt - y) / (yt - yb)
        r = np.maximum(r, np.where((t >= 0) & (t <= 1), rb * t, 0.0))
    return r


def build_tree(n_total=14000):
    dark, light, snowc = rgbf(TREE_DARK), rgbf(TREE_LIGHT), rgbf(TREE_SNOW)
    areas = np.array([math.pi * rb * math.hypot(rb, yt - yb) for yb, yt, rb in TIERS])
    counts = (n_total * areas / areas.sum()).astype(int)
    Ps, Ns, Cs = [], [], []
    for ti, ((yb, yt, rb), n) in enumerate(zip(TIERS, counts)):
        h = yt - yb
        phi = RNG.uniform(0, 2 * math.pi, n)
        hem = 1 - 0.10 * (0.5 + 0.5 * np.sin(9 * phi + 1.7 * ti)) ** 2    # 물결치는 치맛단
        t = np.sqrt(RNG.uniform(0, 1, n)) * hem
        bump = 1 + 0.045 * np.sin(15 * phi + 22 * t + ti) - RNG.uniform(0, 0.07, n)
        r = rb * t * bump
        y = yt - t * h - 0.05 * t ** 8                                      # 가지 끝이 살짝 처짐
        P = np.stack([r * np.cos(phi), y, r * np.sin(phi)], 1)
        N = normalize_rows(np.stack([h * np.cos(phi), np.full(n, rb), h * np.sin(phi)], 1))
        N = N + RNG.normal(0, 0.28, (n, 3))                                 # 잎이 자글자글하게
        m = clamp01(0.55 * RNG.random(n) + 0.3 * (0.5 + 0.5 * np.sin(11 * phi + 17 * t + ti))
                    + 0.25 * t - 0.1)
        C = dark + (light - dark) * m[:, None]
        if ti + 1 < len(TIERS):                                             # 위층 치맛단 밑 그늘 → 층이 보이게
            yb2, _, rb2 = TIERS[ti + 1]
            C *= (0.3 + 0.7 * clamp01((r - rb2) / 0.16))[:, None]
        edge = clamp01((t / hem - 0.8) / 0.2)
        hem_snow = 0.08 if ti == 0 else 0.35                                # 맨 아래층은 눈을 거의 안 묻혀 초록이 보이게
        snow = RNG.random(n) < edge ** 2 * hem_snow * (0.55 + 0.45 * np.sin(7 * phi + 2 * ti)) + 0.012
        C[snow] = snowc * (0.88 + 0.12 * RNG.random((snow.sum(), 1)))
        N[snow] += [0.0, 0.9, 0.0]
        Ps.append(P); Ns.append(normalize_rows(N)); Cs.append(C)
    # 갈색 기둥
    n = 1400
    phi = RNG.uniform(0, 2 * math.pi, n)
    y = RNG.uniform(0, 0.55, n)
    P = np.stack([0.11 * np.cos(phi), y, 0.11 * np.sin(phi)], 1)
    N = normalize_rows(np.stack([np.cos(phi), np.zeros(n), np.sin(phi)], 1) + RNG.normal(0, 0.15, (n, 3)))
    bark = 0.72 + 0.18 * np.sin(phi * 9 + y * 30) + 0.1 * RNG.random(n)
    Ps.append(P); Ns.append(N); Cs.append(rgbf(TRUNK) * bark[:, None])
    return np.concatenate(Ps), np.concatenate(Ns), np.concatenate(Cs)


def build_ground(n=9000, n_rim=1500):
    phi = RNG.uniform(0, 2 * math.pi, n)
    rn = np.sqrt(RNG.uniform(0, 1, n))
    edge = 1 + 0.04 * np.sin(5 * phi) + 0.03 * np.sin(9 * phi + 1)
    r = GROUND_R * edge * rn
    x, z = r * np.cos(phi), r * np.sin(phi)
    R2 = GROUND_R ** 2
    y = 0.02 * np.sin(6 * x + 1) * np.sin(5 * z) + 0.04 * (1 - r * r / R2)
    dydx = 0.12 * np.cos(6 * x + 1) * np.sin(5 * z) - 0.08 * x / R2
    dydz = 0.10 * np.sin(6 * x + 1) * np.cos(5 * z) - 0.08 * z / R2
    N = normalize_rows(np.stack([-dydx, np.ones(n), -dydz], 1) + RNG.normal(0, 0.12, (n, 3)))
    ao = 0.55 + 0.45 * clamp01((r - 0.15) / 0.75)               # 트리 밑은 살짝 그늘
    C = rgbf(GROUND_SNOW) * ((0.92 + 0.08 * RNG.random(n)) * ao)[:, None]
    # 땅 가장자리 두께
    phr = RNG.uniform(0, 2 * math.pi, n_rim)
    er = GROUND_R * (1 + 0.04 * np.sin(5 * phr) + 0.03 * np.sin(9 * phr + 1))
    Pr = np.stack([er * np.cos(phr), RNG.uniform(-0.05, 0.0, n_rim), er * np.sin(phr)], 1)
    Nr = normalize_rows(np.stack([np.cos(phr), np.full(n_rim, 0.3), np.sin(phr)], 1))
    Cr = rgbf(GROUND_SNOW) * (0.85 + 0.1 * RNG.random((n_rim, 1)))
    P = np.concatenate([np.stack([x, y, z], 1), Pr])
    return P, np.concatenate([N, Nr]), np.concatenate([C, Cr]), np.concatenate([rn, np.ones(n_rim)])


def build_ornaments():
    i = np.arange(N_ORNAMENTS)
    y = np.linspace(0.30, 1.82, N_ORNAMENTS) + RNG.uniform(-0.03, 0.03, N_ORNAMENTS)
    phi = i * 2.39996 + RNG.uniform(-0.3, 0.3, N_ORNAMENTS)
    r = tier_radius(y) + 0.02
    centers = np.stack([r * np.cos(phi), y, r * np.sin(phi)], 1)
    palette = [rgbf(RED), rgbf(GOLD), rgbf(SILVER)]
    cols = np.array([palette[k % 3] for k in i])
    spec = np.array([[0.7, 0.8, 1.1][k % 3] for k in i])
    return centers, cols, spec


def build_lights():
    u = np.linspace(0, 1, N_LIGHTS)
    y = 0.22 + u * 1.71
    phi = u * LIGHT_TURNS * 2 * math.pi
    r = tier_radius(y) + 0.03
    P = np.stack([r * np.cos(phi), y, r * np.sin(phi)], 1)
    palette = [rgbf(BULB_WARM), rgbf(BULB_RED), rgbf(BULB_GOLD), rgbf(BULB_GREEN)]
    C = np.array([palette[k % 4] for k in range(N_LIGHTS)])
    return u, P, C, RNG.uniform(2.0, 6.5, N_LIGHTS), RNG.uniform(0, 2 * math.pi, N_LIGHTS)


GIFT_DEFS = [  # (가로, 높이, 세로, 상자 색, 리본 색)
    (0.34, 0.26, 0.30, GIFT_RED,   RIBBON_GOLD),
    (0.24, 0.32, 0.24, GIFT_WHITE, RIBBON_RED),
    (0.40, 0.18, 0.28, GIFT_GREEN, RIBBON_GOLD),
    (0.22, 0.22, 0.22, GIFT_GOLD,  RIBBON_RED),
    (0.30, 0.24, 0.34, GIFT_BLUE,  RIBBON_SILVER),
    (0.20, 0.34, 0.20, GIFT_PINK,  RIBBON_SILVER),
]
GIFT_SLOTS = [(math.radians(20 + 60 * k), 1.00 if k % 2 == 0 else 1.08) for k in range(6)]
RIBBON_W = 0.03


def build_box(w, h, d, body, ribbon, dens=4500):
    body, ribbon = rgbf(body), rgbf(ribbon)
    Ps, Ns, Rb = [], [], []

    def face(n, P, nrm, rib):
        Ps.append(P); Ns.append(np.tile(nrm, (n, 1))); Rb.append(rib)

    U = RNG.uniform
    # 윗면
    n = int(w * d * dens); x = U(-w / 2, w / 2, n); z = U(-d / 2, d / 2, n)
    face(n, np.stack([x, np.full(n, h), z], 1), [0, 1, 0], (abs(x) < RIBBON_W) | (abs(z) < RIBBON_W))
    # 옆면 ±x
    for sgn in (1, -1):
        n = int(d * h * dens); z = U(-d / 2, d / 2, n); y = U(0, h, n)
        face(n, np.stack([np.full(n, sgn * w / 2), y, z], 1), [sgn, 0, 0],
             (abs(z) < RIBBON_W) | (abs(y - h / 2) < RIBBON_W * 0.8))
    # 옆면 ±z
    for sgn in (1, -1):
        n = int(w * h * dens); x = U(-w / 2, w / 2, n); y = U(0, h, n)
        face(n, np.stack([x, y, np.full(n, sgn * d / 2)], 1), [0, 0, sgn],
             (abs(x) < RIBBON_W) | (abs(y - h / 2) < RIBBON_W * 0.8))
    P = np.concatenate(Ps); N = np.concatenate(Ns).astype(np.float64); rib = np.concatenate(Rb)
    C = np.where(rib[:, None], ribbon, body * (0.92 + 0.08 * RNG.random((len(P), 1))))
    S = np.where(rib, 0.5, 0.12)
    # 위에 매듭 (고리 두 개 + 가운데 매듭)
    sph = fib_sphere(70)
    parts = [((0.062, 0.042, 0.03), (0.052, h + 0.032, 0.0)),
             ((0.062, 0.042, 0.03), (-0.052, h + 0.032, 0.0)),
             ((0.028, 0.026, 0.028), (0.0, h + 0.022, 0.0))]
    for sc, ctr in parts:
        sc = np.array(sc)
        P = np.concatenate([P, sph * sc + ctr])
        N = np.concatenate([N, normalize_rows(sph / sc)])
        C = np.concatenate([C, np.tile(ribbon, (len(sph), 1))])
        S = np.concatenate([S, np.full(len(sph), 0.6)])
    return P, N, C, S


def build_sky():
    rr, cc = np.mgrid[0:H, 0:W].astype(np.float64)
    th = math.radians(27)
    dx = cc - W * 0.5
    dy = (rr - H * 0.42) * 2
    sd = dx * math.sin(th) + dy * math.cos(th)
    n = RNG.random((H, W))
    for _ in range(4):
        n = (n + np.roll(n, 1, 0) + np.roll(n, -1, 0) + np.roll(n, 1, 1) + np.roll(n, -1, 1)
             + np.roll(n, 2, 1) + np.roll(n, -2, 1)) / 7
    n = (n - n.min()) / (n.max() - n.min())
    inten = np.exp(-(sd / 11) ** 2) * (0.25 + 0.95 * n ** 1.5) * 0.10
    inten *= 1 - 0.55 * np.exp(-((sd - 1.5) / 2.2) ** 2)          # 가운데 어두운 먼지 띠
    mix = clamp01(cc / W)[..., None]
    milky = inten[..., None] * (rgbf(MILKY_WAY) * (1 - mix) + rgbf(MILKY_WAY_2) * mix)
    flat = RNG.choice(H * W, N_SKY_STARS, replace=False)
    sr, sc = np.divmod(flat, W)
    base = 0.10 + 0.75 * RNG.random(N_SKY_STARS) ** 2.4
    pal = np.array([rgbf(c) for c in SKY_STAR_COLORS])
    scol = pal[RNG.integers(0, len(pal), N_SKY_STARS)]
    return milky, sr, sc, base, RNG.uniform(0.6, 4.5, N_SKY_STARS), RNG.uniform(0, 2 * math.pi, N_SKY_STARS), scol


PLANETS = [
    dict(cx=13.0, cy=8.0, rad=5.0, color=PLANET_SILVER, ring=True, tilt=-0.38, band=0.06, freq=9.0, ph=0.0),
    dict(cx=61.0, cy=9.0, rad=4.5, color=PLANET_BLUE, ring=False, tilt=0.0, band=0.12, freq=7.0, ph=1.7),
    dict(cx=7.0, cy=33.0, rad=3.0, color=PLANET_PURPLE, ring=False, tilt=0.0, band=0.10, freq=10.0, ph=3.1),
] if SCREEN == "shorts" else [
    dict(cx=15.0, cy=9.0, rad=6.5, color=PLANET_SILVER, ring=True, tilt=-0.38, band=0.06, freq=9.0, ph=0.0),
    dict(cx=84.5, cy=10.0, rad=6.0, color=PLANET_BLUE, ring=False, tilt=0.0, band=0.12, freq=7.0, ph=1.7),
    dict(cx=8.5, cy=29.0, rad=3.6, color=PLANET_PURPLE, ring=False, tilt=0.0, band=0.10, freq=10.0, ph=3.1),
]

TREE_P, TREE_N, TREE_C = build_tree()
GRD_P, GRD_N, GRD_C, GRD_RN = build_ground()
ORN_CTR, ORN_COL, ORN_SPEC = build_ornaments()
ORN_W = RNG.uniform(1.5, 4.0, N_ORNAMENTS)
ORN_PH = RNG.uniform(0, 2 * math.pi, N_ORNAMENTS)
SPHERE = fib_sphere(90)
LT_U, LT_P, LT_C, LT_W, LT_PH = build_lights()
GIFTS = [build_box(*g) for g in GIFT_DEFS]
MILKY, ST_R, ST_C, ST_BASE, ST_W, ST_PH, ST_COL = build_sky()

SN_TOP, SN_RANGE = 3.0, 5.0
SN_X = RNG.uniform(-1.7, 1.7, N_SNOW)
SN_Z = RNG.uniform(-1.3, 1.3, N_SNOW)
SN_Y0 = RNG.uniform(0, SN_RANGE, N_SNOW)
SN_V = RNG.uniform(0.22, 0.45, N_SNOW)
SN_W = RNG.uniform(0.6, 1.6, N_SNOW)
SN_PH = RNG.uniform(0, 2 * math.pi, N_SNOW)
SN_HEART = RNG.random(N_SNOW) < SNOW_HEART_RATIO
SN_E = T_SNOW + RNG.random(N_SNOW) * 1.0


def new_loop_state(loop_start):
    """한 바퀴마다: 하트·선물이 생기는 순간 앞쪽에 보이도록 자리를 정해요."""
    rng = np.random.default_rng(int(loop_start * 10) + 7)
    ys = np.linspace(0.40, 1.75, N_HEARTS)
    rng.shuffle(ys)
    hearts = []
    for i in range(N_HEARTS):
        ti = T_HEARTS + i * D_HEARTS / N_HEARTS
        phi = rot_angle(loop_start + ti + 0.4) - math.pi / 2 + rng.uniform(-1.0, 1.0)
        r = float(tier_radius(ys[i])) + 0.05
        hearts.append((r * math.cos(phi), ys[i], r * math.sin(phi)))
    used, order = set(), []
    for gi in range(len(GIFT_DEFS)):
        tg = T_GIFTS + gi * D_GIFTS / len(GIFT_DEFS)
        A = rot_angle(loop_start + tg + 0.3)
        k = min((k for k in range(len(GIFT_SLOTS)) if k not in used),
                key=lambda k: math.sin(GIFT_SLOTS[k][0] - A))
        used.add(k); order.append(k)
    return dict(hearts=np.array(hearts), gift_slot=order)


# ════════════════════════════════════════════════════════════════════
#  한 장면 모으기 (단단한 것 / 빛나는 것 / 글자 덧씌우기)
# ════════════════════════════════════════════════════════════════════
HALO = [(0, 0, 1.0), (-1, 0, 0.45), (1, 0, 0.45), (0, -1, 0.22), (0, 1, 0.22)]
DOT = [(0, 0, 1.0)]


class Scene:
    def __init__(self):
        self.sol, self.glo, self.ovl = [], [], []

    def solid(self, V, rgb):
        c, r = project(V)
        self.sol.append((c, r, V[:, 2], rgb))

    def solid_screen(self, c, r, z, rgb):
        self.sol.append((c, r, z, rgb))

    def glow(self, c, r, z, rgb, halo=True):
        c = np.atleast_1d(np.asarray(c, dtype=np.float64))
        r = np.broadcast_to(np.asarray(r, dtype=np.float64), c.shape)
        z = np.broadcast_to(np.asarray(z, dtype=np.float64), c.shape)
        rgb = np.broadcast_to(np.asarray(rgb, dtype=np.float64), c.shape + (3,))
        self.glo.append((c, r, z, rgb, halo))

    def glow_view(self, V, rgb, halo=True):
        c, r = project(V)
        self.glow(c, r, V[:, 2], rgb, halo)

    def overlay(self, c, r, z, code, rgb):
        self.ovl.append((c, r, z, code, rgb))

    def resolve(self):
        zbuf = np.full(H * W, np.inf)
        scol = np.zeros((H * W, 3))
        if self.sol:
            c = np.concatenate([s[0] for s in self.sol])
            r = np.concatenate([s[1] for s in self.sol])
            z = np.concatenate([s[2] for s in self.sol])
            rgb = np.concatenate([s[3] for s in self.sol])
            ci, ri = np.floor(c).astype(np.int64), np.floor(r).astype(np.int64)
            m = (ci >= 0) & (ci < W) & (ri >= 0) & (ri < H)
            idx, z, rgb = (ri * W + ci)[m], z[m], rgb[m]
            order = np.lexsort((z, idx))          # 칸마다 가장 가까운 점이 이겨요
            ids = idx[order]
            first = np.ones(len(ids), dtype=bool)
            first[1:] = ids[1:] != ids[:-1]
            win = order[first]
            zbuf[idx[win]] = z[win]
            scol[idx[win]] = rgb[win]
        glow = np.zeros((H * W, 3))
        for c, r, z, rgb, halo in self.glo:
            ci0, ri0 = np.floor(c).astype(np.int64), np.floor(r).astype(np.int64)
            for dc, dr, w in (HALO if halo else DOT):
                ci, ri = ci0 + dc, ri0 + dr
                m = (ci >= 0) & (ci < W) & (ri >= 0) & (ri < H)
                idx = ri[m] * W + ci[m]
                vis = z[m] < zbuf[idx] + 0.08      # 트리 뒤에 숨은 빛은 안 보여요
                np.add.at(glow, idx[vis], rgb[m][vis] * w)   # 겹치면 더 밝게
        return zbuf, scol, glow


# ════════════════════════════════════════════════════════════════════
#  배경: 별 · 은하수 · 행성
# ════════════════════════════════════════════════════════════════════
def draw_planet(bg, special, p, T):
    pc = p["cx"] + 0.7 * math.sin(T * 2 * math.pi / 9 + p["ph"])
    pr = p["cy"] + 0.6 * math.sin(T * 2 * math.pi / 6.5 + p["ph"] * 1.3)
    rx = p["rad"]; ry = rx * 0.5
    ext = 2.3 if p["ring"] else 1.4
    c0, c1 = max(0, int(pc - rx * ext) - 1), min(W, int(pc + rx * ext) + 2)
    r0, r1 = max(0, int(pr - ry * ext) - 1), min(H, int(pr + ry * ext) + 2)
    if c0 >= c1 or r0 >= r1:
        return
    rr, cc = np.mgrid[r0:r1, c0:c1].astype(np.float64)
    dx = (cc + 0.5 - pc) / rx
    dy = (rr + 0.5 - pr) / ry
    d2 = dx * dx + dy * dy
    inside = d2 < 1
    nz = -np.sqrt(clamp01(1 - d2))
    lam = np.clip(dx * LIGHT[0] - dy * LIGHT[1] + nz * LIGHT[2], 0, None)
    tex = 1 + p["band"] * np.sin(dy * p["freq"] + 1.5 * np.sin(dx * 2.3 + p["ph"]))
    lum = 0.035 + 1.05 * lam ** 0.85 * tex                # 한쪽만 밝게
    col = rgbf(p["color"])
    sub_bg, sub_sp = bg[r0:r1, c0:c1], special[r0:r1, c0:c1]
    sub_bg[inside] = (col * lum[..., None])[inside]
    sub_sp[inside] = -1
    if p["ring"]:
        ca, sa = math.cos(p["tilt"]), math.sin(p["tilt"])
        u = dx * ca + dy * sa
        v = (-dx * sa + dy * ca) / 0.30
        rad = np.sqrt(u * u + v * v)
        ring = (rad > 1.35) & (rad < 2.2) & ~((rad > 1.72) & (rad < 1.80))
        show = ring & ((v > 0) | ~inside)                  # 뒤쪽 고리는 행성에 가려요
        rb = (0.45 + 0.35 * (0.5 + 0.5 * np.sin(rad * 21))) * (0.75 + 0.35 * np.clip(-u / 2.2, -1, 1))
        sub_bg[show] = (rgbf(PLANET_RING) * rb[..., None])[show]
        sub_sp[show] = -1
    else:
        rim = (d2 >= 1) & (d2 < 1.45)                      # 옅은 대기 빛
        glowr = (0.16 * (1 - (d2 - 1) / 0.45) * (0.4 + clamp01(-dx)))
        sub_bg[rim] = np.maximum(sub_bg[rim], (col * glowr[..., None])[rim])


def draw_sky(T):
    bg = MILKY.copy()
    special = np.full((H, W), -1, dtype=np.int64)
    tw = 0.5 + 0.5 * np.sin(ST_W * T + ST_PH)
    b = ST_BASE * (0.25 + 0.75 * tw)
    bg[ST_R, ST_C] = np.maximum(bg[ST_R, ST_C], ST_COL * b[:, None])
    plus = b > 0.45
    special[ST_R[plus], ST_C[plus]] = RAMP.index("+")
    star = b > 0.62
    special[ST_R[star], ST_C[star]] = RAMP.index("*")
    for p in PLANETS:
        draw_planet(bg, special, p, T)
    return bg, special


# ════════════════════════════════════════════════════════════════════
#  장면 요소들
# ════════════════════════════════════════════════════════════════════
def draw_ground(S, tl, A):
    e = ease_out((tl - T_GROUND) / D_GROUND)
    if e <= 0:
        return
    vis = GRD_RN <= e + 1e-6
    V = view_xform(GRD_P[vis], A)
    rgb = shade(view_normals(GRD_N[vis], A), GRD_C[vis], amb=0.24, dif=0.72)
    settle = 1 - clamp01((tl - T_GROUND - D_GROUND) / 0.3)
    edge = np.exp(-(e - GRD_RN[vis]) / 0.05) * settle      # 퍼지는 가장자리가 반짝
    S.solid(V, rgb + 0.6 * edge[:, None])


def draw_tree(S, tl, A):
    s = clamp01((tl - T_SWIRL) / D_SWIRL)
    if s <= 0:
        return
    vis = TREE_P[:, 1] <= s * SWIRL_H                      # 회오리가 지나간 높이까지
    P = TREE_P[vis]
    rgb = shade(view_normals(TREE_N[vis], A), TREE_C[vis])
    born = T_SWIRL + P[:, 1] / SWIRL_H * D_SWIRL
    w = np.exp(-np.clip(tl - born, 0, None) / 0.28)[:, None]   # 방금 생긴 곳은 하얗게
    rgb = rgb * (1 - w) + w * rgbf(FRESH_WHITE) * 1.25
    S.solid(view_xform(P, A), rgb)


def draw_swirl(S, tl, A):
    s_raw = (tl - T_SWIRL) / D_SWIRL
    if s_raw < 0:
        return
    fade = 1.0 if s_raw <= 1 else max(0.0, 1 - (tl - T_BURST) / 0.35)
    if fade <= 0:
        return
    s = min(s_raw, 1.0)
    trail = 0.26
    u = np.linspace(s - trail, s, 150)
    u = u[u >= 0]
    f = (u - (s - trail)) / trail                          # 0 꼬리 → 1 머리
    y = u * SWIRL_H
    rad = 0.98 * (1 - y / 2.15) + 0.14
    col = rgbf(SWIRL)
    for k in range(2):
        phi = k * math.pi + u * 3.2 * 2 * math.pi
        P = np.stack([rad * np.cos(phi), y, rad * np.sin(phi)], 1)
        V = view_xform(P, A)
        I = (f ** 1.6) * 1.1 * fade
        S.glow_view(V, col * I[:, None])
        S.glow_view(V[-1:], col * 1.4 * fade)              # 밝은 머리
        if len(V) > 4:                                     # 흩날리는 반짝이
            j = RNG.integers(0, len(V), 8)
            Vj = V[j] + RNG.normal(0, 0.05, (8, 3))
            S.glow_view(Vj, col * (RNG.random((8, 1)) * 0.9 * f[j, None] * fade), halo=False)


def draw_burst(S, tl, A):
    q = (tl - T_BURST) / D_BURST
    if not 0 <= q < 1:
        return
    V = view_xform(np.array([[0.0, TREE_TOP + 0.06, 0.0]]), A)
    c0, r0 = project(V)
    z = V[0, 2] - 0.6
    reach = 1 - (1 - q) ** 2.5
    L = 4 + 22 * reach
    amp = (1 - q) ** 1.3
    col = rgbf(FLASH)
    d = np.linspace(0, L, 45)
    for k in range(8):
        a = k * math.pi / 4
        I = amp * (0.35 + 0.9 * (d / L) ** 2) * 1.4
        S.glow(c0[0] + d * math.cos(a), r0[0] - d * math.sin(a) * 0.5, z, col * I[:, None])
    ang = RNG.uniform(0, 2 * math.pi, 40)
    rr = RNG.uniform(0, 3.5, 40)
    S.glow(c0[0] + rr * np.cos(ang), r0[0] + rr * np.sin(ang) * 0.5, z, col * (amp * 1.2))


def draw_ornaments(S, tl, A, T):
    starts = T_ORN + np.arange(N_ORNAMENTS) * D_ORN / N_ORNAMENTS
    e = (tl - starts) / ORN_POP
    vis = np.flatnonzero(e > 0)
    if len(vis) == 0:
        return
    sc = back_out(np.minimum(e[vis], 1.0))                 # 톡톡 커지기
    n = len(SPHERE)
    P = (ORN_CTR[vis][:, None, :] + SPHERE[None] * (ORN_R * sc)[:, None, None]).reshape(-1, 3)
    Nrm = np.tile(SPHERE, (len(vis), 1))
    base = np.repeat(ORN_COL[vis], n, 0)
    spec = np.repeat(ORN_SPEC[vis], n)
    rgb = shade(view_normals(Nrm, A), base, amb=0.18, dif=0.95, spec=spec, shin=24)
    S.solid(view_xform(P, A), rgb)
    # 반짝이는 하이라이트
    Vc = view_xform(ORN_CTR[vis], A)
    c, r = project(Vc)
    tw = np.maximum(0, np.sin(ORN_W[vis] * T + ORN_PH[vis])) ** 10
    pop = np.exp(-np.maximum(tl - starts[vis] - ORN_POP * 0.5, 0) / 0.12)
    I = (0.75 * tw + 1.3 * pop)[:, None] * np.ones(3)
    S.glow(c - 0.7, r - 0.35, Vc[:, 2] - ORN_R * 1.2, I, halo=False)


def draw_lights(S, tl, A, T):
    on = T_LIGHTS + LT_U * D_LIGHTS
    vis = np.flatnonzero(tl >= on)
    if len(vis) == 0:
        return
    b = 0.62 + 0.38 * np.sin(LT_W[vis] * T + LT_PH[vis])            # 각자 반짝반짝
    b = b + 1.3 * np.exp(-(tl - on[vis]) / 0.12)                     # 켜지는 순간 번쩍
    if tl > T_DONE:                                                  # 줄줄이 달려가는 빛
        k = clamp01((tl - T_DONE) / 0.4)
        wave = np.maximum(0, np.cos(2 * math.pi * (vis / 14.0 - (tl - T_DONE) * 1.4))) ** 6
        b = b * (1 - 0.45 * k) + k * 1.5 * wave
    S.glow_view(view_xform(LT_P[vis], A), LT_C[vis] * (b * 1.05)[:, None])


def star_shape(dx, dy):
    ang = np.arctan2(-dy, dx) - math.pi / 2
    seg = 2 * math.pi / 5
    m = np.mod(ang + seg / 2, seg) - seg / 2
    rb = 1 - (np.abs(m) / (seg / 2)) * (1 - 0.42)
    return np.hypot(dx, dy) < rb, m


def draw_star(S, tl, A, T):
    e = (tl - T_STAR) / D_STAR
    if e <= 0:
        return
    sc = float(back_out(min(e, 1.0)))
    V = view_xform(np.array([[0.0, STAR_Y, 0.0]]), A)
    c0, r0 = (float(a[0]) for a in project(V))
    z = V[0, 2] - 0.4
    k = CAM_D / (CAM_D + V[0, 2])
    Ro = STAR_R * max(SX, 1.6 * SY) * k * sc           # 쇼츠 화면에서도 별 크기 유지
    if Ro < 0.4:
        return
    cmin, cmax = int(math.floor(c0 - Ro * 1.1)), int(math.ceil(c0 + Ro * 1.1))
    rmin, rmax = int(math.floor(r0 - Ro * 0.6)), int(math.ceil(r0 + Ro * 0.6))
    rr, cc = np.mgrid[rmin:rmax + 1, cmin:cmax + 1].astype(np.float64)
    rr, cc = rr.ravel(), cc.ravel()
    cov = np.zeros(len(rr))
    for oy in (1 / 6, 3 / 6, 5 / 6):
        for ox in (1 / 6, 3 / 6, 5 / 6):
            ins, _ = star_shape((cc + ox - c0) / Ro, (rr + oy - r0) / (Ro * 0.5))
            cov += ins
    cov /= 9
    keep = cov >= 0.3
    dx = (cc[keep] + 0.5 - c0) / Ro
    dy = (rr[keep] + 0.5 - r0) / (Ro * 0.5)
    _, m = star_shape(dx, dy)
    rad = np.maximum(np.hypot(dx, dy), 1e-6)
    tx, ty = -dy / rad, dx / rad                       # 팔마다 한쪽 면은 밝고 한쪽은 어둡게
    nx = dx / rad * 0.6 + np.sign(m) * tx * 0.5
    ny = dy / rad * 0.6 + np.sign(m) * ty * 0.5
    Nv = normalize_rows(np.stack([nx, -ny, -np.ones_like(nx)], 1))
    pop = math.exp(-max(tl - T_STAR - D_STAR * 0.6, 0) / 0.2)
    rgb = shade(Nv, np.tile(rgbf(STAR_GOLD), (len(nx), 1)), amb=0.35, dif=0.95, spec=0.6, shin=12) * 1.1
    rgb = rgb + 0.8 * pop
    S.solid_screen(cc[keep] + 0.5, rr[keep] + 0.5, np.full(len(nx), z), rgb)
    # 별빛 후광과 빛살
    tw = 0.75 + 0.25 * math.sin(T * 5.3)
    d = np.hypot((cc + 0.5 - c0) / Ro, (rr + 0.5 - r0) / (Ro * 0.5))
    I = 0.45 * tw * np.maximum(0, 1 - d / 2.2) ** 2
    S.glow(cc + 0.5, rr + 0.5, z, rgbf(STAR_RAY) * I[:, None], halo=False)
    ray = rgbf(STAR_RAY)
    for kk in range(8):
        a = kk * math.pi / 4 + math.pi / 2
        main = kk % 2 == 0
        L = Ro * ((2.1 + 0.6 * math.sin(T * 6 + kk)) if main else (1.35 + 0.5 * math.sin(T * 7.3 + kk * 2)))
        dd = np.linspace(Ro * 0.6, L, 30)
        flick = 0.55 + 0.45 * math.sin(T * (4.0 + kk) + kk * 1.7)
        Ii = (1 - (dd - Ro * 0.6) / max(L - Ro * 0.6, 1e-6)) ** 1.5 * (0.9 if main else 0.6) * flick
        S.glow(c0 + dd * math.cos(a), r0 - dd * math.sin(a) * 0.5, z, ray * (Ii + pop)[:, None], halo=False)


def draw_hearts(S, tl, A, T, st):
    pink = rgbf(PINK)
    for i in range(N_HEARTS):
        ti = T_HEARTS + i * D_HEARTS / N_HEARTS
        if tl < ti:
            continue
        V = view_xform(st["hearts"][i:i + 1], A)
        c, r = project(V)
        x = (T * 1.15 + i * 0.37) % 1.0                    # 두근(크게) 두근(작게)
        beat = (math.exp(-(x / 0.07) ** 2) + math.exp(-((x - 1) / 0.07) ** 2)
                + 0.65 * math.exp(-((x - 0.22) / 0.07) ** 2))
        pop = math.exp(-(tl - ti) / 0.25)
        b = 0.45 + 0.75 * beat + 1.2 * pop
        S.overlay(c, r, V[:, 2] - 0.02, HEART_CODE, np.tile(pink * min(b, 1.6), (1, 1)))
        S.glow(c, r, V[:, 2] - 0.02, pink * (0.28 * beat + 0.8 * pop))


def draw_gifts(S, tl, A, st):
    n = len(GIFT_DEFS)
    for gi in range(n):
        tg = T_GIFTS + gi * D_GIFTS / n
        e = (tl - tg) / GIFT_RISE
        if e <= 0:
            continue
        w, h, d = GIFT_DEFS[gi][:3]
        theta, dist = GIFT_SLOTS[st["gift_slot"][gi]]
        yaw = theta * 0.7 + gi
        cy, sy = math.cos(yaw), math.sin(yaw)
        P, N, C, Sp = GIFTS[gi]
        yoff = -(h + 0.1) * (1 - float(back_out(min(e, 1.0))))   # 땅에서 쑥
        Pw = np.stack([P[:, 0] * cy - P[:, 2] * sy + dist * math.cos(theta),
                       P[:, 1] + yoff,
                       P[:, 0] * sy + P[:, 2] * cy + dist * math.sin(theta)], 1)
        Nw = np.stack([N[:, 0] * cy - N[:, 2] * sy, N[:, 1], N[:, 0] * sy + N[:, 2] * cy], 1)
        vis = Pw[:, 1] >= -0.005
        if not vis.any():
            continue
        rgb = shade(view_normals(Nw[vis], A), C[vis], amb=0.22, dif=0.9, spec=Sp[vis], shin=20)
        S.solid(view_xform(Pw[vis], A), rgb)
        if e < 1.5:                                        # 올라올 때 눈가루 반짝
            a = np.linspace(0, 2 * math.pi, 12, endpoint=False) + gi
            rr = max(w, d) * 0.75
            Pp = np.stack([dist * math.cos(theta) + rr * np.cos(a), np.full(12, 0.03),
                           dist * math.sin(theta) + rr * np.sin(a)], 1)
            S.glow_view(view_xform(Pp, A), rgbf(SNOW) * 0.6 * (1 - e / 1.5), halo=False)


def draw_snow(S, tl, T):
    if tl < T_SNOW:
        return
    alpha = clamp01((tl - SN_E) / 0.6)                     # 사르르 나타나기
    on = alpha > 0
    if not on.any():
        return
    y = SN_TOP - np.mod(T * SN_V + SN_Y0, SN_RANGE)
    x = SN_X + 0.09 * np.sin(SN_W * T + SN_PH)             # 살랑살랑
    z = SN_Z + 0.05 * np.cos(SN_W * 0.7 * T + SN_PH)
    V = view_xform(np.stack([x, y, z], 1)[on], 0.0)
    c, r = project(V)
    a = alpha[on]
    near = V[:, 2] < -0.5
    mid = (~near) & (V[:, 2] < 0.6)
    code = np.where(near, RAMP.index("*"), np.where(mid, RAMP.index("+"), RAMP.index(".")))
    bright = np.where(near, 1.0, np.where(mid, 0.78, 0.55)) * a
    rgb = rgbf(SNOW) * bright[:, None]
    hearts = SN_HEART[on]
    code = np.where(hearts, HEART_CODE, code)
    rgb[hearts] = rgbf(PINK) * (0.6 + 0.4 * bright[hearts, None])
    S.overlay(c, r, V[:, 2], code, rgb)


# ════════════════════════════════════════════════════════════════════
#  합치기 → 글자 + 색
# ════════════════════════════════════════════════════════════════════
def render(tl, T, st):
    A = rot_angle(T)
    fade = float(clamp01((LOOP - tl) / 0.45))              # 다시 시작하기 직전 살짝 어두워짐
    bg, special = draw_sky(T)
    S = Scene()
    draw_ground(S, tl, A)
    draw_tree(S, tl, A)
    draw_swirl(S, tl, A)
    draw_burst(S, tl, A)
    draw_ornaments(S, tl, A, T)
    draw_lights(S, tl, A, T)
    draw_star(S, tl, A, T)
    draw_hearts(S, tl, A, T, st)
    draw_gifts(S, tl, A, st)
    draw_snow(S, tl, T)
    zbuf, scol, glow = S.resolve()

    Cc = bg.reshape(-1, 3).copy()
    smask = np.isfinite(zbuf)
    Cc[smask] = scol[smask] * fade + Cc[smask] * (1 - fade)
    Cc += glow * fade
    v = Cc.max(axis=1)
    Cc = clamp01(Cc + 0.85 * np.clip(v - 1, 0, None)[:, None])   # 아주 밝으면 하얗게
    gv = glow.max(axis=1) * fade
    scene = (smask & (fade > 0.3)) | (gv > 0.03)
    lv = np.where(scene, np.clip(v, 0, 1) ** 0.7, np.clip(v, 0, 1) * 1.3)   # 배경은 옅게
    idx = np.clip(np.rint(lv * (len(RAMP) - 1)), 0, len(RAMP) - 1).astype(np.int64)
    if fade > 0.3:
        idx[smask] = np.maximum(idx[smask], 1)
    sp = special.ravel()
    use = (sp >= 0) & ~(smask & (fade > 0.3)) & (gv < 0.25)
    idx[use] = sp[use]
    if fade > 0.05:
        for c, r, z, code, rgb in S.ovl:
            ci, ri = np.floor(c).astype(np.int64), np.floor(r).astype(np.int64)
            code = np.broadcast_to(code, ci.shape)
            m = (ci >= 0) & (ci < W) & (ri >= 0) & (ri < H)
            k = ri[m] * W + ci[m]
            ok = z[m] < zbuf[k]
            idx[k[ok]] = code[m][ok]
            Cc[k[ok]] = clamp01(rgb[m][ok] * fade)
    rgb8 = (Cc ** 0.8 * 255 + 0.5).astype(np.int64)
    key = (rgb8[:, 0] << 16) | (rgb8[:, 1] << 8) | rgb8[:, 2]
    return idx.reshape(H, W), key.reshape(H, W)


def encode(chars, key, ox, oy):
    out = []
    for r in range(H):
        parts = [f"\x1b[{oy + r + 1};{ox + 1}H"]
        prev = -1
        for code, k in zip(chars[r].tolist(), key[r].tolist()):
            if code == 0:
                parts.append(" ")
                continue
            if k != prev:
                parts.append(f"\x1b[38;2;{k >> 16};{(k >> 8) & 255};{k & 255}m")
                prev = k
            parts.append(CHARS[code])
        out.append("".join(parts))
    return "\x1b[48;2;0;0;0m" + "".join(out)


# ════════════════════════════════════════════════════════════════════
#  실행
# ════════════════════════════════════════════════════════════════════
def _on_term(signum, frame):
    raise KeyboardInterrupt


def term_size():
    try:
        s = os.get_terminal_size(sys.stdout.fileno())
        return s.columns, s.lines
    except OSError:
        return W, H


def main():
    signal.signal(signal.SIGTERM, _on_term)
    out = sys.stdout
    out.write("\x1b[?1049h\x1b[?25l\x1b[0m\x1b[48;2;0;0;0m\x1b[2J")   # 따로 쓰는 화면, 커서 숨김
    out.flush()
    t0 = time.perf_counter()
    next_t = t0
    loop_idx, st, last_size = -1, None, None
    try:
        while True:
            now = time.perf_counter()
            T = now - t0
            li = int(T // LOOP)
            tl = T - li * LOOP
            if li != loop_idx:
                loop_idx, st = li, new_loop_state(li * LOOP)
            cols, lines = term_size()
            if (cols, lines) != last_size:
                out.write("\x1b[0m\x1b[48;2;0;0;0m\x1b[2J")
                last_size = (cols, lines)
            if cols < W or lines < H:
                msg = f"터미널 창을 {W}x{H} 이상으로 키워 주세요 (지금 {cols}x{lines})"
                out.write(f"\x1b[H\x1b[38;2;255;220;160m{msg}\x1b[K")
            else:
                chars, key = render(tl, T, st)
                out.write(encode(chars, key, (cols - W) // 2, (lines - H) // 2))
            out.flush()
            next_t += 1.0 / FPS
            delay = next_t - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            elif delay < -0.25:
                next_t = time.perf_counter()
    except KeyboardInterrupt:
        pass
    finally:
        out.write("\x1b[0m\x1b[?25h\x1b[?1049l")            # 글자색·커서 원래대로
        out.flush()


if __name__ == "__main__":
    main()
