#!/usr/bin/env python3
"""
croquis.py — şematik vücut figürü ve İŞARET NOKTASI tablosu.

⚠ DÜRÜSTLÜK SINIRI — bu dosyanın en önemli cümlesi:

    BURADAKİ ORANLAR BİR ÇİZİM KONVANSİYONUDUR, ANTROPOMETRİK BİR
    İDDİA DEĞİLDİR.

Kroki, "şerit metre NEREDEN NEREYE gider" sorusunu yanıtlamak için
vardır. Hiçbir okur bu figürden kendi ölçüsünü OKUMAZ; kendi ölçüsünü
kendi vücudundan alır. Bu yüzden kroki oranları hiçbir kaynağa
dayandırılmaz ve hiçbir kaynak olarak GÖSTERİLMEZ. Ölçünün tanımı
`measurements.json` → `path_rule` alanındadır; kroki yalnızca o kuralın
resmidir. Bu ayrım `CLAIMS_STANDARD.md`'nin doğrudan gereğidir: ölçüsüz
bir çizim bir iddia taşıyamaz.

Koordinat sistemi: figürün toplam boyu 1,0'dır ve bütün değerler bunun
kesridir. Yatay değerler ORTA HATTA göre YARIM genişliktir. Aynı
sayılar üç kitapta da kullanılır (`00_CONTEXT/REUSE_MAP.md`).
"""
from __future__ import annotations

# ── dikey seviyeler (0 = zemin, 1 = baş üstü) ─────────────────────────
LEVEL = {
    "top_of_head":      1.000,
    "chin":             0.878,
    "side_neck_point":  0.856,
    "nape":             0.852,
    "neck_base":        0.848,
    "throat_hollow":    0.838,
    "shoulder_point":   0.826,
    "armscye":          0.789,
    "across_chest":     0.786,
    "across_back":      0.786,
    "high_bust":        0.766,
    "underarm":         0.752,
    "bust_apex":        0.732,
    "underbust":        0.700,
    "bicep":            0.700,
    "waist":            0.628,
    "elbow":            0.612,
    "high_hip":         0.578,
    "full_hip":         0.524,
    "wrist":            0.500,
    "crotch":           0.498,
    "seat_surface":     0.498,
    "thigh":            0.452,
    "knee":             0.272,
    "calf":             0.190,
    "ankle":            0.048,
    "floor":            0.000,
}

# ── GÖVDE KONTURU yarım genişlikleri (siluetin dış hattı) ─────────────
OUTLINE = {
    "shoulder_point":   0.098,
    "armscye":          0.094,
    "underarm":         0.090,
    "high_bust":        0.089,
    "bust_apex":        0.092,
    "underbust":        0.078,
    "waist":            0.064,
    "high_hip":         0.081,
    "full_hip":         0.096,
    "crotch":           0.090,
}

# ── BACAK konturu: dış ve iç hat ──────────────────────────────────────
LEG_OUT = {"crotch": 0.090, "thigh": 0.076, "knee": 0.043, "calf": 0.046, "ankle": 0.024}
LEG_IN = {"crotch": 0.008, "thigh": 0.030, "knee": 0.016, "calf": 0.018, "ankle": 0.007}

# ── ÖLÇÜ yarım genişlikleri (çevre yolunun genişliği) ─────────────────
# Gövde çevresi için konturla aynıdır; UZUV çevresi için uzvun kendi
# genişliğidir — bir kolun çevresi gövdenin yarısı kadar geniş çizilemez.
HALF_W = dict(OUTLINE)
HALF_W.update({
    "neck_base":     0.034,
    "across_chest":  0.082,
    "across_back":   0.090,
    "apex_offset":   0.042,
    "head":          0.048,
    "thigh":         0.023,    # tek bacağın yarı genişliği
    "knee":          0.0135,
    "calf":          0.014,
    "ankle":         0.0085,
})

# ── KOL geometrisi ────────────────────────────────────────────────────
ARM = {
    "gap":         0.008,
    "bicep_half":  0.026,
    "elbow_half":  0.020,
    "wrist_half":  0.013,
}
HALF_W["bicep"] = ARM["bicep_half"]
HALF_W["wrist"] = ARM["wrist_half"]
HALF_W["elbow"] = ARM["elbow_half"]

# ── yandan görünüş derinlikleri (orta hattan ön/arka) ─────────────────
DEPTH = {
    "neck_base":  (0.026, 0.030),
    "shoulder_point": (0.032, 0.044),
    "high_bust":  (0.062, 0.048),
    "bust_apex":  (0.072, 0.048),
    "underbust":  (0.052, 0.048),
    "waist":      (0.040, 0.048),
    "high_hip":   (0.044, 0.062),
    "full_hip":   (0.046, 0.076),
    "crotch":     (0.030, 0.062),
    "seat_surface": (0.030, 0.062),
    "knee":       (0.030, 0.030),
    "ankle":      (0.022, 0.028),
    "floor":      (0.030, 0.030),
}
MAX_HALF_SIDE = 0.080

MAX_HALF_TORSO = 0.100
MAX_HALF_FULL = 0.135

# ── VÜCUT VARYANTLARI ─────────────────────────────────────────────────
# Çelişmeli inceleme bulgusu B-05 (YÜKSEK): 154 figürün tamamı TEK bir
# kroki oranından üretiliyordu. Kitap uyum sorunlarının vücut
# çeşitliliğinden doğduğunu söylüyor ama her figürde aynı vücudu
# gösteriyordu — kendi tezini görsel olarak yalanlıyordu.
#
# ⚠ YUKARIDAKİ DÜRÜSTLÜK SINIRI VARYANTLAR İÇİN DE GEÇERLİDİR.
# Bu üç varyant ANTROPOMETRİK BİR İDDİA DEĞİLDİR ve bir vücut
# TİPOLOJİSİ ÖNERMEZ. Hiçbiri bir nüfusu, bir yüzdeyi ya da bir "tip"i
# temsil etmez. Yaptıkları tek şey şudur: bir belirti figürü, o
# belirtinin ÜZERİNDE GÖRÜLDÜĞÜ gövde farkını gösterebilsin. Yuvarlak
# sırt varyantı "yuvarlak sırtlı insanlar böyledir" DEMEZ; "bu belirti
# bir yuvarlak sırtta böyle görünür" der.
#
# Motor değişmedi. Değişen sayı azdır ve hepsi burada durur.
_VARIANT_DELTAS = {
    "standard": {},
    "straight_back": {
        # Düz sırt: üst sırt derinliği azalır, ense-bel arkası düzleşir.
        "DEPTH": {"shoulder_point": (0.032, 0.036), "high_bust": (0.062, 0.040),
                  "bust_apex": (0.072, 0.040), "underbust": (0.052, 0.041),
                  "waist": (0.040, 0.040), "neck_base": (0.026, 0.024)},
        "OUTLINE": {"armscye": 0.091, "underarm": 0.087},
        "HALF_W": {"across_back": 0.085},
    },
    "rounded_back": {
        # Yuvarlak sırt: üst sırt derinliği ve genişliği artar, nape
        # geriye kayar, omuz noktası öne döner.
        "DEPTH": {"shoulder_point": (0.030, 0.056), "high_bust": (0.060, 0.060),
                  "bust_apex": (0.070, 0.058), "underbust": (0.050, 0.055),
                  "waist": (0.040, 0.054), "neck_base": (0.022, 0.040)},
        "OUTLINE": {"armscye": 0.098, "underarm": 0.094},
        "HALF_W": {"across_back": 0.096},
        "LEVEL": {"nape": 0.849, "side_neck_point": 0.854},
    },
    "fuller_bust": {
        # Dolgun göğüs: apeks genişler, aşağı ve dışa kayar.
        # ⚠ high_bust DEĞİŞMEZ — M-031 farkının kendisi budur.
        "OUTLINE": {"bust_apex": 0.104, "underbust": 0.080},
        "HALF_W": {"apex_offset": 0.048, "across_chest": 0.084},
        "DEPTH": {"bust_apex": (0.092, 0.048), "high_bust": (0.068, 0.048),
                  "underbust": (0.058, 0.048)},
        "LEVEL": {"bust_apex": 0.726},
    },
}
VARIANTS = tuple(_VARIANT_DELTAS)


def variant_tables(name: str) -> dict:
    """Bir varyantın tam tablo kümesi. Taban tablolar HİÇ değişmez.

    Sıra önemlidir: OUTLINE bir gövde KONTURUDUR ve HALF_W (ölçü yolu
    genişliği) onu miras alır. Varyant konturu genişletip ölçü yolunu
    genişletmezse şerit metre çizgisi gövdenin İÇİNDE kalır — sessiz ve
    yanlış bir figür. Bu yüzden OUTLINE deltası HALF_W'ye de yazılır,
    sonra varyantın AÇIK HALF_W deltası en son uygulanır.
    """
    if name not in _VARIANT_DELTAS:
        raise ValueError(f"bilinmeyen kroki varyantı: {name!r} — {VARIANTS}")
    d = _VARIANT_DELTAS[name]
    base = {"LEVEL": dict(LEVEL), "OUTLINE": dict(OUTLINE), "HALF_W": dict(HALF_W),
            "DEPTH": dict(DEPTH), "LEG_OUT": dict(LEG_OUT), "LEG_IN": dict(LEG_IN),
            "ARM": dict(ARM)}
    for tbl in ("LEVEL", "DEPTH", "LEG_OUT", "LEG_IN", "ARM"):
        base[tbl].update(d.get(tbl, {}))
    base["OUTLINE"].update(d.get("OUTLINE", {}))
    base["HALF_W"].update(d.get("OUTLINE", {}))
    base["HALF_W"].update(d.get("HALF_W", {}))
    return base


class Croquis:
    """Kroki — bir figür kutusuna yerleştirilmiş şematik vücut."""

    def __init__(self, cx: float, base_y: float, height_pt: float, view: str = "front",
                 variant: str = "standard"):
        if view not in {"front", "back", "side"}:
            raise ValueError(view)
        self.cx, self.base_y, self.H, self.view = cx, base_y, float(height_pt), view
        self.variant = variant
        t = variant_tables(variant)
        self.LEVEL, self.OUTLINE, self.HALF_W = t["LEVEL"], t["OUTLINE"], t["HALF_W"]
        self.DEPTH, self.LEG_OUT = t["DEPTH"], t["LEG_OUT"]
        self.LEG_IN, self.ARM = t["LEG_IN"], t["ARM"]

    # ── koordinat yardımcıları ────────────────────────────────────────
    def y(self, level: str) -> float:
        return self.base_y + self.LEVEL[level] * self.H

    def hw(self, key: str) -> float:
        return self.HALF_W[key] * self.H

    def p(self, level: str, half_key: str | None = None, side: int = 0) -> tuple:
        x = self.cx + (side * self.hw(half_key) if half_key else 0.0)
        return (x, self.y(level))

    def apex(self, side: int = 1) -> tuple:
        return (self.cx + side * self.HALF_W["apex_offset"] * self.H, self.y("bust_apex"))

    def leg_center(self, side: int) -> float:
        """Bir bacağın orta hattı — bacak çevresi ölçüsü buna göre çizilir."""
        mid = (self.LEG_OUT["thigh"] + self.LEG_IN["thigh"]) / 2.0
        return self.cx + side * mid * self.H

    # ── kontur parçaları ──────────────────────────────────────────────
    def _side_chain(self, s: int, bottom: str) -> list:
        """Omuz ucundan aşağı gövde konturu, `bottom` seviyesinde kesilir."""
        chain = [("shoulder_point", self.OUTLINE["shoulder_point"]),
                 ("armscye", self.OUTLINE["armscye"]),
                 ("underarm", self.OUTLINE["underarm"]),
                 ("high_bust", self.OUTLINE["high_bust"]),
                 ("bust_apex", self.OUTLINE["bust_apex"]),
                 ("underbust", self.OUTLINE["underbust"]),
                 ("waist", self.OUTLINE["waist"]),
                 ("high_hip", self.OUTLINE["high_hip"]),
                 ("full_hip", self.OUTLINE["full_hip"]),
                 ("crotch", self.OUTLINE["crotch"])]
        cut = self.LEVEL[bottom]
        pts = [(self.cx + s * hw * self.H, self.y(lv))
               for lv, hw in chain if self.LEVEL[lv] >= cut - 1e-9]
        if not pts or abs(self.LEVEL[chain[-1][0]] - cut) > 1e-9:
            # kesim seviyesinde ara değer: son iki noktadan doğrusal
            for i in range(len(chain) - 1):
                a, b = chain[i], chain[i + 1]
                if self.LEVEL[b[0]] <= cut <= self.LEVEL[a[0]]:
                    f = (self.LEVEL[a[0]] - cut) / (self.LEVEL[a[0]] - self.LEVEL[b[0]])
                    hw = a[1] + (b[1] - a[1]) * f
                    pts.append((self.cx + s * hw * self.H, self.y(bottom)))
                    break
        return pts

    def _leg_chain(self, s: int, inner: bool) -> list:
        tbl = LEG_IN if inner else LEG_OUT
        return [(self.cx + s * tbl[lv] * self.H, self.y(lv))
                for lv in ("crotch", "thigh", "knee", "calf", "ankle")]

    def _arm_chain(self, s: int) -> list:
        g = self.ARM["gap"] * self.H
        return [
            (self.cx + s * self.OUTLINE["shoulder_point"] * self.H, self.y("shoulder_point")),
            (self.cx + s * (self.OUTLINE["underarm"] * self.H + g + self.ARM["bicep_half"] * self.H),
             self.y("bicep")),
            (self.cx + s * (self.OUTLINE["waist"] * self.H + g + 2.6 * self.ARM["elbow_half"] * self.H),
             self.y("elbow")),
            (self.cx + s * (self.OUTLINE["high_hip"] * self.H + g + 1.6 * self.ARM["wrist_half"] * self.H),
             self.y("wrist")),
        ]

    # ── çizim ─────────────────────────────────────────────────────────
    def _head_and_neck(self, fc, gray):
        hw_n = self.HALF_W["neck_base"] * self.H
        for s in (-1, 1):
            fc.curve([(self.cx + s * hw_n, self.y("neck_base")),
                      (self.cx + s * hw_n * 0.92, self.y("chin"))],
                     role="body_outline", gray=gray)
        fc._gray(gray)
        fc.c.setLineWidth(fc._lw["body_outline"])
        fc.c.ellipse(self.cx - self.hw("head"), self.y("chin"),
                     self.cx + self.hw("head"), self.y("top_of_head"),
                     stroke=1, fill=0)

    def _neck_stub(self, fc, gray):
        hw_n = self.HALF_W["neck_base"] * self.H
        top = self.y("neck_base") + 0.016 * self.H
        for s in (-1, 1):
            fc.line(self.cx + s * hw_n, self.y("neck_base"),
                    self.cx + s * hw_n * 0.94, top, role="body_outline", gray=gray)
        fc.line(self.cx - hw_n * 0.94, top, self.cx + hw_n * 0.94, top,
                role="body_outline", gray=gray)

    def _shoulders_and_neckline(self, fc, gray):
        for s in (-1, 1):
            fc.line(self.cx + s * self.HALF_W["neck_base"] * self.H, self.y("side_neck_point"),
                    self.cx + s * self.OUTLINE["shoulder_point"] * self.H, self.y("shoulder_point"),
                    role="body_outline", gray=gray)
        drop = 0.012 * self.H if self.view != "back" else 0.005 * self.H
        fc.curve([(self.cx - self.HALF_W["neck_base"] * self.H, self.y("side_neck_point")),
                  (self.cx, self.y("neck_base") - drop),
                  (self.cx + self.HALF_W["neck_base"] * self.H, self.y("side_neck_point"))],
                 role="body_outline", gray=gray)

    # ── yandan görünüş ────────────────────────────────────────────────
    def _profile_chain(self, front: bool) -> list:
        order = ["neck_base", "shoulder_point", "high_bust", "bust_apex", "underbust",
                 "waist", "high_hip", "full_hip", "crotch", "knee", "ankle"]
        s = 1 if front else -1
        i = 0 if front else 1
        return [(self.cx + s * self.DEPTH[lv][i] * self.H, self.y(lv)) for lv in order]

    def draw_side(self, fc, *, head=True, gray=0.0, bottom="ankle"):
        """Profil silueti — ağ derinliği ve ağ uzunluğu YALNIZCA burada
        anlaşılır; önden görünüşte ikisi de görünmez."""
        cut = self.LEVEL[bottom]
        for front in (True, False):
            pts = [q for q in self._profile_chain(front)
                   if (q[1] - self.base_y) / self.H >= cut - 1e-9]
            fc.curve(pts, role="body_outline", gray=gray)
        fpts = [q for q in self._profile_chain(True)
                if (q[1] - self.base_y) / self.H >= cut - 1e-9]
        bpts = [q for q in self._profile_chain(False)
                if (q[1] - self.base_y) / self.H >= cut - 1e-9]
        fc.line(fpts[-1][0], fpts[-1][1], bpts[-1][0], bpts[-1][1],
                role="body_outline", gray=gray)
        fc.line(bpts[0][0], bpts[0][1], fpts[0][0], fpts[0][1],
                role="body_outline", gray=gray)
        if head:
            fc._gray(gray)
            fc.c.setLineWidth(fc._lw["body_outline"])
            fc.c.ellipse(self.cx - self.hw("head") * 1.05, self.y("chin"),
                         self.cx + self.hw("head") * 0.95, self.y("top_of_head"),
                         stroke=1, fill=0)
            for s in (-1, 1):
                fc.line(self.cx + s * self.DEPTH["neck_base"][0 if s > 0 else 1] * self.H * 0.9,
                        self.y("neck_base"),
                        self.cx + s * self.DEPTH["neck_base"][0 if s > 0 else 1] * self.H * 0.8,
                        self.y("chin"), role="body_outline", gray=gray)

    def profile_point(self, level: str, front: bool = True) -> tuple:
        i = 0 if front else 1
        s = 1 if front else -1
        return (self.cx + s * self.DEPTH[level][i] * self.H, self.y(level))

    def draw(self, fc, *, arms=True, head=True, legs=True, gray=0.0):
        """Tam figür. view='side' ise profil çizilir."""
        if self.view == "side":
            return self.draw_side(fc, head=head, gray=gray,
                                  bottom="ankle" if legs else "crotch")
        for s in (-1, 1):
            fc.curve(self._side_chain(s, "crotch"), role="body_outline", gray=gray)
            if arms:
                fc.curve(self._arm_chain(s), role="body_outline", gray=gray)
            if legs:
                fc.curve(self._leg_chain(s, inner=False), role="body_outline", gray=gray)
                fc.curve(self._leg_chain(s, inner=True), role="body_outline", gray=gray)
        self._shoulders_and_neckline(fc, gray)
        if head:
            self._head_and_neck(fc, gray)
        else:
            self._neck_stub(fc, gray)
        if legs:
            fc.line(self.cx - self.LEG_OUT["ankle"] * self.H, self.y("ankle"),
                    self.cx - self.LEG_IN["ankle"] * self.H, self.y("ankle"),
                    role="body_outline", gray=gray)
            fc.line(self.cx + self.LEG_IN["ankle"] * self.H, self.y("ankle"),
                    self.cx + self.LEG_OUT["ankle"] * self.H, self.y("ankle"),
                    role="body_outline", gray=gray)
            fc.curve([(self.cx - self.LEG_IN["crotch"] * self.H, self.y("crotch")),
                      (self.cx, self.y("crotch") + 0.008 * self.H),
                      (self.cx + self.LEG_IN["crotch"] * self.H, self.y("crotch"))],
                     role="body_outline", gray=gray)
        else:
            fc.line(self.cx - self.OUTLINE["crotch"] * self.H, self.y("crotch"),
                    self.cx + self.OUTLINE["crotch"] * self.H, self.y("crotch"),
                    role="body_outline", gray=gray)

    def draw_torso_only(self, fc, *, bottom="high_hip", gray=0.0, head=True):
        """Gövde figürü — `bottom` seviyesinde kesilir.

        Baş VARSAYILAN OLARAK çizilir: başsız bir gövde silueti vazoya
        benzer ve okur figürün yönünü kaybeder.
        """
        if self.LEVEL[bottom] < self.LEVEL["crotch"] - 1e-9:
            # kesim ağın altındaysa bacaklar da çizilir
            for s in (-1, 1):
                fc.curve(self._side_chain(s, "crotch"), role="body_outline", gray=gray)
                out = [q for q in self._leg_chain(s, False)
                       if (q[1] - self.base_y) / self.H >= self.LEVEL[bottom] - 1e-9]
                inn = [q for q in self._leg_chain(s, True)
                       if (q[1] - self.base_y) / self.H >= self.LEVEL[bottom] - 1e-9]
                fc.curve(out, role="body_outline", gray=gray)
                fc.curve(inn, role="body_outline", gray=gray)
                fc.line(out[-1][0], out[-1][1], inn[-1][0], inn[-1][1],
                        role="body_outline", gray=gray)
            fc.curve([(self.cx - self.LEG_IN["crotch"] * self.H, self.y("crotch")),
                      (self.cx, self.y("crotch") + 0.008 * self.H),
                      (self.cx + self.LEG_IN["crotch"] * self.H, self.y("crotch"))],
                     role="body_outline", gray=gray)
        else:
            for s in (-1, 1):
                fc.curve(self._side_chain(s, bottom), role="body_outline", gray=gray)
            pts = self._side_chain(1, bottom)
            fc.line(self.cx - abs(pts[-1][0] - self.cx), pts[-1][1],
                    pts[-1][0], pts[-1][1], role="body_outline", gray=gray)
        self._shoulders_and_neckline(fc, gray)
        if head:
            self._head_and_neck(fc, gray)
        else:
            self._neck_stub(fc, gray)

    # ── ölçü yolları ──────────────────────────────────────────────────
    def girth_path(self, level: str, half_key: str, *, front=True, cx=None) -> list:
        """Bir çevre ölçüsünün ÖN yüzden görünen yayı."""
        y0 = self.y(level)
        hw = self.hw(half_key)
        c = self.cx if cx is None else cx
        sag = (0.009 if front else -0.009) * self.H
        return [(c - hw, y0),
                (c - hw * 0.5, y0 - sag * 0.72),
                (c, y0 - sag),
                (c + hw * 0.5, y0 - sag * 0.72),
                (c + hw, y0)]

    def limb_girth_path(self, level: str, half_key: str, side: int = 1) -> list:
        """Uzuv çevresi — uzvun KENDİ orta hattına göre."""
        if level in ("thigh", "knee", "calf", "ankle"):
            c = self.leg_center(side)
        else:
            g = self.ARM["gap"] * self.H
            base = {"bicep": self.OUTLINE["underarm"], "elbow": self.OUTLINE["waist"],
                    "wrist": self.OUTLINE["high_hip"]}[level] * self.H
            c = self.cx + side * (base + g + self.hw(half_key))
        return self.girth_path(level, half_key, cx=c)

    def vertical_path(self, l1: str, l2: str, half_key: str | None = None,
                      side: int = 0) -> list:
        a = self.p(l1, half_key, side)
        b = self.p(l2, half_key, side)
        return [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b]


def fit(box_w: float, box_h: float, lo: str, hi: str, *,
        pad_x: float = 10.0, pad_y: float = 12.0, arms: bool = True,
        cx: float | None = None, view: str = "front",
        variant: str = "standard") -> "Croquis":
    """Bir kroki'yi kutuya SIĞDIRIR.

    [lo, hi] seviye aralığı kutunun dikey iç alanına oturur; genişlik
    kısıtı ayrıca uygulanır. Ölçek ikisinin KÜÇÜĞÜDÜR — figür kutudan
    taşamaz.
    """
    V = variant_tables(variant)
    span = V["LEVEL"][hi] - V["LEVEL"][lo]
    if span <= 0:
        raise ValueError(f"geçersiz aralık: {lo}..{hi}")
    if view == "side":
        max_half = MAX_HALF_SIDE
    else:
        max_half = MAX_HALF_FULL if arms else MAX_HALF_TORSO
    H = min((box_h - 2 * pad_y) / span, (box_w / 2 - pad_x) / max_half)
    base_y = pad_y - V["LEVEL"][lo] * H
    return Croquis(cx if cx is not None else box_w / 2, base_y, H, view=view,
                   variant=variant)
