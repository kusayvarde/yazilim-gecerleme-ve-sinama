"""validators.ipv4 - çok zor (5 puan). EP + BVA + karar tablosu (DT, bonus)."""

import pytest

from tests.yardimci import I, V, tc

EP = [
    # --- Geçerli sınıflar ---
    tc("TC-IPV4-EP-01", "192.168.1.1", V, "V1 standart 4 oktet"),
    tc("TC-IPV4-EP-02", "10.0.0.0/8", V, "V2 CIDR (cidr=True varsayılan)"),
    tc("TC-IPV4-EP-03", "10.0.0.0/8", V, "V3 strict=True + CIDR var", strict=True),
    tc("TC-IPV4-EP-04", "192.168.0.1", V, "V4 private=True + private", private=True),
    tc("TC-IPV4-EP-05", "8.8.8.8", V, "V5 private=False + public", private=False),
    tc("TC-IPV4-EP-06", "192.168.1.0/24", V, "V6 host_bit=False + host bitleri 0", host_bit=False),
    tc("TC-IPV4-EP-07", "127.0.0.1", V, "V4b private=True + loopback", private=True),
    tc("TC-IPV4-EP-08", "255.255.255.255", V, "V4c private=True + broadcast", private=True),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-IPV4-EP-09", "256.1.1.1", I, "I1 oktet > 255"),
    tc("TC-IPV4-EP-10", "192.168.1", I, "I2 eksik oktet (3)"),
    tc("TC-IPV4-EP-11", "1.2.3.4.5", I, "I3 fazla oktet (5)"),
    tc("TC-IPV4-EP-12", "192.168.a.1", I, "I4 harf içeriyor"),
    tc("TC-IPV4-EP-13", "", I, "I5 boş string"),
    tc("TC-IPV4-EP-14", "-1.2.3.4", I, "I6 negatif sayı"),
    tc("TC-IPV4-EP-15", "01.2.3.4", I, "I7 baştaki sıfır"),
    tc("TC-IPV4-EP-16", "1.2.3.4 ", I, "I8a sonda boşluk"),
    tc("TC-IPV4-EP-17", "1.2.3.#", I, "I8b özel karakter"),
    tc("TC-IPV4-EP-18", "1.2.3.4/64", I, "I9 CIDR öneki > 32"),
    tc("TC-IPV4-EP-19", "1.2.3.4", I, "I10 strict=True ama CIDR yok", strict=True),
    tc("TC-IPV4-EP-20", "10.0.0.0/8", I, "I11 cidr=False ama CIDR var", cidr=False),
    tc("TC-IPV4-EP-21", "192.168.1.1", I, "I12 private=False + private", private=False),
    tc("TC-IPV4-EP-22", "8.8.8.8", I, "I13 private=True + public", private=True),
    tc("TC-IPV4-EP-23", "192.168.1.1/24", I, "I14 host_bit=False + host bitleri set", host_bit=False),
    tc("TC-IPV4-EP-24", "::1", I, "I15 IPv6 adresi"),
    # --- Dokümandaki örnekler ---
    tc("TC-IPV4-EP-25", "123.0.0.7", V, "Doküman örneği (geçerli)"),
    tc("TC-IPV4-EP-26", "1.1.1.1/8", V, "Doküman örneği (geçerli, CIDR)"),
    tc("TC-IPV4-EP-27", "900.80.70.11", I, "Doküman örneği (geçersiz)"),
]

BVA = [
    # Oktet alt sınırı (0)
    tc("TC-IPV4-BVA-01", "-1.0.0.0", I, "Oktet alt SD-1"),
    tc("TC-IPV4-BVA-02", "0.0.0.0", V, "Oktet alt SD"),
    tc("TC-IPV4-BVA-03", "1.0.0.0", V, "Oktet alt SD+1"),
    # Oktet üst sınırı (255) - ilk oktet
    tc("TC-IPV4-BVA-04", "254.1.1.1", V, "Oktet üst SD-1"),
    tc("TC-IPV4-BVA-05", "255.1.1.1", V, "Oktet üst SD"),
    tc("TC-IPV4-BVA-06", "256.1.1.1", I, "Oktet üst SD+1"),
    # Oktet üst sınırı - son oktet (sınır her pozisyonda geçerli mi?)
    tc("TC-IPV4-BVA-19", "1.1.1.254", V, "Son oktet üst SD-1"),
    tc("TC-IPV4-BVA-07", "1.1.1.255", V, "Son oktet üst SD"),
    tc("TC-IPV4-BVA-08", "1.1.1.256", I, "Son oktet üst SD+1"),
    tc("TC-IPV4-BVA-09", "255.255.255.255", V, "Tüm oktetler maks SD (hepsi 255)"),
    # Oktet sayısı (4)
    tc("TC-IPV4-BVA-10", "1.2.3", I, "Oktet sayısı SD-1 (3)"),
    tc("TC-IPV4-BVA-11", "1.2.3.4", V, "Oktet sayısı SD (4)"),
    tc("TC-IPV4-BVA-12", "1.2.3.4.5", I, "Oktet sayısı SD+1 (5)"),
    # CIDR alt sınırı (0)
    tc("TC-IPV4-BVA-13", "1.2.3.4/-1", I, "CIDR alt SD-1"),
    tc("TC-IPV4-BVA-14", "1.2.3.4/0", V, "CIDR alt SD"),
    tc("TC-IPV4-BVA-15", "1.2.3.4/1", V, "CIDR alt SD+1"),
    # CIDR üst sınırı (32)
    tc("TC-IPV4-BVA-16", "1.2.3.4/31", V, "CIDR üst SD-1"),
    tc("TC-IPV4-BVA-17", "1.2.3.4/32", V, "CIDR üst SD"),
    tc("TC-IPV4-BVA-18", "1.2.3.4/33", I, "CIDR üst SD+1"),
]

# Karar tablosu: cidr x strict x (girdide CIDR var mı?)
DT = [
    tc("TC-IPV4-DT-01", "1.2.3.4", V, "R1 cidr=T strict=F CIDR yok", cidr=True, strict=False),
    tc("TC-IPV4-DT-02", "1.2.3.0/24", V, "R2 cidr=T strict=F CIDR var", cidr=True, strict=False),
    tc("TC-IPV4-DT-03", "1.2.3.4", I, "R3 cidr=T strict=T CIDR yok", cidr=True, strict=True),
    tc("TC-IPV4-DT-04", "1.2.3.0/24", V, "R4 cidr=T strict=T CIDR var", cidr=True, strict=True),
    tc("TC-IPV4-DT-05", "1.2.3.4", V, "R5 cidr=F strict=F CIDR yok", cidr=False, strict=False),
    tc("TC-IPV4-DT-06", "1.2.3.0/24", I, "R6 cidr=F strict=F CIDR var", cidr=False, strict=False),
    tc("TC-IPV4-DT-07", "1.2.3.4", I, "R7 cidr=F strict=T CIDR yok (çelişkili)", cidr=False, strict=True,
       bug="BUG-01: cidr=False iken strict=True yok sayılıyor; CIDR'sız adres kabul ediliyor"),
    tc("TC-IPV4-DT-08", "1.2.3.0/24", I, "R8 cidr=F strict=T CIDR var (çelişkili)", cidr=False, strict=True),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", EP + BVA + DT)
def test_ipv4(dogrula, girdi, parametreler, beklenen):
    dogrula("ipv4", girdi, parametreler, beklenen)
