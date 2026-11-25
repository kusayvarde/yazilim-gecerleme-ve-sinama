"""ind_aadhar ve ind_pan - kolay (1'er puan). EP + BVA.

Aadhaar (UIDAI): 12 basamak, ilk basamak 2-9 (0 ve 1 olamaz), son basamak Verhoeff kontrol basamağıdır.
Test verisi tests/domains_formats/uretici.py'deki Verhoeff üreticisiyle, kütüphaneden bağımsız üretilir.
PAN (Gelir Vergisi İdaresi): AAAAA9999A = 5 harf + 4 rakam + 1 harf, büyük harf.
Not: 4. harfin (sahip türü) denetimi doküman örneğiyle ('ABCDE9999K', 4. harf D) çeliştiği için
test edilmez; raporda gereksinim belirsizliği olarak belirtilir.
"""

import pytest

from tests.domains_formats.uretici import aadhaar_uret, bosluklu, verhoeff_kontrol_basamagi
from tests.yardimci import I, V, karakter_degistir, tc


def _uret(govde: str) -> str:
    """Herhangi uzunlukta rakam gövdesine Verhoeff kontrol basamağını ekler."""
    return govde + verhoeff_kontrol_basamagi(govde)


def _grup(sayi: str) -> str:
    """Rakamları 4'erli gruplayıp boşlukla ayırır (dokümandaki biçim: '3675 9834 6015')."""
    return " ".join(sayi[i:i + 4] for i in range(0, len(sayi), 4))


_GECERLI = aadhaar_uret("23456789012")      # ilk basamak 2, 12 basamak

# =============================================================== ind_aadhar
AADHAR_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-IND_AADHAR-EP-01", _GECERLI, V, "V1 12 basamak, boşluksuz, Verhoeff doğru",
       bug="BUG-29: boşluksuz 12 basamaklı Aadhaar reddediliyor; yalnızca '4-4-4' boşluklu biçim kabul "
           "ediliyor (doküman yalnızca boşluklu örnek veriyor; UIDAI numarası 12 basamaktır)"),
    tc("TC-IND_AADHAR-EP-02", bosluklu(_GECERLI), V, "V2 4'erli boşluklu biçim, Verhoeff doğru"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-IND_AADHAR-EP-03", bosluklu(karakter_degistir(_GECERLI, 11, str((int(_GECERLI[-1]) + 1) % 10))), I,
       "I1 yanlış Verhoeff kontrol basamağı",
       bug="BUG-28: Verhoeff kontrol basamağı doğrulanmıyor; biçimi doğru her 12 basamak kabul ediliyor "
           "(dokümandaki örnek '3675 9834 6015' de Verhoeff'e göre geçersiz)"),
    tc("TC-IND_AADHAR-EP-04", bosluklu(aadhaar_uret("03456789012")), I, "I2 ilk basamak 0 (Verhoeff doğru)"),
    tc("TC-IND_AADHAR-EP-05", "", I, "I3 boş string"),
    tc("TC-IND_AADHAR-EP-06", "23456789012A", I, "I4 harf içeriyor"),
    # --- Dokümandaki örnekler ---
    tc("TC-IND_AADHAR-EP-07", "3675 9834 6015", V, "Doküman örneği (geçerli)"),
    tc("TC-IND_AADHAR-EP-08", "3675 ABVC 2133", I, "Doküman örneği (geçersiz)"),
]

AADHAR_BVA = [
    # İlk basamak alt sınırı (2): 0 ve 1 yasak; her biri Verhoeff-doğru
    tc("TC-IND_AADHAR-BVA-01", bosluklu(aadhaar_uret("12345678901")), I, "İlk basamak alt SD-1 (1)"),
    tc("TC-IND_AADHAR-BVA-02", bosluklu(aadhaar_uret("22345678901")), V, "İlk basamak alt SD (2)"),
    tc("TC-IND_AADHAR-BVA-03", bosluklu(aadhaar_uret("32345678901")), V, "İlk basamak alt SD+1 (3)"),
    # Basamak sayısı (12): boşluklu biçim, her biri Verhoeff-doğru, yalnızca uzunluk değişir
    tc("TC-IND_AADHAR-BVA-04", _grup(_uret("2345678901")), I, "Basamak sayısı SD-1 (11)"),
    tc("TC-IND_AADHAR-BVA-05", bosluklu(_GECERLI), V, "Basamak sayısı SD (12)"),
    tc("TC-IND_AADHAR-BVA-06", _grup(_uret("234567890123")), I, "Basamak sayısı SD+1 (13)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", AADHAR_EP + AADHAR_BVA)
def test_ind_aadhar(dogrula, girdi, parametreler, beklenen):
    dogrula("ind_aadhar", girdi, parametreler, beklenen)


# =============================================================== ind_pan
PAN_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-IND_PAN-EP-01", "ABCPE1234F", V, "V1 5 harf + 4 rakam + 1 harf"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-IND_PAN-EP-02", "", I, "I1 boş string"),
    tc("TC-IND_PAN-EP-03", "abcpe1234f", I, "I2 küçük harf"),
    tc("TC-IND_PAN-EP-04", "ABCPE12A4F", I, "I3 rakam bölümünde harf"),
    tc("TC-IND_PAN-EP-05", "ABCPE12345", I, "I4 son karakter rakam"),
    tc("TC-IND_PAN-EP-06", "ABCP12345F", I, "I5 ilk bölümde 4 harf + 5 rakam"),
    tc("TC-IND_PAN-EP-07", "ABCPE 234F", I, "I6 boşluk içeriyor"),
    # --- Dokümandaki örnekler ---
    tc("TC-IND_PAN-EP-08", "ABCDE9999K", V, "Doküman örneği (geçerli)"),
    tc("TC-IND_PAN-EP-09", "ABC5d7896B", I, "Doküman örneği (geçersiz)"),
]

PAN_BVA = [
    # Uzunluk (10)
    tc("TC-IND_PAN-BVA-01", "ABCPE1234", I, "Uzunluk SD-1 (9)"),
    tc("TC-IND_PAN-BVA-02", "ABCPE1234F", V, "Uzunluk SD (10)"),
    tc("TC-IND_PAN-BVA-03", "ABCPE1234FF", I, "Uzunluk SD+1 (11)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", PAN_EP + PAN_BVA)
def test_ind_pan(dogrula, girdi, parametreler, beklenen):
    dogrula("ind_pan", girdi, parametreler, beklenen)
