"""md5, sha1, sha224, sha256, sha384, sha512 - kolay (1'er puan).

Altısının yapısı aynı, yalnızca uzunluk N değişir. Senaryolar tek tabloda
tanımlanır ve parametrize ile 6 fonksiyona çoğaltılır (test tekrarı azaltıldı).
Her senaryoya yine tabloyla eşleşen bir Test ID verilir: TC-<FONK>-<EP|BVA>-<no>.
"""

import pytest

from tests.yardimci import I, V, tc

UZUNLUK = {"md5": 32, "sha1": 40, "sha224": 56, "sha256": 64, "sha384": 96, "sha512": 128}

# (teknik, sınıf/sınır, girdi üretici, beklenen)
SENARYOLAR = [
    ("EP", "V1 N adet küçük hex", lambda n: "a" * n, V),
    ("EP", "V2 N adet karışık harf hex", lambda n: "aB" * (n // 2), V),
    ("EP", "V3 rakam + harf hex", lambda n: ("0123456789abcdef" * 8)[:n], V),
    ("EP", "I1 hex olmayan karakter", lambda n: "g" + "a" * (n - 1), I),
    ("EP", "I3 0x öneki", lambda n: "0x" + "a" * n, I),
    ("EP", "I4 boşluk içeriyor", lambda n: " " + "a" * n, I),
    ("EP", "I5 boş string", lambda n: "", I),
    ("BVA", "Uzunluk N-1", lambda n: "a" * (n - 1), I),
    ("BVA", "Uzunluk N", lambda n: "a" * n, V),
    ("BVA", "Uzunluk N+1", lambda n: "a" * (n + 1), I),
]

# I2: başka algoritmanın (bir önceki uzunluktaki) geçerli değeri
BASKA_ALGORITMA = {"md5": "sha1", "sha1": "md5", "sha224": "sha256",
                   "sha256": "sha224", "sha384": "sha512", "sha512": "sha384"}

# Dokümandaki geçerli örnekler (boş dizenin gerçek özetleri)
DOKUMAN_ORNEGI = {
    "md5": "d41d8cd98f00b204e9800998ecf8427e",
    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "sha224": "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f",
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "sha384": "cb00753f45a35e8bb5a03d699ac65007272c32ab0eded163"
              "1a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7",
    "sha512": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce"
              "9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af9"
              "27da3e",
}


def _vakalar():
    vakalar = []
    for ad, n in UZUNLUK.items():
        sayac = {"EP": 0, "BVA": 0}
        for teknik, sinif, uret, beklenen in SENARYOLAR:
            sayac[teknik] += 1
            test_id = f"TC-{ad.upper()}-{teknik}-{sayac[teknik]:02d}"
            vakalar.append((ad, tc(test_id, uret(n), beklenen, sinif)))
        diger = BASKA_ALGORITMA[ad]
        ek = [
            ("a" * UZUNLUK[diger], I, f"I2 başka algoritmanın uzunluğu ({diger}, {UZUNLUK[diger]})"),
            (DOKUMAN_ORNEGI[ad], V, "Doküman örneği (geçerli, gerçek özet)"),
            ("900zz11", I, "Doküman örneği (geçersiz)"),
        ]
        for girdi, beklenen, sinif in ek:
            sayac["EP"] += 1
            vakalar.append((ad, tc(f"TC-{ad.upper()}-EP-{sayac['EP']:02d}", girdi, beklenen, sinif)))
    return vakalar


VAKALAR = [
    pytest.param(ad, *p.values, id=p.id, marks=p.marks) for ad, p in _vakalar()
]


@pytest.mark.parametrize("ad, girdi, parametreler, beklenen", VAKALAR)
def test_hash(dogrula, ad, girdi, parametreler, beklenen):
    dogrula(ad, girdi, parametreler, beklenen)
