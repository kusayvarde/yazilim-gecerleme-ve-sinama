# Presentation Guide: Black-Box Unit Testing of pyvalidators (Network & Crypto)

This guide explains **what** I built, **how the tests are structured**, **how to run them**, **where** the outputs go, and **why** each decision was made. Read it top to bottom once. Then use sections 9–11 as your demo script and Q&A cheat sheet.

---

## 1. The project in one paragraph

We test 15 functions of the Python library **`validators` (pyvalidators)**. The functions are `ipv4`, `ipv6`, `cron`, `btc_address`, `eth_address`, `trx_address`, `bsc_address`, `mac_address`, `uuid`, `md5`, `sha1`, `sha224`, `sha256`, `sha384` and `sha512`. We test them as a **black box**: we never look at the library's source code. We only use its **documentation** and the relevant **standards** (IPv4/IPv6 RFCs, Unix cron, Base58Check, EIP-55, BIP-173). We design the tests with **Equivalence Partitioning (EP)** and **Boundary Value Analysis (BVA)**, plus a **Decision Table (DT)** for ipv4 as a bonus. The tests are automated with **pytest**, and the result tables and charts are produced **automatically** from the test run.

**Result: 310 tests linked to 54 requirements. 302 PASS and 8 XFAIL. The 8 XFAIL tests are 4 real findings where the library disagrees with its own documentation.**

---

## 2. Key concepts (what you'll be asked about)

### 2.1 Black-box testing
We test the function only through its **inputs and outputs**:

```
   input (string + parameters)  ──►  [ validator function ]  ──►  True  /  ValidationError
                                       (inside is invisible)
```

- **Why black-box?** The assignment requires it. It also tests the **contract** (what the docs promise), not the implementation. That is exactly how we found doc-vs-behavior mismatches (section 8).
- **What we used instead of source code:** the docs pages and docstrings (e.g. `uuid` says *"valid UUID-v4 string"*) and the official standards.

### 2.2 Equivalence Partitioning (EP)
We split all possible inputs into **classes** that the function should treat the same way, then test **one representative per class**.
- `V` classes are **valid** (expected `True`). `I` classes are **invalid** (expected `ValidationError`).
- **Each invalid class gets its own test** and is never merged with another, because one error can **mask** another. Example: `"256.1.1"` breaks two rules at once (octet > 255 *and* only 3 octets). If it is rejected, we don't know which rule caught it.

Example (ipv4):
| Class | Meaning | Representative | Expected |
|---|---|---|---|
| V1 | normal 4 octets | `192.168.1.1` | True |
| I1 | octet > 255 | `256.1.1.1` | ValidationError |
| I7 | leading zero | `01.2.3.4` | ValidationError |
| I12 | `private=False` but address is private | `192.168.1.1` | ValidationError |

### 2.3 Boundary Value Analysis (BVA)
Bugs cluster at the **edges** of ranges. For every boundary (SD = *sınır değer*, boundary value) we test **SD−1, SD and SD+1**.

Example, the ipv4 octet range 0…255:
```
        invalid │          valid           │ invalid
   ─────────────┼──────────────────────────┼─────────────
            -1  0  1                254  255  256
            I   V  V                 V    V    I
```
We have two kinds of boundaries:
- **Numeric value boundaries:** octets (0–255), CIDR prefix (/0–/32, /0–/128), cron fields (minute 0–59, hour 0–23, day 1–31, month 1–12, weekday 0–7).
- **Length boundaries:** ipv6 groups (8), hex digits per group (4), eth/bsc hex length (40), trx length (34), mac groups (6), uuid length (36), hash length N (32/40/56/64/96/128).

### 2.4 Decision Table (DT, bonus)
`ipv4` has several boolean parameters that interact. We tabulated the combinations of `cidr` × `strict` × "does the input contain a CIDR?":

| Rule | cidr | strict | CIDR in input? | Expected |
|---|---|---|---|---|
| R1 | T | F | no | V |
| R2 | T | F | yes | V |
| R3 | T | T | no | I |
| R4 | T | T | yes | V |
| R5 | F | F | no | V |
| R6 | F | F | yes | I |
| **R7** | F | T | no | I → **library returns True (BUG-01)** |
| R8 | F | T | yes | I |

R7 is a **contradictory** combination: `strict` requires a CIDR, while `cidr=False` forbids one. The decision table is what exposed it.

### 2.5 The library's special behavior (very important)
The library **does not raise an exception** on invalid input. It returns:
- `True` for a valid input
- a **`ValidationError` object** for an invalid one. This object behaves like `False` (it is "falsy").

So our tests **don't use `pytest.raises`**. We check `sonuc is True` for valid input, and `not sonuc` **and** `isinstance(sonuc, ValidationError)` for invalid input. The second check makes sure the return **type** is also correct, not just "something falsy".

---

## 3. Project structure: what each part is and why it exists

```
proje/
├── pyproject.toml              ① dependencies + pytest settings
├── uv.lock                     ② exact locked versions
├── conftest.py                 ③ shared "dogrula" (verify) fixture
├── tests/
│   ├── yardimci.py             ④ tc() helper (+ V / I)
│   └── network_crypto/         ⑤ my area: the test files
│       ├── test_ipv4.py
│       ├── test_ipv6.py
│       ├── test_cron.py
│       ├── test_crypto_addresses.py   (btc, eth, trx, bsc)
│       ├── test_mac_uuid.py
│       └── test_hashes.py             (6 hashes in one file)
├── uretici/                    ④b standard-based test data (üretici), one module per area
├── scripts/
│   ├── sonuc_tablosu.py        ⑥ XML → tablolar.xlsx (all tables) + T4/T5 CSV
│   ├── sonuc_grafigi.py        ⑦ T5 → D5 chart (PNG)
│   └── rapor_uret.py           ⑦b fills each area report's automatic blocks + D1–D5
├── docs/
│   ├── tablolar/<area>/        ⑧ hand-written tables: T1_gereksinimler.csv, T6_bulgular.csv
│   └── diyagramlar/<area>/     ⑨ D1–D5 diagrams per area (network_crypto D2 in Mermaid)
└── reports/                    ⑩ generated outputs (not in git)
```

| # | Part | What it does | Why |
|---|---|---|---|
| ① | `pyproject.toml` | Pins `validators[crypto-eth-addresses]==0.36.0`. Holds the pytest config (`addopts`, `junit_family`, `xfail_strict`, markers). | **Results can change between library versions.** The whole team must use the same version. `eth_address` only works with the `crypto-eth-addresses` extra. With the options set here, everyone runs the same single command. |
| ② | `uv.lock` | Locks every package version exactly. | Reproducibility: the same results on every machine. |
| ③ | `conftest.py` | Defines the `dogrula` fixture: it calls the function, records the data, then asserts. | One shared verification rule for the whole team. It also records input, expected and actual into the XML so the tables can be built automatically. |
| ④ | `tests/yardimci.py` | `tc(...)` = one test case. Valid data is built separately in `uretici/` from the **standards** (Base58Check, EIP-55, Luhn, IBAN…). | Keeps test files short and uniform; test data code stays outside `tests/`. Our "valid" data is verified independently of the library, so a library bug can't hide behind wrong data. |
| ⑤ | test files | One file per function or function group. | Matches the guide's §7 layout and makes ownership clear. |
| ⑥ | `sonuc_tablosu.py` | Reads `reports/sonuc.xml` and writes **`reports/tablolar.xlsx`**, a formatted Excel file with one sheet per table (see section 6.4). T2, T3 and T4a are **derived from the test code**, so they can never disagree with it. It also **checks traceability**: every Test ID listed in T1 must exist, and every test must belong to at least one requirement (otherwise it exits with an error). | The guide says "Actual" and "Status" must **not** be filled by hand. Automating them prevents copy errors. |
| ⑦ | `sonuc_grafigi.py` | Draws D5: PASS/XFAIL/FAIL per function, and the EP/BVA/DT split. | A result chart is required in the report (§9). |
| ⑧ | `docs/tablolar/<area>/` | T1 (54 requirements, one per row, each with a `REQ-<FONK>-<no>` ID and the tests that cover it) and T6 (findings + root-cause analysis). | These need human judgment, so they are written by hand. |
| ⑩ | `reports/` | `sonuc.xml`, `rapor.html`, `tablolar.xlsx`, T4/T5 CSV, D5 PNG. | Regenerated on every run, so they are git-ignored. |

---

## 4. How one test works, end to end

### 4.1 Writing a test case: one line = one test
```python
tc("TC-IPV4-EP-21", "192.168.1.1", I, "I12 private=False + private", private=False)
#   Test ID          input         expected   class / boundary          extra parameters
```
- **Test ID format:** `TC-<FUNCTION>-<EP|BVA|DT>-<no>`. The **same ID** appears in the code, the pytest output, the HTML report and the T4 table. This gives **traceability**: any row in the report can be found in the code instantly.
- `V` = expect `True`. `I` = expect `ValidationError`.
- `**parametreler` passes options such as `strict=True` or `private=False` to the function.

### 4.2 The test function: the same pattern in every file
```python
@pytest.mark.parametrize("girdi, parametreler, beklenen", EP + BVA + DT)
def test_ipv4(dogrula, girdi, parametreler, beklenen):
    dogrula("ipv4", girdi, parametreler, beklenen)
```
`parametrize` turns **each `tc(...)` line into a separate test**. That is why one function produces 50 test results.

### 4.3 What `dogrula` does (conftest.py)
1. Calls `validators.ipv4("192.168.1.1", private=False)`.
2. Records test_id, function, input, parameters, technique (EP/BVA/DT, read from the ID), class, expected and actual result. These go into **`user_properties`**, which pytest writes into the JUnit XML.
3. Asserts:
   - expected valid → `assert sonuc is True`
   - expected invalid → `assert not sonuc` and `assert isinstance(sonuc, ValidationError)`
4. If the function **raises** an exception instead, that is recorded as the actual result as well.

### 4.4 The data pipeline
```
tc(...) lines ─► pytest ─► reports/sonuc.xml ─► sonuc_tablosu.py ─► tablolar.xlsx (T1, T2, T3, DT, T4, T5, T6)
                    │       (with properties)                    ├► T4_test_senaryolari.csv
                    │                                            └► T5_sonuc_ozeti.csv ─► sonuc_grafigi.py ─► D5_sonuc_grafigi.png
                    └─► reports/rapor.html (visual report)
```
`junit_family = "xunit1"` in `pyproject.toml` is what makes pytest write the per-test properties into the XML. Without it the T4 table couldn't be filled automatically.

### 4.5 Hashes: one scenario list, six functions
The 6 hash functions differ **only in length N** (md5=32, sha1=40, sha224=56, sha256=64, sha384=96, sha512=128). So `test_hashes.py` defines **13 scenarios once** (including each function's own documentation examples) and multiplies them by 6 functions, which gives 78 tests.
- EP: lowercase, mixed case and digit+letter hex (V); non-hex char, `0x` prefix, space, empty string, and another algorithm's length (I); the docs' real hash example (V) and `'900zz11'` (I).
- BVA: lengths N−1 / N / N+1.

Each generated test still gets a proper ID (`TC-SHA256-BVA-03`, …). **Point to make: parametrize reduced test duplication.**

### 4.6 How the "valid" crypto data was verified (black-box safe)
- **BTC/TRX:** `base58check()` implements the standard: payload + first 4 bytes of `sha256(sha256(payload))`, encoded in Base58. TRX = version byte `0x41` + 20 bytes, which gives 34 characters starting with `T`.
- **ETH:** `eip55()` implements EIP-55 (a letter is uppercased if the matching nibble of `keccak256(lowercase address)` ≥ 8). It reproduces the official EIP-55 test vector `0x5aAeb…`. This revealed that the example in our guide, `0x8Ba1f…DBa72`, is **not** a valid checksum, so that test expects a ValidationError (and the library agrees).
- **SegWit:** official BIP-173 example addresses.

---

## 5. What is tested per function

| Function | Difficulty (points) | Tests | EP | BVA | DT | Main boundaries |
|---|---|---|---|---|---|---|
| ipv4 | very hard (5) | 54 | 27 | 19 | 8 | octet 0/255 (first & last position), 4 octets, CIDR /0 & /32 |
| ipv6 | very hard (5) | 41 | 23 | 18 | – | 8 groups, `::` = ≥1 group, 4 hex per group, CIDR /0 & /128, f/g hex edge |
| cron | hard (3) | 47 | 14 | 33 | – | every field: min−1, min, min+1, max−1, max, max+1; field count 5 |
| btc_address | hard (3) | 20 | 14 | 6 | – | SegWit data length 14 / 74 (full triplets) |
| eth_address | hard (3) | 13 | 10 | 3 | – | hex length 40 |
| trx_address | hard (3) | 13 | 10 | 3 | – | total length 34 |
| bsc_address | easy (1) | 11 | 8 | 3 | – | hex length 40 |
| mac_address | easy (1) | 16 | 10 | 6 | – | 6 groups, 2 hex per group |
| uuid | easy (1) | 17 | 14 | 3 | – | length 36 |
| md5 … sha512 (6) | easy (1 each) | 78 | 60 | 18 | – | length N |
| **Total** | **31 points** | **310** | **190** | **112** | **8** | |

**Two-sided ranges get six boundary tests.** For a range like minute 0–59, the lower boundary gets −1/0/1 and the upper gets 58/59/60, so SD−1, SD and SD+1 are covered at *both* ends.

**Documentation examples are tests too.** Every valid/invalid example in each function's docstring has its own test (class "Doküman örneği"), so the docs' own promises are verified.

**Why this distribution:** the guide says to spread effort by points. Very hard functions get the most tests (~20–30, plus the decision table for ipv4), hard ones ~12–18, easy ones ~6–10.

**Requirement ambiguity (mention it!):** the cron docs don't define `*/n`, `a-b` or `a,b` syntax explicitly. We assumed standard **Unix cron** behavior and wrote that in the report. `-1` in cron can also be read as a broken range, because `-` is the range operator.

---

## 6. How to run it: where and why

All commands run **from the project root** (`proje/`, the folder containing `pyproject.toml`).

### 6.1 One-time setup
```bash
uv sync
```
Creates `.venv` with the exact locked versions. **Why `uv`:** one tool for the Python version, the dependencies and the lock file, so the team's environments are identical.

### 6.2 Run all tests
```bash
uv run pytest
```
- Finds the tests in `tests/` (set by `testpaths`).
- Produces **`reports/sonuc.xml`** (machine-readable JUnit) and **`reports/rapor.html`** (a visual report: open it in a browser and screenshot it for the report).
- Expected summary line: `302 passed, 8 xfailed`.

### 6.3 Run a part
```bash
uv run pytest tests/network_crypto                  # only my area
uv run pytest tests/network_crypto/test_ipv4.py     # one file
uv run pytest -k "TC-IPV4-DT-07"                    # one test case by ID
uv run pytest -k "IPV4 and BVA"                     # all ipv4 boundary tests
```

### 6.4 Generate the report tables and chart
```bash
uv run python scripts/sonuc_tablosu.py   # → reports/tablolar.xlsx + T4_test_senaryolari.csv, T5_sonuc_ozeti.csv
uv run python scripts/sonuc_grafigi.py   # → reports/D5_sonuc_grafigi.png
```
Run them **in this order, after pytest**, because each step reads the previous step's output. **Open `reports/tablolar.xlsx` for reading and for the report.** Sheets, in the order the assignment asks for them:

| Sheet | One row per | Content |
|---|---|---|
| T1 Gereksinimler | requirement | ID (`REQ-IPV4-02`), function, requirement, example input, expected output, source (doc/standard), covering tests |
| T2 Eşdeğerlik Sınıfları | class | function, class code (V1, I3, DOK), description, **one representative**, expected |
| T3 Sınır Değerler | boundary | function, boundary, **SD−1 / SD / SD+1** values, expected (e.g. `I / V / V`) |
| DT Karar Tablosu | rule | ipv4 cidr × strict × CIDR-in-input |
| T4a Test Senaryoları | test | design stage: Test ID, requirement, input, technique, expected; **Actual and Status empty** |
| T4b Test Sonuçları | test | same, with Actual and Status filled from pytest |
| T5 Sonuç Özeti | function | totals, EP/BVA/DT counts, PASS/FAIL/XFAIL, success %, TOTAL row |
| T6 Bulgular | finding | failed tests and root-cause analysis |

If `tablolar.xlsx` is open in Excel, Windows locks it; the script then writes `tablolar_yeni.xlsx` instead and tells you. Every table is on its own sheet, with a colored header, wrapped text, filters, and colored statuses (PASS green, XFAIL yellow). The CSVs use a UTF-8 BOM and the `;` delimiter, so they also open correctly in Turkish Excel with Turkish characters and separate columns.

> On this Windows machine, if the console shows a `UnicodeEncodeError`, prefix the command: `PYTHONIOENCODING=utf-8 uv run pytest`.

### 6.5 What the statuses mean
| Status | Meaning |
|---|---|
| PASS | The library behaved as the documentation/standard says. |
| XFAIL | A **known finding**: the test is correct, the library disagrees, and the test is marked with a BUG ID. |
| FAIL | Something unexpected. It must be analyzed (see section 7). |
| XPASS (shows as FAIL) | A test marked as a bug suddenly passes, e.g. the library was fixed. `xfail_strict = true` makes this visible instead of silent. |

---

## 7. Failure-analysis process (assignment item 8)

When a test fails, first ask: **is my test wrong, or is the library wrong?**
1. Compare the expected value with the requirement again (docs/standard).
2. Verify the test data (e.g. is the address really valid? Check it with our EIP-55/Base58Check üretici functions in `uretici/`).
3. If the data is correct and the library returns something else, it is a **finding**.
4. **Don't delete the test.** Mark it with `tc(..., bug="BUG-xx: ...")`. It becomes a strict xfail, shows up in the reports, and gets a row in `docs/tablolar/network_crypto/T6_bulgular.csv`.

```
FAIL ─► is the expected value / test data correct?
          ├─ no  ─► fix the test ─► rerun
          └─ yes ─► finding: BUG-xx (xfail) + T6 row ─► rerun
```

---

## 8. Findings (T6): the highlight of the presentation

| ID | Test IDs | What happens | Why it's a finding | Severity |
|---|---|---|---|---|
| **BUG-01** | TC-IPV4-DT-07 | `ipv4("1.2.3.4", cidr=False, strict=True)` → **True** | `strict=True` means "CIDR required", but it is silently ignored when `cidr=False`. The docs don't define this combination (requirement ambiguity). Found by the **decision table**. | Low |
| **BUG-02** | TC-UUID-EP-12, -13 | a v1 UUID and the nil UUID `00000000-…` → **True** | The docstring says *"valid UUID-v4 string"*, but the version field is not checked. | Medium |
| **BUG-03** | TC-UUID-EP-08, -09, -10 | no dashes, `{…}` and `urn:uuid:…` → **True** | The 8-4-4-4-12 format is not enforced. This matches what Python's own `uuid.UUID()` accepts (an observation from behavior, not from source). | Low |
| **BUG-04** | TC-UUID-EP-11, -14 | `2bc1c94f0-deb-…`, `2-b-c-1c94f…` → **True** | Dash positions aren't checked at all, so malformed strings pass a *format* validator. | Medium |
| GÖZLEM-01 (observation) | TC-BTC-BVA-02, -03, -05, -06 | `bc1` + `qqq…` (14–74 chars) → **True** | SegWit addresses are only **format**-checked, not checksum-verified. **The docstring says so explicitly** ("for segwit addresses a regexp is used to provide a reasonable estimate"), so this is a known, documented limitation, not a bug. Legacy addresses *are* checksum-checked (TC-BTC-EP-05 is rejected). | Info |

**Message for the audience:** most findings are in `uuid`, an "easy" function. A function's difficulty doesn't predict where the bugs are. A systematic EP/BVA design catches them anyway.

---

## 9. Suggested presentation flow (~10 minutes)

1. **Scope** (1 min): 15 functions, the difficulty/points table, library version 0.36.0, and black-box (source code not consulted).
2. **Method** (2 min): black-box model (D1), EP, BVA (show the octet number line), the decision table for ipv4.
3. **The library's quirk** (30 s): it returns `ValidationError` instead of raising, so we check `is True` / `not sonuc` + `isinstance`.
4. **Structure** (2 min): the folder tree. The `tc(...)` one-liner → `parametrize` → `dogrula`. Test ID traceability.
5. **Live demo** (2 min), see section 10.
6. **Results** (1 min): 310 tests, T5 table, D5 chart.
7. **Findings** (1.5 min): BUG-01 … BUG-04 + the SegWit observation.
8. **Evaluation** (30 s): strengths and weaknesses (section 11).

## 10. Live demo script

```bash
uv run pytest tests/network_crypto -q          # 1. whole suite: "302 passed, 8 xfailed"
uv run pytest -k "IPV4 and BVA"                # 2. show the boundary tests by ID
uv run pytest -k "TC-IPV4-DT-07"               # 3. show one finding (XFAIL with BUG-01 reason)
uv run python scripts/sonuc_tablosu.py         # 4. build the tables
uv run python scripts/sonuc_grafigi.py         # 5. build the chart
```
Then open `reports/rapor.html` in a browser, `reports/tablolar.xlsx` (T1 → T2 → T3 → T4a; then sheet "T4b Test Sonuçları" filtered on Durum = XFAIL; then T5 and T6), and `reports/D5_sonuc_grafigi.png`.

Optional: show the library's quirk live in a Python shell:
```python
>>> import validators
>>> validators.ipv4("192.168.1.1")
True
>>> validators.ipv4("256.1.1.1")
ValidationError(func=ipv4, args={'value': '256.1.1.1'})
>>> bool(validators.ipv4("256.1.1.1"))
False
```

---

## 11. Likely questions and answers

**Q: How do you know you didn't look at the source code?**
A: All expectations come from the docs and standards. `network_crypto/T1_gereksinimler.csv` has a "Kuralın kaynağı" (rule source) column that says, for each function, which part comes from the docstring and which from a standard. All 15 docstrings were checked against it. Failures were analyzed by calling the function and reading the docstring only. Valid crypto data is generated by our own standard implementations in `yardimci.py`.

**Q: Why not `pytest.raises`?**
A: The library doesn't raise on invalid input. It returns a falsy `ValidationError`. We also assert the type, so a wrong falsy value (e.g. `False` or `None`) would still fail the test.

**Q: Why is every invalid class a separate test?**
A: To avoid masking: if an input breaks two rules, a rejection doesn't tell you which rule worked.

**Q: Why test the last octet too, not only the first?**
A: To check that the boundary is enforced at every position (TC-IPV4-BVA-07/08).

**Q: Why do failing tests stay in the code?**
A: The assignment asks for failure analysis. Strict xfail keeps findings visible in every report, and it alerts us if the behavior ever changes (XPASS → FAIL).

**Q: Some SegWit BVA tests use addresses that aren't real. Is that valid?**
A: Yes, and we say so explicitly. Those tests check the documented **format** rule (14–74 data chars). The fact that they pass matches the docstring, which says SegWit is only checked by a regex (GÖZLEM-01).

**Q: Strengths and weaknesses of black-box testing here?**
- **Strengths:** independent of the implementation, and it tests what users are promised. It found real doc/behavior mismatches (uuid v4, strict+cidr). Tests stay valid if the implementation is rewritten.
- **Weaknesses:** we can't know whether all internal paths were covered (no code coverage). Ambiguous docs (cron syntax, contradictory parameters) force assumptions. The number of input combinations is huge, so EP/BVA only samples it.

**Q: How would the team merge their work?**
A: Same ID format, same `tc` + `dogrula` pattern, each person in their own `tests/<area>/` folder. One `uv run pytest` produces one combined HTML report and one T4/T5 table set.
