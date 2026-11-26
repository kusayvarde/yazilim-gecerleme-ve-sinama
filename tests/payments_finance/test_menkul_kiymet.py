"""cusip, isin, sedol - zor (3'er puan). EP + BVA.

Beklentiler docstring'deki Wikipedia bağlantıları ve standartlardan türetilmiştir:
CUSIP (ANSI X9.6, CUSIP Global Services: 9 karakter, 8 + mod-10 "çift konumu ikiye katla"
kontrolü), ISIN (ISO 6166: 2 harf ülke kodu + 9 alfasayısal NSIN + Luhn kontrolü),
SEDOL (LSE: 6 alfasayısal, sesli harf yok, ağırlık 1-3-1-7-3-9 + kontrol).
Geçerli veriler tests/payments_finance/uretici.py ile bağımsız üretilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.payments_finance.uretici import cusip_uret, isin_uret, sedol_uret
from tests.yardimci import I, V, tc

# ================================================================= cusip
CUSIP = [
    tc("TC-CUSIP-EP-01", "037833DP2", V, "Doküman örneği (geçerli)"),
    tc("TC-CUSIP-EP-02", "037833DP3", I, "Doküman örneği (geçersiz)"),
    tc("TC-CUSIP-EP-03", cusip_uret("03783310"), V, "V1 tamamen sayısal (Apple hissesi)"),
    tc("TC-CUSIP-EP-04", cusip_uret("38259P50"), V, "V2 ihraççı kodunda harf"),
    tc("TC-CUSIP-EP-05", cusip_uret("ABC12*@#"), V, "V3 özel yerleşim karakterleri * @ #"),
    tc("TC-CUSIP-EP-06", "037833101", I, "I1 yanlış kontrol basamağı"),
    tc("TC-CUSIP-EP-07", "037833DPA", I, "I2 kontrol basamağı harf"),
    tc("TC-CUSIP-EP-08", "037833dp2", I, "I3 küçük harf",
       bug="BUG-50: küçük harfli CUSIP kabul ediliyor; CUSIP karakter kümesi büyük harftir"),
    tc("TC-CUSIP-EP-09", "03783 DP2", I, "I4 gövdede boşluk"),
    tc("TC-CUSIP-EP-10", "0378!3DP2", I, "I5 izin verilmeyen özel karakter"),
    tc("TC-CUSIP-EP-11", "", I, "I6 boş girdi"),
    tc("TC-CUSIP-BVA-01", "037833DP", I, "Biçim uzunluğu SD-1 (8)"),
    tc("TC-CUSIP-BVA-02", "037833DP2", V, "Biçim uzunluğu SD (9)"),
    tc("TC-CUSIP-BVA-03", "037833DP20", I, "Biçim uzunluğu SD+1 (10)"),
]

# ================================================================== isin
ISIN = [
    tc("TC-ISIN-EP-01", "037833DP2", I, "Doküman örneği (geçersiz)"),
    tc("TC-ISIN-EP-02", "037833DP3", I, "Doküman örneği (geçersiz)"),
    tc("TC-ISIN-EP-03", isin_uret("US037833100"), V, "V1 ABD ISIN (Apple)"),
    tc("TC-ISIN-EP-04", isin_uret("GB000263494"), V, "V2 Birleşik Krallık ISIN (SEDOL gömülü)"),
    tc("TC-ISIN-EP-05", isin_uret("DE000BAY001"), V, "V3 NSIN içinde harf (Almanya)"),
    tc("TC-ISIN-EP-06", isin_uret("XS123456789"), V, "V4 uluslararası XS öneki"),
    tc("TC-ISIN-EP-07", "US0378331006", I, "I1 yanlış kontrol basamağı"),
    tc("TC-ISIN-EP-08", isin_uret("12037833100"), I, "I2 ülke kodu yerine rakam (kontrol doğru)"),
    tc("TC-ISIN-EP-09", "us0378331005", I, "I3 küçük harf",
       bug="BUG-51: küçük harfli ISIN kabul ediliyor; ISO 6166 büyük harf kullanır"),
    tc("TC-ISIN-EP-10", isin_uret("ZZ000263494"), I, "I4 ISO 3166'da olmayan ülke kodu (kontrol doğru)",
       bug="BUG-52: ISIN ülke kodu ISO 3166-1 ile karşılaştırılmıyor (ZZ kabul ediliyor)"),
    tc("TC-ISIN-EP-11", "US037833100A", I, "I5 kontrol basamağı harf"),
    tc("TC-ISIN-EP-12", "US03783#1005", I, "I6 izin verilmeyen özel karakter"),
    tc("TC-ISIN-EP-13", "", I, "I7 boş girdi"),
    tc("TC-ISIN-BVA-01", "US037833100", I, "Biçim uzunluğu SD-1 (11)"),
    tc("TC-ISIN-BVA-02", "US0378331005", V, "Biçim uzunluğu SD (12)"),
    tc("TC-ISIN-BVA-03", "US03783310050", I, "Biçim uzunluğu SD+1 (13)"),
]

# ================================================================= sedol
SEDOL = [
    tc("TC-SEDOL-EP-01", "2936921", V, "Doküman örneği (geçerli)"),
    tc("TC-SEDOL-EP-02", "29A6922", I, "Doküman örneği (geçersiz)"),
    tc("TC-SEDOL-EP-03", sedol_uret("026349"), V, "V1 tamamen sayısal (BAE Systems)"),
    tc("TC-SEDOL-EP-04", sedol_uret("B0YBKJ"), V, "V2 harfli (B serisi)"),
    tc("TC-SEDOL-EP-05", sedol_uret("B0WNLY"), V, "V3 harfli, farklı ağırlık konumları"),
    tc("TC-SEDOL-EP-06", "0263495", I, "I1 yanlış kontrol basamağı"),
    tc("TC-SEDOL-EP-07", sedol_uret("B0YEKJ"), I, "I2 sesli harf E (kontrol doğru)"),
    tc("TC-SEDOL-EP-08", "b0ybkj7", I, "I3 küçük harf"),
    tc("TC-SEDOL-EP-09", "026349A", I, "I4 kontrol basamağı harf"),
    tc("TC-SEDOL-EP-10", "026#494", I, "I5 izin verilmeyen özel karakter"),
    tc("TC-SEDOL-EP-11", "", I, "I6 boş girdi"),
    tc("TC-SEDOL-BVA-01", "026349", I, "Biçim uzunluğu SD-1 (6)"),
    tc("TC-SEDOL-BVA-02", "0263494", V, "Biçim uzunluğu SD (7)"),
    tc("TC-SEDOL-BVA-03", "02634940", I, "Biçim uzunluğu SD+1 (8)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", CUSIP)
def test_cusip(dogrula, girdi, parametreler, beklenen):
    dogrula("cusip", girdi, parametreler, beklenen)


@pytest.mark.parametrize("girdi, parametreler, beklenen", ISIN)
def test_isin(dogrula, girdi, parametreler, beklenen):
    dogrula("isin", girdi, parametreler, beklenen)


@pytest.mark.parametrize("girdi, parametreler, beklenen", SEDOL)
def test_sedol(dogrula, girdi, parametreler, beklenen):
    dogrula("sedol", girdi, parametreler, beklenen)
