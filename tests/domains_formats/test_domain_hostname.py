"""validators.domain ve validators.hostname - çok zor (5'er puan). EP + BVA + karar tablosu (DT, bonus).

Beklentiler yalnızca dokümandan (docstring) ve standartlardan türetilmiştir:
RFC 1034/1035 (etiket <= 63, toplam <= 253 karakter, etiket tire ile başlayıp bitmez),
RFC 1123 (etiket rakamla başlayabilir), RFC 3696 §2 (TLD tamamen sayısal olamaz),
RFC 2782 (SRV adları alt çizgi içerir), RFC 4291 (IPv6), TCP/UDP port aralığı 0-65535.
"""

import pytest

from tests.yardimci import I, V, tc


def _alan_adi(toplam: int) -> str:
    """Tam `toplam` karakterlik alan adı: 3 adet 63'lük etiket + son etiket (TLD)."""
    son = toplam - 192
    assert 1 <= son <= 63
    return ".".join(["a" * 63] * 3 + ["a" * son])


# =============================================================== domain
DOMAIN_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-DOMAIN-EP-01", "example.com", V, "V1 standart alan adı"),
    tc("TC-DOMAIN-EP-02", "sub.example.com", V, "V2 alt alan adı"),
    tc("TC-DOMAIN-EP-03", "my-site.example.com", V, "V3 etiket ortasında tire"),
    tc("TC-DOMAIN-EP-04", "123.example.com", V, "V4 rakamla başlayan etiket (RFC 1123)"),
    tc("TC-DOMAIN-EP-05", "EXAMPLE.COM", V, "V5 büyük harf"),
    tc("TC-DOMAIN-EP-06", "example.museum", V, "V6 uzun TLD"),
    tc("TC-DOMAIN-EP-07", "example.com", V, "V7 consider_tld=True + IANA TLD", consider_tld=True),
    tc("TC-DOMAIN-EP-08", "example.com.", V, "V8 rfc_1034=True + sondaki nokta", rfc_1034=True),
    tc("TC-DOMAIN-EP-09", "_sip._tcp.example.com", V, "V9 rfc_2782=True + alt çizgi", rfc_2782=True),
    tc("TC-DOMAIN-EP-10", "bücher.example", V, "V10 Unicode IDN (IDNA)"),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-DOMAIN-EP-11", "", I, "I1 boş string"),
    tc("TC-DOMAIN-EP-12", "localhost", I, "I2 tek etiket (TLD yok)"),
    tc("TC-DOMAIN-EP-13", "-example.com", I, "I3 etiket tire ile başlıyor"),
    tc("TC-DOMAIN-EP-14", "example-.com", I, "I4 etiket tire ile bitiyor"),
    tc("TC-DOMAIN-EP-15", "exa_mple.com", I, "I5 alt çizgi (rfc_2782=False)"),
    tc("TC-DOMAIN-EP-16", "exa mple.com", I, "I6 boşluk içeriyor"),
    tc("TC-DOMAIN-EP-17", "example.com.", I, "I7 sondaki nokta (rfc_1034=False)"),
    tc("TC-DOMAIN-EP-18", "example..com", I, "I8 boş etiket (çift nokta)"),
    tc("TC-DOMAIN-EP-19", ".example.com", I, "I9 baştaki nokta"),
    tc("TC-DOMAIN-EP-20", "http://example.com", I, "I10 şema içeriyor"),
    tc("TC-DOMAIN-EP-21", "example.com:80", I, "I11 port içeriyor"),
    tc("TC-DOMAIN-EP-22", "example.invalidtld", I, "I12 IANA'da olmayan TLD (consider_tld=True)",
       consider_tld=True),
    tc("TC-DOMAIN-EP-23", "example.123", I, "I13 tamamen sayısal TLD (RFC 3696)"),
    tc("TC-DOMAIN-EP-24", "exa$mple.com", I, "I14 özel karakter"),
    tc("TC-DOMAIN-EP-25", "_sip._tcp.example.com", I, "I15 SRV adı (rfc_2782=False)"),
    # --- Dokümandaki örnekler ---
    tc("TC-DOMAIN-EP-26", "example.com", V, "Doküman örneği (geçerli)"),
    tc("TC-DOMAIN-EP-27", "example.com/", I, "Doküman örneği (geçersiz)"),
    tc("TC-DOMAIN-EP-28", "xn----gtbspbbmkef.xn--p1ai", V, "Doküman örneği (geçerli, IDN)"),
]

DOMAIN_BVA = [
    # Etiket uzunluğu üst sınırı (63) - RFC 1035
    tc("TC-DOMAIN-BVA-01", "a" * 62 + ".com", V, "Etiket uzunluğu üst SD-1 (62)"),
    tc("TC-DOMAIN-BVA-02", "a" * 63 + ".com", V, "Etiket uzunluğu üst SD (63)"),
    tc("TC-DOMAIN-BVA-03", "a" * 64 + ".com", I, "Etiket uzunluğu üst SD+1 (64)"),
    # Etiket uzunluğu alt sınırı (1)
    tc("TC-DOMAIN-BVA-04", ".com", I, "Etiket uzunluğu alt SD-1 (0)"),
    tc("TC-DOMAIN-BVA-05", "a.com", V, "Etiket uzunluğu alt SD (1)"),
    tc("TC-DOMAIN-BVA-06", "ab.com", V, "Etiket uzunluğu alt SD+1 (2)"),
    # Toplam uzunluk üst sınırı (253) - RFC 1035
    tc("TC-DOMAIN-BVA-07", _alan_adi(252), V, "Toplam uzunluk üst SD-1 (252)"),
    tc("TC-DOMAIN-BVA-08", _alan_adi(253), V, "Toplam uzunluk üst SD (253)"),
    tc("TC-DOMAIN-BVA-09", _alan_adi(254), I, "Toplam uzunluk üst SD+1 (254)"),
]

# Karar tablosu: rfc_1034 x (sondaki nokta var mı?)
DOMAIN_DT = [
    tc("TC-DOMAIN-DT-01", "example.com", V, "R1 rfc_1034=F nokta yok", rfc_1034=False),
    tc("TC-DOMAIN-DT-02", "example.com.", I, "R2 rfc_1034=F nokta var", rfc_1034=False),
    tc("TC-DOMAIN-DT-03", "example.com", V, "R3 rfc_1034=T nokta yok", rfc_1034=True),
    tc("TC-DOMAIN-DT-04", "example.com.", V, "R4 rfc_1034=T nokta var", rfc_1034=True),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", DOMAIN_EP + DOMAIN_BVA + DOMAIN_DT)
def test_domain(dogrula, girdi, parametreler, beklenen):
    dogrula("domain", girdi, parametreler, beklenen)


# =============================================================== hostname
HOSTNAME_EP = [
    # --- Geçerli sınıflar ---
    tc("TC-HOSTNAME-EP-01", "example.com", V, "V1 standart FQDN"),
    tc("TC-HOSTNAME-EP-02", "sub.example.com:8080", V, "V2 FQDN + port"),
    tc("TC-HOSTNAME-EP-03", "[2001:db8::1]", V, "V3 köşeli parantezli IPv6, portsuz",
       bug="BUG-21: köşeli IPv6 port olmadan reddediliyor ('[::1]' I), port ile kabul ediliyor ('[::1]:22' V)"),
    tc("TC-HOSTNAME-EP-04", "2001:db8::1", V, "V4 köşelisiz IPv6"),
    tc("TC-HOSTNAME-EP-05", "example.com", V, "V5 consider_tld=True + IANA TLD", consider_tld=True),
    tc("TC-HOSTNAME-EP-06", "192.168.1.10", V, "V6 private=True + özel IPv4", private=True),
    tc("TC-HOSTNAME-EP-07", "8.8.8.8", V, "V7 private=False + genel IPv4", private=False),
    tc("TC-HOSTNAME-EP-08", "example.com.", V, "V8 rfc_1034=True + sondaki nokta", rfc_1034=True),
    tc("TC-HOSTNAME-EP-09", "_sip._tcp.example.com", V, "V9 rfc_2782=True + alt çizgi", rfc_2782=True),
    # --- Geçersiz sınıflar (her biri ayrı test) ---
    tc("TC-HOSTNAME-EP-10", "", I, "I1 boş string"),
    tc("TC-HOSTNAME-EP-11", "example.com:65536", I, "I2 port > 65535"),
    tc("TC-HOSTNAME-EP-12", "example.com:abc", I, "I3 port sayı değil"),
    tc("TC-HOSTNAME-EP-13", "example.com:", I, "I4 boş port"),
    tc("TC-HOSTNAME-EP-14", "-example.com", I, "I5 etiket tire ile başlıyor"),
    tc("TC-HOSTNAME-EP-15", "exa mple.com", I, "I6 boşluk içeriyor"),
    tc("TC-HOSTNAME-EP-16", "http://example.com", I, "I7 şema içeriyor"),
    tc("TC-HOSTNAME-EP-17", "example.com/path", I, "I8 yol içeriyor"),
    tc("TC-HOSTNAME-EP-18", "999.1.1.1", I, "I9 geçersiz IPv4 (oktet > 255)"),
    tc("TC-HOSTNAME-EP-19", "[::1", I, "I10 kapanmayan köşeli parantez"),
    tc("TC-HOSTNAME-EP-20", "example.com:80", I, "I11 may_have_port=False + port var", may_have_port=False),
    tc("TC-HOSTNAME-EP-21", "12.12.12.12", I, "I12 skip_ipv4_addr=True + IPv4", skip_ipv4_addr=True),
    tc("TC-HOSTNAME-EP-22", "[::1]:22", I, "I13 skip_ipv6_addr=True + IPv6", skip_ipv6_addr=True),
    tc("TC-HOSTNAME-EP-23", "this-pc", I, "I14 maybe_simple=False + tek etiket", maybe_simple=False),
    tc("TC-HOSTNAME-EP-24", "8.8.8.8", I, "I15 private=True + genel IPv4", private=True),
    tc("TC-HOSTNAME-EP-25", "192.168.1.10", I, "I16 private=False + özel IPv4", private=False),
    tc("TC-HOSTNAME-EP-26", "example.invalidtld", I, "I17 IANA'da olmayan TLD (consider_tld=True)",
       consider_tld=True),
    tc("TC-HOSTNAME-EP-27", "example.com.", I, "I18 sondaki nokta (rfc_1034=False)"),
    # --- Dokümandaki örnekler ---
    tc("TC-HOSTNAME-EP-28", "ubuntu-pc:443", V, "Doküman örneği (geçerli)"),
    tc("TC-HOSTNAME-EP-29", "this-pc", V, "Doküman örneği (geçerli, tek etiket)"),
    tc("TC-HOSTNAME-EP-30", "xn----gtbspbbmkef.xn--p1ai:65535", V, "Doküman örneği (geçerli, IDN + port)"),
    tc("TC-HOSTNAME-EP-31", "_example.com", I, "Doküman örneği (geçersiz)"),
    tc("TC-HOSTNAME-EP-32", "123.5.77.88:31000", V, "Doküman örneği (geçerli, IPv4 + port)"),
    tc("TC-HOSTNAME-EP-33", "12.12.12.12", V, "Doküman örneği (geçerli, IPv4)"),
    tc("TC-HOSTNAME-EP-34", "[::1]:22", V, "Doküman örneği (geçerli, IPv6 + port)"),
    tc("TC-HOSTNAME-EP-35", "dead:beef:0:0:0:0000:42:1", V, "Doküman örneği (geçerli, IPv6)"),
    tc("TC-HOSTNAME-EP-36", "[0:0:0:0:0:ffff:1.2.3.4]:-65538", I, "Doküman örneği (geçersiz, negatif port)"),
    tc("TC-HOSTNAME-EP-37", "[0:&:b:c:@:e:f::]:9999", I, "Doküman örneği (geçersiz, IPv6)"),
]

HOSTNAME_BVA = [
    # Port üst sınırı (65535)
    tc("TC-HOSTNAME-BVA-01", "example.com:65534", V, "Port üst SD-1 (65534)"),
    tc("TC-HOSTNAME-BVA-02", "example.com:65535", V, "Port üst SD (65535)"),
    tc("TC-HOSTNAME-BVA-03", "example.com:65536", I, "Port üst SD+1 (65536)"),
    # Port alt sınırı (1): port 0 IANA'da ayrılmıştır (RFC 6335), doküman aralığı tanımlamaz
    tc("TC-HOSTNAME-BVA-04", "example.com:0", I, "Port alt SD-1 (0)"),
    tc("TC-HOSTNAME-BVA-05", "example.com:1", V, "Port alt SD (1)"),
    tc("TC-HOSTNAME-BVA-06", "example.com:2", V, "Port alt SD+1 (2)"),
    # Etiket uzunluğu üst sınırı (63) - RFC 1035 (tek etiketli ad)
    tc("TC-HOSTNAME-BVA-07", "a" * 62, V, "Etiket uzunluğu üst SD-1 (62)",
       bug="BUG-20: tek etiketli hostname en çok 61 karakter kabul ediliyor; RFC 1035 sınırı 63"),
    tc("TC-HOSTNAME-BVA-08", "a" * 63, V, "Etiket uzunluğu üst SD (63)",
       bug="BUG-20: tek etiketli hostname en çok 61 karakter kabul ediliyor; RFC 1035 sınırı 63"),
    tc("TC-HOSTNAME-BVA-09", "a" * 64, I, "Etiket uzunluğu üst SD+1 (64)"),
    # Toplam uzunluk üst sınırı (253)
    tc("TC-HOSTNAME-BVA-10", _alan_adi(252), V, "Toplam uzunluk üst SD-1 (252)"),
    tc("TC-HOSTNAME-BVA-11", _alan_adi(253), V, "Toplam uzunluk üst SD (253)"),
    tc("TC-HOSTNAME-BVA-12", _alan_adi(254), I, "Toplam uzunluk üst SD+1 (254)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", HOSTNAME_EP + HOSTNAME_BVA)
def test_hostname(dogrula, girdi, parametreler, beklenen):
    dogrula("hostname", girdi, parametreler, beklenen)
