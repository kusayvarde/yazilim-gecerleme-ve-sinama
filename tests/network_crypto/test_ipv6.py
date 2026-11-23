"""validators.ipv6 - çok zor (5 puan). EP + BVA. (ipv6'da private parametresi yok.)"""

import pytest

from tests.yardimci import I, V, tc

EP = [
    # --- Geçerli sınıflar ---
    tc("TC-IPV6-EP-01", "2001:0db8:0000:0000:0000:ff00:0042:8329", V, "V1 tam 8 grup"),
    tc("TC-IPV6-EP-02", "2001:db8::1", V, "V2 :: kısaltması"),
    tc("TC-IPV6-EP-03", "::1", V, "V3 loopback"),
    tc("TC-IPV6-EP-04", "::ffff:192.0.2.128", V, "V4 IPv4-mapped"),
    tc("TC-IPV6-EP-05", "2001:db8::/32", V, "V5 CIDR"),
    tc("TC-IPV6-EP-06", "2001:DB8::1", V, "V6 büyük harf hex"),
    tc("TC-IPV6-EP-07", "::", V, "V7 belirtilmemiş adres (tümü sıfır)"),
    tc("TC-IPV6-EP-08", "2001:db8::/32", V, "V8 strict=True + CIDR var", strict=True),
    tc("TC-IPV6-EP-09", "2001:db8::/32", V, "V9 host_bit=False + host bitleri 0", host_bit=False),
    # --- Geçersiz sınıflar ---
    tc("TC-IPV6-EP-10", "1:2:3:4:5:6:7:8:9", I, "I1 9 grup"),
    tc("TC-IPV6-EP-11", "2001:db8::12345", I, "I2 grupta 5 hex"),
    tc("TC-IPV6-EP-12", "2001:db8::g", I, "I3 hex olmayan karakter"),
    tc("TC-IPV6-EP-13", "2001::db8::1", I, "I4 iki kez ::"),
    tc("TC-IPV6-EP-14", "::1/200", I, "I5 önek > 128"),
    tc("TC-IPV6-EP-15", "1.2.3.4", I, "I6 IPv4 adresi"),
    tc("TC-IPV6-EP-16", "", I, "I7 boş string"),
    tc("TC-IPV6-EP-17", "::1", I, "I8 strict=True ama CIDR yok", strict=True),
    tc("TC-IPV6-EP-18", "2001:db8::1/32", I, "I9 host_bit=False + host bitleri set", host_bit=False),
    tc("TC-IPV6-EP-19", "2001:db8::/32", I, "I10 cidr=False ama CIDR var", cidr=False),
    tc("TC-IPV6-EP-20", ":::1", I, "I11 üç iki nokta (:::)"),
    tc("TC-IPV6-EP-21", "2001:db8::1 ", I, "I12 sonda boşluk"),
    # --- Dokümandaki örnekler (::ffff:192.0.2.128 zaten EP-04) ---
    tc("TC-IPV6-EP-22", "::1/128", V, "Doküman örneği (geçerli, CIDR)"),
    tc("TC-IPV6-EP-23", "abc.0.0.1", I, "Doküman örneği (geçersiz)"),
]

BVA = [
    # Grup sayısı (8, :: olmadan)
    tc("TC-IPV6-BVA-01", "1:2:3:4:5:6:7", I, "Grup sayısı SD-1 (7)"),
    tc("TC-IPV6-BVA-02", "1:2:3:4:5:6:7:8", V, "Grup sayısı SD (8)"),
    tc("TC-IPV6-BVA-03", "1:2:3:4:5:6:7:8:9", I, "Grup sayısı SD+1 (9)"),
    # :: ile açık grup sayısı (:: en az bir sıfır grubu temsil eder -> en fazla 7 açık grup)
    tc("TC-IPV6-BVA-17", "1::3:4:5:6:7", V, ":: ile açık grup sayısı SD-1 (6)"),
    tc("TC-IPV6-BVA-04", "1::2:3:4:5:6:7", V, ":: ile açık grup sayısı SD (7, :: = 1 grup)"),
    tc("TC-IPV6-BVA-05", "1:2:3:4:5:6:7:8::", I, ":: ile açık grup sayısı SD+1 (8, :: = 0 grup)"),
    # Grup uzunluğu (4 hex)
    tc("TC-IPV6-BVA-06", "::fff", V, "Grup uzunluğu SD-1 (3)"),
    tc("TC-IPV6-BVA-07", "::ffff", V, "Grup uzunluğu SD (4)"),
    tc("TC-IPV6-BVA-08", "::fffff", I, "Grup uzunluğu SD+1 (5)"),
    # CIDR alt sınırı (0)
    tc("TC-IPV6-BVA-09", "::1/-1", I, "CIDR alt SD-1"),
    tc("TC-IPV6-BVA-10", "::1/0", V, "CIDR alt SD"),
    tc("TC-IPV6-BVA-11", "::1/1", V, "CIDR alt SD+1"),
    # CIDR üst sınırı (128)
    tc("TC-IPV6-BVA-12", "::1/127", V, "CIDR üst SD-1"),
    tc("TC-IPV6-BVA-13", "::1/128", V, "CIDR üst SD"),
    tc("TC-IPV6-BVA-14", "::1/129", I, "CIDR üst SD+1"),
    # Hex karakter sınırı (f geçerli son harf, g ilk geçersiz)
    tc("TC-IPV6-BVA-18", "::e", V, "Hex harf sınırı SD-1 ('e')"),
    tc("TC-IPV6-BVA-15", "::f", V, "Hex harf sınırı SD ('f', son hex harfi)"),
    tc("TC-IPV6-BVA-16", "::g", I, "Hex harf sınırı SD+1 ('g')"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", EP + BVA)
def test_ipv6(dogrula, girdi, parametreler, beklenen):
    dogrula("ipv6", girdi, parametreler, beklenen)
