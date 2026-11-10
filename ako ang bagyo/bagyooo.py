import tkinter as tk
import tkinter.font as tkfont
import math
import time
import random
import ctypes
import re
import gc
from functools import lru_cache, partial

lrc = """
[01:48.81]Tinatali mo ko sa pag asa
[01:54.48]@Kap
[01:56.25]Matakot na kayo
[02:01.12]Ako, ako, ako ang bagyoooo
[02:05.86]Kulimlim ng langit sainyong dalawa
[02:11.42]Bulong ko sa hangin sana di kayo masaya
[02:16.97]Sa tibay ng bahay na titirhan nyo
[02:22.91]Tatangayin ko bawat yero
"""

start_at = 108.81
end_at = 148.17
last_line_duration = 8.0

transparent_color = "#010101"
font_family = "Montserrat"
base_div = 36
text_color = "#E6F2F0"
shadow_color = "#02090B"

tint_color = "#071317"
tint_alpha = 0.66
use_blur = False
lightning_flash = True
dpi_aware = False

color_steps = 128

word_fade_in = 1.1
line_fade_out = 1.2
max_word_gap = 0.9

keywords = {
    "bagyo": dict(color="#B9F3E8", glow="#287F83", scale=2.1, event="strike"),
    "ako": dict(color="#C8E8E5", glow="#376F73", scale=1.45, event=None),
    "yero": dict(color="#D2E2DF", glow="#617C7A", scale=1.9, event="yero"),
    "matakot": dict(color="#E6A18C", glow="#8D4437", scale=1.5, event=None),
    "tatangayin": dict(color="#A6E8E2", glow="#347F83", scale=1.5, event="gust"),
    "kulimlim": dict(color="#AEBFBE", glow="#405B5C", scale=1.4, event=None),
    "masaya": dict(color="#D98A9B", glow="#873C50", scale=1.4, event=None),
    "kayo": dict(color="#D98A9B", glow="#873C50", scale=1.2, event=None),
    "dalawa": dict(color="#D98A9B", glow="#873C50", scale=1.3, event=None),
}

zones = [
    (0.28, 0.42), (0.72, 0.44), (0.28, 0.74),
    (0.72, 0.72), (0.50, 0.58), (0.50, 0.38),
]

invisible = re.compile("[\u200b-\u200f\u202a-\u202e\u2060\ufeff]")
stamp = re.compile(r"^\s*\[(\d+):(\d+(?:\.\d+)?)\](.*)$")


class Gfx:
    def bind(self, canvas):
        call = canvas.tk.call
        cw = canvas._w
        self.coords = partial(call, cw, "coords")
        self.cfg = partial(call, cw, "itemconfigure")
        self.move = partial(call, cw, "move")
        self.delete = partial(call, cw, "delete")
        self.raise_ = partial(call, cw, "raise")


gfx = Gfx()


def load_lyrics():
    entries = []
    for raw in invisible.sub("", lrc).splitlines():
        m = stamp.match(raw)
        if m:
            entries.append((int(m.group(1)) * 60 + float(m.group(2)), m.group(3).strip()))
    entries.sort(key=lambda e: e[0])
    lines = []
    for i, (ts, text) in enumerate(entries):
        if not text or ts < start_at - 0.01 or ts >= end_at - 0.01:
            continue
        nxt = entries[i + 1][0] if i + 1 < len(entries) else ts + last_line_duration
        lines.append((ts - start_at, text, max(2.0, nxt - ts)))
    if not lines:
        raise SystemExit("No lyric lines found. Paste your timestamped lyrics into lrc.")
    base = lines[0][0]
    return [(s - base, t, d) for s, t, d in lines]


def norm(word):
    return re.sub(r"\W+", "", word.lower())


@lru_cache(maxsize=None)
def hex_to_rgb(c):
    return int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)


@lru_cache(maxsize=32768)
def _mix(c1, c2, q):
    t = q / color_steps
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1 + (r2 - r1) * t),
        int(g1 + (g2 - g1) * t),
        int(b1 + (b2 - b1) * t),
    )


def mix(c1, c2, t):
    if t <= 0.0:
        return c1
    if t >= 1.0:
        return c2
    return _mix(c1, c2, int(t * color_steps + 0.5))


def clamp01(v):
    return max(0.0, min(1.0, v))


def ease_out_cubic(p):
    return 1 - (1 - p) ** 3


def ease_in_cubic(p):
    return p ** 3


def ease_in_out(p):
    return p * p * (3 - 2 * p)


def set_dpi_aware():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def fine_timer(on):
    try:
        winmm = ctypes.windll.winmm
        (winmm.timeBeginPeriod if on else winmm.timeEndPeriod)(1)
    except Exception:
        pass


def _hwnd(win):
    win.update_idletasks()
    return ctypes.windll.user32.GetParent(win.winfo_id())


def make_click_through(win):
    try:
        user32 = ctypes.windll.user32
        hwnd = _hwnd(win)
        style = user32.GetWindowLongW(hwnd, -20)
        user32.SetWindowLongW(hwnd, -20, style | 0x80000 | 0x20 | 0x80 | 0x08000000)
    except Exception:
        pass


def enable_blur(win, tint_hex, opacity=0.6):
    try:
        class Accent(ctypes.Structure):
            _fields_ = [("state", ctypes.c_int), ("flags", ctypes.c_int),
                        ("color", ctypes.c_uint), ("anim", ctypes.c_int)]

        class Data(ctypes.Structure):
            _fields_ = [("attr", ctypes.c_int), ("data", ctypes.c_void_p),
                        ("size", ctypes.c_size_t)]

        r, g, b = hex_to_rgb(tint_hex)
        argb = (int(opacity * 255) << 24) | (b << 16) | (g << 8) | r
        accent = Accent(4, 2, argb, 0)
        data = Data(19, ctypes.cast(ctypes.pointer(accent), ctypes.c_void_p),
                    ctypes.sizeof(accent))
        ctypes.windll.user32.SetWindowCompositionAttribute(_hwnd(win), ctypes.byref(data))
    except Exception:
        pass


class Drop:
    __slots__ = ("sw", "sh", "vy", "x", "y", "stop_at", "gone", "item", "wf")

    layers = [
        (0.40, (500, 800), 1, "#405B60", 1.4),
        (0.40, (800, 1200), 1, "#68888A", 1.9),
        (0.20, (1200, 1700), 2, "#A6C9C5", 2.4),
    ]

    def __init__(self, canvas, sw, sh, layer, stop_at):
        (v0, v1), width, color, self.wf = layer
        self.sw, self.sh = sw, sh
        self.vy = random.uniform(v0, v1)
        self.x = random.uniform(-sw * 0.3, sw)
        self.y = -random.uniform(0, sh * 1.1)
        self.stop_at = stop_at
        self.gone = False
        self.item = canvas.create_line(0, -50, 0, -49, fill=color, width=width,
                                       capstyle="round", tags=("rain",))

    def update(self, dt, wind, ending, t):
        vx = wind * self.wf
        vy = self.vy
        x = self.x + vx * dt
        y = self.y + vy * dt
        if y > self.sh + 40 or x > self.sw + 80:
            if ending and t >= self.stop_at:
                self.gone = True
                gfx.delete(self.item)
                return
            y = -random.uniform(10, 120)
            x = random.uniform(-self.sw * 0.3, self.sw)
        self.x, self.y = x, y
        gfx.coords(self.item, x - vx * 0.025, y - vy * 0.025, x, y)


def build_rain(canvas, sw, sh, end_time):
    k = max(0.6, min(1.5, sw / 1920))
    total = int(260 * k)
    drops = []
    for share, vr, w, c, wf in Drop.layers:
        for _ in range(int(total * share)):
            drops.append(Drop(canvas, sw, sh, (vr, w, c, wf),
                              end_time + random.uniform(0.5, 4.0)))
    return drops


class Clouds:
    tiers = ["#101F22", "#172B2D", "#263B3B"]
    tier_tags = ("tier0", "tier1", "tier2")
    drop_px = 340

    def __init__(self, canvas, sw, sh):
        self.sw = sw
        self.cur = 0.0
        self.last_flash = -1.0
        self.clouds = []
        n = max(8, sw // 190)
        for ci in range(n):
            cx = random.uniform(-100, sw + 100)
            cy = random.uniform(-10, sh * 0.13)
            sc = random.uniform(0.9, 1.6)
            for _ in range(7):
                ox = random.uniform(-130, 130) * sc
                oy = random.uniform(-26, 34) * sc
                rx = random.uniform(95, 170) * sc
                ry = random.uniform(48, 92) * sc
                tier = random.randint(0, 2)
                canvas.create_oval(cx + ox - rx, cy + oy - ry, cx + ox + rx, cy + oy + ry,
                                   fill=self.tiers[tier], outline="",
                                   tags=("cloud", f"cl{ci}", f"tier{tier}"))
            self.clouds.append(dict(x=cx, speed=random.uniform(10, 32), acc=0.0,
                                    tag=f"cl{ci}"))

    def update(self, t, dt, wind, flash, end_time):
        enter = ease_out_cubic(clamp01(t / 3.0))
        leave = ease_in_cubic(clamp01((t - end_time - 0.5) / 3.0))
        target = -self.drop_px * (1 - enter) - (self.drop_px + 60) * leave
        if abs(target - self.cur) > 0.01:
            gfx.move("cloud", 0, target - self.cur)
            self.cur = target
        drift = wind * 0.22
        for c in self.clouds:
            c["acc"] += (c["speed"] + drift) * dt
            if c["acc"] >= 1.0:
                dx = c["acc"]
                c["acc"] = 0.0
                gfx.move(c["tag"], dx, 0)
                c["x"] += dx
                if c["x"] > self.sw + 400:
                    shift = self.sw + 800
                    gfx.move(c["tag"], -shift, 0)
                    c["x"] -= shift
        if abs(flash - self.last_flash) > 0.01 or (flash == 0 and self.last_flash != 0):
            self.last_flash = flash
            for i in range(3):
                gfx.cfg(self.tier_tags[i], "-fill",
                        mix(self.tiers[i], "#A7D8D1", flash * (0.35 + 0.2 * i)))


class Bolt:
    def __init__(self, canvas, sw, sh, t, target=None):
        self.canvas, self.born = canvas, t
        self.sig = None
        if target:
            x1, y1 = target
            x0 = x1 + random.uniform(-sw * 0.07, sw * 0.07)
        else:
            x0 = random.uniform(sw * 0.08, sw * 0.92)
            x1 = x0 + random.uniform(-sw * 0.12, sw * 0.12)
            y1 = random.uniform(sh * 0.55, sh * 0.92)
        y0 = sh * 0.06
        main = self._path(x0, y0, x1, y1, 16, 38)
        if target:
            main[-2], main[-1] = x1, y1
        self.glows, self.cores = [], []
        self._add(main, 14, 3)
        for _ in range(random.randint(2, 4)):
            i = random.randint(3, 12)
            bx, by = main[2 * i], main[2 * i + 1]
            ex = bx + random.choice([-1, 1]) * random.uniform(70, 220)
            ey = by + random.uniform(90, 260)
            self._add(self._path(bx, by, ex, ey, 7, 20), 7, 1.5)

    def _path(self, x0, y0, x1, y1, segs, jitter):
        pts = []
        for i in range(segs + 1):
            u = i / segs
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            if 0 < i < segs:
                x += random.uniform(-jitter, jitter)
                y += random.uniform(-jitter, jitter) * 0.4
            pts += [x, y]
        return pts

    def _add(self, pts, gw, cw):
        self.glows.append(self.canvas.create_line(
            *pts, fill=transparent_color, width=gw, joinstyle="round",
            capstyle="round", tags=("bolt",)))
        self.cores.append(self.canvas.create_line(
            *pts, fill=transparent_color, width=cw, joinstyle="round",
            capstyle="round", tags=("bolt",)))

    @staticmethod
    def level(age):
        if age < 0.07:
            return 1.0
        if age < 0.13:
            return 0.15
        if age < 0.32:
            return 1.0 - (age - 0.13) / 0.19 * 0.55
        return max(0.0, 0.45 * (1 - (age - 0.32) / 0.28))

    def update(self, t):
        age = t - self.born
        if age > 0.6:
            gfx.delete(*self.glows, *self.cores)
            return False
        lv = self.level(age)
        gcol = mix(transparent_color, "#4C9E9B", lv * 0.7)
        ccol = mix(transparent_color, "#E9FFFA", lv)
        if (gcol, ccol) != self.sig:
            self.sig = (gcol, ccol)
            for g in self.glows:
                gfx.cfg(g, "-fill", gcol)
            for c in self.cores:
                gfx.cfg(c, "-fill", ccol)
        return True


class Streak:
    def __init__(self, canvas, sw, sh):
        self.sw = sw
        self.x = -random.uniform(50, 300)
        self.y = random.uniform(sh * 0.1, sh * 0.95)
        self.length = random.uniform(140, 380)
        self.v = random.uniform(1500, 2600)
        self.amp = random.uniform(6, 24)
        self.f = random.uniform(2, 5)
        self.ph = random.uniform(0, math.tau)
        self.gone = False
        self.col = None
        self.item = canvas.create_line(0, 0, 1, 1, fill=transparent_color, width=1,
                                       smooth=True, tags=("streak",))

    def update(self, dt, t):
        self.x += self.v * dt
        x = self.x
        if x - self.length > self.sw:
            self.gone = True
            gfx.delete(self.item)
            return
        base = t * self.f + self.ph
        step = self.length / 6
        amp = self.amp
        y = self.y
        pts = []
        for i in range(7):
            pts.append(x - step * i)
            pts.append(y + math.sin(base + i * 0.7) * amp)
        gfx.coords(self.item, *pts)
        col = mix(transparent_color, "#83B9B2",
                  0.55 * math.sin(math.pi * clamp01(x / self.sw)))
        if col != self.col:
            self.col = col
            gfx.cfg(self.item, "-fill", col)


class Debris:
    colors = ["#354A3F", "#4B5B45", "#705342", "#526D6B", "#3D5555"]

    def __init__(self, canvas, sw, sh, kind):
        self.sw, self.kind = sw, kind
        self.gone = False
        self.col = None
        self.x = -random.uniform(60, 400)
        self.y = random.uniform(sh * 0.15, sh * 0.95)
        self.ang = random.uniform(0, math.tau)
        self.ph = random.uniform(0, math.tau)
        if kind == "yero":
            self.w = random.uniform(90, 150)
            self.h = random.uniform(40, 62)
            self.vx = random.uniform(650, 1000)
            self.spin = random.uniform(-4, 4)
            self.flip = random.uniform(2.5, 5.0)
            self.poly = canvas.create_polygon(
                -999, -999, -999, -999, -999, -999, -999, -999, fill="#718987",
                outline="#C1D8D3", width=2, tags=("debris",))
            self.ribs = [canvas.create_line(-999, -999, -998, -998, fill="#4B6866", width=2,
                                            tags=("debris",)) for _ in range(3)]
        else:
            self.w = random.uniform(10, 22)
            self.h = self.w * random.uniform(0.5, 1.0)
            self.vx = random.uniform(500, 950)
            self.spin = random.uniform(-12, 12)
            self.flip = random.uniform(3, 8)
            self.poly = canvas.create_polygon(
                -999, -999, -999, -999, -999, -999, fill=random.choice(self.colors),
                outline="", tags=("debris",))
            self.ribs = []

    def _kill(self):
        self.gone = True
        gfx.delete(self.poly, *self.ribs)

    def update(self, dt, t, wind):
        self.x += (self.vx + wind * 1.4) * dt
        self.y += math.sin(t * 1.7 + self.ph) * 90 * dt
        self.ang += self.spin * dt
        x, y = self.x, self.y
        if x > self.sw + 250:
            self._kill()
            return
        if x < -150:
            return
        flip = abs(math.cos(t * self.flip + self.ph))
        hh = self.h * (0.25 + 0.75 * flip)
        c, s = math.cos(self.ang), math.sin(self.ang)
        w2, h2 = self.w / 2, hh / 2
        if self.kind == "yero":
            skew = self.w * 0.1
            local = ((-w2 + skew, -h2), (w2 + skew, -h2),
                     (w2 - skew, h2), (-w2 - skew, h2))
        else:
            local = ((-w2, h2), (w2, hh / 4), (0, -h2))
        flat = []
        for px, py in local:
            flat.append(x + px * c - py * s)
            flat.append(y + px * s + py * c)
        gfx.coords(self.poly, *flat)
        if self.kind == "yero":
            col = mix("#405B5B", "#AFC9C4", flip)
            if col != self.col:
                self.col = col
                gfx.cfg(self.poly, "-fill", col)
            for r, f in zip(self.ribs, (-0.25, 0.0, 0.25)):
                px = f * self.w
                bx = x + px * c
                by = y + px * s
                gfx.coords(r, bx + h2 * s, by - h2 * c, bx - h2 * s, by + h2 * c)


def _heart_halves():
    n = 40

    def hp(t):
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        return (x / 17.0, y / 17.0)

    right = [hp(math.pi * i / n) for i in range(n + 1)]
    left = [hp(math.pi + math.pi * i / n) for i in range(n + 1)]
    zig = [(0, 17), (2.5, 12), (-2, 7), (2, 2), (-2.5, -1.5), (0, -5)]
    zig = [(x / 17.0, y / 17.0) for x, y in zig]
    return right + zig[1:-1], left + list(reversed(zig[1:-1]))


heart_right, heart_left = [[(ux, uy - 1.0) for ux, uy in half] for half in _heart_halves()]


def _xf(pts, cx, cy, scale, rot):
    c = math.cos(rot) * scale
    s = math.sin(rot) * scale
    cy += scale
    out = []
    add = out.append
    for rx, ry in pts:
        add(cx + rx * c - ry * s)
        add(cy + rx * s + ry * c)
    return out


class BrokenHeart:
    life = 3.0

    def __init__(self, canvas, x, y, size, t):
        self.x, self.y, self.size, self.t0 = x, y, size, t
        self.hit_at = None
        self.sig = None
        self.due = t + random.uniform(0.9, 1.5)
        self.left = canvas.create_polygon(0, 0, 0, 0, 0, 0, fill=transparent_color,
                                          outline=transparent_color, width=2, tags=("heart",))
        self.right = canvas.create_polygon(0, 0, 0, 0, 0, 0, fill=transparent_color,
                                           outline=transparent_color, width=2, tags=("heart",))

    @property
    def center(self):
        return self.x, self.y

    def hit(self, t):
        if self.hit_at is None:
            self.hit_at = t

    def update(self, t, wind):
        age = t - self.t0
        a_in = ease_out_cubic(clamp01(age / 0.5))
        scale = self.size / 2 * (0.6 + 0.4 * a_in)
        sep = rot = fall = drift = flash = 0.0
        a = a_in

        if self.hit_at is None:
            scale *= 1 + 0.07 * math.sin(age * 16)
        else:
            hage = t - self.hit_at
            if hage > self.life:
                gfx.delete(self.left, self.right)
                return False
            a_out = clamp01((hage - (self.life - 1.2)) / 1.2)
            a = a_in * (1 - a_out)
            p = clamp01(hage / 1.6)
            sep = ease_out_cubic(p) * self.size * 0.32
            rot = ease_out_cubic(p) * 0.42
            fall = hage ** 2 * self.size * 0.35
            drift = wind * 0.05 * hage
            flash = clamp01(1 - hage / 0.18)

        cy = self.y + fall
        gfx.coords(self.left, *_xf(heart_left, self.x - sep + drift, cy, scale, -rot))
        gfx.coords(self.right, *_xf(heart_right, self.x + sep + drift, cy, scale, rot))
        fill = mix(mix(transparent_color, "#A83248", a), "#ffffff", flash * 0.85 * a)
        line = mix(mix(transparent_color, "#D77D8D", a), "#ffffff", flash * a)
        if (fill, line) != self.sig:
            self.sig = (fill, line)
            gfx.cfg(self.left, "-fill", fill, "-outline", line)
            gfx.cfg(self.right, "-fill", fill, "-outline", line)
        return True


class Word:
    pass


class LyricLine:
    def __init__(self, canvas, text, start, slot, sw, sh, zone, font_for):
        self.words = []
        self.items = []
        parts = text.split() or [" "]
        n = len(parts)
        base = max(26, int(sw / base_div))
        space = font_for(base, False)[0].measure(" ")

        infos = []
        for w in parts:
            kw = keywords.get(norm(w))
            size = int(base * (kw["scale"] if kw else random.uniform(0.94, 1.1)))
            f, ft = font_for(size, bool(kw))
            infos.append(dict(text=w, kw=kw, ft=ft, w=f.measure(w),
                              h=f.metrics("linespace")))

        per_row = 1 if n <= 2 else random.choice([2, 3])
        rows = [list(range(i, min(i + per_row, n))) for i in range(0, n, per_row)]
        sign = random.choice([-1, 1])
        pos = [None] * n
        for r, row in enumerate(rows):
            gaps = [space * random.uniform(1.0, 2.4) for _ in row[1:]]
            total = sum(infos[i]["w"] for i in row) + sum(gaps)
            x = -total / 2 + sign * ((-1) ** r) * random.uniform(0.02, 0.09) * sw
            y = (r - (len(rows) - 1) / 2) * base * random.uniform(2.0, 2.4)
            for k, i in enumerate(row):
                pos[i] = (x + infos[i]["w"] / 2, y + random.uniform(-0.4, 0.4) * base)
                x += infos[i]["w"] + (gaps[k] if k < len(gaps) else 0)

        minx = min(pos[i][0] - infos[i]["w"] / 2 for i in range(n))
        maxx = max(pos[i][0] + infos[i]["w"] / 2 for i in range(n))
        miny = min(pos[i][1] - infos[i]["h"] * 0.6 for i in range(n))
        maxy = max(pos[i][1] + infos[i]["h"] * 0.6 for i in range(n))
        margin = 70
        dx = sw * zone[0]
        if dx + minx < margin:
            dx = margin - minx
        if dx + maxx > sw - margin:
            dx = sw - margin - maxx
        dy = sh * zone[1]
        if dy + miny < sh * 0.2:
            dy = sh * 0.2 - miny
        if dy + maxy > sh * 0.92:
            dy = sh * 0.92 - maxy
        self.bbox = (dx + minx, dy + miny, dx + maxx, dy + maxy)

        hold_end = start + slot - 0.9
        last_max = hold_end - word_fade_in - 0.5
        gap_t = (last_max - (start + 0.2)) / max(n - 1, 1)
        gap_t = max(0.15, min(max_word_gap, gap_t))
        self.out_start = hold_end
        self.end = hold_end + line_fade_out + 0.5

        for i, inf in enumerate(infos):
            kw = inf["kw"]
            w = Word()
            w.x, w.y = dx + pos[i][0], dy + pos[i][1]
            w.ang = random.uniform(-4, 4) if kw else random.uniform(-7, 7)
            w.t0 = start + 0.2 + i * gap_t
            w.color = kw["color"] if kw else text_color
            w.glow_color = kw["glow"] if kw else None
            w.event = kw["event"] if kw else None
            w.fired = False
            w.shown = False
            w.finished = False
            w.sig = None
            w.amp = (2.6 if w.event == "strike" else 2.0) if kw else 0.9
            w.blow_dx = random.uniform(350, 800)
            w.blow_dy = random.uniform(-60, 70)
            w.spin_out = random.uniform(-40, 40)
            w.stagger = random.uniform(0, 0.45)
            w.ph1 = random.uniform(0, math.tau)
            w.ph2 = random.uniform(0, math.tau)
            opts = dict(text=inf["text"], font=inf["ft"], fill=transparent_color,
                        anchor="center", angle=w.ang, tags=("lyric",), state="hidden")
            w.glows = []
            if kw:
                for gx, gy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                    w.glows.append((canvas.create_text(w.x + gx, w.y + gy, **opts), gx, gy))
            w.shadow = canvas.create_text(w.x + 3, w.y + 4, **opts)
            w.main = canvas.create_text(w.x, w.y, **opts)
            w.items = [g for g, _, _ in w.glows] + [w.shadow, w.main]
            self.items += w.items
            self.words.append(w)

    def update(self, t, flash, fire):
        coords = gfx.coords
        cfg = gfx.cfg
        for w in self.words:
            if w.finished or t < w.t0:
                continue
            if not w.fired:
                w.fired = True
                if w.event:
                    fire(w.event)
            e = ease_out_cubic(clamp01((t - w.t0) / word_fade_in))
            o = ease_in_cubic(clamp01((t - self.out_start - w.stagger) / line_fade_out))
            if o >= 1.0:
                w.finished = True
                if w.shown:
                    for it in w.items:
                        cfg(it, "-state", "hidden")
                continue
            a = e * (1 - o)
            tr = w.amp * (0.4 + 0.6 * e) * (1 - o * 0.7)
            tx = (math.sin(t * 21 + w.ph1) + 0.6 * math.sin(t * 34 + w.ph2)) * tr
            ty = (math.cos(t * 19 + w.ph2) + 0.6 * math.sin(t * 31 + w.ph1)) * tr * 0.7
            x = w.x - (1 - e) * 70 + o * w.blow_dx + tx
            y = w.y + (1 - e) * 10 + o * w.blow_dy + ty
            ang = w.ang - (1 - e) * 8 + o * w.spin_out
            col = mix(mix(transparent_color, w.color, a), "#ffffff", flash * 0.4 * a)
            gcol = mix(transparent_color, w.glow_color, a * 0.85) if w.glows else None
            scol = mix(transparent_color, shadow_color, a)
            sig = (col, gcol, scol, ang)
            if sig != w.sig:
                w.sig = sig
                if w.shown:
                    extra = ()
                else:
                    extra = ("-state", "normal")
                    w.shown = True
                for g, _, _ in w.glows:
                    cfg(g, "-fill", gcol, "-angle", ang, *extra)
                cfg(w.shadow, "-fill", scol, "-angle", ang, *extra)
                cfg(w.main, "-fill", col, "-angle", ang, *extra)
            for g, gx, gy in w.glows:
                coords(g, x + gx, y + gy)
            coords(w.shadow, x + 3, y + 4)
            coords(w.main, x, y)
        if t >= self.end:
            gfx.delete(*self.items)
            return False
        return True


class bagyo:
    frame_ms = 16

    def __init__(self):
        self.lines = load_lyrics()
        self.end_time = max(s + d for s, _, d in self.lines)

        if dpi_aware:
            set_dpi_aware()
        fine_timer(True)
        self.root = tk.Tk()
        self.root.title("Ako ang Bagyo Backdrop")
        self.root.overrideredirect(True)
        self.root.configure(bg=tint_color)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.0)
        self.set_alpha = partial(self.root.tk.call, "wm", "attributes", self.root._w, "-alpha")
        self.set_bg = partial(self.root.tk.call, self.root._w, "configure", "-bg")
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        self.root.geometry(f"{self.sw}x{self.sh}+0+0")
        make_click_through(self.root)
        if use_blur:
            enable_blur(self.root, tint_color, tint_alpha)

        self.win = tk.Toplevel(self.root)
        self.win.title("Ako ang Bagyo")
        self.win.overrideredirect(True)
        self.win.wm_attributes("-topmost", True)
        self.win.wm_attributes("-transparentcolor", transparent_color)
        self.win.geometry(f"{self.sw}x{self.sh}+0+0")
        self.canvas = tk.Canvas(self.win, width=self.sw, height=self.sh,
                                bg=transparent_color, highlightthickness=0)
        self.canvas.pack()
        gfx.bind(self.canvas)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.win.bind("<Escape>", lambda e: self.root.destroy())

        self.fonts = {}
        self.clouds = Clouds(self.canvas, self.sw, self.sh)
        self.rain = build_rain(self.canvas, self.sw, self.sh, self.end_time)

        self.spawned = [False] * len(self.lines)
        self.active = []
        self.bolts = []
        self.debris = []
        self.streaks = []
        self.hearts = []
        self.heart_events = []
        self.pulses = []
        self.gusts = []
        self.recent_zones = []
        self.alpha = 0.0
        self.bg = tint_color
        self.dirty = False
        self.t = 0.0

        self.next_strike = 0.6
        self.next_gust = 2.0
        self.next_yero = 6.0
        self.next_shard = 1.0

        gc.collect()
        gc.freeze()
        gc.set_threshold(30000, 50, 50)

        self.t0 = time.perf_counter()
        self.last = self.t0
        self.next_frame = self.t0
        self._tick()
        self.root.mainloop()
        fine_timer(False)

    def font_for(self, size, bold):
        key = (size, bold)
        if key not in self.fonts:
            style = "bold italic" if bold else "italic"
            f = tkfont.Font(family=font_family, size=size,
                            weight="bold" if bold else "normal", slant="italic")
            self.fonts[key] = (f, (font_family, size, style))
        return self.fonts[key]

    def raise_lyrics(self):
        self.dirty = True

    def add_gust(self, t, amp=None):
        self.gusts.append((t, random.uniform(1.6, 3.0), amp or random.uniform(150, 320)))

    def wind_at(self, t):
        w = 70 + 45 * math.sin(t * 0.6) + 20 * math.sin(t * 1.7)
        live = []
        for gs, gd, ga in self.gusts:
            ph = (t - gs) / gd
            if ph < 1:
                live.append((gs, gd, ga))
                if ph >= 0:
                    w += ga * math.sin(math.pi * ph)
        self.gusts = live
        return w

    def strike(self, t, heart=None):
        if heart is None:
            ready = [h for h in self.hearts if h.hit_at is None and t - h.t0 > 0.35]
            if ready:
                heart = random.choice(ready)
        target = heart.center if heart else None
        self.bolts.append(Bolt(self.canvas, self.sw, self.sh, t, target))
        if heart:
            heart.hit(t)
        if lightning_flash:
            self.pulses += [(t, 1.0), (t + 0.14, 0.55), (t + 0.30, 0.8)]
        self.raise_lyrics()

    def fire(self, event):
        t = self.t
        if event == "strike":
            self.strike(t)
            self.add_gust(t, 280)
            for _ in range(8):
                self.debris.append(Debris(self.canvas, self.sw, self.sh, "shard"))
        elif event == "yero":
            for _ in range(5):
                self.debris.append(Debris(self.canvas, self.sw, self.sh, "yero"))
            self.add_gust(t, 240)
        elif event == "gust":
            self.add_gust(t, 300)
        self.raise_lyrics()

    def pick_zone(self):
        choices = [z for z in zones if z not in self.recent_zones] or zones
        zone = random.choice(choices)
        self.recent_zones = (self.recent_zones + [zone])[-3:]
        return zone

    def start_line(self, i):
        start, text, slot = self.lines[i]
        line = LyricLine(self.canvas, text, start, slot, self.sw, self.sh,
                         self.pick_zone(), self.font_for)
        self.active.append(line)
        self.spawned[i] = True
        self.heart_events.append((start + random.uniform(0.9, 1.5), random.randint(46, 84)))
        self.heart_events.append((start + slot * random.uniform(0.5, 0.65), random.randint(46, 84)))
        if any(norm(w) == "bagyo" for w in text.split()):
            self.heart_events.append((start + slot * 0.35, random.randint(120, 160)))

    def spawn_heart(self, size, t):
        x = y = None
        for _ in range(14):
            x = random.uniform(120, self.sw - 120)
            y = random.uniform(self.sh * 0.24, self.sh * 0.88)
            pad = size * 0.7 + 30
            if all(not (ln.bbox[0] - pad < x < ln.bbox[2] + pad and
                        ln.bbox[1] - pad < y < ln.bbox[3] + pad) for ln in self.active):
                break
        self.hearts.append(BrokenHeart(self.canvas, x, y, size, t))
        self.raise_lyrics()

    def _tick(self):
        now = time.perf_counter()
        t = now - self.t0
        dt = min(0.05, now - self.last)
        self.last = now
        self.t = t
        ending = t > self.end_time

        for i, (start, _, _) in enumerate(self.lines):
            if not self.spawned[i] and t >= start:
                self.start_line(i)

        if not ending:
            if t >= self.next_strike:
                self.strike(t)
                self.next_strike = t + random.uniform(2.8, 6.5)
            if t >= self.next_gust:
                self.add_gust(t)
                self.next_gust = t + random.uniform(4, 8)
            if t >= self.next_yero:
                self.debris.append(Debris(self.canvas, self.sw, self.sh, "yero"))
                self.next_yero = t + random.uniform(5, 10)
                self.dirty = True
            if t >= self.next_shard and len(self.debris) < 18:
                self.debris.append(Debris(self.canvas, self.sw, self.sh, "shard"))
                self.next_shard = t + random.uniform(0.25, 0.7)
                self.dirty = True

        wind = self.wind_at(t)
        if not ending and wind > 200 and len(self.streaks) < 18 and random.random() < 0.35:
            self.streaks.append(Streak(self.canvas, self.sw, self.sh))
            self.dirty = True

        if self.heart_events:
            due = [e for e in self.heart_events if e[0] <= t]
            if due:
                self.heart_events = [e for e in self.heart_events if e[0] > t]
                for _, size in due:
                    self.spawn_heart(size, t)

        for h in self.hearts:
            if h.hit_at is None and t >= h.due:
                self.strike(t, h)
                self.add_gust(t, 200)

        flash = 0.0
        live = []
        for ts, amp in self.pulses:
            dtp = t - ts
            if dtp < 0:
                live.append((ts, amp))
            elif dtp < 1.6:
                live.append((ts, amp))
                flash = max(flash, amp * math.exp(-dtp * 7.5))
        self.pulses = live

        self.clouds.update(t, dt, wind, flash, self.end_time)
        for d in self.rain:
            d.update(dt, wind, ending, t)
        self.rain = [d for d in self.rain if not d.gone]
        for s in self.streaks:
            s.update(dt, t)
        self.streaks = [s for s in self.streaks if not s.gone]
        for d in self.debris:
            d.update(dt, t, wind)
        self.debris = [d for d in self.debris if not d.gone]
        self.bolts = [b for b in self.bolts if b.update(t)]
        self.hearts = [h for h in self.hearts if h.update(t, wind)]
        self.active = [ln for ln in self.active if ln.update(t, flash, self.fire)]

        if self.dirty:
            self.dirty = False
            gfx.raise_("lyric")

        fade_in = ease_in_out(clamp01(t / 2.0))
        fade_out = ease_in_out(clamp01((t - self.end_time) / 4.5))
        raw = min(0.96, tint_alpha * fade_in * (1 - fade_out) + 0.3 * flash * (1 - fade_out))
        alpha = round(raw * 255) / 255
        bg = mix(tint_color, "#B9E5DE", flash * 0.6)
        try:
            if alpha != self.alpha:
                self.alpha = alpha
                self.set_alpha(alpha)
            if bg != self.bg:
                self.bg = bg
                self.set_bg(bg)
        except tk.TclError:
            pass

        finished = not (self.rain or self.active or self.hearts or self.debris
                        or self.bolts or self.streaks)
        if (ending and t > self.end_time + 1 and finished) or t > self.end_time + 14:
            self.root.destroy()
            return

        self.next_frame += self.frame_ms / 1000.0
        after = time.perf_counter()
        if self.next_frame < after:
            self.next_frame = after
        self.root.after(max(2, int((self.next_frame - after) * 1000)), self._tick)


if __name__ == "__main__":
    bagyo()