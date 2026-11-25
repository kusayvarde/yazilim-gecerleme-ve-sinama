# Kara-Kutu Birim Testi - URL ve Ulusal Kimlikler

Sorumlu: **MMHDJ**. Dal: `MMHDJ`. Doğrulama tarihi: **26 Kasım 2026**.
Bu bölüm, ortak rapora eklenmek üzere hazırlanmıştır. Sonuç tabloları pytest JUnit
XML çıktısından yenilenir; diğer ekip üyelerinin dosyaları değiştirilmemiştir.

## 1. Kapsam

Bu çalışmada `url`, `es_nif`, `es_nie`, `es_cif`, `es_doi`, `fi_business_id`,
`fi_ssn`, `fr_ssn`, `ru_inn` ve `fr_department` incelenmiştir. `url` çok zor (5),
sekiz ulusal kimlik işlevi zor (8 × 3), `fr_department` kolay (1) olup toplam 31 puandır.

Ortam: Python **3.14.0**, `validators[crypto-eth-addresses]==0.36.0`, pytest **9.2.0**.
Bağımlılıklar mevcut `uv.lock` ile kurulmuştur; proje bağımlılıkları değiştirilmemiştir.
Testler yalnızca biçim, seçenek ve kontrol karakteri doğrulamasını sınar. Bir kimliğin
gerçek bir kişiye/kuruluşa atanmış olduğunu veya bir URL'nin erişilebilir olduğunu kanıtlamaz.

## 2. Yöntem

**Beklentilerin tasarımında validators kaynak kodu kullanılmamıştır.** İzin verilen
`inspect.signature()` ve `.__doc__` üzerinden kurallar çıkarılmış; aşağıdaki resmi
kaynaklarla karşılaştırılmıştır. Başarısızlıklar yalnızca fonksiyon çağrıları ve bağımsız
kontrol hesaplarıyla incelenmiştir. Kök neden yorumları iç uygulama hakkında kanıt değildir.

**Süreç açıklığı:** İlk dokümantasyon aramasının sonuçlarında istemeden validators
kaynağından bir kesit görünmüştür. Kaynak dosyası bilerek açılmamış ve bu kesit test
tasarımında kullanılmamıştır. Bununla birlikte "kaynağa hiçbir maruz kalma olmadı"
şeklinde mutlak bir iddia ileri sürülmemektedir.

- **EP:** Geçerli/geçersiz biçimler, yanlış kontrol karakterleri ve seçenekler ayrı sınıflardır.
- **BVA:** Uzunluklar, portlar, tarih bileşenleri ve geçici seri eşikleri için SD-1/SD/SD+1
  üçlüleri kullanılır. Gün ve ay sınırlarında kontrol karakteri her veri için yeniden hesaplanır.
- **Geçersiz sınıfları ayırma:** INN'nin 11. basamağı bozulduğunda 12. basamak yeniden
  hesaplanır; böylece ikinci kontrol kuralı birincideki hatayı maskeleyemez.
- **Örnekler:** On işlevin docstring'lerindeki tüm çalıştırılabilir örnekler ayrı testtir.
- **Karar tablosu:** Bu bölüm EP ve BVA'ya odaklanır; DT bonusu eklenmemiştir.
  Ortak Excel'deki DT sayfası Kusay'ın IPv4 karar tablosuna aittir.

![D1 - Kara-kutu modeli](diyagramlar/D1_urls_national_ids.png)

![D2 - Test süreci](diyagramlar/D2_urls_national_ids.png)

### Kaynaklar ve gereksinim önceliği

İlk sözleşme kurulu **0.36.0** sürümünün docstring'idir. Standarttan eklenen ve
docstring'de açıklanmayan beklentiler ayrıca belirtilir; gözlenen davranışa göre beklenti üretilmez.

- URL bileşenleri: [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986).
  DNS etiket uzunluğu: [RFC 1035 §2.3.4](https://www.rfc-editor.org/rfc/rfc1035).
  Port 0'ın ayrılmış olması: [RFC 6335 §6](https://www.rfc-editor.org/rfc/rfc6335.html#section-6).
- NIF/NIE kontrol tablosu ve XYZ dönüşümü:
  [İspanya İçişleri Bakanlığı](https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/).
  Kuruluş kimliklerinin yapısı: [Agencia Tributaria](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/guia-practica-cumplimentacion-modelo-censal-036/anexos/anexo-01-solicitud-nif-documentacion-aportar/informacion-sobre-numero-identificacion-fiscal/composicion-nif/personas-juridicas-entidades.html).
  CIF hesabı: [MAPA'da barındırılan teknik arşiv](https://www.mapa.gob.es/app/materialvegetal/docs/CIF.pdf).
  Bu son belge normatif metin değildir; tek konumların iki katının rakam toplamı,
  çift konumların toplamı ve kontrol 10 olduğunda 0'a dönüşümünü açıklar.
- Finlandiya işletme/HETU kontrol hesapları ve 2023 sonrası yüzyıl karakterleri:
  [Vero teknik belgesi](https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf).
  Normal bireysel seri 002-899: [Statistics Finland](https://stat.fi/meta/kas/hetu.html).
- NIR yapısı: [Service Public](https://www.service-public.gouv.fr/particuliers/vosdroits/F33078).
  Mod-97 ve Korsika dönüşümleri: [SNE arayüz sözleşmesi §6.9.2](https://sne.info.application.logement.gouv.fr/sites/default/files/2023-06/SNE_Contrat_interface_V13-20230619_v0.10.pdf).
  Departman kümesi: [INSEE COG 2026](https://www.insee.fr/fr/information/8740222).
- INN yapısı: [Rusya Federal Vergi Servisi](https://www.nalog.gov.ru/rn77/fl/interest/inn/).
  İki kontrol basamağının gerekliliği ayrıca `ru_inn.__doc__` içinde açıkça belirtilir.
  Katsayılar: [MediaScout WebAPI §4.1, INN doğrulaması](https://www.mediascout.ru/for_docs/WebAPI_ORD_09062023.pdf).
  Bu bir API sağlayıcısının teknik şartnamesidir; mevzuat kaynağı olarak sunulmaz.
  10 hane için `2,4,10,3,5,9,4,6,8`; 12 hanenin ilk kontrolü için
  `7,2,4,10,3,5,9,4,6,8`, ikinci kontrolü için `3,7,2,4,10,3,5,9,4,6,8`
  kullanılır. Her ağırlıklı toplam `(toplam % 11) % 10` ile tek basamağa indirilir.
  Üreteç ayrıca iki sabit docstring örneğiyle çapraz doğrulanmıştır.

## 3. Gereksinimler (T1)

Asıl dosya: `docs/tablolar/T1_urls_national_ids.csv` (UTF-8 BOM, `;`). Her satır tek
kuraldır. Beklenen çıktı sütunu o satırdaki örnek girdiye aittir. Son sütun aynı kuralın
hem geçerli hem geçersiz örneklerini kapsayabilir. Kısaltmalar işlev önekiyle açılır;
örneğin `REQ-URL` satırındaki `EP-01`, `TC-URL-EP-01` anlamındadır.

<!-- OTOMATIK:T1 -->
| ID | Fonksiyon | Gereksinim | Örnek girdi | Beklenen çıktı | Kaynak | Sınayan testler |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-ES_NIF-01 | es_nif | NIF kontrol harfi mod-23 tablosuyla uyuşmalıdır | '26643189N' | True | validators==0.36.0 es_nif.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-01, EP-02, EP-06, EP-07, EP-08, EP-09 |
| REQ-ES_NIF-02 | es_nif | NIF gövdesi yalnızca sekiz rakam içerir | '2664 189N' | ValidationError | validators==0.36.0 es_nif.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-04, EP-05, EP-10 |
| REQ-ES_NIF-03 | es_nif | Boş NIF geçersizdir | '' | ValidationError | validators==0.36.0 es_nif.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-03 |
| REQ-ES_NIF-04 | es_nif | NIF tam 9 karakterdir | '26643189' | ValidationError | validators==0.36.0 es_nif.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | BVA-01..03 |
| REQ-ES_NIE-01 | es_nie | NIE kontrol harfi XYZ dönüşümünden sonra mod-23 ile uyuşmalıdır | 'X0095892M' | True | validators==0.36.0 es_nie.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-01, EP-02, EP-06..08, EP-10 |
| REQ-ES_NIE-02 | es_nie | NIE öneki X Y veya Z olmalıdır | 'W1234567L' | ValidationError | validators==0.36.0 es_nie.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-09 |
| REQ-ES_NIE-03 | es_nie | NIE gövdesi yedi rakam içerir | 'X009 892M' | ValidationError | validators==0.36.0 es_nie.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-04, EP-05 |
| REQ-ES_NIE-04 | es_nie | Boş NIE geçersizdir | '' | ValidationError | validators==0.36.0 es_nie.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-03 |
| REQ-ES_NIE-05 | es_nie | NIE tam 9 karakterdir | 'X0095892' | ValidationError | validators==0.36.0 es_nie.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | BVA-01..03 |
| REQ-ES_CIF-01 | es_cif | CIF kontrol karakteri ağırlıklı toplam ile uyuşmalıdır | 'B25162520' | True | validators==0.36.0 es_cif.__doc__; https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/guia-practica-cumplimentacion-modelo-censal-036/anexos/anexo-01-solicitud-nif-documentacion-aportar/informacion-sobre-numero-identificacion-fiscal/composicion-nif/personas-juridicas-entidades.html; teknik algoritma ve mod-10 düzeltmesi: https://www.mapa.gob.es/app/materialvegetal/docs/CIF.pdf | EP-01, EP-02, EP-10 |
| REQ-ES_CIF-02 | es_cif | CIF kuruluş türü izin verilen harflerden olmalıdır | 'A25162520' | True | validators==0.36.0 es_cif.__doc__; https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/guia-practica-cumplimentacion-modelo-censal-036/anexos/anexo-01-solicitud-nif-documentacion-aportar/informacion-sobre-numero-identificacion-fiscal/composicion-nif/personas-juridicas-entidades.html | EP-06..09 |
| REQ-ES_CIF-03 | es_cif | CIF gövdesi yedi rakam içerir | 'B251 2520' | ValidationError | validators==0.36.0 es_cif.__doc__; https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/guia-practica-cumplimentacion-modelo-censal-036/anexos/anexo-01-solicitud-nif-documentacion-aportar/informacion-sobre-numero-identificacion-fiscal/composicion-nif/personas-juridicas-entidades.html | EP-04, EP-05 |
| REQ-ES_CIF-04 | es_cif | Boş CIF geçersizdir | '' | ValidationError | validators==0.36.0 es_cif.__doc__; https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/guia-practica-cumplimentacion-modelo-censal-036/anexos/anexo-01-solicitud-nif-documentacion-aportar/informacion-sobre-numero-identificacion-fiscal/composicion-nif/personas-juridicas-entidades.html | EP-03 |
| REQ-ES_CIF-05 | es_cif | CIF tam 9 karakterdir | 'B2516252' | ValidationError | validators==0.36.0 es_cif.__doc__; https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/guia-practica-cumplimentacion-modelo-censal-036/anexos/anexo-01-solicitud-nif-documentacion-aportar/informacion-sobre-numero-identificacion-fiscal/composicion-nif/personas-juridicas-entidades.html | BVA-01..03 |
| REQ-ES_DOI-01 | es_doi | Birleşik DOI doğrulayıcısı NIF NIE ve CIF türlerini kabul eder | 'X0095892M' | True | validators==0.36.0 es_doi.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-01, EP-06..08 |
| REQ-ES_DOI-02 | es_doi | DOI alt türünün kontrol karakteri geçerli olmalıdır | 'X0095892X' | ValidationError | validators==0.36.0 es_doi.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-02, EP-10 |
| REQ-ES_DOI-03 | es_doi | DOI gövdesinde boşluk veya özel karakter olamaz | 'X009 892M' | ValidationError | validators==0.36.0 es_doi.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-04, EP-05 |
| REQ-ES_DOI-04 | es_doi | Boş DOI geçersizdir | '' | ValidationError | validators==0.36.0 es_doi.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-03 |
| REQ-ES_DOI-05 | es_doi | Bibliyografik DOI İspanyol kimliği değildir | '10.1000/xyz123' | ValidationError | validators==0.36.0 es_doi.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | EP-09 |
| REQ-ES_DOI-06 | es_doi | İspanyol DOI biçimi 9 karakterdir | 'X0095892' | ValidationError | validators==0.36.0 es_doi.__doc__; https://www.interior.gob.es/opencms/ca/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/ | BVA-01..03 |
| REQ-FI_BUSINESS_ID-01 | fi_business_id | İşletme kimliğinde ağırlıklı mod-11 kontrolü gerekir | '0112038-9' | True | validators==0.36.0 fi_business_id.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-01..04, EP-10 |
| REQ-FI_BUSINESS_ID-02 | fi_business_id | Kontrol hesabında kalan 0 ise kontrol rakamı 0 olur | '1000002-0' | True | validators==0.36.0 fi_business_id.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-11 |
| REQ-FI_BUSINESS_ID-03 | fi_business_id | Kontrol hesabında kalan 1 olan gövde geçersizdir | '1000008-0' | ValidationError | validators==0.36.0 fi_business_id.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-12 |
| REQ-FI_BUSINESS_ID-04 | fi_business_id | Yedi basamak ve kontrol rakamı arasında tire bulunur | '01120389' | ValidationError | validators==0.36.0 fi_business_id.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-06, EP-07 |
| REQ-FI_BUSINESS_ID-05 | fi_business_id | Gövde ve kontrol rakamı sayısaldır | 'A112038-9' | ValidationError | validators==0.36.0 fi_business_id.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-08, EP-09 |
| REQ-FI_BUSINESS_ID-06 | fi_business_id | Boş işletme kimliği geçersizdir | '' | ValidationError | validators==0.36.0 fi_business_id.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-05 |
| REQ-FI_BUSINESS_ID-07 | fi_business_id | İşletme kimliği toplam 9 karakterdir | '0112038-' | ValidationError | validators==0.36.0 fi_business_id.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | BVA-01..03 |
| REQ-FI_SSN-01 | fi_ssn | HETU kontrol karakteri sayısal gövdenin mod-31 kalanıyla uyuşur | '010101-0101' | True | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-01, EP-02, EP-09 |
| REQ-FI_SSN-02 | fi_ssn | HETU tarihi takvimde var olmalıdır | '290200A010M' | True | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-03, EP-06, EP-07, BVA-10..21 |
| REQ-FI_SSN-03 | fi_ssn | Yüzyıl karakteri resmi kümeden olmalıdır | '010101+0101' | True | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-04, EP-05, EP-10..12 |
| REQ-FI_SSN-04 | fi_ssn | Boş HETU geçersizdir | '' | ValidationError | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-08 |
| REQ-FI_SSN-05 | fi_ssn | HETU tam 11 karakterdir | '010101-010' | ValidationError | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | BVA-01..03 |
| REQ-FI_SSN-06 | fi_ssn | allow_temporal_ssn=False iken geçici 900-999 serileri reddedilir | '010101-899P' | True | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | BVA-04..08 |
| REQ-FI_SSN-07 | fi_ssn | Seri alanı üç basamakla sınırlıdır | '010101-1000B' | ValidationError | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | BVA-09 |
| REQ-FI_SSN-08 | fi_ssn | Geçici seriler varsayılan veya açık True seçeneğiyle kabul edilir | '010101-900R' | True | validators==0.36.0 fi_ssn.__doc__; https://www.vero.fi/globalassets/tietoa-verohallinnosta/ohjelmistokehittajille/finnish-tax-administration_the-control-character-for-verifying-the-authenticity-of-finnish-business-ids-and-personal-identity-codes.pdf | EP-13, EP-14 |
| REQ-FR_SSN-01 | fr_ssn | Kontrol anahtarı verilmişse mod-97 ile uyuşmalıdır | '1 84 12 76 451 089 46' | True | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078; https://sne.info.application.logement.gouv.fr/sites/default/files/2023-06/SNE_Contrat_interface_V13-20230619_v0.10.pdf bölüm 6.9.2 | EP-01, EP-04, EP-10 |
| REQ-FR_SSN-02 | fr_ssn | Kontrol anahtarı isteğe bağlıdır | '1 84 12 76 451 089' | True | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078 | EP-02 |
| REQ-FR_SSN-03 | fr_ssn | Docstring kapsamındaki cinsiyet kodları 1 ve 2 kabul edilir | '3 84 12 76 451 089 46' | ValidationError | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078 | EP-03, EP-05 |
| REQ-FR_SSN-04 | fr_ssn | Korsika 2A ve 2B kodları kontrol hesabında 19 ve 18 olur | '1 84 12 2A 451 089 33' | True | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078; https://sne.info.application.logement.gouv.fr/sites/default/files/2023-06/SNE_Contrat_interface_V13-20230619_v0.10.pdf bölüm 6.9.2 | EP-06, EP-07 |
| REQ-FR_SSN-05 | fr_ssn | Boşluksuz resmi NIR gösterimi kabul edilmelidir (dokümanda belirsiz) | '184127645108946' | True | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078 | EP-08 |
| REQ-FR_SSN-06 | fr_ssn | Boş NIR geçersizdir | '' | ValidationError | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078 | EP-09 |
| REQ-FR_SSN-07 | fr_ssn | Komün kodu sayısal olmalıdır | '1 84 12 76 45A 089 46' | ValidationError | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078 | EP-11 |
| REQ-FR_SSN-08 | fr_ssn | Normal doğum ayı 01-12 aralığındadır; özel idari aylar kapsam dışıdır | '1 84 00 76 451 089 48' | ValidationError | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078 | BVA-01..06 |
| REQ-FR_SSN-09 | fr_ssn | Boşluksuz NIR 13 veya anahtarla 15 karakterdir (biçim varsayımı) | '184127645108' | ValidationError | validators==0.36.0 fr_ssn.__doc__; https://www.service-public.gouv.fr/particuliers/vosdroits/F33078 | BVA-07..12 |
| REQ-RU_INN-01 | ru_inn | 10 haneli INN kontrol basamağı ağırlıklı mod-11/mod-10 ile uyuşmalıdır | '7830002293' | True | validators==0.36.0 ru_inn.__doc__; https://www.nalog.gov.ru/rn77/fl/interest/inn/; katsayılar: https://www.mediascout.ru/for_docs/WebAPI_ORD_09062023.pdf (ИНН doğrulama bölümü) | EP-02..04, EP-09 |
| REQ-RU_INN-02 | ru_inn | 12 haneli INN her iki kontrol basamağını sağlamalıdır | '500100732259' | True | validators==0.36.0 ru_inn.__doc__; https://www.nalog.gov.ru/rn77/fl/interest/inn/; katsayılar: https://www.mediascout.ru/for_docs/WebAPI_ORD_09062023.pdf (ИНН doğrulama bölümü) | EP-01, EP-05, EP-10, EP-11 |
| REQ-RU_INN-03 | ru_inn | INN yalnızca rakamlardan oluşur | '783000229A' | ValidationError | validators==0.36.0 ru_inn.__doc__; https://www.nalog.gov.ru/rn77/fl/interest/inn/ | EP-07, EP-08 |
| REQ-RU_INN-04 | ru_inn | Boş INN geçersizdir | '' | ValidationError | validators==0.36.0 ru_inn.__doc__; https://www.nalog.gov.ru/rn77/fl/interest/inn/ | EP-06 |
| REQ-RU_INN-05 | ru_inn | INN uzunluğu yalnızca 10 veya 12 olabilir | '777777777' | ValidationError | validators==0.36.0 ru_inn.__doc__; https://www.nalog.gov.ru/rn77/fl/interest/inn/ | BVA-01..06 |
| REQ-FR_DEPARTMENT-01 | fr_department | 20 artık departman kodu olarak kabul edilmez | 20 | ValidationError | validators==0.36.0 fr_department.__doc__; https://www.insee.fr/fr/information/8740222 | EP-01, EP-02 |
| REQ-FR_DEPARTMENT-02 | fr_department | Denizaşırı departman kodları kabul edilir | '971' | True | validators==0.36.0 fr_department.__doc__; https://www.insee.fr/fr/information/8740222 | EP-03, EP-11 |
| REQ-FR_DEPARTMENT-03 | fr_department | 00 geçersiz departman kodudur | '00' | ValidationError | validators==0.36.0 fr_department.__doc__; https://www.insee.fr/fr/information/8740222 | EP-04 |
| REQ-FR_DEPARTMENT-04 | fr_department | Korsika kodları yalnızca 2A ve 2B olabilir | '2A' | True | validators==0.36.0 fr_department.__doc__; https://www.insee.fr/fr/information/8740222 | EP-05..07, EP-12 |
| REQ-FR_DEPARTMENT-05 | fr_department | Sayısal kodlar metin veya tamsayı olabilir | '75' | True | validators==0.36.0 fr_department.__doc__; https://www.insee.fr/fr/information/8740222 | EP-08, EP-09 |
| REQ-FR_DEPARTMENT-06 | fr_department | Boş departman kodu geçersizdir | '976' | True | validators==0.36.0 fr_department.__doc__; https://www.insee.fr/fr/information/8740222 | EP-10 |
| REQ-FR_DEPARTMENT-07 | fr_department | Sayısal metropol aralığı 01-95 olup 20 ayrı istisnadır | '00' | ValidationError | validators==0.36.0 fr_department.__doc__; https://www.insee.fr/fr/information/8740222 | BVA-01..06 |
| REQ-URL-01 | url | Belgelenmiş HTTP FTP ve HTTPS şemaları kabul edilir | 'http://duck.com' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-01, EP-02, EP-05 |
| REQ-URL-02 | url | URL ana makinesi IPv4 IPv6 veya IDN olabilir | 'http://10.0.0.1' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-03, EP-07, EP-08 |
| REQ-URL-03 | url | URL bileşenleri yasak karakter içeremez | 'http://example.com/">user@example.com' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-04, EP-12, EP-13 |
| REQ-URL-04 | url | Kullanıcı adı ve parola URL içinde kullanılabilir | 'https://user:pass@example.com' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-06 |
| REQ-URL-05 | url | Boş URL geçersizdir | '' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-09 |
| REQ-URL-06 | url | Mutlak URL şema içermelidir | 'example.com' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-10 |
| REQ-URL-07 | url | URL ana makine içermelidir | 'http:///path' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-11 |
| REQ-URL-08 | url | skip_ipv4_addr=True IPv4 adresini reddeder | 'http://8.8.8.8' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-14 |
| REQ-URL-09 | url | skip_ipv6_addr=True IPv6 adresini reddeder | 'http://[2001:db8::1]' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-15 |
| REQ-URL-10 | url | may_have_port=False açık portu reddeder | 'http://example.com:80' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-16 |
| REQ-URL-11 | url | simple_host yalnızca açık olduğunda tek etiketli ana makineye izin verir | 'http://localhost' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-17, EP-18 |
| REQ-URL-12 | url | consider_tld=True IANA TLD kümesini uygular | 'http://example.invalidtld' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-19, EP-20 |
| REQ-URL-13 | url | private seçeneği IP adresinin özel veya genel olmasını kısıtlar | 'http://192.168.1.1' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-21..24 |
| REQ-URL-14 | url | rfc_1034 seçeneği sondaki noktayı kontrol eder | 'http://example.com.' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-25, EP-26 |
| REQ-URL-15 | url | rfc_2782 seçeneği SRV alt çizgilerine izin verir | 'http://_sip._tcp.example.com' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-27, EP-28 |
| REQ-URL-16 | url | strict_query seçeneği hatalı sorgu alanını reddeder | 'http://example.com/?foo' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-29, EP-30 |
| REQ-URL-17 | url | validate_scheme kullanıcı tarafından sağlanan işlevi uygular | 'https://example.com' | True | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986 | EP-31, EP-32 |
| REQ-URL-18 | url | Hizmet portu 1-65535 aralığındadır; port 0 ayrılmıştır | 'http://example.com:-1' | ValidationError | validators==0.36.0 url.__doc__; https://www.rfc-editor.org/rfc/rfc3986; https://www.rfc-editor.org/rfc/rfc6335.html#section-6 | BVA-01..06, BVA-10..12 |
| REQ-URL-19 | url | DNS etiketi en çok 63 karakterdir | 'http://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com' | True | RFC 1035 bölüm 2.3.4; https://www.rfc-editor.org/rfc/rfc1035 | BVA-07..09 |
| REQ-FI_SSN-09 | fi_ssn | Normal bireysel seri en az 002 olmalıdır | 010101-001R | ValidationError | Statistics Finland: https://stat.fi/meta/kas/hetu.html; validators 0.36.0 fi_ssn.__doc__ | BVA-22..24 |
<!-- /OTOMATIK:T1 -->

## 4. Eşdeğerlik sınıfları (T2)

Tam T2, `reports/tablolar.xlsx` içindeki **T2 Eşdeğerlik Sınıfları** sayfasında işlev
adına göre filtrelenebilir. Sınıflar kod içindeki `tc` işaretlerinden otomatik üretilir.

Aşağıdaki temsilciler de aynı pytest XML verisinden alınır; her işlev için bir geçerli
ve bir geçersiz EP örneği gösterilir.

<!-- OTOMATIK:T2 -->
| Fonksiyon | Sınıf | Temsilci girdi | Beklenen | Test ID |
| --- | --- | --- | --- | --- |
| url | Doküman örneği (geçerli) | 'http://duck.com' | True | TC-URL-EP-01 |
| url | Doküman örneği (geçersiz) | 'http://example.com/">user@example.com' | ValidationError | TC-URL-EP-04 |
| es_nif | Doküman örneği (geçerli) | '26643189N' | True | TC-ES_NIF-EP-01 |
| es_nif | Doküman örneği (geçersiz) | '26643189X' | ValidationError | TC-ES_NIF-EP-02 |
| es_nie | Doküman örneği (geçerli) | 'X0095892M' | True | TC-ES_NIE-EP-01 |
| es_nie | Doküman örneği (geçersiz) | 'X0095892X' | ValidationError | TC-ES_NIE-EP-02 |
| es_cif | Doküman örneği (geçerli) | 'B25162520' | True | TC-ES_CIF-EP-01 |
| es_cif | Doküman örneği (geçersiz) | 'B25162529' | ValidationError | TC-ES_CIF-EP-02 |
| es_doi | Doküman örneği (geçerli) | 'X0095892M' | True | TC-ES_DOI-EP-01 |
| es_doi | Doküman örneği (geçersiz) | 'X0095892X' | ValidationError | TC-ES_DOI-EP-02 |
| fi_business_id | Doküman örneği (geçerli) | '0112038-9' | True | TC-FI_BUSINESS_ID-EP-01 |
| fi_business_id | Doküman örneği (geçersiz) | '1234567-8' | ValidationError | TC-FI_BUSINESS_ID-EP-02 |
| fi_ssn | Doküman örneği (geçerli) | '010101-0101' | True | TC-FI_SSN-EP-01 |
| fi_ssn | Doküman örneği (geçersiz) | '101010-0102' | ValidationError | TC-FI_SSN-EP-02 |
| fr_ssn | Doküman örneği (geçerli) | '1 84 12 76 451 089 46' | True | TC-FR_SSN-EP-01 |
| fr_ssn | Doküman örneği (geçersiz) | '3 84 12 76 451 089 46' | ValidationError | TC-FR_SSN-EP-03 |
| ru_inn | Doküman örneği (geçerli) | '500100732259' | True | TC-RU_INN-EP-01 |
| ru_inn | Doküman örneği (geçersiz) | '1234567890' | ValidationError | TC-RU_INN-EP-03 |
| fr_department | Doküman örneği (geçerli) | '971' | True | TC-FR_DEPARTMENT-EP-03 |
| fr_department | Doküman örneği (geçersiz) | 20 | ValidationError | TC-FR_DEPARTMENT-EP-01 |
<!-- /OTOMATIK:T2 -->

| İşlev | Geçerli sınıf | Geçersiz sınıf |
| --- | --- | --- |
| url | Şema + FQDN/IP/IDN, izin verilen seçenek | Eksik şema, yasak IP türü, hatalı sorgu |
| es_nif | Sekiz rakam ve mod-23 harfi | Yanlış harf veya gövdede karakter |
| es_nie | X/Y/Z öneki, yedi rakam, doğru harf | Başka önek veya yanlış kontrol |
| es_cif | Kuruluş türü ve doğru kontrol | Geçersiz tür veya yanlış kontrol |
| es_doi | NIF/NIE/CIF birleşimi | Bibliyografik DOI veya bozuk kimlik |
| fi_business_id | Tireli gövde ve mod-11 | Kalan 1, yanlış kontrol veya ayırıcı |
| fi_ssn | Takvim tarihi, yüzyıl, mod-31 | Olmayan tarih veya bozuk kontrol |
| fr_ssn | Anahtarlı/anahtarsız NIR ve Korsika | Yanlış anahtar veya bozuk komün |
| ru_inn | 10 haneli kontrol veya 12 haneli iki kontrol | Yanlış kontrol, uzunluk veya harf |
| fr_department | Metropol, 2A/2B, denizaşırı kod | 00, 20, 2C veya boş girdi |

![D3 - INN eşdeğerlik sınıfları](diyagramlar/D3_urls_national_ids.png)

`uretici.py` standart hesaplarını uygular ve `validators` içe aktarmaz. Sekiz sabit
docstring örneği `ornekleri_dogrula()` ile çapraz kontrol edilmiştir. NIR'da Korsika
dönüşümü, Finlandiya işletme kimliğinde mod-11 kalan 0/1 dalları ayrıca ele alınır.
Üretilen veriler gerçek bir kayıt sorgusundan alınmamıştır.

## 5. Sınır değer analizi (T3)

Uzunluğu sabit kimliklerin N-1/N/N+1 değerlerinde amaç biçim sınırını sınamaktır;
biçim dışındaki uzunluklarda kontrol anahtarının anlamı yoktur. FR NIR'ın iki ayrı
kabul uzunluğu (13/15) ayrı gruptur. Geçici HETU için 1000 serisi üç basamak alanından
taşar; bu test geçici numara seçeneğinden bağımsız olarak biçim açısından geçersizdir.
Normal HETU serisinin alt sınırı ayrıca 001/002/003 üçlüsüyle sınanır; her örneğin
mod-31 karakteri bağımsız hesaplandığından kontrol karakteri hatası sınırı maskelemez.
URL'de port 0 çevresi ayrıca gösterilmiştir; geçerli hizmet portunun alt sınırı 1 için de
0/1/2 üçlüsü vardır. NIR'ın özel idari ay değerleri bu normal doğum ayı analizinin dışındadır.

![D4 - Sınır değerler](diyagramlar/D4_urls_national_ids.png)

<!-- OTOMATIK:T3 -->
| Fonksiyon | Sınır | SD-1 | SD | SD+1 | Beklenen | Test ID |
| --- | --- | --- | --- | --- | --- | --- |
| es_cif | Biçim uzunluğu | 'B2516252' | 'B25162520' | 'B251625200' | I / V / I | TC-ES_CIF-BVA-01, TC-ES_CIF-BVA-02, TC-ES_CIF-BVA-03 |
| es_doi | Biçim uzunluğu | 'X0095892' | 'X0095892M' | 'X0095892M0' | I / V / I | TC-ES_DOI-BVA-01, TC-ES_DOI-BVA-02, TC-ES_DOI-BVA-03 |
| es_nie | Biçim uzunluğu | 'X0095892' | 'X0095892M' | 'X0095892M0' | I / V / I | TC-ES_NIE-BVA-01, TC-ES_NIE-BVA-02, TC-ES_NIE-BVA-03 |
| es_nif | Biçim uzunluğu | '26643189' | '26643189N' | '26643189N0' | I / V / I | TC-ES_NIF-BVA-01, TC-ES_NIF-BVA-02, TC-ES_NIF-BVA-03 |
| fi_business_id | Biçim uzunluğu | '0112038-' | '0112038-9' | '0112038-90' | I / V / I | TC-FI_BUSINESS_ID-BVA-01, TC-FI_BUSINESS_ID-BVA-02, TC-FI_BUSINESS_ID-BVA-03 |
| fi_ssn | Biçim uzunluğu | '010101-010' | '010101-0101' | '010101-01010' | I / V / I | TC-FI_SSN-BVA-01, TC-FI_SSN-BVA-02, TC-FI_SSN-BVA-03 |
| fi_ssn | Geçici seri 900 | '010101-899P'  [allow_temporal_ssn=False] | '010101-900R'  [allow_temporal_ssn=False] | '010101-901S'  [allow_temporal_ssn=False] | V / I / I | TC-FI_SSN-BVA-04, TC-FI_SSN-BVA-05, TC-FI_SSN-BVA-06 |
| fi_ssn | Geçici seri 999 | '010101-998W'  [allow_temporal_ssn=False] | '010101-999X'  [allow_temporal_ssn=False] | '010101-1000B'  [allow_temporal_ssn=False] | I / I / I | TC-FI_SSN-BVA-07, TC-FI_SSN-BVA-08, TC-FI_SSN-BVA-09 |
| fi_ssn | Gün 1 | '000101-010C' | '010101-0101' | '020101-010N' | I / V / V | TC-FI_SSN-BVA-10, TC-FI_SSN-BVA-11, TC-FI_SSN-BVA-12 |
| fi_ssn | Gün 31 | '300101-010R' | '310101-010C' | '320101-0101' | V / V / I | TC-FI_SSN-BVA-13, TC-FI_SSN-BVA-14, TC-FI_SSN-BVA-15 |
| fi_ssn | Ay 1 | '010001-0107' | '010101-0101' | '010201-010U' | I / V / V | TC-FI_SSN-BVA-16, TC-FI_SSN-BVA-17, TC-FI_SSN-BVA-18 |
| fi_ssn | Ay 12 | '011101-0103' | '011201-010W' | '011301-010P' | V / V / I | TC-FI_SSN-BVA-19, TC-FI_SSN-BVA-20, TC-FI_SSN-BVA-21 |
| fi_ssn | Normal seri alt | '010101-001R' | '010101-002S' | '010101-003T' | I / V / V | TC-FI_SSN-BVA-22, TC-FI_SSN-BVA-23, TC-FI_SSN-BVA-24 |
| fr_department | Metropol 1 | '00' | '01' | '02' | I / V / V | TC-FR_DEPARTMENT-BVA-01, TC-FR_DEPARTMENT-BVA-02, TC-FR_DEPARTMENT-BVA-03 |
| fr_department | Metropol 95 | '94' | '95' | '96' | V / V / I | TC-FR_DEPARTMENT-BVA-04, TC-FR_DEPARTMENT-BVA-05, TC-FR_DEPARTMENT-BVA-06 |
| fr_ssn | Ay 1 | '1 84 00 76 451 089 48' | '1 84 01 76 451 089 64' | '1 84 02 76 451 089 80' | I / V / V | TC-FR_SSN-BVA-01, TC-FR_SSN-BVA-02, TC-FR_SSN-BVA-03 |
| fr_ssn | Ay 12 | '1 84 11 76 451 089 30' | '1 84 12 76 451 089 46' | '1 84 13 76 451 089 62' | V / V / I | TC-FR_SSN-BVA-04, TC-FR_SSN-BVA-05, TC-FR_SSN-BVA-06 |
| fr_ssn | Boşluksuz uzunluk 13 | '184127645108' | '1841276451089' | '18412764510894' | I / V / I | TC-FR_SSN-BVA-07, TC-FR_SSN-BVA-08, TC-FR_SSN-BVA-09 |
| fr_ssn | Boşluksuz uzunluk 15 | '18412764510894' | '184127645108946' | '1841276451089460' | I / V / I | TC-FR_SSN-BVA-10, TC-FR_SSN-BVA-11, TC-FR_SSN-BVA-12 |
| ru_inn | Uzunluk 10 | '777777777' | '7830002293' | '77777777777' | I / V / I | TC-RU_INN-BVA-01, TC-RU_INN-BVA-02, TC-RU_INN-BVA-03 |
| ru_inn | Uzunluk 12 | '77777777777' | '500100732259' | '7777777777777' | I / V / I | TC-RU_INN-BVA-04, TC-RU_INN-BVA-05, TC-RU_INN-BVA-06 |
| url | Port 0 | 'http://example.com:-1' | 'http://example.com:0' | 'http://example.com:1' | I / I / V | TC-URL-BVA-01, TC-URL-BVA-02, TC-URL-BVA-03 |
| url | Port 65535 | 'http://example.com:65534' | 'http://example.com:65535' | 'http://example.com:65536' | V / V / I | TC-URL-BVA-04, TC-URL-BVA-05, TC-URL-BVA-06 |
| url | Etiket üst | 'http://aaaaa…' (73 karakter)  → sınır değeri (62) | 'http://aaaaa…' (74 karakter)  → sınır değeri (63) | 'http://aaaaa…' (75 karakter)  → sınır değeri (64) | V / V / I | TC-URL-BVA-07, TC-URL-BVA-08, TC-URL-BVA-09 |
| url | Hizmet portu alt | 'http://example.com:0' | 'http://example.com:1' | 'http://example.com:2' | I / V / V | TC-URL-BVA-10, TC-URL-BVA-11, TC-URL-BVA-12 |
<!-- /OTOMATIK:T3 -->

## 6. Test senaryoları (T4)

Tam liste `reports/tablolar.xlsx` içindeki **T4a Test Senaryoları** ve
**T4b Test Sonuçları** sayfalarındadır; işlev sütunundan bu bölümün on işlevi seçilir.
T4a'da gerçek sonuç/durum boş bırakılır; T4b yalnızca pytest XML çıktısından doldurulur.
`reports/T4_test_senaryolari.csv` aynı sonuçları taşır. Bu çıktılar yeniden üretilebilir
olduğu için Git'e eklenmez. Koddaki her senaryonun kimliği T1 ile eşleşir.

Her işlevden bir BVA kaydının gerçekleşen sonucu aşağıda pytest XML'den gösterilir:

<!-- OTOMATIK:T4 -->
| Test ID | Girdi | Parametreler | Beklenen | Gerçekleşen | Durum |
| --- | --- | --- | --- | --- | --- |
| TC-URL-BVA-01 | 'http://example.com:-1' | — | ValidationError | ValidationError | PASS |
| TC-ES_NIF-BVA-01 | '26643189' | — | ValidationError | ValidationError | PASS |
| TC-ES_NIE-BVA-01 | 'X0095892' | — | ValidationError | ValidationError | PASS |
| TC-ES_CIF-BVA-01 | 'B2516252' | — | ValidationError | ValidationError | PASS |
| TC-ES_DOI-BVA-01 | 'X0095892' | — | ValidationError | ValidationError | PASS |
| TC-FI_BUSINESS_ID-BVA-01 | '0112038-' | — | ValidationError | ValidationError | PASS |
| TC-FI_SSN-BVA-01 | '010101-010' | — | ValidationError | ValidationError | PASS |
| TC-FR_SSN-BVA-01 | '1 84 00 76 451 089 48' | — | ValidationError | ValidationError | PASS |
| TC-RU_INN-BVA-01 | '777777777' | — | ValidationError | ValidationError | PASS |
| TC-FR_DEPARTMENT-BVA-01 | '00' | — | ValidationError | ValidationError | PASS |
<!-- /OTOMATIK:T4 -->

Örnek: `TC-RU_INN-EP-11` birinci kontrol basamağı yanlış, ikinci kontrol basamağı
yeniden hesaplanmış 12 haneli sentetik INN'yi reddetmeyi bekler. `TC-FI_SSN-EP-06`
takvimde bulunmayan 31 Nisan'ı doğru mod-31 karakteriyle sınar.

## 7. Otomasyon

Her işlev ayrı `test_<fonksiyon>.py` dosyasındadır. Ortak `tc` ve `dogrula` kullanılır:

```python
@pytest.mark.parametrize("girdi, parametreler, beklenen", VAKALAR)
def test_es_nif(dogrula, girdi, parametreler, beklenen):
    dogrula("es_nif", girdi, parametreler, beklenen)
```

`dogrula` geçerli sonuçta `sonuc is True`, geçersiz sonuçta hem falsy değer hem
`ValidationError` tipini denetler. `pytest.raises` kullanılmaz. Doğru beklentiyle çelişen
bulgular `bug="BUG-60: ..."` biçiminde **strict xfail** olarak korunur; beklenmedik
bir düzelme XPASS nedeniyle test çalışmasını başarısız yapar.

PowerShell ile depo kökünden yeniden üretim:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
uv sync --locked
uv run python -c "from tests.urls_national_ids.uretici import ornekleri_dogrula; ornekleri_dogrula()"
uv run pytest
uv run python scripts/sonuc_tablosu.py
uv run python -m tests.urls_national_ids.rapor_uret
```

Son komut yalnızca bu bölümün raporundaki otomatik blokları, T6'nın gözlenen değerlerini
ve kendi D1-D5 görsellerini yeniler. Tüm testler yerine yalnızca bu alan çalıştırılırsa
ortak T1 kontrolü diğer alanın sonuçlarını eksik bulur; birleşik rapor için tam pytest gerekir.

## 8. Sonuçlar (T5)

Aşağıdaki sayılar mevcut JUnit XML dosyasından hesaplanmıştır. XFAIL, işlevin doğru
çalıştığı anlamına gelmez; belgelenmiş bir uyuşmazlığın yeniden gözlendiğini gösterir.

<!-- OTOMATIK:T5 -->
| Fonksiyon | Toplam | EP | BVA | PASS | FAIL | XFAIL |
| --- | --- | --- | --- | --- | --- | --- |
| url | 44 | 32 | 12 | 44 | 0 | 0 |
| es_nif | 13 | 10 | 3 | 13 | 0 | 0 |
| es_nie | 13 | 10 | 3 | 13 | 0 | 0 |
| es_cif | 13 | 10 | 3 | 13 | 0 | 0 |
| es_doi | 13 | 10 | 3 | 13 | 0 | 0 |
| fi_business_id | 15 | 12 | 3 | 15 | 0 | 0 |
| fi_ssn | 38 | 14 | 24 | 36 | 0 | 2 |
| fr_ssn | 23 | 11 | 12 | 20 | 0 | 3 |
| ru_inn | 17 | 11 | 6 | 16 | 0 | 1 |
| fr_department | 18 | 12 | 6 | 18 | 0 | 0 |
| TOPLAM | 207 | 132 | 75 | 201 | 0 | 6 |

Alan: 207 test, 201 PASS, 0 FAIL, 6 XFAIL. Tüm depo: 517 test, 503 PASS, 0 FAIL, 14 XFAIL.

T1: 76 gereksinim; T3: 25 sınır grubu. Başarı oranı: %97.1 (XFAIL başarıya eklenmemiştir).
<!-- /OTOMATIK:T5 -->

![D5 - Alan sonuçları](diyagramlar/D5_urls_national_ids.png)

İncelenebilir yürütme kanıtları: `reports/sonuc.xml` ve `reports/rapor.html`.
Sonuçlar çalıştırma tarihindeki kilitli sürümlere aittir; başka sürümler için genellenemez.

![Birleşik pytest HTML raporunun özeti](diyagramlar/HTML_urls_national_ids.png)

Bu görüntü gerçek HTML raporundan alınmıştır ve tüm deponun özetini gösterir;
yalnızca MMHDJ bölümünün sonucu olarak yorumlanmamalıdır.

![pytest konsol çıktısı](diyagramlar/CONSOLE_urls_national_ids.png)

Konsol görseli gerçek pytest stdout/stderr kaydının tarayıcıda görüntülenmiş
halidir; yerel terminal penceresinin ekran görüntüsü olarak sunulmaz.
Ham kayıt: `reports/pytest_urls_national_ids_console.txt`.

## 9. Bulgular ve analiz (T6)

<!-- OTOMATIK:T6 -->
| Bulgu ID | Test ID | Girdi | Beklenen | Gerçekleşen | Kök neden yorumu | Önem |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-60 | TC-FI_SSN-EP-06, TC-FI_SSN-EP-07 | '310401-010T' \| '290201-010W' | ValidationError | True | Takvimde olmayan günler doğru kontrol karakteriyle kabul ediliyor. Vero belgesi ilk altı haneyi doğum tarihi olarak tanımlar. datetime.date ile 31 Nisan ve artık olmayan yıldaki 29 Şubat bağımsız doğrulanmıştır. İç neden kaynak kodu okunmadığı için bilinmiyor. | Orta |
| BUG-61 | TC-FR_SSN-EP-08, TC-FR_SSN-BVA-08, TC-FR_SSN-BVA-11 | '184127645108946' \| '1841276451089' | True | ValidationError | Boşluksuz 13/15 karakterli NIR reddediliyor; aynı veri docstring biçiminde boşluklarla kabul ediliyor. Resmi NIR sayısal gösterimi destekler; ancak docstring yalnızca boşluklu örnek verir. Bu nedenle biçim gereksinimi belirsizliği olarak sınıflandırılmıştır. | Düşük |
| BUG-62 | TC-RU_INN-EP-11 | '500100732266' | ValidationError | True | 12 haneli INN için 11. kontrol basamağı bozulup 12. basamak yeniden hesaplandığında veri kabul ediliyor. Docstring iki kontrol basamağını da denetlemeyi taahhüt eder. Bu tek bir kontrol kuralını ihlal eden sentetik örnektir; iç neden kanıtlanmamıştır. | Yüksek |
<!-- /OTOMATIK:T6 -->

**BUG-60:** Takvim bütünlüğü standarda dayalı bir gereksinimdir; docstring ayrıntılı
takvim doğrulamasını açıklamaz. Dolayısıyla bulgu doğum tarihi anlambilimiyle uyumsuzluk
olarak değerlendirilir. Geçerli artık yıl örneği kabul edilirken iki olanaksız tarih de
kabul edilmiştir. Python `datetime.date` ile bu iki tarihin olanaksızlığı ayrıca doğrulanmıştır.

**BUG-61:** Boşluk eklemek aynı NIR verisini geçerli yapar. Standart gösterim ile API'nin
örnek biçimi arasındaki beklenti farkı açıkça kaydedilir; bu bulgu kesin bir hesap hatası
olarak sunulmaz. Üç test aynı biçim belirsizliğini sınar.

**BUG-62:** Docstring iki kontrol basamağını da taahhüt ettiği için en net sözleşme
uyuşmazlığı budur. 11. basamak yanlışken 12. basamağı bu yanlış veri üzerinden yeniden
hesaplamak sonucu geçerli yapmaktadır. Bu, atanmamış kimlik sorgusu değil, kontrol
karakteri doğrulamasının davranışsal sınamasıdır.

Port 0 için beklenti yalnızca 16 bit alan genişliğine göre belirlenmemiştir:
RFC 6335'in ayırma kuralı esas alınmıştır. Bu, hizmet portu politikasıdır;
URI sözdizimindeki bütün sayısal gösterimlerin kullanılabilir hizmet olduğu varsayılmaz.

## 10. Değerlendirme

EP, biçim ve seçenek kurallarını ayrı sınamayı; BVA ise küçük uzunluk/seri değişimlerini
görünür kılmayı sağlamıştır. Bağımsız kontrol hesapları, geçersiz test verisini geçerli
sanma riskini azaltmıştır. Testlerin kaynak kodundan bağımsız olması, aynı sözleşmeye
sahip başka bir uygulamada da kullanılabilmesini sağlar.

Bununla birlikte kod kapsamı ölçülmemiştir; iç yollar veya kök nedenler hakkında iddia
edilemez. Gerçek kişi/kuruluş kaydı, URL erişimi, tüm kuruluş türleri ve bütün tarihsel
kimlik istisnaları kapsam dışındadır. NIF'nin özel K/L/M türleri, NIR'ın özel idari ayları
ve bütün INN bölge tahsisleri için eksiksiz kapsama iddiası yoktur. Kaynaklar arasında
belirsizlik varsa açıkça ayrıştırılmıştır. Çalışma, seçilen sözleşmeler için izlenebilir
ve yeniden üretilebilir bir doğrulama bölümüdür.

**Ekip entegrasyonu notu:** AFAHMAD1'in `domain` DT testleri de birleştiğinde ortak
`scripts/sonuc_tablosu.py` IPv4'e özgü DT sütunları kullandığı için bu dört satırın
sütunları kaymaktadır. Bu bölüm DT eklemez ve paylaşılan betiği değiştirmez.
Bu ortak raporlama sorunu ekip koordinasyonuyla ele alınmalıdır.
