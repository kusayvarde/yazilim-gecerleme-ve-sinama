"""es_nif için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-ES_NIF-EP-01', '26643189N', V, 'Doküman örneği (geçerli)'),
    tc('TC-ES_NIF-EP-02', '26643189X', I, 'Doküman örneği (geçersiz)'),
    tc('TC-ES_NIF-EP-03', '', I, 'I3 boş girdi'),
    tc('TC-ES_NIF-EP-04', '2664 189N', I, 'I4 gövde içinde boşluk'),
    tc('TC-ES_NIF-EP-05', '2664#189N', I, 'I5 gövde içinde özel karakter'),
    tc('TC-ES_NIF-EP-06', '12345678Z', V, 'V6 bağımsız mod-23 üretimi'),
    tc('TC-ES_NIF-EP-07', '00000001R', V, 'V7 bağımsız mod-23 üretimi'),
    tc('TC-ES_NIF-EP-08', '99999999R', V, 'V8 bağımsız mod-23 üretimi'),
    tc('TC-ES_NIF-EP-09', '12345678A', I, 'I9 yanlış kontrol harfi'),
    tc('TC-ES_NIF-EP-10', 'A2345678Z', I, 'I10 gövde harf içeriyor'),
    tc('TC-ES_NIF-BVA-01', '26643189', I, 'Biçim uzunluğu SD-1 (8)'),
    tc('TC-ES_NIF-BVA-02', '26643189N', V, 'Biçim uzunluğu SD (9)'),
    tc('TC-ES_NIF-BVA-03', '26643189N0', I, 'Biçim uzunluğu SD+1 (10)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_es_nif(dogrula, girdi, parametreler, beklenen):
    dogrula("es_nif", girdi, parametreler, beklenen)
