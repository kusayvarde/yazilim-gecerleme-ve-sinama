"""validators.cron - zor (3 puan). EP + BVA.

Gereksinim belirsizliği: doküman */n, a-b, a,b sözdizimini açıkça tanımlamıyor;
beklenen sonuçlar standart Unix cron davranışına göre yazıldı.
"""

import pytest

from tests.yardimci import I, V, tc

EP = [
    # --- Geçerli sınıflar ---
    tc("TC-CRON-EP-01", "* * * * *", V, "V1 tüm alanlar *"),
    tc("TC-CRON-EP-02", "*/5 * * * *", V, "V2 adım */n"),
    tc("TC-CRON-EP-03", "0-30 9-17 * * 1-5", V, "V3 aralık a-b"),
    tc("TC-CRON-EP-04", "0,15,30 * * * *", V, "V4 liste a,b"),
    tc("TC-CRON-EP-05", "30 6 15 8 3", V, "V5 tam sayılar"),
    tc("TC-CRON-EP-06", "0-59/15 * * * *", V, "V6 aralık + adım a-b/n"),
    # --- Geçersiz sınıflar ---
    tc("TC-CRON-EP-07", "* * *", I, "I1 alan sayısı az (3)"),
    tc("TC-CRON-EP-08", "* * * * * * *", I, "I2 alan sayısı fazla (7)"),
    tc("TC-CRON-EP-09", "75 * * * *", I, "I3 dakika aralık dışı"),
    tc("TC-CRON-EP-10", "30-20 * * * *", I, "I4 ters aralık"),
    tc("TC-CRON-EP-11", "a * * * *", I, "I5 harf / geçersiz karakter"),
    tc("TC-CRON-EP-12", "", I, "I6 boş string"),
    tc("TC-CRON-EP-13", "*/0 * * * *", I, "I7 adım sıfır"),
    tc("TC-CRON-EP-14", "1,,2 * * * *", I, "I8 listede boş eleman"),
]

BVA = [
    # Dakika (0-59): alt sınır -1/0/1, üst sınır 58/59/60
    tc("TC-CRON-BVA-01", "-1 * * * *", I, "Dakika alt SD-1 (-1)*"),
    tc("TC-CRON-BVA-02", "0 * * * *", V, "Dakika alt SD (0)"),
    tc("TC-CRON-BVA-22", "1 * * * *", V, "Dakika alt SD+1 (1)"),
    tc("TC-CRON-BVA-23", "58 * * * *", V, "Dakika üst SD-1 (58)"),
    tc("TC-CRON-BVA-03", "59 * * * *", V, "Dakika üst SD (59)"),
    tc("TC-CRON-BVA-04", "60 * * * *", I, "Dakika üst SD+1 (60)"),
    # Saat (0-23)
    tc("TC-CRON-BVA-24", "* -1 * * *", I, "Saat alt SD-1 (-1)*"),
    tc("TC-CRON-BVA-05", "* 0 * * *", V, "Saat alt SD (0)"),
    tc("TC-CRON-BVA-25", "* 1 * * *", V, "Saat alt SD+1 (1)"),
    tc("TC-CRON-BVA-26", "* 22 * * *", V, "Saat üst SD-1 (22)"),
    tc("TC-CRON-BVA-06", "* 23 * * *", V, "Saat üst SD (23)"),
    tc("TC-CRON-BVA-07", "* 24 * * *", I, "Saat üst SD+1 (24)"),
    # Ayın günü (1-31)
    tc("TC-CRON-BVA-08", "* * 0 * *", I, "Gün alt SD-1 (0)"),
    tc("TC-CRON-BVA-09", "* * 1 * *", V, "Gün alt SD (1)"),
    tc("TC-CRON-BVA-27", "* * 2 * *", V, "Gün alt SD+1 (2)"),
    tc("TC-CRON-BVA-28", "* * 30 * *", V, "Gün üst SD-1 (30)"),
    tc("TC-CRON-BVA-10", "* * 31 * *", V, "Gün üst SD (31)"),
    tc("TC-CRON-BVA-11", "* * 32 * *", I, "Gün üst SD+1 (32)"),
    # Ay (1-12)
    tc("TC-CRON-BVA-12", "* * * 0 *", I, "Ay alt SD-1 (0)"),
    tc("TC-CRON-BVA-13", "* * * 1 *", V, "Ay alt SD (1)"),
    tc("TC-CRON-BVA-29", "* * * 2 *", V, "Ay alt SD+1 (2)"),
    tc("TC-CRON-BVA-30", "* * * 11 *", V, "Ay üst SD-1 (11)"),
    tc("TC-CRON-BVA-14", "* * * 12 *", V, "Ay üst SD (12)"),
    tc("TC-CRON-BVA-15", "* * * 13 *", I, "Ay üst SD+1 (13)"),
    # Haftanın günü (0-7)
    tc("TC-CRON-BVA-31", "* * * * -1", I, "Haftanın günü alt SD-1 (-1)*"),
    tc("TC-CRON-BVA-16", "* * * * 0", V, "Haftanın günü alt SD (0)"),
    tc("TC-CRON-BVA-32", "* * * * 1", V, "Haftanın günü alt SD+1 (1)"),
    tc("TC-CRON-BVA-33", "* * * * 6", V, "Haftanın günü üst SD-1 (6)"),
    tc("TC-CRON-BVA-17", "* * * * 7", V, "Haftanın günü üst SD (7)"),
    tc("TC-CRON-BVA-18", "* * * * 8", I, "Haftanın günü üst SD+1 (8)"),
    # Alan sayısı (5)
    tc("TC-CRON-BVA-19", "* * * *", I, "Alan sayısı SD-1 (4)"),
    tc("TC-CRON-BVA-20", "* * * * *", V, "Alan sayısı SD (5)"),
    tc("TC-CRON-BVA-21", "* * * * * *", I, "Alan sayısı SD+1 (6)"),
]
# * '-' aralık operatörü olduğundan "-1" bozuk aralık olarak da yorumlanabilir.


@pytest.mark.parametrize("girdi, parametreler, beklenen", EP + BVA)
def test_cron(dogrula, girdi, parametreler, beklenen):
    dogrula("cron", girdi, parametreler, beklenen)
