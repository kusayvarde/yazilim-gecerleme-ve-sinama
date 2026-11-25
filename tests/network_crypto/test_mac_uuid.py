"""mac_address ve uuid - kolay (1'er puan). EP + BVA."""

import uuid

import pytest

from tests.yardimci import I, V, tc

UUID_STR = "2bc1c94f-0deb-43e9-92a1-4775189ec9f8"   # doküman örneği

# Bulgular (docs/tablolar/T6_network_crypto.csv)
BUG_02 = "BUG-02: doküman 'UUID-v4' diyor ama v4 olmayan UUID'ler (v1, nil) kabul ediliyor"
BUG_03 = "BUG-03: 8-4-4-4-12 biçimi zorlanmıyor; tiresiz, {...} ve urn:uuid: biçimleri kabul ediliyor"
BUG_04 = "BUG-04: tire konumu denetlenmiyor; tireler herhangi bir yerde olabilir"

MAC = [
    tc("TC-MAC-EP-01", "01:23:45:67:ab:CD", V, "V1 ':' ayırıcı"),
    tc("TC-MAC-EP-02", "01-23-45-67-AB-CD", V, "V2 '-' ayırıcı"),
    tc("TC-MAC-EP-03", "01:23:45:67:ab:cd", V, "V3 tümü küçük harf"),
    tc("TC-MAC-EP-04", "01:23-45:67:ab:CD", I, "I1 karışık ayırıcı"),
    tc("TC-MAC-EP-05", "GG:23:45:67:ab:CD", I, "I2 hex olmayan"),
    tc("TC-MAC-EP-06", "0123456789AB", I, "I3 ayırıcısız"),
    tc("TC-MAC-EP-07", "0123.4567.89ab", I, "I4 Cisco formatı"),
    tc("TC-MAC-EP-08", "01.23.45.67.ab.cd", I, "I5 '.' ayırıcı"),
    tc("TC-MAC-EP-09", "", I, "I6 boş string"),
    tc("TC-MAC-EP-10", "00:00:00:00:00", I, "Doküman örneği (geçersiz, 5 grup)"),
    tc("TC-MAC-BVA-01", "01:23:45:67:89", I, "Grup sayısı SD-1 (5)"),
    tc("TC-MAC-BVA-02", "01:23:45:67:89:ab", V, "Grup sayısı SD (6)"),
    tc("TC-MAC-BVA-03", "01:23:45:67:89:ab:cd", I, "Grup sayısı SD+1 (7)"),
    tc("TC-MAC-BVA-04", "1:23:45:67:89:ab", I, "Grup uzunluğu SD-1 (1 hane)"),
    tc("TC-MAC-BVA-05", "01:23:45:67:89:AB", V, "Grup uzunluğu SD (2 hane)"),
    tc("TC-MAC-BVA-06", "001:23:45:67:89:ab", I, "Grup uzunluğu SD+1 (3 hane)"),
]

UUID = [
    tc("TC-UUID-EP-01", UUID_STR, V, "V1 standart string"),
    tc("TC-UUID-EP-02", UUID_STR.upper(), V, "V2 büyük harf"),
    tc("TC-UUID-EP-03", uuid.uuid4(), V, "V3 uuid.UUID nesnesi (uuid4)"),
    tc("TC-UUID-EP-04", uuid.UUID(UUID_STR), V, "V4 uuid.UUID nesnesi (sabit)"),
    tc("TC-UUID-EP-05", UUID_STR.replace("-", " ", 1), I, "I1 tire yerine boşluk"),
    tc("TC-UUID-EP-06", "z" + UUID_STR[1:], I, "I2 hex olmayan"),
    tc("TC-UUID-EP-07", "", I, "I3 boş string"),
    tc("TC-UUID-EP-08", UUID_STR.replace("-", ""), I, "I4 tiresiz 32 hex", bug=BUG_03),
    tc("TC-UUID-EP-09", "{" + UUID_STR + "}", I, "I5 süslü parantezli", bug=BUG_03),
    tc("TC-UUID-EP-10", "urn:uuid:" + UUID_STR, I, "I6 urn:uuid: önekli", bug=BUG_03),
    tc("TC-UUID-EP-11", "2bc1c94f0-deb-43e9-92a1-4775189ec9f8", I, "I7 tire konumu yanlış", bug=BUG_04),
    tc("TC-UUID-EP-12", "c01e6940-da3f-11f1-8a43-d843ae7f0e48", I, "I8 UUID v1 (doküman v4 diyor)", bug=BUG_02),
    tc("TC-UUID-EP-13", "00000000-0000-0000-0000-000000000000", I, "I9 nil UUID (sürüm 0)", bug=BUG_02),
    tc("TC-UUID-EP-14", "2-b-c-1c94f0deb43e992a14775189ec9f8", I, "I10 tireler rastgele konumda", bug=BUG_04),
    tc("TC-UUID-BVA-01", UUID_STR[:-1], I, "Uzunluk SD-1 (35)"),
    tc("TC-UUID-BVA-02", UUID_STR, V, "Uzunluk SD (36)"),
    tc("TC-UUID-BVA-03", UUID_STR + "a", I, "Uzunluk SD+1 (37)"),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", MAC)
def test_mac_address(dogrula, girdi, parametreler, beklenen):
    dogrula("mac_address", girdi, parametreler, beklenen)


@pytest.mark.parametrize("girdi, parametreler, beklenen", UUID)
def test_uuid(dogrula, girdi, parametreler, beklenen):
    dogrula("uuid", girdi, parametreler, beklenen)
