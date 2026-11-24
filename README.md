# Kara-Kutu Birim Testi – pyvalidators

`validators` kütüphanesinin fonksiyonlarının **kaynak koduna bakılmadan**, yalnızca
dokümantasyon ve ilgili standartlara göre Eşdeğerlik Bölümleme (EP), Sınır Değer
Analizi (BVA) ve karar tablosu (DT) ile test edilmesi.

- Kütüphane: `validators==0.36.0` (+ `crypto-eth-addresses` ekstrası), Python 3.14
- Sürümler `pyproject.toml` + `uv.lock` ile sabittir; ekipteki herkes aynı sonucu alır.

## Kurulum ve çalıştırma

```bash
uv sync                                    # ortamı kur
uv run pytest                              # tüm testler -> reports/sonuc.xml + reports/rapor.html
uv run python scripts/sonuc_tablosu.py     # -> reports/tablolar.xlsx (T1, T2, T3, DT, T4a, T4b, T5, T6) + izlenebilirlik kontrolü
uv run python scripts/sonuc_grafigi.py     # -> reports/D5_sonuc_grafigi.png
uv run python scripts/diyagramlar.py       # -> docs/diyagramlar/D1, D3, D4 (PNG)
```

Tek bir alanı çalıştırmak için: `uv run pytest tests/network_crypto`

## Klasör yapısı

```
conftest.py              ortak `dogrula` fixture'ı (çağır + XML'e kaydet + doğrula)
tests/yardimci.py        tc() senaryo tanımı, Base58Check / EIP-55 veri üreticileri
tests/network_crypto/    Network & Crypto alanı (15 fonksiyon)
tests/<kisi_alani>/      diğer ekip üyelerinin alanları (aynı düzen)
scripts/                 JUnit XML -> CSV tabloları ve grafik
docs/tablolar/           elle yazılan tablolar, alan başına: T1_<alan>.csv, T6_<alan>.csv
docs/diyagramlar/        D1–D5 diyagramları
reports/                 üretilen çıktılar (git'e girmez)
```

## Ekip kuralları

Tam kurallar, Git iş akışı (master ← dev ← kişi dalları) ve AI agent talimatları: **AGENTS.md**.

1. **Test ID:** `TC-<FONK>-<EP|BVA|DT>-<no>`, ör. `TC-IPV4-BVA-03`. Koddaki
   `tc("TC-...")` ID'si tablodaki ID ile birebir aynıdır.
2. **Her senaryo bir `tc(...)` satırıdır:**
   ```python
   tc("TC-IPV4-EP-21", "192.168.1.1", I, "I12 private=False + private", private=False)
   #   Test ID          girdi        beklenen  sınıf / sınır             parametreler
   ```
   `V` = geçerli (`sonuc is True`), `I` = geçersiz (`not sonuc` ve `ValidationError`).
   Kütüphane geçersiz girdide hata **fırlatmaz**; bu yüzden `pytest.raises` kullanılmaz.
3. **Test fonksiyonu her zaman aynı kalıptadır:**
   ```python
   @pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
   def test_ipv4(dogrula, girdi, parametreler, beklenen):
       dogrula("ipv4", girdi, parametreler, beklenen)
   ```
4. **Başarısız test silinmez.** Test verisi doğruysa `tc(..., bug="BUG-xx: ...")`
   ile strict xfail olarak işaretlenir ve kendi `docs/tablolar/T6_<alan>.csv` dosyasına yazılır.
5. **Geçerlilik verisi standarttan doğrulanır** (Base58Check, EIP-55, BIP-173);
   `tests/yardimci.py`'deki üreticiler kütüphaneden bağımsızdır.
