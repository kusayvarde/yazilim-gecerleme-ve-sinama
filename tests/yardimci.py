"""Ekip ortak test yardımcısı: test senaryosu tanımı (tc) ve beklenen sonuç sabitleri.

Test verisi üreticileri tests/ dışında, `uretici/` paketindedir.
"""

import pytest

V = True    # beklenen: geçerli  -> sonuc is True
I = False   # beklenen: geçersiz -> ValidationError (falsy)


def tc(test_id, girdi, beklenen, sinif, *, bug=None, **parametreler):
    """Tek test senaryosu = tek pytest.param. ID, T4 tablosundaki Test ID ile aynıdır.

    bug: Başarısız test bir bulguysa "BUG-xx: açıklama" verilir; test silinmez,
    strict xfail olarak işaretlenir ve raporda görünür.
    """
    marks = [pytest.mark.tc(sinif=sinif)]
    if bug:
        marks.append(pytest.mark.xfail(reason=bug, strict=True))
    return pytest.param(girdi, parametreler, beklenen, id=test_id, marks=marks)
