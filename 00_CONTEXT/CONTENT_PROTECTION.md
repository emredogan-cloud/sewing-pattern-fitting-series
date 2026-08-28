# CONTENT PROTECTION — ne korunur, neden

> Kardeş projelerin iki-katmanlı koruma iskeleti; korunan İÇERİK bu
> ürüne özgü olarak yeniden tanımlandı (`DECISIONS.md K9`).

---

## 1 · Neden "cevap anahtarı" modeli buraya taşınmadı

Sigorta ve Enigmatica projelerinde korunan şey gerçek, tekil bir GİZLİ
ALANDIR: `correct_answer`, bulmaca çözümü. Bir kalıp düzeltme kitabında
böyle bir alan **yoktur** — bir düzeltmenin geometrisi kamuya açık
teknik bilgidir ve telifle korunmaz (araştırma raporu § 21).

Bu yüzden koruma modeli yeniden tasarlandı, zayıflatılmadı.

## 2 · Üç koruma hattı

### ① Yayın-öncesi içerik (sıradan yayın gizliliği)

`BOOK-*/02_CONTENT/protected/`, `BOOK-*/04_EDITORIAL/pilot/`,
`02_TAXONOMY/protected/` — tam bölüm prozası, akış şemalarının nihai
metni, derlenmiş manüskript.

Gerekçe: bir rakip 13 yeni başlıkla nişi test ediyor (araştırma raporu
§ 32). Yayın öncesi tam metin görünür olmamalıdır.

### ② Fiziksel doğrulama fotoğrafları — GİZLİLİK

Bir toile prova fotoğrafı **gerçek bir insanın vücut görüntüsüdür.**
Bu, kardeş projelerin hiçbirinde bulunmayan, bu ürüne özgü bir kısıttır.

Fotoğraflar depoya **hiçbir koşulda** girmez. `VAL-xxxx` kaydı yalnızca
ölçüm sayılarını, koşulları ve sonucu taşır.

Mekanik: `.gitignore § ②` + `validate_structure.py § check_photo_leak`
(`validation_photos/`, `*_fitting_photo.*`, `*_muslin_photo.*`).

### ③ Telif korumalı referans malzeme

`01_SOURCE/reference_material/` — taranmış kitap sayfası, satın alınmış
ticari kalıp, kurs materyali. Kaynak KAYDI public, malzeme değil.

## 3 · Public kalan

kod · CI · şema · doğrulayıcı · belgeler · **taksonomi metadatası**
(id, zone, sign_class, doğrulama durumu, kaynak referansı) · kaynak
KAYITLARI · görsel notasyon sözlüğü · ölçüm ve faz raporları

Taksonomi metadatasının public olması bilinçlidir: bir belirtinin
`SYM-016` olarak adlandırılması ve `bust_chest` bölgesine ait olması
bir sır değildir. **Sır olan, o belirtinin nasıl anlatıldığıdır.**

## 4 · İzin listesi > yasak listesi

`.gitignore` her korumalı dizinde önce **her şeyi** yasaklar, sonra
adlandırılmış istisnaları açar. Yeni bir dosya türü sessizce sızamaz.

---

*Vâliçe Press · TRUE FIT · Content Protection · 28 Ağustos 2026*
