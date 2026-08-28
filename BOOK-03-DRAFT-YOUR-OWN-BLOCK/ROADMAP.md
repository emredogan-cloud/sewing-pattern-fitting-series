# ROADMAP — TRUE FIT 3: Draft Your Own Block

> **Bu yol haritası YÜRÜTÜLMEDİ.** Görev talimatı § 40 uyarınca
> planlandı ve burada durur.
>
> **Açılma koşulu:** Kitap 2 P1 onayı (aile→blok crosswalk'ının
> doğrulanması için). Kitap 2'nin YAYIMLANMASINA bağımlı değildir.

---

## Faz akışı

```text
   P0 Temel  →  P1 Çizim Metodolojisi Araştırması + Sistem Seçimi
       │           ╞═ KURUCU ONAY (A10: hangi sistem) ═╡
       ▼
   P2 Görsel Sistem (MİRAS)
       │
       ▼
   P3 Pilot + FİZİKSEL ÇİZİM DOĞRULAMASI ──[FAIL]──HARD STOP
       │  [PASS]
       ▼
   P4 Tam Üretim  →  P5 KA  →  P6 Format  →  P7 Lansman
```

---

## P0 — TEMEL · `foundation`

Dizin, `book_config.json`, `.gate`, kayıt defterleri.

---

## P1 — ÇİZİM METODOLOJİSİ ARAŞTIRMASI + SİSTEM SEÇİMİ · `phase1-spec`

**Kurucu bağımlılığı:** **KRİTİK** — `A10` ve `A3`

### Bu fazın ana sorusu

> Hangi çizim sistemi? Ve **neden o?**

Görev talimatı § 18'in açık uyarısı: *"Do not assume a particular
drafting method is automatically correct."* Bu proje bir sistemi
peşinen seçmez.

### Görevler

1. **Sistem karşılaştırması.** En az üç yerleşik çizim yaklaşımı,
   aynı ölçütlerle: girdi ölçü sayısı · matematik yükü · ev dikişçisi
   için erişilebilirlik · doğrulanabilirlik · Kitap 1'in ölçü
   çerçevesiyle (`M-xxx`) uyumu · IP durumu.
2. **Ölçü seti genişletmesi** (`TOP-21`). Kitap 1'in 32 ölçüsü teşhis
   içindir; blok çizimi EK ölçüler ister. Hangileri, neden — ve neden
   bunlar Kitap 1'e KONULMADI.
3. **Çizim sırası** (`TOP-22`). Hangi adım hangisinden önce, ve her
   adımın hangi ölçüyü tükettiği.
4. **Denge ve çözgünün ÇİZİMDE kurulması** (`TOP-24`). Kitap 1
   dengeyi GÖRMEYİ öğretir; Kitap 3 onu KURMAYI öğretir — ayrı beceri.
5. **Blok sınama toile'i protokolü** (`TOP-27`). Referans yalnızca
   bedenin kendisidir; ticari kalıp YOKTUR.
6. **Rafine etme döngüsü.** İlk blok nadiren doğrudur; kaç tur, hangi
   ölçütle durulur.
7. **Kitap 2 → Kitap 3 crosswalk doğrulaması.** 19 ailenin 18'i bir
   blok bileşenine bağlandı; bu eşleme teknik olarak doğru mu.
8. **`AF-18` istisnasının işlenmesi.** Beden dereceleme blokta yoktur —
   bu, bir eksik değil, kitabın **satış argümanıdır**; nasıl anlatılacağı.
9. **IP kontrolü.** Seçilen sistemin geometrisi telifle korunmaz, ama
   bir kitabın ANLATIMI korunur — her çizim adımı sıfırdan yazılır
   (`IP_AND_BRAND_POLICY.md § 2`).

### Definition of Done

Sistem seçimi **gerekçeli** olarak yapıldı ve `DECISIONS.md`'ye
yazıldı · reddedilen sistemler ve red gerekçeleri kayıtlı ·
ölçü seti genişletildi · çizim sırası tanımlandı · kurucu onayı ·
`.gate` → `phase1-spec`.

### Risk

**KRİTİK — metodoloji riski.** Yanlış sistem seçimi kitabın tamamını
yeniden yazmayı gerektirir. Bu yüzden karar **kaynak edinimine** (`A3`)
bağlıdır: sistem seçimi otoriter kaynak olmadan yapılamaz.

---

## P2 — GÖRSEL SİSTEM (MİRAS) · `phase2-visual`

Kitap 1'in token seti ve figür motoru devralınır. Beklenen tek yeni
ihtiyaç: `figure_type: drafting_step` — adım adım çizim figürleri.

**Ölçülebilir hedef:** Kitap 1'in P2'sinden belirgin biçimde kısa.

---

## P3 — PİLOT + FİZİKSEL ÇİZİM DOĞRULAMASI · `phase3-pilot` · **HARD STOP**

**Kill-gate (bu kitaba özgü ve serinin en sert ölçümü):**

| Ölçüm | PASS koşulu | FAIL sonucu |
|---|---|---|
| **Çizim doğruluğu** — pilot bölümdeki blok, yazılı adımlar TAM OLARAK izlenerek çizilir ve toile dikilir | Blok bedene oturur; ölçüler beklenen değerleri verir | Sistem veya anlatım yeniden tasarlanır |
| **Bağımsız uygulanabilirlik** — üç gerçek dikişçi bloğu **yalnızca kitapla** çizer | En az **2/3** kullanılabilir bir blok üretir | Anlatım ve figür dili yeniden tasarlanır |

Bu, serinin en sert ölçümüdür çünkü çıktı bir düzeltme değil **bir
kalıptır**: hata gizlenemez.

---

## P4 — TAM ÜRETİM · P5 — KA · P6 — FORMAT · P7 — LANSMAN

| Faz | Ayırt edici görev |
|---|---|
| P4 | 12 blok bileşeninin tamamı; her adım tek ölçüye bağlı |
| P5 | Dört hat + **hesap doğrulaması**: her formül/oran bağımsız olarak yeniden hesaplanır |
| P6 | Format kapısı; **çizim sayfalarının ölçek doğruluğu** kritik — basılı ölçekte bir hata tüm kitabı geçersiz kılar |
| P7 | Lansman + üç yönlü karşılıklı reklam hedeflemesi tamamlanır |

---

## Devralınan çerçeve — Kitap 1 ve 2'den ne gelir

| Varlık | Kaynak | Kitap 3'teki rolü |
|---|---|---|
| Ölçü çerçevesi (32 `M-xxx`) | Kitap 1 | **Birincil kullanıcı** + `TOP-21` ekleri |
| Terminoloji (20 `T-xx`) | Kitap 1 | Değiştirilemez |
| Görsel notasyon (18 `TK-xx`) | Kitap 1 | Değiştirilemez |
| Belirti taksonomisi | Kitap 1 | Blok sınama toile'inde ATIF |
| Düzeltme aileleri | Kitap 2 | Seçici — "bu tekrar neden oluyordu" köprüsü |
| Fiziksel doğrulama protokolü | Seri | Aynen |

---

*Vâliçe Press · TRUE FIT 3 · Roadmap (planlandı, yürütülmedi) · 28 Ağustos 2026*
