# PHASE 4 — BAĞIMSIZ TEKNİK İNCELEME

> **ÜRETİLMİŞ BELGE — elle düzenlenmez.**
> Kaynak: `06_BUILD/build_review_report.py` · ham çıktı:
> `08_REPORTS/tracked/phase4_review/R*.json`
>
> **Amaç: Kitap 1'i KIRMAK.** Bu belge bir onay değildir ve bir onay
> olarak alıntılanamaz.
>
> ⚠ **Bu bir insan uzman incelemesi DEĞİLDİR** ve hiçbir yerde öyle
> sunulamaz (`CLAIMS_STANDARD.md § 1`). Dört bağımsız inceleme hattı,
> birincil içerik üretiminden AYRI çalıştırıldı; hiçbirine kendini
> onaylama yetkisi verilmedi ve hiçbiri birincil ajanın ifadesini
> kanıt saymadı. Yine de **insan doğrulamasının yerine geçmez**:
> `D-01` ve `D-02` açık kalır.
>
> Rapor neden ÜRETİLİYOR: incelenen taraf ile raporu yazan taraf aynı
> ajandır. Tek koruma, raporun ham çıktıdan mekanik türetilmesi ve ham
> çıktının depoda durmasıdır.

---

## 1 · Kapsam ve yöntem

| Hat | İnceleme | Bulgu | Kaynak |
|---|---|---:|---:|
| ① Ölçü tanımları ve işaret noktaları | `R1_measurements` | 37 | 18 |
| ② Ease, beden seçimi ve düzeltme aileleri | `R2_ease_sizing` | 32 | 17 |
| ③ Teşhis mantığı ve belirti→neden ilişkileri | `R3_diagnostic_logic` | 66 | 22 |
| ④ Prova protokolü, karıştırıcılar ve sıra | `R4_protocol` | 14 | 23 |
| **Toplam** | | **149** | **68** (tekilleştirilmiş) |

## 2 · Sonuç dağılımı

| Sonuç | Sayı | Anlamı |
|---|---:|---|
| `CONTRADICTED` | 56 | Otoriter bir kaynak AKSİNİ söylüyor. |
| `UNSUPPORTED` | 10 | Hiçbir otoriter destek bulunamadı. |
| `CONTESTED` | 14 | Otoriter kaynaklar BİRBİRİYLE çelişiyor. |
| `SUPPORTED_NARROWER` | 40 | Yalnızca daraltılmış hâliyle doğru. |
| `SUPPORTED` | 29 | Yazıldığı hâliyle destekleniyor. |

**Revizyon gerektiren: 132/149** · **kaynak çelişkisi taşıyan: 111**

> Yalnızca bir iddia (`CC-02`, 'belirti ≠ neden') dört hattın
> hiçbirinde revizyon gerektirmedi.

## 3 · Bulgu tablosu

Faz 4 talimatı § 6'nın istediği alanlar. Tam gerekçe ve kaynak
listesi ham JSON'dadır; buradaki `Not` sütunu kısaltılmıştır.

| İddia | Kaynak | Kalite | Sonuç | Güven | Çelişki | Revizyon | Not |
|---|---|---|---|---|:---:|:---:|---|
| `AF-00` | — | internal repository check, … | `CONTRADICTED` | HIGH | evet | EVET | SIX interacts_with edges are one-way, verified by script over the file: AF-04 to AF-09, AF-05 to AF-09, AF-06 to AF-03, AF-07 to AF-08, AF-18 to AF-1… |
| `AF-07` | 2 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | THE FAMILY VIOLATES THE SERIES' OWN ORDERING RULE. E-372, verbatim: 'Make only one alteration at a time. Begin with lengthwise alterations at the sho… |
| `AF-13` | 2 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | THIS IS THE MOST CONSEQUENTIAL TAXONOMY DEFECT I FOUND, BECAUSE THE CROSSWALK ALREADY ROUTES READERS INTO IT. (a) THE PATTERN_AREA IS CONTRADICTED BY… |
| `AF-15` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | THE ORDER IS RIGHT AND IS THE ONLY ORDERING CLAIM IN THE FILE QUOTED FROM A SOURCE'S OWN FOOTNOTE - C-227, footnote 2 to the PANTS MEASUREMENT CHART:… |
| `AF-18` | 3 kaynak | pattern-publisher documenta… | `CONTRADICTED` | HIGH | evet | EVET | TWO DEFECTS. (a) THE ORDER_CONSTRAINT IS A CATEGORY ERROR AND CONTRADICTS THE FILE IT SITS IN. Choosing which two size lines to use IS a size selecti… |
| `CC-20` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | CONTRADICTED BY THE BOOK'S OWN DATA, not by a source. The rule forbids cutting; 17 of the 129 candidate causes prescribe cutting as their FIRST and o… |
| `M-015` | 3 kaynak | university + standards_body… | `CONTRADICTED` | HIGH | evet | EVET | DIRECT CONTRADICTION by an authoritative extension guide from the same publisher as the repository's own S-0001. NMSU C-220 §IV lists these as two SE… |
| `S-0004` | 2 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | CORRECTION TO MY OWN EARLIER POSITION, recorded deliberately. I first reported this document as unobtainable on the strength of a failed retrieval. I… |
| `SYM-001` | 2 kaynak | official_institutional + pe… | `CONTRADICTED` | MEDIUM | evet | EVET | Two failures. (1) The asymmetry criterion is inverted: bust volume is bilateral in the ordinary case, so the book's rule sends the commonest presenta… |
| `SYM-001.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: A front neckline that stands away from the chest, present while the wearer is upright, on bo… |
| `SYM-001.C3` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | The declared 'no measurement exists' is false, and the record refutes itself: its own physical_test is that measurement performed by superimposition … |
| `SYM-002.C1` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | Three records prescribe cutting a neckline deeper as a first test, and SYM-001's own do_not_change_yet forbids exactly that: 'Yaka egrisini KESME - y… |
| `SYM-002.C3` | 1 kaynak | official_institutional | `CONTRADICTED` | MEDIUM | evet | EVET | One family is being used for two opposite displacements with no statement of the mechanism that produces each, so the reader cannot tell which way to… |
| `SYM-003` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | Four records name round back as a cause (SYM-002.C2, SYM-003.C1, SYM-006.C2, SYM-011.C1, SYM-012.C2). Four of the five send it to AF-07; SYM-003.C1 a… |
| `SYM-003.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: Back neckline riding up and the back hem rising, with the front hem hanging correctly. \|\| WH… |
| `SYM-004` | 2 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | WSU E.M. 2246 'Garment Fitting' separates these two faults by endpoints and by tension, and I read both entries in the original. Square: 'Shoulders t… |
| `SYM-004.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: Diagonal drag lines running between the neck point and the underarm. \|\| WHY THE STATED EVIDE… |
| `SYM-005.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: A horizontal fold gathering just below the shoulder seam near the armhole. \|\| WHY THE STAT… |
| `SYM-006.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: Shoulder seam sitting behind the top-of-shoulder centreline on both shoulders, in a relaxed … |
| `SYM-007.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: The shoulder seam extends past the shoulder point onto the arm, symmetrically, with the armh… |
| `SYM-008.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: A hard pull across the back when the arm reaches forward, absent with the arm at the side.… |
| `SYM-009.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: A horizontal fold standing across the back at shoulder-blade level. \|\| WHY THE STATED EVIDEN… |
| `SYM-010.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Vertical slack folds down the back between the armholes. \|\| WHY THE STATED EVIDENCE FAILS:… |
| `SYM-013` | 1 kaynak | official_institutional | `CONTRADICTED` | MEDIUM | evet | EVET | The observation string combines two mutually exclusive signs. WSU E.M. 2246 gives the binding case and its marks precisely: 'Armhole tight, with cros… |
| `SYM-014.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: The front armhole edge standing away from the body, with slack over the upper chest. \|\| WH… |
| `SYM-016` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | WSU E.M. 2246 treats all three as ONE observation with ONE cause, and I read the entry in the original: 'Diagonal wrinkles from bust line to underarm… |
| `SYM-016.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: Drag lines radiating from the bust apex toward the side seam and armhole. \|\| WHY THE STATED … |
| `SYM-019.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Puckering or a small bubble at the point of the bust dart. \|\| WHY THE STATED EVIDENCE FAIL… |
| `SYM-020.C2` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: A hollow, collapsing area across the upper front between the collarbone and the bust. \|\| W… |
| `SYM-021.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: The button band pulling open at bust level, with the closure lying flat above and below. \|\| … |
| `SYM-022.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: The waist seam sitting above or below the natural waist by the same amount all round. \|\| W… |
| `SYM-023.C1` | 3 kaynak | official_institutional + ex… | `CONTRADICTED` | HIGH | evet | EVET | Two sourced problems, both now checked in primary texts. (1) HIP TIGHTNESS PRODUCES THE SAME SIGN AND THE LITERATURE LISTS IT FIRST. WSU E.M. 2246: '… |
| `SYM-024.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: The waistband standing away from the body at the centre back. \|\| WHY THE STATED EVIDENCE F… |
| `SYM-025.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Vertical slack folds at the waist near the side seams, with the bust and hip fitting. \|\| W… |
| `SYM-026.C2` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: The waistband binding low down, over the abdomen. \|\| WHY THE STATED EVIDENCE FAILS: C2's e… |
| `SYM-027` | 1 kaynak | peer-reviewed university | `CONTRADICTED` | HIGH | evet | EVET | This is the taxonomy paying the price for CC-22. The enum offers horizontal_fold, vertical_fold, diagonal_drag_line and strain_pull as if tightness w… |
| `SYM-027.C1` | 2 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | NMSU C-228's own remedy for a protruding derriere performs both changes in one operation, and I read the sentence in the source: 'Protruding Derriere… |
| `SYM-029` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | The record contradicts its own stated rule in the same JSON object. It is the clearest instance of a file-wide pattern: of the 20 candidate causes th… |
| `SYM-031.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Diagonal drag lines from the sleeve cap toward the bicep, worse when the arm is raised. \|\|… |
| `SYM-032.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Vertical slack folds in the upper sleeve; the sleeve hangs like a bag; the arm moves freel… |
| `SYM-033.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | symptom_schema.json states the rule explicitly in its own comment on the field: 'null = bu neden bir kalip duzeltmesi DEGILDIR (or. yapim hatasi)'. T… |
| `SYM-033.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Both sleeves twisting in the same direction, the underarm seam spiralling. \|\| WHY THE STAT… |
| `SYM-034.C3` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | The confirming_measurement and the physical_test are the same act, so the record offers no independent confirmation - measuring twice is not testing.… |
| `SYM-035` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | A reader in a badly fitting trouser sees one thing and the file gives two records with an ordering conflict between them: SYM-027's order note is sil… |
| `SYM-035.C1` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | An extension service states the coupling outright, and I verified the sentence in the PDF myself: NMSU Guide C-227 'Making Perfect Pants' (rev. April… |
| `SYM-035.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity high). Both causes produce: Horizontal drag lines below the seat with the crotch pulling up. \|\| WHY THE STATED EVIDENCE … |
| `SYM-036.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Fabric pooling in a 'U' at the front crotch, back clean. \|\| WHY THE STATED EVIDENCE FAILS:… |
| `SYM-036.C3` | 2 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | All three of this record's candidate causes move the SAME quantity. A deeper front crotch curve is a longer front crotch seam (C1), and per NMSU C-22… |
| `SYM-038.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: Both trouser legs twisting, evident standing. \|\| WHY THE STATED EVIDENCE FAILS: C1's evide… |
| `SYM-039.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: The crotch hanging low and away from the body, making it hard to stride. \|\| WHY THE STATED… |
| `SYM-040` | 4 kaynak | official_institutional + ex… | `CONTRADICTED` | HIGH | evet | EVET | All three listed causes are faults ABOVE the hem, which is CC-29 asserted as data. Two whole cause families are missing. (a) FABRIC: NMSU C-314 presc… |
| `SYM-040` | 1 kaynak | official_institutional | `CONTRADICTED` | HIGH | evet | EVET | This is the most consequential routing collision in the file, and it is created by CC-29 itself: the hem is declared a mirror of everything above, so… |
| `SYM-041.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity low). Both causes produce: The garment rotating consistently in one direction on the body. \|\| WHY THE STATED EVIDENCE FA… |
| `SYM-042.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity medium). Both causes produce: The centre-front or centre-back line not hanging perpendicular to the floor. \|\| WHY THE ST… |
| `SYM-043.C1` | — | internal_logic | `CONTRADICTED` | HIGH | evet | EVET | EVIDENCE COLLISION (severity low). Both causes produce: One dimension is the wrong length and there is no other sign at all. \|\| WHY THE STATED EVIDEN… |
| `T-10` | 4 kaynak | pattern-publisher documenta… | `CONTRADICTED` | MEDIUM | evet | EVET | Every authority I found runs the tape UNDER the arms. T-10 says 'kollarin USTUNDEN' - over/above the arms. If a reader takes that literally the tape … |
| `AF-05` | 1 kaynak | official_institutional + ex… | `UNSUPPORTED` | MEDIUM | hayır | EVET | The pattern_area is technically correct: a forward-shoulder adjustment removes width from the front shoulder, adds the same amount to the back should… |
| `AF-19` | 3 kaynak | official_institutional | `UNSUPPORTED` | HIGH | evet | EVET | THREE PROBLEMS. (a) IT IS NOT A FAMILY UNDER THE REPOSITORY'S OWN DEFINITION. T-17 defines adjustment family as 'Ayni kalip bolgesini ayni mekanikle … |
| `CC-02` | 1 kaynak | official_institutional | `UNSUPPORTED` | HIGH | evet | EVET | MEASURED, not asserted: 20 of the 43 signs carry origin_rule = null. Step 4 therefore has no mechanism at all for 47 percent of the dataset, includin… |
| `M-019` | 2 kaynak | standards_body + official_i… | `UNSUPPORTED` | MEDIUM | hayır | EVET | I could not find this measurement under this name in ISO 8559-1:2017 (its list of 5.4 surface distances has no bust-point-to-waist entry), in the AFR… |
| `M-021` | 3 kaynak | standards_body + official_i… | `UNSUPPORTED` | HIGH | evet | EVET | Worse than M-020: no source at all, and no height rule. The three authorities that do define it do not agree. ISO 8559-1:2017 5.4.7 'Across front wid… |
| `M-032` | 3 kaynak | university + standards_body… | `UNSUPPORTED` | HIGH | evet | EVET | No source, and the arithmetic is not sound as currently defined. (a) It inherits M-015's contradiction: with M-015 routed OVER the bust apex (the rec… |
| `S-0001` | 1 kaynak | official_institutional | `UNSUPPORTED` | HIGH | evet | EVET | I read NMSU C-228 end to end. It is a catalogue of alteration recipes - 'Full Bust (large cup size): Slash across the pattern along bust dart foldlin… |
| `SYM-007.C1` | 1 kaynak | official_institutional | `UNSUPPORTED` | HIGH | evet | EVET | The stated measurement returns the same result for C1 (broad-shoulder pattern on a narrow-shouldered body) and for C2 (drop-shoulder design). A numbe… |
| `SYM-020.C3` | 1 kaynak | official_institutional | `UNSUPPORTED` | MEDIUM | evet | EVET | Commercial patterns do not publish a 'high-bust equivalent'; the right-hand side of the stated comparison does not exist on the artefact the reader h… |
| `SYM-023.C1` | 1 kaynak | official_institutional | `UNSUPPORTED` | MEDIUM | evet | EVET | M-016 is a single nape-to-waist length; it has no identifiable 'part falling at waist level', so the stated comparison has no defined right-hand side… |
| `CC-10` | 6 kaynak | official_institutional + pa… | `CONTESTED` | HIGH | evet | EVET | THIS IS THE HIGHEST-RISK CLAIM IN MY DOMAIN AND IT FAILS ON THREE SEPARATE COUNTS. (1) IT MISSTATES ITS OWN SOURCE. CC-10 cites S-0003 (Texas AgriLif… |
| `CC-11` | 4 kaynak | official_institutional + pa… | `CONTESTED` | HIGH | evet | EVET | THE RULE AS WRITTEN IS CONTRADICTED BY THE INSTRUCTIONS PRINTED ON THE PATTERNS THIS BOOK'S DECLARED US READER WILL ACTUALLY BUY. Vogue/Butterick/McC… |
| `CC-13` | 6 kaynak | expert_practitioner | `CONTESTED` | HIGH | evet | EVET | This claim is written as an absolute ('must ... otherwise') and there is a genuine, documented disagreement. FOR: Tilly and the Buttons — 'Fabric wei… |
| `CC-17` | 6 kaynak | official_institutional + ex… | `CONTESTED` | HIGH | evet | EVET | Four failures, three of them now checked against the primary texts. (1) THE SOURCES DO NOT GIVE A SEQUENCE. EM4582's own framing is 'As you fit, KEEP… |
| `CC-24` | 5 kaynak | official_institutional + un… | `CONTESTED` | MEDIUM | evet | EVET | THE CITED SOURCE CONTAINS NOTHING ABOUT DRAG LINES. I read EM4582 in full: no diagonal wrinkles, no drag lines, no wrinkles pointing anywhere. CC-24 … |
| `CC-28` | 5 kaynak | official_institutional | `CONTESTED` | HIGH | evet | EVET | RULE-BY-RULE. (1) LENGTH BEFORE WIDTH — SUPPORTED. E-372 verbatim: 'Make only one alteration at a time. Begin with lengthwise alterations at the shou… |
| `M-004` | 11 kaynak | standards_body + official_i… | `CONTESTED` | HIGH | evet | EVET | The recorded conflict is REAL and is more serious than the repository states. Six mutually incompatible authoritative conventions exist. (a) ISO 8559… |
| `M-005` | 4 kaynak | university + standards_body | `CONTESTED` | HIGH | evet | EVET | The repository's range is not any source's range. Verbatim: NMSU C-227, body-measurement list item 2: 'High hip (3 inches below waist)'; but the same… |
| `M-020` | 5 kaynak | standards_body + official_i… | `CONTESTED` | HIGH | evet | EVET | Not reproducible as written, and the field disagrees with itself about what 'across back' even means. (1) The record is internally inconsistent: its … |
| `M-024` | 4 kaynak | university + standards_body | `CONTESTED` | HIGH | evet | EVET | The record contradicts its OWN cited source. Texas AgriLife E-372, 'Know your measurements' (S-0003): 'Take all measurements snugly, but not tightly,… |
| `M-025` | 4 kaynak | standards_body + official_i… | `CONTESTED` | HIGH | evet | EVET | The recorded conflict is REAL. Body-measurement side: ISO 8559-1:2017 lists 5.1.15 'Inside leg height' (a vertical height, therefore from the floor) … |
| `S-0001` | 4 kaynak | official_institutional + ed… | `CONTESTED` | HIGH | evet | EVET | I VERIFIED C-228 TABLE 1 LINE BY LINE FROM THE PDF and it does not carry the load the repository puts on it. Its ease column reads: Bust 3-4; High Bu… |
| `SYM-043` | 2 kaynak | official_institutional + ex… | `CONTESTED` | MEDIUM | evet | EVET | SOURCE-vs-SOURCE CONFLICT, verified on both sides. E-372 supports length-before-width explicitly. The Palmer/Pletsch tissue-fitting excerpt, in the b… |
| `T-05` | 2 kaynak | educational + expert_practi… | `CONTESTED` | MEDIUM | evet | EVET | Two problems with T-05 as written. (a) 'TAM ESDEGER' overstates the equivalence. Multiple patternmaking references distinguish the terms: a sloper is… |
| `AF-01` | 2 kaynak | official_institutional | `SUPPORTED_NARROWER` | HIGH | hayır | EVET | The order is well supported. E-372: 'Begin with lengthwise alterations at the shoulder or neck and work down ... Many problems in side seams, bust ar… |
| `AF-02` | 1 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | hayır | EVET | The pattern_area is technically correct and C-228's 'High Bust' and 'Low Bust' alterations are exactly this family (fold out above or below the dart … |
| `AF-06` | 2 kaynak | official_institutional | `SUPPORTED_NARROWER` | HIGH | evet | EVET | TWO DEFECTS, both against the record's own cited source. (a) METHOD FAMILY MISSING. C-228's neckline alterations are not all curve reshaping: 'Gaping… |
| `AF-08` | 2 kaynak | official_institutional + ex… | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | The ordering principle is sound and is the consensus of the practitioner literature: the shoulder slope, armhole depth, across-back, across-front and… |
| `AF-14` | 2 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | pattern_area is correct for the classic centre-back shortening. TWO ISSUES. (a) A RECORDED SOURCE CONFLICT ON THE TERM ITSELF, which the repository d… |
| `AF-16` | 1 kaynak | official_institutional | `SUPPORTED_NARROWER` | HIGH | hayır | EVET | pattern_area is exactly right and matches C-227's procedure ('extending seam at crotch point ... redraw crotch curve ... redraw inseam from new crotc… |
| `AF-17` | 1 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | hayır | hayır | pattern_area is correct and verbatim supported: C-227, 'To increase leg circumference: Place a piece of paper under the front and back pattern pieces… |
| `CC-01` | 2 kaynak | official_institutional | `SUPPORTED_NARROWER` | HIGH | hayır | EVET | The three-number structure is directly supported by E-372, read in full: 'Measure each pattern piece at points that correspond with body measurements… |
| `CC-03` | 4 kaynak | university + official_insti… | `SUPPORTED_NARROWER` | HIGH | evet | EVET | The principle is supported but the claim as written is both weaker and narrower than its sources. Weaker: NMSU C-220 §I is imperative and the reposit… |
| `CC-05` | 1 kaynak | official_institutional | `SUPPORTED_NARROWER` | HIGH | evet | EVET | The principle is right but S-0006 does not support the protocol as stated. NHANES's quality-control design (Appendix B, 'Gold Standard Replicate Exam… |
| `CC-06` | 4 kaynak | university + standards_body | `SUPPORTED_NARROWER` | HIGH | evet | EVET | Two things are being claimed and only one is sourced. SOURCED: the size-selection role. Texas AgriLife E-372, verbatim: 'Select the smaller size patt… |
| `CC-08` | 5 kaynak | official_institutional + st… | `SUPPORTED_NARROWER` | HIGH | hayır | EVET | The separation itself is not in doubt and is stated by the extension literature in a form the book can use: NMSU C-220 says verbatim 'The amount of e… |
| `CC-12` | 3 kaynak | official_institutional + ed… | `SUPPORTED_NARROWER` | HIGH | evet | EVET | THE PRINCIPLE IS WELL SOURCED. Texas E-372, verbatim: 'First, smooth the pattern pieces flat. Pin in darts, pleats or gathers as though sewn. Measure… |
| `CC-15` | 4 kaynak | official_institutional | `SUPPORTED_NARROWER` | HIGH | evet | EVET | The underlying mechanism is well supported. E-372: 'Measure from seamline to seamline'; and 'If the alteration needed is 1 inch (2.5 cm) or less, alt… |
| `CC-20` | 3 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | hayır | EVET | The irreversibility premise is stated almost word for word by E-372: 'Once the fabric is cut, however, fitting adjustments are limited to existing da… |
| `CC-21` | 3 kaynak | expert_practitioner | `SUPPORTED_NARROWER` | MEDIUM | hayır | EVET | FIRST HALF SUPPORTED. Palmer/Pletsch's published order is literally an apply-and-re-observe loop across three tissue-fittings plus a fabric fit-as-yo… |
| `CC-22` | 6 kaynak | official_institutional + pe… | `SUPPORTED_NARROWER` | HIGH | evet | EVET | THE CITED SOURCE DOES NOT CONTAIN THIS RULE. I read EM4582 in full; there is no fold-axis rule in it. CC-22 is currently an unsourced claim wearing a… |
| `CC-23` | 4 kaynak | official_institutional + pe… | `SUPPORTED_NARROWER` | HIGH | hayır | EVET | The best-sourced claim in Chapter 7 and the only one EM4582 actually carries. Verbatim, from the copy I read: 'Ease. The garment should be neither to… |
| `CC-25` | 1 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | The principle is sound and partly supported by E-372's insistence on undergarments, shoes and repeat measurement. But the taxonomy inverts its own ru… |
| `CC-25` | 6 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | PER-ITEM CHECK against authority. (1) Fabric — SUPPORTED, E-372's opening: 'Standards of good fit are influenced by many things such as the current f… |
| `CC-26` | 8 kaynak | official_institutional + pe… | `SUPPORTED_NARROWER` | HIGH | evet | EVET | THIS ONE THE CITED SOURCE DOES CARRY, VERBATIM. WSU EM4582: 'Grain. The lengthwise grain should be perpendicular to the floor. The crosswise grain sh… |
| `CC-27` | 1 kaynak | expert_practitioner | `SUPPORTED_NARROWER` | MEDIUM | hayır | EVET | The practice is universal across PDF pattern publishers and is a genuine, checkable step, so the claim is right. Two honest limits. (a) NO AUTHORITAT… |
| `CC-29` | 7 kaynak | official_institutional + ex… | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | THE CITED SOURCE DOES NOT STATE THIS CLAIM. EM4582 says only 'Hems should be parallel to the floor', listed under Line among the five basic points - … |
| `CC-30` | 4 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | hayır | EVET | The reuse principle is institutionally supported, but in a materially different form from the claim. Every authority I read records the amount ON THE… |
| `CC-31` | 3 kaynak | educational | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | IS IT DEFENSIBLE OR A SALES ARGUMENT? Both — it is a real inference with a real confounder that the claim does not control for, and the uncontrolled … |
| `M-001` | 6 kaynak | university + standards_body | `SUPPORTED_NARROWER` | HIGH | evet | EVET | The measurement is real and institutionally recognised. NMSU C-228 Table 1: 'High Bust — Measure just above breasts, under the arms, and across the f… |
| `M-009` | 4 kaynak | standards_body + official_i… | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | ISO 8559-1:2017 defines 5.3.20 'Thigh girth' AND 5.3.21 'Mid-thigh girth' as different measurements, so 'thigh' alone is under-specified. AFRL/HSIAC … |
| `M-018` | 3 kaynak | standards_body + official_i… | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | The measurement exists but the repository has put it in the wrong measurement class. ISO 8559-1:2017 files it as 5.2.3 'Bust point width' under 5.2 '… |
| `M-022` | 3 kaynak | standards_body + official_i… | `SUPPORTED_NARROWER` | HIGH | evet | EVET | The measurement IS recognised — under a different name. ISO 8559-1:2017 lists 5.4.6 'Scye depth length' among the surface distances. AFRL/HSIAC 737: … |
| `M-026` | 4 kaynak | university + standards_body… | `SUPPORTED_NARROWER` | HIGH | evet | EVET | The seated method is genuinely and precisely supported by the repository's own source. NMSU C-227, body measurement 9, verbatim: 'Crotch depth. Sit o… |
| `M-028` | 5 kaynak | standards_body + official_i… | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | Supported as craft practice but not as a single standard measurement, and the arm position in the record does not match its own source. NMSU C-228 Ta… |
| `M-030` | 3 kaynak | official_institutional + st… | `SUPPORTED_NARROWER` | HIGH | hayır | EVET | The measurement is standard (ISO 8559-1:2017 5.1.1 'Stature'; AFRL/HSIAC 805) but the record omits the controlling technique. NHANES 2021 §3.4.3 verb… |
| `M-031` | 4 kaynak | university + standards_body | `SUPPORTED_NARROWER` | HIGH | evet | EVET | Two separate defects. (1) SCOPE: the cited source supports SIZE SELECTION, not shaping amount. Texas AgriLife E-372 verbatim: 'For best results, top … |
| `M-033` | 4 kaynak | standards_body + university | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | The quantity is meaningful and its downstream use is well supported — ISO 8559-2:2017 Table 1 makes hip girth the PRIMARY dimension for women's trous… |
| `SYM-016.C2` | 1 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | Eight of the 129 causes carry NO_PHYSICAL_TEST. That is defensible in itself - some causes really are documentary - but the seven-step cycle has no p… |
| `SYM-029.C1` | 1 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | A right/left waist-to-floor difference confirms that the two sides differ; it does not confirm that a hip is 'higher or fuller', because an unequal l… |
| `SYM-029.C1` | 3 kaynak | official_institutional | `SUPPORTED_NARROWER` | MEDIUM | evet | EVET | A higher hip needs length redistributed; a fuller hip needs volume; a longer leg needs the hem. Three different corrections behind one cause string a… |
| `T-06` | 2 kaynak | educational | `SUPPORTED_NARROWER` | HIGH | hayır | EVET | The definition matches Threads #221's 'MINIMUM EASE / Also called "wearing ease", it is needed for a garment to go around the body, be reasonably com… |
| `T-08` | 2 kaynak | educational + official_inst… | `SUPPORTED_NARROWER` | MEDIUM | hayır | hayır | The decomposition is the standard one and is consistent with C-228's footnote arithmetic (36 in body + 2.5 in ease = 38.5 in pattern measurement). On… |
| `T-09` | 2 kaynak | official_institutional | `SUPPORTED_NARROWER` | HIGH | evet | EVET | The definition names only seam allowances. Both cited extension sources make dart exclusion mandatory and equally important - C-227: 'Do not include … |
| `AF-03` | 2 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | hayır | Both pattern_area and order_constraint are correct and directly sourced. C-228 'Sloping Shoulders: Redraw shoulder seam and armscye seams, sloping an… |
| `AF-04` | 2 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | EVET | Technically correct and sourced. C-228 'Broad Shoulders: Slash from midpoint of shoulder down and across to the middle of armscye. Spread pattern the… |
| `AF-09` | 1 kaynak | official_institutional + ex… | `SUPPORTED` | HIGH | hayır | hayır | Correct and well founded. The armhole-before-cap dependency is standard, and C-228's large-arm procedure demonstrates the coupling arithmetically: 'M… |
| `AF-10` | 2 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | hayır | pattern_area is correct and the order_constraint is a local instance of E-372's global length-before-width rule. C-228's Large Arm alteration operate… |
| `AF-11` | 1 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | EVET | The claim is directly and verbatim supported by the record's own cited source, yet the record grades itself unverified. That is an evidence-layer err… |
| `AF-12` | 2 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | EVET | Both the pattern_area and the order are correct and are covered by sources ALREADY IN THE REPOSITORY, yet source_refs is empty. C-227 gives the proce… |
| `CC-02` | 3 kaynak | official_institutional + pe… | `SUPPORTED` | HIGH | hayır | hayır | Directly supported by the book's own cited source, verbatim: Texas AgriLife E-372, 'Make alterations at the source of the problem. For example, when … |
| `CC-04` | 5 kaynak | official_institutional + un… | `SUPPORTED` | HIGH | evet | EVET | Supported almost verbatim, but over-generalised as written. NHANES 2021 §3.4.8: 'Position the tape in a horizontal plane at the level of the measurem… |
| `CC-07` | 3 kaynak | university | `SUPPORTED` | HIGH | hayır | EVET | Supported verbatim and could be stated more usefully. Texas AgriLife E-372, 'Know your measurements': 'Measurements should be taken AT LEAST EVERY 6 … |
| `CC-09` | 4 kaynak | educational (technical maga… | `SUPPORTED` | HIGH | evet | EVET | The wearing/design split is a genuine, long-standing industry distinction and NOT this project's invention. Threads #221 (Louise Cutting) heads its l… |
| `CC-14` | 3 kaynak | expert_practitioner | `SUPPORTED` | MEDIUM | hayır | EVET | The practice and the stated purpose are both confirmed by practitioner and draping sources: Closet Core (Susan Khalje method) — 'All pattern marks ar… |
| `CC-16` | 4 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | EVET | Directly supported at institutional level, but note the sources state it for MEASURING rather than for the fitting session: E-372 — 'Take all measure… |
| `CC-18` | 4 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | EVET | Supported at institutional level, though as an ease criterion rather than as a named protocol. E-372 fit checklist: 'Adequate wearing ease is availab… |
| `CC-19` | 1 kaynak | official_institutional | `SUPPORTED` | HIGH | hayır | EVET | The task brief records CC-19 as having NO source. That is a repository error, not a real gap: the project's own S-0003 states the rule verbatim — 'Ma… |
| `M-002` | 4 kaynak | standards_body + university | `SUPPORTED` | HIGH | hayır | hayır | ISO 8559-1:2017 defines 5.3.4 'Bust girth' and 3.1.11 'bust point — most anterior point of the bust WHEN WEARING BRA' (Note 2 refers to 4.1.1 for the… |
| `M-003` | 5 kaynak | standards_body + university… | `SUPPORTED` | HIGH | hayır | EVET | ISO 8559-1:2017 3.1.20 'under bust level — level directly below breast when wearing a bra' and 5.3.8 'Under bust girth'. AFRL/HSIAC 232: 'Chest circu… |
| `M-006` | 6 kaynak | standards_body + official_i… | `SUPPORTED` | HIGH | hayır | hayır | ISO 8559-1:2017 3.1.25: 'hip level — level of the greatest projection at the back of the body (buttocks)'; 5.3.13 Hip girth and 5.3.14 'Maximum hip g… |
| `M-007` | 3 kaynak | standards_body + university | `SUPPORTED` | MEDIUM | hayır | hayır | ISO 8559-1:2017 lists 5.3.16 'Upper-arm girth' (clause-5 wording not obtained). NMSU C-220 §IV.15: 'Upper arm circumference. Measure around fullest p… |
| `M-008` | 4 kaynak | standards_body + official_i… | `SUPPORTED` | HIGH | evet | EVET | The project has correctly RECORDED a conflict but has MIS-CLASSIFIED it. It is not two rival definitions of one measurement; it is two different stan… |
| `M-010` | 4 kaynak | standards_body + official_i… | `SUPPORTED` | MEDIUM | evet | hayır | The definition is right even though the record cites nothing. ISO 8559-1:2017 3.1.17: 'centre point of kneecap — centre of patella when the thigh mus… |
| `M-011` | 2 kaynak | standards_body + official_i… | `SUPPORTED` | MEDIUM | hayır | hayır | ISO 8559-1:2017 5.3.24 'Calf girth' (and 5.3.25 'Minimum leg girth' separately). AFRL/HSIAC 207: 'Calf Circumference — the maximum horizontal circumf… |
| `M-013` | 6 kaynak | standards_body + official_i… | `SUPPORTED` | HIGH | evet | EVET | As with M-008 the recorded 'conflict' is really two different standard measurements. ISO 8559-1:2017 defines BOTH 5.3.2 'Neck girth' and 5.3.3 'Neck … |
| `M-014` | 5 kaynak | standards_body + official_i… | `SUPPORTED` | HIGH | hayır | hayır | Best-supported record in the file. ISO 8559-1:2017 3.1.1 'shoulder point — most lateral point of the lateral edge of the spine (acromial process) of … |
| `M-016` | 5 kaynak | standards_body + official_i… | `SUPPORTED` | HIGH | hayır | hayır | ISO 8559-1:2017 3.1.6: 'back neck point — tip of the prominent bone at the base of the back of the neck (spinous process of the seventh cervical vert… |
| `M-017` | 3 kaynak | standards_body + official_i… | `SUPPORTED` | HIGH | hayır | hayır | ISO 8559-1:2017 5.4.10 'Side neck point to bust point' (listed under 5.4, distances measured following the surface of the body). AFRL/HSIAC 648: 'Nec… |
| `M-023` | 4 kaynak | standards_body + official_i… | `SUPPORTED` | HIGH | hayır | hayır | ISO 8559-1:2017 5.4.21 'Side waist to hip'. AFRL/HSIAC 947: 'Waist Hip Length — the surface distance between the right waist (omphalion) landmark and… |
| `M-027` | 3 kaynak | university + standards_body… | `SUPPORTED` | HIGH | evet | EVET | The measurement itself is exactly right and exactly sourced. NMSU C-227 item 10, verbatim: 'Crotch length. Measure from center front waist through cr… |
| `M-029` | 4 kaynak | standards_body + official_i… | `SUPPORTED` | MEDIUM | evet | hayır | ISO 8559-1:2017 5.4.14 'Upper arm length (shoulder to elbow, elbow bent)' — the elbow-bent condition is in the standard's own title, so the record ma… |
| `T-07` | 3 kaynak | educational + pattern-publi… | `SUPPORTED` | HIGH | hayır | hayır | Matches Threads #221: 'DESIGN EASE - This is volume added to a pattern to achieve a desired look. It can be a couple of inches or many. Note that thi… |

## 4 · EN YÜKSEK RİSKLİ 20 TEKNİK İDDİA

Dört hattın `top_risks` çıktısı, şiddet sırasına dizildi.

| # | İddia | Önerilen eylem | Neden riskli |
|---:|---|---|---|
| 1 | `CC-24` | `physical_validation` | Step 4 of the seven-step cycle (LOCALIZE) has no mechanism other than this claim. Its cited source contains nothing about drag lines at all - I read EM4582 in full. The authorities that do … |
| 2 | `SYM-013` | `physical_validation` | The observation string combines two opposite armhole faults ('binds when the arm is lowered' = armhole too high; 'the garment is pulled up from the shoulder' = armhole too low). C1's remedy… |
| 3 | `M-015` | `further_research` | Contradicted by NMSU Guide C-220, which defines centre front length as measured STRAIGHT DOWN and treats the over-the-bust route as a separate measurement ('bodice length over bust'). The r… |
| 4 | `M-020` | `further_research` | Across back is not reproducible as written: the record's landmarks (armhole creases) and its stated level (shoulder blades) are two different heights, no vertical position is given, and the… |
| 5 | `M-024` | `further_research` | The record lists 'measuring with shoes' as an error while its own cited source, Texas AgriLife E-372, instructs the reader to 'wear shoes similar to those usually worn'. It is nonetheless s… |
| 6 | `CC-05` | `further_research` | NHANES's replicate protocol is an INTER-observer check performed after the landmark marks are erased. The repository's self-repeat, performed against an elastic left in place per CC-03, can… |
| 7 | `AF-13` | `further_research` | AF-13's pattern_area is declared 'Back trouser/skirt' but its own cited sources place hip and side-hip volume on front AND back, and the taxonomy has NO abdomen family despite C-228 naming … |
| 8 | `AF-07` | `further_research` | AF-07 bundles round back (a length and posture correction) with broad and narrow back (width corrections) in one family whose only ordering note is 'read together with AF-11'. CC-28 asserts… |
| 9 | `AF-19` | `further_research` | AF-18 and AF-19 are methods presented as families - each has exactly one method_family and neither has a real pattern area - and they duplicate decisions already owned by AF-10, AF-11, AF-1… |
| 10 | `SYM-040` | `further_research` | CC-29 asserted as data. All three candidate causes are faults above the hem; bias drop in flared and bias-cut garments and off-grain cutting - both attested in extension publications, and o… |
| 11 | `CC-25` | `further_research` | Not one of the 20 confounder-class or design-intent causes is listed first in its sign; 13 are last and 7 second. Step 6 tells the reader to test one hypothesis and to test the cheapest fir… |
| 12 | `CC-31` | `further_research` | The series bridge to Book 3 rests on an inference with an uncontrolled confounder and no source. Every pattern from one company derives from that company's block, so 'this alteration is nee… |
| 13 | `CC-25` | `further_research` | The count is internally contradictory: three specification documents say nine, the claim and the data say eleven. Worse, the eleven are not operationalised — each sign lists only 3–5, so th… |
| 14 | `M-008` | `additional_source` | The recorded 'contested' status is a mis-diagnosis: wrist girth and hand girth are two different standard measurements (ISO 8559-1 5.3.19 and 5.5.1), not two definitions of one. Because onl… |
| 15 | `M-019` | `additional_source` | No definition of this measurement was found in ISO 8559-1, the AFRL/HSIAC definitions manual, the ANSUR II variable list, or any of the three NMSU guides, and the record carries no source. … |
| 16 | `S-0001` | `additional_source` | The repository's declared single ease source, NMSU C-228 Table 1, has no waist row at all, assigns girth ease to the high bust and low bust (which are not garment circumferences), mixes gir… |
| 17 | `S-0004` | `additional_source` | Two of the book's four core rules are cited to a document that does not contain them. I obtained EM4582 at the exact URL in the project's own source record and read all eight pages: it carr… |
| 18 | `CC-14` | `additional_source` | The claim is sound but the two cited authorities do not support it — E-372 (read in full) contains no toile-marking instruction at all, and S-0004 could not be opened to check. The evidence… |
| 19 | `M-004` | `cautious_wording` | The whole book's vertical geometry, M-005, M-015, M-016, M-019, M-023, M-024, M-026, M-027, M-032 and M-033 are all defined from a waist whose definition ('narrowest point of the torso') is… |
| 20 | `M-001` | `cautious_wording` | Everything downstream of M-031, CC-06 and CC-10 rests on the high bust, yet its path rule ('göğüs dokusunun ÜZERİNDEN geçer') permits the tape to sit on the upper slope of the breast, it ha… |

## 5 · Ayırt edici kanıt ÇAKIŞMALARI

**28 çakışma, 28 belirtide** (yüksek 9 · orta 17 · düşük 2).

Şema her aday nedenin bir `distinguishing_evidence` taşımasını
**dayatıyordu**; incelemeci o alanların GERÇEKTEN ayırıp ayırmadığını
denetledi. Bir alanın dolu olması, işini yaptığı anlamına gelmiyordu.

**Çözüm uydurulmadı.** Çakışmalar
`02_TAXONOMY/public/evidence_collisions.json`'a kaydedildi ve
`06_BUILD/atlas.py` bunları OKURA BEYAN eder: *"bu iki neden aynı
görünebilir, ikisini de sına."* Ayrımın kendisi `D-02` fiziksel
doğrulamasına bağlıdır.

| Belirti | Şiddet | Neden ayırmıyor |
|---|---|---|
| `SYM-001` | high | C1's evidence is 'gap present while standing upright AND symmetric'; C2's is 'gap ASYMMETRIC toward the bust ... increases markedly on bending forward'. Two defects. Fir… |
| `SYM-003` | high | C1's entire distinguishing evidence is 'the front hem is fine, ONLY the back rises'. All three candidate causes are located in the back, so all three produce exactly tha… |
| `SYM-004` | high | The stated primary discriminator is the line's DIRECTION - C1 'lines run from the neck point OUT AND DOWN', C2 'lines run the other way, from the shoulder tip toward the… |
| `SYM-006` | high | C1's evidence is 'the seam is behind on BOTH shoulders; it is like this in a relaxed stance too'. A round back (C2) is bilateral and present in a relaxed stance. A short… |
| `SYM-007` | high | C2 is 'the design is deliberately drop-shouldered'. A drop-shoulder design produces C1's evidence word for word: symmetric overhang, armhole seam outside the arm bone. C… |
| `SYM-009` | high | C2's location marker ('the fold is CONCENTRATED at blade level, fading downward') restates where_it_appears, which is already 'blade level, between the two armholes'. C1… |
| `SYM-016` | high | A dart whose tip stops well short of the apex (C3) also produces lines radiating from the apex and can also lift the front hem. C3's discriminator is 'total front width … |
| `SYM-021` | high | C3 is 'there is no button at apex level'. When there is no button at the apex the gap opens at bust level and the closure is clean above and below - which is C1's distin… |
| `SYM-035` | high | Crotch depth is a component of crotch length; the two measurements (M-026, M-027) are not independent. C1's own physical test - 'increase the crotch depth at the lengthe… |
| `SYM-005` | medium | C1's evidence is 'the fold is near the shoulder TIP, absent on the neck side'. The upper armhole is the shoulder-tip region, so C2's location marker ('the fold follows t… |
| `SYM-008` | medium | C1's evidence is 'no sign with the arm at the side; only when the arm comes forward' - which is the observation restated. All three causes are movement-revealed. C2 and … |
| `SYM-010` | medium | C1's evidence is 'the folds are vertical and symmetric'. A pattern one size too large (C2) produces vertical symmetric folds in the back. C2's exclusive marker is 'the s… |
| `SYM-014` | medium | C1's evidence is 'looseness is felt over the upper chest'; C2's is 'together with the gap there is an EMPTY AREA ABOVE THE BUST'. The upper chest and the area above the … |
| `SYM-019` | medium | C1's evidence is 'the bubble is exactly at the dart tip' - which is the observation and the where_it_appears field, restated. Nothing in C1 excludes an over-deep dart (C… |
| `SYM-020` | medium | C2 is 'upper front width excessive' with evidence 'the hollow is spread over a WIDE AREA'; C3 is 'the pattern was drawn for a fuller upper bust' with evidence 'the hollo… |
| `SYM-022` | medium | C1's evidence is 'the displacement is EQUAL all round, the same in front and back'. A deliberately raised or dropped waistline (C3) is equal all round by construction. C… |
| `SYM-024` | medium | C2 is 'the waist-to-hip ratio differs from the pattern's' but its evidence describes HIP fit ('the waistband sits on the waist but the hip area is tight or loose') and s… |
| `SYM-025` | medium | C1's evidence is 'folds vertical and symmetric; bust and hip FIT'. If the bust and hip fit and only the waist is loose, that is the definition of insufficient waist shap… |
| `SYM-026` | medium | C2's evidence is 'the constriction is below the waist, at abdomen level'; C3's is 'the constriction is only in FRONT; the back is comfortable'. The abdomen is in front. … |
| `SYM-031` | medium | C1's evidence is 'the lines are concentrated at the bicep line; they increase markedly when the arm is raised' - the second half is the observation restated. More fundam… |
| `SYM-032` | medium | C1's evidence is 'the folds are vertical; arm movement is completely free'. A deliberately full sleeve (C2) gives vertical folds and free movement. C1 does not exclude t… |
| `SYM-033` | medium | C1's evidence is 'the twist is in the SAME direction on both sleeves'. A forward arm carriage - the sleeve-pitch mismatch that C2 describes - is bilateral and produces e… |
| `SYM-036` | medium | C3's evidence is 'the NUMBERS ARE CORRECT but the curve is too deep'. A deeper front crotch curve necessarily lengthens the front crotch seam, which is the number C1 mea… |
| `SYM-038` | medium | C1's evidence is 'the twist is symmetric on both legs and evident standing'. An unbalanced front/back crotch curve (C2) is a pattern fault and therefore bilateral and ev… |
| `SYM-039` | medium | C1's evidence is 'the gap between crotch and body is present standing; comfortable sitting'. A deliberately dropped crotch (C2) gives the same. A waistband sitting below… |
| `SYM-042` | medium | C1's evidence is 'the deviation is symmetric and persists in the reader's natural stance'. A volume pulling the fabric (C2) is symmetric and persists in the natural stan… |
| `SYM-041` | low | C1's evidence is 'the rotation is consistent in one direction and the same at every wearing'. Body asymmetry (C2) also rotates consistently in one direction at every wea… |
| `SYM-043` | low | C1's evidence is 'the garment sits correctly everywhere, balance lines correct, no drag or fold - ONLY the length differs'. A deliberate design length (C2) and a differe… |

## 6 · İncelemenin ULAŞAMADIĞI kaynaklar

Bir incelemenin bulamadıkları da bulguları kadar kayda değerdir.

- *(R1_measurements)* ISO 8559-1:2017 clauses 4 and 5 (measuring conditions, and the procedural wording of each of the 90+ measurements). Only the table of contents and clause 3 (landmark points, levels, lines and planes) are in the free previews I could reach (GSO and Ethiopian identical adoptions); pages 17–79 of the …
- *(R1_measurements)* ASTM D5219-25 Standard Terminology Relating to Body Dimensions for Apparel Sizing. Paywalled; I verified only that the designation exists and is ACTIVE (16 pages, Book of Standards 07.02, subcommittee D13.55, DOI 10.1520/D5219-25), which confirms the repository's S-0015 record including its note th…
- *(R1_measurements)* ANSUR II NATICK/TR-15/007 itself (DTIC ADA611869 and the Penn State mirror both failed to serve the PDF). I verified the repository's S-0005 locator INDIRECTLY and it holds: enumerating the ANSUR II public female dataset header confirms cervicaleheight = measurement 22, chestcircumference = 24, int…
- *(R1_measurements)* Texas AgriLife E-373 'Personal Measurement Chart' — the document E-372 defers to for all measuring instructions. Not retrievable, exactly as the repository already records. Consequently NO landmark definition in this file can currently be supported by S-0003, and eight records cite S-0003 for exact…
- *(R1_measurements)* The WHO Expert Consultation report on Waist Circumference and Waist-Hip Ratio (HTTP 403). The WHO protocol wording quoted here is taken from the MRC Epidemiology Unit (University of Cambridge) Measurement Toolkit, which attributes it to the WHO STEPS manual.
- *(R1_measurements)* Whether the bust-minus-high-bust difference predicts the AMOUNT of bust shaping required. I found no controlled study, no standards clause and no extension publication testing this; the pattern-company convention of one inch per cup appears only in practitioner blogs, which I did not fetch and do n…
- *(R1_measurements)* Whether the seated crotch-depth measurement (M-026) agrees numerically with a standing/calculated body rise. Both methods are documented; no source I reached quantifies the difference caused by soft-tissue compression on the seat. REQUIRES_PHYSICAL_TEST.
- *(R1_measurements)* M-012 is absent from measurements.json (the file jumps M-011 to M-013) and the file's own $comment does not explain the gap. Whether this is an intentional retirement or a data loss could not be determined from the file itself.
- *(R2_ease_sizing)* Burda's official size-selection guidance for skirts and trousers. The official Burda sizing PDF (burdastyle.fr/media/productattach/s/i/sizes_burda_style.pdf) returned HTTP 403 and I could not read it. My statement that Burda selects skirts and trousers by the hip rests on a search-engine summary, n…
- *(R2_ease_sizing)* The Vogue/Butterick/McCall's fitting guide on a publisher-owned domain. mccallpattern.mccall.com/size-charts now 301-redirects to simplicity.com/mccalls-patterns. I read the guide's text on two independent retailer reproductions (jaycotts.co.uk and weaverdee.com), which agree with each other, but I…
- *(R2_ease_sizing)* ASTM D5585-21 and D5586/D5586M-10. I read only the ASTM catalogue records; both standards are paywalled and I did NOT read their contents. The statement that pattern publishers do not follow them rests on secondary reporting plus the direct observation that the published pattern-company charts diff…
- *(R2_ease_sizing)* PS 42-70 and CS 215-58 themselves. I did not open either document. The 1970 effective date, the supersession of CS 215-58, and the 1983 withdrawal come from secondary academic and trade sources, not from the standards.
- *(R2_ease_sizing)* Threads Magazine article pages (threadsmagazine.com/2023/01/18/learn-about-garment-ease, /2016/07/20/qa-proper-sequence-for-pattern-adjustments, /project-guides/...) all returned HTTP 403. The only Threads material I actually read is the Threads #221 PDF, which is why every Threads figure I quote i…
- *(R2_ease_sizing)* American Sewing Guild, 'Adding Ease to Your Garment' - HTTP 503, not read.
- *(R2_ease_sizing)* Simplicity's downloadable Sizing.pdf - fetched but contains no extractable text layer, so I used the HTML size-charts page instead.
- *(R2_ease_sizing)* Patternmaking textbook ease values (Helen Joseph Armstrong, Patternmaking for Fashion Design; Winifred Aldrich, Metric Pattern Cutting for Women's Wear). I did not open either book; only secondary summaries were available, which disagreed with each other (Armstrong's fitted bodice block is reported…
- *(R2_ease_sizing)* Whether the 2-inch and 2.5-inch drafted cup differences hold across the whole size range of any given company, or widen with size. Cashmerette publishes per-size high bust columns rather than a constant offset, which implies the offset is not constant, but I found no publisher statement of how it v…
- *(R2_ease_sizing)* Whether AF-08's 'armhole is the last bodice adjustment' and AF-17's 'leg girth after the crotch' are taught as ordering rules by any institutional source. Neither appears in the five extension guides I read in full; both rest on practitioner consensus only.
- *(R3_diagnostic_logic)* Galada, A. & Baytar, F. (2025), Fashion and Textiles 12(1), DOI 10.1186/s40691-025-00417-y — FULL TEXT. I verified the article's existence, authors, journal, DOI, CC-BY licence and reference list (which includes Veblen 2012 and Liechty/Rasband/Pottberg-Steineckert 2016) through DOI content negotiat…
- *(R3_diagnostic_logic)* SDSU Extension Circular, 'Facts about Fitting' (1968), openprairie.sdstate.edu — reported to contain the most precise drag-line rule found anywhere ('If there is a group of wrinkles they will generally point in the direction of the seam to be let out. A line drawn at right angles from the center of…
- *(R3_diagnostic_logic)* Texas AgriLife single-topic alteration leaflets E-375 (Bodice Back Width), E-376, E-377, E-383 (Upper Arm Sleeve Width) and E-384 — the same series as the book's own S-0003, reported to contain further horizontal-wrinkle-from-tightness counterexamples and one direct source-vs-source conflict on the…
- *(R3_diagnostic_logic)* Threads Magazine, 'Fitting Revelations: Read Your Clothes to Identify Key Fit Issues' - the four-cell wrinkle rule (tight/loose x horizontal/vertical) reached me only through a search-engine extract. threadsmagazine.com returns HTTP 403 to WebFetch and to curl with a browser user-agent; I could not…
- *(R3_diagnostic_logic)* Texas A&M AgriLife 'Shoulder Slope' publication (oaktrust.library.tamu.edu/bitstream/handle/1969.1/87753/pdf_693.pdf) - HTTP 403 to WebFetch and to curl with a browser UA. This is the document that would settle whether square shoulders present as diagonal drag lines (as SYM-004 asserts) or as horiz…
- *(R3_diagnostic_logic)* Wild Ginger, 'Solving Fit Issues' (Shanley & Campbell), wildginger.com/pdffiles/pmfittingguide.pdf - connection refused (ECONNREFUSED). Repeatedly surfaced in searches as a systematic wrinkle-diagnosis reference; not read.
- *(R3_diagnostic_logic)* Liechty, Rasband & Pottberg-Steineckert, 'Fitting & Pattern Alteration' - the standard textbook for drag-line diagnosis, and the source Yang & Baytar cite for the tight/loose x horizontal/vertical/diagonal taxonomy. Not obtained; only its bibliographic description and publisher copy were seen. The …
- *(R3_diagnostic_logic)* Utah Education Network CTE handout S5_PatternAlterationsTips.pdf - HTTP 404.
- *(R3_diagnostic_logic)* Porter, M. E. (1969), 'Analysis of the Fit of Women's Custom-Made Pants', M.S. thesis, Oregon State University - reported to me by a sub-researcher as showing that total-crotch-length measurement predicts the needed alteration significantly better than crotch-depth measurement (tailor's square accu…
- *(R3_diagnostic_logic)* Threads Magazine, 'Fitting a High Hip vs. Sway Back' - the exact distinction SYM-023 and SYM-029 need. HTTP 403.
- *(R3_diagnostic_logic)* Texas A&M AgriLife E-390 'Special Alterations for Pants' and B-1295, and UNL Extension EC69-455 - the trouser-diagnosis publications that would most directly test SYM-027, SYM-035 and SYM-036. All returned 403/503.
- *(R3_diagnostic_logic)* Palmer/Pletsch, 'Pants for Real People' - the primary practitioner authority for SYM-035 and SYM-036. Only the publisher's fitting excerpt from a different title was obtainable.
- *(R3_diagnostic_logic)* Whether 'sway back' as used in fitting is the same condition as 'sway back posture' in kinesiology (which denotes posterior pelvic tilt with a FLATTENED lumbar spine, not the lumbar hollow the sewing sense implies). The book uses the sewing sense throughout; the possible collision with the clinical…
- *(R3_diagnostic_logic)* THE CENTRAL UNVERIFIABLE ITEM, stated plainly: the 129 distinguishing_evidence fields are the book's actual product, and no documentary source distinguishes two causes of the SAME sign from each other. The project says this itself (SOURCE_MAP.md section 6; DIAGNOSTIC_SYSTEM.md section 6.4) and I co…
- *(R4_protocol)* WSU Extension EM4582 'Challenging Patterns' (Ettl) — the repository's S-0004 and a cited source for CC-13, CC-14, CC-17, CC-22, CC-23, CC-24, CC-26, CC-29. The only copy I could locate is an expiring signed Amazon S3 link from the WSU library, which returned HTTP 403 to WebFetch and to curl; the WS…
- *(R4_protocol)* Threads Magazine articles ('To Get the Right Armhole, Fit the Bodice'; 'Use a Sloper to Alter Patterns'; 'Before You Hem a Bias Garment, Let the Fabric Hang Out'; 'Proper Fitting for a Forward Shoulder'). Every threadsmagazine.com URL returned HTTP 403 behind a Cloudflare challenge to both WebFetch…
- *(R4_protocol)* Iowa State University Extension 'State 4-H Awardrobe Clothing Event — Checklist for Ready-to-Wear' (HTTP 403). This appeared in search results to contain institutional movement-check language ('Will you be bending over? If so, try it in front of the mirror'), which would have raised CC-18's movemen…
- *(R4_protocol)* Seamwork/Colette help-centre article on the test square (HTTP 403). No institutional or standards-body tolerance for home-printed pattern scale was found anywhere; the 1 mm figure in the CC-27 proposed wording is practitioner convention only.
- *(R4_protocol)* Liechty, Rasband & Pottberg-Steineckert, 'Fitting and Pattern Alteration: A Multi-Method Approach' (Bloomsbury/Fairchild) — the standard university textbook for this exact subject, and the natural authority for the five fit standards (grain, set, line, balance, ease), for adjustment ordering and fo…
- *(R4_protocol)* Whether the eleven confounders can actually be distinguished from pattern faults in practice — the word 'indistinguishable' in CC-25 and the discriminating-evidence layer beneath it. This is REQUIRES_PHYSICAL_TEST and the repository already says so (SOURCE_MAP § 1 row C-H, DIAGNOSTIC_SYSTEM § 6.4).
- *(R4_protocol)* ISO 8559-1 and ASTM D5219 were not consulted for this domain; they govern measurement definitions and body dimensions, not fitting protocol, so they would not settle any claim in this brief.

## 7 · Bu incelemenin YAPAMADIĞI

1. **Okur anlıyor mu.** Tek gerçek sınav `D-01`'dir.
2. **Teşhis ilişkileri doğru mu.** 129 nedensel ilişki belgesel
   kanıtla çözülemez; tek gerçek sınav `D-02`'dir. İnceleme
   ilişkilerin İÇ TUTARLILIĞINI denetleyebildi, DOĞRULUĞUNU değil.
3. **Diyagramlar geometrik olarak doğru mu.** `D-02`.
4. **Baskıda okunuyor mu.** `D-05`, `D-06`.

---

*Vâliçe Press · BEFORE YOU CUT · Phase 4 Independent Technical Review · ÜRETİLMİŞ*
