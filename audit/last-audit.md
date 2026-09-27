## 7차 검증·병합 기록 (2026-09-27)

> 검증 회차(별도 세션)는 브랜치 `fix-20260927`(`0500967`)을 실물로 대조했고, 이 절은 병합 회차가 적는다. 아래 "7차 수정 기록"·"7차 정기점검 진단 기준선" 절은 그대로 둔다.

- **검증 1 결과**: 재현 실패 **0** · 브랜치 `0500967` · 전문 `hometax-invoice-check_검증_2026-09-27.md`(사용자 폴더). 확인 범위: 수정 기록 항목 0~14 실물(파일·줄·원문) · 5개 실행(9/27 기본 · `--strict --no-state` · `--as-of 2026-01-05` · `2026-02-05` · `2026-09-06`) validate 요약·등급별·콘솔 `!` 줄·결과 집합 · 부록 파괴 실험 30회 + 등급 재산출 4회 전부 FAIL 유지 · dry-run 4케이스(네트워크 차단, config md5 불변, rc 0) · `--branch` 스텁 5시나리오(원격 미접촉, PUT 0) · 역검증 `t_dry_run_readonly`(가드 제거 시 FAIL, 복구 시 통과) · 의도 검증(B) 6건 + 부록 교체 전부 진단 의도와 맞음. **검증 2: 없음**(수정 회차 2 불필요).
- **병합**: 커밋 `90aceeadba841d7bee0ff5484cba8cf735d1de6d` · parents 2개(no-ff: `3780abd` + `0500967`) · 2026-09-27 14:43:14 KST (05:43:14Z) · 방법 GitHub Merges API(`POST /repos/…/merges`, base main ← head fix-20260927, 브랜치 push 가 아닌 서버 측 병합). 브랜치 `fix-20260927` 잔존(삭제 안 함). 병합 직전 `git ls-remote`: main `3780abd` · fix `0500967` 확인.
- **병합 후 재수령 대조**(`sync.py` main): 변경 9파일 md5 = 브랜치와 동일(push.py `6bec801b…` · validate.py `184d9796…` · build_report.py `2e45c213…` · check_input.py `46c9531e…` · SKILL.md `72a9a316…` · checklist.md `bf04a35d…` · last-audit.md `2de200ad…`(이 절 추가 전) · judgment-rules.md `66b12e9a…` · test_edge_cases.py `a5233ba6…`) / 불변: state `46f8542a…` · vendors.json `3f68fea6…` · check-config.json `cacd9692…` · install/SKILL.md `6f686b57…`.
- **병합된 main 재실행**(사본, state 백업·복구, 한 실행당 build_report 1회, 실행별 `--out`):

| 실행 | validate 요약 | 등급별 | `!` 줄 |
|---|---|---|---|
| tests/test_edge_cases.py | 26 t_ · 112 체크 · 실패 0 · exit 0 · 49s · state 불변 | | |
| 9/27 기본 | FAIL 0 · SKIP 1 · PASS 18 | 확인 필요 9 · 기한 전 0 · 단발 3 · 정상 6 · 해결 0 | 9 |
| `--strict --no-state` | FAIL 0 · SKIP 3 · PASS 16 | 9·0·3·6·0 | 9 |
| `--as-of 2026-01-05`(check_input FAIL 1 = fixtures 한계, 세 명령 따로) | FAIL 0 · SKIP 2 · PASS 17 | 0·0·0·0·해결 3 | 0 |
| `--as-of 2026-02-05` | FAIL 0 · SKIP 1 · PASS 18 | 0·0·0·0·해결 3 | 0 |
| `--as-of 2026-09-06` | FAIL 0 · SKIP 1 · PASS 18 | 확인 필요 3 · 기한 전 6 · 단발 1 · 정상 3 · 해결 0 | 3 |

  9/27 결과 집합: 튜플 22(확인 필요 9 · 단발 3 · 정상 6 · 거래 종료 4) · 월별 합 9개월 동일(1월 53,992,788 … 8월 63,848,349 · 9월 0) · state 순서 9곳 동일(2648135761 … 8693500721) = 수정 기록 "속도·효율" 절 값. 끝에 `__pycache__` 삭제.
- **부트스트랩 재업로드**: 불필요(`install/SKILL.md` 불변, md5 `6f686b57…`).
- **기록 보완(검증 §14)**: 부록 파괴 실험 표에 한 줄 — 매트릭스 셀 검사(월 컬럼 0개) 사본 요약 **18개**(`FAIL 4 · SKIP 1 · PASS 13`) — 새 검사 +1(진단 때 17).
- **이월 목록**: 개선안 3(state `flagged` biz_no 정렬) · 4(`state.run_date > as_of` 경고) · 5(FAIL 산출물 파일명) / S3(`audit/OPEN.md` 또는 last-audit 상단 요약 절 + view 범위) · S4(정상 회차 dry-run 관행) / "다음 점검에서 대조할 것" 11(Git Data API 단일 커밋) / 점검표 개정안 5·14후반(`tests/t_audit_static` · `tests/mutation_test.py` 이관) / 새로 본 것 2건(`push._scan` 이 `__pycache__`·`.pyc` 를 안 거름 → 다음 진단 회차 결함 후보 · `check_cycle` WARN 문구의 상호 빈칸) / 미실측 `check_resolved` 상태열만 N>0 실사용 대조(5회차째).
- **첫 실사용에서 볼 것(10월 초)**: 콘솔 `  ! ` 줄만으로 채팅 요약이 나오는지(즉석 openpyxl 0줄) / validate 요약 19개, '기한 전' 기대 = 시트 / 9월분 기한 2026-10-10 임박 문구 · 당월(10월) 열 생성(P8 [추론] 2건 실측) / `--branch` 없는 일반 push(state 만)가 main 으로 가는지 / 실 데이터 최종일 기록.
- **다음 회차 첫 확인**: main = 병합 커밋 `90aceeadba841d7bee0ff5484cba8cf735d1de6d`(+ 이 기록 커밋) · 브랜치 `fix-20260927` 잔존 · checklist.md 버전 줄 `v7 · 2026-09-27`.

---

# 7차 수정 기록 (2026-09-27 · 브랜치 `fix-20260927` · 진단과 같은 세션)

> 사용자 지시(프롬프트 ②)로 **결함 1~10 · 개선안 1·2 · 속도 S1·S2 · 점검표 개정안 1·2·4·6~16(3 폐기, 5·14후반 계획)** 을 고쳤다.
> 모든 변경은 브랜치 `fix-20260927` 에만 올렸고 **main 은 `3780abd`(7차 진단 1차 커밋) 그대로**다. main 병합은 검증 뒤 사용자가 한다.
> 검증용 수령 명령: `python3 sync.py --ref refs/heads/fix-20260927 /home/claude/hometax-fix`
> (부트스트랩이 받는 main 사본은 옛 코드다 — 검증 대상은 이 브랜치.)
> 이월(사용자 결정): 개선안 3(state biz_no 정렬) · 4(state run_date > as_of 경고) · 5(FAIL 산출물 파일명) · S3(OPEN.md) · S4(dry-run 관행) · "다음 점검에서 대조할 것" 11(파일별 커밋).
> 아래 "7차 정기점검 진단 기준선" 절은 진단 시점 그대로 보존한다(수정으로 달라진 숫자는 이 절에 적는다).

## 원래 제안·지시를 바꾼 곳과 이유

| 항목 | 지시·진단 제안 | 실제 구현 | 이유 |
|---|---|---|---|
| 결함 #6 | 114-116·157-159 만 SKIP 기록, 실측 "요약 18개" | 그 두 함수는 지시대로 SKIP 기록. 정상 실행의 검사 개수가 새 검사(등급 재산출 대조)로 **19** 가 됐으므로 헤더 미검출 요약도 **19** 로 맞췄다 | 처음엔 `check_matrix_months` 에도 '매트릭스 월 컬럼' SKIP 을 넣어 20 이 됐다(정상 19 보다 하나 많음). 되돌려 `매트릭스 헤더` FAIL 이 그 검사 자리를 대신하게 두었다 — 원칙은 "정상 실행과 같은 개수" 다 |
| 결함 #1 · 개선안 1 | `check_grace` 의 `n == 0` 신호를 기대 건수 정확 일치로, 색 칸 신호는 "보조 유지", january 분기는 "가능하면 제거" | 기대 건수 정확 일치 + **색 칸도 정확 일치**(facts 에서 직전 달이 `grace` 상태인 행 수 == 매트릭스 유예 색 칸 수). january 분기 제거 | "0 이면 FAIL" 류의 임계 신호를 하나라도 남기면 같은 유형의 오탐이 다른 달에 재발한다. 두 신호 모두 기대값 비교로 바꾸면 월 특례가 필요 없다 |
| 결함 #2 | push.py 331 문구 **삭제** | `"이름·주기는 최신 산출물의 대상외 목록에서 가져온다. "` 를 삭제하고 그 자리에 `"상호는 다음 리포트에서 자료로 채워지고, cycle 은 --cycle. "` 을 넣었다 | help 에 상호·cycle 이 어디서 오는지 한 줄은 있어야 `--cycle` 의 존재를 알 수 있다 |
| 개선안 2 | `push.remote`·`push.put` 스텁 | `remote`·`put`·**`api`** 세 개 스텁(api 는 호출되면 AssertionError) | dry-run 경로가 `api` 를 직접 부르는 회귀까지 잡기 위해 |
| 점검표 개정안 12 | 3행·244-247행 2회 커밋 규칙 | 247행 첫 문장 "둘 중 하나만 올리면…" 은 삭제하고 앞 문단 끝에 "커밋은 두 번, 파일은 둘 다" 로 흡수 | 같은 뜻을 두 번 적지 않기 위해 |
| 점검표 개정안 1 | 11행 정정 뒤 머리말 5-11행 삭제 | 삭제(원문은 아래 "점검표에서 옮긴 기록") | 지시대로. 정정("3~8번")은 이 파일에만 남긴다 |
| 부록 스크립트 | (지시: 파괴 실험 전부 재실행, 부록 갱신) | 부록을 7차 수정 후 버전(등급 재산출 파괴 3건 추가)으로 교체 | 다음 회차가 새 검사까지 재현하게 |

## 항목별 수정 기록 (절·함수명 기준)

| # | 파일 · 위치 | 무엇을 | 실측 |
|---|---|---|---|
| 0 | `scripts/push.py` — 모듈 상수 `BRANCH = "main"`(기본값 유지) · `REPO_API` 신설 · `remote(path, token, branch=None)` · `put(..., branch=None)` · **`branch_sha()` · `ensure_branch()` 신설** · `main()` `--branch` 옵션, `ref = ensure_branch(branch, a.token, a.dry_run)` → 비교는 `ref`, 업로드는 `branch` · 독스트링 사용법 · SKILL.md 7단계 옵션 표 `--branch` 1행 | 브랜치가 없으면 `GET git/ref/heads/main` sha 로 `POST git/refs` 생성, 실패·조회 불가 시 `[중단] 브랜치 … 생성 실패 — <응답 코드 메시지>`. dry-run 은 생성 없이 "브랜치 fix-20260927 없음 — 실제 실행 시 main 에서 생성합니다. 아래 비교는 main 대비입니다" 출력. GROUPS·테스트 게이트·state 가드 무변경 | `--only code --branch fix-20260927 --dry-run` 목록 = 변경 파일 9개(아래) → 실제 push 로 브랜치 생성·업로드 → `git ls-remote` main `3780abd` 불변 + `refs/heads/fix-20260927` 존재 → `sync.py --ref refs/heads/fix-20260927` 수령본 push.py md5 = 로컬(채팅 보고에 해시) |
| 1 | `scripts/validate.py` — **`check_grade_recompute()` 신설**(`check_grades` 뒤) · `check_grace(wb, cfg, as_of, facts, rows)` 재작성 · `main()` 에서 `facts, _ = build_facts(df, vendors, as_of, cfg)` / `rows = grade_all(facts, as_of, cfg)` 를 한 번 만들어 두 검사에 전달 · `SHEET_CHECKS` 에 "등급 재산출 대조" · import `Counter`, `build_facts, grade_all, _labels` | 기대 `(공급자번호, 등급, 결번월 표기)` **다중집합**(Counter) vs 시트의 '해결' 제외 행. 누락 → FAIL, 초과·불일치 → FAIL, 0=0 → PASS "(기대 0 · 시트 0)". 독스트링에 "같은 함수를 쓰므로 판정 논리 오류는 tests 몫" 기록. `check_grace`: '기한 전' 시트 건수 == 기대 건수, 매트릭스 직전 달 열 유예 색 칸 == facts grace 칸, 월 특례 없음 | 9/27 기본 `FAIL 0 · SKIP 1 · PASS 18` · `--strict --no-state` `FAIL 0 · SKIP 3 · PASS 16` · `--as-of 2026-01-05` `FAIL 0 · SKIP 2 · PASS 17`(등급 재산출 "기대 0 · 시트 0") · **`--as-of 2026-02-05` `FAIL 0 · SKIP 1 · PASS 18`**(진단 때 FAIL 1). 파괴: 미수취목록 첫 행 삭제 FAIL / 첫 행 복제 FAIL / '정상'→'단발·비정기' 교체 FAIL / 9/6 산출물 '기한 전'→'정상' **FAIL 유지** / 1월 전년 12월 열 유예 색 제거 **FAIL 유지**(`유예 색 0칸 vs 기대 29칸`) |
| 2 | `scripts/build_report.py` `_one()` `"name": v["name"] or (str(g["상호"].iloc[-1]) if len(g) else "")` · `scripts/push.py` `edit_vendor_lists()` 콘솔 문구 "다음 리포트에서 자료의 상호로 채워집니다(고정 표기를 쓰려면 vendors.json 에 직접 적으세요)" · argparse help 교체 · `SKILL.md` 243행 같은 표현으로 통일 | | vendors 사본에 `name: ""` 212-04-59010 → 매트릭스 `['212-04-59010', '유성빌딩', …]` · 미수취목록 `[…, '212-04-59010', '유성빌딩', …]` · state `name: '유성빌딩'` 셋 다 자료 상호. grep `대상외 목록에서 가져온다` 0건, `자료에서 채워`·`자료의 상호로 채워` 남은 곳 SKILL.md 248 · push.py 322 두 곳 — 둘 다 이제 참 |
| 3 | `scripts/push.py` `edit_vendor_lists()` add 루프에 `if not biz_checksum_ok(sid): 건너뜀 … 사업자번호 체크섬 오류` · import `biz_checksum_ok` | | `--add-vendor 999-99-99999 --dry-run` → `건너뜀  999-99-99999 — 사업자번호 체크섬 오류` / `[중단] 추가된 거래처가 없습니다.` |
| 4 | `scripts/validate.py` `check_config_single_source()` (b-5) 코드 패턴에 `re.search(rf'\.title\s*=\s*["\']{v}["\']', src)` | | `ws.title = "매트릭스"` 사본 → `[FAIL] 단일 출처 위반 1곳` (진단 때 PASS) · 원본 PASS(오탐 0). 파괴 실험 표에 행 상시화 |
| 5 | `references/judgment-rules.md` 86행 · `SKILL.md` 169행 | "`until` 이 **지난** 곳(실행월 이전). 미래 `until` 은 아직 거래 중 — 결번 판정을 그대로 받는다" | grep `` `until` 등록됨 `` · `` `until` 로 등록됨 `` → SKILL.md·README·install·references **0건**(audit/ 의 인용문은 제외 대상) |
| 6 | `scripts/validate.py` `check_matrix_blank_and_fill()` `if not r:` → `rec(SKIP, "미수취=공란 검사"…)` + `rec(SKIP, "전액취소=0+노랑 검사"…)` · `check_vendor_coverage()` `if not r:` → `rec(SKIP, "점검 대상 누락 검사"…)` · `check_grades()` PASS 문구를 `mrow` 유무로 분리 · `check_matrix_months()` 의 `매트릭스 헤더` FAIL 이 월 컬럼 자리를 대신함(주석) | | 매트릭스 헤더 `공급자 번호` 사본: 요약 **19개**(= 정상 19) `FAIL 4 · SKIP 4 · PASS 11`. 등급 분류 문구 `등급값·정렬 정상 · 결번 표기 미확인(매트릭스 헤더 미검출)` |
| 7 | `scripts/push.py` `edit_vendor_lists()` ignore 루프 앞에 `listed = {norm_biz(v["biz_no"]) …}` 읽고 `if sid in listed: 건너뜀 … 아직 vendors.json 에 등록돼 있습니다. 먼저 지우세요` | | `--ignore-vendor 869-35-00721 --dry-run` → 그 문구 / `[중단] 제외 목록에 추가된 항목이 없습니다.` |
| 8 | `scripts/push.py` argparse help `--ignore-vendor 와 같이 쓸 수 없다.` | | grep `--ignore 와` 0건 |
| 9 | `SKILL.md` "저장소 구성" `audit/checklist.md         정기 점검표 정본 (점검 회차만 읽는다)` 1행 | | 424행에 존재 |
| 10 | `scripts/check_input.py` `check_vendors()` `vmap = {norm_biz(v["biz_no"]): v …}` · `scripts/push.py` `edit_vendor_lists()` `have = {norm_biz(v["biz_no"]) …}` · import `norm_biz` | | 제이푸드 구 번호 `"559-96-01523"` 사본에서 `[OK  ] 사업자번호 변경 처리 완료 1건`, WARN 재발 없음 |
| 11 | `tests/test_edge_cases.py` **`t_dry_run_readonly()` 신설**(`t_no_upload_files` 뒤, main 목록 등록) — sandbox 사본의 `push.py` 를 `importlib` 로 읽어 `remote`·`put`·`api` 스텁, `--add-vendor 2120459010 --dry-run` / `--add-vendor 999-99-99999 --dry-run` / `--ignore-vendor 8693500721 --dry-run` 실행 | 단언: `config/` md5 동일 · `put 0회 · remote 0회 · api 0회` · '추가 예정'+exit 0 · '체크섬 오류' · '등록돼 있습니다' | 5건 전부 ok. 테스트 총 **26 t_ · 개별 체크 112 · 실패 0 · 54s** |
| 12 | `scripts/build_report.py` `main()` `_print_deadline` 호출 직전 S1 4줄(진단 실험 원문 그대로) · `tests` `t_run_variants` 에 `콘솔 '!' 줄 수 == 확인 필요 건수` 단언 | | 9/6 경로 `3줄 vs 3건` ok. 9/27 콘솔 9줄. 결과 집합 = 진단 기준선(아래 표) |
| 13 | `SKILL.md` 3단계 코드 블록을 `&&` 한 줄로(`U=`·`O=` 변수, 실행별 `--out` 권장 주석), 4단계·5단계 코드 블록 3개는 "3단계 한 줄의 두 번째·세 번째 항" 문장으로, `--as-of`·`--strict` 세 곳 동시 지정 명시. 코드 변경 0 | | `<생성된파일>` grep 0건. 코드펜스 짝수 |
| 14 | `audit/checklist.md` **v7** — 개정안 1(버전 줄·머리말 후속 조치 문단 삭제) · 2(범위 밖) · 4(실행별 --out) · 6(검사 고유명 기준, 7차 19+2) · 7(D 항목 교체) · 8(A 옵션 4개 + B `ignore_suppliers`) · 9(0단계 (2) 후속 조치 문장 대조) · 10(F 02-05) · 11(H 축소) · 12(머리말·마무리 2회 커밋) · 13(`[의도된 동작]` 10건 · `[되돌리면 안 되는 것]` 15행 · skill-audit ②③ 한 줄) · 14(효율 기준선 표 상시 + 기준선 형식) · 15(4줄 삭제 → 프롬프트 ①) · 16([운영 조건] 읽는 파일·분량) · 5·14후반 "계획(다음 회차)" · 3 폐기(미기재) | 281 → 306행 | grep `같은 push 로` · `같은 push.py --code 로` · `None과 빈 문자열` · `버전: 6차` · `1·3~8번` · `붙여넣을 4줄` 전부 **0건** |

변경 파일(원본 `3780abd` 대비 diff -rq): `SKILL.md` · `references/judgment-rules.md` · `scripts/build_report.py` · `scripts/check_input.py` · `scripts/push.py` · `scripts/validate.py` · `tests/test_edge_cases.py` + `audit/last-audit.md` · `audit/checklist.md` = **9개**. `state/last-run.json`·`config/vendors.json`·`config/check-config.json`·fixtures·`install/SKILL.md`·`README.md`·`sync.py`·`common.py` 무변경(state 는 매 실행 뒤 복구, md5 `46f8542a…` 원격과 동일).

문법: `py_compile` common·check_input·build_report·validate·push·sync·test_edge_cases 7개 OK. 코드펜스 짝수(SKILL·README·install·references 3·checklist·last-audit). UTF-8 OK.

## 속도·효율 — 전/후 (기준선 표와 같은 열)

| 실행 이름 | 전(A, 진단) | 후(B, 수정) | 결과 집합 |
|---|---|---|---|
| base_today | 3.10s · 도구 호출 3 · 즉석 코드 0 (+요약용 openpyxl 11줄·1회) · `FAIL 0 · SKIP 1 · PASS 17` | 3.46s(검사 +1) · **한 줄 실행 1회 · 즉석 코드 0** · `FAIL 0 · SKIP 1 · PASS 18` | 튜플 22/22 동일 · 월별 합 동일 · state 순서 9곳 동일 |
| strict_nostate | 3.10s · `FAIL 0 · SKIP 3 · PASS 15` | 3.49s · `FAIL 0 · SKIP 3 · PASS 16` | 동일 |
| asof_0105 | 2.22s · `FAIL 0 · SKIP 2 · PASS 16` | 2.27s · `FAIL 0 · SKIP 2 · PASS 17` | 튜플 3/3 동일 |
| asof_0205 | 2.35s · **`FAIL 1` · SKIP 1 · PASS 16** | 2.34s · **`FAIL 0` · SKIP 1 · PASS 18** | 튜플 3/3 동일 |
| tests | 49.9s · 25 t_ · 106 체크 | 54s · 26 t_ · 112 체크 · 실패 0 | |

진단 기준선 값(컨테이너 `base7/baseline7.json` 에서 옮겨 적음): base_today 튜플 22 = 확인 필요 9 · 단발 3 · 정상 6 · 거래 종료 4 / 월별 합 1월 53,992,788 · 2월 70,700,362 · 3월 47,403,992 · 4월 49,796,017 · 5월 44,242,599 · 6월 52,723,343 · 7월 101,251,737 · 8월 63,848,349 · 9월 0 / state 순서 2648135761 · 8948802963 · 7328801079 · 7248501096 · 1198687135 · 4029701369 · 3061253427 · 2148796237 · 8693500721. 수정 후 전부 동일.
validate 요약이 +1 PASS 인 것은 새 검사 "등급 재산출 대조" 때문이다(정상 요약 18 → **19**).

## 파괴 실험 재실행 (수정 후 · 고유 검사명 19 + 실패 경로 전용 2)

진단 회차 표의 30회 전부 재실행 + 등급 재산출 대조 4회. 결과: **파괴 시 FAIL 전부 유지**, 달라진 곳은 아래뿐.

| 검사 · 파괴 방법 | 진단 때 | 수정 후 |
|---|---|---|
| 단일 출처 (b-5) `ws.title = "매트릭스"` | PASS(범위 밖) | **FAIL** `단일 출처 위반 1곳` |
| 매트릭스 헤더 미검출 사본 요약 | 15개 | **19개**(SKIP: 미수취=공란·전액취소·점검 대상 누락) |
| 시트 구성 FAIL 시 요약 | `FAIL 1 · SKIP 14 · PASS 3` | `FAIL 1 · SKIP 15 · PASS 3`(등급 재산출 대조 포함) |
| 등급 재산출 대조 — 첫 데이터 행 삭제 / 첫 행 복제 / '정상'→'단발·비정기' | (검사 없음) | FAIL / FAIL / FAIL |
| 등급 재산출 대조 — 1월 산출물 무변경 | | PASS "기대 0 · 시트 0" |
| 발급기한 유예 — 9/6 '기한 전'→'정상' / 1월 유예 색 제거 | FAIL / FAIL | FAIL(`시트 0건 vs 기대 6건`) / FAIL(`유예 색 0칸 vs 기대 29칸`) |
| 발급기한 유예 — 9/27 무변경 | PASS(expect=False 비활성) | PASS(`'기한 전' 0건 = 기대 · 유예 색 0칸 = 기대`) — 이제 비활성 구간 없음 |

## 점검표에서 옮긴 기록 (checklist.md v6 머리말 5-11행 원문 — 개정안 1)

```
**후속 조치(2026-09-07 저녁)**: 결함 #5·#20·#28·#29·#30·N4·N6·#14·#16·#19·#21·#27 과
개선안 1·2·3·5 처리됨. validate 검사가 늘었으니 파괴 실험 목록을 다시 뽑을 것.
#15 · #18 · 개선안 4 도 같은 날 심야에 종결. **6차 미해결 0건.**
`push.py` 에 `--add-vendor` / `--ignore-vendor` 가 생겼으니 A 항목 옵션 목록에 포함해 확인할 것.

**반영 상태**: 6차 개정안 12건 중 **2·9·10·11·12번 반영 완료** (대상 파일 목록에 checklist.md · --as-of 연도와 state 백업 · 토큰 선요청 · 마무리 순서 push 우선 · 실 데이터 판정 기준).
1·3~8번과 #18·#28 방향은 사용자 채택 대기 중이며 아직 반영하지 않았다.
```
정정: 1번(`--as-of` 연도)도 6차 사후에 이미 반영돼 있었다(F 항목). 즉 v6.1 = 1·2·9·10·11·12 반영, 3~8 대기 → 7차에서 2·4·6·7·8 채택, 3 폐기, 5 계획.

## 점검표 갱신 이력 (checklist.md)

- 6차 2026-09-07 — 첫 이관. 사후에 1·2·9·10·11·12 반영(버전 줄은 "6차" 그대로였음).
- **7차 2026-09-27 — v7.** 개정안 1·2·4·6~16 반영(14 는 효율 표 상시화만), 3 폐기, 5·14후반 "계획(다음 회차)". 281 → 306행. 2차 커밋(브랜치 `fix-20260927`).

## 검증 회차가 볼 것 (재현 목록)

브랜치 수령: `python3 sync.py --ref refs/heads/fix-20260927 /home/claude/hometax-fix`. 기준값: main `3780abd` 불변 · 변경 파일 9개 · 테스트 26 t_ / 112 체크 · validate 정상 요약 19(실패 경로 전용 2 = 21).
1. 위 항목별 표의 실측 전부(0~14). 특히 `--as-of 2026-02-05` FAIL 0, 9/6 산출물 '기한 전'→'정상' FAIL, 1월 유예 색 제거 FAIL, 미수취목록 행 복제 FAIL, `ws.title` 사본 FAIL, 매트릭스 헤더 미검출 요약 19개.
2. `tests/test_edge_cases.py` 전체 통과(26 t_ · 112 체크) · `py_compile` 7개 · 코드펜스 짝수 · UTF-8.
3. 옛 문구 grep 0건: `` `until` 등록됨 `` · `` `until` 로 등록됨 `` · `대상외 목록에서 가져온다` · `--ignore 와` · `<생성된파일>` (SKILL·README·install·references·scripts·tests) / checklist: `같은 push 로` · `같은 push.py --code 로` · `None과 빈 문자열` · `버전: 6차` · `1·3~8번`.
4. `--branch`: `--only code --branch fix-20260927 --dry-run` 이 "변경 없음"(브랜치와 동일) · 존재하지 않는 브랜치 이름으로 `--dry-run` 하면 "브랜치 … 없음 — 실제 실행 시 main 에서 생성" 문구와 main 대비 비교 · main HEAD 불변.
5. 결과 집합: 9/27 기본 실행의 미수취목록 튜플 22 · 월별 합 · state 순서가 위 "속도·효율" 절의 값과 같은지(state 는 백업·복구).
6. 의도 검증(B): 위 "원래 제안·지시를 바꾼 곳" 6건이 진단의 의도와 맞는지 한 줄씩.

## 이번 회차에 새로 본 것 (다음 회차 후보 — 고치지 않았다)

- `push.py` `_scan()` 이 `__pycache__/*.pyc` 를 거르지 않는다(숨김 파일만 제외). `py_compile`·테스트 실행 뒤 `tests/__pycache__/` 가 생기면 `--code` 에 딸려 올라간다. 이번 회차는 push 전에 `find . -name __pycache__ -exec rm -rf` 로 지웠다. `.gitignore` 의 `__pycache__/`·`*.pyc` 를 `_scan` 이 존중하게 하는 것이 결함 후보(다음 진단 회차에 인용과 함께).
- `check_input.check_cycle` 의 WARN 문구는 `v['name']` 을 쓰므로 `--add-vendor` 직후 첫 check_input 에서는 상호가 빈칸이다(리포트·state 는 #2 로 채워짐). 낮음.

## 실사용에서 볼 것 (main 병합 뒤 첫 실행)

- 콘솔 `  ! ` 줄이 채팅 요약 표의 원천이 됐다 — openpyxl 즉석 코드 없이 요약이 나오는지.
- validate 요약이 19개(`등급 재산출 대조` 포함)인지, 10월 초 실행에서 '기한 전' 기대 건수와 시트 건수가 같은지(첫 실자료 검증).
- `--branch` 없는 일반 push(state 만)가 종전과 같이 main 에 올라가는지.

---

# 7차 정기점검 진단 기준선 (2026-09-27 — 진단 시점 원문)

> **7차 정기점검 (2026-09-27) — 진단만.** 고친 것 없음. 이 절이 최신 기준선이고, 6차 기록은
> 아래 "이전 기록" 에 원문 그대로 보존한다. 채택 후 수정 회차는 브랜치 `fix-20260927`(예정) 에서.
> 이번 회차는 **한 세션이 도구 호출 한도로 두 번에 걸쳐** 진행했다(1차: 0~3단계 실측 → 채팅 중간보고,
> 2차: 나머지 실측·이 파일·push). 컨테이너 산출물(`/home/claude/out7`, `/home/claude/base7`)은 그대로였다.

점검일: 2026-09-27 (7차 — 정기점검, 진단 회차)
직전: 2026-09-07 6차(진단 커밋 `0d911fa`, 후속 4차까지 `b2fc5de`) + 2026-09-20 실사용 1회(`7a99a0f`, state 만 갱신)

**재확인 결과: 해결됨 28건 / 미해결 6건(미실측 1 포함) / 근거없음 0건 / 신규 결함 10건**
결함 10건(신규 8 + 이월 메모에서 승격 2) / 개선안 5건 / 속도·효율 후보 5건(합격 2·사용자 결정 2·후보 아님 1) / 인용불가로 제외 0건

> HEAD `7a99a0f` = 지시와 일치. `b2fc5de→7a99a0f` diff 는 `state/last-run.json` 1파일(+7/−7, 같은 3곳
> 순서만 변경). 6차 후속이 "수정함" 으로 적은 항목 중 미해결로 나온 것 **0건**.

## 이번 회차 실측 조건

| | 값 |
|---|---|
| 받은 커밋 | `7a99a0f` (2026-09-20 11:48 KST) "update: state/last-run.json". codeload tarball 과 `git clone` 트리 동일(diff -r 차이 0). 총 102커밋 |
| 실 데이터 | **업로드 없음 — fixtures 만 사용.** fixtures = 사용자 실제 다운로드본(2026-01-01~08-31, 441건, 공급자 51곳). 최종일이 오늘(09-27)로부터 27일 전 → 점검표 판정표 "전월까지만" → 당월(9월) 열 생성·9월분 기한(10/10) 임박 판정 2건만 **[추론]**. 그 밖은 실측 |
| 실행한 `--as-of` | 없음(오늘 2026-09-27) / `--strict --no-state` / `2026-01-05` / `2026-02-05`(신규, check_grace 2월 경로) / 파괴 실험용 `2026-09-06` |
| 파일 행수 | SKILL.md 420 · install/SKILL.md 55 · README.md 64 · sync.py 126 · check-config.json 113 · vendors.json 191(30곳) · column-mapping.md 103 · excel-format.md 75 · judgment-rules.md 140 · common.py 374 · check_input.py 273 · build_report.py 666 · validate.py 809 · push.py 426 · last-run.json 25 · test_edge_cases.py 673(t_ 25개 · 개별 체크 106) · checklist.md 281 · last-audit.md 804(직전) · .gitignore 9 |
| ls 대조 | 점검표 "대상 파일 전체" 목록 + `audit/checklist.md` + `.gitignore` = 실물 27파일. push GROUPS 24 + 저장소 25(= 24 + `.gitignore`) → 누락 0 · 유령 0 |
| md5 | 설치본 `c732414e88931f0ec219b51e292e5d15` ↔ `install/SKILL.md` `6f686b5721644381382be801a939c92d` — diff 는 끝 개행 1자만. 설치본에 절차·옵션·등급명 grep 0건 ✓ · 저장소 SKILL.md `a68c2449…` · state `46f8542a…`(원격과 동일, 매 실행 뒤 복구 확인) · vendors `3f68fea6…` · config `cacd9692…` |
| 컨테이너 | 옛 잔존물 없음(`/home/claude` 빈 상태에서 시작). 실험은 전부 `/home/claude/exp_*` 사본, 산출물은 `/home/claude/out7/<실행이름>/` |
| 부작용 | 저장소 폴더 SKILL.md·scripts·references·config·vendors·fixtures 무변경. 이번 push 는 `audit/last-audit.md` 1파일 |

## 1. 기준선 표 (현재 코드 그대로, 실험보다 먼저)

명령은 전부 `cd /home/claude/hometax` 에서. state 는 첫 실행 전 `/home/claude/base7/last-run.backup.json` 으로 백업, 매 실행 뒤 복구(md5 `46f8542a…` 동일 확인).

| 실행 이름 | 명령 | 벽시계(초) | 도구 호출 | 즉석 코드 줄 | check_input | build_report | validate |
|---|---|---|---|---|---|---|---|
| base_today | `check_input.py tests/fixtures` → `build_report.py --uploads tests/fixtures --out out7/base_today` → `validate.py <xlsx> --uploads tests/fixtures` | 0.47 / 1.52 / 1.10 = **3.10** | 3 | 0 | FAIL 0 · WARN 0 · 441건 · 51곳 · 체크섬 30/30 · 사업자번호 변경 처리 완료 1 | 확인 필요 **9** · 기한 전 0 · 단발 3 · 정상 6 · 거래 종료 4 · 해결 0 · 상계 6쌍 · 매출분 제외 0 · 기간 밖 0 · 점검대상 30 / 대상외 21 · 기한 임박 문구 **없음**(8월분 기한 9/10 경과, 9월은 당월) · 추가 권장 0 | FAIL 0 · SKIP 1(해결 집계) · PASS 17 |
| strict_nostate | 위 + `--strict --no-state` (validate 에도 `--strict`) | 0.46 / 1.51 / 1.12 = 3.10 | 3 | 0 | 동일 | **동일**(9·0·3·6) — 8월 기한 경과라 auto 와 strict 가 같은 시점 | FAIL 0 · SKIP 3(이력·해결·유예) · PASS 15 |
| asof_0105 | `--as-of 2026-01-05` 3곳 모두 | 0.47 / 0.87 / 0.89 = 2.22 | 3 | 0 | **FAIL 1**(전년 12월 데이터가 통째로 없음 — fixtures 한계) · WARN 1(기간 밖 7개월) | 대상 월 전년 12월~1월 · 5건 · 확인 필요 0 · 해결 **3**(state 가 미래 9/20 이라 직전 3곳이 해결로) · 임박 "전년 12월분 기한 2026-01-10 (D-5) · 27곳" | FAIL 0 · SKIP 2(전액취소·상계) · PASS 16 · 유예 검사 `색 29칸` PASS |
| asof_0205 | `--as-of 2026-02-05` 3곳 모두 | 0.46 / 0.98 / 0.91 = 2.35 | 3 | 0 | FAIL 0 · WARN 1(기간 밖 6개월) | 대상 월 1월~2월 · 69건 · 확인 필요 0 · 기한 전 **0** · 해결 3 · 임박 "1월분 기한 2026-02-10 (D-5) · 3곳" | **FAIL 1(발급기한 유예)** · SKIP 1 · PASS 16 — 결함 #1 |
| tests | `tests/test_edge_cases.py` | 49.9 | 1 | 0 | — | — | 25 t_ · 개별 체크 106 · 실패 0 · exit 0 · state 불변 |

결과 집합(미수취목록 `(공급자번호, 결번월, 등급, 상태)` 튜플 집합 22개 + 매트릭스 월별 합 + validate 요약 + state 순서 + xlsx md5)은 `/home/claude/base7/baseline7.json` (컨테이너 한정). 핵심만 옮겨 적는다:

- base_today 확인 필요 9: 광개토(5·7·8월, 계속) · 세종네트웍스(8월, 신규) · 예스코(8월, 신규) · 세무법인 신아(8월, 신규) · 바로고(8월, 신규) · 성우축산(8월, 신규) · 신앙촌상회(8월, 신규) · 비앤지(2월, 계속) · 다연유통(2·4월, 계속). 단발 3: 서바이빙·플리드·인투 란. 정상 6: 세스코·보문하우스·케이티·청호나이스·한전·제이푸드(신). 거래 종료 4: 제이푸드(구)·디패스·코원·팩프렌즈
- 매트릭스 월별 합(원): 1월 53,992,788 · 2월 70,700,362 · 3월 47,403,992 · 4월 49,796,017 · 5월 44,242,599 · 6월 52,723,343 · 7월 101,251,737 · 8월 63,848,349 · 9월 0 (총 483,959,187 = 원본 합 일치)
- 9/27 state 순서(9곳): 광개토 · 세종 · 예스코 · 신아 · 바로고 · 성우 · 신앙촌 · 비앤지 · 다연 = **최종수취일 오름차순** (P6 참조)
- 산출물 직접 확인: 시트 4개 · 매트릭스 헤더 5행(4행 신고기 밴드 1기×6/2기×3) · 1~9월 9열 · 9월 열 전 칸 유예 색 · A1 `(2026-01-01 ~ 2026-09-27)` · 1월 산출물 A1 `(2025-12-01 ~ 2026-01-05)` 헤더 `전년 12월 / 1월` 밴드 `2기 / 1기` ✓ (6차 #20 해결 유지)

### 실사용 1회(SKILL.md 1~7단계)의 도구 호출·즉석 코드 [실측 + 추론]

| 단계 | 현재(A) 도구 호출 | 즉석 코드 | 근거 |
|---|---|---|---|
| 1 저장소 받기 + 설명서·기준선 읽기 | bash 1 + view **7~8** | 0 | [실측] SKILL.md 23,099자(view 16,000자 절단 → 2회) · last-audit.md 83,115자(→ 5~6회). 부트스트랩 36-43행 "함께 읽는다" |
| 2 업로드 확인 | view 1 | 0 | |
| 3·4·5 검증·생성·검증 | bash 3 | 0 | 파일명은 build_report 의 `저장:` 줄에서 |
| 6 결과 전달(확인 필요 표) | bash 1 + present_files 1 | **11** | [실측] 콘솔에는 건수만 있고 행(상호·결번월·상태·최종수취일)이 없어 openpyxl 로 미수취목록을 읽어야 한다(아래 S1 의 A 스니펫 11줄) |
| 7 저장소 반영 | bash 1~2 (dry-run 관행 시 2) | 0 | |
| **합계** | **15~17** | **11** | |

## 직전 기준선 판정 (34건)

### "다음 점검에서 대조할 것" 0~8

| # | 판정 | 근거(지금 원문) |
|---|---|---|
| 0 업로드 최종일 먼저 | **준수** | 업로드 없음 → fixtures 사용, 최종일 08-31(27일 전)로 판정. md5 근거로 "실 데이터 아님" 이라 쓰지 않음 |
| 1 개정안 1~11 채택분 반영 + 버전 줄 | **미해결(기록 정정 후보)** | `checklist.md` 3 `버전: 6차 정기점검 · 2026-09-07` 인데 10 `**반영 상태**: 6차 개정안 12건 중 **2·9·10·11·12번 반영 완료**` (v6.1 취지). 또 1번(`--as-of` 연도)은 175 `실측할 것: \`--as-of <데이터 연도>-01-05\` (현재 자료 기준 2026-01-05)` 로 **이미 반영돼 있는데** 11행은 "1·3~8번 … 아직 반영하지 않았다" → 기록 오류. 3~8 은 미반영 맞음 |
| 2 #5 #20 (1월) | **해결됨** [실측] | `validate.py` 536-538 `ms = month_range(as_of)` / `py, pm = ms[-2] …` / `expect = is_in_grace(py, pm, as_of, cfg)` · `build_report.py` 356-357 `_y0, _m0 = months[0]` / `ws["A1"] = f"… ({_y0}-{_m0:02d}-01 ~ {as_of})"` — 1월 산출물 A1 `2025-12-01 ~ 2026-01-05`, 유예 색 55칸 제거 시 FAIL(파괴 실험 표) |
| 3 커플링 개선안1 ↔ #14 #15 N4 | **해결됨** [실측] | `validate.py` 697-731 (b-5)(b-6)(b-7) 존재 · `excel-format.md` 15-18 `\| 1 \| \`sheets.matrix\` \|` · `column-mapping.md` 5 `**코드가 읽는 값의 출처는 \`config/check-config.json\` 의 \`input\` 블록 하나다.**` · `judgment-rules.md` 46 `익월의 \`grace.deadline_day\`` — 단일 출처 검사 PASS(스크립트 5 · 문서 6) |
| 4 커플링 #29 가안 + 개선안 4 | **해결됨** [실측] | `build_report.py` 132-133 `if f["ended"]:` / `continue` · 161-164 C 루프 `if f["ended"]: rows.append(_row("C. 거래 종료", …` · `check-config.json` `"ignore_suppliers": ["2120459010"]` · `push.py` 329-337 `--add-vendor / --ignore-vendor / --cycle`. 9/27 콘솔·시트에 유성빌딩 추가 권장 없음(추가 권장 0곳) |
| 5 check_resolved 실사용 대조 | **미실측(이월 4회차째)** | fixtures 9/27 해결 0 → `[SKIP] 해결 집계`. 1월·2월 재현에서 해결 3 은 **등급열 3 · 상태열만 0** 경로. `상태열만 N>0` 은 `t_resolved_status` 의 sandbox 에서만 밟힘 |
| 6 #18 #28 방향 | **해결됨** [실측] | #18: `check_input.py` 160 `if until_passed(v.get("until"), as_of):   # build_report 와 같은 기준(common)` · #28 다안: `SKILL.md` 321 `### \`비정기\` 라벨의 범위 — 등급이 안 바뀌어도 정상이다`, `judgment-rules.md` 88 `### cycle 라벨은 A 경로를 면제하지 않는다` |
| 7 checklist.md push·check_paths | **해결됨** [실측] | 첫 ls 에 `audit/checklist.md` 존재 · `validate.py` 597 `"audit/last-audit.md", "audit/checklist.md",` · 9/27 `[PASS] 경로 존재 확인 17개 전부 존재` |
| 8 1차 패스 잔존물 | **해결됨** [실측] | `/home/claude` 에 hometax_old_session · audit_new_head.md · kill.py 없음(빈 홈에서 시작) |

### 6차 후속 4차 "다음 회차에 볼 것" 4건

| 항목 | 판정 | 근거 |
|---|---|---|
| until_passed 단일 기준 | **해결됨** [실측] | `grep -n "until" scripts/*.py` 에서 until 을 날짜로 비교하는 곳은 `common.py` 164 `return (y, m) < (as_of.year, as_of.month)` **한 곳**. `build_report.py` 67 `_m(v.get("until"), y, 12)` 는 scope 월 환산(통과 여부 판정 아님), `check_input.py` 254 `vmap.get(i, {}).get("until")` 은 값 유무만 |
| `f["ended"]` 문자열 잔존 | **해결됨** [실측] | `grep -n "ended"` → `build_report.py` 109 `"ended": until_passed(v.get("until"), as_of),` · 132 `if f["ended"]:` · 161 `if f["ended"]:` 뿐. 문자열 사용 0. C 행 메모는 163 `until={f['until']}` |
| (b-5) `ws.title =` 미검출 | **미해결 → 결함 #4** [실측] | `build_report.py` 351 을 `ws.title = "매트릭스"` 로 바꾼 사본: `[PASS] 임계값·색상 단일 출처`. 대조: `validate.py` 의 `wb[cfg["sheets"]["matrix"]]` 를 `wb["매트릭스"]` 로 바꾸면 `[FAIL] 단일 출처 위반 1곳` |
| check_grace 2월 경로 | **결함 #1** [실측] | `--as-of 2026-02-05` 정상 산출물에 `[FAIL] 발급기한 유예 — 2026-01분 기한(10일)이 안 지났는데 '기한 전' 판정이 0건이다(매트릭스 유예 색 3칸)` |

### 6차 후속 3차 "다음 회차에 볼 것" 2건

| 항목 | 판정 | 근거 |
|---|---|---|
| `--dry-run` 읽기 전용 테스트 | **미해결 → 개선안 2** | `tests/test_edge_cases.py` 에 `dry` · `md5` · `readonly` grep 0건. 동작 자체는 실측 정상(P5) |
| 조치 표 문장 ↔ 코드 대조를 점검표에 | **미해결 → 개정안 9** | `checklist.md` 에 해당 문구 없음. 이번 회차에 실제로 SKILL.md 243 · push.py 283 의 "자료에서 채워진다" 가 코드와 어긋난 채 두 회차를 넘어왔다(결함 #2) |

### 6차 결함 14건 + 개선안 5건 — 전부 해결됨 유지 [실측]

| # | 근거(지금 원문) |
|---|---|
| 5 | 위 0~8 의 2번 |
| 28 | 위 6번 (다안 = 코드 무변경 + 문서) |
| 29 | 위 4번 |
| 20 | 위 2번 |
| 30 | `build_report.py` 292-293 `if listed_ids is not None and bid not in listed_ids:` / `continue` · `validate.py` 401 `if sid not in listed and g != "해결":` |
| N4 | `judgment-rules.md` 46 |
| 16 | `validate.py` 28 `from build_report import GRADE_ORDER` · 381 `order = GRADE_ORDER` |
| 14 | `excel-format.md` 15-18 config 키 표 |
| 15 | `column-mapping.md` 5-14 |
| 27 | `SKILL.md` 257 `### 가드가 걸렸을 때 밟는 3단계` · `push.py` 379-382 `거래처를 의도적으로 뺐다면 … 전부 설명되면 --force 가 정당합니다` |
| 21 | `build_report.py` 359-361 `"빈칸=미수취 · 색칠된 0=발행 후 전액취소 · 옅게 칠한 칸=발급기한 전 " "(색은 config/check-config.json 의 colors)"` |
| N6 | `validate.py` 43-46 `SHEET_CHECKS = [...]`(14개) · 787-791 개별 SKIP. 시트명 변경 사본: `FAIL 1 · SKIP 14 · PASS 3` = 18 |
| 18 | 위 6번 |
| 19 | `check_input.py` 268-269 `변경이라면 구 번호에 until, 신 번호에 since 를 넣어 둘 다 남긴다.` · 9/27 `[OK  ] 사업자번호 변경 처리 완료 1건 제이푸드` |
| 개선안 1·2·3·5 | (b-5~7) 존재 · `check_paths` 17개 · `build_report.py` 578-584 `[중단] 기간 안 자료 0건` · `t_no_upload_files` `t_zero_rows_not_resolved` 존재 |
| 개선안 4 | `push.py` 329 `--add-vendor` (dry-run 실측 P5) |

### 운영 주의(5차·6차)

| 항목 | 판정 |
|---|---|
| 유성빌딩 재권유 금지 | 종결. `ignore_suppliers` 로 콘솔·시트 모두 안 뜸(대상외 시트 유성빌딩 행 추가 권장 칸 None, 콘솔 "추가 권장" 줄 없음) |

---

## 결함 (10건 — 신규 8 · 이월 메모 승격 2)

심각도 순. 작업경로는 전부 `push.py --code`(브랜치). 월 의존 재평가: 오늘 9월. **#1 은 2027-02 회차에 확정 재현**되므로 12월 회차 전까지 1순위.

| # | 심각도 | 파일 | 줄 | 문제 원문(그대로) | 실측/추론 | 왜 틀렸는지 | 수정 방향 | 작업경로 |
|---|---|---|---|---|---|---|---|---|
| 1 | **높음** | `scripts/validate.py` | 572-576 | `elif expect and not january and n == 0:` / `rec(FAIL, "발급기한 유예", f"{label}분 기한({cfg['grace']['deadline_day']}일)이 안 지났는데 " f"'기한 전' 판정이 0건이다(매트릭스 유예 색 {grace_cells}칸). "` | [실측] `--as-of 2026-02-05` | 2월은 점검 창이 1~2월뿐이라 C 경로(경과 `stale_days` 이상 **그리고** 유예 월 보유)에 들어올 거래처가 구조적으로 없다 — 1월을 못 받은 곳은 유효 건 0(`elapsed None`)이라 C 진입 불가, 1월을 받은 곳은 유예 월이 없다. 그래서 '기한 전' 0 이 **정상**인데 6차 후속 4차 #2 가 비(非)1월에 등급 건수 신호를 택해 정상 산출물에 FAIL. 2027-02 초 실사용에서 "FAIL 이면 산출물을 주지 않는다"(SKILL.md 145) 로 막힌다. 3월 이후도 데이터에 따라 0 이 될 수 있다 | 신호를 월로 고르지 말고 **기대값을 재산출**: validate 가 이미 df·vendors 를 갖고 있으니 `build_facts`+`grade_all` 로 '기한 전' 기대 건수를 구해 실제 건수와 **정확 일치** 비교(0=0 이면 PASS). 색 칸 교차 신호는 보조로 유지. 개선안 1 과 같은 회차 | `push.py --code` |
| 2 | **중간** | `SKILL.md` / `scripts/push.py` / `scripts/build_report.py` | 243 / 283-284 · 331 / 100 | SKILL 243 `- \`--add-vendor\` 는 \`name\` 을 비워 둔다. 리포트를 다시 만들면 자료에서 채워진다.` · push 283 `"\n  상호(name)는 비어 있습니다. 리포트를 다시 만들면 자료에서 채워지며,\n"` · push 331 `"이름·주기는 최신 산출물의 대상외 목록에서 가져온다. "` · build_report 100 `"biz_no": sid, "name": v["name"], "cycle": v.get("cycle", ""),` | [실측] vendors 에 `name: ""` 로 212-04-59010 추가 후 실행 → 매트릭스 `['212-04-59010', None, '매월', …]` · 미수취목록 `['A. 발행 후 전액취소', '확인 필요', '212-04-59010', None, …]` | 채워주는 코드가 없다. `--add-vendor` 로 넣은 거래처는 리포트·state·채팅 요약에 상호가 빈칸으로 나간다. 문서(SKILL·push 콘솔·argparse help)만 세 곳이 같은 거짓을 말한다(6차 후속 2차 기록도 동일) | (a) `_one()` 에서 `v["name"] or (str(g["상호"].iloc[-1]) if len(g) else "")` 로 자료에서 채움 + `--add-vendor` 가 최신 산출물 없이도 동작하므로 push 331 문구는 삭제, 또는 (b) 세 문구를 "상호는 vendors.json 에 직접 적는다" 로 정정. (a) 권장 | `push.py --code` |
| 3 | **중간** | `scripts/push.py` | 260-270 | `sid = re.sub(r"\D", "", raw)` / `if len(sid) != 10:` / `print(f"  건너뜀  {raw} — 사업자번호가 10자리가 아닙니다")` … `d["vendors"].append({"biz_no": sid, "name": "",` | [실측] `--add-vendor 999-99-99999` → `추가    999-99-99999` 후 vendors.json 에 기록(31곳). 이어 `check_input` → `[FAIL] vendors.json 사업자번호 체크섬 오류 1건` | 체크섬(`common.biz_checksum_ok`)을 안 본다. 오타 번호가 그대로 push 되고(`vendors` 묶음은 테스트 게이트 없음), 다음 실행이 check_input FAIL 로 통째로 막힌다. SKILL.md 306 "체크섬은 check_input.py 가 검증" 은 사후 검증뿐 | 등록 전 `biz_checksum_ok(sid)` 로 거르고 `건너뜀 … 체크섬 오류` 출력 | `push.py --code` |
| 4 | **중간** (범위 밖 미검출) | `scripts/validate.py` | 705-708 | `for name, src in py.items():` / `if re.search(rf'\[\s*["\']{v}["\']\s*\]', src) or \` / `re.search(rf'create_sheet\(\s*["\']{v}["\']', src):` | [실측] P3 | `build_report.py` 351 `ws.title = cfg["sheets"]["matrix"]` 를 리터럴로 바꿔도 PASS. 첫 시트만 `ws.title =` 로 이름을 주므로 매트릭스 시트명 하드코딩은 영영 못 잡는다(6차 후속 4차 메모 이월) | 패턴에 `re.search(rf'\.title\s*=\s*["\']{v}["\']', src)` 추가. 파괴 실험 표에 "ws.title 리터럴" 행 상시화 | `push.py --code` |
| 5 | 낮음 | `references/judgment-rules.md` / `SKILL.md` | 86 / 169 | judgment 86 `\| 거래 종료 \| vendors 에 \`until\` 등록됨 \| 점검 대상 아님 \|` · SKILL 169 `\| \`거래 종료\` \| \`vendors.json\` 에 \`until\` 로 등록됨 — 점검 대상 아님 \| 무시. …` | [추론] 코드 원문 기준(`build_report.py` 109 `"ended": until_passed(v.get("until"), as_of)` · 132 · 161). 6차 후속 4차가 미래 until(비앤지 2026-12) → `확인 필요` 유지를 실측함 | 6차 후속 4차 이후 코드는 **until 이 지난 곳만** 거래 종료다. 미래 until 은 결번 판정을 그대로 받는다. 문서 두 곳은 옛 기준("등록되면 종료")을 말한다 — 6차 후속 4차가 코드·테스트만 고치고 문서를 안 고쳤다(0단계 (2) 유형) | "until 이 **지난** 곳(실행월 이전). 미래 until 은 아직 거래 중으로 판정" 으로 두 곳 정정 | `push.py --code` |
| 6 | 낮음 | `scripts/validate.py` | 114-116 · 157-159 · 405 · 424 | 114 `r, m = find_header_row(ws, ["공급자번호", "상호"])` / 115 `if not r:` / 116 `return` (check_matrix_blank_and_fill) · 157-159 동일(check_vendor_coverage) · 405 `if g == "확인 필요" and mrow.get(sid):` · 424 `rec(PASS, "등급 분류", f"{n}행 · 등급값·정렬·결번 표기 정상")` | [실측] 매트릭스 헤더 `공급자번호`→`공급자 번호` 사본: 요약 **15개**(`FAIL 3 · SKIP 1 · PASS 11`). `매트릭스 월 컬럼`·`미수취=공란 검사`·`전액취소=0+노랑 검사`·`점검 대상 누락 검사` 4건이 기록 없이 사라지고, `등급 분류` 는 `mrow={}` 라 결번 대조를 한 건도 안 하고도 `22행 · 등급값·정렬·결번 표기 정상` PASS | 6차 후속 4차 5a 가 "요약 개수는 늘 18" 을 원칙으로 세웠는데(788-789 주석) 헤더 미검출 경로는 그 원칙 밖이다. 전체는 FAIL 이라 조용한 통과는 아니지만 "검사가 사라졌다" 와 구분이 안 되고, 등급 분류 PASS 문구는 거짓 | `if not r:` 에서 `rec(SKIP, <검사명>, "매트릭스 헤더 미검출")` 로 개별 기록 · 등급 분류는 `mrow` 가 비면 "결번 표기 미확인" 으로 문구 분리(또는 SKIP) | `push.py --code` |
| 7 | 낮음 | `scripts/push.py` | 291-300 | `for raw in a.ignore_vendor:` / `sid = re.sub(r"\D", "", raw)` / `if len(sid) != 10:` … `if sid in cur:` / `print(f"  건너뜀 … 이미 제외 목록에 있습니다")` / `cur.append(sid)` | [실측] `--ignore-vendor 869-35-00721 --dry-run`(다연유통, vendors.json 에 **등록된** 곳) → `제외 예정  869-35-00721 — '추가 권장' 재권유를 끕니다` | vendors.json 에 남아 있는 거래처는 `ignore_suppliers` 에 넣어도 판정에 아무 영향이 없다(대상외 시트·`_print_reco` 두 곳만 읽음, 6차 후속 3차 D). help 333-335 "의도적으로 점검 대상에서 뺀 거래처용" 과 어긋난 입력을 그대로 받아 사용자는 뺐다고 믿게 된다 | vendors.json 에 있으면 `건너뜀 … 아직 vendors.json 에 등록돼 있습니다. 먼저 지우세요` | `push.py --code` |
| 8 | 낮음 | `scripts/push.py` | 332 | `"--ignore 와 같이 쓸 수 없다.")` | [실측] `--help` 원문 | 옵션 이름은 `--ignore-vendor`(333) | 문구 정정 | `push.py --code` |
| 9 | 낮음 | `SKILL.md` | 418 | `audit/last-audit.md        직전 점검 기준선 (1단계에서 함께 읽는다)` (구성 목록에 `audit/checklist.md` 없음) | [실측] 실물 ls 에 `audit/checklist.md` 존재(6차부터) | "저장소 구성" 목록이 실물과 다르다(점검표 A "파일 구성 목록 일치") | `audit/checklist.md   정기 점검표 정본` 한 줄 추가 | `push.py --code` |
| 10 | 낮음 | `scripts/check_input.py` | 252 | `vmap = {v["biz_no"]: v for v in vendors}` | [실측] 제이푸드 구 번호를 `"559-96-01523"`(하이픈) 로 바꾼 사본: `[OK  ] … 체크섬 정상` 인데 `[WARN] 같은 상호인데 사업자번호가 다름` 이 재발("처리 완료" 사라짐) | 같은 파일의 체크섬·중복 검사(227·237)와 `build_facts` 46 은 `norm_biz` 로 정규화하는데 이 한 곳만 원문 키를 써서, 표기가 섞이면 이미 처리한 쌍을 다시 경고한다. `push.py` 258 `have = {v["biz_no"] …}` 도 같은 유형(하이픈 등록분은 "이미 등록" 을 못 잡아 중복 추가 가능). 형식 규칙(하이픈 없음)을 지키면 안 밟는다 | 두 곳 `norm_biz(v["biz_no"])` | `push.py --code` |

### 통과 처리 (인용은 되나 결함으로 올리지 않음) — 5건

- `build_report.py` 8 `3. 발급기한(익월 10일)이 안 지난 달은 미수취로 확정하지 않는다.` · `check_input.py` 124 `기한이 익년 1/10 이라` · `common.py` 82 `12월분 발급기한은 익년 1/10 이라` — 독스트링 사본 3곳, validate 620-627 가 일부러 제외(6차와 동일). #2·#5 문구를 고칠 때 같이 고치면 싸다
- `validate.check_matrix_blank_and_fill` 130 `if c.value is None:` — `''` 조건은 openpyxl 저장 시 None 환원으로 만들 수 없음(4회차 연속). `' '` 는 `월별 합 대사` 가 `[FAIL] … 숫자가 아닌 값 1개: 1월: ' '` 로 잡음(6차 5b 유지)
- `check_input.py` 132 `if day > 10:` — deadline_day 와 무관한 시작일 휴리스틱(5·6차 판정 유지)
- `sync.py` 72 `--with-tests` SUPPRESS no-op 호환 플래그(6차 판정 유지)
- `validate.check_grace` 는 9/27 처럼 직전 달 기한이 지난 뒤(`expect=False`)에는 등급열을 어떻게 훼손해도 PASS — 설계상 비활성 구간이지 죽은 검사가 아님. 9/6 산출물(기한 전→정상)과 1월 산출물(색 제거)로 FAIL 확인. 다만 개선안 1 로 가면 이 구간도 검사된다

**인용불가로 제외: 0건.**

---

## 개선안 (최대 5)

| # | 내용 | 이유 | 우선순위 |
|---|---|---|---|
| 1 | validate 에 **등급 재산출 대조** 신설: `build_facts`+`grade_all` 로 기대 `(공급자번호, 등급, 결번월)` 집합을 만들어 미수취목록과 정확 일치 비교(누락→FAIL, 초과→FAIL). `check_grace` 의 등급 건수 신호를 이 기대값으로 교체 | 점검표 E "등급 분류가 옳은지" 가 아직 형태 검사(값·정렬·결번 공란)뿐이다. 결함 #1 의 근본 해법이고, 6차 후속 4차 #2 가 "or/and" 로 고민하던 신호 선택 문제가 사라진다. 리스크: build_report 와 같은 함수를 쓰므로 판정 논리 자체의 오류는 못 잡는다(그건 tests 의 몫) — 기록해 둘 것 | **1** |
| 2 | `t_dry_run_readonly`: sandbox 에서 `push.py X --add-vendor … --dry-run` · `--ignore-vendor … --dry-run` 실행 전후 `config/` md5 동일 단언 (6차 후속 3차 이월) | 6차 후속 3차 A 사고(dry-run 이 파일을 씀)의 재발을 손 대조에만 맡기고 있다. 이번 회차도 손으로 27파일 md5 대조(P5) | 2 |
| 3 | `save_state` 의 `flagged` 를 `biz_no` 로 정렬(`build_report.py` 312-314) | 지금은 `grade_all` 정렬(등급→최종수취일)을 따라 최종수취일이 바뀔 때마다 순서가 바뀌어 9/20 처럼 내용 동일·순서만 다른 커밋(+7/−7)이 생긴다. `check_state`·`state_regressed` 는 집합·건수 비교라 판정 영향 0(P6 실측) — 결함 아님 | 3 |
| 4 | `build_report` 가 `state.run_date > as_of` 이면 경고(또는 `--as-of` 과거 재현 시 이력 비교 자동 off) | 이번 회차 1월·2월 재현에서 9/20 이력이 미래라 직전 확인 필요 3곳이 전부 `해결` 로 표기됐다(콘솔 `해결 3`). 과거 재현이면 "해결" 이 아니라 "이력이 미래" 다. push 가드가 state 역행은 막지만 리포트의 거짓 해결 표기는 못 막는다 | 4 |
| 5 | validate FAIL 이면 산출물 파일명에 `_FAIL` 접미를 붙이거나 `--out` 에서 지운다(옵션) | SKILL.md 145 "FAIL 이 있으면 산출물을 주지 않는다" 가 사람 절차에만 의존한다. 2월 회차 오탐(#1) 같은 때 판단은 사용자가 하되, 정상 파일명으로 `/mnt/user-data/outputs` 에 남아 present_files 되는 사고를 막는다 | 5 |

---

## 속도·효율 후보 S1~S5

합격 기준: 같은 입력으로 A(현재)/B(후보) 각 1회, 결과 집합(튜플 22 + 월별 합 + validate 요약 + state 순서) 동일 + validate FAIL 0. 실험은 `/home/claude/exp_speed` 사본, 저장소·설치본 불변. 파이프라인 벽시계는 A 3.10s / B 3.07s 로 같다 — 절감 대상은 **도구 호출 수·즉석 코드 줄 수**다.

| # | 후보 | (a) 현재 원문 | (b) 실측 | (c) 절감 | (d) 리스크·검증 | 판정 |
|---|---|---|---|---|---|---|
| S1 | `build_report` 콘솔에 **확인 필요 행**(공급자번호·상호·결번월·상태·최종수취일·유형)을 찍는다 | SKILL.md 151 `채팅에는 **확인 필요 항목만** 표로 요약한다.` — 콘솔 627-628 은 건수뿐 | A: openpyxl 스니펫 **11줄** + bash 1회 → B: 0줄·0회. 결과 집합 **동일**(튜플 22/22 · 월별 합 · `FAIL 0 · SKIP 1 · PASS 17` · state 순서) | 도구 호출 −1 · 즉석 코드 −11줄 | 콘솔 출력만 추가, xlsx·state 무변경. 검증: `tests` 에 콘솔 `!` 줄 수 == 확인 필요 건수 단언 추가 | **합격** |
| S2 | SKILL.md 3~5단계를 `&&` **한 줄**로: `python3 scripts/check_input.py $U && python3 scripts/build_report.py --uploads $U --out $O && python3 scripts/validate.py "$(ls -t $O/*.xlsx \| head -1)" --uploads $U` (`--as-of`·`--strict` 는 세 곳에 같이) | SKILL.md 95-98 · 114-116 · 133-135 세 코드 블록, 134 `<생성된파일>.xlsx` | B 1회 실행 3.07s, 결과 집합 동일. check_input FAIL 이면 `&&` 가 멈춰 "FAIL 이면 만들지 말 것"(104) 이 그대로 지켜진다(1월 재현에서 rc=1 확인) | 도구 호출 −2 | `ls -t` 최신 파일이 이번 산출물이라는 가정 — `--out` 이 실행별 폴더면 안전. 코드 변경 0(문서만) | **합격** |
| S3 | 실사용 회차의 문서 읽기 축소: `audit/last-audit.md`(83,115자, view 5~6회) 대신 **`audit/OPEN.md`(≤30줄: 미해결·첫 실사용에서 볼 것)** 만 읽고, last-audit.md 는 "결과가 이상하거나 고칠 때" 로 한정 | install/SKILL.md 36-43 `/home/claude/hometax/audit/last-audit.md   ← 있으면 함께 읽는다` · SKILL.md 73 `\`audit/last-audit.md\` 가 있으면 **함께 읽는다.**` | 문자 수만 실측(view 절단 16,000자). 회차마다 파일이 커진다(6차 387→804행→이번 ~1,100행) | 도구 호출 약 −5 | 결과 무관. **설계·문서 변경이라 사용자 결정, 기본 미채택.** 채택 시 OPEN.md 갱신 의무를 마무리 절에 넣어야 함(두 곳 유지 비용) | 사용자 결정 |
| S4 | 정상 회차(state 만 올림)의 `push.py --dry-run` 선행 관행 생략 | SKILL.md 217 `python3 scripts/push.py <토큰> --code --dry-run # 뭐가 바뀌는지 먼저 확인` · 223 `확신이 없으면 먼저 이걸로 본다` | push.py 394-397 이 올리기 전 바뀐 파일·줄 수를 찍고, state 역행 가드가 있다 [추론 — 이번 회차는 code 묶음이라 dry-run 을 썼다] | 도구 호출 −1 | 되돌릴 수 없는 커밋이라 **사용자 결정, 기본 미채택**. code 묶음은 dry-run 유지 | 사용자 결정 |
| S5 | 스크립트 벽시계 | 세 스크립트가 각각 6개 xls 를 파싱(≈0.45s×3) | 합계 3.10s 중 파싱 중복 ≈0.9s | <2s | 지시 기준("합쳐 2초 미만이면 후보 아님")에 해당 없음 | 후보 아님(기록만) |

### 실험 코드 원문

S1 (사본 `exp_speed/scripts/build_report.py`, `_print_deadline(facts, as_of, cfg)` 호출 직전에 4줄):

```python
    for r in rows:      # S1: 확인 필요 행을 콘솔에도 — 채팅 요약용 즉석 openpyxl 코드를 없앤다
        if r["grade"] == "확인 필요":
            print(f"  ! {fmt_biz(r['biz_no'])} {r['name']} · 결번 {_labels(r['gap'], as_of) or '-'}"
                  f" · {r.get('status', '')} · 최종수취 {r['last']} · {r['kind']}")
```

B 출력(9곳): `! 264-81-35761 농업회사법인 광개토엠앤에프 주식회사 · 결번 5월, 7월, 8월 · 계속 · 최종수취 2026-06-30 · A. 정기 거래처 결번` … `! 869-35-00721 다연유통 · 결번 2월, 4월 · 계속 · 최종수취 2026-08-31 · A. 정기 거래처 결번`

S2 (B 실행에 쓴 한 줄, `U=tests/fixtures O=/home/claude/out7/B_speed`):

```bash
python3 scripts/check_input.py $U && python3 scripts/build_report.py --uploads $U --out $O && python3 scripts/validate.py "$(ls -t $O/*.xlsx | head -1)" --uploads $U
```

A 스니펫(현재 6단계에 필요한 즉석 코드, 11줄): `load_config()` → `load_workbook(<xlsx>)[cfg["sheets"]["missing"]]` → 헤더 행 탐색 → `{이름: 열}` → 등급 `확인 필요` 행의 상호·누락된 월·상태·최종수취일 출력.

---

## 정확성 P1~P9 결과

| # | 결과 | 근거 |
|---|---|---|
| P1 | until 날짜 비교 **1곳**(`common.py` 164) | 위 후속 4차 표 |
| P2 | `f["ended"]` 문자열 사용 **0** | 〃 |
| P3 | `ws.title` 리터럴 → **PASS(범위 밖 미검출)** → 결함 #4 | 〃 |
| P4 | 2월 `check_grace` → **FAIL**(정상 산출물) → 결함 #1. SKIP 은 없음 | 기준선 표 asof_0205 |
| P5 | `--add-vendor 212-04-59010 999-99-99999 1198687135 --dry-run` · `--ignore-vendor 869-35-00721 2120459010 --dry-run` · 둘 다 지정 → 저장소 폴더 **27파일 md5 전부 동일**(읽기 전용 ✓, 둘 다 지정은 `[중단]` rc 0). 테스트는 없음 → 개선안 2. 부수 발견: 체크섬 미검증(#3) · 등록 거래처 수락(#7) | |
| P6 | state 순서 = `grade_all` 정렬 `(GRADE_ORDER, last)` 즉 **최종수취일 오름차순** — 379행 매트릭스 키 `(not listed, -months_got, name)` 를 따르지 않는다. 9/6 `광개토·비앤지·다연`(fixtures 최종수취 6/30·8/29·8/31) → 9/20 `비앤지·다연·광개토` 는 실자료에서 광개토가 9월분을 받아 최종수취일이 뒤로 간 것. `validate.check_state` 443·457 은 set, `push.state_regressed` 181-192 는 run_date+건수 → 순서 무관(같은 날 순서만 바뀐 케이스 `None` 실측). 결함 아님 → 개선안 3 | |
| P7 | `--add-vendor`·`--ignore-vendor`·`--cycle` 은 `SKILL.md` 228-230·238-247, `ignore_suppliers` 는 229·249 에 있음. **README.md 0건**(README 는 `--dry-run`·`--only` 등도 없는 축약본) · `checklist.md` A 옵션 목록(126행) 없음 → 개정안 2 | |
| P8 | **[추론]** 9월 열은 실행월이라 생성되지만(9/27 실측 9열·전 칸 유예 색) 9월분 기한(10/10) 임박 문구는 당월 제외 규칙(`_print_deadline` 640-641)으로 10/1~10/10 실행에서만 나온다. `check_resolved` 상태열만 N>0 실사용 대조는 이번에도 미실측(해결 0) | |
| P9 | `push.py` 의 `BRANCH` 사용처 **4곳**: 44 `BRANCH = "main"` · 139 `url = f"{API}/{urllib.request.quote(path)}?ref={BRANCH}"` · 149 `"branch": BRANCH}` · 355 `print(f"저장소: {REPO}@{BRANCH}")`. `sync.py` 는 29 `BRANCH = "main"` · 69 `ap.add_argument("--ref", default=f"refs/heads/{BRANCH}",`. `python3 sync.py --ref refs/heads/main /home/claude/synctest` → `24개 파일 · 준비 완료`, 작업본과 `diff -rq` 차이 0 (브랜치 경로로 받아짐) | 설계는 하지 않았다 |

기타 실측: 테스트 게이트 — 사본 `common.py` 에 `range(1, 10)` 주입 후 `push.run_tests()` → `False`(테스트 FAIL 출력). state 역행 가드 — 과거날짜 / 같은날 감소 / 원격 깨짐 → 차단 메시지, 정상 전진·같은날 순서만 변경 → `None`. config 삭제 — `build_report`·`check_input` 모두 `[중단] 설정(check-config.json) 파일이 없습니다` rc 1. GROUPS 커버리지 누락 0. sync codeload(42행) 유지.

---

## validate.py 검사 생존 확인 (고유 검사명 20개 · 파괴 30회)

기준: fixtures 로 9/27 산출물(`FAIL 0 · SKIP 1 · PASS 17`, state = 그 실행이 저장한 9곳) · 9/6 산출물(기한 전 있음) · 1월 산출물(`--as-of 2026-01-05`, state = 9/20 이력 → 해결 3). 사본 `/home/claude/exp_val` 에서 한 곳씩 바꿔 재검증. 실행 스크립트 원문은 아래 부록. 정상 경로 18개 + **실패 경로 전용 2개(매트릭스 헤더 · 매트릭스 셀 검사)** 전부 FAIL 확인. 범위 밖 1건.

| 검사 | 파괴 방법 | 결과 |
|---|---|---|
| 경로 존재 확인 | README.md 임시 제거 | FAIL ✓ |
| config 죽은 키 | `thresholds.zzz_dead: 1` | FAIL ✓ `config 죽은 키 1개` |
| 임계값·색상 단일 출처 (b-4) | README 끝 `발급기한은 익월 10일이다.` | FAIL ✓ |
| 〃 (b-1) | excel-format 끝 `FFEB9C` | FAIL ✓ |
| 〃 (b-7) | README 끝 `1/10` | FAIL ✓ |
| 〃 (b-5 문서) | judgment-rules 에 `\| 매트릭스 \|` 표 | FAIL ✓ |
| 〃 (b-3) | common.py `range(1, 10)` | FAIL ✓ |
| 〃 (b-6) | build_report `th["monthly_min_months"]` → `6` | FAIL ✓ |
| 〃 (b-5 코드) | build_report `create_sheet("미수취목록")` | FAIL ✓ |
| 〃 (b-5 코드) | build_report `ws.title = "매트릭스"` | **PASS ✗ — 범위 밖(결함 #4)** |
| 시트 구성 | 시트명 매트릭스→매트릭수 | FAIL ✓ `FAIL 1 · SKIP 14 · PASS 3` = 18 |
| 매트릭스 헤더 (실패 전용) | 매트릭스 헤더 `공급자번호`→`공급자 번호` | FAIL ✓ — 요약 **15개**(결함 #6) |
| 매트릭스 월 컬럼 | 헤더 `9월`→`9 월` | FAIL ✓ |
| 매트릭스 셀 검사 (실패 전용) | 월 헤더 전부 `1M`… (월 컬럼 0개) | FAIL ✓ `월 컬럼을 하나도 못 찾음` (요약 17개) |
| 미수취=공란 검사 | 공란 한 칸에 취소색 | FAIL ✓ |
| 〃 | 공란 한 칸에 `' '` | 이 검사는 PASS, `월별 합 대사` 가 FAIL(설계, 6차 5b) |
| 전액취소=0+노랑 검사 | 0 칸 노랑 제거 | FAIL ✓ |
| 점검 대상 누락 검사 | 점검대상 1행 삭제 | FAIL ✓ (합계·월별도 FAIL) |
| 합계 대사 | 순공급가액 +1 / `' '` | FAIL ✓ / FAIL ✓ `숫자가 아닌 칸 1개` |
| 월별 합 대사 | 한 행 1월↔5월 교환 | FAIL ✓ `불일치 2개월` |
| 원본 행수 | 원본정제 마지막 행 삭제 | FAIL ✓ |
| 승인번호 중복 | 1건 복제 | FAIL ✓ `승인번호 중복 1건` |
| 상계 매칭 | `취소분(상계)` 1건 → `-` | FAIL ✓ |
| 대상외공급자 시트 | 공급자번호를 vendors 것(바로고)으로 | FAIL ✓ |
| 등급 분류 | `이상등급` / 결번월 8월→값 있는 1월 / 첫 행 `정상`(정렬 뒤집힘) | FAIL ✓ 1건 / 1건 / 11건 |
| 실행 이력 비교 | state flagged 9→1 | FAIL ✓ |
| 해결 집계 | 1월 산출물 해결 행 상태 비움 | FAIL ✓ |
| 발급기한 유예 | 9/27: 무변경(`expect=False` 비활성) / 9/6 산출물 `기한 전`→전부 `정상` / 1월 전년 12월 열 유예 색 제거 / auto 산출물을 `--strict` 로 검증 | PASS(설계) / FAIL ✓ / FAIL ✓ / SKIP(strict 모드) |

주의(6차 유지): `--strict`/`--no-state` 는 같은 파일명에 덮어쓰므로 파괴 실험 기준 파일은 실행별 `--out` 폴더에 둘 것(이번 회차 `out7/<이름>`).

---

## 점검표 양방향 대조 (saero-ad-report-skill `audit/checklist.md` v4.5, 463행 ↔ 이 저장소 v6/6.1, 281행)

| 저쪽(saero)에만 있는 것 | 이쪽(hometax)에만 있는 것 |
|---|---|
| 머리말 **2회 커밋 규칙**(last-audit 1차 → 채택 후 checklist 2차) — 이쪽 3·244-247행은 아직 "같은 push 로" | 점검 요청 4줄 붙여넣기 문구(13-20행) |
| `[의도된 동작 — 결함으로 올리지 마라]` 절(번호 목록) | `[시작 전 확인 ②]` 데이터 최종일 3단계 판정표 · fixtures 교체 금지 |
| `[되돌리면 안 되는 것]` 표(확인할 것 · 되돌아가면 생기는 일 · 위치) | `[운영 조건]`(실행 빈도·설치본 55행·재업로드) |
| `[알려진 이월 항목]` 절이 last-audit 를 가리키기만 함(이쪽도 [이월 항목] 절은 같은 원칙인데 머리말 5-11행에 후속 조치 상태를 적어 모순) | A~J 세부 점검 항목(옵션명·등급 6종·config 키 목록·월 경계·J 엣지 목록) |
| `[수정 회차에 적용할 것]`(같은 개념 두 파일 대조 등) | validate 파괴 실험 **수동** 지시 + 검사별 표 형식 |
| `[검증 회차 A 동작 / B 의도]` 붙여넣기 문구 | 기준선(last-audit) 형식 절 |
| 효율 기준선 표 상시화 · 파괴 실험 `tests/mutation_test.py` 이관 · 설치본 매 회차 확인 · 토큰 폐기 · PC push | 월 의존·커플링 항목 재판정 지시 |
| 다음 회차 구조 변경 계획(파일 분리 registry/updates) · 경쟁사 판정 이력(스킬 고유) | `--as-of` state 백업·복구 지시(F) |

---

## 점검표 개정안 (통합 목록 — 6차 대기 1·3~8 판정 포함)

1. **[대기 1 — 실은 반영됨, 기록 정정]** F 175행이 이미 `--as-of <데이터 연도>-01-05` 다. 11행 "1·3~8번 … 아직 반영하지 않았다" 를 "3~8번" 으로, 버전 줄 3행을 `v6.1 · 2026-09-07(사후 반영 1·2·9·10·11·12)` 로 정정. 머리말 5-11행(후속 조치 상태)은 [이월 항목] 절 원칙("점검표에 적지 않는다")과 모순이므로 삭제하고 last-audit 로 옮긴다.
2. **[대기 3 — 채택 권고]** B 항목·파괴 실험 표에 "**범위 밖**" 판정 허용. 이번 `ws.title` 이 정확히 그 유형.
3. **[대기 4 — 폐기 권고]** md5 대조 추가는 12번(최종일 기준)이 대체했다.
4. **[대기 5 — 채택 권고]** 파괴 실험·`--strict`·`--no-state` 는 실행별 `--out` 폴더(이번 지시가 이미 그렇게 시킴).
5. **[대기 6 — 채택 시 개선안과 함께]** 3회차 연속 통과 항목(A 옵션 존재 · C 체크섬 · G codeload · G GROUPS 커버리지 · I 경로 존재 · B config 삭제 시 정지)을 `tests/t_audit_static` 하나로 묶고 점검표에서 뺀다. 7차도 전부 통과.
6. **[대기 7 — 채택 권고]** "validate 검사 전부 파괴" 지시를 "현재 `rec(` 두 번째 인자 고유 이름 기준(정상 요약 18 · 실패 경로 전용 2 포함 20)" 으로.
7. **[대기 8 — 채택 권고]** D "None 과 빈 문자열" 항목 삭제(4회차 연속 조건 성립 불가). 대신 "매트릭스 헤더를 못 찾는 경로에서 요약 검사 개수가 18 을 유지하는지"(결함 #6) 추가.
8. **[신규]** A 옵션 목록(126행)에 `--add-vendor` `--ignore-vendor` `--cycle` 추가, B 항목에 config `ignore_suppliers` 추가(문서·코드 참조 두 곳 대조).
9. **[신규]** 0단계 (2)에 "**직전 후속 조치 표의 문장을 코드와 한 번씩 대조**" 추가(6차 후속 3차 이월). 근거: SKILL.md 243 · push.py 283 의 거짓 문구가 두 회차를 넘어왔다.
10. **[신규]** F 실측에 `--as-of <연도>-02-05`(2월 경로: 창 2개월, check_grace 등급 건수 신호) 추가. 결함 #1 의 발견 경로.
11. **[신규]** H 항목 5건(D-day · cycle 경고 · 추가 권장 반영 · 1/1 시작 검사 · 전년 12월)은 전부 구현됐다 → "구현됨, 새 후보만" 으로 축소.
12. **[신규 — saero 통일]** 머리말·마무리 절을 **2회 커밋 규칙**으로 정정(3행 "같은 push 로", 244-247행 "같은 push.py --code 로", 247 "둘 중 하나만 올리면 어긋난다"). 이번 회차 실제 절차(1차 last-audit 만)와 점검표가 어긋난 상태다.
13. **[신규 — saero 통일]** `[의도된 동작]` 절 신설 후보: ① 비정기 라벨은 A 경로 면제 안 함 ② 1월 산출물 '기한 전' 0 정상 ③ 점검대상 0곳은 경고 ④ 직전 달 기한 경과 후 유예 검사 비활성 ⑤ 미등록 공급자 제거≠해결 ⑥ dry-run 시 둘 다 지정 `[중단]` rc 0. `[되돌리면 안 되는 것]` 표 후보: until_passed 단일 기준 · listed_ids 가드 · 0건 가드 · check_sheets 개별 SKIP · dry-run 무기록 · ignore_suppliers · codeload · `_scan`. `[수정 회차에 적용할 것]`·`[검증 회차 A/B]` 문구는 skill-audit 프롬프트 ②③ 을 가리키는 한 줄로.
14. **[신규 — saero 통일]** 효율 기준선 표(1절 형식: 명령·벽시계·도구 호출·즉석 코드 줄·산출값)를 상시 항목으로. 파괴 실험은 부록 스크립트를 `tests/mutation_test.py` 로 이관하는 것을 다음 수정 회차 후보로(개정안 6 의 개수 기준을 스크립트가 세게).
15. **[신규]** 점검 요청 4줄(13-20행)은 실제 회차 지시(skill-audit 프롬프트 ①)와 다르다 — 4줄을 지우고 "지시는 skill-audit 프롬프트 ① 형식, 이 파일은 절차만" 으로.
16. **[신규]** 부트스트랩 install/SKILL.md 36-43 · SKILL.md 73-75 의 "last-audit.md 를 함께 읽는다" 는 실사용 회차 도구 호출 5~6회를 쓴다(S3) — 채택 여부와 무관하게 점검표 [운영 조건]에 "실사용 회차가 읽는 파일과 분량" 을 적어 매 회차 재측정.

---

## 점검표 갱신 이력 (checklist.md)

- 6차 2026-09-07 — 첫 이관. 사후에 2·9·10·11·12(+1) 반영, 버전 줄은 "6차" 그대로(개정안 1 로 정정 예정).
- 7차 2026-09-27 — **미갱신**(진단 회차, 2회 커밋 규칙: 채택 뒤 2차 커밋).

---

## 다음 점검에서 대조할 것

1. **결함 #1(2월 check_grace)** — 2027-02 회차 전에 반드시. 고칠 때 개선안 1(등급 재산출)과 한 회차. 고친 뒤 `--as-of 2026-02-05` 가 FAIL 0 인지, 9/6 산출물 '기한 전'→정상 훼손이 **여전히** FAIL 인지(파괴 실험 재실행).
2. **결함 #2** 를 (a) 코드 채움으로 고치면 `_one()` 의 `name` 이 `v["name"] or 자료 상호` 가 됐는지 + push.py 283·331 문구, SKILL.md 243 세 곳 grep(`자료에서 채워`).
3. **결함 #3·#7** 을 고치면 `--add-vendor 999-99-99999 --dry-run` 이 `건너뜀 … 체크섬`, `--ignore-vendor 8693500721 --dry-run` 이 `건너뜀 … 등록돼 있음` 인지. 개선안 2(`t_dry_run_readonly`)와 같은 회차면 그 테스트가 두 케이스를 함께 단언하게.
4. **결함 #4** 파괴 실험 행 "ws.title 리터럴" 이 FAIL 로 바뀌었는지.
5. **결함 #6** 매트릭스 헤더 미검출 사본의 요약이 18개인지, 등급 분류 문구가 "결번 표기 미확인" 인지.
6. **개선안 3** 을 넣으면 첫 실사용 state 커밋이 정렬 변화로 한 번 더 diff 가 큰 것이 정상(그 뒤로는 내용 변화만).
7. **미실측 이월(5회차째)**: `check_resolved` 상태열만 N>0 실사용 대조.
8. **P8 [추론] 2건**: 10월 초 실사용에서 9월분 기한(10/10) 임박 문구 · 당월 열 생성 실측.
9. **개정안 12(2회 커밋)** 이 checklist.md 에 반영됐는지 — 반영 전까지 마무리 절(244-247)은 실제 절차와 다르다.
10. 이번 회차 실험 사본·산출물(`/home/claude/exp_*`, `out7`, `base7`)은 컨테이너 한정. 다음 회차는 부록 스크립트로 재현한다.
11. 저장소 커밋이 push 1회당 파일 수만큼 생긴다(6차 후속 4차 7커밋, 3차 4커밋 — Contents API 파일별 PUT). 결함 아님(기록만). 브랜치 push 가 들어오면 `--branch` 와 함께 다중 파일 커밋(Git Data API) 을 검토할지 사용자 결정.

**내가 고를 항목(사용자 채택용 번호)**: 결함 1~10 / 개선안 1~5 / 속도 S1·S2(합격), S3·S4(사용자 결정) / 점검표 개정안 1~16.

### 부록 — validate 파괴 실험 스크립트 원문 (7차 수정 후 버전 · 사본 /home/claude/exp_val 에서 실행 · 등급 재산출 대조 파괴 3건 포함)

```python
"""validate.py 검사별 파괴 실험 (사본 /home/claude/exp_val 에서만)."""
import os, sys, json, shutil, subprocess, re, copy
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
SB = "/home/claude/exp_val"; OUT = "/home/claude/out7/destroy"; FIX = f"{SB}/tests/fixtures"
sys.path.insert(0, f"{SB}/scripts")
from common import load_config, norm_biz
cfg = load_config()
S = cfg["sheets"]
BACKUP = "/home/claude/base7/last-run.backup.json"
def run(args, cwd=SB):
    return subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True)
def build(name, asof, state_src):
    d = f"{OUT}/{name}"; os.makedirs(d, exist_ok=True)
    shutil.copy(state_src, f"{SB}/state/last-run.json")
    r = run(["scripts/build_report.py", "--uploads", FIX, "--out", d, "--as-of", asof])
    assert r.returncode == 0, r.stderr
    x = [f for f in os.listdir(d) if f.endswith(".xlsx")][0]
    shutil.copy(f"{SB}/state/last-run.json", f"{d}/state.json")
    return f"{d}/{x}"
def validate(x, asof, state_src=None, extra=()):
    if state_src: shutil.copy(state_src, f"{SB}/state/last-run.json")
    r = run(["scripts/validate.py", x, "--uploads", FIX, "--as-of", asof, *extra])
    lines = [l for l in r.stdout.splitlines() if l.startswith("[")]
    summ = re.search(r"FAIL \d+ · SKIP \d+ · PASS \d+", r.stdout)
    return lines, (summ.group(0) if summ else "요약 없음: " + (r.stderr.strip().splitlines()[-1:] or [""])[0]), r.returncode
def hdr(ws, must):
    for r in range(1, 9):
        m = {str(c.value).strip(): c.column for c in ws[r] if c.value}
        if all(k in m for k in must): return r, m
def pick(lines, key):
    return [l for l in lines if key in l] or ["(해당 검사 줄 없음)"]

# --- 기준 산출물
base = build("base0927", "2026-09-27", BACKUP)   # state: 3 flagged → after build 9 flagged
st0927 = f"{OUT}/base0927/state.json"
jan = build("base0105", "2026-01-05", BACKUP)   # 해결 3
st0105 = f"{OUT}/base0105/state.json"
sep06 = build("base0906", "2026-09-06", BACKUP)  # 기한 전 있음
st0906 = f"{OUT}/base0906/state.json"
res = []
def rec(check, how, lines, summ, key):
    res.append((check, how, " | ".join(pick(lines, key)), summ))
for nm, x, asof, st in [("base0927", base, "2026-09-27", st0927), ("base0105", jan, "2026-01-05", st0105), ("base0906", sep06, "2026-09-06", st0906)]:
    l, s, rc = validate(x, asof, st)
    res.append((f"기준 {nm}", "무변경", s, ""))

def mod(x, name, fn):
    p = f"{OUT}/{name}.xlsx"; wb = load_workbook(x); fn(wb); wb.save(p); return p

# 1 경로 존재
os.rename(f"{SB}/README.md", f"{SB}/README.md.bak")
l, s, _ = validate(base, "2026-09-27", st0927); rec("경로 존재 확인", "README.md 임시 제거", l, s, "경로 존재")
os.rename(f"{SB}/README.md.bak", f"{SB}/README.md")
# 2 config 죽은 키
cp = f"{SB}/config/check-config.json"; orig_cfg = open(cp, encoding="utf-8").read()
d = json.loads(orig_cfg); d["thresholds"]["zzz_dead"] = 1; open(cp, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
l, s, _ = validate(base, "2026-09-27", st0927); rec("config 죽은 키", "thresholds.zzz_dead 추가", l, s, "죽은 키")
open(cp, "w", encoding="utf-8").write(orig_cfg)
# 3 단일 출처 (여러 변형)
def with_doc_append(path, text, label):
    p = f"{SB}/{path}"; keep = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(keep + "\n" + text + "\n")
    l, s, _ = validate(base, "2026-09-27", st0927); rec("임계값·색상 단일 출처", label, l, s, "단일 출처")
    open(p, "w", encoding="utf-8").write(keep)
with_doc_append("README.md", "발급기한은 익월 10일이다.", "README 끝에 '익월 10일' (b-4)")
with_doc_append("references/excel-format.md", "색은 FFEB9C 다.", "excel-format 끝에 FFEB9C (b-1)")
with_doc_append("README.md", "12월분은 1/10 까지.", "README 끝에 '1/10' (b-7)")
with_doc_append("references/judgment-rules.md", "| 매트릭스 | 시트 |", "judgment-rules 에 '| 매트릭스 |' 표 (b-5 문서)")
def with_code(path, old, new, label):
    p = f"{SB}/{path}"; keep = open(p, encoding="utf-8").read(); assert old in keep, old
    open(p, "w", encoding="utf-8").write(keep.replace(old, new, 1))
    l, s, _ = validate(base, "2026-09-27", st0927); rec("임계값·색상 단일 출처", label, l, s, "단일 출처")
    open(p, "w", encoding="utf-8").write(keep)
with_code("scripts/common.py", "for m in range(1, as_of.month + 1)]", "for m in range(1, 10)]", "common.py range(1, 10) (b-3)")
with_code("scripts/build_report.py", 'f["months_got"] >= th["monthly_min_months"]', 'f["months_got"] >= 6', "build_report monthly_min_months → 6 (b-6)")
with_code("scripts/build_report.py", 'ws = wb.create_sheet(cfg["sheets"]["missing"])', 'ws = wb.create_sheet("미수취목록")', "build_report create_sheet('미수취목록') (b-5 코드)")
with_code("scripts/build_report.py", 'ws.title = cfg["sheets"]["matrix"]', 'ws.title = "매트릭스"', "build_report ws.title = '매트릭스' (b-5 범위 밖?)")
# 4 시트 구성
p = mod(base, "sheet_renamed", lambda wb: setattr(wb[S["matrix"]], "title", "매트릭수"))
l, s, _ = validate(p, "2026-09-27", st0927); rec("시트 구성", "시트명 매트릭스→매트릭수", l, s, "시트 구성"); res.append(("  (요약)", "", " | ".join(l), s))
# 5 매트릭스 헤더 (실패 경로 전용)
def rename_hdr(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"]); ws.cell(r, m["공급자번호"]).value = "공급자 번호"
p = mod(base, "matrix_hdr", rename_hdr)
l, s, _ = validate(p, "2026-09-27", st0927); rec("매트릭스 헤더", "매트릭스 헤더 '공급자번호'→'공급자 번호'", l, s, "매트릭스 헤더"); res.append(("  (요약: 검사 개수 확인)", "", " | ".join(l), s))
# 6 매트릭스 월 컬럼
def m9(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"]); ws.cell(r, m["9월"]).value = "9 월"
p = mod(base, "month_hdr", m9)
l, s, _ = validate(p, "2026-09-27", st0927); rec("매트릭스 월 컬럼", "헤더 9월→'9 월'", l, s, "매트릭스 월 컬럼")
# 7 매트릭스 셀 검사 (실패 경로 전용) — 월 헤더 전부 제거
def nomonths(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"])
    for k, c in m.items():
        if k.endswith("월"): ws.cell(r, c).value = k.replace("월", "M")
p = mod(base, "no_month_cols", nomonths)
l, s, _ = validate(p, "2026-09-27", st0927); rec("매트릭스 셀 검사", "월 헤더 전부 '1M'… 로 (월 컬럼 0개)", l, s, "매트릭스 셀 검사"); res.append(("  (요약)", "", " | ".join(l), s))
# 8 미수취=공란
yellow = PatternFill("solid", fgColor=cfg["colors"]["cancelled"])
def blank_yellow(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"])
    for i in range(r+1, ws.max_row+1):
        c = ws.cell(i, m["2월"])
        if c.value is None: c.fill = yellow; return
p = mod(base, "blank_yellow", blank_yellow)
l, s, _ = validate(p, "2026-09-27", st0927); rec("미수취=공란 검사", "공란 한 칸에 취소색", l, s, "미수취=공란")
def blank_space(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"])
    for i in range(r+1, ws.max_row+1):
        c = ws.cell(i, m["2월"])
        if c.value is None: c.value = " "; return
p = mod(base, "blank_space", blank_space)
l, s, _ = validate(p, "2026-09-27", st0927); rec("미수취=공란 검사 (' ')", "공란 한 칸에 ' ' 문자", l, s, "월별 합 대사"); res.append(("  (같은 파일 미수취=공란 줄)", "", " | ".join(pick(l, "미수취=공란")), s))
# 9 전액취소
def zero_noyellow(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"])
    for row in ws.iter_rows(min_row=r+1):
        for c in row:
            if c.value == 0 and c.column >= 4: c.fill = PatternFill(fill_type=None); return
p = mod(base, "zero_noyellow", zero_noyellow)
l, s, _ = validate(p, "2026-09-27", st0927); rec("전액취소=0+노랑 검사", "0 칸 노랑 제거", l, s, "전액취소")
# 10 점검 대상 누락
def del_target(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "대상"])
    for i in range(r+1, ws.max_row+1):
        if ws.cell(i, m["대상"]).value == "점검대상": ws.delete_rows(i); return
p = mod(base, "del_target", del_target)
l, s, _ = validate(p, "2026-09-27", st0927); rec("점검 대상 누락 검사", "매트릭스 점검대상 1행 삭제", l, s, "점검 대상 누락")
# 11 합계 대사
def net_plus(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "순공급가액"]); ws.cell(r+1, m["순공급가액"]).value += 1
p = mod(base, "net_plus", net_plus)
l, s, _ = validate(p, "2026-09-27", st0927); rec("합계 대사", "순공급가액 +1", l, s, "합계 대사")
def net_space(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "순공급가액"]); ws.cell(r+1, m["순공급가액"]).value = " "
p = mod(base, "net_space", net_space)
l, s, _ = validate(p, "2026-09-27", st0927); rec("합계 대사 (' ')", "순공급가액 칸에 ' '", l, s, "합계 대사")
# 12 월별 합
def swap15(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"])
    for i in range(r+1, ws.max_row+1):
        a, b = ws.cell(i, m["1월"]).value, ws.cell(i, m["5월"]).value
        if a and b and a != b:
            ws.cell(i, m["1월"]).value, ws.cell(i, m["5월"]).value = b, a; return
p = mod(base, "swap15", swap15)
l, s, _ = validate(p, "2026-09-27", st0927); rec("월별 합 대사", "한 행의 1월↔5월 교환(총합 유지)", l, s, "월별 합 대사")
# 13 원본 행수
p = mod(base, "raw_del", lambda wb: wb[S["raw"]].delete_rows(wb[S["raw"]].max_row))
l, s, _ = validate(p, "2026-09-27", st0927); rec("원본 행수", "원본정제 마지막 행 삭제", l, s, "원본 행수")
# 14 승인번호 중복
def dup_appr(wb):
    ws = wb[S["raw"]]; r, m = hdr(ws, ["승인번호"]); ws.cell(3, m["승인번호"]).value = ws.cell(2, m["승인번호"]).value
p = mod(base, "dup_appr", dup_appr)
l, s, _ = validate(p, "2026-09-27", st0927); rec("승인번호 중복", "승인번호 1건 복제", l, s, "승인번호 중복")
# 15 상계 매칭
def unpair(wb):
    ws = wb[S["raw"]]; r, m = hdr(ws, ["상계처리"])
    for i in range(r+1, ws.max_row+1):
        if str(ws.cell(i, m["상계처리"]).value).startswith("취소분"): ws.cell(i, m["상계처리"]).value = "-"; return
p = mod(base, "unpair", unpair)
l, s, _ = validate(p, "2026-09-27", st0927); rec("상계 매칭", "'취소분(상계)' 1건 → '-'", l, s, "상계 매칭")
# 16 대상외
def unl_vendor(wb):
    ws = wb[S["unlisted"]]; r, m = hdr(ws, ["공급자번호", "추가 권장"]); ws.cell(r+1, m["공급자번호"]).value = "119-86-87135"
p = mod(base, "unl_vendor", unl_vendor)
l, s, _ = validate(p, "2026-09-27", st0927); rec("대상외공급자 시트", "시트 공급자번호를 vendors 것(바로고)으로", l, s, "대상외공급자")
# 17 등급 분류
def bad_grade(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급"]); ws.cell(r+1, m["등급"]).value = "이상등급"
p = mod(base, "bad_grade", bad_grade)
l, s, _ = validate(p, "2026-09-27", st0927); rec("등급 분류", "등급값 '이상등급'", l, s, "등급 분류")
def gap_has_value(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급", "누락된 월"])
    for i in range(r+1, ws.max_row+1):
        if ws.cell(i, m["등급"]).value == "확인 필요" and ws.cell(i, m["누락된 월"]).value == "8월":
            ws.cell(i, m["누락된 월"]).value = "1월"; return
p = mod(base, "gap_value", gap_has_value)
l, s, _ = validate(p, "2026-09-27", st0927); rec("등급 분류", "확인 필요 행 결번월 8월→값 있는 1월", l, s, "등급 분류")
def unsorted(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급"]); ws.cell(r+1, m["등급"]).value = "정상"
p = mod(base, "unsorted", unsorted)
l, s, _ = validate(p, "2026-09-27", st0927); rec("등급 분류", "첫 행 등급을 '정상' 으로(정렬 뒤집힘)", l, s, "등급 분류")
# 17b 등급 재산출 대조 (7차 신설)
def del_row(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급"]); ws.delete_rows(r + 1)
p = mod(base, "row_del", del_row)
l, s, _ = validate(p, "2026-09-27", st0927); rec("등급 재산출 대조", "미수취목록 첫 데이터 행 삭제", l, s, "등급 재산출")
def dup_row(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급"]); ws.append([c.value for c in ws[r + 1]])
p = mod(base, "row_dup", dup_row)
l, s, _ = validate(p, "2026-09-27", st0927); rec("등급 재산출 대조", "미수취목록 첫 데이터 행 복제(끝에 추가)", l, s, "등급 재산출")
def swap_grade(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급"])
    for i in range(r + 1, ws.max_row + 1):
        if ws.cell(i, m["등급"]).value == "정상": ws.cell(i, m["등급"]).value = "단발·비정기"; return
p = mod(base, "grade_swap", swap_grade)
l, s, _ = validate(p, "2026-09-27", st0927); rec("등급 재산출 대조", "'정상' 한 행의 등급을 '단발·비정기' 로(정렬은 유지)", l, s, "등급 재산출")
l, s, _ = validate(jan, "2026-01-05", st0105); rec("등급 재산출 대조 (1월 산출물)", "무변경 — 기대 0 · 시트 0 경로", l, s, "등급 재산출")
# 18 실행 이력 비교
st = json.load(open(st0927, encoding="utf-8")); st2 = copy.deepcopy(st); st2["flagged"] = st2["flagged"][:1]
tmp = f"{OUT}/state_1.json"; json.dump(st2, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
l, s, _ = validate(base, "2026-09-27", tmp); rec("실행 이력 비교", "state flagged 9→1", l, s, "실행 이력 비교")
# 19 해결 집계 (1월 산출물, 해결 3)
def clear_status(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급", "상태"])
    for i in range(r+1, ws.max_row+1):
        if ws.cell(i, m["등급"]).value == "해결": ws.cell(i, m["상태"]).value = None; return
p = mod(jan, "jan_clear_status", clear_status)
l, s, _ = validate(p, "2026-01-05", BACKUP); rec("해결 집계", "1월 산출물 해결 행의 상태 비움 (state=3곳 이력)", l, s, "해결 집계")
l, s, _ = validate(p, "2026-01-05", BACKUP); res.append(("  (같은 파일 실행 이력 비교 줄)", "", " | ".join(pick(l, "실행 이력")), s))
# 20 발급기한 유예
l, s, _ = validate(base, "2026-09-27", st0927); rec("발급기한 유예 (9/27 기준)", "무변경 — 8월분 기한(9/10) 경과, 기대 0=0", l, s, "발급기한 유예")
def all_normal(wb):
    ws = wb[S["missing"]]; r, m = hdr(ws, ["등급"])
    for i in range(r+1, ws.max_row+1):
        if ws.cell(i, m["등급"]).value == "기한 전": ws.cell(i, m["등급"]).value = "정상"
p = mod(sep06, "sep06_all_normal", all_normal)
l, s, _ = validate(p, "2026-09-06", st0906); rec("발급기한 유예 (9/6 산출물)", "'기한 전' 전부 → '정상'", l, s, "발급기한 유예")
def strip_grace(wb):
    ws = wb[S["matrix"]]; r, m = hdr(ws, ["공급자번호", "상호"])
    for i in range(r+1, ws.max_row+1): ws.cell(i, m["전년 12월"]).fill = PatternFill(fill_type=None)
p = mod(jan, "jan_strip_grace", strip_grace)
l, s, _ = validate(p, "2026-01-05", BACKUP); rec("발급기한 유예 (1월 산출물)", "전년 12월 열 유예 색 전부 제거", l, s, "발급기한 유예")
l, s, _ = validate(base, "2026-09-27", st0927, extra=["--strict"]); rec("발급기한 유예 (--strict 검증)", "auto 산출물을 --strict 로 검증", l, s, "발급기한 유예")

shutil.copy(BACKUP, f"{SB}/state/last-run.json")
print("| 검사 | 파괴 방법 | 결과 줄 | 요약 |"); print("|---|---|---|---|")
for c, h, r, s in res:
    print(f"| {c} | {h} | {r[:150]} | {s} |")
```

---

## 이전 기록 (6차 정기점검 + 후속 조치 1~4차, 2026-09-07 — 원문 보존)

# 점검 기준선

> **6차 정기점검 (2026-09-07).** 진단 시점에는 고치지 않았고, 같은 날 저녁
> 사용자 승인 후 결함 10건·개선안 4건을 처리했다 — 아래 "6차 후속 조치" 참조.
> 이월이었던 #15 · #18 · 개선안 4 도 같은 날 심야에 종결 — "6차 후속 2차" 참조.
> 진단 시점의 기록은 아래 그대로 보존한다.

> **주의 — 같은 날 두 번 진행했다.** 1차 패스(2026-09-07 01:2x~01:4x UTC)는 진단을 끝내고
> 이 파일과 `checklist.md` 초안을 컨테이너에 만들었으나 **저장소에 push 되지 않았다**
> (토큰 없이 세션이 끝남). 2차 패스(04:1x UTC~)에서 codeload 로 다시 받아 **모든 실측을
> 재수행**했고(결과 전부 동일 — 커밋 `8adae14760` 불변), 그 결과로 이 파일을 저장했다.
> 컨테이너 `/home/claude/hometax/` 에 1차 패스 잔존물이 남아 있어 발견했다. 원격 `audit/`
> 에는 `last-audit.md` 하나뿐이었다(GitHub tree API 로 확인). 교훈은 "점검표 개정안" 10·11번.

점검일: 2026-09-07 (6차 — 정기점검)
직전: 2026-09-06 5차 정기점검 + 같은 날 6차 실사용 실행 (기준선 항목: 이월 결함 12 · 해결 8 · 개선안 5 · 대조 항목 6 · 운영 주의 1)

**재확인 결과: 해결됨 10건 / 미해결 15건 / 근거없음 0건 / 신규 2건**
결함 14건 (이월 12 + 신규 2) / 개선안 5건 / 인용불가로 제외 0건

> **미해결 15건 전부 '미착수'다.** 기준선에 '수정함' 표시가 있는데 미해결로 나온
> 항목은 0건. 5차가 고친 8건(#26 #13 N1 N2 N3 #11 #25 #12)과 개선안 2건은 실물에
> 그대로 있다. 설치본 ↔ `install/SKILL.md` 도 개행 1자 외 차이 없음 — 드리프트 없음.

## 이번 회차 실측 조건

| | 값 |
|---|---|
| 받은 커밋 | `8adae14760` (2026-09-06T12:55Z) "유성빌딩 점검 대상 제외 + audit: 결함 #29 #30 기록" |
| 실 데이터 | **있음 (2026-09-07 사후 정정).** 업로드 6개는 `tests/fixtures/` 와 바이트 동일(md5 6/6)이나, 이는 **fixtures 자체가 사용자의 실제 홈택스 다운로드본**이기 때문이다. 실 데이터가 맞다. 내용 확인: 사업자 239-86-03249, 작성일자 `2026-01-01 ~ 2026-08-31`, 441건. 최종일이 오늘(09-07)로부터 7일 전이라 **당월(9월) 월 컬럼 생성·당월분 기한 임박 판정 2건만 [추론]**이고, 형식 변경·신규 거래처·사업자번호 변경·vendors 대조·체크섬·상계 매칭은 실자료 실측이다. 점검 당시 "실 데이터 없음"으로 기록한 것은 오판이었다 |
| 실행한 `--as-of` | 없음(오늘 2026-09-07) / `2026-01-05` / `2027-01-05`(점검표 지시. 아래 개정안 참조) / `--strict --no-state` |
| 파일 행수 | SKILL.md 360 · install/SKILL.md 55 · README.md 64 · sync.py 126 · check-config.json 88 · vendors.json 191(30곳) · column-mapping.md 91 · excel-format.md 72 · judgment-rules.md 126 · common.py 354 · check_input.py 253 · build_report.py 614 · validate.py 690 · push.py 319 · last-run.json 25 · test_edge_cases.py 639(t_ 23개) · last-audit.md 387(직전) |
| ls 대조 | 점검표 목록과 일치(23파일 = push 대상 23). 목록 밖 파일은 `.gitignore` 하나(sync.py 가 일부러 건너뜀). `audit/checklist.md` 는 이번 회차에 신설 — **1차 패스 시점에는 원격에 없었다** |
| md5 | 설치본 `c732414e88931f0ec219b51e292e5d15` / `install/SKILL.md` `6f686b5721644381382be801a939c92d` — diff 는 마지막 줄 개행 1자만. 설치본에 절차·옵션·등급명 없음 ✓ |

| 실행 | 결과 |
|---|---|
| `check_input` 9/7 | FAIL 0 · WARN 1(제이푸드 사업자 변경 — 이미 until/since 처리된 건인데 매번 다시 뜬다) · 441건 · 공급자 51곳 · 체크섬 30/30 |
| `build_report` 9/7 기본 | 확인 필요 **3** · 기한 전 6 · 단발 1 · 정상 3 · 거래 종료 4 · 해결 0 · 상계 6쌍 · 매출분 제외 0 · 기간 밖 0 · 점검대상 30 / 대상외 21 · 기한 임박 "8월분 2026-09-10 (D-3) 미수취 8곳" |
| `validate` 9/7 | **FAIL 0 · SKIP 1(해결 집계) · PASS 17** |
| `--as-of 2026-01-05` | 대상 월 `전년 12월~1월` · 5건 · 확인 필요 0 · 해결 3 · validate FAIL 0 · SKIP 2 · PASS 16 · `'기한 전' 0건 (전월 유예 구간: False)` PASS |
| `--as-of 2027-01-05` | `check_input` **FAIL** `점검 기간 작성분이 한 건도 없음` (fixtures 는 2026년 자료라 당연) · build_report 는 그대로 돌아 총 0건 · 해결 3 리포트를 만든다 |
| `--strict` (`--no-state`) | 확인 필요 **9** · 기한 전 0 (5차 10 → 유성빌딩 제거로 9) · validate `--strict` FAIL 0 · SKIP 3 · PASS 15 |
| `test_edge_cases.py` | 실패 0 · exit 0 |
| 테스트 게이트 | 1차 패스: `common.py` 에 `range(1, 10)` 주입 → `push.py <토큰> --code` **main() 경로** 실제 실행 → 업로드 없이 return 1, 원격 common.py md5 `e83a0644…` 불변. 2차 패스: 같은 주입으로 `run_tests()` 함수 단위 재확인 → **실패 41건 · False**, 복구 후 True. **5차 미실측 항목 4번 해소** |
| state 역행 가드 | 과거날짜 / 같은날 감소 / 원격깨짐 3케이스 모두 차단 메시지 · 정상 전진은 None |
| push `GROUPS` 커버리지 | 저장소 실제 파일 대비 누락 0 · 유령 0 (`.gitignore` 제외) |
| config / vendors / state 파일 삭제·손상 | 셋 다 `[중단] …` 로 명시적 정지(config: `설정(check-config.json) 파일이 없습니다` · vendors `[]`: `'vendors' 키가 없습니다` · state `{broken`: `1행 2열 — Expecting property name…` 안내). 조용한 기본값 없음. 단 `{"vendors": []}` 는 **중단 없이** `점검대상 0곳 / 대상외 51곳` 리포트를 만든다(개선안 3 에 합침) |
| 홈택스 파일 0개 | `[중단] … 홈택스 파일(.xls)이 없습니다.` |
| first_seen | 9/7 재실행 후 3곳 모두 `2026-09-06` 유지(누적됨). 상태 `계속` |
| 산출물 직접 확인 | 시트 4개 · 매트릭스 헤더 5행(4행 신고기 밴드 1기×6/2기×3) · 1~9월 9열 · 미수취목록 17행 · 대상외 21곳 · 유성빌딩 `추가 권장 (정기성)` 으로 계속 뜸(5차 결정대로 **사용자에게 묻지 않았다**) |

---

## 직전 기준선 판정 (25건 + 운영 주의 1)

### 이월 결함 12건 — 전부 미해결 (지난 회차가 의도적으로 이월한 것. '수정함' 표시 없음)

| # | 판정 | 근거(지금 원문) |
|---|---|---|
| 5 | **미해결** [실측] | `validate.py` 500-501 `prev = as_of.month - 1` / `expect = prev >= 1 and is_in_grace(as_of.year, prev, as_of, cfg)` — 1월 산출물에서 '기한 전' 을 전부 '정상' 으로 바꿔도 **PASS** (`'기한 전' 0건 (전월 유예 구간: False)`). 9월 산출물에서는 같은 파괴로 FAIL. 즉 1월에만 죽는 검사 |
| 28 | **미해결** [실측] | `build_report.py` 122 `monthly = f["cycle"] == "매월" or f["months_got"] >= th["monthly_min_months"]` / 162 `elif f["cycle"] == "비정기" or …`. 비앤지 cycle→`비정기` 로 바꿔 재실행 → 여전히 `확인 필요` (주기 열만 '비정기' 로 바뀜) |
| 29 | **미해결** [실측] | `build_report.py` 74 `out_of_scope = not (lo <= m <= hi)` / 84 `state = "cancelled" if len(lv) == 0 else "ok"` / 135 `elif f["cancelled"]:` / 154 `if f["ended"]:`. 유성빌딩을 `until: 2026-03` 으로 다시 넣어 실행 → `A. 발행 후 전액취소 · 확인 필요` 그대로(확인 필요 3→4) |
| 20 | **미해결** [실측] | `build_report.py` 334 `ws["A1"] = f"공급자 × 월 매입 발급 매트릭스 ({as_of.year}-01-01 ~ {as_of})"`. `--as-of 2026-01-05` 산출물 A1 = `(2026-01-01 ~ 2026-01-05)`, 헤더는 `전년 12월 / 1월` |
| 30 | **미해결** [실측] | `build_report.py` 268-278 `for bid, p in prev_map.items(): … rows.append({"kind": "해결됨", "grade": "해결", …` / `validate.py` 370-371 `if sid not in listed: bad.append(f"{i}행: vendors.json 에 없는 공급자 {sid}")`. state 에 미등록 2120459010 을 넣고 실행 → 해결 1 · validate `[FAIL] 등급 분류 이상 1건 / 22행: vendors.json 에 없는 공급자 2120459010` 재현 |
| 16 | **미해결** | `validate.py` 349-350 `order = {"확인 필요": 0, "기한 전": 1, "단발·비정기": 2, "정상": 3, "거래 종료": 4, "해결": 5}` — `build_report.GRADE_ORDER`(29-30) 사본 그대로 |
| 14 | **미해결** | `references/excel-format.md` 15-18 `\| 1 \| 매트릭스 \| 공급자 × 월. 점검대상 먼저, 대상외 나중 \|` … 4행. 11행 `시트 이름도 config(sheets)에서 읽는다` 와 병존 |
| 15 | **미해결** | `references/column-mapping.md` 5 `여기에 다시 적지 않는다 — config/check-config.json 의 input 블록이 유일한 출처다.` / 32-37 `\| 공급자 식별 \| \`공급자사업자등록번호\` \|` … |
| 27 | **미해결** | `SKILL.md` 227 `\| \`--force\` \| 실행 이력이 뒤로 가도 강행. **쓰지 않는다** (아래 참고) \|` / 231-232 `이게 걸리면 \`--force\` 로 뚫지 말고 **\`sync.py\` 로 최신본을 받은 폴더에서 다시 실행한다.**` / `push.py` 271-276 가드 메시지에 "의도적 거래처 제거" 분기 없음. 5차가 실사용으로 검증한 3단계 절차가 아직 문서에 없다 |
| 21 | **미해결** [실측] | `build_report.py` 337 `f"빈칸=미수취 · 노랑=발행 후 전액취소 · 연파랑=발급기한 전")` — 9/7 산출물 A2 에 그대로 찍힘 |
| 18 | **미해결** | `check_input.py` 156-157 `if v.get("until"):` / `    continue` — 결함/설계 판단 3회차 연속 미결 |
| 19 | **미해결** [실측] | `check_input.py` 249 `"\n변경이라면 vendors.json 에서 구 번호를 지우고 신 번호로 교체할 것."` — 9/7 실행 WARN 에 그대로 출력. SKILL.md 279 · judgment-rules 102 는 `구 번호에 until, 신 번호에 since`. 게다가 제이푸드는 이미 그렇게 처리돼 있는데 WARN 이 매 회차 다시 뜬다 |

### 5차에 해결한 8건 — 해결됨 유지

| # | 판정 | 근거(지금 원문) |
|---|---|---|
| 26 | 해결됨 | `common.py` 147 `def is_resolved(grade, status):` / 161 `return grade == "해결" or status == "해결"` · `build_report.py` 570-571 · `validate.py` 422, 469 에서 호출 |
| 13 | 해결됨 | `validate.py` 563 `for rel in ["references", "install", ""]:` · 9/7 결과 `스크립트 5개 · 문서 6개에 하드코딩 없음` |
| N1 | 해결됨 | `SKILL.md` 343 `SKILL.md                   이 파일. **정본 설명서.** 설치 경로에 넣는 건 install/SKILL.md 다` |
| N2 | 해결됨 | `README.md` 12-13 `2. Claude 스킬 폴더에 **\`install/SKILL.md\`** 만 넣는다. 절차·옵션·등급이 없는 얇은` |
| N3 | 해결됨 | `README.md` 28 `python3 -c "import xlrd" 2>/dev/null \|\| pip install xlrd --break-system-packages -q` |
| 11 | 해결됨 | `SKILL.md` 31 `세금계산서 발급기한은 작성월 다음 달의 정해진 날짜다(\`config\` 의 \`grace.deadline_day\`).` |
| 25 | 해결됨 | `SKILL.md` 166 `\| \`기한 전\` \| 발급기한이 아직 남음 \| 기다린다 \|` |
| 12 | 해결됨 | `SKILL.md` 287 `→ 발급기한 전이라 정상이다. 등급이 \`기한 전\`이면 기다리면 된다.` |

### 개선안 5건

| # | 판정 | 근거(지금 원문) |
|---|---|---|
| 1 단일출처 스캔 확대 | 해결됨 | `validate.py` 563 (위 #13 과 동일). README 에 `10일` 을 되살리자 `[FAIL] 단일 출처 위반 1곳` — 살아 있음 |
| 2 해결 집계 대사 | 해결됨 | `validate.py` 435 `def check_resolved(wb, cfg):` · 1월 산출물에서 해결 행 상태를 비우자 FAIL |
| 3 `--add-vendor` | 미해결 | `push.py` 233-243 add_argument 에 없음. `_print_reco()`(build_report 602) 는 여전히 콘솔 출력만 |
| 4 check_paths 에 audit/install | 미해결 | `validate.py` 515-521 `want = ["SKILL.md", "README.md", "sync.py", … "tests/test_edge_cases.py"]` — `audit/last-audit.md` · `install/SKILL.md` 없음 |
| 5 홈택스 0개 테스트 | 미해결 | `tests/test_edge_cases.py` 에 빈 업로드 폴더 케이스 없음(grep `파일이 없` 0건). 코드 동작은 실측 정상 |

### "다음 점검에서 대조할 것" 6건

| # | 판정 | 근거 |
|---|---|---|
| 1 #5 수정 후 1월 FAIL 0 유지? | 미해결(전제 미충족) | #5 자체가 미수정. 1월 산출물 '기한 전' 은 구조상 0건(수취 0건 거래처는 C 루프 미진입)임을 다시 확인 — 고칠 때 판정 조건도 함께 바꿔야 함 |
| 2 check_resolved 실사용 대조 | **미실측** | 이번에도 해결 0 → `[SKIP] 해결 집계`. 실자료도 fixtures 와 동일해 밟을 수 없었다 |
| 3 단일출처 확대 부작용 | 확인됨(문제 없음) | 문서 6개 스캔 오탐 0. `audit/` 제외 판단 유효 — 이번에 `audit/checklist.md` 가 추가되며 "10일" 리터럴이 문서에 들어갔는데 스캔 대상이 아니라 FAIL 안 남 |
| 4 테스트 게이트 main() 경로 | **해결됨(실측)** | 위 실측 조건 표 참조. 차단 후 원격 불변 확인 |
| 5 #18 결정 | 미결 | 사용자 결정 대기 |
| 6 #28 방향 결정 | 미결 | 사용자 결정 대기. 재현은 이번에도 됨 |

### 운영 주의(5차)

| 항목 | 판정 |
|---|---|
| 유성빌딩 재권유 금지 | 준수. 콘솔·시트에 `추가 권장 (정기성) · 6,000,000원` 으로 떴고 사용자에게 묻지 않았다. #29 '다' 안 반영 전까지 계속 뜬다 |

---

## 결함 (14건 — 이월 12 + 신규 2)

심각도 순. 이월 항목의 원문은 위 판정표에 있으므로 여기서는 행만 잇는다.
월 의존 재평가: 오늘 9월. #5 #20 은 **다음 1월 실행(2027-01) 전**에 반드시 처리. 남은 정기점검 회차가 3~4회라 이번엔 '높음' 유지, 12월 회차에는 1순위.

| # | 심각도 | 파일 | 줄 | 문제 원문(그대로) | 실측/추론 | 왜 틀렸는지 | 수정 방향 | 작업경로 |
|---|---|---|---|---|---|---|---|---|
| 5 | **높음** | `scripts/validate.py` | 500-501 | `prev = as_of.month - 1` / `expect = prev >= 1 and …` | [실측] | 1월 실행이면 `prev=0` → `expect=False` → 무조건 PASS. 이번 회차 파괴 실험에서 **1월 산출물은 어떻게 깨뜨려도 PASS** | `prev` 를 `month_range(as_of)[-2]` 로. 단, 1월은 '기한 전' 0 이 정상 구조이므로 FAIL 조건을 "매트릭스에 grace 색 칸이 0" 같은 다른 신호로 잡아야 한다 | `push.py --code` |
| 28 | **높음** | `scripts/build_report.py` | 122 / 162 | `monthly = f["cycle"] == "매월" or f["months_got"] >= th["monthly_min_months"]` | [실측] | `비정기` 라벨이 A 경로에서 무시됨. 라벨 바꿔도 등급 불변 | 가/나/다 중 사용자 결정 후 수정 + `비정기`+수취 6개월 회귀 테스트 | `push.py --code` |
| 29 | **높음** | `scripts/build_report.py` | 74 / 84 / 135 / 154 | `out_of_scope = not (lo <= m <= hi)` … `if f["ended"]:` | [실측] | 전액취소 거래처에 `until` 이 안 듣는다. SKILL.md 169·291 의 안내가 거짓 | 가(`ended` 를 A 루프 앞으로) + 다(`ignore` 필드/제외 목록, `_print_reco` 도 존중) | `push.py --code` + vendors.json |
| 20 | **높음↑** (월 의존) | `scripts/build_report.py` | 334 | `({as_of.year}-01-01 ~ {as_of})` | [실측] | 1월 A1 이 전년 12월 열을 빼고 표기 | `months[0]` 을 `month_label` 로 | `push.py --code` |
| 30 | 중간 | `scripts/build_report.py` / `scripts/validate.py` | 268-278 / 370-371 | `rows.append({"kind": "해결됨", "grade": "해결", …` / `if sid not in listed:` | [실측] | 목록에서 지운 거래처가 `해결` 로 생성되고 validate 가 FAIL. 제거≠해결 | `apply_state` 는 미등록 공급자를 `해결` 로 만들지 않음 + `check_grades` 는 `해결` 등급에 한해 미등록 허용 | `push.py --code` |
| N4 | 중간 | `references/judgment-rules.md` | 46 | `실행 당월은 **모드와 무관하게** 유예 상태다(9/6에 9월분 기한은 10/10).` | [실측] | 같은 문서 5행 `**이 문서에 숫자를 적지 않는다.**` 와 모순. `grace.deadline_day` 사본인데 `10/10` 날짜 표기라 validate (b-4) 정규식 `10\s*일` 을 피해간다. 5차에 SKILL.md 사본 3곳을 지웠는데 references 에 1곳이 남아 있었다 | `(9/6 실행이면 9월분 기한은 10월의 deadline_day)` 로. 필요하면 (b-4) 패턴에 `/{val}\b` 추가 | `push.py --code` |
| 16 | 중간 | `scripts/validate.py` | 349-350 | `order = {"확인 필요": 0, …}` | [추론] 등급을 늘린 적이 없어 어긋난 실물은 없음 | GRADE_ORDER 사본 | `from build_report import GRADE_ORDER` | `push.py --code` |
| 14 | 중간 | `references/excel-format.md` | 15-18 | `\| 1 \| 매트릭스 \| …` | [실측] 검사 확대 실험 참조 | 시트명 리터럴 4개 | config 키로 교체. **개선안 1 과 같은 회차에** | `push.py --code` |
| 15 | 중간 | `references/column-mapping.md` | 5, 32-37 | `여기에 다시 적지 않는다` / 컬럼명 표 | [추론] | 선언과 표 모순 | 5행 선언을 현실화하거나 표를 키 참조로 | `push.py --code` |
| 27 | 중간 | `SKILL.md` / `scripts/push.py` | 227, 231-232 / 271-276 | `이게 걸리면 \`--force\` 로 뚫지 말고 **\`sync.py\` 로 …** ` | [추론] 5차 실사용에서 실측된 상황 | 의도적 제거로 줄어든 경우 안내가 막다른 길. 5차가 밟은 3단계가 문서화되지 않음 | SKILL.md 에 3단계 예외 절차, push.py 가드 메시지에 한 줄 | `push.py --code` |
| 21 | 중간 | `scripts/build_report.py` | 337 | `f"빈칸=미수취 · 노랑=발행 후 전액취소 · 연파랑=발급기한 전")` | [실측] | 색 이름이 문자열 고정. config 색을 바꾸면 A2 가 거짓 | 색 이름 제거 또는 config 라벨 | `push.py --code` |
| N6 | 낮음 | `scripts/validate.py` | 71 (및 92, 135, 156 …) | `ws = wb[cfg["sheets"]["matrix"]]` | [실측] | 시트명이 config 와 다르면 `check_sheets` 가 FAIL 을 **기록**하지만 바로 다음 검사에서 `KeyError: 'Worksheet 매트릭스 does not exist.'` 로 죽어 **요약이 한 줄도 출력되지 않는다.** exit 는 비정상이라 조용한 PASS 는 아니지만, SKILL.md 146 "검사 대상을 못 찾음도 FAIL 이다" 가 표시되지 않는다. 같은 유형으로 매트릭스 월 칸에 문자열(`' '`)이 들어가면 `check_totals` 162 `sum(... or 0)` 에서 TypeError | `check_sheets` 가 FAIL 이면 이후 시트 의존 검사를 건너뛰고 요약을 찍는다; 셀 합산은 숫자만 | `push.py --code` |
| 18 | 낮음 | `scripts/check_input.py` | 156-157 | `if v.get("until"):` / `continue` | [추론] | `until` 오입력 거래처의 주기 이상을 영영 못 잡음(설계 주석 있음) | `until` 이 과거일 때만 skip — **사용자 결정 필요** | `push.py --code` |
| 19 | 낮음 | `scripts/check_input.py` | 249 | `구 번호를 지우고 신 번호로 교체할 것.` | [실측] | 문서·실제 vendors.json 과 반대. 처리 완료 건도 매 회차 재경고 | 문구 교체 + 이미 `until`/`since` 로 짝지어진 쌍은 WARN 제외 | `push.py --code` |

### 통과 처리 (인용은 되나 결함으로 올리지 않음) — 6건

- `build_report.py` 8 `3. 발급기한(익월 10일)이 안 지난 달은 미수취로 확정하지 않는다.` · `check_input.py` 124 `기한이 익년 1/10 이라` · `common.py` 82 `12월분 발급기한은 익년 1/10 이라` — 모듈 독스트링 안의 `deadline_day` 사본 3곳. validate 542-549 가 독스트링을 **일부러** 스캔에서 뺀다(설계). 다만 N4 를 고칠 때 같이 고치는 게 싸다
- `validate.check_matrix_blank_and_fill` 109 `if c.value is None:` — 빈 문자열 `''` 은 공란도 0 도 아니라 조용히 건너뛴다(메모리상 240→239 확인). 그러나 openpyxl 은 `''` 을 저장하면서 None 으로 바꾸므로 **디스크 파일에 그 조건을 만들 수 없다.** 공백 `' '` 은 N6 의 TypeError 로 죽는다(조용한 통과 아님)
- `sync.py` 72 `ap.add_argument("--with-tests", action="store_true", help=argparse.SUPPRESS)` — 문서에 없는 옵션이지만 no-op 호환 플래그. 안전장치와 무관
- `validate.check_state` 401 `find_header_row(ws, ["등급"])` 만 요구하고 418 에서 `m["공급자번호"]` 사용 — 산출물이 두 열을 항상 함께 만들어 발생 조건 없음(4·5차와 동일)
- `check_input.py` 132 `if day > 10:` — deadline_day 와 무관한 별개 휴리스틱(5차 판정 유지)
- `SKILL.md` 258-259 vendors 예시의 `"until": null` — 실제 파일은 키를 생략하지만 코드가 `v.get("until")` 이라 동작 동일

**인용불가로 제외: 0건.**

---

## 개선안 (최대 5)

| # | 내용 | 이유 | 우선순위 |
|---|---|---|---|
| 1 | 단일 출처 검사(validate 530-630)를 **시트명 리터럴 · thresholds 숫자 리터럴(코드 포함) · `N/DD` 날짜형 deadline 표기**까지 확대 | 이번 실측: `build_report.py` 의 `cfg["sheets"]["matrix"]` 를 `"매트릭스"` 로, `th["monthly_min_months"]` 를 `6` 으로 바꿔도 **PASS**. N4 의 `10/10` 도 안 걸림. **#14 #15 N4 와 같은 회차에** 해야 함(확대하는 순간 셋이 FAIL 로 떠 push 가 막힌다) | **1** |
| 2 | `check_paths` 에 `audit/last-audit.md` · `audit/checklist.md` · `install/SKILL.md` 추가 (5차 #4 승계) | 점검표 정본이 저장소로 들어왔다. 둘 중 하나가 없으면 다음 회차 절차가 조용히 절반 유실된다 | 2 |
| 3 | `build_report.py` 가 기간 안 데이터 0건 **또는 점검대상 0곳**이면 `[중단]` (또는 강한 WARN) | `--as-of 2027-01-05` 실측: check_input 은 FAIL 인데 build_report 는 총 0건으로 리포트를 만들고 직전 확인 필요 3곳을 전부 `해결` 로 표기. SKILL.md 104 절차(FAIL 이면 만들지 말 것)를 건너뛰면 "자료 없음 = 해결" 이 된다 | 3 |
| 4 | `push.py --add-vendor` (5차 #3 승계) | `_print_reco()` 가 목록을 이미 만든다. #29 '다' 안(제외 목록)과 같이 설계하면 유성빌딩 재권유도 함께 끝난다 | 4 |
| 5 | `test_edge_cases.py` 에 홈택스 파일 0개 케이스 (5차 #5 승계) | J 항목 중 유일하게 테스트 없음. 동작은 실측 정상 | 5 |

---

## validate.py 검사 생존 확인 (18개 검사 · 파괴 27회)

기준: fixtures 로 9/7 산출물(FAIL 0 · SKIP 1 · PASS 17)과 `--as-of 2026-01-05` 산출물을 만든 뒤 한 곳씩 바꿔 재검증. 표시된 결과는 해당 검사의 판정.

| 검사 | 파괴 방법 | 결과 |
|---|---|---|
| 경로 존재 확인 | `README.md` 임시 제거 | FAIL ✓ |
| config 죽은 키 | config 에 `thresholds.zzz_dead: 1` 추가 | FAIL ✓ |
| 임계값·색상 단일 출처 | README 끝에 `발급기한은 익월 10일이다.` | FAIL ✓ |
| 〃 | excel-format.md 끝에 `FFEB9C` | FAIL ✓ |
| 〃 | common.py 끝에 `range(1, 10)` | FAIL ✓ |
| 〃 | build_report `cfg["sheets"]["matrix"]` → `"매트릭스"` | **PASS ✗ (검사 범위 밖 — 개선안 1)** |
| 〃 | build_report `th["monthly_min_months"]` → `6` | **PASS ✗ (검사 범위 밖 — 개선안 1)** |
| 시트 구성 | 시트명 `매트릭스`→`매트릭수` | FAIL 기록되나 **다음 검사 KeyError 로 크래시, 요약 미출력 (결함 N6)** |
| 매트릭스 월 컬럼 | 헤더 `9월`→`9 월` | FAIL ✓ |
| 미수취=공란 | 공란 한 칸에 취소색 | FAIL ✓ |
| 〃 | 공란 240칸 전부 `''` | PASS — openpyxl 저장 시 None 으로 환원되어 조건 성립 불가(통과 처리) |
| 〃 | 공란 한 칸에 `' '` | check_totals TypeError 크래시(N6) |
| 전액취소=0+노랑 | 0 칸 노랑 제거 | FAIL ✓ |
| 점검 대상 누락 | 매트릭스 점검대상 1행 삭제 | FAIL ✓ (합계·월별도 함께 FAIL) |
| 합계 대사 | 순공급가액 +1 | FAIL ✓ |
| 월별 합 대사 | 한 행의 1월↔5월 교환(총합 유지) | FAIL ✓ `불일치 2개월` |
| 원본 행수 | 원본정제 마지막 행 삭제 | FAIL ✓ |
| 승인번호 중복 | 승인번호 1건 복제 | FAIL ✓ |
| 상계 매칭 | `취소분(상계)` 1건 → `-` | FAIL ✓ |
| 대상외공급자 시트 | 시트 공급자번호를 vendors 것으로 | FAIL ✓ |
| 등급 분류 | 등급값 `이상등급` | FAIL ✓ |
| 〃 | 확인 필요 행 결번월을 값 있는 `1월` 로 | FAIL ✓ |
| 실행 이력 비교 | state flagged 3→1 | FAIL ✓ |
| 해결 집계 (1월 산출물) | 해결 행의 상태 비움 | FAIL ✓ |
| 발급기한 유예 (9월) | 기한 전 전부 → 정상 | FAIL ✓ |
| 발급기한 유예 (1월, `--as-of 2026-01-05`) | 같은 파괴 | **PASS ✗ (결함 #5 — 1월엔 죽은 검사)** |

재현 스크립트는 남기지 않았다(설치 경로는 보존 안 됨). 위 표대로 openpyxl 로 한 칸씩 바꾸면 그대로 재현된다. 주의: `--strict --no-state` 로 돌리면 **같은 파일명에 덮어쓰므로** 파괴 실험 기준 파일은 그 뒤에 다시 만들 것(이번 회차에 한 번 그 실수로 결과가 전부 어긋나 재실행했다).

---

## 6차 후속 조치 (2026-09-07 저녁) — 결함 10건 · 개선안 4건 처리

사용자 결정: **#28 = 다안(현행 유지 + 문서화)**, **#29 = 가+다 조합**.
전부 실 데이터(2026-01-01~08-31, 441건)와 fixtures 로 실측 검증했다.
`tests/test_edge_cases.py` 25건 전부 통과. state 는 작업 전 백업하고 원복했다.

### 결함

| # | 조치 | 실측 근거 |
|---|---|---|
| #5 | `validate.check_grace` 를 `month_range` 기준으로 바꾸고, **매트릭스 유예 색 칸 수**를 교차 신호로 추가 | 단순히 `month_range` 로만 바꾸니 1월에 오탐 FAIL 발생(1월은 '기한 전' 0 이 정상). 색 칸으로 바꾼 뒤 1월 PASS(29칸) / 색 55칸 제거 시 FAIL |
| #20 | A1 제목이 `months[0]` 을 쓰도록 | 1월 산출물 제목 `2025-12-01 ~ 2026-01-05` 확인 |
| #28 | **다안.** SKILL.md 에 "`비정기` 라벨의 범위" 절, judgment-rules.md 에 "cycle 라벨은 A 경로를 면제하지 않는다" 절 신설. A/C 경로 표로 명시 | 코드 변경 없음 |
| #29 | **가+다.** A 루프 맨 앞에서 `ended` 를 걸러 C 로 넘기고, C 의 `ended` 검사를 경과일 가드보다 앞으로. config 에 `ignore_suppliers` 신설. 실제 참조는 `build_report.py` 두 곳 — 대상외 시트의 '추가 권장' 칸과 `_print_reco` 의 콘솔 재권유다. **등급 판정 루프는 이 키를 읽지 않는다** (vendors.json 에 없는 곳은 애초에 판정 대상이 아니라 결과는 같다) | 유성빌딩(212-04-59010)에 `until: 2026-08` → `A. 발행 후 전액취소 · 확인 필요` 에서 **`C. 거래 종료`** 로 변경. `ignore_suppliers` 에 넣으면 추가 권장 사라지고 비우면 재등장 (대조 확인) |
| #30 | `apply_state(..., listed_ids=)` 로 미등록 공급자를 `해결` 행으로 만들지 않음. `check_grades` 는 `해결` 등급에 한해 미등록 허용 | 직전 state 에 유성빌딩을 심고 실행 → 미수취목록에 행 없음, validate FAIL 0 |
| N4 | judgment-rules.md 46행 `10/10` → `익월의 grace.deadline_day` | 단일 출처 검사 (b-7) 이 잡던 것이 PASS 로 |
| N6 | `check_sheets` 가 성공 여부를 반환하고, 실패 시 시트 의존 검사 12건을 건너뛰고 요약을 출력 | 이전에는 `KeyError` 로 죽어 요약이 한 줄도 안 나왔다 |
| #14 | excel-format.md 시트 표를 `sheets.*` 키 참조로 교체 | (b-5) 확대 시 4건 FAIL → 수정 후 PASS |
| #16 | `validate` 의 `order` 사본 제거, `from build_report import GRADE_ORDER` | |
| #19 | "구 번호를 지우고 교체" → "구 번호에 until, 신 번호에 since 로 둘 다 남긴다". 이미 짝지어진 쌍은 WARN 에서 빼고 `OK` 로 | 제이푸드가 `사업자번호 변경 처리 완료 1건` 으로 내려감 |
| #21 | A2 안내문의 색 이름(`노랑`·`연파랑`) 제거, config 참조로 | |
| #27 | SKILL.md 에 "가드가 걸렸을 때 밟는 3단계" 신설. `push.py` 가드 메시지에도 한 줄 | "줄어든 항목 전부를 이름으로 설명할 수 있을 때만 `--force` 가 정당하다" |
| #15 | column-mapping.md 는 이번에 손대지 않음 — 5행 선언과 컬럼명 표의 모순은 **남아 있다.** 컬럼명은 config `input` 이 아니라 홈택스가 정하는 값이라, 단일 출처로 옮길 대상인지부터 결정이 필요하다 | **이월** |
| #18 | 사용자 결정 필요 항목이라 이번에 손대지 않음 | **이월** |

### 개선안

| # | 조치 |
|---|---|
| 1 | 단일 출처 검사에 **(b-5) 시트명 · (b-6) thresholds 숫자 · (b-7) `N/DD` 날짜 표기** 추가. 처음엔 코드의 검사 라벨까지 잡아 오탐 11건이 났고, 실제 시트 조회(`wb["..."]`·`create_sheet(...)`)와 문서 표만 잡도록 좁혔다 |
| 2 | `check_paths` 에 `audit/last-audit.md` · `audit/checklist.md` · `install/SKILL.md` 추가. 테스트 `sandbox` 도 `audit/` 를 복사하도록 수정 |
| 3 | **자료 0건이면 `[중단]`.** 점검대상 0곳은 중단이 아니라 경고로 낮췄다 — 빈 vendors.json 으로 대상외 목록만 보는 정당한 사용을 막고 기존 테스트와 충돌했기 때문이다. "자료 없음 = 해결" 문제는 #30 의 `listed_ids` 가드가 이미 막는다 |
| 5 | `t_no_upload_files` · `t_zero_rows_not_resolved` 추가 (테스트 23 → 25건) |
| 4 | `push.py --add-vendor` 는 **미구현 이월.** `ignore_suppliers` 로 재권유 문제는 먼저 해소됐다 |

### 테스트 기대값 변경 1건

`t_resolved_status` 의 기대값을 **`by_status == 2` · `by_grade == 0`** 로 바꿨다.
#29 수정으로 `until` 등록 거래처가 `거래 종료` 행을 먼저 갖게 되어, 해결 표기가
새 행(등급 열)이 아니라 **상태 열**로 간다. 그래서 상태 열이 2, 등급 열이 0 이다.
합계는 2로 동일하며 이중계상은 없다.
(2026-09-07 정정: 이 항목을 처음에 "상태열만 0 → 총 2건" 이라고 거꾸로 적었다.
실제 코드가 단언하는 방향은 위와 같다. 합계 2 는 그때도 지금도 맞다.)

---

## 6차 후속 2차 (2026-09-07 심야) — 이월 3건 종결

앞선 후속 조치에서 "사용자 결정 필요"로 남겼던 3건을 실물 근거를 확인한 뒤 처리했다.
`tests/test_edge_cases.py` 25건 통과, 전체 흐름 재실행 FAIL 0.

| # | 조치 | 판단 근거 |
|---|---|---|
| #15 | `references/column-mapping.md` 머리말을 현실화. "여기에 다시 적지 않는다" → "코드가 읽는 값의 출처는 config `input` 하나이며, 이 문서는 어떤 컬럼을 왜 쓰는지 설명하므로 이름이 나온다". 컬럼 대응 표는 유지하되 `required_columns` 를 가리키는 한 줄을 붙였다 | 컬럼명은 이미 config `input.required_columns` 에 7개 다 있다(이전 판단은 틀렸다). 다만 표를 없애면 `발급일자` 대신 `작성일자` 를 쓰는 이유 같은 설명이 사라지고, `발급일자`·`전송일자` 는 config 에 없어 참조 자체가 불가능하다. 값의 정의가 아니라 이유를 적는 문서로 선언을 맞췄다 |
| #18 | `check_cycle` 의 `if v.get("until"): continue` → `if _until_passed(v.get("until"), as_of): continue`. 헬퍼 `_until_passed` 신설(형식이 깨지면 False) | **실측**: 코원에너지서비스의 `until` 을 `2026-04` → `2026-12`(미래), cycle 을 `비정기` 로 바꾸니 이전에는 조용히 넘어가던 것이 `[WARN] cycle 이 실제 패턴과 어긋나 보이는 거래처 1곳` 으로 잡혔다. 과거 `until` 은 종전과 동일하게 건너뛴다(회귀 확인) |
| 개선안 4 | `push.py --add-vendor` · `--ignore-vendor` · `--cycle` 신설. 목록을 고친 뒤 해당 묶음을 자동으로 push 대상에 넣는다 | 대상외 '추가 권장' 목록의 번호를 그대로 붙이면 된다. 하이픈 유무 무관, 10자리 아니면 건너뜀, 중복이면 건너뜀, 둘 다 지정하면 중단. `--dry-run` 으로 파일 변경만 확인 가능 — 전부 실측 |

`--add-vendor` 는 `name` 을 비워 둔다. 리포트를 다시 만들면 자료에서 채워지며,
고정 표기가 필요하면 vendors.json 에서 직접 적는다. SKILL.md 배포 절차에
사용법과 "의도적으로 뺀 거래처는 `--ignore-vendor` 를 쓴다"는 안내를 넣었다.

**이로써 6차 결함·개선안은 전부 종결됐다.** 남은 미해결 항목 없음.

---

## 6차 후속 3차 (2026-09-07) — 재검증에서 나온 기록·문구 4건 정정

앞선 두 절의 조치를 실물에서 다시 검증했다. **기재된 실측 근거는 숫자까지 전부
재현됐고 재현 실패 항목은 0건이다** (1월 유예 29칸 / 색 55칸 제거 시 FAIL /
유성빌딩 A→C / state 심기 후 미수취목록 행 0 / 코원 WARN 1곳 / 테스트 25건 통과 /
validate 18개 검사 전부 파괴 시 FAIL). 다만 동작이 아니라 **기록과 문구**가
어긋난 곳 4건이 나와 이번에 고쳤다.

| # | 무엇이 어긋났나 | 조치 | 실측 |
|---|---|---|---|
| A | `push.py` 의 `--dry-run` 이 **로컬 파일을 실제로 썼다.** 옵션 이름과 동작이 어긋나 미리보기로 알고 돌리면 이미 바뀐 파일을 갖게 된다 | `edit_vendor_lists` 가 `a.dry_run` 이면 `json.dump` 를 건너뛰고 `추가 예정` / `제외 예정` 만 찍는다. `_DRY_NOTE` 로 "쓰지 않았습니다" 를 명시. 이때 0 을 돌려주되 `main` 이 dry-run 은 **실패가 아니므로 exit 0** 으로 끝낸다 | `--add-vendor` · `--ignore-vendor` 를 `--dry-run` 으로 실행 후 `md5sum -c` → `vendors.json` · `check-config.json` 둘 다 OK(불변). `--dry-run` 없이 실행하면 종전대로 기록됨(회귀 확인). 10자리 아님 · 중복 · 둘 다 지정 가드도 dry-run 에서 그대로 동작 |
| B | SKILL.md "고친 파일이 바로 올라간다(`--dry-run` 으로 확인 가능)" 가 A 의 낡은 동작을 설명하고 있었다 | 줄을 나눠 "`--dry-run` 을 같이 쓰면 화면에만 찍고 파일은 안 고친다" 로 교체 | |
| C | "6차 후속 2차" 의 `t_resolved_status` 기대값 기록이 **방향이 반대**였다("상태열만 0 → 총 2건") | `by_status == 2` · `by_grade == 0` 으로 정정. 합계 2 는 그때도 맞았다 | 코드 261행이 단언하는 값과 대조 |
| D | "6차 후속 조치" 의 #29 기록 "판정·`_print_reco`·대상외 시트가 존중" 이 근거보다 넓었다. 등급 판정 루프는 `ignore_suppliers` 를 읽지 않는다 | 실제 참조 두 곳(`build_report.py` 대상외 시트 · `_print_reco`)만 남기고, 미등록 공급자는 애초에 판정 대상이 아니라 결과가 같다는 단서를 붙였다 | `grep ignore_suppliers` 결과 `build_report.py` 487 · 645 두 곳뿐 |

`validate.py` 의 `check_grace` 주석이 거의 같은 블록으로 두 번 들어가 있던 것도
하나로 합쳤다(동작 무변경, #5 수정 때 붙은 잔존물).

정정 후 `tests/test_edge_cases.py` 25건 전부 통과(개별 체크 106건, exit 0),
9/7 기본 `validate` FAIL 0 · SKIP 1 · PASS 17, 1월 산출물 유예 검사 29칸 PASS 로
회귀 없음. state 는 작업 전 백업하고 원복해 원본과 바이트 동일함을 확인했다.

### 다음 회차에 볼 것

- `--dry-run` 이 **읽기 전용이라는 성질을 테스트가 지키고 있지 않다.** 이번엔 손으로
  md5 대조했다. `t_dry_run_readonly` 같은 테스트를 넣으면 회귀를 자동으로 잡는다.
- 기록 문구의 방향·범위 오류(C·D)는 코드를 아무리 봐도 안 잡힌다. 점검표에
  "조치 표의 문장을 코드와 한 번씩 대조" 를 넣을지 결정할 것.

---

## 6차 후속 4차 (2026-09-07) — 검증 세션 지적 6건 수정

별도 세션의 재검증(6차 후속 1~3차를 코드와 대조)에서 나온 지적 6건을 사용자가
채택해 고쳤다. 사용자가 받아들인 지적 2건은 **1)** 과 **2)** 다. 코드·설정 수정
후 `tests/test_edge_cases.py` 25건 전부 통과, 전체 흐름 재실행 FAIL 0.
state·config 는 작업 전 백업하고 끝에 md5 대조(state·vendors 는 원본과 바이트 동일,
check-config 만 3) 의 의도된 변경).

| # | 무엇 | 조치 | 실측 |
|---|---|---|---|
| 1 | **until 판정 기준 불일치** — "6차 후속 2차"의 #18 수정은 `check_input` 에 `_until_passed`(until < 실행월일 때만 종료)를 넣었고, "6차 후속 조치"의 #29 수정은 `build_report` 의 A·C 루프에 `if f["ended"]`(until 값이 있으면 날짜 무관 종료)를 넣었다. 같은 회차에 반대 기준이 들어가 1월 실행(`--as-of 2026-01-05`)에서 until 4~7월(제이푸드·디패스·팩프렌즈·코원)이 `C. 거래 종료 · 점검 대상 아님` 4행으로 나왔고, `t_resolved_status` 의 기대값을 그 증상("총 2건")에 맞춰 바꾼 상태였다 | `common.until_passed(until, as_of)` 신설(단일 기준, 독스트링에 경위). `check_input.check_cycle` 과 `build_report._one` 이 같은 함수를 쓴다. `f["ended"]` 는 이제 **bool**(지났는가), raw 문자열은 `f["until"]` 로 분리(C 행 메모가 이걸 쓴다). 테스트 기대값을 `"상태열만 0"` 으로 되돌리고 주석에 경위 기록 | 1월: 미수취목록 데이터 행 **0** (거래 종료 4행 사라짐) · 9월 비앤지 `until: 2026-12`(미래) → `A. 정기 거래처 결번 · 확인 필요 · 2월` **다시 잡힘**(수정 전엔 거래 종료로 사라졌음) · 9월 유성빌딩 `until: 2026-08`(과거) → `C. 거래 종료` 유지(회귀 없음) · `t_resolved_status` 1월 경로 `총 2건 (등급열 2 · 상태열만 0)` 통과 · vendors.json 원복 |
| 2 | **#5 유예 검사 FAIL 조건 완화** — `if expect and n == 0 and grace_cells == 0` 이 전 월에서 등급열 훼손을 못 봤다 | 신호를 월에 따라 하나만 쓴다: 직전 달이 전년 12월(1월 실행)이면 매트릭스 유예 색 칸, 그 밖의 달은 '기한 전' 건수. **선택 이유: `or` 로 두면 1월에 '기한 전' 0 이 정상 구조라 늘 FAIL 이 난다** — 색 칸 대체는 1월에만 필요한 것이었다 | 9월 산출물 '기한 전' 6→정상 전부: **FAIL** (`'기한 전' 판정이 0건이다(매트릭스 유예 색 22칸)`) · 1월 산출물 무변경: **PASS** (`색 29칸`) · 1월 유예 색 55칸 제거: **FAIL** (`전년 12월 열에 유예 색 칸이 0칸`) |
| 3 | `ignore_suppliers` 가 `[]` 라 유성빌딩이 매 실행 '추가 권장' 으로 떴다 | `config/check-config.json` `ignore_suppliers: ["2120459010"]` (10자리, `--ignore-vendor` 와 같은 형식) | 콘솔에 `vendors.json 추가 권장` 줄 **없음** · 대상외공급자 시트 유성빌딩 행 '추가 권장' 칸 **None** |
| 4 | vendors.json `ignore` 필드가 문서 없이 존재(`build_report.py` 105 · 122 · 152 · 569) | **(b) 제거.** 이유: 판정에서 빼는 수단은 이미 "vendors.json 에서 지운다" 하나가 있고(미등록 = 판정 대상 아님), 재권유 억제는 `ignore_suppliers` 가 맡는다. `ignore: true` 는 "지우되 기록은 남긴다" 만 더해주는데, 그 기록은 `_comment` 나 git 이력이 대신할 수 있고 제외 장치가 둘이면 어느 쪽을 써야 하는지 매번 헷갈린다. 사용 중인 항목도 없었다(vendors.json 에 `ignore` 키 0건) | `grep ignore scripts/` → `ignore_suppliers` 관련만 남음. 테스트 25건 통과 |
| 5a | `check_sheets` FAIL 시 건너뛴 검사가 "시트 의존 검사 12건" 한 줄이라 요약이 18개가 안 됐다(실제 건너뛰는 검사는 **14개**였다 — 기록의 12 도 틀림) | `SHEET_CHECKS` 목록(14개, main 호출 순서)을 두고 하나씩 SKIP 기록 | 시트명 변경 사본: `FAIL 1 · SKIP 14 · PASS 3` = 18 |
| 5b | 매트릭스 칸에 `' '` 가 있으면 `check_totals` 에서 `TypeError` 크래시, 요약 미출력 | `_is_num()` 헬퍼. `check_totals`·`check_monthly_totals` 가 숫자 아닌 칸을 더하지 않고 **FAIL 로 보고** | 월 칸 `' '`: `[FAIL] 월별 합 대사 — 월 칸에 숫자가 아닌 값 1개: 1월: ' '` 크래시 없음 · 순공급가액 칸 `' '`: `[FAIL] 합계 대사 — 숫자가 아닌 칸 1개` |
| 6 | `build_report.py` 565-567 주석이 "점검 대상 0곳이면 만들지 않는다"(옛 설계) | 실제 동작(자료 0건만 중단, 0곳은 경고)과 경고인 이유(listed_ids 가드 · 대상외 전용 사용 정당)로 교체 | 주석만 |

손대지 않은 것: `check_grades` 의 `g != "해결"` 허용(죽은 분기·방어용, 사용자 동의). 그 밖의 파일 무변경.

### 이번 회차 파괴 실험 (validate 18개 검사)

기준: fixtures 9/7 산출물(`FAIL 0 · SKIP 1 · PASS 17`) 과 `--as-of 2026-01-05` 산출물(state 포함).
위 표의 2)·5) 결과에 더해:

| 검사 · 파괴 방법 | 결과 |
|---|---|
| 매트릭스 월 컬럼: 9월→9 월 | [FAIL] 매트릭스 월 컬럼 |
| 미수취=공란: 공란에 취소색 | [FAIL] 미수취=공란 검사 |
| 전액취소=0+노랑: 노랑 제거 | [FAIL] 전액취소=0+노랑 검사 |
| 점검 대상 누락: 점검대상 1행 삭제 | [FAIL] 점검 대상 누락 검사 |
| 합계 대사: 순공급가액 +1 | [FAIL] 합계 대사 |
| 월별 합 대사: 1월↔5월 교환 | [FAIL] 월별 합 대사 불일치 2개월 |
| 원본 행수: 마지막 행 삭제 | [FAIL] 원본 행수 |
| 승인번호 중복: 1건 복제 | [FAIL] 승인번호 중복 1건 |
| 상계 매칭: 취소분 표시 제거 | [FAIL] 상계 매칭 |
| 대상외공급자: 번호를 vendors 것으로 | [FAIL] 대상외공급자 시트 |
| 등급 분류: 미정의 등급값 | [FAIL] 등급 분류 이상 1건 |
| 등급 분류: 결번월을 값 있는 1월로 | [FAIL] 등급 분류 이상 1건 |
| 실행 이력 비교: state flagged 3→1 | [FAIL] 실행 이력 비교 |
| 해결 집계: 해결 행 상태 비움 (1월+state) | [FAIL] 해결 집계 |
| 경로 존재: README 임시 제거 | [FAIL] 경로 존재 확인 |
| config 죽은 키 | [FAIL] config 죽은 키 1개 |
| 단일 출처: README 10일 | [FAIL] 단일 출처 위반 1곳 |
| 단일 출처: 시트명 리터럴 (b-5) | [PASS] 임계값·색상 단일 출처 |
| 단일 출처: thresholds 리터럴 (b-6) | [FAIL] 단일 출처 위반 1곳 |
| 단일 출처: N/DD 표기 (b-7) | [FAIL] 단일 출처 위반 1곳 |

> **다음 회차 메모: (b-5) 시트명 검사가 `ws.title = "매트릭스"` 형태를 못 본다.**
> `build_report.py` 351행 `ws.title = cfg["sheets"]["matrix"]` 를 리터럴로 바꿔도 PASS.
> 6차 후속 조치가 오탐 11건을 줄이며 `wb["…"]`·`create_sheet(…)` 로 좁힌 결과다.
> 이번 지시 범위 밖이라 고치지 않았다. `ws.title\s*=\s*["']…["']` 패턴 추가로 잡힌다.

### 이번 회차의 숫자 변화

| | 이전 | 지금 |
|---|---|---|
| 9/7 기본 | 확인 필요 3 · 기한 전 6 · 단발 1 · 정상 3 · 해결 0 · validate FAIL 0 · SKIP 1 · PASS 17 | **동일** (콘솔 '추가 권장' 줄만 사라짐) |
| 1월 `--no-state` | 미수취목록 4행(거래 종료) · SKIP 2 | 미수취목록 **0행** · **SKIP 5** (등급 분류·실행 이력·해결 집계·전액취소·상계 — 행이 없어 SKIP, 정상) |
| `t_resolved_status` 1월 경로 | `총 2건 (등급열 0 · 상태열만 2)` | `총 2건 (등급열 2 · 상태열만 0)` — 5차 원래 동작으로 복귀 |

### 다음 회차에 볼 것 (이 절에서 새로 생긴 것)

- `until_passed` 가 단일 기준이 됐는지: `grep -n "until" scripts/*.py` 에 날짜 비교가 `common.py` 한 곳뿐이어야 한다.
- `f["ended"]` 가 bool 로 바뀌었다. 문자열로 쓰던 곳이 남았는지(이번엔 C 행 메모 1곳을 `f["until"]` 로 바꿈).
- (b-5) `ws.title =` 패턴 미검출 — 위 메모.
- `check_grace` 의 1월 판정은 "직전 달이 전년 12월" 로 잡는다(`py != as_of.year`). 2월 실행에는 1월이 직전 달이라 등급 건수 신호로 돌아간다 — 2월 회차에 SKIP/FAIL 이 없는지 확인.

---

## 점검표 개정안 (12건 중 5건 반영 · 7건 대기)

**2·9·10·11·12번은 2026-09-07 사후에 반영 완료** (checklist.md v6.1):
대상 파일 목록에 checklist.md 추가 · `--as-of` 를 데이터 연도 기준으로 + state 백업·복구 지시 ·
토큰을 첫 응답에서 선요청 · 마무리 순서를 push→재수령확인→보고 로 고정 · 실 데이터 판정 기준.
**1·3~8번은 여전히 사용자 채택 대기 중이다.**

1. **F 항목 `--as-of 2027-01-05` 지시가 fixtures 와 맞지 않는다.** fixtures 는 2026년 자료라 2027-01-05 는 `check_input FAIL 점검 기간 작성분이 한 건도 없음` 이고 1월 경로가 아니라 '자료 없음 경로'가 된다. 5차도 `2026-01-05` 로 돌렸다. `--as-of <fixtures 연도>-01-05 (현재 2026-01-05)` 로 고칠 것. 실 데이터가 있으면 그 연도의 1월.
2. **"대상 파일 전체" 목록에 `audit/checklist.md` 추가.** 이번 회차부터 저장소에 있다. (이번 저장본에는 넣지 않았다 — 채택 전이므로.)
3. **B 항목에 단일 출처 검사의 '범위 밖'도 적을 것**: 시트명·thresholds 는 현재 검사 범위 밖이라 매번 PASS 가 난다. 검사가 죽은 게 아니라 안 보는 것 — 표에 "검사 범위 밖" 판정을 허용해야 개선안과 결함이 섞이지 않는다.
4. **"실 데이터 유무" 판정에 "업로드 == fixtures 인지 md5 대조"를 추가.** 이번처럼 업로드 6개가 fixtures 와 동일하면 '실 데이터 있음' 으로 착각하기 쉽다.
5. **파괴 실험 주의 문구 추가**: `--strict`/`--no-state` 실행은 같은 파일명에 덮어쓴다. 기준 파일은 `--out` 을 따로 두거나 마지막에 만들 것.
6. **매 회차 통과만 나는 항목 — 자동화 한 줄로 대체 제안**: A-옵션 존재 여부, C-체크섬, G-sync codeload, G-GROUPS 커버리지, I-경로 존재, B-config 삭제 시 정지. 5차·6차 연속 통과. `tests/` 에 `t_audit_static()` 하나로 묶으면 점검표에서 뺄 수 있다(테스트 게이트가 대신 본다). 채택하면 개선안 5 와 함께 구현.
7. **"validate 검사 전부 파괴" 지시에 검사 개수를 적지 말고 "현재 `rec(` 호출 기준"으로 둘 것.** 이번 18개. SKIP 으로 끝나는 검사(해결 집계·전액취소·상계)는 1월 산출물이나 별도 조건이 필요하다는 문장 추가.
8. **D 항목 "'미수취=공란' 검사가 None 과 빈 문자열을 구분 못 해 무조건 통과하는지"** — 3회차 연속 '조건 성립 불가(openpyxl 이 '' 를 None 으로 저장)'. 삭제 또는 "문자열 칸이 들어가면 크래시하는지" 로 교체.
9. **`--as-of` 로 과거 시점을 돌릴 때 state 를 백업하라는 문장 추가.** build_report 는 실행마다 `state/last-run.json` 을 덮어쓴다. 점검 회차는 진단만 하므로 끝나고 원본을 복구해야 push 에 state 가 섞이지 않는다(이번 회차는 매 실행 뒤 복구했고 원격과 md5 동일 확인).
10. **다음 회차 4줄 요청에 push 토큰이 빠져 있다.** 점검표는 "같은 push 로 올려라"까지 시키는데 토큰 없이는 마무리 단계가 수행 불가다. 실제로 이번 1차 패스가 그 상태로 끝나 진단 전체가 저장소에 남지 않았다. 4줄 요청에 `push.py 토큰: …` 한 줄을 넣거나, "토큰이 없으면 시작 전에 요청할 것"을 점검표 머리에 명시.
11. **마무리 순서를 뒤집을 것: push → codeload 재수령 확인 → 그 다음에 채팅 보고.** 채팅 보고를 먼저 쓰면 세션이 끊길 때 저장소에 아무것도 남지 않는다(1차 패스 실증). 컨테이너 잔존물은 다음 세션에 있을 수도 없을 수도 있으니 믿지 말 것.

---

## 점검표 갱신 이력 (checklist.md)

- 6차 2026-09-07 — 사용자 제공 점검표 전문을 `audit/checklist.md` 로 저장(첫 이관). 머리말 안내 문단만 "정본" 문구로 교체. 본문 무변경. 위 개정안 11건은 미반영(채택 대기). 같은 날 1차 패스는 push 실패, 2차 패스에서 저장.

12. **[반영 완료] 실 데이터 판정 기준을 md5 → 데이터 최종일로 바꿀 것.** 이번 회차에
    업로드본이 fixtures와 md5 동일하다는 이유로 "실 데이터 아님"으로 판정했으나, fixtures가
    사용자의 실제 다운로드본이라 md5 일치는 당연한 결과였다. 실제로는 실 데이터였고
    최종일이 8/31(7일 전)이라 당월 항목 2건만 [추론] 대상이었다. `checklist.md`
    `[시작 전 확인]` 블록을 최종일 기준 3단계 판정표로 교체하고, [추론]으로 넘길 항목을
    2건으로 좁혔다. fixtures를 함부로 갈아끼우지 말라는 조항(기대값 고정, 별도 회차 처리)도
    함께 넣었다.

---

## 다음 점검에서 대조할 것

0. **업로드본의 데이터 최종일을 먼저 확인할 것.** md5가 fixtures와 같아도 실 데이터다.
   `checklist.md` 새 판정표대로 따르고, md5 일치를 근거로 "실 데이터 아님"이라 쓰지 마라.
1. **점검표 개정안 1~11번 중 사용자가 채택한 것이 `checklist.md` 에 반영되고 버전 줄이 갱신됐는가.** 특히 1번(`--as-of` 연도)은 채택 안 하면 다음 회차도 헛돈다.
2. **#5 #20 은 12월 회차에 1순위.** 2027-01 실행 전에 안 고치면 1월 리포트 A1 이 틀리고 '기한 전' 검사는 죽어 있다. #5 를 고칠 때 "1월엔 기한 전 0 이 정상" 구조를 판정 조건에 반영할 것.
3. **커플링: 개선안 1(검사 확대) ↔ #14 #15 N4.** 확대 코드를 먼저 push 하면 테스트 게이트가 아니라 validate 가 문서 3곳에서 FAIL 을 내며 다음 실사용 실행이 막힌다. 한 커밋에 넣을 것.
4. **커플링: #29 가 안 + 개선안 4(`--add-vendor`/제외 목록).** 유성빌딩 재권유는 제외 목록이 있어야 끝난다. 그때까지 "묻지 말 것" 운영 주의 유지.
5. **미실측 이월**: `check_resolved` 실사용 대조(3회차 연속 해결 0 → SKIP). 실 홈택스 자료에서 `상태열만 N>0` 인 회차가 나오면 콘솔 '해결 N' 과 대조.
6. **#18 #28 방향 결정** — 사용자 대기 4회차째.
7. **이번 회차에 새로 생긴 것**: `audit/checklist.md`. `push.py` 의 `_scan("audit")` 가 이 파일을 자동 포함해 올렸는지 다음 회차 첫 ls 로 확인(이번 push 직후 codeload 재수령으로 1차 확인함). `check_paths` 는 아직 이 파일을 모른다(개선안 2).
8. **1차 패스 잔존물이 컨테이너에 남아 있는지.** `/home/claude/hometax_old_session/`, `/home/claude/audit_new_head.md`, `kill.py` 등. 있으면 지우고 codeload 실물만 쓸 것 — 잔존 사본을 실물로 착각하면 점검표 규칙(설치 경로 사본 무효)과 같은 함정이다.

---

## 이전 기록 (5차 정기점검 + 6차 실사용, 2026-09-06 — 원문 보존)

# 점검 기준선

> **5차 수정 반영 완료 (2026-09-06).** 진단 후 사용자가 두 묶음을 지정해
> 실제로 고치고 `push.py --code` 로 2회 나눠 올렸다. 아래 "이번 회차에 수정한 것"
> 절 참조. **결함 17건 중 8건 해결, 9건 미해결로 이월.**

점검일: 2026-09-06 (5차 — 정기점검)
직전: 2026-09-06 4차 (기준선 항목 27건)

**재확인 결과: 해결됨 13건 / 미해결 14건 / 근거없음 0건 / 신규 3건**
결함 17건 / 개선안 5건 / 인용불가로 제외 0건

> **미해결 14건은 드리프트가 아니라 미착수다.** 설치본 SKILL.md 와 저장소
> `install/SKILL.md` 를 md5·diff 로 대조한 결과 개행 1자 외 차이가 없었다.
> 2·3차가 도입한 "설치본 = 얇은 부트스트랩" 구조가 실제로 작동했다.
> 미해결 항목은 전부 저장소 실물에 그대로 남아 있다 — 2차는 "재확인+문서보완만",
> 4차는 "코드 수정 없음"으로 끝냈기 때문이다.

## 이번 회차 실측 조건

`codeload` tarball 로 `LeeKwanBeom/hometax-invoice-check@main` 실물 수령.
`tests/fixtures/` 6개로 4회 실행: 기본 / `--as-of 2026-01-05` / 같은 날짜 `--no-state` /
`--strict`. 산출물 xlsx 를 openpyxl 로 직접 열어 확인. `push.run_tests()` 는
`common.py` 를 일부러 깨뜨려 차단되는지 실측.

| | 실측값 |
|---|---|
| 9/6 기본 | 확인 필요 4 · 기한 전 6 · 단발 1 · 정상 3 · 거래 종료 4 · 해결 0 |
| 총 건수 | 441건 · 매출분 제외 0 · 기간 밖 제외 0 · 상계 6쌍 |
| 9/6 validate | FAIL 0 · SKIP 0 · PASS 17 |
| 1월 실행(state 포함) | FAIL 0 · **SKIP 2** · PASS 15 |
| 1월 실행(`--no-state`) | FAIL 0 · **SKIP 4** · PASS 13 |
| `--strict` | 확인 필요 10 · **기한 전 0** |
| `test_edge_cases.py` | 실패 0 (t_ 함수 22개) · exit 0 |
| 테스트 게이트 | `range(1, 10)` 주입 시 실패 10건 → `run_tests() = False` **차단됨** |
| state 역행 가드 | 과거날짜·같은날 감소·원격깨짐 3케이스 모두 차단 메시지 반환 |
| push `GROUPS` 커버리지 | 저장소 실제 파일과 **완전 일치**(누락 0 · 유령 0) |

> **4차 미결 "1월 실행 SKIP 4 vs 2" 해소.** `--no-state` 를 붙이면 `실행 이력 비교`
> 와 `등급 분류` 가 추가로 SKIP 되어 4건, 안 붙이면 2건이다. 1차는 `--no-state`
> 로 돌렸던 것이다. 두 숫자 모두 정상.

> **4차 미결 "1월 전년 12월 자료 없으면 FAIL(의도된 동작)" 실측 완료.**
> `check_input.py --as-of 2026-01-05` → `[FAIL] 전년 12월 데이터가 통째로 없음`.
> SKILL.md 83-85행과 코드가 같은 말을 한다. 정상 동작.

---

---

## 이번 회차에 수정한 것 (push 2회)

### 1묶음 — `#26` + 개선안 #2
커밋: `fix #26: '해결' 집계가 상태 열 표기를 빠뜨리던 문제 + validate 해결 집계 대사 검사 추가`
파일 4개: `scripts/common.py`(+17/−0) · `scripts/build_report.py`(+5/−2) ·
`scripts/validate.py`(+55/−2) · `tests/test_edge_cases.py`(+50/−1)

| 무엇 | 어디 |
|---|---|
| `is_resolved(grade, status)` 신설 — 세는 규칙을 한 곳에만 둔다 | `common.py` 147 |
| 콘솔 집계가 등급+상태를 함께 셈 | `build_report.py` 568-571 |
| `check_state` 가 상태 열의 '해결' 도 인식 | `validate.py` 422 |
| `check_resolved()` 신설 — 등급열/상태열만 을 나눠 보고 | `validate.py` 435 |
| `t_resolved_status()` 회귀 테스트 신설 | `tests/` |

**실측**: 재현 조건(직전 이력에 코원에너지·서바이빙) 재실행 →
콘솔 `해결 0` → **`해결 2`**, validate `해결 0곳` → **`해결 2곳`**,
새 검사 `총 2건 (등급열 0 · 상태열만 2)`.

### 2묶음 — `#13` `N1` `N2` `N3` + `deadline_day` 사본 3건
커밋: `fix #13 N1 N2 N3 + deadline_day 사본 3건: 단일 출처 검사 범위를 SKILL.md/README/install 로 확대하고 문서 모순·사본 제거`
파일 4개: `SKILL.md`(+5/−4) · `README.md`(+7/−3) ·
`scripts/validate.py`(+29/−18) · `tests/test_edge_cases.py`(+39/−2)

| # | 지금 원문 | 위치 |
|---|---|---|
| 13 | `for rel in ["references", "install", ""]:` — `audit/` 는 인용문 오탐 때문에 **일부러 제외** | `validate.py` 502 |
| 11 | `세금계산서 발급기한은 작성월 다음 달의 정해진 날짜다(`config` 의 `grace.deadline_day`).` | `SKILL.md` 31 |
| 25 | `\| `기한 전` \| 발급기한이 아직 남음 \| 기다린다 \|` | `SKILL.md` 166 |
| 12 | `→ 발급기한 전이라 정상이다. 등급이 `기한 전`이면 기다리면 된다.` | `SKILL.md` 287 |
| N1 | `SKILL.md                   이 파일. **정본 설명서.** 설치 경로에 넣는 건 install/SKILL.md 다` | `SKILL.md` 343 |
| N2 | `2. Claude 스킬 폴더에 **`install/SKILL.md`** 만 넣는다.` + 보존 안 됨 인용 블록 | `README.md` 12-17 |
| N3 | `python3 -c "import xlrd" 2>/dev/null \|\| pip install xlrd --break-system-packages -q` | `README.md` 28 |

**실측**: 문서 스캔 3개 → **6개**. 고친 사본을 일부러 되살리자
`[FAIL] 단일 출처 위반 1곳 / SKILL.md: '10일' — grace.deadline_day 를 문서에 다시 적음`
→ 검사가 죽어 있지 않음을 확인. 되돌리자 PASS 복귀.
회귀 테스트 `SKILL.md·README.md 의 deadline_day 사본을 잡음` 2건 추가.

### 이번 회차에 새로 만들었다가 같은 회차에 고친 것

개선안 #2 의 첫 구현이 `total != by_grade + by_status` 를 무결성 조건으로 썼다.
**전제가 틀렸다** — `apply_state` 의 새 행 경로는 등급과 상태에 '해결' 을
**함께** 붙인다. 1월 실행에서
`[FAIL] 등급 4 + 상태 4 = 8 인데 실제 해결 행은 4건` 오탐이 났다.
조건을 "등급이 '해결' 인데 상태가 빈 행" 으로 바꾸고, 테스트에
새 행 경로(`--as-of 2026-01-05`) 하위검사 2건을 추가했다.
**1묶음 테스트 게이트는 이걸 못 잡았다** — 상태만 경로 하나만 밟았기 때문이다.

### 수정 후 최종 실측

| | 결과 |
|---|---|
| 9/6 기본 | 확인 필요 4 · 기한 전 6 · 단발 1 · 정상 3 · 해결 0 · **FAIL 0 · SKIP 1 · PASS 17** |
| 1월 실행 | 해결 4 · **FAIL 0 · SKIP 2 · PASS 16** · `총 4건 (등급열 4 · 상태열만 0)` |
| `--strict` | 확인 필요 10 · 기한 전 0 |
| `test_edge_cases.py` | 실패 0 · exit 0 (t_ 함수 **23개**) |
| 저장소 대조 | push 후 codeload 재다운로드 → `audit/` 외 차이 없음 |

> 9/6 기본의 SKIP 1 은 신설된 `해결 집계` 다(이번 이력과 결과가 같아 해결 0건).
> 4차까지의 `SKIP 0` 과 다른 이유는 검사가 하나 늘어서다.

---

## 결함 (17건 — 8건 해결 / 9건 이월)

| # | 심각도 | 파일 | 줄 | 문제 원문(그대로) | 왜 틀렸는지 | 수정 방향 | 작업경로 |
|---|---|---|---|---|---|---|---|
| 26 | **높음** | `scripts/build_report.py` / `scripts/validate.py` | 568 / 420-421 | `n = {g: sum(1 for r in rows if r["grade"] == g) for g in list(GRADE_ORDER) + ["해결"]}` / `elif g == "해결": resolved.add(sid)` | `해결` 을 **등급 열**로만 센다. 실제 해결 건은 `상태` 열에 적힌다(build_report 272행). **이번 회차에 재현함**: 직전 이력에 코원에너지서비스·서바이빙에프앤비를 넣고 돌리니 시트에는 `상태=해결` 2행인데 콘솔은 `해결 0`, validate 는 `해결 0곳` PASS | 두 곳 모두 `등급=="해결" or 상태=="해결"` 로 센다 + validate 에 대사 검사 추가 | `push.py --code` |
| 5 | **높음** | `scripts/validate.py` | 446-447 | `prev = as_of.month - 1` / `expect = prev >= 1 and is_in_grace(as_of.year, prev, as_of, cfg)` | 1월 실행이면 `prev=0` → `expect=False` → **무조건 PASS**. 남아 있는 유일한 0건 매칭 PASS. 실측: 1월 실행에서 `'기한 전' 0건 (전월 유예 구간: False)` PASS | `prev` 를 `month_range(as_of)[-2]` 로 잡아 1월엔 전년 12월을 보게 한다 | `push.py --code` |
| 13 | **높음** | `scripts/validate.py` | 498, 503 | `for fn in os.listdir(os.path.join(SKILL_DIR, "scripts")):` / `ref = os.path.join(SKILL_DIR, "references")` | 단일 출처 검사가 `scripts/` 와 `references/` 만 훑는다. **SKILL.md·README.md·install/SKILL.md 는 영영 안 본다.** 그래서 사본이 3곳까지 늘어나도 FAIL 0 이 나온다 — 아래 결함 8·9·10의 직접 원인 | 스캔 대상에 저장소 루트 `*.md` 와 `install/*.md` 추가 | `push.py --code` |
| N1 | **높음** | `SKILL.md` | 342 | `SKILL.md                   이 파일. 저장소 사본이며, 설치 경로에도 함께 반영한다` | 같은 파일 197행 `**설치 경로에 직접 쓰지 않는다.**` 와 **정면 모순**. 3차 #22 정정으로 폐기된 지침이 '저장소 구성' 절에만 남았다. 이 줄만 읽으면 1·2차에서 두 번 반복한 헛수정을 다시 한다 | `이 파일. 정본 설명서. 설치본은 install/SKILL.md 다` 로 교체 | `push.py --code` |
| N2 | **높음** | `README.md` | 12-13 | `2. Claude 스킬 폴더에 `SKILL.md` 만 넣는다. 저장소에도 같은 파일의 사본이 있어 / 버전이 남는다. 고칠 때는 **저장소와 설치 경로 두 곳 다** 반영해야 한다.` | N1 과 같은 모순이고 더 나쁘다. **재설치할 때 읽는 문서**라서, 여기 적힌 대로 하면 359행짜리 정본을 설치 경로에 넣게 되고 다음 세션에 통째로 원복된다 | `install/SKILL.md` 를 넣는다 + `설치 경로는 세션 간 보존되지 않는다` 로 교체 | `push.py --code` |
| 20 | 중간 | `scripts/build_report.py` | 334 | `ws["A1"] = f"공급자 × 월 매입 발급 매트릭스 ({as_of.year}-01-01 ~ {as_of})"` | 시작일을 `당해 1/1` 로 박아뒀는데 1월 실행에는 전년 12월이 들어간다. **실측**: `--as-of 2026-01-05` 산출물 A1 은 `(2026-01-01 ~ 2026-01-05)` 인데 헤더는 `전년 12월 / 1월` 2열이다. 1월마다 반드시 틀린다 | `months[0]` 을 `month_label` 로 찍어 실제 범위를 쓴다 | `push.py --code` |
| N3 | 중간 | `README.md` | 24 | `pip install xlrd            # 홈택스 .xls 를 읽는 데 필요` | **실측**: 이 컨테이너에서 그대로 실행하면 `externally-managed-environment` 로 실패하고 `import xlrd` 가 계속 ModuleNotFoundError 다. SKILL.md 48행은 `--break-system-packages` 를 붙인 올바른 형태다 | SKILL.md 48행과 같은 한 줄로 교체 | `push.py --code` |
| 11 | 중간 | `SKILL.md` | 31 | `세금계산서 발급기한은 작성월 다음 달 10일. 9월 초에 돌리면 8월분이 아직` | `grace.deadline_day` 사본 1/3 | `(config 의 grace.deadline_day)` 로 | `push.py --code` |
| 25 | 중간 | `SKILL.md` | 165 | `\| 기한 전 \| 발급기한(익월 10일)이 아직 남음 \| 기다린다 \|` | `grace.deadline_day` 사본 2/3. 2차에 등급표를 만들며 **새로 늘린** 사본 | `발급기한이 아직 남음` 으로 | `push.py --code` |
| 12 | 중간 | `SKILL.md` | 286 | `→ 발급기한(9/10) 전이라 정상이다. 등급이 `기한 전`이면 기다리면 된다.` | `grace.deadline_day` 사본 3/3. 게다가 9월 고정이라 다른 달엔 말이 안 맞는다 | `→ 발급기한 전이라 정상이다` 로 | `push.py --code` |
| 16 | 중간 | `scripts/validate.py` | 349-350 | `order = {"확인 필요": 0, "기한 전": 1, "단발·비정기": 2, "정상": 3, "거래 종료": 4, "해결": 5}` | `build_report.GRADE_ORDER`(29-30행)의 완전한 사본. 등급을 하나 더 넣으면 한쪽만 고쳐 조용히 어긋난다. config 에 `grades` 블록이 없어 단일 출처 검사도 못 잡는다 | `from build_report import GRADE_ORDER` 또는 config 로 승격 | `push.py --code` |
| 14 | 중간 | `references/excel-format.md` | 15-18 | `\| 1 \| 매트릭스 \| 공급자 × 월. 점검대상 먼저, 대상외 나중 \|` (이하 미수취목록·대상외공급자·원본정제데이터) | 11행이 `시트 이름도 config(sheets)에서 읽는다` 고 선언해놓고 바로 아래 표에 4개를 리터럴로 다시 적었다 | 표의 시트 이름 열을 config 키(`sheets.matrix` 등)로 교체 | `push.py --code` |
| 15 | 중간 | `references/column-mapping.md` | 5, 32-37 | `여기에 다시 적지 않는다 — config/check-config.json 의 input 블록이 유일한 출처다.` / `\| 공급자 식별 \| 공급자사업자등록번호 \| …` | 5행 선언과 32-37행 표가 모순. `input.required_columns` 의 컬럼명이 표에 그대로 복사돼 있다 | 컬럼명 열을 config 키 참조로 바꾸거나, 5행 선언을 "컬럼명은 적되 헤더 행 번호는 적지 않는다"로 현실화 | `push.py --code` |
| 27 | 중간 | `SKILL.md` | 226, 230-231 | `\| --force \| 실행 이력이 뒤로 가도 강행. **쓰지 않는다** \|` / `이게 걸리면 --force 로 뚫지 말고 **sync.py 로 최신본을 받은 폴더에서 다시 실행한다.**` | 4차에 실제로 막혔고 안내된 조치(재 sync)로는 빠져나갈 수 없었다. vendors.json 개선으로 `확인 필요` 가 **정당하게** 줄어든 경우가 문서에 없다 | `--force` 금지는 유지하되 예외 3단계(원격 state 대조 → 하락 사유가 `거래 종료`·`단발·비정기` 인지 확인 → 사용자 승인) 명시. push.py 272-276행 가드 메시지에도 한 줄 추가 | `push.py --code` |
| 21 | 중간 | `scripts/build_report.py` | 337 | `f"빈칸=미수취 · 노랑=발행 후 전액취소 · 연파랑=발급기한 전")` | 산출물 A2 안내가 색 이름을 문자열로 박았다. `colors.cancelled` / `grade_grace` 를 바꾸면 안내문만 거짓이 된다 | 색 이름을 빼거나 config 에 라벨을 둔다 | `push.py --code` |
| 18 | 낮음 | `scripts/check_input.py` | 156-157 | `if v.get("until"):` / `    continue` | `until` 이 붙으면 cycle 검사를 통째로 건너뛴다. `until` 을 잘못 넣은 거래처는 주기 이상을 영영 못 잡는다. (154-155행에 의도 주석이 있어 결함/설계 판단이 갈림) | `until` 이 **과거**일 때만 skip 하고, 미래·당월이면 계속 검사 | `push.py --code` |
| 19 | 낮음 | `scripts/check_input.py` | 249 | `"\n변경이라면 vendors.json 에서 구 번호를 지우고 신 번호로 교체할 것.")` | SKILL.md 278행·`judgment-rules.md` 102행은 `구 번호에 until, 신 번호에 since` 라고 한다. 실제 vendors.json 의 제이푸드 2건도 until/since 방식이다. 경고 문구만 반대를 말한다 | 문구를 `구 번호에 until, 신 번호에 since 를 넣을 것` 으로 | `push.py --code` |

### 해결됨 13건 (원문 확인)

| # | 파일 | 줄 | 지금 원문 |
|---|---|---|---|
| 1 | `SKILL.md` | 136 | `**4단계에서 --as-of 나 --strict 를 줬으면 여기에도 똑같이 준다.**` |
| 2 | `SKILL.md` | 83 | `- **1월에 실행할 때만 전년 12월 1일부터 받는다.** 12월분 발급기한이 익년 1월이라` |
| 3 | 설치본 ↔ `install/SKILL.md` | — | `diff` 개행 1자 차이만. md5 `c732414e88931f0ec219b51e292e5d15`(설치) / `6f686b5721644381382be801a939c92d`(저장소). 구조 변경으로 정본은 저장소 `SKILL.md`(359행), 설치본은 부트스트랩(55행) |
| 4 | `scripts/validate.py` | 379, 384 | `if n == 0 and mrow:` / `rec(SKIP, "등급 분류", "미수취목록이 비어 있음 — 이번 회차에 잡힌 거래처가 없다")` |
| 6 | `scripts/build_report.py` | 540 | `split = drop_split_offsets(df)` |
| 7 | `scripts/validate.py` | 273, 288, 298 | `cancel = orig = refund = neg = split = 0` / `split += 1` / `+ (f" · 짝이 기간 밖 {split}건" if split else "")` |
| 8 | `SKILL.md` | 184 | code 묶음 목록에 `install/SKILL.md`·`audit/` 포함. push.py `GROUPS` 와 실측 완전 일치 |
| 9 | `SKILL.md` | 120, 123 | `\| --strict \| 지난 달까지 유예 없이 전부 미수취 판정.` / `--strict 라도 **실행 당월은 유예**다.` |
| 10 | `SKILL.md` | 257 | `{"biz_no": "0000000000", "name": "예시상사", "cycle": "매월",` |
| 17 | `scripts/build_report.py` | 162 | `elif f["cycle"] == "비정기" or f["months_got"] <= cfg["thresholds"]["sporadic_max_months"]:` |
| 22 | `sync.py` | 34-36 | `# 설치 경로에 직접 써도 세션 간 보존되지 않는다(2026-09-06 실측).` |
| 23 | `scripts/push.py` | 182, 187 | `if od and nd and nd == od:` / `if nf < of:` — 3케이스 실측 차단 확인 |
| 24 | `scripts/build_report.py` | 272 | `by_id[bid]["status"] = "해결"` |

### 통과 처리 (인용은 되나 지금 틀리지 않음) — 4건

- `validate.check_state` 401행이 `find_header_row(ws, ["등급"])` 만 요구하고 417행에서 `m["공급자번호"]` 를 쓴다. 산출물은 항상 두 열을 함께 만들므로 발생 조건이 없다
- `check_matrix_blank_and_fill` 109행이 `c.value is None` 만 공란으로 본다. build_report 는 빈 문자열을 쓰지 않는다
- `check_input.py` 132행 `if day > 10` 매직넘버. `deadline_day` 와 무관한 별개 휴리스틱이라 config 사본이 아니다
- `build_report.py` 530행 `pairs = match_offsets(...)` 가 541행에서 재할당된다. 죽은 대입이지만 결과는 옳다

**인용불가로 제외: 0건.**

---

## 개선안 (최대 5)

| # | 내용 | 이유 | 우선순위 |
|---|---|---|---|
| 1 | 단일 출처 검사 스캔 대상에 `SKILL.md` · `README.md` · `install/*.md` 추가 (4차 개선안 #2 승계) | 결함 #13 의 정면 대응. 이게 없으면 `deadline_day` 사본이 계속 늘어난다 — 1차 1곳 → 지금 3곳 | **1** |
| 2 | validate 에 "`상태=해결` 행 수 == 콘솔·집계" 대사 추가 | #26 을 코드만 고치면 다음에 또 조용히 어긋난다. 검증기가 같은 기준으로 세는 한 영영 안 걸린다 | 2 |
| 3 | `push.py --add-vendor` — 대상외 '추가 권장' 을 vendors.json 에 반영 (4차 개선안 #3 승계) | 지금은 매번 손으로 JSON 을 편집한다. `_print_reco()` 가 목록은 이미 만들어준다 | 3 |
| 4 | `check_paths` 에 `audit/last-audit.md` · `install/SKILL.md` 추가 | 기준선 파일이 없으면 1단계가 조용히 그냥 넘어간다. 정본이 저장소로 옮겨진 지금은 존재 확인이 의미가 있다 | 4 |
| 5 | `test_edge_cases.py` 에 '홈택스 파일 0개' 케이스 추가 | J 항목 중 유일하게 테스트가 없다. 코드 동작은 실측 확인함(`[중단] … 홈택스 파일(.xls)이 없습니다`) | 5 |

> **4차 개선안 #1 (`sync.py --install-skill`) 종료.** 설치본을 얇은 부트스트랩으로
> 분리한 3차 조치가 이번에 실증됐다 — 설치본과 저장소 `install/SKILL.md` 가
> 개행 1자 외 동일했다. 손 동기화 절차 자체가 사라졌으므로 폐기한다.
> **4차 개선안 #4(실행 메타 파일)** 도 목록에서 내린다. 필요성이 실측으로
> 확인되지 않았고, 개선안은 5개를 넘기지 않는다.

---

## 이월된 결함 12건 (우선순위 순)

| # | 심각도 | 파일 | 왜 남았나 |
|---|---|---|---|
| 5 | 높음 | `validate.py` 446-447 | 1묶음/2묶음 어디에도 안 넣었다. **남아 있는 유일한 0건 매칭 PASS** — 다음 회차 1순위 |
| 28 | 높음 | `build_report.py` 122 / 162 | **실사용 중 발견(2026-09-06 6차).** `비정기` 라벨이 A 경로에서만 무시된다. 사용자가 코드 수정을 다음 회차로 미룸 — 아래 절 참조 |
| 29 | 높음 | `build_report.py` 73-75 / 84 / 135 / 154 | **실사용 중 발견(2026-09-06 6차).** 전액취소 거래처에 `until` 이 안 듣는다. SKILL.md 의 안내가 작동하지 않는 경로 — 아래 절 참조 |
| 20 | 중간 | `build_report.py` 334 | 1월 실행 A1 제목이 전년 12월 열을 빼고 표기. **1월마다 반드시 틀린다** — 다음 1월 실행 전에 처리 |
| 30 | 중간 | `build_report.py` 265-276 / `validate.py` | **실사용 중 발견(2026-09-06 6차).** 거래처를 목록에서 지우면 `해결` 행이 생기고 validate 가 FAIL. 이력 손질로 우회함 — 아래 절 참조 |
| 16 | 중간 | `validate.py` 349-350 | `GRADE_ORDER` 사본 |
| 14 | 중간 | `references/excel-format.md` 15-18 | 시트명 리터럴 |
| 15 | 중간 | `references/column-mapping.md` 5, 32-37 | 컬럼명 리터럴 |
| 27 | 중간 | `SKILL.md` 226-231 | `--force` 예외 절차 부재 |
| 21 | 중간 | `build_report.py` 337 | 산출물 A2 색 이름 문자열 |
| 18 | 낮음 | `check_input.py` 156-157 | 결함/설계 판단 미결 |
| 19 | 낮음 | `check_input.py` 249 | 사업자 변경 안내가 SKILL.md·judgment-rules 와 반대 |

> **#14 #15 는 2묶음 이후 새 위험이 생겼다.** 단일 출처 검사가 이제 문서를
> 6개 훑는데, `references/` 의 두 위반은 시트명·컬럼명이라 현재 규칙
> (색상 헥스·사업자번호·`N일`)에 안 걸린다. 검사를 그쪽으로 넓히면
> #14 #15 가 즉시 FAIL 로 뜬다 — **검사 확대와 문서 수정을 같은 회차에 해야 한다.**

---

## 실사용 중 발견 — 결함 #28 (2026-09-06, 6차 실행)

정기점검이 아니라 **실제 홈택스 자료로 점검을 돌리던 중** 나왔다.
사용자가 "비앤지부동산중개는 단발성, 다연유통은 가끔"이라고 알려줘
`vendors.json` 의 `cycle` 을 `비정기` 로 바꿨는데, **등급이 하나도 안 바뀌었다.**
둘 다 `확인 필요` 그대로였다.

| | 원문 | 라벨을 |
|---|---|---|
| A 경로 | `monthly = f["cycle"] == "매월" or f["months_got"] >= th["monthly_min_months"]` (`build_report.py` 122) | **무시한다** — 수취 월수가 임계 이상이면 `비정기` 라벨이 덮인다 |
| C 경로 | `elif f["cycle"] == "비정기" or f["months_got"] <= cfg["thresholds"]["sporadic_max_months"]:` (`build_report.py` 162) | **존중한다** |

C 경로에는 163-166행에 "cycle 을 안 보면 `비정기` 라벨이 사실상 아무 일도
안 하게 된다"는 의도 주석까지 달려 있다. **A 경로는 정확히 그 상태다.**
같은 라벨이 판정 경로에 따라 반대로 작동한다.

**실측**: 비앤지(7개월 수취) · 다연유통(6개월 수취) 을 `비정기` 로 바꾼 뒤 재실행 →
`확인 필요 4 · 단발 1` 로 변경 전과 동일. `check_input.py` 는 같은 상황을
`[WARN] cycle 이 실제 패턴과 어긋나 보이는 거래처 2곳` 으로 잡아냈다 —
**입력 검증은 라벨과 데이터의 충돌을 알려주는데, 판정은 라벨을 버린다.**

### 판단이 필요한 지점 (수정 전에 결정할 것)

단순 버그가 아니라 **설계 충돌**이라 고치는 방향이 갈린다.

| 안 | 내용 | 위험 |
|---|---|---|
| 가 | A 경로도 `cycle == "비정기"` 면 정기 판정에서 빼고 C 로 넘긴다 | 라벨을 잘못 붙이면 진짜 미수취를 통째로 놓친다. 지금 `months_got` 임계는 그 오등록에 대한 안전장치다 |
| 나 | 라벨을 우선하되 `check_input` WARN 을 FAIL 로 올려 충돌 시 멈춘다 | 매 실행마다 사용자 확인이 필요해진다 |
| 다 | 현행 유지 + 문서화. `비정기` 는 "C 경로 전용 힌트"이지 정기 판정 면제가 아님을 SKILL.md·judgment-rules 에 명시 | 사용자가 라벨을 고쳐도 등급이 안 바뀌는 혼란이 그대로 남는다 |

이번 회차는 결정하지 않았다. **사용자가 코드 수정을 다음 회차로 미뤘다.**

### 이번 회차의 후속 처리

라벨 변경은 **되돌렸다.** 사용자가 데이터를 다시 보고 두 곳 모두
"꾸준히 거래하는 업체" 로 정정했다. `cycle` 은 `매월` 로 복귀했고
`note` 에 확인 사실만 남겼다. 즉 **#28 은 이번 산출물에 영향을 주지 않았다** —
라벨과 데이터가 다시 일치하기 때문이다. 결함은 그대로 살아 있다.

---

## 실사용 중 발견 — 결함 #29 (2026-09-06, 6차 실행)

**`until` 이 '발행 후 전액취소' 거래처에는 전혀 듣지 않는다.**
SKILL.md 290-292행과 291행 FAQ 는 거래 종료 시 `until` 을 넣으라고 안내하는데,
마지막 몇 달이 전액취소된 거래처에는 그 안내가 작동하지 않는다.

| 원문 | 위치 |
|---|---|
| `out_of_scope = not (lo <= m <= hi)` — **`len(gm) == 0` 인 달에만 적용된다** | `build_report.py` 73-75 |
| `state = "cancelled" if len(lv) == 0 else "ok"` — 행이 있으면 scope 를 안 본다 | `build_report.py` 84 |
| `elif f["cancelled"]:` → `확인 필요` + `a_ids.add()` | `build_report.py` 135-138 |
| `if f["ended"]:` → `거래 종료` — **C 루프에만 있다. A 가 이미 a_ids 에 넣어 도달 불가** | `build_report.py` 154 |

취소분은 행이 존재하므로 `out_of_scope` 분기를 타지 않고 `cancelled` 로 들어간다.
그리고 A 경로가 C 경로보다 먼저 돌면서 `a_ids` 에 넣어버려, `ended` 검사가
있는 C 루프에 **도달 자체를 못 한다.**

**실측 (유성빌딩 212-04-59010, 4~8월 전액취소)**

| 설정 | 결과 |
|---|---|
| `until` 없음 | `A. 발행 후 전액취소 · 확인 필요` |
| `until: 2026-08` | `A. 발행 후 전액취소 · 확인 필요` — **변화 없음** |
| `until: 2026-03` (취소 시작 전) | `A. 발행 후 전액취소 · 확인 필요` — **변화 없음** |
| `vendors.json` 에서 제거 | 미수취목록에서 사라짐. 대상외공급자 시트로 이동 |

즉 **`until` 로는 뺄 방법이 없고, 목록에서 지우는 것이 유일한 수단이다.**
#28 과 같은 뿌리다 — A 경로가 `vendors.json` 의 운영자 판단을 안 본다.

### 남는 문제 — 지워도 매번 다시 물어본다

목록에서 지우면 `대상외공급자` 시트에 `추가 권장 (정기성)` 으로 뜨고
`_print_reco()`(`build_report.py` 602-607)가 콘솔에도 찍는다.
SKILL.md 269-271행은 "추가 권장이 붙으면 vendors.json 에 추가할지 사용자에게
물어보라" 고 지시한다. **의도적으로 뺀 거래처를 매 회차 다시 넣으라고 권하게 된다.**
`config` 에 제외 목록이 없다 — `thresholds.unlisted_recommend_*` 만 있다.

### 수정 방향 (다음 회차)

| 안 | 내용 |
|---|---|
| 가 | `f["ended"]` 검사를 A 루프 맨 앞으로 올린다. `until` 안내가 문서대로 작동하게 된다 |
| 나 | `_one()` 에서 `out_of_scope` 를 행이 있는 달에도 적용해 `cancelled` 에 담지 않는다 |
| 다 | `vendors.json` 에 `"ignore": true` 또는 config 에 제외 목록을 두고, 판정과 `_print_reco` 양쪽에서 존중한다 |

**가+다 조합이 유력하다.** 가만 하면 '추가 권장' 재권유가 남고,
다만 하면 `until` 안내가 여전히 거짓말을 한다.

### 이번 회차의 운영 결정 — 유성빌딩

**212-04-59010 유성빌딩을 `vendors.json` 에서 제거했다 (31곳 → 30곳).**
사용자가 "이대로 종료되는 곳, 더 이상 언급하지 말 것" 으로 확정했다.
4~8월 취소분 재발행은 없다.

> **다음 회차 주의.** 대상외공급자 시트와 콘솔에 유성빌딩이
> `추가 권장 (정기성) · 6,000,000원` 으로 계속 뜬다. **의도적 제외이므로
> vendors.json 에 다시 추가할지 사용자에게 묻지 말 것.** 위 결함 #29 의
> '다' 안이 반영되기 전까지는 이 문단이 유일한 방지 장치다.

### 결함 #27 의 예외 절차를 처음으로 실제로 밟았다

거래처를 지운 회차라 `push.py` 의 이력 역행 가드가 걸렸다.

```
[중단] 같은 날짜(2026-09-06)인데 확인 필요가 4건 → 3건 으로 줄어듭니다
```

SKILL.md 230-231행은 이때 **재 sync 를 권한다.** 이번엔 그 안내가 통하지 않는다.
감소 원인이 낡은 폴더가 아니라 **의도한 거래처 제거**이기 때문이다.
4차에서도 같은 벽에 부딪혔고 그때 결함 #27 로 남겼던 바로 그 상황이다.

실제로 밟은 절차(#27 이 제안한 3단계 그대로):

1. 원격 `state/last-run.json` 을 codeload 로 직접 받아 로컬과 대조
2. 줄어든 1건이 **유성빌딩 단독**이고 나머지 3곳(광개토·비앤지·다연유통)은
   그대로임을 확인 — 정당한 감소
3. 사용자에게 근거를 제시하고 **승인 받은 뒤** `--force`

**#27 의 수정 방향이 실사용으로 검증됐다.** 다음 회차에 SKILL.md 226-231행에
이 3단계를 명시하고, `push.py` 가드 메시지에도 "거래처를 의도적으로 제거한
경우" 를 한 줄 넣을 것. 지금 문구는 재 sync 만 안내해서 막다른 길로 보낸다.

### 제거 직후 validate 가 FAIL 을 냈다 — 결함 #30

목록에서 지운 회차에 `validate.py` 가 **FAIL 1** 을 냈다.

```
[FAIL] 등급 분류 이상 1건
       22행: vendors.json 에 없는 공급자 2120459010
```

직전 이력에 `확인 필요` 로 남아 있던 거래처를 `vendors.json` 에서 지우면,
`apply_state`(`build_report.py` 265-276)가 **`해결` 행을 하나 만든다.**
그 행의 공급자는 이미 목록에 없으므로 `check_grades` 의 "vendors.json 에 있는가"
검사에 걸린다. 즉 **정상적인 거래처 제거 절차가 곧바로 FAIL 을 유발한다.**

내용상으로도 틀렸다. 유성빌딩은 해결된 게 아니라 **추적을 그만둔 것**인데
리포트가 `해결` 이라고 말한다.

**이번 회차 조치**: 이력(`state/last-run.json`)의 `flagged` 에서 유성빌딩을
뺀 뒤 재생성했다. `해결 0 · FAIL 0 · PASS 17 · SKIP 1` 로 복귀.
근본 수정은 다음 회차 — `apply_state` 가 **목록에서 사라진 공급자는
`해결` 로 만들지 않게** 하고(제거와 해결은 다른 사건이다),
`check_grades` 는 `해결` 등급 행에 한해 미등록을 허용해야 한다.

| # | 심각도 | 파일 | 줄 |
|---|---|---|---|
| 30 | 중간 | `build_report.py` / `validate.py` | 265-276 / `check_grades` 의 미등록 검사 |

---

## 다음 점검에서 대조할 것

1. **#5 를 고친 뒤 1월 실행이 여전히 FAIL 0 인가.** `prev` 를 전년 12월로 바꾸면
   `기한 전 0건` 이 FAIL 로 뒤집힐 수 있다. 1월 실행은 구조상 `기한 전` 이 0 이
   정상이므로(수취 0건 거래처는 C 루프에 들어오지 않음) 판정 조건도 함께 봐야 함
2. **`check_resolved` 가 다음 실사용 실행에서도 PASS 인가.** 이번에 픽스처로만
   두 경로를 밟았다. 실제 홈택스 자료에서 `상태열만 N` 이 0 이 아닌 회차가
   나오면, 그때 콘솔 '해결 N' 과 숫자가 같은지 눈으로 대조할 것
3. **단일 출처 검사 확대의 부작용.** 문서 6개를 훑게 되어 오탐이 늘 수 있다.
   `audit/` 를 제외한 판단이 맞았는지, 새 문서를 추가할 때 걸리는 게 없는지 확인
4. **실측 못 한 것: `push.py --dry-run` 의 `main()` 전체 흐름은 이번에 실측됨**
   (dry-run 2회 + 실제 push 2회). 남은 미실측은 **테스트 실패 시 실제 push 차단**
   경로 — `run_tests()` 만 함수 단위로 확인했고, `main()` 안에서 게이트가
   업로드를 막는 것은 이번에도 안 밟았다
5. **#18 을 고칠지 말지 결정.** 154-155행에 의도 주석이 있어 '결함' 인지
   '설계' 인지가 갈린다. 두 회차 연속 미룬 항목이다
6. **#28 의 방향(가/나/다)을 먼저 정하고 코드를 만진다.** 사용자가 다음 회차로
   미룬 항목이다. `check_input` 의 cycle WARN 과 `build_report` A 경로가 같은
   기준을 쓰게 하는 게 핵심이고, 고치면 `t_` 회귀 테스트가 함께 필요하다
   (`비정기` 라벨 + 수취 6개월 케이스가 지금 테스트에 없다)

> **6차 실사용 실행 실측 (2026-09-06, 홈택스 실자료 441건).**
> 확인 필요 4 · 기한 전 6 · 단발 1 · 정상 3 · 거래 종료 4 · 해결 0 ·
> 상계 6쌍 · 매출분 제외 0 · `check_input` FAIL 0 / WARN 2 ·
> `validate` FAIL 0 · SKIP 1 · PASS 17.
> 위 2번(`check_resolved` 실사용 대조)은 **이번에도 못 밟았다** — 해결 0건이라
> `해결 집계` 가 SKIP 이다. 여전히 픽스처로만 확인된 상태다.
