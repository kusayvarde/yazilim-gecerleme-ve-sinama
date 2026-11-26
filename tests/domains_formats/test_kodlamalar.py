"""slug, base16, base32, base58, base64 - kolay (1'er puan). EP + BVA.

Beklentiler dokümandan ve RFC 4648 (base16/32/64), Bitcoin Base58 alfabesi standartlarından
türetilmiştir. Base32/Base64 geçerli örnekler RFC 4648 §10 test vektörleridir.
Base58'de sayısal uzunluk sınırı tanımlı değildir; yalnızca en küçük uzunluk (1) sınanır.
"""

import pytest

from tests.yardimci import I, V, tc
from uretici.ortak import B58

# =============================================================== slug
SLUG_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-SLUG-EP-01", "abc", V, "V1 yalnızca küçük harf"),
    tc("TC-SLUG-EP-02", "a-b", V, "V2 ortada tire"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-SLUG-EP-03", "", I, "I1 boş string"),
    tc("TC-SLUG-EP-04", "My-Slug", I, "I2 büyük harf"),
    tc("TC-SLUG-EP-05", "-abc", I, "I3 tire ile başlıyor"),
    tc("TC-SLUG-EP-06", "abc-", I, "I4 tire ile bitiyor"),
    tc("TC-SLUG-EP-07", "a_b", I, "I5 alt çizgi"),
    tc("TC-SLUG-EP-08", "a b", I, "I6 boşluk"),
    # --- Dokümandaki örnekler ---
    tc("TC-SLUG-EP-09", "my-slug-2134", V, "Doküman örneği (geçerli)"),
    tc("TC-SLUG-EP-10", "my.slug", I, "Doküman örneği (geçersiz)"),
]

SLUG_BVA = [
    # Uzunluk alt sınırı (1)
    tc("TC-SLUG-BVA-01", "", I, "Uzunluk alt SD-1 (0)"),
    tc("TC-SLUG-BVA-02", "a", V, "Uzunluk alt SD (1)"),
    tc("TC-SLUG-BVA-03", "ab", V, "Uzunluk alt SD+1 (2)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", SLUG_EP + SLUG_BVA)
def test_slug(dogrula, girdi, parametreler, beklenen):
    dogrula("slug", girdi, parametreler, beklenen)


# =============================================================== base16
BASE16_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-BASE16-EP-01", "A3F4B2", V, "V1 büyük harf hex (RFC 4648 alfabesi)"),
    tc("TC-BASE16-EP-02", "0123456789abcdef", V, "V2 tüm hex karakterleri"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-BASE16-EP-03", "", I, "I1 boş string"),
    tc("TC-BASE16-EP-04", "g1", I, "I2 hex olmayan karakter"),
    tc("TC-BASE16-EP-05", "0xab", I, "I3 0x öneki"),
    tc("TC-BASE16-EP-06", "ab cd", I, "I4 boşluk"),
    tc("TC-BASE16-EP-07", "abc", I, "I5 tek sayıda karakter (bayt başına 2 karakter)",
       bug="BUG-26: tek uzunluklu hex dizesi kabul ediliyor; RFC 4648 §8 bayt başına 2 karakter ister"),
    # --- Dokümandaki örnekler ---
    tc("TC-BASE16-EP-08", "a3f4b2", V, "Doküman örneği (geçerli)"),
    tc("TC-BASE16-EP-09", "a3f4Z1", I, "Doküman örneği (geçersiz)"),
]

BASE16_BVA = [
    # Uzunluk: bayt başına 2 karakter
    tc("TC-BASE16-BVA-01", "a", I, "Uzunluk alt SD-1 (1)",
       bug="BUG-26: tek uzunluklu hex dizesi kabul ediliyor; RFC 4648 §8 bayt başına 2 karakter ister"),
    tc("TC-BASE16-BVA-02", "ab", V, "Uzunluk alt SD (2)"),
    tc("TC-BASE16-BVA-03", "abc", I, "Uzunluk alt SD+1 (3)",
       bug="BUG-26: tek uzunluklu hex dizesi kabul ediliyor; RFC 4648 §8 bayt başına 2 karakter ister"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", BASE16_EP + BASE16_BVA)
def test_base16(dogrula, girdi, parametreler, beklenen):
    dogrula("base16", girdi, parametreler, beklenen)


# =============================================================== base32
BASE32_EP = [
    # --- Geçerli sınıflar (RFC 4648 §10 vektörleri) ---
    tc("TC-BASE32-EP-01", "MZXW6YTBOI======", V, "V1 6 dolgu karakteri ('foobar')"),
    tc("TC-BASE32-EP-02", "MZXW6===", V, "V2 3 dolgu karakteri ('foo')"),
    tc("TC-BASE32-EP-03", "MZXW6YTB", V, "V3 dolgusuz, tam blok ('fooba')"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-BASE32-EP-04", "", I, "I1 boş string"),
    tc("TC-BASE32-EP-05", "mzxw6===", I, "I2 küçük harf (alfabe büyük harf)"),
    tc("TC-BASE32-EP-06", "MY1=====", I, "I3 alfabede olmayan rakam (1)"),
    tc("TC-BASE32-EP-07", "MZXW6", I, "I4 dolgu eksik (uzunluk 8'in katı değil)",
       bug="BUG-27: base32'de uzunluk/dolgu denetlenmiyor; RFC 4648 §6 uzunluğun 8'in katı olmasını ister"),
    tc("TC-BASE32-EP-08", "MY=====", I, "I5 yanlış dolgu sayısı (5)",
       bug="BUG-27: base32'de uzunluk/dolgu denetlenmiyor; RFC 4648 §6 uzunluğun 8'in katı olmasını ister"),
    # --- Dokümandaki örnekler ---
    tc("TC-BASE32-EP-09", "MFZWIZLTOQ======", V, "Doküman örneği (geçerli)"),
    tc("TC-BASE32-EP-10", "MfZW3zLT9Q======", I, "Doküman örneği (geçersiz)"),
]

BASE32_BVA = [
    # Uzunluk 8'in katı olmalıdır
    tc("TC-BASE32-BVA-01", "MZXW6YT", I, "Blok uzunluğu SD-1 (7)",
       bug="BUG-27: base32'de uzunluk/dolgu denetlenmiyor; RFC 4648 §6 uzunluğun 8'in katı olmasını ister"),
    tc("TC-BASE32-BVA-02", "MZXW6YTB", V, "Blok uzunluğu SD (8)"),
    tc("TC-BASE32-BVA-03", "MZXW6YTBO", I, "Blok uzunluğu SD+1 (9)",
       bug="BUG-27: base32'de uzunluk/dolgu denetlenmiyor; RFC 4648 §6 uzunluğun 8'in katı olmasını ister"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", BASE32_EP + BASE32_BVA)
def test_base32(dogrula, girdi, parametreler, beklenen):
    dogrula("base32", girdi, parametreler, beklenen)


# =============================================================== base58
BASE58_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-BASE58-EP-01", "z", V, "V1 tek karakter"),
    tc("TC-BASE58-EP-02", B58, V, "V2 alfabenin tamamı (58 karakter)"),
    # --- Geçersiz sınıflar (alfabede olmayan her karakter ayrı test) ---
    tc("TC-BASE58-EP-03", "", I, "I1 boş string"),
    tc("TC-BASE58-EP-04", "ab0c", I, "I2 sıfır (0) alfabede yok"),
    tc("TC-BASE58-EP-05", "abOc", I, "I3 büyük O alfabede yok"),
    tc("TC-BASE58-EP-06", "abIc", I, "I4 büyük I alfabede yok"),
    tc("TC-BASE58-EP-07", "ablc", I, "I5 küçük l alfabede yok"),
    tc("TC-BASE58-EP-08", "ab c", I, "I6 boşluk"),
    # --- Dokümandaki örnekler ---
    tc("TC-BASE58-EP-09", "14pq6y9H2DLGahPsM4s7ugsNSD2uxpHsJx", V, "Doküman örneği (geçerli)"),
    tc("TC-BASE58-EP-10", "cUSECm5YzcXJwP", V, "Doküman örneği (geçerli, kısa)"),
]

BASE58_BVA = [
    # Uzunluk alt sınırı (1)
    tc("TC-BASE58-BVA-01", "", I, "Uzunluk alt SD-1 (0)"),
    tc("TC-BASE58-BVA-02", "z", V, "Uzunluk alt SD (1)"),
    tc("TC-BASE58-BVA-03", "zz", V, "Uzunluk alt SD+1 (2)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", BASE58_EP + BASE58_BVA)
def test_base58(dogrula, girdi, parametreler, beklenen):
    dogrula("base58", girdi, parametreler, beklenen)


# =============================================================== base64
BASE64_EP = [
    # --- Geçerli sınıflar (RFC 4648 §10 vektörleri) ---
    tc("TC-BASE64-EP-01", "Zm9vYmFy", V, "V1 dolgusuz ('foobar')"),
    tc("TC-BASE64-EP-02", "Zm9vYg==", V, "V2 2 dolgu karakteri ('foob')"),
    tc("TC-BASE64-EP-03", "Zm9vYmE=", V, "V3 1 dolgu karakteri ('fooba')"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-BASE64-EP-04", "", I, "I1 boş string"),
    tc("TC-BASE64-EP-05", "Zm9v$mFy", I, "I2 alfabede olmayan karakter ($)"),
    tc("TC-BASE64-EP-06", "Zm-_", I, "I3 URL-güvenli alfabe karakterleri (- _), standart değil"),
    tc("TC-BASE64-EP-07", "Zg==Zm9v", I, "I4 dolgu ortada"),
    tc("TC-BASE64-EP-08", "Z===", I, "I5 çok fazla dolgu (3)"),
    # --- Dokümandaki örnekler ---
    tc("TC-BASE64-EP-09", "Y2hhcmFjdGVyIHNldA==", V, "Doküman örneği (geçerli)"),
    tc("TC-BASE64-EP-10", "cUSECm5YzcXJwP", I, "Doküman örneği (geçersiz)"),
]

BASE64_BVA = [
    # Uzunluk 4'ün katı olmalıdır
    tc("TC-BASE64-BVA-01", "Zm9", I, "Blok uzunluğu SD-1 (3)"),
    tc("TC-BASE64-BVA-02", "Zm9v", V, "Blok uzunluğu SD (4)"),
    tc("TC-BASE64-BVA-03", "Zm9vY", I, "Blok uzunluğu SD+1 (5)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", BASE64_EP + BASE64_BVA)
def test_base64(dogrula, girdi, parametreler, beklenen):
    dogrula("base64", girdi, parametreler, beklenen)
