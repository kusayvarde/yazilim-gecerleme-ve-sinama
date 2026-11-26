"""country_code, currency, iban (zor, 3'er puan) ve calling_code (orta, 2 puan). EP + BVA.

Beklentiler dokümandan ve standartlardan türetilmiştir: ISO 3166-1 (alpha-2, alpha-3, numeric),
ISO 4217, ISO 13616 (IBAN, mod-97-10), ITU-T E.164 (ülke çağrı kodu 1-3 basamak).
IBAN test verisi uretici/domains_formats.py ile standarda göre üretilir.
"""

import pytest

from uretici.domains_formats import iban_uret
from tests.yardimci import I, V, tc
from uretici.ortak import karakter_degistir

# =============================================================== country_code
COUNTRY_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-COUNTRY_CODE-EP-01", "US", V, "V1 alpha-2 (auto)"),
    tc("TC-COUNTRY_CODE-EP-02", "tr", V, "V2 küçük harf + ignore_case=True", ignore_case=True),
    tc("TC-COUNTRY_CODE-EP-03", "004", V, "V3 baştaki sıfırlı numeric (Afganistan)", iso_format="numeric"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-COUNTRY_CODE-EP-04", "", I, "I1 boş string"),
    tc("TC-COUNTRY_CODE-EP-05", "us", I, "I2 küçük harf (varsayılan: büyük/küçük harf duyarlı)"),
    tc("TC-COUNTRY_CODE-EP-06", "ZZ", I, "I3 atanmamış alpha-2"),
    tc("TC-COUNTRY_CODE-EP-07", "999", I, "I4 atanmamış numeric"),
    tc("TC-COUNTRY_CODE-EP-08", "840", I, "I5 numeric değeri + iso_format=alpha2", iso_format="alpha2"),
    tc("TC-COUNTRY_CODE-EP-09", "U5", I, "I6 rakam karışık alpha-2"),
    tc("TC-COUNTRY_CODE-EP-10", "US ", I, "I7 sonda boşluk"),
    # --- Dokümandaki örnekler ---
    tc("TC-COUNTRY_CODE-EP-11", "GB", I, "Doküman örneği (geçersiz, alpha3 beklenirken alpha-2)",
       iso_format="alpha3"),
    tc("TC-COUNTRY_CODE-EP-12", "USA", V, "Doküman örneği (geçerli)"),
    tc("TC-COUNTRY_CODE-EP-13", "840", V, "Doküman örneği (geçerli, numeric)", iso_format="numeric"),
    tc("TC-COUNTRY_CODE-EP-14", "iN", I, "Doküman örneği (geçersiz, karışık harf)", iso_format="alpha2"),
    tc("TC-COUNTRY_CODE-EP-15", "ZWE", V, "Doküman örneği (geçerli, alpha3)", iso_format="alpha3"),
]

COUNTRY_BVA = [
    # Alfabetik kod uzunluğu alt sınırı (2)
    tc("TC-COUNTRY_CODE-BVA-01", "U", I, "Alfabetik kod alt SD-1 (1)"),
    tc("TC-COUNTRY_CODE-BVA-02", "US", V, "Alfabetik kod alt SD (2)"),
    tc("TC-COUNTRY_CODE-BVA-03", "USA", V, "Alfabetik kod alt SD+1 (3)"),
    # Alfabetik kod uzunluğu üst sınırı (3)
    tc("TC-COUNTRY_CODE-BVA-04", "USAA", I, "Alfabetik kod üst SD+1 (4)"),
    # Numeric kod aralığı (004 ... 894)
    tc("TC-COUNTRY_CODE-BVA-05", "003", I, "Numeric alt SD-1 (003)", iso_format="numeric"),
    tc("TC-COUNTRY_CODE-BVA-06", "004", V, "Numeric alt SD (004)", iso_format="numeric"),
    tc("TC-COUNTRY_CODE-BVA-07", "894", V, "Numeric üst SD (894)", iso_format="numeric"),
    tc("TC-COUNTRY_CODE-BVA-08", "895", I, "Numeric üst SD+1 (895)", iso_format="numeric"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", COUNTRY_EP + COUNTRY_BVA)
def test_country_code(dogrula, girdi, parametreler, beklenen):
    dogrula("country_code", girdi, parametreler, beklenen)


# =============================================================== currency
CURRENCY_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-CURRENCY-EP-01", "EUR", V, "V1 ISO 4217 kodu"),
    tc("TC-CURRENCY-EP-02", "usd", V, "V2 küçük harf + ignore_case=True", ignore_case=True),
    tc("TC-CURRENCY-EP-03", "$", V, "V3 sembol + skip_symbols=False", skip_symbols=False),
    tc("TC-CURRENCY-EP-04", "XXX", V, "V4 'para birimi yok' özel kodu (ISO 4217)",
       bug="BUG-25: ISO 4217'de tanımlı XXX/XTS/XAU reddediliyor, XDR/XOF/XAF kabul ediliyor (tutarsız)"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-CURRENCY-EP-05", "", I, "I1 boş string"),
    tc("TC-CURRENCY-EP-06", "usd", I, "I2 küçük harf (varsayılan: büyük/küçük harf duyarlı)"),
    tc("TC-CURRENCY-EP-07", "AAA", I, "I3 atanmamış 3 harfli kod"),
    tc("TC-CURRENCY-EP-08", "$", I, "I4 sembol + skip_symbols=True (varsayılan)"),
    tc("TC-CURRENCY-EP-09", "US1", I, "I5 rakam içeriyor"),
    tc("TC-CURRENCY-EP-10", "?", I, "I6 geçersiz sembol (skip_symbols=False)", skip_symbols=False),
    # --- Dokümandaki örnekler ---
    tc("TC-CURRENCY-EP-11", "USD", V, "Doküman örneği (geçerli)"),
    tc("TC-CURRENCY-EP-12", "ZWX", I, "Doküman örneği (geçersiz)"),
]

CURRENCY_BVA = [
    # Kod uzunluğu (3)
    tc("TC-CURRENCY-BVA-01", "US", I, "Kod uzunluğu SD-1 (2)"),
    tc("TC-CURRENCY-BVA-02", "USD", V, "Kod uzunluğu SD (3)"),
    tc("TC-CURRENCY-BVA-03", "USDD", I, "Kod uzunluğu SD+1 (4)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", CURRENCY_EP + CURRENCY_BVA)
def test_currency(dogrula, girdi, parametreler, beklenen):
    dogrula("currency", girdi, parametreler, beklenen)


# =============================================================== calling_code
CALLING_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-CALLING_CODE-EP-01", "+1", V, "V1 tek basamaklı kod (+1)"),
    tc("TC-CALLING_CODE-EP-02", "+44", V, "V2 iki basamaklı kod (+44)"),
    tc("TC-CALLING_CODE-EP-03", "+971", V, "V3 üç basamaklı kod (+971)"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-CALLING_CODE-EP-04", "", I, "I1 boş string"),
    tc("TC-CALLING_CODE-EP-05", "+999", I, "I2 atanmamış kod"),
    tc("TC-CALLING_CODE-EP-06", "+9a", I, "I3 harf içeriyor"),
    tc("TC-CALLING_CODE-EP-07", "+ 44", I, "I4 boşluk içeriyor"),
    tc("TC-CALLING_CODE-EP-08", "++44", I, "I5 çift artı işareti"),
    # --- Dokümandaki örnekler ---
    tc("TC-CALLING_CODE-EP-09", "+91", V, "Doküman örneği (geçerli)"),
    tc("TC-CALLING_CODE-EP-10", "-31", I, "Doküman örneği (geçersiz)"),
]

CALLING_BVA = [
    # Rakam sayısı: 1-3 (E.164)
    tc("TC-CALLING_CODE-BVA-01", "+", I, "Rakam sayısı alt SD-1 (0)"),
    tc("TC-CALLING_CODE-BVA-02", "+1", V, "Rakam sayısı alt SD (1)"),
    tc("TC-CALLING_CODE-BVA-03", "+44", V, "Rakam sayısı alt SD+1 (2)"),
    tc("TC-CALLING_CODE-BVA-04", "+971", V, "Rakam sayısı üst SD (3)"),
    tc("TC-CALLING_CODE-BVA-05", "+1234", I, "Rakam sayısı üst SD+1 (4)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", CALLING_EP + CALLING_BVA)
def test_calling_code(dogrula, girdi, parametreler, beklenen):
    dogrula("calling_code", girdi, parametreler, beklenen)


# =============================================================== iban
_DE = "370400440532013000"            # 18 -> toplam 22
_NO = "86011117947"                   # 11 -> toplam 15 (en kısa IBAN)
_MT = "MALT011000012345MTLCAST001S"   # 27 -> toplam 31 (uzun IBAN)

IBAN_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-IBAN-EP-01", iban_uret("GB", "WEST12345698765432"), V, "V1 Birleşik Krallık (22, harfli BBAN)"),
    tc("TC-IBAN-EP-02", iban_uret("FR", "20041010050500013M02606"), V, "V2 Fransa (27)"),
    tc("TC-IBAN-EP-03", iban_uret("TR", "0006100519786457841326"), V, "V3 Türkiye (26)"),
    tc("TC-IBAN-EP-04", iban_uret("NO", _NO), V, "V4 Norveç (15, en kısa)"),
    tc("TC-IBAN-EP-05", iban_uret("MT", _MT), V, "V5 Malta (31, uzun)"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-IBAN-EP-06", "", I, "I1 boş string"),
    tc("TC-IBAN-EP-07", karakter_degistir(iban_uret("DE", _DE), 21, "1"), I, "I2 yanlış kontrol basamağı (mod-97)"),
    tc("TC-IBAN-EP-08", iban_uret("XX", "1234567890123456"), I, "I3 bilinmeyen ülke kodu (mod-97 doğru)",
       bug="BUG-23: ISO 13616 kaydında olmayan ülke kodu (XX) mod-97 doğruysa kabul ediliyor"),
    tc("TC-IBAN-EP-09", iban_uret("DE", _DE).lower(), I, "I4 küçük harf (elektronik biçim büyük harf)",
       bug="BUG-24: küçük harfli IBAN kabul ediliyor; ISO 13616 elektronik biçimi büyük harftir (doküman belirtmiyor)"),
    tc("TC-IBAN-EP-10", "DE89 3704 0044 0532 0130 00", I, "I5 boşluklu (basılı) biçim"),
    tc("TC-IBAN-EP-11", "8" + iban_uret("DE", _DE)[1:], I, "I6 ülke kodu rakamla başlıyor"),
    tc("TC-IBAN-EP-12", iban_uret("DE", _DE)[:-1] + "#", I, "I7 özel karakter"),
    # --- Dokümandaki örnekler ---
    tc("TC-IBAN-EP-13", "DE29100500001061045672", V, "Doküman örneği (geçerli)"),
    tc("TC-IBAN-EP-14", "123456", I, "Doküman örneği (geçersiz)"),
]

IBAN_BVA = [
    # Almanya IBAN uzunluğu (22): mod-97 her uzunlukta doğru, yalnızca uzunluk değişir
    tc("TC-IBAN-BVA-01", iban_uret("DE", _DE[:-1]), I, "Almanya uzunluğu SD-1 (21)",
       bug="BUG-22: ülkeye özgü IBAN uzunluğu denetlenmiyor; mod-97 doğruysa 15-34 arası her uzunluk kabul ediliyor"),
    tc("TC-IBAN-BVA-02", iban_uret("DE", _DE), V, "Almanya uzunluğu SD (22)"),
    tc("TC-IBAN-BVA-03", iban_uret("DE", _DE + "0"), I, "Almanya uzunluğu SD+1 (23)",
       bug="BUG-22: ülkeye özgü IBAN uzunluğu denetlenmiyor; mod-97 doğruysa 15-34 arası her uzunluk kabul ediliyor"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", IBAN_EP + IBAN_BVA)
def test_iban(dogrula, girdi, parametreler, beklenen):
    dogrula("iban", girdi, parametreler, beklenen)
