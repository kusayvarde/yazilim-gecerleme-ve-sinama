"""url için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc


def yalniz_https(sema):
    """Kullanıcı tarafından sağlanan şema sözleşmesi."""
    return sema == "https"


VAKALAR = [
    tc('TC-URL-EP-01', 'http://duck.com', V, 'Doküman örneği (geçerli)'),
    tc('TC-URL-EP-02', 'ftp://foobar.dk', V, 'Doküman örneği (geçerli)'),
    tc('TC-URL-EP-03', 'http://10.0.0.1', V, 'Doküman örneği (geçerli)'),
    tc('TC-URL-EP-04', 'http://example.com/">user@example.com', I, 'Doküman örneği (geçersiz)'),
    tc('TC-URL-EP-05', 'https://example.com/path?q=1#part', V, 'V5 yol sorgu ve parça'),
    tc('TC-URL-EP-06', 'https://user:pass@example.com', V, 'V6 kullanıcı ve parola'),
    tc('TC-URL-EP-07', 'http://[2001:db8::1]/', V, 'V7 IPv6'),
    tc('TC-URL-EP-08', 'https://bücher.de', V, 'V8 IDN'),
    tc('TC-URL-EP-09', '', I, 'I9 boş girdi'),
    tc('TC-URL-EP-10', 'example.com', I, 'I10 şema yok'),
    tc('TC-URL-EP-11', 'http:///path', I, 'I11 ana makine yok'),
    tc('TC-URL-EP-12', 'http://exa mple.com', I, 'I12 ana makinede boşluk'),
    tc('TC-URL-EP-13', 'http://example.com/a b', I, 'I13 yolda boşluk'),
    tc('TC-URL-EP-14', 'http://8.8.8.8', I, 'I14 IPv4 yasak', skip_ipv4_addr=True),
    tc('TC-URL-EP-15', 'http://[2001:db8::1]', I, 'I15 IPv6 yasak', skip_ipv6_addr=True),
    tc('TC-URL-EP-16', 'http://example.com:80', I, 'I16 port yasak', may_have_port=False),
    tc('TC-URL-EP-17', 'http://localhost', V, 'V17 basit ana makine açık', simple_host=True),
    tc('TC-URL-EP-18', 'http://localhost', I, 'I18 basit ana makine kapalı'),
    tc('TC-URL-EP-19', 'http://example.invalidtld', I, 'I19 IANA dışı TLD', consider_tld=True),
    tc('TC-URL-EP-20', 'http://example.com', V, 'V20 IANA TLD', consider_tld=True),
    tc('TC-URL-EP-21', 'http://192.168.1.1', V, 'V21 özel IP gerekli', private=True),
    tc('TC-URL-EP-22', 'http://8.8.8.8', I, 'I22 genel IP özel değil', private=True),
    tc('TC-URL-EP-23', 'http://192.168.1.1', I, 'I23 özel IP genel değil', private=False),
    tc('TC-URL-EP-24', 'http://8.8.8.8', V, 'V24 genel IP gerekli', private=False),
    tc('TC-URL-EP-25', 'http://example.com.', V, 'V25 son nokta izinli', rfc_1034=True),
    tc('TC-URL-EP-26', 'http://example.com.', I, 'I26 son nokta izinsiz'),
    tc('TC-URL-EP-27', 'http://_sip._tcp.example.com', V, 'V27 SRV izinli', rfc_2782=True),
    tc('TC-URL-EP-28', 'http://_sip._tcp.example.com', I, 'I28 SRV izinsiz'),
    tc('TC-URL-EP-29', 'http://example.com/?foo', I, 'I29 katı sorguda eşittir yok', strict_query=True),
    tc('TC-URL-EP-30', 'http://example.com/?foo', V, 'V30 esnek sorguda eşittir yok', strict_query=False),
    tc('TC-URL-BVA-01', 'http://example.com:-1', I, 'Port 0 SD-1 (-1)'),
    tc('TC-URL-BVA-02', 'http://example.com:0', I, 'Port 0 SD (0)'),
    tc('TC-URL-BVA-03', 'http://example.com:1', V, 'Port 0 SD+1 (1)'),
    tc('TC-URL-BVA-04', 'http://example.com:65534', V, 'Port 65535 SD-1 (65534)'),
    tc('TC-URL-BVA-05', 'http://example.com:65535', V, 'Port 65535 SD (65535)'),
    tc('TC-URL-BVA-06', 'http://example.com:65536', I, 'Port 65535 SD+1 (65536)'),
    tc('TC-URL-BVA-07', 'http://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com', V, 'Etiket üst SD-1 (62)'),
    tc('TC-URL-BVA-08', 'http://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com', V, 'Etiket üst SD (63)'),
    tc('TC-URL-BVA-09', 'http://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com', I, 'Etiket üst SD+1 (64)'),
    tc('TC-URL-BVA-10', 'http://example.com:0', I, 'Hizmet portu alt SD-1 (0)'),
    tc('TC-URL-BVA-11', 'http://example.com:1', V, 'Hizmet portu alt SD (1)'),
    tc('TC-URL-BVA-12', 'http://example.com:2', V, 'Hizmet portu alt SD+1 (2)'),
    tc('TC-URL-EP-31', 'https://example.com', V, 'V31 özel şema işlevi kabul eder', validate_scheme=yalniz_https),
    tc('TC-URL-EP-32', 'http://example.com', I, 'I32 özel şema işlevi reddeder', validate_scheme=yalniz_https),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_url(dogrula, girdi, parametreler, beklenen):
    dogrula("url", girdi, parametreler, beklenen)
