#!/usr/bin/env python3
"""
cause_order.py — ADAY NEDENLERİN BASILMA SIRASI. TEK KAYNAK.

⚠ NEDEN VAR: sıra İKİ yerde hesaplanıyordu (atlas girişleri ve akış
şemaları) ve bir kez zaten ayrışmıştı. Ama asıl kusur daha derindi ve
OKUR SİMÜLASYONU buldu (KRİTİK-3): sıra YALNIZCA test maliyetinden
geliyordu, oysa bazı girişler bir KLİNİK ÖNCELİK de ilan ediyor —
"önce sırtı ele, sonra omuz konumunu" gibi. İkisi çeliştiğinde basılan
sıra maliyeti izliyor, "Order:" satırı ise başka bir şey söylüyordu.
Dört girişte tam da kitabın "yanlış olanı düzeltmek ötekini kötüleştirir"
diye uyardığı çiftte sıra TERSTİ.

Klinik öncelik artık VERİDE durur (`order_before`: [önce, sonra] neden
çiftleri) ve sırayı maliyetten ÖNCE belirler. Sıra:

    ① kalıp değişikliği GEREKTİRMEYEN nedenler (bedava eleme)
    ② klinik öncelik  ③ test maliyeti  ④ GERİ ALINAMAZ aileler en sonda

`order_before` bir KISMİ sıradır; çevrim varsa `graph_audit` yakalar.
"""
from __future__ import annotations

import functools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402


@functools.lru_cache(maxsize=1)
def deferred_families() -> frozenset:
    """GERİ ALINAMAZ aileler — KAYITTAN okunur, elde yazılmaz.

    ⚠ İlk sürüm bu üçünü sabit olarak taşıyordu ve bu, kaldırmaya
    çalıştığım ayrışma riskinin ta kendisiydi: bir ailenin
    `defer_in_diagnosis` bayrağı değişse sıralama onu GÖRMEZDİ."""
    fams = json.loads(paths.ADJUSTMENT_FAMILIES.read_text(encoding="utf-8"))
    return frozenset(f["adjustment_family_id"] for f in fams["families"]
                     if f.get("defer_in_diagnosis"))


def _priority(n: int, pairs) -> list:
    """Her nedene, kendisinden ÖNCE gelmesi gerekenlerin en uzun
    zincirine göre bir rütbe verir. Kısmi sıra yeterlidir."""
    rank = [0] * (n + 1)
    for _ in range(n):
        moved = False
        for a, b in pairs:
            if 1 <= a <= n and 1 <= b <= n and rank[b] <= rank[a]:
                rank[b] = rank[a] + 1
                moved = True
        if not moved:
            break
    return rank


def ordered_causes(sign: dict) -> list:
    """(1 tabanlı indeks, neden) çiftlerini BASILACAK sırada döndürür."""
    causes = sign["candidate_causes"]
    pairs = [tuple(p) for p in (sign.get("order_before") or [])]
    rank = _priority(len(causes), pairs)

    idx = list(enumerate(causes, 1))
    gates = [p for p in idx if not p[1].get("adjustment_family_ref")]
    rest = [p for p in idx if p[1].get("adjustment_family_ref")]
    _defer = deferred_families()
    defer = [p for p in rest if p[1]["adjustment_family_ref"] in _defer]
    rest = [p for p in rest if p not in defer]
    rest.sort(key=lambda p: (rank[p[0]], p[1].get("test_cost", 9)))
    return gates + rest + defer
