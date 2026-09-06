# hometax-invoice-check

홈택스 매입 전자세금계산서·전자계산서 목록에서 **거래처가 안 보낸 건**을 찾는 Claude 스킬.

이 저장소는 스킬의 **코드·설정·거래처 목록·실행 이력**을 보관한다.
Claude 쪽에는 `SKILL.md` 하나만 설치하고, 실행할 때마다 여기서 최신본을 받아 쓴다.
그래서 어느 컴퓨터에서 실행해도 같은 거래처 목록과 이력을 쓴다.

## 설치

1. 이 저장소를 **공개(public)** 로 둔다. (읽기에 토큰이 필요 없게)
2. Claude 스킬 폴더에 `SKILL.md` 만 넣는다. 저장소에도 같은 파일의 사본이 있어
   버전이 남는다. 고칠 때는 **저장소와 설치 경로 두 곳 다** 반영해야 한다.
3. 끝. 나머지는 실행할 때 codeload tarball 로 받아온다.

> `raw.githubusercontent.com` 은 5분간 캐시되므로 쓰지 않는다.
> push 직후 다시 받으면 옛 파일이 내려온다. codeload 는 캐시되지 않는다.

## 수동 실행

```bash
mkdir -p ~/hometax && cd ~/hometax
curl -sL https://codeload.github.com/LeeKwanBeom/hometax-invoice-check/tar.gz/refs/heads/main | tar xz --strip-components=1
pip install xlrd            # 홈택스 .xls 를 읽는 데 필요

python3 scripts/check_input.py <홈택스파일폴더>
python3 scripts/build_report.py --uploads <홈택스파일폴더> --out <출력폴더>
python3 scripts/validate.py <출력폴더>/*.xlsx --uploads <홈택스파일폴더>
```

`build_report.py` 에 `--as-of` / `--strict` 를 줬다면 `validate.py` 에도 똑같이 준다.

## 쓰기 권한이 필요한 것

`config/vendors.json`(거래처 목록), `state/last-run.json`(실행 이력),
그리고 대화 중에 고친 코드는 저장소에 되돌려 올려야 남는다.

```bash
python3 scripts/push.py <토큰>          # 이력·거래처
python3 scripts/push.py <토큰> --code   # 코드까지
```

토큰: Settings → Developer settings → Fine-grained tokens,
이 저장소에 **Contents: Read and write**.
**토큰은 저장소에 커밋하지 않는다.**

## 고친 뒤에는

```bash
python3 tests/test_edge_cases.py
python3 scripts/push.py <토큰> --code
```

`push.py --code` 는 테스트를 먼저 돌리고 **실패하면 올리지 않는다.**

## 문서

- `references/column-mapping.md` — 홈택스 파일 읽는 법과 그 이유
- `references/judgment-rules.md` — 등급 판정 논리
- `references/excel-format.md` — 산출물 서식 규격
