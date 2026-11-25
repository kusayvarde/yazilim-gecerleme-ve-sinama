"""es_nie için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-ES_NIE-EP-01', 'X0095892M', V, 'Doküman örneği (geçerli)'),
    tc('TC-ES_NIE-EP-02', 'X0095892X', I, 'Doküman örneği (geçersiz)'),
    tc('TC-ES_NIE-EP-03', '', I, 'I3 boş girdi'),
    tc('TC-ES_NIE-EP-04', 'X009 892M', I, 'I4 gövde içinde boşluk'),
    tc('TC-ES_NIE-EP-05', 'X009#892M', I, 'I5 gövde içinde özel karakter'),
    tc('TC-ES_NIE-EP-06', 'X1234567L', V, 'V6 X öneki ve mod-23'),
    tc('TC-ES_NIE-EP-07', 'Y1234567X', V, 'V7 Y öneki ve mod-23'),
    tc('TC-ES_NIE-EP-08', 'Z1234567R', V, 'V8 Z öneki ve mod-23'),
    tc('TC-ES_NIE-EP-09', 'W1234567L', I, 'I9 izin verilmeyen başlangıç harfi'),
    tc('TC-ES_NIE-EP-10', 'X1234567A', I, 'I10 yanlış kontrol harfi'),
    tc('TC-ES_NIE-BVA-01', 'X0095892', I, 'Biçim uzunluğu SD-1 (8)'),
    tc('TC-ES_NIE-BVA-02', 'X0095892M', V, 'Biçim uzunluğu SD (9)'),
    tc('TC-ES_NIE-BVA-03', 'X0095892M0', I, 'Biçim uzunluğu SD+1 (10)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_es_nie(dogrula, girdi, parametreler, beklenen):
    dogrula("es_nie", girdi, parametreler, beklenen)
