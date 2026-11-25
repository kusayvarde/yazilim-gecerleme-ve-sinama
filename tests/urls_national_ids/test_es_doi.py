"""es_doi için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-ES_DOI-EP-01', 'X0095892M', V, 'Doküman örneği (geçerli)'),
    tc('TC-ES_DOI-EP-02', 'X0095892X', I, 'Doküman örneği (geçersiz)'),
    tc('TC-ES_DOI-EP-03', '', I, 'I3 boş girdi'),
    tc('TC-ES_DOI-EP-04', 'X009 892M', I, 'I4 gövde içinde boşluk'),
    tc('TC-ES_DOI-EP-05', 'X009#892M', I, 'I5 gövde içinde özel karakter'),
    tc('TC-ES_DOI-EP-06', '12345678Z', V, 'V6 NIF türü birleşik doğrulayıcıda kabul edilir'),
    tc('TC-ES_DOI-EP-07', 'Y1234567X', V, 'V7 NIE türü birleşik doğrulayıcıda kabul edilir'),
    tc('TC-ES_DOI-EP-08', 'B25162520', V, 'V8 CIF türü birleşik doğrulayıcıda kabul edilir'),
    tc('TC-ES_DOI-EP-09', '10.1000/xyz123', I, 'I9 bibliyografik DOI İspanyol kimliği değildir'),
    tc('TC-ES_DOI-EP-10', '12345678A', I, 'I10 NIF türünde yanlış kontrol harfi'),
    tc('TC-ES_DOI-BVA-01', 'X0095892', I, 'Biçim uzunluğu SD-1 (8)'),
    tc('TC-ES_DOI-BVA-02', 'X0095892M', V, 'Biçim uzunluğu SD (9)'),
    tc('TC-ES_DOI-BVA-03', 'X0095892M0', I, 'Biçim uzunluğu SD+1 (10)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_es_doi(dogrula, girdi, parametreler, beklenen):
    dogrula("es_doi", girdi, parametreler, beklenen)
