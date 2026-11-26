"""validators.email - çok zor (5 puan). EP + BVA.

Beklentiler docstring ve RFC 5321 / RFC 5322 / RFC 1035'ten türetilmiştir:
yerel kısım en çok 64 karakter (RFC 5321 §4.5.3.1.1), DNS etiketi en çok 63 karakter
(RFC 1035 §2.3.4), adres toplam en çok 254 karakter (RFC 5321 yol sınırı 256 - köşeli
parantezler; RFC 3696 errata 1690). validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc


def _adres(toplam):
    """64 karakterlik yerel kısım + etiketleri 63'ü aşmayan alan adı; toplam uzunluk `toplam`."""
    yerel = "a" * 64
    sabit = 63 + 1 + 63 + 1 + 4  # 'b'*63 . 'c'*63 . <d> .com
    alan = "b" * 63 + "." + "c" * 63 + "." + "d" * (toplam - 65 - sabit) + ".com"
    sonuc = yerel + "@" + alan
    assert len(sonuc) == toplam
    return sonuc


EP = [
    tc("TC-EMAIL-EP-01", "someone@example.com", V, "Doküman örneği (geçerli)"),
    tc("TC-EMAIL-EP-02", "bogus@@", I, "Doküman örneği (geçersiz)"),
    # --- Geçerli sınıflar ---
    tc("TC-EMAIL-EP-03", "ali.veli@ornek.com.tr", V, "V1 noktalı yerel kısım + alt alan adı"),
    tc("TC-EMAIL-EP-04", "user+etiket@example.com", V, "V2 '+' alt adresleme"),
    tc("TC-EMAIL-EP-05", "!#$%&'*+-/=?^_`{|}~@example.com", V, "V3 RFC 5322 atext özel karakterleri"),
    tc("TC-EMAIL-EP-06", '"ali veli"@example.com', V, "V4 tırnaklı yerel kısım (boşluklu)",
       bug="BUG-40: tırnaklı yerel kısım reddediliyor; RFC 5322 §3.4.1 quoted-string'e izin verir"),
    tc("TC-EMAIL-EP-07", "USER@EXAMPLE.COM", V, "V5 büyük harf"),
    tc("TC-EMAIL-EP-08", "user@xn--mnchen-3ya.de", V, "V6 punycode (IDN) alan adı"),
    tc("TC-EMAIL-EP-09", "user@[192.168.0.1]", V, "V7 IPv4 adres-literali (ipv4_address=True)",
       ipv4_address=True),
    tc("TC-EMAIL-EP-10", "user@[IPv6:2001:db8::1]", V, "V8 IPv6 adres-literali (ipv6_address=True)",
       ipv6_address=True,
       bug="BUG-41: RFC 5321 §4.1.3 'IPv6:' etiketli adres-literali reddediliyor"),
    tc("TC-EMAIL-EP-11", "user@localhost", V, "V9 tek etiketli ana makine (simple_host=True)",
       simple_host=True),
    tc("TC-EMAIL-EP-12", "user@example.com.", V, "V10 sondaki nokta (rfc_1034=True)", rfc_1034=True),
    tc("TC-EMAIL-EP-13", "user@_sip._tcp.example.com", V, "V11 SRV adı (rfc_2782=True)", rfc_2782=True),
    # --- Geçersiz sınıflar (her biri tek kural ihlali) ---
    tc("TC-EMAIL-EP-14", "aliornek.com", I, "I1 '@' yok"),
    tc("TC-EMAIL-EP-15", "ali@veli@ornek.com", I, "I2 tırnaksız ikinci '@'"),
    tc("TC-EMAIL-EP-16", "@example.com", I, "I3 boş yerel kısım"),
    tc("TC-EMAIL-EP-17", "user@", I, "I4 boş alan adı"),
    tc("TC-EMAIL-EP-18", ".user@example.com", I, "I5 yerel kısım noktayla başlıyor"),
    tc("TC-EMAIL-EP-19", "user.@example.com", I, "I6 yerel kısım noktayla bitiyor"),
    tc("TC-EMAIL-EP-20", "us..er@example.com", I, "I7 ardışık nokta"),
    tc("TC-EMAIL-EP-21", "us er@example.com", I, "I8 tırnaksız boşluk"),
    tc("TC-EMAIL-EP-22", "user@-example.com", I, "I9 etiket tire ile başlıyor"),
    tc("TC-EMAIL-EP-23", "user@example", I, "I10 TLD yok (simple_host=False)"),
    tc("TC-EMAIL-EP-24", "user@example.com.", I, "I11 sondaki nokta (rfc_1034=False)"),
    tc("TC-EMAIL-EP-25", "user@_sip._tcp.example.com", I, "I12 alt çizgi (rfc_2782=False)"),
    tc("TC-EMAIL-EP-26", "user@[192.168.0.1]", I, "I13 IP literali (ipv4_address=False)"),
    tc("TC-EMAIL-EP-27", "user@example.123", I, "I14 tamamen sayısal TLD"),
    tc("TC-EMAIL-EP-28", "", I, "I15 boş girdi"),
]

BVA = [
    tc("TC-EMAIL-BVA-01", "a" * 63 + "@example.com", V, "Yerel kısım uzunluğu SD-1 (63)"),
    tc("TC-EMAIL-BVA-02", "a" * 64 + "@example.com", V, "Yerel kısım uzunluğu SD (64)"),
    tc("TC-EMAIL-BVA-03", "a" * 65 + "@example.com", I, "Yerel kısım uzunluğu SD+1 (65)"),
    tc("TC-EMAIL-BVA-04", "user@" + "a" * 62 + ".com", V, "Alan adı etiketi SD-1 (62)"),
    tc("TC-EMAIL-BVA-05", "user@" + "a" * 63 + ".com", V, "Alan adı etiketi SD (63)"),
    tc("TC-EMAIL-BVA-06", "user@" + "a" * 64 + ".com", I, "Alan adı etiketi SD+1 (64)"),
    tc("TC-EMAIL-BVA-07", _adres(253), V, "Adres toplam uzunluğu SD-1 (253)"),
    tc("TC-EMAIL-BVA-08", _adres(254), V, "Adres toplam uzunluğu SD (254)"),
    tc("TC-EMAIL-BVA-09", _adres(255), I, "Adres toplam uzunluğu SD+1 (255)",
       bug="BUG-42: 254 karakteri aşan adres kabul ediliyor (319'a kadar); RFC 5321 sınırı 254"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", EP + BVA)
def test_email(dogrula, girdi, parametreler, beklenen):
    dogrula("email", girdi, parametreler, beklenen)
