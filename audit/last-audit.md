# 점검 기준선

점검일: 2026-09-06 (2차 — 1차 기준선 재확인)
직전: 2026-09-06 1차 (결함 22건 → 수정 11 / 미수정 11)

**재확인 결과: 해결됨 12건 / 미해결 10건 / 근거없음 0건**
(2차 최초 판정은 해결 11 / 미해결 11 이었으나, #22 를 3차에서 정정했다)
추가로 1차에서 "인용불가"로 제외했던 6건 중 6건 전부 해결, "다음 점검에서
대조할 것" 4건 중 1건 해결. 신규 결함 1건 발견(#25, 이번 회차에 새로 만든 것).

> 이번 회차는 **재확인 + 문서 보완**만 했다. 실행 결과 숫자를 바꾸는 코드 수정은
> 하지 않았다. 그래서 1차의 `미수정` 11건은 전부 그대로 `미해결` 이다.

점검 방법: push 직후 `codeload` tarball 로 `LeeKwanBeom/hometax-invoice-check@main`
실물을 다시 받아(`/home/claude/verify`) 설치본 SKILL.md 와 대조.
`tests/fixtures/` 6개로 build_report → validate 를 기본·`--as-of 2026-01-05` 2회 실행.

경로 표기는 1차와 같다. `SKILL.md(설치)` = `/mnt/skills/plugins/hometax-invoice-check/SKILL.md`.

**줄 번호는 2026-09-06 2차 시점 실물 기준이다.** 1차 기준선의 줄 번호와 다르다
(설치 SKILL.md 가 259행 → 348행이 되었다).

---

## 1차 결함 24행 재판정

| # | 1차 | **재판정** | 파일 | 지금 줄 | 지금 파일의 원문 |
|---|---|---|---|---|---|
| 1 | 수정함 | **해결됨** | SKILL.md(설치) | 123 | `**4단계에서 `--as-of` 나 `--strict` 를 줬으면 여기에도 똑같이 준다.**` |
| 2 | 수정함 | **해결됨** | SKILL.md(설치) | 74 | `- **1월에 실행할 때만 전년 12월 1일부터 받는다.** 12월분 발급기한이 익년 1월이라` |
| 3 | 수정함 | **해결됨** | SKILL.md(저장소) | 74 | 설치본과 `diff` 무차이 · md5 동일 (`25ec0ca1992034937a63ba9b1f6685d3`) |
| 4 | 수정함 | **해결됨** | scripts/validate.py | 379, 384 | `if n == 0 and mrow:` / `rec(SKIP, "등급 분류", "미수취목록이 비어 있음 — 이번 회차에 잡힌 거래처가 없다")` |
| 5 | 미수정 | **미해결** | scripts/validate.py | 446-447 | `prev = as_of.month - 1`<br>`expect = prev >= 1 and is_in_grace(as_of.year, prev, as_of, cfg)` |
| 6 | 수정함 | **해결됨** | scripts/build_report.py | 540 | `split = drop_split_offsets(df)` (common.py 305행에 `def drop_split_offsets(df):`) |
| 7 | 수정함 | **해결됨** | scripts/validate.py | 273, 288, 298 | `cancel = orig = refund = neg = split = 0` / `split += 1` / `+ (f" · 짝이 기간 밖 {split}건" if split else "")` |
| 8 | 수정함 | **해결됨** | SKILL.md(설치) | 180 | `` \| `code` \| `SKILL.md`, `scripts/`, `config/check-config.json`, `references/`, `tests/`, `audit/`, `sync.py`, `README.md` \| `` |
| 9 | 수정함 | **해결됨** | SKILL.md(설치) | 107, 110 | `` \| `--strict` \| 지난 달까지 유예 없이 전부 미수취 판정. `` / `` `--strict` 라도 **실행 당월은 유예**다. `` |
| 10 | 수정함 | **해결됨** | SKILL.md(설치) | 246 | `{"biz_no": "0000000000", "name": "예시상사", "cycle": "매월",` |
| 11 | 미수정 | **미해결 (악화)** | SKILL.md(설치) | 31, **161** | `세금계산서 발급기한은 작성월 다음 달 10일. 9월 초에 돌리면 8월분이 아직`<br>**신규 사본** → `` \| `기한 전` \| 발급기한(익월 10일)이 아직 남음 \| 기다린다 \| `` |
| 12 | 미수정 | **미해결** | SKILL.md(설치) | 275 | `` → 발급기한(9/10) 전이라 정상이다. 등급이 `기한 전`이면 기다리면 된다. `` |
| 13 | 미수정 | **미해결** | scripts/validate.py | 498, 502 | `for fn in os.listdir(os.path.join(SKILL_DIR, "scripts")):`<br>`ref = os.path.join(SKILL_DIR, "references")` |
| 14 | 미수정 | **미해결** | references/excel-format.md | 15 | `` \| 1 \| 매트릭스 \| 공급자 × 월. 점검대상 먼저, 대상외 나중 \| `` |
| 15 | 미수정 | **미해결** | references/column-mapping.md | 5, 32 | `여기에 다시 적지 않는다 — `config/check-config.json` 의 `input` 블록이 유일한 출처다.`<br>`` \| 공급자 식별 \| `공급자사업자등록번호` \| `` |
| 16 | 미수정 | **미해결** | scripts/validate.py | 349 | `order = {"확인 필요": 0, "기한 전": 1, "단발·비정기": 2, "정상": 3,` (build_report.py 29행 `GRADE_ORDER` 와 동일 · config 에 `grades` 블록 없음) |
| 17 | 수정함 | **해결됨** | scripts/build_report.py | 162 | `elif f["cycle"] == "비정기" or f["months_got"] <= cfg["thresholds"]["sporadic_max_months"]:` |
| 18 | 미수정 | **미해결** | scripts/check_input.py | 156 | `if v.get("until"):`<br>`    continue` |
| 19 | 미수정 | **미해결** | scripts/check_input.py | 249 | `"\n변경이라면 vendors.json 에서 구 번호를 지우고 신 번호로 교체할 것.")`<br>(SKILL.md 267행 · judgment-rules.md 102행은 `구 번호에 until, 신 번호에 since`) |
| 20 | 미수정 | **미해결** | scripts/build_report.py | 334 | `ws["A1"] = f"공급자 × 월 매입 발급 매트릭스 ({as_of.year}-01-01 ~ {as_of})"` |
| 21 | 미수정 | **미해결** | scripts/build_report.py | 337 | `f"빈칸=미수취 · 노랑=발행 후 전액취소 · 연파랑=발급기한 전")` |
| 22 | 미수정 | **판정 정정 → 해결됨** | sync.py | 34 | **2차 판정이 방향을 반대로 잡았다.** 아래 "#22 판정 정정" 참조 |
| 23 | 수정함 | **해결됨** | scripts/push.py | 181, 186 | `if od and nd and nd == od:` / `if nf < of:` |
| 24 | 수정함 | **해결됨** | scripts/build_report.py | 272 | `by_id[bid]["status"] = "해결"` (`rows.append` 는 `bid` 가 이번 회차에 없을 때만) |

**근거없음 0건.** 1차 기준선의 24개 지적은 전부 실물에서 원문이 확인되거나
(미해결 11건) 수정 흔적이 확인되었다(해결 11건). 사실과 다른 지적은 없었다.

---

## #22 판정 정정 (2026-09-06 3차)

**2차 판정이 틀렸다.** 2차는 `sync.py` 34행 주석과 `SKILL.md` 192행이 모순되니
주석 쪽이 틀렸다고 보고 `미해결` 로 남겼다. 방향이 반대였다.

| | 원문 | 실제 |
|---|---|---|
| `sync.py` 34행 | `# Claude 계정에 설치된 SKILL.md 는 사용자가 직접 재업로드해야 바뀐다.` | **맞다** |
| `SKILL.md` 192행(2차 시점) | `이 경로는 **쓰기 가능하다.** 사용자에게 재업로드를 시키지 말고 직접 반영한다.` | **틀렸다** |

경로가 쓰기 가능한 것은 맞다(`touch` 실측). 그러나 **세션 간 보존되지 않는다.**
2차는 "쓰기 가능"만 확인하고 "보존되는가"를 확인하지 않아 결론을 뒤집었다.

### 보존되지 않는다는 근거

- `/mnt/skills/plugins/` 전체가 컨테이너 시작 시각(07:24)에 만들어졌고,
  손대지 않은 다른 플러그인 4개의 `SKILL.md` 는 전부 타임스탬프가 `Jan 1 1980`
  이다 — 아카이브에서 풀린 것이다
- **1차 기준선은 "스킬 폴더 — `SKILL.md` 덮어씀. 저장소본과 `diff` 동일 확인"
  이라고 기록했는데, 2차 세션 시작 시점의 설치본은 259행 옛 버전이었다.**
  전날 덮어쓴 내용이 되돌아간 것이다
- 1차가 같이 둔 `audit/last-audit.md` 도 사라져 사용자가 재업로드해야 했다

즉 1차·2차 두 번 모두 설치본을 고쳤고 두 번 다 헛일이었다. 2차의 SKILL.md
교체(259행 → 348행)도 다음 세션에는 남지 않는다.

### 이 정정에 따른 조치 (3차)

| 무엇 | 파일 |
|---|---|
| `SKILL.md` 192행 지침을 사실에 맞게 교체 — "직접 쓰지 말 것 + 재업로드 필요" | `SKILL.md` |
| `sync.py` 34행 주석에 보존 안 됨 실측 근거 추가 | `sync.py` |
| 설치용 얇은 부트스트랩 신설 — 절차를 담지 않아 재업로드가 필요 없게 | `install/SKILL.md` |
| `install/` 을 `GROUPS['code']` 스캔 대상에 추가 | `scripts/push.py` |
| 1단계에 `audit/last-audit.md` 를 함께 읽으라는 지침 추가 | `SKILL.md` |

> **개선안 #1(`sync.py --install-skill`)은 이제 불가능하다.** 설치 경로에
> 복사해봐야 세션이 끝나면 사라진다. 개선안 #1 을 `install/SKILL.md` +
> 사용자 재업로드 방식으로 **대체한다.** 다음 점검에서 개선안 목록을 갱신할 것.

---

## 신규 결함 (2차에서 발견)

| # | 심각도 | 파일 | 줄 | 원문 | 왜 틀렸는지 | 수정 방향 |
|---|---|---|---|---|---|---|
| 25 | 중간 | SKILL.md(양쪽) | 161 | `` \| `기한 전` \| 발급기한(익월 10일)이 아직 남음 \| 기다린다 \| `` | **이번 회차에 등급 표를 추가하면서 `deadline_day` 사본을 하나 더 만들었다.** 결함 #11 #12 와 같은 종류이고, 같은 회차에 같은 실수를 반복한 것이다. `validate.check_config_single_source` 는 SKILL.md 를 스캔하지 않아(#13) 영영 안 걸린다 | `기한 전` 행에서 `(익월 10일)` 을 빼고 "발급기한이 아직 남음" 으로. #11 #12 와 함께 처리 |

---

## 1차 "인용불가로 제외" 6건 재판정 — 전부 **해결됨**

저장소 SKILL.md 사본 교체 + 이번 회차 보완으로 6건이 모두 해소되었다.

| 1차 항목 | 재판정 | 지금 파일의 원문 (SKILL.md 설치) |
|---|---|---|
| 1. `pip install xlrd` 부트스트랩 없음 | **해결됨** | 48행 `python3 -c "import xlrd" 2>/dev/null \|\| pip install xlrd --break-system-packages -q` |
| 2. 양쪽 반영 절차 없음 | **해결됨** | 192행 `이 경로는 **쓰기 가능하다.** 사용자에게 재업로드를 시키지 말고 직접 반영한다.` |
| 3. cycle 어긋남 WARN 설명 없음 | **해결됨** | 263행 `` `check_input.py` 는 **cycle 이 실제 수취 패턴과 어긋나는 거래처**도 WARN 으로 `` |
| 4. `unlisted_recommend_*` / `_print_reco()` 설명 없음 | **해결됨** | 260-261행 `` `build_report.py` 가 실행 끝에 같은 목록을 콘솔에도 찍어주므로 놓치지 않는다. `` / `` 기준(수취 월수·금액)은 `config` 의 `thresholds.unlisted_recommend_*` 에 있다. `` |
| 5. 1월 전년 12월 자동 포함 설명 없음 | **해결됨** | 74행 (#2 와 동일 원문) |
| 6. 등급 `거래 종료` 언급 없음 | **해결됨** | 164행 `` \| `거래 종료` \| `vendors.json` 에 `until` 로 등록됨 — 점검 대상 아님 \| 무시. 아직 거래 중인데 여기 뜨면 `until` 을 지운다 \| `` |

---

## 1차 "다음 점검에서 대조할 것" 4건 재판정

| 1차 항목 | 재판정 | 근거 |
|---|---|---|
| `짝이 기간 밖` 리터럴이 config 에 없고 코드 3파일에 흩어짐 | **미해결** | `build_report.py` · `common.py` · `validate.py`(2곳)에 리터럴 존재. `config/check-config.json` 에 해당 문자열 없음 |
| `check_input.py` 미수정 — 1월 전년 12월 자료 없으면 FAIL (의도된 동작) | **미해결(의도된 동작)** | 156행 `if v.get("until"):` 등 1차 이후 변경 없음. 픽스처에 2025-12 자료가 여전히 없어 "넣으면 통과" 경로는 이번에도 미실측 |
| 개선안 5건 미착수 | **미해결** | `sync.py` 에 `--install-skill` 없음 / `push.py` 에 `--add-vendor` 없음 / 실행 메타 파일 없음 / 테스트 함수 22개로 1차와 동일 |
| `audit/` 가 `GROUPS['code']` 에 없어 저장소에 안 올라감 | **해결됨** | `push.py` 88행 `GROUPS["code"] += _scan("tests") + _scan("audit")` |

> **1차의 전제 하나가 틀렸다.** 1차는 `audit/` 파일이 "컨테이너가 아니라 스킬
> 폴더라 사라지지는 않는다"고 적었으나, 실제로는 설치 경로에 남지 않아 사용자가
> 이 파일을 다시 업로드해야 했다. 설치 경로는 **쓰기는 되지만 세션 간 보존은
> 안 된다.** 이제 `audit/` 가 저장소에 올라가므로 `sync.py` 로 항상 복원된다.
> 앞으로 이 파일의 정본은 **저장소 `audit/last-audit.md`** 다.

---

## 이번 회차에 한 일

실행 결과 숫자를 바꾸는 수정은 없다. 문서 정확도와 push 범위만 손봤다.

| 무엇 | 파일 |
|---|---|
| 설치 SKILL.md 를 저장소 사본으로 교체 (259행 → 348행) | `SKILL.md`(설치) |
| 등급 6종 표 추가 — `거래 종료` 포함 | `SKILL.md` 양쪽 |
| 미문서 옵션 전부 반영: `sync.py --ref/--token`, `check_input.py --as-of`, `push.py --only/--message/--force/--skip-tests` | `SKILL.md` 양쪽 |
| `_fixtures()` → `_scan()` 일반화. `tests/` 전체 + `audit/` 를 디렉토리째 스캔 | `scripts/push.py` |
| 모듈 docstring 의 code 묶음 목록을 실제 `GROUPS` 와 일치시킴 | `scripts/push.py` |
| `run_tests()` 가 안내하던 숨김 옵션 `sync.py . --with-tests` → `sync.py .` | `scripts/push.py` |

### 실측 (2026-09-06 2차, fixtures 6개)

| | 1차 수정 후 기록 | **2차 실측** |
|---|---|---|
| 9/6 기본 실행 | 확인 필요 4 · 단발 1 · 해결 0 | 확인 필요 4 · 기한 전 6 · 단발 1 · 정상 3 · 해결 0 — 일치 |
| 총 건수 / 상계 | 441건 | 441건 · 매출분 제외 0 · 기간 밖 제외 0 · 상계 6쌍 — 일치 |
| 9/6 `validate` | FAIL 0 · PASS 17 | FAIL 0 · SKIP 0 · PASS 17 — 일치 |
| 1월 실행 `validate` | FAIL 0 · SKIP 4 | **FAIL 0 · SKIP 2** — 결론은 같으나 SKIP 수가 다름 |
| `test_edge_cases.py` | 실패 0 | 실패 0 (22개 함수) |

> 1월 실행 SKIP 은 `전액취소=0+노랑 검사` · `상계 매칭` 2건이다. 1차 기록의 4건은
> 재현되지 않았다. FAIL 0 이라는 결론이 같아 판정에는 영향이 없지만, **1차의
> 숫자 하나가 실물과 다르다.** 다음 점검에서 1차 실행 조건을 특정할 것.

### 반영 경로

- **설치 경로** — `SKILL.md` 덮어씀. 저장소본과 `diff` 무차이 확인
- **`push.py --code`** — `SKILL.md`(+42/−2), `scripts/push.py`(+21/−10) 2개.
  테스트 게이트 통과 후 업로드. codeload 재다운로드 후 `diff` 일치 확인
- **`audit/last-audit.md`** — 이번 파일. `_scan("audit")` 로 처음 저장소에 올라감

---

## 다음 점검에서 먼저 볼 것

1. **#25 를 #11 #12 와 묶어 처리** — 문서의 `deadline_day` 사본이 이제 3곳이다.
   같은 회차에 같은 실수를 반복했으므로, 개선안 #2(단일 출처 검사에 SKILL.md 추가)
   없이는 계속 늘어난다. 개선안 #2 의 우선순위를 올릴 것
2. **개선안 #1 (`sync.py --install-skill`)** — 설치 경로가 세션 간 보존되지
   않음이 이번에 실증됐다. 손 동기화 절차가 남아 있는 한 드리프트는 재발한다
3. **#5 (1월 유예 검사 무력화)** — 남아 있는 유일한 0건 매칭 PASS.
   1월 실행 실측에서 `'기한 전' 0건 (전월 유예 구간: False)` 로 PASS 되는 것을 재확인
4. **1월 실행 SKIP 4 vs 2** — 1차 기록과 2차 실측이 다른 유일한 숫자
