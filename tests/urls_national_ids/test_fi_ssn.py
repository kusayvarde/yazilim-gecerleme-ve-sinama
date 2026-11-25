"""fi_ssn için kara-kutu EP/BVA testleri; MMHDJ.

Beklentiler docstring ve raporda listelenen standartlardan türetilmiştir.
validators kaynak kodu kullanılmamıştır.
"""

import pytest

from tests.yardimci import I, V, tc

VAKALAR = [
    tc('TC-FI_SSN-EP-01', '010101-0101', V, 'Doküman örneği (geçerli)'),
    tc('TC-FI_SSN-EP-02', '101010-0102', I, 'Doküman örneği (geçersiz)'),
    tc('TC-FI_SSN-EP-03', '290200A010M', V, 'V3 artık yıl'),
    tc('TC-FI_SSN-EP-04', '010101+0101', V, 'V4 1800 yüzyılı'),
    tc('TC-FI_SSN-EP-05', '010101A0101', V, 'V5 2000 yüzyılı'),
    tc('TC-FI_SSN-EP-06', '310401-010T', I, 'I6 Nisan 31 olamaz', bug='BUG-60: Takvimde olmayan günler doğru kontrol karakteriyle kabul ediliyor. Vero belgesi ilk altı haneyi doğum tarihi olarak tanımlar. datetime.date ile 31 Nisan ve artık olmayan yıldaki 29 Şubat bağımsız doğrulanmıştır. İç neden kaynak kodu okunmadığı için bilinmiyor.'),
    tc('TC-FI_SSN-EP-07', '290201-010W', I, 'I7 artık olmayan yılda Şubat 29', bug='BUG-60: Takvimde olmayan günler doğru kontrol karakteriyle kabul ediliyor. Vero belgesi ilk altı haneyi doğum tarihi olarak tanımlar. datetime.date ile 31 Nisan ve artık olmayan yıldaki 29 Şubat bağımsız doğrulanmıştır. İç neden kaynak kodu okunmadığı için bilinmiyor.'),
    tc('TC-FI_SSN-EP-08', '', I, 'I8 boş girdi'),
    tc('TC-FI_SSN-EP-09', '010101-0102', I, 'I9 yanlış mod-31 karakteri'),
    tc('TC-FI_SSN-EP-10', '010101?0101', I, 'I10 tanımsız yüzyıl karakteri'),
    tc('TC-FI_SSN-EP-11', '010101B0101', V, 'V11 2023 sonrası yüzyıl karakteri B'),
    tc('TC-FI_SSN-EP-12', '010101Y0101', V, 'V12 2023 sonrası yüzyıl karakteri Y'),
    tc('TC-FI_SSN-BVA-01', '010101-010', I, 'Biçim uzunluğu SD-1 (10)'),
    tc('TC-FI_SSN-BVA-02', '010101-0101', V, 'Biçim uzunluğu SD (11)'),
    tc('TC-FI_SSN-BVA-03', '010101-01010', I, 'Biçim uzunluğu SD+1 (12)'),
    tc('TC-FI_SSN-BVA-04', '010101-899P', V, 'Geçici seri 900 SD-1 (899)', allow_temporal_ssn=False),
    tc('TC-FI_SSN-BVA-05', '010101-900R', I, 'Geçici seri 900 SD (900)', allow_temporal_ssn=False),
    tc('TC-FI_SSN-BVA-06', '010101-901S', I, 'Geçici seri 900 SD+1 (901)', allow_temporal_ssn=False),
    tc('TC-FI_SSN-BVA-07', '010101-998W', I, 'Geçici seri 999 SD-1 (998)', allow_temporal_ssn=False),
    tc('TC-FI_SSN-BVA-08', '010101-999X', I, 'Geçici seri 999 SD (999)', allow_temporal_ssn=False),
    tc('TC-FI_SSN-BVA-09', '010101-1000B', I, 'Geçici seri 999 SD+1 (1000)', allow_temporal_ssn=False),
    tc('TC-FI_SSN-EP-13', '010101-900R', V, 'V13 geçici seri 900 varsayılan'),
    tc('TC-FI_SSN-EP-14', '010101-999X', V, 'V14 geçici seri 999 açık True', allow_temporal_ssn=True),
    tc('TC-FI_SSN-BVA-10', '000101-010C', I, 'Gün 1 SD-1 (0)'),
    tc('TC-FI_SSN-BVA-11', '010101-0101', V, 'Gün 1 SD (1)'),
    tc('TC-FI_SSN-BVA-12', '020101-010N', V, 'Gün 1 SD+1 (2)'),
    tc('TC-FI_SSN-BVA-13', '300101-010R', V, 'Gün 31 SD-1 (30)'),
    tc('TC-FI_SSN-BVA-14', '310101-010C', V, 'Gün 31 SD (31)'),
    tc('TC-FI_SSN-BVA-15', '320101-0101', I, 'Gün 31 SD+1 (32)'),
    tc('TC-FI_SSN-BVA-16', '010001-0107', I, 'Ay 1 SD-1 (0)'),
    tc('TC-FI_SSN-BVA-17', '010101-0101', V, 'Ay 1 SD (1)'),
    tc('TC-FI_SSN-BVA-18', '010201-010U', V, 'Ay 1 SD+1 (2)'),
    tc('TC-FI_SSN-BVA-19', '011101-0103', V, 'Ay 12 SD-1 (11)'),
    tc('TC-FI_SSN-BVA-20', '011201-010W', V, 'Ay 12 SD (12)'),
    tc('TC-FI_SSN-BVA-21', '011301-010P', I, 'Ay 12 SD+1 (13)'),
    tc('TC-FI_SSN-BVA-22', '010101-001R', I, 'Normal seri alt SD-1 (1)'),
    tc('TC-FI_SSN-BVA-23', '010101-002S', V, 'Normal seri alt SD (2)'),
    tc('TC-FI_SSN-BVA-24', '010101-003T', V, 'Normal seri alt SD+1 (3)'),
]


@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_fi_ssn(dogrula, girdi, parametreler, beklenen):
    dogrula("fi_ssn", girdi, parametreler, beklenen)
