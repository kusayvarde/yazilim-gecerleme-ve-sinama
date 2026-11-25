"""between ve length - orta (2'şer puan). EP + BVA.

Beklentiler dokümandan türetilmiştir: değer [min_val, max_val] kapalı aralığındaysa True;
min_val/max_val verilmezse o taraf denetlenmez; ikisi de yoksa sonuç her zaman True.
Kapsam dışı: min_val > max_val (ValueError), negatif uzunluk (ValueError) ve tür
uyuşmazlığı (TypeError) kütüphane hata fırlattığı için bu şemada (ValidationError dönüşü
beklenen) test edilemez; raporda belirtilir.
"""

from datetime import datetime

import pytest

from tests.yardimci import I, V, tc

# =============================================================== between
BETWEEN_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-BETWEEN-EP-01", 5, V, "V1 tamsayı aralık içinde", min_val=1, max_val=10),
    tc("TC-BETWEEN-EP-02", 5, V, "V2 sınır verilmedi (her zaman True)"),
    tc("TC-BETWEEN-EP-03", -5, V, "V3 negatif sayı aralık içinde", min_val=-10, max_val=-1),
    tc("TC-BETWEEN-EP-04", "b", V, "V4 metin aralık içinde", min_val="a", max_val="c"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-BETWEEN-EP-05", 0, I, "I1 min_val altında", min_val=1, max_val=10),
    tc("TC-BETWEEN-EP-06", 11, I, "I2 max_val üstünde", min_val=1, max_val=10),
    tc("TC-BETWEEN-EP-07", "d", I, "I3 metin aralık dışında", min_val="a", max_val="c"),
    # --- Dokümandaki örnekler ---
    tc("TC-BETWEEN-EP-08", 5, V, "Doküman örneği (geçerli, min_val)", min_val=2),
    tc("TC-BETWEEN-EP-09", 13.2, V, "Doküman örneği (geçerli, ondalık)", min_val=13, max_val=14),
    tc("TC-BETWEEN-EP-10", 500, I, "Doküman örneği (geçersiz)", max_val=400),
    tc("TC-BETWEEN-EP-11", datetime(2000, 11, 11), V, "Doküman örneği (geçerli, tarih)",
       min_val=datetime(1999, 11, 11)),
]

BETWEEN_BVA = [
    # Alt sınır (min_val=1)
    tc("TC-BETWEEN-BVA-01", 0, I, "Alt sınır SD-1 (0)", min_val=1, max_val=10),
    tc("TC-BETWEEN-BVA-02", 1, V, "Alt sınır SD (1)", min_val=1, max_val=10),
    tc("TC-BETWEEN-BVA-03", 2, V, "Alt sınır SD+1 (2)", min_val=1, max_val=10),
    # Üst sınır (max_val=10)
    tc("TC-BETWEEN-BVA-04", 9, V, "Üst sınır SD-1 (9)", min_val=1, max_val=10),
    tc("TC-BETWEEN-BVA-05", 10, V, "Üst sınır SD (10)", min_val=1, max_val=10),
    tc("TC-BETWEEN-BVA-06", 11, I, "Üst sınır SD+1 (11)", min_val=1, max_val=10),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", BETWEEN_EP + BETWEEN_BVA)
def test_between(dogrula, girdi, parametreler, beklenen):
    dogrula("between", girdi, parametreler, beklenen)


# =============================================================== length
LENGTH_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-LENGTH-EP-01", "abcd", V, "V1 uzunluk aralık içinde", min_val=2, max_val=6),
    tc("TC-LENGTH-EP-02", "abcd", V, "V2 sınır verilmedi (her zaman True)"),
    tc("TC-LENGTH-EP-03", "", V, "V3 boş string + min_val=0", min_val=0),
    tc("TC-LENGTH-EP-04", "çğışöü", V, "V4 Unicode karakter sayısıyla ölçülür", min_val=6, max_val=6),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-LENGTH-EP-05", "a", I, "I1 min_val'den kısa", min_val=2, max_val=6),
    tc("TC-LENGTH-EP-06", "abcdefgh", I, "I2 max_val'den uzun", min_val=2, max_val=6),
    tc("TC-LENGTH-EP-07", "", I, "I3 boş string + min_val=1", min_val=1),
    # --- Dokümandaki örnekler ---
    tc("TC-LENGTH-EP-08", "something", V, "Doküman örneği (geçerli, min_val)", min_val=2),
    tc("TC-LENGTH-EP-09", "something", V, "Doküman örneği (geçerli, min=max)", min_val=9, max_val=9),
    tc("TC-LENGTH-EP-10", "something", I, "Doküman örneği (geçersiz)", max_val=5),
]

LENGTH_BVA = [
    # Alt sınır (min_val=3)
    tc("TC-LENGTH-BVA-01", "ab", I, "Alt sınır SD-1 (2)", min_val=3, max_val=6),
    tc("TC-LENGTH-BVA-02", "abc", V, "Alt sınır SD (3)", min_val=3, max_val=6),
    tc("TC-LENGTH-BVA-03", "abcd", V, "Alt sınır SD+1 (4)", min_val=3, max_val=6),
    # Üst sınır (max_val=6)
    tc("TC-LENGTH-BVA-04", "abcde", V, "Üst sınır SD-1 (5)", min_val=3, max_val=6),
    tc("TC-LENGTH-BVA-05", "abcdef", V, "Üst sınır SD (6)", min_val=3, max_val=6),
    tc("TC-LENGTH-BVA-06", "abcdefg", I, "Üst sınır SD+1 (7)", min_val=3, max_val=6),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", LENGTH_EP + LENGTH_BVA)
def test_length(dogrula, girdi, parametreler, beklenen):
    dogrula("length", girdi, parametreler, beklenen)
